import re

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

# 1. Add computed properties for availableDivisions and availableUnits
script_to_add = """const filterDivision = ref<number[]>([])
const filterUnit = ref<number[]>([])

const availableDivisions = computed(() => {
  if (filterWorkplaces.value.length === 0) return coreStore.divisions
  
  const centrals = filterWorkplaces.value.filter(v => v.startsWith('central_')).map(v => parseInt(v.replace('central_', ''), 10))
  const branches = filterWorkplaces.value.filter(v => v.startsWith('branch_')).map(v => parseInt(v.replace('branch_', ''), 10))
  const districts = filterWorkplaces.value.filter(v => v.startsWith('district_')).map(v => parseInt(v.replace('district_', ''), 10))
  
  return coreStore.divisions.filter((div: any) => {
    if (div.central_department && centrals.includes(div.central_department)) return true
    if (div.branch && branches.includes(div.branch)) return true
    if (div.district_police && districts.includes(div.district_police)) return true
    return false
  })
})

const availableUnits = computed(() => {
  if (filterDivision.value.length === 0) return coreStore.units
  return coreStore.units.filter((u: any) => filterDivision.value.includes(u.division))
})
"""

content = content.replace("const filterDivision = ref<number[]>([])\nconst filterUnit = ref<number[]>([])", script_to_add)


# 2. Update the template to use the computed properties
html_old_div = """:options="coreStore.divisions" 
                    valueKey="id" 
                    labelKey="name" 
                    placeholder="كل الأقسام" """

html_new_div = """:options="availableDivisions" 
                    valueKey="id" 
                    labelKey="name" 
                    placeholder="كل الأقسام" 
                    :disabled="filterWorkplaces.length > 0 && availableDivisions.length === 0"
                    disabledPlaceholder="لا توجد أقسام تابعة" """
content = content.replace(html_old_div, html_new_div)

html_old_unit = """:options="coreStore.units" 
                    valueKey="id" 
                    labelKey="name" 
                    placeholder="كل الوحدات" """

html_new_unit = """:options="availableUnits" 
                    valueKey="id" 
                    labelKey="name" 
                    placeholder="كل الوحدات" 
                    :disabled="filterDivision.length > 0 && availableUnits.length === 0"
                    disabledPlaceholder="لا توجد وحدات تابعة" """
content = content.replace(html_old_unit, html_new_unit)


# 3. Add watchers to clear division/unit if their parent changes and the selected item is no longer valid
watcher_script = """
watch(filterWorkplaces, () => {
  const validDivIds = availableDivisions.value.map((d: any) => d.id)
  filterDivision.value = filterDivision.value.filter(id => validDivIds.includes(id))
})

watch(filterDivision, () => {
  const validUnitIds = availableUnits.value.map((u: any) => u.id)
  filterUnit.value = filterUnit.value.filter(id => validUnitIds.includes(id))
})
"""

# Place watcher right after the availableUnits computation
content = content.replace("return coreStore.units.filter((u: any) => filterDivision.value.includes(u.division))\n})", "return coreStore.units.filter((u: any) => filterDivision.value.includes(u.division))\n})\n" + watcher_script)

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(content)

print("Divisions logic fixed.")
