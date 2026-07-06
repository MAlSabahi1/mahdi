from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import (
    Correspondence, Task, Circular, CorrespondenceAttachment,
    MeetingMinutes, DocumentWorkRequest, InventoryItem, InventoryRequest,
    Custody, AttendanceLog, FinancialAllocation, Expense
)
from .serializers import (
    CorrespondenceSerializer, TaskSerializer, CircularSerializer,
    CorrespondenceAttachmentSerializer, MeetingMinutesSerializer,
    DocumentWorkRequestSerializer, InventoryItemSerializer,
    InventoryRequestSerializer, CustodySerializer, AttendanceLogSerializer,
    FinancialAllocationSerializer, ExpenseSerializer
)
from infra.security.permissions import ABACPermission, filter_by_department_scope, get_user_profile

class BaseSecretariatViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    def get_queryset(self):
        return filter_by_department_scope(
            self.request.user, 
            self.queryset, 
            'security_admin'
        )
        
    def perform_create(self, serializer):
        profile = get_user_profile(self.request.user)
        security_admin = getattr(profile, 'security_admin', None) if profile else None
        if not security_admin:
            from core.models.organization import SecurityAdministration
            security_admin = SecurityAdministration.objects.first()
        serializer.save(
            created_by=self.request.user,
            security_admin=security_admin
        )

class CorrespondenceViewSet(BaseSecretariatViewSet):
    queryset = Correspondence.objects.all()
    serializer_class = CorrespondenceSerializer
    filterset_fields = ['type', 'status', 'date']
    search_fields = ['reference_number', 'subject', 'sender', 'receiver']
    ordering_fields = ['date', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset

        from infra.security.permissions import has_permission
        from infra.authorization.registry.permissions import Perms

        # مدراء السكرتارية يرون الكل (مقيّد بنطاق الإدارة الأمنية)
        if has_permission(user, Perms.SECRETARIAT_VIEW):
            return filter_by_department_scope(user, self.queryset, 'security_admin')

        # الموظف المكلف يرى فقط المراسلات المرتبطة بمهامه
        if has_permission(user, Perms.SECRETARIAT_VIEW_OWN):
            from systems.personnel.models import PersonnelMaster
            try:
                personnel = PersonnelMaster.objects.get(military_number=user.username)
                linked_corr_ids = Task.objects.filter(
                    assigned_to=personnel
                ).values_list('related_correspondence_id', flat=True).distinct()
                return self.queryset.filter(id__in=linked_corr_ids)
            except PersonnelMaster.DoesNotExist:
                return self.queryset.none()

        return self.queryset.none()


class CorrespondenceAttachmentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ABACPermission]
    queryset = CorrespondenceAttachment.objects.all()
    serializer_class = CorrespondenceAttachmentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['correspondence']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        profile = get_user_profile(self.request.user)
        user_sec_admin = getattr(profile, 'security_admin', None) if profile else None
        if user_sec_admin:
            return self.queryset.filter(correspondence__security_admin=user_sec_admin)
        return self.queryset.none()

