"""
Infrastructure Repository: StatusChangeForm (Django ORM)
══════════════════════════════════════════════════════════
تطبيق الـ Repository بـ Django ORM.
يحول بين نموذج Django والـ Domain Entity.
"""
from __future__ import annotations
from typing import Optional, List
from uuid import UUID

from ...domain.entities.status_change_form import StatusChangeFormEntity
from ...domain.repositories.i_status_change_form_repo import IStatusChangeFormRepository
from ...domain.value_objects.status_change import FormStatus, FormType
from ..models.status_change import StatusChangeForm   # Django ORM Model


class DjangoStatusChangeFormRepository(IStatusChangeFormRepository):
    """
    التطبيق الفعلي للـ Repository.
    يُعطى للـ Use Cases عبر Dependency Injection في الـ View.
    """

    def get_by_id(self, form_id: UUID) -> Optional[StatusChangeFormEntity]:
        try:
            model = StatusChangeForm.objects.select_related(
                'personnel', 'security_admin',
                'from_status', 'to_status',
                'submitted_by', 'rejected_by',
            ).get(id=form_id)
            return self._to_entity(model)
        except StatusChangeForm.DoesNotExist:
            return None

    def save(self, entity: StatusChangeFormEntity) -> StatusChangeFormEntity:
        model, _ = StatusChangeForm.objects.update_or_create(
            id=entity.id,
            defaults=self._to_model_data(entity),
        )
        return self._to_entity(model)

    def save_fields(self, entity: StatusChangeFormEntity, fields: List[str]) -> None:
        """
        تحديث حقول محددة فقط — مطابق لـ form.save(update_fields=[...])
        يُحوّل أسماء الـ Entity إلى أسماء Model حيث يختلفان.
        """
        if not entity.id:
            self.save(entity)
            return

        # أسماء الحقول في الـ Entity تنتهي بـ _id لكن في الـ Model بدونها أحياناً
        field_map = {
            'rejected_by':          'rejected_by_id',
            'submitted_by':         'submitted_by_id',
            'current_step':         'current_step_id',
        }
        data = self._to_model_data(entity)
        db_fields = [field_map.get(f, f) for f in fields]

        StatusChangeForm.objects.filter(id=entity.id).update(
            **{f: data[f] for f in db_fields if f in data}
        )

    def list_by_admin(
        self,
        security_admin_id: int,
        status: Optional[FormStatus] = None,
    ) -> List[StatusChangeFormEntity]:
        qs = StatusChangeForm.objects.filter(security_admin_id=security_admin_id)
        if status:
            qs = qs.filter(status=status.value)
        return [self._to_entity(m) for m in qs.order_by('-created_at')]

    def get_personnel_forms(
        self,
        personnel_id: int,
        status: Optional[FormStatus] = None,
    ) -> List[StatusChangeFormEntity]:
        qs = StatusChangeForm.objects.filter(personnel_id=personnel_id)
        if status:
            qs = qs.filter(status=status.value)
        return [self._to_entity(m) for m in qs.order_by('-created_at')]

    # ──────────────────────────────────────────────
    # Private: تحويل Model ↔ Entity
    # ──────────────────────────────────────────────

    def _to_entity(self, m: StatusChangeForm) -> StatusChangeFormEntity:
        return StatusChangeFormEntity(
            id=m.id,
            personnel_id=m.personnel_id,
            security_admin_id=m.security_admin_id,
            form_type=m.form_type,
            submitted_by_id=m.submitted_by_id,
            from_status_id=m.from_status_id,
            to_status_id=m.to_status_id,
            form_data=m.form_data or {},
            effective_date=m.effective_date,
            notes=m.notes or "",
            status=FormStatus(m.status),
            submitted_at=m.submitted_at,
            current_step_id=m.current_step_id,
            workflow_log=m.workflow_log or [],
            rejection_reason=m.rejection_reason or "",
            rejected_by_id=m.rejected_by_id,
            required_attachments=m.required_attachments or [],
            attachments_complete=m.attachments_complete,
        )

    def _to_model_data(self, entity: StatusChangeFormEntity) -> dict:
        return {
            'personnel_id':           entity.personnel_id,
            'security_admin_id':      entity.security_admin_id,
            'form_type':              entity.form_type,
            'submitted_by_id':        entity.submitted_by_id,
            'from_status_id':         entity.from_status_id,
            'to_status_id':           entity.to_status_id,
            'form_data':              entity.form_data,
            'effective_date':         entity.effective_date,
            'notes':                  entity.notes,
            'status':                 entity.status.value,
            'submitted_at':           entity.submitted_at,
            'current_step_id':        entity.current_step_id,
            'workflow_log':           entity.workflow_log,
            'rejection_reason':       entity.rejection_reason,
            'rejected_by_id':         entity.rejected_by_id,
            'attachments_complete':   entity.attachments_complete,
        }
