"""
Reconciliation API Views — طبقة HTTP رفيعة
═══════════════════════════════════════════
View لا يحتوي أي منطق أعمال.
يقوم فقط بـ: Request → Command → UseCase → Response
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from ...application.use_cases.reconciliation_use_cases import (
    CreateReconciliationUseCase,
    ExecuteReconciliationUseCase,
)
from ...application.commands.reconciliation_commands import (
    CreateReconciliationCommand,
    ExecuteReconciliationCommand,
)
from ...infrastructure.repositories.django_reconciliation_repo import (
    DjangoReconciliationRepository,
)
from ..serializers.reconciliation_serializers import (
    CreateReconciliationSerializer,
    ReconciliationTaskOutputSerializer,
)


def _get_repo() -> DjangoReconciliationRepository:
    """Dependency Factory — ينشئ Repository جاهزاً للاستخدام."""
    return DjangoReconciliationRepository()


class CreateReconciliationView(APIView):
    """
    POST /api/v1/service-cycle/reconciliation/
    إنشاء مهمة مطابقة جديدة.
    """
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # 1. التحقق من صحة البيانات الواردة
        serializer = CreateReconciliationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # 2. بناء الأمر
        command = CreateReconciliationCommand(
            name=data["name"],
            task_type=data["task_type"],
            security_admin_id=data["security_admin_id"],
            created_by_id=request.user.id,
            key_field=data.get("key_field", "military_number"),
            source_file_path=str(data["source_file"]),
        )

        # 3. تنفيذ الـ Use Case
        use_case = CreateReconciliationUseCase(repo=_get_repo())
        try:
            task = use_case.execute(command)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)

        # 4. الرد
        return Response(
            {"id": str(task.id), "status": task.status.value},
            status=status.HTTP_201_CREATED,
        )


class ExecuteReconciliationView(APIView):
    """
    POST /api/v1/service-cycle/reconciliation/{task_id}/execute/
    تشغيل مطابقة موجودة.
    """

    def post(self, request, task_id):
        command = ExecuteReconciliationCommand(
            task_id=task_id,
            requested_by=request.user.id,
        )

        # Processor يأتي من الـ reconciliation_service الموجود
        from ...infrastructure.processors.excel_processor import ExcelReconciliationProcessor
        processor = ExcelReconciliationProcessor()

        use_case = ExecuteReconciliationUseCase(
            repo=_get_repo(),
            processor=processor,
        )

        try:
            task = use_case.execute(command)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "id":      str(task.id),
                "status":  task.status.value,
                "summary": task.get_result_summary(),
            }
        )


class ReconciliationListView(APIView):
    """
    GET /api/v1/service-cycle/reconciliation/
    قائمة المطابقات للإدارة الحالية.
    """

    def get(self, request):
        # الإدارة تأتي من صلاحيات المستخدم
        admin_id = request.user.profile.security_admin_id
        tasks = _get_repo().list_by_admin(security_admin_id=admin_id)
        output = [
            {
                "id":        str(t.id),
                "name":      t.name,
                "task_type": t.task_type.value,
                "status":    t.status.value,
                "summary":   t.get_result_summary(),
            }
            for t in tasks
        ]
        return Response(output)
