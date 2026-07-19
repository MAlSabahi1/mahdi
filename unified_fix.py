import re

with open('/home/mahdi/.config/Antigravity/User/History/291fc274/D1bW.vue', 'r') as f:
    content = f.read()

# 1. Imports
if "import MultiSelect" not in content:
    content = content.replace("import ReportHeader from '@/components/reports/ReportHeader.vue'", 
                              "import MultiSelect from '@/components/common/MultiSelect.vue'\nimport ReportHeader from '@/components/reports/ReportHeader.vue'")

# 2. Variable fixes
content = content.replace("coreStore.categories", "coreStore.jobCategories")
content = content.replace("coreStore.forceClassifications", "coreStore.forceTypes")

# 3. Replace simple Selects with MultiSelect
def replace_simple(var_name, options_var, placeholder, label_text):
    global content
    pattern = r'<label class="mb-1\.5 block text-sm font-medium text-gray-700 dark:text-gray-400">' + label_text + r'</label>\s*<div class="relative z-20 bg-transparent">\s*<select v-model="' + var_name + r'".*?</div>'
    repl = f'<label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{label_text}</label>\n                  <MultiSelect v-model="{var_name}" :options="{options_var}" valueKey="id" labelKey="name" placeholder="{placeholder}" />'
    content = re.sub(pattern, repl, content, flags=re.DOTALL)

replace_simple("filterRank", "coreStore.ranks", "جميع الرتب", "الرتبة")
replace_simple("filterCategory", "coreStore.jobCategories", "جميع الفئات", "الفئة")
replace_simple("filterResidenceGov", "coreStore.governorates", "كل المحافظات", "المحافظة")
replace_simple("filterQualification", "coreStore.qualifications", "كل المؤهلات", "المؤهل")
replace_simple("filterPosition", "coreStore.positions", "كل المناصب", "المنصب")
replace_simple("filterForceClass", "coreStore.forceTypes", "كل التصنيفات", "تصنيف القوة")

# 4. Extract and Replace the Workplaces & Status grid (which is very tricky to regex exactly, so I will match the whole section)
# We look for "الإدارة المركزية" down to "Dropdown Menu -->"
workplace_pattern = r'<div>\s*<label class="mb-1\.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الإدارة المركزية \(للقطاعات\)</label>.*?<!-- Dropdown Menu -->.*?</div>\s*</div>\s*</div>'

workplace_repl = """<div class="lg:col-span-2">
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">جهة العمل (إدارة / فرع / مديرية)</label>
              <MultiSelect v-model="filterWorkplaces" :options="groupedWorkplaces" valueKey="value" labelKey="label" placeholder="كل الجهات" />
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">التصنيف العام للحالة</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="filterStatusClassification" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option value="">جميع الحالات</option>
                  <option value="active_full">قوة عاملة فعلية</option>
                  <option value="active_part">قوة عاملة غير فعلية</option>
                  <option value="inactive_temp">قوة غير عاملة مؤقتاً</option>
                  <option value="inactive_perm">قوة غير عاملة نهائياً</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                </span>
              </div>
            </div>
            
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">نوع الحالة المخصص</label>
              <MultiSelect v-model="filterStatusIds" :options="filteredStatuses" valueKey="id" labelKey="name" placeholder="جميع الأنواع" :disabled="!filterStatusClassification" disabledPlaceholder="اختر التصنيف أولاً..." />
            </div>"""

content = re.sub(workplace_pattern, workplace_repl, content, flags=re.DOTALL)


# 5. Fix Javascript Ref Types
for var_name in ["filterRank", "filterCategory", "filterResidenceGov", "filterQualification", "filterPosition", "filterForceClass"]:
    content = re.sub(rf"const {var_name} = ref<number \| ''>\(''\)", f"const {var_name} = ref<number[]>([])", content)
    content = re.sub(rf"const {var_name} = ref\(''\)", f"const {var_name} = ref<number[]>([])", content)

