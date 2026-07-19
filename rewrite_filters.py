import re

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

# 1. Replace <select> blocks with <MultiSelect> blocks

template_replacements = {
    "filterSecurityAdmin": ("coreStore.securityAdmins", "كل الوحدات"),
    "filterCentralDept": ("coreStore.centralDepartments", "كل الإدارات المركزية"),
    "filterBranch": ("coreStore.branches", "كل الفروع"),
    "filterDistrict": ("coreStore.districtPolices", "كل المديريات"),
    "filterPosition": ("coreStore.positions", "كل المناصب"),
    "filterRank": ("coreStore.ranks", "كل الرتب"),
    "filterForceClass": ("coreStore.forceClassifications", "كل التصنيفات"),
    "filterQualification": ("coreStore.qualifications", "كل المؤهلات"),
    "filterCategory": ("coreStore.categories", "كل الفئات")
}

for var_name, (options, placeholder) in template_replacements.items():
    # Regex to find the <div class="relative z-20 bg-transparent">...<select v-model="var_name"...</select>...</div>
    # Actually, let's just find the whole <div class="relative z-20 bg-transparent"> block containing v-model="var_name"
    pattern = r'<div class="relative z-20 bg-transparent">\s*<select v-model="' + var_name + r'".*?</select>\s*</div>'
    
    replacement = f"""<MultiSelect
                    v-model="{var_name}"
                    :options="{options}"
                    valueKey="id"
                    labelKey="name"
                    placeholder="{placeholder}"
                  />"""
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# 2. Add import for MultiSelect
import_statement = "import MultiSelect from '@/components/common/MultiSelect.vue'\n"
content = content.replace("import ReportHeader from '@/components/reports/ReportHeader.vue'", 
                          import_statement + "import ReportHeader from '@/components/reports/ReportHeader.vue'")

# 3. Change ref definitions to arrays
for var_name in template_replacements.keys():
    content = re.sub(rf"const {var_name} = ref<number \| ''>\(''\)", f"const {var_name} = ref<number[]>([])", content)
    content = re.sub(rf"const {var_name} = ref\(''\)", f"const {var_name} = ref<number[]>([])", content)

# 4. Change params assignment in fetchData
# From: if (filterRank.value) params.rank = filterRank.value
# To: if (filterRank.value.length > 0) params.rank = filterRank.value.join(',')

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
for var_name in template_replacements.keys():
    content = content.replace(f"{var_name}.value = ''", f"{var_name}.value = []")

# Write it back
with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(content)

print("Done rewrite")
