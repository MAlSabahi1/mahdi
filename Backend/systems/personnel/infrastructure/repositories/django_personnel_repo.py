"""
Infrastructure Repository: Personnel (Django ORM)
═════════════════════════════════════════════════
تطبيق المستودع الفعلي باستخدام Django ORM.
"""
from typing import Optional

from ...domain.entities.personnel import PersonnelEntity
from ...domain.repositories.i_personnel_repo import IPersonnelRepository
from systems.personnel.models import PersonnelMaster


class DjangoPersonnelRepository(IPersonnelRepository):
    
    def _to_entity(self, model: PersonnelMaster) -> PersonnelEntity:
        return PersonnelEntity(
            military_number=model.military_number,
            full_name=model.full_name,
            current_rank_id=model.current_rank_id,
            current_status_id=model.current_status_id,
            security_admin_id=model.security_admin_id,
            
            old_military_number=model.old_military_number,
            national_id=model.national_id,
            
            birth_date=model.birth_date,
            join_date=model.join_date,
            phone_number=model.phone_number,
            
            central_department_id=model.central_department_id,
            branch_id=model.branch_id,
            district_police_id=model.district_police_id,
            division_id=model.division_id,
            unit_id=model.unit_id,
            
            category_id=model.category_id,
            job_title_id=model.job_title_id,
            position_id=model.position_id,
            force_classification_id=model.force_classification_id,
            
            is_complete=model.is_complete,
            is_data_clean=model.is_data_clean,
            data_quality_score=model.data_quality_score,
            is_deleted=model.is_deleted,
        )

    def _to_model(self, entity: PersonnelEntity) -> PersonnelMaster:
        return PersonnelMaster(
            military_number=entity.military_number,
            full_name=entity.full_name,
            current_rank_id=entity.current_rank_id,
            current_status_id=entity.current_status_id,
            security_admin_id=entity.security_admin_id,
            
            old_military_number=entity.old_military_number,
            national_id=entity.national_id,
            
            birth_date=entity.birth_date,
            join_date=entity.join_date,
            phone_number=entity.phone_number,
            
            central_department_id=entity.central_department_id,
            branch_id=entity.branch_id,
            district_police_id=entity.district_police_id,
            division_id=entity.division_id,
            unit_id=entity.unit_id,
            
            category_id=entity.category_id,
            job_title_id=entity.job_title_id,
            position_id=entity.position_id,
            force_classification_id=entity.force_classification_id,
            
            is_complete=entity.is_complete,
            is_data_clean=entity.is_data_clean,
            data_quality_score=entity.data_quality_score,
            is_deleted=entity.is_deleted,
        )

    def get_by_military_number(self, military_number: str) -> Optional[PersonnelEntity]:
        try:
            model = PersonnelMaster.objects.get(military_number=military_number, is_deleted=False)
            return self._to_entity(model)
        except PersonnelMaster.DoesNotExist:
            return None

    def get_by_national_id(self, national_id: str) -> Optional[PersonnelEntity]:
        try:
            model = PersonnelMaster.objects.get(national_id=national_id, is_deleted=False)
            return self._to_entity(model)
        except PersonnelMaster.DoesNotExist:
            return None

    def save(self, personnel: PersonnelEntity) -> None:
        model = self._to_model(personnel)
        # Using save ensures signals and triggers are executed if any
        model.save()

    def soft_delete(self, military_number: str) -> None:
        try:
            model = PersonnelMaster.objects.get(military_number=military_number)
            model.delete() # Soft delete if SoftDeletableModel overrides delete()
        except PersonnelMaster.DoesNotExist:
            pass
