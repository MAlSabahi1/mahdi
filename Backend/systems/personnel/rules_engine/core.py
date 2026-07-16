from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from django.core.exceptions import ValidationError

class ValidationContext:
    """
    يحمل سياق البيانات لعملية التحقق.
    يُمرر إلى كل قاعدة (Rule) لكي تستطيع قراءة البيانات بشكل موحد.
    """
    def __init__(self, instance):
        self.instance = instance  # PersonnelMaster instance
        self.errors: Dict[str, List[str]] = {}

    def add_error(self, field: str, message: str):
        """إضافة خطأ لحقل معين"""
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)

    def has_errors(self) -> bool:
        """هل يوجد أخطاء؟"""
        return len(self.errors) > 0

    def raise_if_errors(self):
        """إذا كان هناك أخطاء، قم بإطلاق ValidationError لكي يمسكها Django"""
        if self.has_errors():
            raise ValidationError(self.errors)


class BusinessRule(ABC):
    """
    الواجهة الأساسية (Interface) لأي قاعدة أعمال في النظام.
    كل قاعدة يجب أن ترث من هذا الصنف وتطبق دالة execute.
    """
    
    @abstractmethod
    def execute(self, context: ValidationContext) -> None:
        """
        تنفيذ القاعدة على السياق.
        إذا كان هناك خطأ، استدعِ context.add_error(field, message)
        """
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__


class RulesEngine:
    """
    محرك القواعد (Rules Engine).
    يقوم بتسجيل القواعد وتشغيلها بالتسلسل.
    """
    def __init__(self):
        self._rules: List[BusinessRule] = []

    def register_rule(self, rule: BusinessRule):
        """تسجيل قاعدة جديدة في المحرك"""
        self._rules.append(rule)

    def execute_all(self, instance) -> None:
        """
        تشغيل جميع القواعد المسجلة على المثيل (PersonnelMaster).
        يجمع الأخطاء ويطلق ValidationError واحد شامل في النهاية.
        """
        context = ValidationContext(instance)
        
        for rule in self._rules:
            rule.execute(context)
            
        context.raise_if_errors()

    @classmethod
    def get_default(cls):
        """
        مصنع (Factory Method) يعيد محرك محمل مسبقاً بالقواعد الافتراضية
        لكي يسهل استخدامه من داخل Models.
        """
        from .rules import (
            StrictDataConsistencyRule,
            PermanentDeactivationRule,
            RankCategoryCompatibilityRule,
            PositionRequirementsRule,
            MilitaryNumberPrefixRule,
            NoStateOverlapRule,
            AdministrativePositionRule,
            PositionImmutabilityRule,
            UniqueLeadershipPositionRule,
            QualificationCategoryRule
        )
        
        engine = cls()
        # StrictDataConsistencyRule يجب أن تعمل أولاً لمنع حفظ بيانات متناقضة
        engine.register_rule(StrictDataConsistencyRule())
        
        engine.register_rule(PermanentDeactivationRule())
        engine.register_rule(RankCategoryCompatibilityRule())
        engine.register_rule(PositionRequirementsRule())
        engine.register_rule(MilitaryNumberPrefixRule())
        engine.register_rule(AdministrativePositionRule())
        engine.register_rule(PositionImmutabilityRule())
        engine.register_rule(UniqueLeadershipPositionRule())
        engine.register_rule(NoStateOverlapRule())
        engine.register_rule(QualificationCategoryRule())
        return engine
