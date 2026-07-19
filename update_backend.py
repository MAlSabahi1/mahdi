import re

with open('Backend/systems/reports/api/views.py', 'r') as f:
    content = f.read()

# 1. Add extraction of query params
content = content.replace(
    "district_police_id = request.query_params.get('district_police')",
    "district_police_id = request.query_params.get('district_police')\n        division_id = request.query_params.get('division')\n        unit_id = request.query_params.get('unit')"
)

# 2. Add filtering in filter_qs
old_filter = """            if district_police_id:
                dist_id_list = [int(x.strip()) for x in district_police_id.split(',') if x.strip().isdigit()]
                if dist_id_list:
                    qs = qs.filter(**{f'{prefix}district_police_id__in': dist_id_list})"""

new_filter = """            if district_police_id:
                dist_id_list = [int(x.strip()) for x in district_police_id.split(',') if x.strip().isdigit()]
                if dist_id_list:
                    qs = qs.filter(**{f'{prefix}district_police_id__in': dist_id_list})
            
            if division_id:
                div_id_list = [int(x.strip()) for x in division_id.split(',') if x.strip().isdigit()]
                if div_id_list:
                    qs = qs.filter(**{f'{prefix}division_id__in': div_id_list})
            
            if unit_id:
                unit_id_list = [int(x.strip()) for x in unit_id.split(',') if x.strip().isdigit()]
                if unit_id_list:
                    qs = qs.filter(**{f'{prefix}unit_id__in': unit_id_list})"""

content = content.replace(old_filter, new_filter)

with open('Backend/systems/reports/api/views.py', 'w') as f:
    f.write(content)

print("Backend updated")
