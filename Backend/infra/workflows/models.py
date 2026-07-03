"""
Enterprise Process Engine (BPMN-like Workflow System)
═══════════════════════════════════════════════════════
محرك عمليات مؤسسي ديناميكي. يعتمد على هندسة (State Machine) و (SLA).
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from core.models import SoftDeletableModel
from infra.authorization.models import Role
from simple_history.models import HistoricalRecords
import uuid

User = get_user_model()


# ── 1. الأساسيات (Workflow & Version) ──

class Workflow(SoftDeletableModel):
    """
    العملية الرئيسية (مثال: طلب إجازة, تصحيح بيانات)
    """
    name = models.CharField(max_length=200, unique=True, verbose_name=_('اسم العملية'))
    code = models.CharField(max_length=50, unique=True, verbose_name=_('رمز العملية'))
    description = models.TextField(blank=True, verbose_name=_('الوصف'))
    
    class Meta:
        db_table = 'workflow_master'
        verbose_name = _('مسار عمل')
        verbose_name_plural = _('مسارات العمل')
        
    def __str__(self):
        return self.name


class WorkflowVersion(SoftDeletableModel):
    """
    إصدار العملية (لضمان عدم انكسار الطلبات القديمة عند تغيير القوانين)
    """
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField(verbose_name=_('رقم الإصدار'))
    is_active = models.BooleanField(default=False, verbose_name=_('نشط حالياً'))
    
    class Meta:
        db_table = 'workflow_version'
        unique_together = [['workflow', 'version_number']]
        verbose_name = _('إصدار المسار')
        verbose_name_plural = _('إصدارات المسارات')

    def __str__(self):
        return f"{self.workflow.name} - V{self.version_number}"

    def save(self, *args, **kwargs):
        if self.is_active:
            # إيقاف الإصدارات الأخرى لنفس الـ Workflow
            WorkflowVersion.objects.filter(workflow=self.workflow).update(is_active=False)
        super().save(*args, **kwargs)


# ── 2. محرك الحالات (States & Transitions) ──

class State(SoftDeletableModel):
    """
    الحالة (Draft, Under Review, Approved...)
    """
    STATE_TYPES = [
        ('draft', _('مسودة')),
        ('review', _('قيد المراجعة')),
        ('approved', _('معتمد')),
        ('rejected', _('مرفوض')),
        ('archived', _('مؤرشف')),
    ]
    version = models.ForeignKey(WorkflowVersion, on_delete=models.CASCADE, related_name='states')
    name = models.CharField(max_length=100, verbose_name=_('اسم الحالة'))
    code = models.CharField(max_length=50, verbose_name=_('رمز الحالة'))
    state_type = models.CharField(max_length=20, choices=STATE_TYPES, default='review', verbose_name=_('نوع الحالة'))
    is_initial = models.BooleanField(default=False, verbose_name=_('حالة البداية'))
    is_final = models.BooleanField(default=False, verbose_name=_('حالة النهاية'))

    class Meta:
        db_table = 'workflow_state'
        unique_together = [['version', 'code']]
        verbose_name = _('حالة')
        verbose_name_plural = _('الحالات')

    def __str__(self):
        return f"{self.name} ({self.version})"


class Transition(SoftDeletableModel):
    """
    الانتقال من حالة إلى أخرى
    """
    version = models.ForeignKey(WorkflowVersion, on_delete=models.CASCADE, related_name='transitions')
    from_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='outgoing_transitions')
    to_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='incoming_transitions')
    name = models.CharField(max_length=100, verbose_name=_('اسم الانتقال (الزر)'))
    
    class Meta:
        db_table = 'workflow_transition'
        unique_together = [['version', 'from_state', 'to_state']]
        verbose_name = _('انتقال')
        verbose_name_plural = _('الانتقالات')

    def __str__(self):
        return f"[{self.name}] {self.from_state.name} → {self.to_state.name}"


class TransitionRule(SoftDeletableModel):
    """
    القواعد الديناميكية للانتقال (JSON Conditions)
    مثال: {"requires_attachment": true, "min_days_in_service": 365}
    """
    transition = models.OneToOneField(Transition, on_delete=models.CASCADE, related_name='rule')
    conditions = models.JSONField(default=dict, blank=True, verbose_name=_('الشروط الديناميكية'))
    
    class Meta:
        db_table = 'workflow_transition_rule'


# ── 3. الموافقات واتفاقية مستوى الخدمة (Approvals & SLA) ──

class ApprovalStep(SoftDeletableModel):
    """
    مرحلة الموافقة. مربوطة بـ Transition.
    """
    transition = models.ForeignKey(Transition, on_delete=models.CASCADE, related_name='approval_steps')
    required_role = models.ForeignKey(Role, on_delete=models.PROTECT, verbose_name=_('الدور المطلوب'))
    min_approvals = models.PositiveIntegerField(default=1, verbose_name=_('عدد الموافقات المطلوبة'))
    sla_hours = models.PositiveIntegerField(default=48, verbose_name=_('الحد الأقصى للساعات (SLA)'))
    order = models.PositiveIntegerField(default=1, verbose_name=_('الترتيب'))

    class Meta:
        db_table = 'workflow_approval_step'
        ordering = ['order']

    def __str__(self):
        return f"{self.required_role.name} - {self.sla_hours}hrs"


class EscalationRule(SoftDeletableModel):
    """
    ماذا يحدث إذا تجاوز الطلب الـ SLA؟
    """
    approval_step = models.ForeignKey(ApprovalStep, on_delete=models.CASCADE, related_name='escalations')
    escalate_to_role = models.ForeignKey(Role, on_delete=models.PROTECT, verbose_name=_('الدور المُصعّد إليه'))
    notify_only = models.BooleanField(default=True, verbose_name=_('إشعار فقط (بدون نقل الصلاحية)'))

    class Meta:
        db_table = 'workflow_escalation_rule'


# ── 4. محرك التشغيل (Instance & History) ──

class WorkflowInstance(SoftDeletableModel):
    """
    الطلب الفعلي الذي فتحه الموظف ويمر في المسار
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(Workflow, on_delete=models.PROTECT, related_name='instances')
    version = models.ForeignKey(WorkflowVersion, on_delete=models.PROTECT)
    current_state = models.ForeignKey(State, on_delete=models.PROTECT, related_name='current_instances')
    initiator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='initiated_workflows')
    
    # ربط ديناميكي بأي نموذج في النظام (مثال: StatusChangeForm)
    context_type = models.CharField(max_length=100, verbose_name=_('نوع الكيان'))
    context_id = models.CharField(max_length=100, verbose_name=_('معرف الكيان'))
    
    history_records = HistoricalRecords()

    class Meta:
        db_table = 'workflow_instance'
        verbose_name = _('طلب عملية')
        verbose_name_plural = _('طلبات العمليات')
        indexes = [
            models.Index(fields=['context_type', 'context_id']),
            models.Index(fields=['current_state']),
        ]

    def __str__(self):
        return f"{self.workflow.name} - {self.id}"


class InstanceHistory(models.Model):
    """
    تتبع أحداث الطلب (الأشخاص الذين وافقوا أو علقوا)
    """
    instance = models.ForeignKey(WorkflowInstance, on_delete=models.CASCADE, related_name='action_history')
    action_by = models.ForeignKey(User, on_delete=models.PROTECT)
    from_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='history_from_state', null=True)
    to_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='history_to_state')
    comments = models.TextField(blank=True, verbose_name=_('تعليقات'))
    signature_hash = models.CharField(max_length=64, blank=True, verbose_name=_('التوقيع الرقمي (لضمان عدم التلاعب)'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'workflow_instance_history'
        ordering = ['-created_at']