class TaskViewSet(BaseSecretariatViewSet):
    queryset = Task.objects.select_related('assigned_to').all()
    serializer_class = TaskSerializer
    filterset_fields = ['status', 'priority', 'due_date', 'assigned_to', 'related_correspondence']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at', 'priority']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset

        from infra.security.permissions import has_permission
        from infra.authorization.registry.permissions import Perms

        # السكرتارية ومدراء التكليفات يرون الكل
        if has_permission(user, Perms.SECRETARIAT_TASK_MANAGE):
            return filter_by_department_scope(user, self.queryset, 'security_admin')

        # الموظف المكلف يرى فقط مهامه الخاصة
        if has_permission(user, Perms.SECRETARIAT_TASK_EXECUTE):
            # البحث عن military_number الخاص بالمستخدم
            from systems.personnel.models import PersonnelMaster
            try:
                personnel = PersonnelMaster.objects.get(military_number=user.username)
                return self.queryset.filter(assigned_to=personnel)
            except PersonnelMaster.DoesNotExist:
                return self.queryset.none()

        return self.queryset.none()

    def perform_update(self, serializer):
        user = self.request.user
        task_instance = serializer.instance
        old_status = task_instance.status

        from infra.security.permissions import has_permission
        from infra.authorization.registry.permissions import Perms
        from rest_framework.exceptions import PermissionDenied

        # الموظف المكلف — يستطيع فقط تغيير الحالة (in_progress / completed)
        if not has_permission(user, Perms.SECRETARIAT_TASK_MANAGE):
            allowed_changes = {'status'}
            requested_changes = set(serializer.validated_data.keys())
            if not requested_changes.issubset(allowed_changes):
                raise PermissionDenied('يمكنك فقط تحديث حالة المهمة المسندة إليك')

            new_status = serializer.validated_data.get('status', old_status)
            if old_status == 'pending' and new_status not in ('in_progress',):
                raise PermissionDenied('يمكنك فقط تغيير الحالة من "قيد الانتظار" إلى "جاري العمل"')
            if old_status == 'in_progress' and new_status not in ('completed',):
                raise PermissionDenied('يمكنك فقط تغيير الحالة من "جاري العمل" إلى "مكتملة"')

        instance = serializer.save()
        new_status = instance.status

        # إشعار منشئ التكليف عند تغيير الحالة
        if old_status != new_status and new_status in ('in_progress', 'completed'):
            try:
                from core.models.notification import NotificationRecord
                creator = instance.created_by
                if creator:
                    assignee_name = (
                        instance.assigned_to.full_name
                        if instance.assigned_to else 'الموظف'
                    )
                    corr_ref = (
                        instance.related_correspondence.reference_number
                        if instance.related_correspondence else ''
                    )
                    action_url = (
                        f"/secretariat/correspondences/{instance.related_correspondence.id}"
                        if instance.related_correspondence else "/secretariat/tasks"
                    )
                    if new_status == 'in_progress':
                        title = f"استلام المهمة: {instance.title}"
                        message = (
                            f"قام الموظف {assignee_name} باستلام التكليف «{instance.title}» "
                            f"المرتبط بالمراسلة ({corr_ref}) وبدأ العمل عليه."
                        )
                        priority = 'normal'
                    else:
                        title = f"✅ إنجاز المهمة: {instance.title}"
                        message = (
                            f"أنهى الموظف {assignee_name} تنفيذ التكليف «{instance.title}» "
                            f"المرتبط بالمراسلة ({corr_ref}). يرجى مراجعة النتائج وتوليد خطاب الرد."
                        )
                        priority = 'high'

                    NotificationRecord.objects.create(
                        notification_type='SYSTEM',
                        title=title,
                        message=message,
                        priority=priority,
                        target_user=creator,
                        triggered_by=self.request.user,
                        action_url=action_url,
                        related_object_type='Task',
                        related_object_id=str(instance.pk),
                    )
            except Exception as e:
                import logging
                logging.getLogger('django').error(
                    f"Failed to create task status notification: {e}"
                )

class CircularViewSet(BaseSecretariatViewSet):
    queryset = Circular.objects.all()
    serializer_class = CircularSerializer
    filterset_fields = ['is_active', 'date_issued']
    search_fields = ['title', 'content']
    ordering_fields = ['date_issued', 'created_at']

class MeetingMinutesViewSet(BaseSecretariatViewSet):
    queryset = MeetingMinutes.objects.prefetch_related('attendees').all()
    serializer_class = MeetingMinutesSerializer
    filterset_fields = ['date']
    search_fields = ['title', 'content', 'decisions', 'external_attendees']
    ordering_fields = ['date', 'created_at']

class DocumentWorkRequestViewSet(BaseSecretariatViewSet):
    queryset = DocumentWorkRequest.objects.select_related('requested_by').all()
    serializer_class = DocumentWorkRequestSerializer
    filterset_fields = ['type', 'status', 'requested_by']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'completed_at']

class InventoryItemViewSet(BaseSecretariatViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    filterset_fields = ['type']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'quantity_in_stock']

    def perform_create(self, serializer):
        # override since it does not have created_by
        profile = get_user_profile(self.request.user)
        security_admin = getattr(profile, 'security_admin', None) if profile else None
        if not security_admin:
            from core.models.organization import SecurityAdministration
            security_admin = SecurityAdministration.objects.first()
        serializer.save(security_admin=security_admin)

class InventoryRequestViewSet(BaseSecretariatViewSet):
    queryset = InventoryRequest.objects.select_related('item', 'requested_by').all()
    serializer_class = InventoryRequestSerializer
    filterset_fields = ['status', 'item', 'requested_by']
    search_fields = ['notes']
    ordering_fields = ['created_at']

class CustodyViewSet(BaseSecretariatViewSet):
    queryset = Custody.objects.select_related('item', 'assigned_to').all()
    serializer_class = CustodySerializer
    filterset_fields = ['status', 'item', 'assigned_to']
    search_fields = ['notes']
    ordering_fields = ['date_assigned', 'date_returned']

class AttendanceLogViewSet(BaseSecretariatViewSet):
    queryset = AttendanceLog.objects.select_related('employee').all()
    serializer_class = AttendanceLogSerializer
    filterset_fields = ['date', 'status', 'employee']
    search_fields = ['notes', 'employee__full_name', 'employee__military_number']
    ordering_fields = ['date']

class FinancialAllocationViewSet(BaseSecretariatViewSet):
    queryset = FinancialAllocation.objects.all()
    serializer_class = FinancialAllocationSerializer
    filterset_fields = ['month']
    ordering_fields = ['month']

class ExpenseViewSet(BaseSecretariatViewSet):
    queryset = Expense.objects.select_related('allocation').all()
    serializer_class = ExpenseSerializer
    filterset_fields = ['allocation', 'date', 'category']
    search_fields = ['description', 'receipt_number', 'category']
    ordering_fields = ['date', 'amount']
