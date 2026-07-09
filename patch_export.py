import os

filepath = '/home/mahdi/Desktop/n/mahdi/Backend/systems/services/application/services/export_service.py'
with open(filepath, 'r') as f:
    content = f.read()

# 1. ForceClassification -> ForceType
content = content.replace('ForceClassification, Qualification', 'ForceType, Qualification')

# 2. __DEPT_BRANCH__
old_dept = "val = person.central_department.name if getattr(person, 'central_department', None) else (person.branch.name if getattr(person, 'branch', None) else '')"
new_dept = "val = person.central_department.name if getattr(person, 'central_department', None) else (\n                                person.branch.name if getattr(person, 'branch', None) else (\n                                    person.district_police.name if getattr(person, 'district_police', None) else ''\n                                )\n                            )"
content = content.replace(old_dept, new_dept)

# 3. __DISTRICT_DIVISION__
old_div = "val = person.district_police.name if getattr(person, 'district_police', None) else (person.division.name if getattr(person, 'division', None) else '')"
new_div = "val = person.division.name if getattr(person, 'division', None) else ''\n                        elif raw_col == '__STATUS_TYPE__':\n                            val = person.current_status.get_classification_display() if getattr(person, 'current_status', None) else ''"
content = content.replace(old_div, new_div)

with open(filepath, 'w') as f:
    f.write(content)
