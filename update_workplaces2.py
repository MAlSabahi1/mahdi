import re

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

# 1. Update HTML Label
content = content.replace(
    '<label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">جهة العمل التابعة (إدارة مركزية / فرع / مديرية)</label>',
    '<label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">جهة العمل التابعة (إدارة مركزية / فرع / قسم / سرية / وحدة)</label>'
)

# 2. Update groupedWorkplaces computed
old_script = """const groupedWorkplaces = computed(() => {
  const groups: any[] = []
  
  // Show all if no Security Admin is selected, or let user select anyway
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

new_script = """const groupedWorkplaces = computed(() => {
  const groups: any[] = []
  
  const centrals = coreStore.centralDepartments
  const branches = coreStore.branches
  const districts = coreStore.districtPolices
  const divisions = coreStore.divisions
  const units = coreStore.units

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
  if (divisions && divisions.length) {
    groups.push({
      label: 'الأقسام',
      options: divisions.map((div: any) => ({ value: `division_${div.id}`, label: div.name }))
    })
  }
  if (districts.length) {
    groups.push({
      label: 'مراكز الشرطة / المديريات',
      options: districts.map((d: any) => ({ value: `district_${d.id}`, label: d.name_ar || d.name }))
    })
  }
  if (units && units.length) {
    groups.push({
      label: 'الوحدات',
      options: units.map((u: any) => ({ value: `unit_${u.id}`, label: u.name }))
    })
  }
  return groups
})"""

content = content.replace(old_script, new_script)

# 3. Add to params
old_params = """    const districts = filterWorkplaces.value.filter(v => v.startsWith('district_')).map(v => v.replace('district_', ''))
    if (districts.length > 0) params.district_police = districts.join(',')"""

new_params = """    const districts = filterWorkplaces.value.filter(v => v.startsWith('district_')).map(v => v.replace('district_', ''))
    if (districts.length > 0) params.district_police = districts.join(',')

    const divisions = filterWorkplaces.value.filter(v => v.startsWith('division_')).map(v => v.replace('division_', ''))
    if (divisions.length > 0) params.division = divisions.join(',')

    const units = filterWorkplaces.value.filter(v => v.startsWith('unit_')).map(v => v.replace('unit_', ''))
    if (units.length > 0) params.unit = units.join(',')"""

content = content.replace(old_params, new_params)

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(content)

print("FrontEnd updated")
