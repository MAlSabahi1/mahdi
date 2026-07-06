"""
API لجلب الدوال المتاحة - Available Functions API
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _

from d_services.apis.external_methods.base import ExternalMethodHandler, FunctionType


class AvailableFunctionsView(APIView):
    """
    API لجلب قائمة الدوال المتاحة
    
    Query params:
        - type: نوع الدالة (validator, execution, output_data, input_data, requester)
    """
    permission_classes = [IsAuthenticated]
    
    # ربط النوع بـ FunctionType
    TYPE_MAP = {
        'validator': FunctionType.VALIDATOR,
        'execution': FunctionType.EXECUTION,
        'output_data': FunctionType.OUTPUT_DATA,
        'input_data': FunctionType.INPUT_DATA,
        'requester': FunctionType.REQUESTER,
        'erp_data': FunctionType.ERP_DATA,
    }
    
    def get(self, request):
        """قائمة الدوال المتاحة مع تفاصيلها"""
        type_param = request.query_params.get('type')
        
        function_type = None
        if type_param:
            function_type = self.TYPE_MAP.get(type_param.lower())
            if not function_type:
                return Response({
                    'success': False,
                    'message': f"نوع غير صالح: {type_param}",
                    'available_types': list(self.TYPE_MAP.keys())
                }, status=400)
        
        functions = ExternalMethodHandler.get_functions_details(function_type)
        
        return Response(functions, status=200)
