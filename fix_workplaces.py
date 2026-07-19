import re

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

# 1. Update the label back to what it was
content = content.replace(
    '<label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">جهة العمل التابعة (إدارة مركزية / فرع / قسم / سرية / وحدة)</label>',
    '<label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">جهة العمل التابعة (إدارة مركزية / فرع / مديرية)</label>'
)

# 2. Add Divisions and Units HTML right after the Workplaces div
workplaces_div_end = """                  <MultiSelect 
                    v-model="filterWorkplaces" 
                    :options="groupedWorkplaces" 
                    valueKey="value" 
                    labelKey="label" 
                    placeholder="كل الجهات" 
                  />
                </div>"""

new_divs = """                  <MultiSelect 
                    v-model="filterWorkplaces" 
                    :options="groupedWorkplaces" 
                    valueKey="value" 
                    labelKey="label" 
                    placeholder="كل الجهات" 
                  />
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">القسم</label>
                  <MultiSelect 
                    v-model="filterDivision" 
                    :options="coreStore.divisions" 
                    valueKey="id" 
                    labelKey="name" 
                    placeholder="كل الأقسام" 
                  />
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الوحدة</label>
                  <MultiSelect 
                    v-model="filterUnit" 
                    :options="coreStore.units" 
                    valueKey="id" 
                    labelKey="name" 
                    placeholder="كل الوحدات" 
                  />
                </div>"""

content = content.replace(workplaces_div_end, new_divs)


# 3. Fix groupedWorkplaces computed
old_computed = """  const centrals = coreStore.centralDepartments
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

new_computed = """  const centrals = coreStore.centralDepartments
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

content = content.replace(old_computed, new_computed)

# 4. Define filterDivision and filterUnit refs
content = content.replace(
    "const filterWorkplaces = ref<string[]>([])",
    "const filterWorkplaces = ref<string[]>([])\nconst filterDivision = ref<number[]>([])\nconst filterUnit = ref<number[]>([])"
)

# 5. Fix params logic
old_params = """    const divisions = filterWorkplaces.value.filter(v => v.startsWith('division_')).map(v => v.replace('division_', ''))
    if (divisions.length > 0) params.division = divisions.join(',')

    const units = filterWorkplaces.value.filter(v => v.startsWith('unit_')).map(v => v.replace('unit_', ''))
    if (units.length > 0) params.unit = units.join(',')"""

new_params = """    if (filterDivision.value.length > 0) params.division = filterDivision.value.join(',')
    if (filterUnit.value.length > 0) params.unit = filterUnit.value.join(',')"""

content = content.replace(old_params, new_params)


# 6. Add them to active filters count
old_count = "if (filterWorkplaces.value.length > 0) count++"
new_count = "if (filterWorkplaces.value.length > 0) count++\n  if (filterDivision.value.length > 0) count++\n  if (filterUnit.value.length > 0) count++"
content = content.replace(old_count, new_count)

# 7. Add them to resetAllFilters
old_reset = "filterWorkplaces.value = []"
new_reset = "filterWorkplaces.value = []\n  filterDivision.value = []\n  filterUnit.value = []"
content = content.replace(old_reset, new_reset)

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(content)

print("Workplaces fixed.")
