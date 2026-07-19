import re

with open('FrontEnd/src/components/common/MultiSelect.vue', 'r') as f:
    content = f.read()

# 1. Update Template: Add search input
search_input_html = """
        <!-- Search Input -->
        <div class="px-2 pb-2 pt-1 sticky top-0 bg-white dark:bg-gray-800 z-10 border-b border-gray-100 dark:border-gray-700">
          <div class="relative">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="ابحث هنا..." 
              class="w-full h-9 pl-3 pr-8 rounded-md bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/50 dark:text-white"
            />
            <svg class="absolute right-2.5 top-2.5 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
        """

content = content.replace(
    '<div class="space-y-1">',
    '<div class="space-y-1">' + search_input_html
)


# 2. Update Template to use filteredOptions instead of options
content = content.replace('v-if="options.length > 0"', 'v-if="filteredOptions.length > 0"')
content = content.replace('v-for="(group, gIdx) in options"', 'v-for="(group, gIdx) in filteredOptions"')
content = content.replace('v-for="opt in options"', 'v-for="opt in filteredOptions"')
content = content.replace('v-if="!options || options.length === 0"', 'v-if="!filteredOptions || filteredOptions.length === 0"')
content = content.replace(':checked="isAllSelected"', ':checked="isAllFilteredSelected"')

# 3. Add Script: searchQuery and filteredOptions
script_imports = "import { ref, computed } from 'vue'"
script_updates = """
const searchQuery = ref('')

const filteredOptions = computed(() => {
  if (!searchQuery.value) return props.options

  const query = searchQuery.value.toLowerCase()

  if (isGrouped.value) {
    return props.options.map((group: any) => {
      if (!group.options) return group
      return {
        ...group,
        options: group.options.filter((opt: any) => 
          String(opt[props.labelKey]).toLowerCase().includes(query)
        )
      }
    }).filter((group: any) => group.options && group.options.length > 0)
  }

  return props.options.filter((opt: any) => 
    String(opt[props.labelKey]).toLowerCase().includes(query)
  )
})

const flatFilteredOptionsLength = computed(() => {
  if (isGrouped.value) {
    return filteredOptions.value.reduce((acc: number, group: any) => acc + (group.options?.length || 0), 0)
  }
  return filteredOptions.value.length
})

const isAllFilteredSelected = computed(() => {
  if (flatFilteredOptionsLength.value === 0) return false
  
  if (isGrouped.value) {
    const allFilteredVals = filteredOptions.value.flatMap((g: any) => g.options.map((o: any) => o[props.valueKey]))
    return allFilteredVals.every((v: any) => internalValue.value.includes(v))
  }
  const allFilteredVals = filteredOptions.value.map((o: any) => o[props.valueKey])
  return allFilteredVals.every((v: any) => internalValue.value.includes(v))
})
"""

content = content.replace("const isOpen = ref(false)", "const isOpen = ref(false)\n" + script_updates)

# 4. Update toggleAll to use filteredOptions and preserve unchecked items
old_toggle = """const toggleAll = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked
  if (checked && props.options) {
    if (isGrouped.value) {
      const allVals: any[] = []
      props.options.forEach((group: any) => {
        if (group.options) {
          group.options.forEach((opt: any) => allVals.push(opt[props.valueKey]))
        }
      })
      internalValue.value = allVals
    } else {
      internalValue.value = props.options.map((opt: any) => opt[props.valueKey])
    }
  } else {
    internalValue.value = []
  }
}"""

new_toggle = """const toggleAll = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked
  let newVals = [...internalValue.value]
  
  if (checked) {
    if (isGrouped.value) {
      filteredOptions.value.forEach((group: any) => {
        if (group.options) {
          group.options.forEach((opt: any) => {
            if (!newVals.includes(opt[props.valueKey])) newVals.push(opt[props.valueKey])
          })
        }
      })
    } else {
      filteredOptions.value.forEach((opt: any) => {
        if (!newVals.includes(opt[props.valueKey])) newVals.push(opt[props.valueKey])
      })
    }
  } else {
    if (isGrouped.value) {
      const filteredVals = filteredOptions.value.flatMap((g: any) => g.options.map((o: any) => o[props.valueKey]))
      newVals = newVals.filter((v: any) => !filteredVals.includes(v))
    } else {
      const filteredVals = filteredOptions.value.map((o: any) => o[props.valueKey])
      newVals = newVals.filter((v: any) => !filteredVals.includes(v))
    }
  }
  
  internalValue.value = newVals
}"""

content = content.replace(old_toggle, new_toggle)


with open('FrontEnd/src/components/common/MultiSelect.vue', 'w') as f:
    f.write(content)

print("Search functionality added.")