# 6. Setup filterWorkplaces and groupedWorkplaces
script_additions = """
const filterWorkplaces = ref<string[]>([])
const groupedWorkplaces = computed(() => {
  const groups = []
  if (coreStore.securityAdmins.length) {
    groups.push({
      label: 'الإدارات الأمنية',
      options: coreStore.securityAdmins.map((d: any) => ({ value: `admin_${d.id}`, label: d.name }))
    })
  }
  if (coreStore.centralDepartments.length) {
    groups.push({
      label: 'الإدارات المركزية',
      options: coreStore.centralDepartments.map((d: any) => ({ value: `central_${d.id}`, label: d.name }))
    })
  }
  if (coreStore.branches.length) {
    groups.push({
      label: 'الفروع',
      options: coreStore.branches.map((b: any) => ({ value: `branch_${b.id}`, label: b.name }))
    })
  }
  if (coreStore.districtPolices.length) {
    groups.push({
      label: 'المديريات',
      options: coreStore.districtPolices.map((d: any) => ({ value: `district_${d.id}`, label: d.name_ar || d.name }))
    })
  }
  return groups
})
"""
content = content.replace("const filterSecurityAdmin = ref<number | ''>('')", script_additions)
# Remove old workplace refs
content = re.sub(r"const filterCentralDept = ref<number \| ''>\(''\)\n", "", content)
content = re.sub(r"const filterBranch = ref<number \| ''>\(''\)\n", "", content)
content = re.sub(r"const filterDistrict = ref<number \| ''>\(''\)\n", "", content)
# Remove old status dropdown refs
content = re.sub(r"const showStatusDropdown = ref\(false\)\n", "", content)
content = re.sub(r"const toggleAllStatuses = \(e: Event\) => \{.*?\n\}\n", "", content, flags=re.DOTALL)

# 7. Setup Active Filters Count
# Replace `if (filterRank.value) count++` with `if (filterRank.value.length > 0) count++`
for var_name in ["filterRank", "filterCategory", "filterResidenceGov", "filterQualification", "filterPosition", "filterForceClass"]:
    content = content.replace(f"if ({var_name}.value) count++", f"if ({var_name}.value.length > 0) count++")

content = content.replace("if (filterSecurityAdmin.value) count++", "if (filterWorkplaces.value.length > 0) count++")
content = re.sub(r"if \(filterCentralDept\.value\) count\+\+\n\s*", "", content)
content = re.sub(r"if \(filterBranch\.value\) count\+\+\n\s*", "", content)
content = re.sub(r"if \(filterDistrict\.value\) count\+\+\n\s*", "", content)

# 8. Setup resetAllFilters
for var_name in ["filterRank", "filterCategory", "filterResidenceGov", "filterQualification", "filterPosition", "filterForceClass"]:
    content = content.replace(f"{var_name}.value = ''", f"{var_name}.value = []")

content = content.replace("filterSecurityAdmin.value = ''", "filterWorkplaces.value = []")
content = re.sub(r"\s*filterCentralDept\.value = ''", "", content)
content = re.sub(r"\s*filterBranch\.value = ''", "", content)
content = re.sub(r"\s*filterDistrict\.value = ''", "", content)
content = content.replace("showStatusDropdown.value = false", "")

# 9. Setup fetchData params
for var_name in ["filterRank", "filterCategory", "filterResidenceGov", "filterQualification", "filterPosition", "filterForceClass"]:
    # The param assignment maps:
    p_name = var_name.replace('filter', '').lower()
    if p_name == 'residencegov': p_name = 'residence_governorate'
    elif p_name == 'forceclass': p_name = 'force_classification'
    
    old_code = f"if ({var_name}.value) params.{p_name} = {var_name}.value"
    new_code = f"if ({var_name}.value.length > 0) params.{p_name} = {var_name}.value.join(',')"
    content = content.replace(old_code, new_code)

# Custom params for workplaces
new_params = """
    const admins = filterWorkplaces.value.filter(v => v.startsWith('admin_')).map(v => v.replace('admin_', ''))
    if (admins.length > 0) params.security_admin = admins.join(',')
    
    const centrals = filterWorkplaces.value.filter(v => v.startsWith('central_')).map(v => v.replace('central_', ''))
    if (centrals.length > 0) params.central_department = centrals.join(',')
    
    const branches = filterWorkplaces.value.filter(v => v.startsWith('branch_')).map(v => v.replace('branch_', ''))
    if (branches.length > 0) params.branch = branches.join(',')
    
    const districts = filterWorkplaces.value.filter(v => v.startsWith('district_')).map(v => v.replace('district_', ''))
    if (districts.length > 0) params.district_police = districts.join(',')
"""

content = re.sub(r"if \(filterSecurityAdmin\.value\) params\.security_admin = filterSecurityAdmin\.value", new_params, content)
content = re.sub(r"\s*if \(filterCentralDept\.value\) params\.central_department = filterCentralDept\.value", "", content)
content = re.sub(r"\s*if \(filterBranch\.value\) params\.branch = filterBranch\.value", "", content)
content = re.sub(r"\s*if \(filterDistrict\.value\) params\.district_police = filterDistrict\.value", "", content)

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(content)

print("Unified refactor done!")
