import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from systems.personnel.models import PersonnelMaster
p = PersonnelMaster.objects.get(military_number="9900005")
print("expense_status:", repr(p.expense_status))
print("get_expense_status_display:", repr(p.get_expense_status_display()))
print("All expense choices:", p._meta.get_field('expense_status').choices)
