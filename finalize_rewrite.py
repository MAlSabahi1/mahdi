import re

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

# 2. Add import for MultiSelect
import_statement = "import MultiSelect from '@/components/common/MultiSelect.vue'\n"
if "import MultiSelect" not in content:
    content = content.replace("import ReportHeader from '@/components/reports/ReportHeader.vue'", 
                              import_statement + "import ReportHeader from '@/components/reports/ReportHeader.vue'")

# 3. Change ref definitions to arrays
template_replacements = [
    "filterSecurityAdmin", "filterCentralDept", "filterBranch", "filterDistrict", 
    "filterPosition", "filterQualification", "filterForceClass", "filterRank", "filterCategory"
]

for var_name in template_replacements:
    content = re.sub(rf"const {var_name} = ref<number \| ''>\(''\)", f"const {var_name} = ref<number[]>([])", content)
    content = re.sub(rf"const {var_name} = ref\(''\)", f"const {var_name} = ref<number[]>([])", content)

# 4. Change params assignment in fetchData
params_replacements = {
    "filterRank": "rank",
    "filterCategory": "category",
    "filterSecurityAdmin": "security_admin",
    "filterCentralDept": "central_department",
    "filterBranch": "branch",
    "filterDistrict": "district_police",
    "filterPosition": "position",
    "filterQualification": "qualification",
    "filterForceClass": "force_classification"
}

for var_name, param_name in params_replacements.items():
    old_line = f"if ({var_name}.value) params.{param_name} = {var_name}.value"
    new_line = f"if ({var_name}.value.length > 0) params.{param_name} = {var_name}.value.join(',')"
    content = content.replace(old_line, new_line)

# 5. Reset all filters should reset to [] instead of ''
for var_name in template_replacements:
    content = content.replace(f"{var_name}.value = ''", f"{var_name}.value = []")

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(content)

print("Done finalize")
