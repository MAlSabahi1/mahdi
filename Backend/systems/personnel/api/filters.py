import django_filters
from django.db.models import Q
from .models import PersonnelMaster

class PersonnelFilter(django_filters.FilterSet):
    """
    فلاتر متقدمة للأفراد مع دعم Fuzzy matching للاسم الرباعي
    """
    search = django_filters.CharFilter(method='filter_search', label='بحث عام')
    full_name = django_filters.CharFilter(lookup_expr='icontains', label='الاسم (يحتوي)')
    military_number = django_filters.CharFilter(lookup_expr='exact')
    national_id = django_filters.CharFilter(lookup_expr='exact')
    
    security_admin = django_filters.NumberFilter(field_name='security_admin_id')
    central_department = django_filters.NumberFilter(field_name='central_department_id')
    branch = django_filters.NumberFilter(field_name='branch_id')
    district_police = django_filters.NumberFilter(field_name='district_police_id')
    division = django_filters.NumberFilter(field_name='division_id')
    unit = django_filters.NumberFilter(field_name='unit_id')
    
    
    # فلاتر الحالة والرتبة
    status = django_filters.NumberFilter(field_name='current_status_id')
    rank = django_filters.NumberFilter(field_name='current_rank_id')
    
    # فلاتر الجودة والاكتمال
    is_complete = django_filters.BooleanFilter()
    is_data_clean = django_filters.BooleanFilter()
    min_quality = django_filters.NumberFilter(field_name='data_quality_score', lookup_expr='gte')
    max_quality = django_filters.NumberFilter(field_name='data_quality_score', lookup_expr='lte')

    class Meta:
        model = PersonnelMaster
        fields = [
            'military_number', 'national_id', 'full_name',
            'security_admin', 'central_department', 'branch', 'district_police', 'division', 'unit',
            'status', 'rank',
            'is_complete', 'is_data_clean'
        ]

    def filter_search(self, queryset, name, value):
        """
        بحث شامل يدعم المطابقة التقريبية (Fuzzy)
        يبحث في الرقم العسكري، الرقم الوطني، والاسم
        """
        if not value:
            return queryset
            
        # إذا كان رقم، نبحث في الرقم العسكري أو الوطني
        if value.isdigit():
            return queryset.filter(
                Q(military_number__icontains=value) |
                Q(national_id__icontains=value)
            )
            
        # بخلاف ذلك نبحث في الاسم أو الملاحظات
        # فصل كلمات البحث لتحسين دقة البحث (Fuzzy-like)
        words = value.split()
        query = Q()
        for word in words:
            query &= Q(full_name__icontains=word)
            
        return queryset.filter(query | Q(notes__icontains=value))
