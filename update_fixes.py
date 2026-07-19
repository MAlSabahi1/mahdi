import re

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

# 1. Fix Placeholders for Birth Dropdowns
content = content.replace(
    '<select v-model="filterBirthDist"',
    '<select v-model="filterBirthDist"'
)
content = content.replace(
    '<option value="">اختر...</option>\n                      <option v-for="d in birthDistricts"',
    '<option value="">{{ !filterBirthGov ? \'اختر المحافظة أولاً...\' : \'الكل\' }}</option>\n                      <option v-for="d in birthDistricts"'
)
content = content.replace(
    '<option value="">اختر...</option>\n                      <option v-for="sd in birthSubDistricts"',
    '<option value="">{{ !filterBirthDist ? \'اختر المديرية أولاً...\' : \'الكل\' }}</option>\n                      <option v-for="sd in birthSubDistricts"'
)
content = content.replace(
    '<option value="">اختر...</option>\n                      <option v-for="v in birthVillages"',
    '<option value="">{{ !filterBirthSubDist ? \'اختر العزلة أولاً...\' : \'الكل\' }}</option>\n                      <option v-for="v in birthVillages"'
)

# 2. Fix filterStatusClassification to be MultiSelect
html_to_replace = """<div>
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
            </div>"""

new_html = """<div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">التصنيف العام للحالة</label>
              <MultiSelect 
                v-model="filterStatusClassification" 
                :options="[{id: 'active_full', name: 'قوة عاملة فعلية'}, {id: 'active_part', name: 'قوة عاملة غير فعلية'}, {id: 'inactive_temp', name: 'قوة غير عاملة مؤقتاً'}, {id: 'inactive_perm', name: 'قوة غير عاملة نهائياً'}]" 
                valueKey="id" 
                labelKey="name" 
                placeholder="جميع الحالات" 
              />
            </div>"""
content = content.replace(html_to_replace, new_html)

# Update disabled prop for filterStatusIds
content = content.replace(':disabled="!filterStatusClassification"', ':disabled="filterStatusClassification.length === 0"')


# Update script for filterStatusClassification
content = content.replace("const filterStatusClassification = ref('')", "const filterStatusClassification = ref<string[]>([])")

# Update filteredStatuses computed property
old_computed = """const filteredStatuses = computed(() => {
  if (filterStatusClassification.value) {
    return coreStore.statuses.filter((s: any) => s.classification === filterStatusClassification.value)
  }
  return []
})"""
new_computed = """const filteredStatuses = computed(() => {
  if (filterStatusClassification.value.length > 0) {
    return coreStore.statuses.filter((s: any) => filterStatusClassification.value.includes(s.classification))
  }
  return []
})"""
content = content.replace(old_computed, new_computed)

# Update count logic
content = content.replace("if (filterStatusClassification.value) count++", "if (filterStatusClassification.value.length > 0) count++")

# Update reset logic
content = content.replace("filterStatusClassification.value = ''", "filterStatusClassification.value = []")

# Update params logic
old_param = "if (filterStatusClassification.value) params.status_classification = filterStatusClassification.value"
new_param = "if (filterStatusClassification.value.length > 0) params.status_classification = filterStatusClassification.value.join(',')"
content = content.replace(old_param, new_param)


# 3. Fix Workplaces filtering
old_wp_script = """const groupedWorkplaces = computed(() => {
  const groups: any[] = []
  if (filterSecurityAdmin.value.length === 0) return groups // No admins selected, return empty

  // Filter central depts, branches and districts by selected admins
  // NOTE: If central departments are independent, we might want to show them anyway, but per user request: "بمجر ماتختار امن محافظه كذا او كذا في هذا الحقل تضهر الادارات والمديريات والفروع الخاصه به"
  // Assuming they are linked by `security_admin` field.

  const centrals = coreStore.centralDepartments.filter((d: any) => filterSecurityAdmin.value.includes(d.security_admin))
  const branches = coreStore.branches.filter((b: any) => filterSecurityAdmin.value.includes(b.security_admin))
  const districts = coreStore.districtPolices.filter((d: any) => filterSecurityAdmin.value.includes(d.security_admin))"""

new_wp_script = """const groupedWorkplaces = computed(() => {
  const groups: any[] = []
  
  // Show all if no Security Admin is selected, or let user select anyway
  const centrals = coreStore.centralDepartments
  const branches = coreStore.branches
  const districts = coreStore.districtPolices"""

content = content.replace(old_wp_script, new_wp_script)

# Remove the disabled prop from HTML
content = content.replace(
    'placeholder="كل الجهات" \n                    :disabled="filterSecurityAdmin.length === 0"\n                    disabledPlaceholder="اختر الإدارة الأمنية أولاً..."',
    'placeholder="كل الجهات" '
)

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(content)

print("Fixes applied.")
