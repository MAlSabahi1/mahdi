import re

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

variables = [
    "filterSecurityAdmin", "filterCentralDept", "filterBranch", "filterDistrict", 
    "filterPosition", "filterQualification", "filterForceClass", "filterRank", "filterCategory"
]

for var_name in variables:
    # Fix count logic
    content = content.replace(f"if ({var_name}.value) count++", f"if ({var_name}.value.length > 0) count++")

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(content)

print("Fixed count")
