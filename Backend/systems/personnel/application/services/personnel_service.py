"""
Personnel Services - خدمات الأفراد المتكاملة
═══════════════════════════════════════════════
كل عملية تمر عبر هذه الخدمة لضمان:
1. المعاملات الذرية (atomic transactions)
2. تسجيل التدقيق (AuditLog)
3. تسجيل الأحداث (ServiceEventLog)
4. ربط المرفقات (AttachmentService)
5. التحقق من الصلاحيات
"""
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import date

from systems.personnel.infrastructure.models.personnel_models import PersonnelMaster, SuggestedCorrection, RankSettlement
from systems.services.models import ServiceEventLog
from infra.audit.models import AuditLog


class PersonnelService:
    """
    خدمات الأفراد — نقطة الدخول الوحيدة لكل عمليات التعديل.
    لا يُسمح بتعديل PersonnelMaster مباشرة من Views.
    """

    # ════════════════════════════════════════════════════
    # 1. إنشاء وتحديث أساسي
    # ════════════════════════════════════════════════════

    @staticmethod
    @transaction.atomic
    def create_personnel(data, user=None):
        """إنشاء فرد جديد باستخدام Clean Architecture"""
        from systems.personnel.infrastructure.repositories.django_personnel_repo import DjangoPersonnelRepository
        from systems.personnel.application.use_cases.personnel_use_cases import (
            RegisterPersonnelUseCase, RegisterPersonnelCommand
        )

        repo = DjangoPersonnelRepository()
        uc = RegisterPersonnelUseCase(repo)

        def get_id(field_name):
            val = data.get(field_name)
            return val.id if val and hasattr(val, 'id') else val

        cmd = RegisterPersonnelCommand(
            military_number=data.get('military_number'),
            full_name=data.get('full_name'),
            current_rank_id=get_id('current_rank'),
            current_status_id=get_id('current_status'),
            security_admin_id=get_id('security_admin'),
            
            national_id=data.get('national_id'),
            birth_date=data.get('birth_date'),
            join_date=data.get('join_date'),
            phone_number=data.get('phone_number'),
            
            central_department_id=get_id('central_department'),
            branch_id=get_id('branch'),
            district_police_id=get_id('district_police'),
            division_id=get_id('division'),
            unit_id=get_id('unit'),
            
            category_id=get_id('category'),
            job_title_id=get_id('job_title'),
            position_id=get_id('position'),
            force_classification_id=get_id('force_classification')
        )

        personnel_entity = uc.execute(cmd)
        
        # We need to return the Django Model instance for DRF to serialize it correctly
        created_model = PersonnelMaster.objects.get(military_number=personnel_entity.military_number)

        AuditLog.objects.create(
            user=user,
            action='CREATE',
            model_name='PersonnelMaster',
            object_id=created_model.military_number,
            new_data={k: str(v) for k, v in data.items()},
        )
        return created_model

    @staticmethod
    @transaction.atomic
    def update_personnel(personnel, data, user=None, ip_address=None):
        """تحديث بيانات فرد مع حفظ التاريخ"""
        old_data = {}
        for key in data:
            if hasattr(personnel, key):
                old_val = getattr(personnel, key)
                old_data[key] = str(old_val) if old_val is not None else None

        for key, value in data.items():
            if hasattr(personnel, key):
                setattr(personnel, key, value)

        personnel.full_clean()
        personnel.save()

        AuditLog.objects.create(
            user=user,
            action='UPDATE',
            model_name='PersonnelMaster',
            object_id=personnel.military_number,
            old_data=old_data,
            new_data={k: str(v) for k, v in data.items()},
            ip_address=ip_address,
        )
        return personnel

    # ════════════════════════════════════════════════════
    # 2. سيناريو الرقم الوطني الكامل
    # ════════════════════════════════════════════════════

    @staticmethod
    def check_national_id(value, exclude_military_number=None):
        """
        فحص فوري: هل الرقم الوطني صالح وغير مكرر؟
        يُستخدم في Frontend للتحقق اللحظي أثناء الكتابة.

        Returns: dict {valid_format, exists, owner?}
        """
        result = {'valid_format': False, 'exists': False, 'owner': None}

        if not value or not value.strip():
            return result

        cleaned = value.strip()
        if not cleaned.isdigit() or len(cleaned) != 11:
            return result

        result['valid_format'] = True

        qs = PersonnelMaster.objects.filter(national_id=cleaned)
        if exclude_military_number:
            qs = qs.exclude(military_number=exclude_military_number)

        match = qs.select_related('current_rank').first()
        if match:
            result['exists'] = True
            result['owner'] = {
                'full_name': match.full_name,
                'military_number': match.military_number,
                'rank': match.current_rank.name if match.current_rank else None,
            }

        return result

    @staticmethod
    def check_military_number(value, exclude_military_number=None):
        """
        فحص فوري: هل الرقم العسكري صالح ومتاح وغير مكرر؟
        Returns: dict {valid_format, exists, owner?, pending_settlement?, pending_correction?}
        """
        result = {'valid_format': False, 'exists': False, 'owner': None, 'pending_settlement': False, 'pending_correction': False}

        if not value or not value.strip():
            return result

        cleaned = value.strip()
        if not cleaned.isdigit() or len(cleaned) != 7 or cleaned.startswith('0'):
            return result

        result['valid_format'] = True

        # 1. Check in PersonnelMaster
        qs = PersonnelMaster.objects.filter(military_number=cleaned)
        if exclude_military_number:
            qs = qs.exclude(military_number=exclude_military_number)

        match = qs.select_related('current_rank').first()
        if match:
            result['exists'] = True
            result['owner'] = {
                'full_name': match.full_name,
                'military_number': match.military_number,
                'rank': match.current_rank.name if match.current_rank else None,
            }
            return result

        # 2. Check pending rank settlements
        pending_settlement = RankSettlement.objects.filter(
            new_military_number=cleaned,
            status='pending'
        ).first()
        if pending_settlement:
            result['pending_settlement'] = True
            result['owner'] = {
                'full_name': pending_settlement.personnel.full_name if pending_settlement.personnel else '',
                'military_number': pending_settlement.personnel.military_number if pending_settlement.personnel else '',
            }
            return result

        # 3. Check pending corrections
        pending_correction = SuggestedCorrection.objects.filter(
            field_name='military_number',
            new_value=cleaned,
            status='pending'
        ).first()
        if pending_correction:
            result['pending_correction'] = True
            result['owner'] = {
                'full_name': pending_correction.personnel.full_name if pending_correction.personnel else '',
                'military_number': pending_correction.personnel.military_number if pending_correction.personnel else '',
            }
            return result

        return result

    @staticmethod
    @transaction.atomic
    def update_national_id(personnel, new_national_id, document_ids,
                           user=None, ip_address=None):
        """
        تحديث الرقم الوطني — للمسؤولين فقط (رئيس الخدمات / مدير).
        المرجع: بعض الوصوف للرقم الوطني.md

        القواعد:
        - 11 رقماً بالضبط
        - لا تكرار (UNIQUE)
        - مرفق إلزامي (صورة البطاقة أمام + خلف)
        - تسجيل في AuditLog + ServiceEventLog
        """
        from systems.services.attachment_service import AttachmentService

        # 1. التحقق من الشكل
        if not new_national_id or not new_national_id.isdigit() or len(new_national_id) != 11:
            raise ValidationError(
                _('الرقم الوطني يجب أن يكون 11 رقماً بالضبط')
            )

        # 2. التحقق من التكرار
        duplicate = PersonnelMaster.objects.filter(
            national_id=new_national_id
        ).exclude(military_number=personnel.military_number).first()
        if duplicate:
            raise ValidationError(
                _('الرقم الوطني مرتبط بالفرد: %(name)s (%(mil)s)') % {
                    'name': duplicate.full_name,
                    'mil': duplicate.military_number,
                }
            )

        # 3. التحقق من المرفقات
        if not document_ids:
            raise ValidationError(
                _('يجب إرفاق صورة البطاقة الوطنية (أمام + خلف)')
            )

        validation = AttachmentService.validate_requirements(
            context_type='NationalIdUpdate',
            document_ids=document_ids,
        )
        if not validation['valid']:
            raise ValidationError(
                _('المرفقات غير مكتملة: %(errors)s') % {
                    'errors': '، '.join(validation.get('errors', []))
                }
            )

        # 4. تحديث البيانات
        old_national_id = personnel.national_id or ''
        personnel.national_id = new_national_id
        personnel.save(update_fields=['national_id', 'updated_at'])

        # 5. ربط المرفقات
        AttachmentService.link_to_context(
            document_ids=document_ids,
            context_type='NationalIdUpdate',
            context_id=personnel.military_number,
            related_field='national_id',
            personnel=personnel,
        )
        AttachmentService.commit_documents(document_ids)

        # 6. سجل الأحداث
        ServiceEventLog.objects.create(
            personnel=personnel,
            security_admin=personnel.security_admin,
            event_date=date.today(),
            service_month=date.today().strftime('%Y-%m'),
            field_name='national_id',
            old_value=old_national_id,
            new_value=new_national_id,
            created_by=user,
        )

        # 7. سجل التدقيق
        AuditLog.objects.create(
            user=user,
            action='UPDATE',
            model_name='PersonnelMaster',
            object_id=personnel.military_number,
            old_data={'national_id': old_national_id},
            new_data={
                'national_id': new_national_id,
                'document_ids': document_ids,
                'action_type': 'direct_national_id_update',
            },
            ip_address=ip_address,
        )

        return personnel

    @staticmethod
    @transaction.atomic
    def request_national_id_correction(personnel, new_national_id,
                                       document_ids, user=None, ip_address=None):
        """
        طلب تصحيح رقم وطني — للمستخدمين العاديين.
        يُنشئ SuggestedCorrection بانتظار موافقة رئيس الخدمات.
        """
        from systems.services.attachment_service import AttachmentService
        from infra.storage.models import Document

        # التحقق من الشكل
        if not new_national_id or not new_national_id.isdigit() or len(new_national_id) != 11:
            raise ValidationError(_('الرقم الوطني يجب أن يكون 11 رقماً'))

        # التحقق من التكرار
        duplicate = PersonnelMaster.objects.filter(
            national_id=new_national_id
        ).exclude(military_number=personnel.military_number).first()
        if duplicate:
            raise ValidationError(
                _('الرقم الوطني مرتبط بالفرد: %(name)s (%(mil)s)') % {
                    'name': duplicate.full_name, 'mil': duplicate.military_number
                }
            )

        # التحقق من المرفقات
        if not document_ids:
            raise ValidationError(_('يجب إرفاق صورة البطاقة الوطنية'))

        docs = list(Document.objects.filter(id__in=document_ids))
        if len(docs) != len(document_ids):
            raise ValidationError(_('بعض المرفقات غير موجودة'))

        # إنشاء طلب التصحيح
        correction = SuggestedCorrection.objects.create(
            personnel=personnel,
            security_admin=personnel.security_admin,
            field_name='national_id',
            old_value=personnel.national_id or '',
            new_value=new_national_id,
            correction_type='national_id_correction',
            status='pending',
            supporting_document=docs[0] if docs else None,
            requested_by=user,
        )

        # ربط المرفقات
        AttachmentService.link_to_context(
            document_ids=document_ids,
            context_type='SuggestedCorrection',
            context_id=correction.pk,
            related_field='national_id',
            personnel=personnel,
        )

        # سجل التدقيق
        AuditLog.objects.create(
            user=user,
            action='CREATE',
            model_name='SuggestedCorrection',
            object_id=str(correction.pk),
            new_data={
                'personnel': personnel.military_number,
                'field': 'national_id',
                'new_value': new_national_id,
                'action_type': 'national_id_correction_request',
            },
            ip_address=ip_address,
        )

        return correction

    # ════════════════════════════════════════════════════
    # 3. سيناريو تصحيح الاسم الكامل
    # ════════════════════════════════════════════════════

    @staticmethod
    @transaction.atomic
    def correct_name(personnel, new_name, document=None,
                     document_ids=None, user=None):
        """
        تصحيح اسم فرد — الاعتماد النهائي بعد موافقة الوزارة.

        السيناريو:
        1. يُخزن الاسم القديم في AuditLog
        2. يُحدث full_name بالاسم الجديد مباشرة
        3. يُثبّت المرفقات عبر AttachmentService
        4. يُسجل الحدث في ServiceEventLog

        ملاحظة: لا يوجد حقل corrected_name بعد الآن.
        طلبات التصحيح تُدار حصراً عبر جدول SuggestedCorrection.
        """
        from systems.services.attachment_service import AttachmentService

        old_name = personnel.full_name

        personnel.full_name = new_name
        personnel.save(update_fields=['full_name', 'updated_at'])

        # تثبيت المرفقات
        if document_ids:
            AttachmentService.commit_documents(document_ids)
        elif document:
            AttachmentService.commit_documents([document.id])

        # سجل الحدث
        ServiceEventLog.objects.create(
            personnel=personnel,
            security_admin=personnel.security_admin,
            event_date=date.today(),
            service_month=date.today().strftime('%Y-%m'),
            field_name='full_name',
            old_value=old_name,
            new_value=new_name,
            order_document=document,
            created_by=user,
        )

        AuditLog.objects.create(
            user=user,
            action='UPDATE',
            model_name='PersonnelMaster',
            object_id=personnel.military_number,
            old_data={'name': old_name},
            new_data={'name': new_name},
        )
        return personnel

    @staticmethod
    @transaction.atomic
    def submit_name_corrections_batch(corrections_data, document_ids=None, user=None):
        """
        رفع تصحيحات أسماء جماعية — نموذج 23.
        المرجع: الدليل الإرشادي البند 8 — الاسم الرباعي مع اللقب.

        ═══════════════════════════════════════════════════════
        قواعد الأمان:
        1. المرفق إلزامي (صورة البطاقة أو الوثيقة الداعمة).
        2. كل طلب يمر عبر SuggestedCorrection.full_clean().
        3. AuditLog يُسجّل الدفعة بالكامل كعملية واحدة.
        4. لا يُعدّل PersonnelMaster مباشرة — ينتظر موافقة رئيس القسم.
        ═══════════════════════════════════════════════════════

        Input:
            corrections_data: [{'military_number': '7348799', 'new_name': 'أحمد ...'}, ...]
            document_ids: [uuid, uuid, ...] — إلزامي لتصحيح الأسماء
        """
        from infra.storage.models import Document

        # ═══ 1. التحقق الإلزامي من المرفقات ═══
        if not document_ids:
            raise ValidationError(
                _('يجب إرفاق ملف داعم لتصحيح الأسماء (صورة البطاقة أو نموذج 23). '
                  'المرجع: الدليل الإرشادي البند 8.')
            )

        docs = list(Document.objects.filter(id__in=document_ids))
        if len(docs) != len(document_ids):
            raise ValidationError(_('بعض المرفقات غير موجودة في قاعدة البيانات.'))

        primary_doc = docs[0]

        # TODO: Generate PDF Form 23 here
        # form23_doc = Form23Generator.generate(corrections_data, requested_by=user)
        # primary_doc = form23_doc  (سيُستبدل بمستند مولّد تلقائياً)

        # ═══ 2. معالجة كل طلب ═══
        created = []
        errors = []

        for item in corrections_data:
            mil = str(item.get('military_number', '')).strip()
            new_name = item.get('new_name', '').strip()

            if not mil or not new_name:
                errors.append({'military_number': mil, 'error': 'بيانات ناقصة (الرقم العسكري أو الاسم)'})
                continue

            try:
                p = PersonnelMaster.objects.select_related(
                    'security_admin'
                ).get(military_number=mil)
            except PersonnelMaster.DoesNotExist:
                errors.append({'military_number': mil, 'error': 'الفرد غير موجود'})
                continue

            if p.is_deleted:
                errors.append({'military_number': mil, 'error': 'الفرد محذوف من النظام'})
                continue

            # التحقق من وجود طلب معلق بالفعل
            existing_pending = SuggestedCorrection.objects.filter(
                personnel=p,
                correction_type='name_correction',
                status='pending',
            ).exists()
            if existing_pending:
                errors.append({
                    'military_number': mil,
                    'error': 'يوجد طلب تصحيح اسم معلق بالفعل — انتظر البت فيه أولاً',
                })
                continue

            # إنشاء طلب التصحيح عبر SuggestedCorrection — لا تعديل مباشر للفرد
            correction = SuggestedCorrection(
                personnel=p,
                security_admin=p.security_admin,
                field_name='full_name',
                old_value=p.full_name,
                new_value=new_name,
                correction_type='name_correction',
                status='pending',
                supporting_document=primary_doc,
                requested_by=user,
            )
            # full_clean() يُطبّق قواعد النموذج (DOCUMENT_REQUIREMENTS، تجميد المعتمدة...)
            correction.full_clean()
            correction.save()

            created.append({
                'correction_id': correction.pk,
                'military_number': mil,
                'old_name': p.full_name,
                'new_name': new_name,
            })

        # ═══ 3. AuditLog للدفعة ═══
        if created:
            AuditLog.objects.create(
                user=user,
                action='BATCH_CREATE',
                model_name='SuggestedCorrection',
                object_id='batch',
                new_data={
                    'action_type': 'name_correction_batch',
                    'total_submitted': len(corrections_data),
                    'created_count': len(created),
                    'error_count': len(errors),
                    'document_ids': [str(d) for d in document_ids],
                    'military_numbers': [c['military_number'] for c in created],
                },
                severity='medium',
                module='personnel',
                change_reason=f'دفعة تصحيح أسماء — {len(created)} طلب',
            )

        return {'created': created, 'errors': errors}


    @staticmethod
    @transaction.atomic
    def bulk_approve_corrections(correction_ids, memo_document_ids=None, user=None):
        """
        موافقة جماعية على طلبات التصحيح + رفع مرفق الموافقة (مذكرة الوزارة).
        المرجع: تعليق "تحديد الكل ورفع المرفق"

        السيناريو:
        1. جلب كل الطلبات المعلقة
        2. تطبيق كل تصحيح عبر correct_name()
        3. ربط مرفق الموافقة (مذكرة الوزارة) بالكل في حقل approval_document
        """
        from systems.services.attachment_service import AttachmentService
        from infra.storage.models import Document

        if not memo_document_ids:
            raise ValidationError(_("يجب إرفاق المذكرة الوزارية (مستند الموافقة) لاعتماد هذه الطلبات."))

        memo_docs = list(Document.objects.filter(id__in=memo_document_ids))
        if len(memo_docs) != len(memo_document_ids):
            raise ValidationError(_('بعض مستندات الموافقة غير موجودة في قاعدة البيانات.'))
            
        primary_memo = memo_docs[0]

        corrections = SuggestedCorrection.objects.filter(
            id__in=correction_ids,
            status='pending',
        ).select_related('personnel', 'personnel__security_admin')

        approved = []
        errors = []

        for correction in corrections:
            try:
                if not correction.personnel:
                    errors.append({
                        'correction_id': correction.pk,
                        'error': 'لا يوجد فرد مرتبط'
                    })
                    continue

                # تطبيق التصحيح
                if correction.field_name == 'full_name':
                    PersonnelService.correct_name(
                        correction.personnel,
                        correction.new_value,
                        document_ids=memo_document_ids,
                        user=user,
                    )
                elif correction.field_name == 'national_id':
                    PersonnelService.update_national_id(
                        correction.personnel,
                        correction.new_value,
                        document_ids=memo_document_ids,
                        user=user,
                    )

                # تحديث حالة الطلب وربط مستند الاعتماد
                correction.status = 'approved'
                correction.reviewed_by = user
                correction.reviewed_at = timezone.now()
                correction.approval_document = primary_memo
                correction.save()

                approved.append(correction.pk)

            except Exception as e:
                errors.append({
                    'correction_id': correction.pk,
                    'error': str(e),
                })

        # ربط المرفق المشترك بكل الطلبات لضمان ظهوره في ServiceEventLog أيضاً
        if memo_document_ids and approved:
            for cid in approved:
                AttachmentService.link_to_context(
                    document_ids=memo_document_ids,
                    context_type='SuggestedCorrection',
                    context_id=cid,
                    related_field='approval_document',
                )
            AttachmentService.commit_documents(memo_document_ids)

            # تسجيل الاعتماد الجماعي في AuditLog
            from systems.services.models import AuditLog
            AuditLog.objects.create(
                user=user,
                action='BATCH_APPROVE',
                model_name='SuggestedCorrection',
                object_id='batch',
                new_data={
                    'approved_count': len(approved),
                    'error_count': len(errors),
                    'memo_document_ids': [str(d) for d in memo_document_ids],
                    'correction_ids': approved,
                },
                severity='high',
                module='personnel',
                change_reason=f'موافقة جماعية على تصحيحات الأسماء — {len(approved)} طلب',
            )

        return {
            'approved_count': len(approved),
            'error_count': len(errors),
            'approved_ids': approved,
            'errors': errors,
        }

    @staticmethod
    @transaction.atomic
    def bulk_reject_corrections(correction_ids, reason, user=None, clear_name=False):
        """
        رفض جماعي لطلبات التصحيح.

        المعاملات:
        ──────────
        • correction_ids : قائمة معرّفات الطلبات المراد رفضها.
        • reason         : سبب الرفض (إلزامي — يُسجَّل في rejection_reason).
        • user           : المستخدم الذي نفّذ الرفض.
        • clear_name     : (اختياري — افتراضي False) — محجوز للتوافق مع الـ API
            True  → يُسجَّل في AuditLog أن رفض الوزارة نهائي (الاسم صحيح فعلاً).
            False → الوزارة رفضت لأسباب إجرائية (نقص أوراق) وقد يُعاد التقديم.

        ملاحظة هندسية:
        ──────────────
        لا يوجد حقل corrected_name في قاعدة البيانات بعد الآن.
        هذا البارامتر يُوثَّق فقط في AuditLog كوصف للقرار.
        """
        from systems.services.models import AuditLog

        corrections = SuggestedCorrection.objects.filter(
            id__in=correction_ids,
            status='pending',
        ).select_related('personnel')

        now = timezone.now()
        rejected_ids = []

        for correction in corrections:
            correction.status = 'rejected'
            correction.reviewed_by = user
            correction.reviewed_at = now
            correction.rejection_reason = reason
            correction.save(update_fields=[
                'status', 'reviewed_by', 'reviewed_at', 'rejection_reason'
            ])
            rejected_ids.append(correction.pk)

        # تسجيل العملية في AuditLog للمراجعة المستقبلية
        if rejected_ids:
            AuditLog.objects.create(
                user=user,
                action='BATCH_REJECT',
                model_name='SuggestedCorrection',
                object_id='batch',
                new_data={
                    'rejected_count': len(rejected_ids),
                    'correction_ids': rejected_ids,
                    'reason': reason,
                    'ministry_final_rejection': clear_name,
                },
                severity='medium',
                module='personnel',
                change_reason=f'رفض جماعي — {len(rejected_ids)} طلب',
            )

        return len(rejected_ids)


    # ════════════════════════════════════════════════════
    # 4. نقل الإدارة
    # ════════════════════════════════════════════════════

    @staticmethod
    @transaction.atomic
    def transfer_directorate(
        personnel,
        new_central_department=None,
        new_branch=None,
        new_district_police=None,
        document=None,
        user=None,
    ):
        """
        نقل فرد إلى جهة عمل جديدة — يتطلب أمر نقل رسمي.

        يجب تمرير واحد فقط من الثلاثة:
          - new_central_department  (إدارة مركزية)
          - new_branch              (فرع)
          - new_district_police     (أمن مديرية)

        يُصفّر الحقلين الآخرَين تلقائياً لضمان القاعدة: فرد في جهة واحدة فقط.
        """
        if not document:
            raise ValidationError(_('يجب رفع أمر النقل'))

        # التحقق أن جهة واحدة فقط تم تحديدها
        targets = [new_central_department, new_branch, new_district_police]
        filled = [t for t in targets if t is not None]
        if len(filled) != 1:
            raise ValidationError(
                _('يجب تحديد جهة عمل واحدة فقط: إدارة مركزية أو فرع أو أمن مديرية.')
            )

        # حفظ القيم القديمة للـ Audit
        old_central_department = personnel.central_department
        old_branch = personnel.branch
        old_district_police = personnel.district_police
        old_target = old_central_department or old_branch or old_district_police

        # مسح الجهات القديمة وتعيين الجديدة الوحيدة
        personnel.central_department = new_central_department
        personnel.branch = new_branch
        personnel.district_police = new_district_police
        personnel.save(update_fields=[
            'central_department', 'branch', 'district_police', 'updated_at'
        ])

        new_target = filled[0]

        ServiceEventLog.objects.create(
            personnel=personnel,
            security_admin=personnel.security_admin,
            event_date=date.today(),
            service_month=date.today().strftime('%Y-%m'),
            field_name='work_location',
            old_value=str(old_target) if old_target else '',
            new_value=str(new_target),
            order_document=document,
            created_by=user,
        )

        AuditLog.objects.create(
            user=user,
            action='UPDATE',
            model_name='PersonnelMaster',
            object_id=personnel.military_number,
            old_data={
                'central_department': old_central_department.name if old_central_department else None,
                'branch': old_branch.name if old_branch else None,
                'district_police': old_district_police.name if old_district_police else None,
            },
            new_data={
                'central_department': new_central_department.name if new_central_department else None,
                'branch': new_branch.name if new_branch else None,
                'district_police': new_district_police.name if new_district_police else None,
            },
        )
        return personnel

    # ════════════════════════════════════════════════════
    # 5. ترقية الرتبة
    # ════════════════════════════════════════════════════

    @staticmethod
    @transaction.atomic
    def promote_rank(personnel, new_rank, document=None, user=None):
        """ترقية رتبة فرد — يتطلب مرفق قرار الترقية"""
        if not document:
            raise ValidationError(_('يجب رفع أمر الترقية'))

        old_rank = personnel.current_rank
        # قاعدة الترقيب: order أصغر = رتبة أعلى (1 = أعلى رتبة في النظام)
        # الترقية تعني: new_rank.order < old_rank.order
        # نرفض إذا كان الـ order الجديد مساوياً أو أكبر (رتبة مساوية أو أدنى)
        if new_rank.order >= old_rank.order:
            raise ValidationError(_('الرتبة الجديدة يجب أن تكون أعلى من الحالية (رقم ترتيب أصغر)'))

        personnel.current_rank = new_rank
        personnel.pending_rank = None
        personnel.save(update_fields=['current_rank', 'pending_rank', 'updated_at'])

        ServiceEventLog.objects.create(
            personnel=personnel,
            security_admin=personnel.security_admin,
            event_date=date.today(),
            service_month=date.today().strftime('%Y-%m'),
            field_name='current_rank',
            old_value=str(old_rank),
            new_value=str(new_rank),
            order_document=document,
            created_by=user,
        )

        AuditLog.objects.create(
            user=user,
            action='UPDATE',
            model_name='PersonnelMaster',
            object_id=personnel.military_number,
            old_data={'rank': old_rank.name},
            new_data={'rank': new_rank.name},
        )
        return personnel

    # ════════════════════════════════════════════════════
    # 6. تطبيق تسوية الرتبة (RankSettlement)
    # ════════════════════════════════════════════════════

    @staticmethod
    @transaction.atomic
    def apply_settlement(settlement, user=None, ip_address=None):
        """
        تطبيق طلب تسوية رتبة على PersonnelMaster.
        المرجع: الدليل الإرشادي - البند 17

        سيناريوهات:
        1. same_class_promotion: تغيير current_rank فقط
        2. personnel_to_officer: تغيير rank + military_number
        3. demotion: تخفيض (عقوبة) — يتطلب مرفق القرار
        """
        from systems.services.attachment_service import AttachmentService

        if settlement.status != 'approved':
            raise ValidationError(_('يمكن تطبيق الطلبات الموافق عليها فقط'))

        personnel = settlement.personnel
        old_rank = personnel.current_rank
        old_mil = personnel.military_number

        # تطبيق حسب النوع
        if settlement.settlement_type == 'personnel_to_officer':
            # حفظ الرقم القديم
            personnel.old_military_number = old_mil
            personnel.military_number = settlement.new_military_number
            personnel.current_rank = settlement.to_rank
            personnel.pending_rank = None
            personnel.save()

        elif settlement.settlement_type in ('same_class_promotion', 'demotion'):
            personnel.current_rank = settlement.to_rank
            personnel.pending_rank = None
            personnel.save(update_fields=[
                'current_rank', 'pending_rank', 'updated_at'
            ])

        # تحديث حالة الطلب
        settlement.status = 'applied'
        settlement.applied_by = user
        settlement.applied_at = timezone.now()
        settlement.save()

        # ربط المرفق
        if settlement.supporting_document_id:
            AttachmentService.commit_documents([settlement.supporting_document_id])

        # سجل الأحداث
        ServiceEventLog.objects.create(
            personnel=personnel,
            security_admin=personnel.security_admin,
            event_date=settlement.decision_date or date.today(),
            service_month=date.today().strftime('%Y-%m'),
            field_name='current_rank',
            old_value=str(old_rank),
            new_value=str(settlement.to_rank),
            order_document=settlement.supporting_document,
            created_by=user,
        )

        AuditLog.objects.create(
            user=user,
            action='SETTLEMENT',
            model_name='RankSettlement',
            object_id=str(settlement.pk),
            old_data={
                'rank': old_rank.name if old_rank else None,
                'military_number': old_mil,
            },
            new_data={
                'rank': settlement.to_rank.name,
                'military_number': personnel.military_number,
                'settlement_type': settlement.settlement_type,
                'decision_number': settlement.decision_number,
            },
            ip_address=ip_address,
        )

        return personnel

    # ════════════════════════════════════════════════════
    # 7. Auto-fill: job_title → category تلقائياً
    # ════════════════════════════════════════════════════

    @staticmethod
    def auto_fill_category(personnel):
        """
        عند اختيار job_title → يتم تعبئة category تلقائياً
        من JobTitle.category (FK → JobCategory)
        """
        if personnel.job_title_id and personnel.job_title.category_id:
            personnel.category = personnel.job_title.category
        return personnel

    # ════════════════════════════════════════════════════
    # 8. التصدير الشهري للمتغيرات (EAV Mutation Grid)
    # ════════════════════════════════════════════════════

    @staticmethod
    def generate_monthly_services_export(month: str) -> list[dict]:
        """
        يقوم بجمع البيانات الأساسية للأفراد ودمج المتغير الشهري للشهر المحدد
        وإرجاع قائمة مسطحة (Flat List) جاهزة للتصدير إلى ملف إكسل.
        """
        from .models import PersonnelMaster, HistoricalMonthlyVariables
        from django.db.models import Prefetch

        prefetch = Prefetch(
            'monthly_variables',
            queryset=HistoricalMonthlyVariables.objects.filter(month=month),
            to_attr='prefetched_active_variables'
        )
        
        personnel_qs = PersonnelMaster.objects.select_related(
            'current_rank', 'central_department', 'current_status'
        ).prefetch_related(prefetch)

        export_data = []
        for p in personnel_qs:
            variable_val = ''
            if getattr(p, 'prefetched_active_variables', []):
                variable_val = p.prefetched_active_variables[0].variable_value

            export_data.append({
                'الرقم العسكري': p.military_number,
                'الاسم': p.full_name,
                'الرتبة': p.current_rank.name if p.current_rank else '',
                'الإدارة': p.central_department.name if p.central_department else '',
                'الحالة': p.current_status.name if p.current_status else '',
                f'متغير {month}': variable_val
            })
            
        return export_data
