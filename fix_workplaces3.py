import re

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

old_script = """const groupedWorkplaces = computed(() => {
  const groups: any[] = []
  
  const centrals = coreStore.centralDepartments
  const branches = coreStore.branches
  const districts = coreStore.districtPolices

  if (centrals.length) {
    groups.push({
      label: 'الإدارات المركزية / السرايا',
      options: centrals.map((d: any) => ({ value: `central_${d.id}`, label: d.name }))
    })
  }
  if (branches.length) {
    groups.push({
      label: 'الفروع',
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

new_script = """const groupedWorkplaces = computed(() => {
  const groups: any[] = []
  
  let centrals = coreStore.centralDepartments
  let branches = coreStore.branches
  let districts = coreStore.districtPolices

  // Filter based on selected Security Admins
  if (filterSecurityAdmin.value.length > 0) {
    centrals = centrals.filter((d: any) => filterSecurityAdmin.value.includes(d.security_admin))
    branches = branches.filter((b: any) => filterSecurityAdmin.value.includes(b.security_admin))
    districts = districts.filter((d: any) => filterSecurityAdmin.value.includes(d.security_admin))
  } else {
    // If no security admin is selected, do we show empty or all? The user says "لا تظهر الا ما يخص المحافظة".
    // Let's return empty groups to force selection first.
    return []
  }

  if (centrals.length) {
    groups.push({
      label: 'الإدارات المركزية / السرايا',
      options: centrals.map((d: any) => ({ value: `central_${d.id}`, label: d.name }))
    })
  }
  if (branches.length) {
    groups.push({
      label: 'الفروع',
      options: branches.map((b: any) => ({ value: `branch_${b.id}`, label: b.name }))
    })
  }
  if (districts.length) {
    groups.push({
      label: 'مراكز الشرطة / المديريات',
      options: districts.map((d: any) => ({ value: `district_${d.id}`, label: d.name_ar || d.name }))
    })
  }
  return groups
})"""

content = content.replace(old_script, new_script)


# Update template to disable `filterWorkplaces` if no Security Admin is selected
html_old_wp = """<MultiSelect 
                    v-model="filterWorkplaces" 
                    :options="groupedWorkplaces" 
                    valueKey="value" 
                    labelKey="label" 
                    placeholder="كل الجهات" 
                  />"""

html_new_wp = """<MultiSelect 
                    v-model="filterWorkplaces" 
                    :options="groupedWorkplaces" 
                    valueKey="value" 
                    labelKey="label" 
                    placeholder="كل الجهات" 
                    :disabled="filterSecurityAdmin.length === 0"
                    disabledPlaceholder="اختر الإدارة الأمنية أولاً..."
                  />"""
content = content.replace(html_old_wp, html_new_wp)


# Ensure the watcher clears `filterWorkplaces` if security admin is unchecked and the chosen workplace is no longer valid
watcher_script = """
watch(filterSecurityAdmin, () => {
  const validVals = groupedWorkplaces.value.flatMap(g => g.options.map(o => o.value))
  filterWorkplaces.value = filterWorkplaces.value.filter(val => validVals.includes(val))
})
"""
content = content.replace("const groupedWorkplaces = computed(() => {", watcher_script + "\nconst groupedWorkplaces = computed(() => {")

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(content)

print("Workplaces logic filtered.")
