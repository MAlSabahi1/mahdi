import re

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

# 1. Update Placeholders for Residence Dropdowns
content = content.replace(
    '<select v-model="filterResDist"',
    '<select v-model="filterResDist"'
)
content = content.replace(
    '<option value="">اختر...</option>\n                      <option v-for="d in resDistricts"',
    '<option value="">{{ filterResidenceGov.length === 0 ? \'اختر المحافظة أولاً...\' : \'الكل\' }}</option>\n                      <option v-for="d in resDistricts"'
)

content = content.replace(
    '<option value="">اختر...</option>\n                      <option v-for="sd in resSubDistricts"',
    '<option value="">{{ !filterResDist ? \'اختر المديرية أولاً...\' : \'الكل\' }}</option>\n                      <option v-for="sd in resSubDistricts"'
)

content = content.replace(
    '<option value="">اختر...</option>\n                      <option v-for="v in resVillages"',
    '<option value="">{{ !filterResSubDist ? \'اختر العزلة أولاً...\' : \'الكل\' }}</option>\n                      <option v-for="v in resVillages"'
)


# 2. Add filterSecurityAdmin to HTML
html_to_replace = """<div class="lg:col-span-2">
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">جهة العمل (إدارة / فرع / مديرية)</label>
                  <MultiSelect 
                    v-model="filterWorkplaces" 
                    :options="groupedWorkplaces" 
                    valueKey="value" 
                    labelKey="label" 
                    placeholder="كل الجهات" 
                  />
                </div>"""

new_html = """<div class="lg:col-span-2">
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الإدارة الأمنية (المحافظات)</label>
                  <MultiSelect 
                    v-model="filterSecurityAdmin" 
                    :options="availableSecurityAdmins" 
                    valueKey="id" 
                    labelKey="name" 
                    placeholder="كل الإدارات الأمنية" 
                  />
                </div>
                <div class="lg:col-span-2">
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">جهة العمل التابعة (إدارة مركزية / فرع / مديرية)</label>
                  <MultiSelect 
                    v-model="filterWorkplaces" 
                    :options="groupedWorkplaces" 
                    valueKey="value" 
                    labelKey="label" 
                    placeholder="كل الجهات" 
                    :disabled="filterSecurityAdmin.length === 0"
                    disabledPlaceholder="اختر الإدارة الأمنية أولاً..."
                  />
                </div>"""

content = content.replace(html_to_replace, new_html)

# 3. Add filterSecurityAdmin to Script
script_to_replace = """const filterWorkplaces = ref<string[]>([])
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
})"""

new_script = """const filterSecurityAdmin = ref<number[]>([])
const filterWorkplaces = ref<string[]>([])

const groupedWorkplaces = computed(() => {
  const groups = []
  if (filterSecurityAdmin.value.length === 0) return groups // No admins selected, return empty

  // Filter central depts, branches and districts by selected admins
  // NOTE: If central departments are independent, we might want to show them anyway, but per user request: "بمجر ماتختار امن محافظه كذا او كذا في هذا الحقل تضهر الادارات والمديريات والفروع الخاصه به"
  // Assuming they are linked by `security_admin` field.

  const centrals = coreStore.centralDepartments.filter((d: any) => filterSecurityAdmin.value.includes(d.security_admin))
  const branches = coreStore.branches.filter((b: any) => filterSecurityAdmin.value.includes(b.security_admin))
  const districts = coreStore.districtPolices.filter((d: any) => filterSecurityAdmin.value.includes(d.security_admin))

  if (centrals.length) {
    groups.push({
      label: 'الإدارات المركزية / السرايا',
      options: centrals.map((d: any) => ({ value: `central_${d.id}`, label: d.name }))
    })
  }
  if (branches.length) {
    groups.push({
      label: 'الفروع / الأقسام',
      options: branches.map((b: any) => ({ value: `branch_${b.id}`, label: b.name }))
    })
  }
  if (districts.length) {
    groups.push({
      label: 'مراكز الشرطة',
      options: districts.map((d: any) => ({ value: `district_${d.id}`, label: d.name_ar || d.name }))
    })
  }
  return groups
})"""

content = content.replace(script_to_replace, new_script)


# 4. Add watcher for filterSecurityAdmin to reset filterWorkplaces when changed
watcher_script = """
watch(filterSecurityAdmin, () => {
  // Only keep workplaces that are still valid under the new security admin selection
  const validVals = groupedWorkplaces.value.flatMap(g => g.options.map(o => o.value))
  filterWorkplaces.value = filterWorkplaces.value.filter(val => validVals.includes(val))
})
"""
content = content.replace("const filterWorkplaces = ref<string[]>([])", watcher_script + "\nconst filterWorkplaces = ref<string[]>([])")


# 5. Add to Active Filters count
content = content.replace("if (filterWorkplaces.value.length > 0) count++", "if (filterSecurityAdmin.value.length > 0) count++\n  if (filterWorkplaces.value.length > 0) count++")


# 6. Add to resetAllFilters
content = content.replace("filterWorkplaces.value = []", "filterSecurityAdmin.value = []\n  filterWorkplaces.value = []")


# 7. Add params handling for SecurityAdmin
param_replace = """    const admins = filterWorkplaces.value.filter(v => v.startsWith('admin_')).map(v => v.replace('admin_', ''))
    if (admins.length > 0) params.security_admin = admins.join(',')"""
param_new = """    if (filterSecurityAdmin.value.length > 0) params.security_admin = filterSecurityAdmin.value.join(',')"""
content = content.replace(param_replace, param_new)


with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(content)

print("Workplaces script run completed.")
