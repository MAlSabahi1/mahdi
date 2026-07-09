from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, Sum, Avg, Min, Max
from django.apps import apps
from django.db import connection

from ...models import BIDataSource, EnterpriseReportTemplate
from ..serializers.bi_serializers import BIDataSourceSerializer, EnterpriseReportTemplateSerializer

class BIDataSourceViewSet(viewsets.ModelViewSet):
    queryset = BIDataSource.objects.all()
    serializer_class = BIDataSourceSerializer
    permission_classes = [IsAuthenticated]

class EnterpriseReportTemplateViewSet(viewsets.ModelViewSet):
    queryset = EnterpriseReportTemplate.objects.all()
    serializer_class = EnterpriseReportTemplateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

class BIEngineRunnerAPIView(APIView):
    """
    محرك BI المتقدم لتنفيذ التقارير المعقدة (AST Filters, Aggregations, Views)
    """
    permission_classes = [IsAuthenticated]

    def _build_q_object(self, condition):
        # Base case: it's a leaf node condition
        if 'operator' not in condition or condition['operator'] not in ['AND', 'OR']:
            field = condition.get('field')
            op = condition.get('op', 'exact')
            val = condition.get('value')
            
            if not field: return Q()
            
            lookup = field
            if op == 'icontains': lookup = f"{field}__icontains"
            elif op == 'gt': lookup = f"{field}__gt"
            elif op == 'lt': lookup = f"{field}__lt"
            elif op == 'in': lookup = f"{field}__in"
            elif op == 'isnull': lookup = f"{field}__isnull"
            
            return Q(**{lookup: val})
            
        # Recursive case: AND/OR node
        q_obj = Q()
        logical_op = condition.get('operator')
        children = condition.get('conditions', [])
        
        for i, child in enumerate(children):
            child_q = self._build_q_object(child)
            if i == 0:
                q_obj = child_q
            else:
                if logical_op == 'AND':
                    q_obj &= child_q
                elif logical_op == 'OR':
                    q_obj |= child_q
                
        return q_obj

    def post(self, request, slug):
        try:
            report = EnterpriseReportTemplate.objects.get(slug=slug, is_active=True)
        except EnterpriseReportTemplate.DoesNotExist:
            return Response({"error": "التقرير غير موجود."}, status=404)
            
        schema = report.config_schema
        ds = report.data_source
        
        if ds.source_type == 'orm_model':
            try:
                app_label, model_name = ds.target.split('.')
                Model = apps.get_model(app_label=app_label, model_name=model_name)
            except Exception as e:
                return Response({"error": f"خطأ في مصدر البيانات: {str(e)}"}, status=400)
                
            qs = Model.objects.all()
            
            # Apply Filters (AST tree)
            filters = schema.get('filters', {})
            # Overwrite with runtime filters from request
            runtime_filters = request.data.get('filters', {})
            if runtime_filters:
                filters = runtime_filters
                
            if filters:
                try:
                    q_filters = self._build_q_object(filters)
                    qs = qs.filter(q_filters)
                except Exception as e:
                     return Response({"error": f"خطأ في تطبيق الفلاتر: {str(e)}"}, status=400)
                
            # Apply Group By and Aggregations
            group_by = schema.get('group_by', [])
            aggregations = schema.get('aggregations', [])
            
            if group_by:
                qs = qs.values(*group_by)
                if aggregations:
                    agg_kwargs = {}
                    for agg in aggregations:
                        field = agg.get('field')
                        func = agg.get('function') # SUM, COUNT, AVG
                        alias = agg.get('alias', f"{func}_{field}")
                        if func == 'COUNT': agg_kwargs[alias] = Count(field)
                        elif func == 'SUM': agg_kwargs[alias] = Sum(field)
                        elif func == 'AVG': agg_kwargs[alias] = Avg(field)
                    try:
                        qs = qs.annotate(**agg_kwargs)
                    except Exception as e:
                         return Response({"error": f"خطأ في التجميع: {str(e)}"}, status=400)
            else:
                # Select explicit columns
                columns = [c.get('field') for c in schema.get('columns', []) if c.get('field')]
                if columns:
                    qs = qs.values(*columns)
                    
            try:
                data = list(qs[:1000]) # Limit for safety
            except Exception as e:
                 return Response({"error": f"فشل تنفيذ الاستعلام: {str(e)}"}, status=400)
            
        elif ds.source_type == 'db_view':
            # Execute raw sql against the view
            target_view = ds.target
            # VERY BASIC sanitization - in production needs robust escaping
            if ';' in target_view or ' ' in target_view:
                 return Response({"error": "Invalid view name."}, status=400)
                 
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {target_view} LIMIT 1000")
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        else:
            return Response({"error": "نوع المصدر غير مدعوم."}, status=400)
            
        return Response({
            "report_title": report.title,
            "description": report.description,
            "layout_type": schema.get('layout_type', 'table'),
            "schema": schema,
            "data": data
        })
