#!/usr/bin/env python
"""
اختبار الـ API مباشرة
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from core.models import JobCategory, JobTitle, Directorate, Position
from core.serializers import JobCategorySerializer, DirectorateSerializer

print("=" * 60)
print("اختبار الـ API Serializers")
print("=" * 60)

# اختبار JobCategory Serializer
print("\n1. JobCategory Serializer:")
categories = JobCategory.objects.all()
for cat in categories:
    serializer = JobCategorySerializer(cat)
    data = serializer.data
    print(f"   {data['name']}: job_titles_count = {data.get('job_titles_count', 'MISSING')}")
    # التحقق من العدد الفعلي
    actual_count = cat.job_titles.count()
    print(f"      (Actual count in DB: {actual_count})")

# اختبار Directorate
print("\n2. Directorate:")
dept_count = Directorate.objects.count()
print(f"   Total directorates: {dept_count}")

# اختبار Position
print("\n3. Position:")
pos_count = Position.objects.count()
print(f"   Total positions: {pos_count}")

print("\n" + "=" * 60)
