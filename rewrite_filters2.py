import re

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

template_replacements = {
    "filterSecurityAdmin": ("availableSecurityAdmins", "كل الوحدات"),
    "filterCentralDept": ("availableCentralDepts", "كل الإدارات المركزية"),
    "filterBranch": ("availableBranches", "كل الفروع"),
    "filterDistrict": ("coreStore.districtPolices", "كل المديريات"),
    "filterPosition": ("coreStore.positions", "كل المناصب"),
    "filterRank": ("coreStore.ranks", "كل الرتب"),
    "filterForceClass": ("coreStore.forceClassifications", "كل التصنيفات"),
    "filterQualification": ("coreStore.qualifications", "كل المؤهلات"),
    "filterCategory": ("coreStore.categories", "كل الفئات")
}

for var_name, (options, placeholder) in template_replacements.items():
    # Find the <div class="relative z-20 bg-transparent"> that contains v-model="var_name"
    # and replace the whole div with MultiSelect
    pattern = r'<div class="relative z-20 bg-transparent">\s*<select v-model="' + var_name + r'".*?</div>'
    replacement = f"""<MultiSelect
                    v-model="{var_name}"
                    :options="{options}"
                    valueKey="id"
                    labelKey="name"
                    placeholder="{placeholder}"
                  />"""
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(content)

print("Done rewrite 2")
