<template>
  <div class="relative">
    <!-- Backdrop to close dropdown -->
    <div v-if="isOpen" @click="isOpen = false" class="fixed inset-0 z-40"></div>
    
    <!-- Select Button -->
    <button 
      type="button"
      @click="isOpen = !isOpen"
      :disabled="disabled"
      class="relative z-10 flex h-11 w-full items-center justify-between rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      <span class="truncate">
        {{ displayText }}
      </span>
      <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 20 20" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" />
      </svg>
    </button>
    
    <!-- Dropdown Menu -->
    <div v-if="isOpen" class="absolute z-50 mt-1 max-h-60 w-full overflow-y-auto rounded-xl border border-gray-200 bg-white p-2 shadow-lg dark:border-gray-700 dark:bg-gray-800">
      <div class="space-y-1">
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
        
        <!-- Select All Option (Global) -->
        <label v-if="filteredOptions.length > 0" class="flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2 hover:bg-gray-50 dark:hover:bg-gray-700">
          <input 
            type="checkbox" 
            :checked="isAllFilteredSelected" 
            @change="toggleAll" 
            class="h-4 w-4 rounded border-gray-300 text-brand-600 focus:ring-brand-500" 
          />
          <span class="text-sm font-bold text-gray-900 dark:text-gray-100">تحديد الكل</span>
        </label>
        <div v-if="filteredOptions.length > 0" class="h-px bg-gray-100 dark:bg-gray-700 my-1"></div>
        
        <!-- Grouped Options -->
        <template v-if="isGrouped">
          <div v-for="(group, gIdx) in filteredOptions" :key="'group_' + gIdx" class="mb-2">
            <div v-if="group.options && group.options.length > 0">
              <!-- Group Header with Group Select All -->
              <label class="flex cursor-pointer items-center gap-3 rounded-lg px-3 py-1.5 bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                <input 
                  type="checkbox" 
                  :checked="isGroupSelected(group)" 
                  @change="toggleGroup($event, group)" 
                  class="h-4 w-4 rounded border-gray-300 text-brand-600 focus:ring-brand-500" 
                />
                <span class="text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-wider">{{ group.label }}</span>
              </label>
              
              <!-- Group Items -->
              <div class="pl-2 rtl:pl-0 rtl:pr-2 mt-1 space-y-1">
                <label v-for="opt in group.options" :key="opt[valueKey]" class="flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2 hover:bg-gray-50 dark:hover:bg-gray-700">
                  <input 
                    type="checkbox" 
                    :value="opt[valueKey]" 
                    v-model="internalValue" 
                    class="h-4 w-4 rounded border-gray-300 text-brand-600 focus:ring-brand-500" 
                  />
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ opt[labelKey] }}</span>
                </label>
              </div>
            </div>
          </div>
        </template>
        
        <!-- Flat Options -->
        <template v-else>
          <label v-for="opt in filteredOptions" :key="opt[valueKey]" class="flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2 hover:bg-gray-50 dark:hover:bg-gray-700">
            <input 
              type="checkbox" 
              :value="opt[valueKey]" 
              v-model="internalValue" 
              class="h-4 w-4 rounded border-gray-300 text-brand-600 focus:ring-brand-500" 
            />
            <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ opt[labelKey] }}</span>
          </label>
        </template>
        
        <!-- Empty State -->
        <div v-if="!filteredOptions || filteredOptions.length === 0" class="px-3 py-2 text-sm text-gray-500 dark:text-gray-400 text-center">
          لا توجد بيانات
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  options: {
    type: Array,
    default: () => []
  },
  placeholder: {
    type: String,
    default: 'الكل'
  },
  disabledPlaceholder: {
    type: String,
    default: 'اختر...'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  valueKey: {
    type: String,
    default: 'id'
  },
  labelKey: {
    type: String,
    default: 'name'
  }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)

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


const internalValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const isGrouped = computed(() => {
  return props.options.length > 0 && 'options' in (props.options[0] as any)
})

const flatOptionsLength = computed(() => {
  if (isGrouped.value) {
    return props.options.reduce((acc: number, group: any) => acc + (group.options?.length || 0), 0 as number)
  }
  return props.options.length as number
})

const isAllSelected = computed(() => {
  return flatOptionsLength.value > 0 && (internalValue.value?.length || 0) === flatOptionsLength.value
})

const displayText = computed(() => {
  if (props.disabled) return props.disabledPlaceholder
  if (!internalValue.value || internalValue.value.length === 0) return props.placeholder
  if (isAllSelected.value) return 'الكل'
  return `محدد (${internalValue.value.length})`
})

const toggleAll = (e: Event) => {
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
}

const isGroupSelected = (group: any) => {
  if (!group.options || group.options.length === 0) return false
  const groupVals = group.options.map((opt: any) => opt[props.valueKey])
  return groupVals.every((val: any) => internalValue.value.includes(val))
}

const toggleGroup = (e: Event, group: any) => {
  if (!group.options) return
  const checked = (e.target as HTMLInputElement).checked
  const groupVals = group.options.map((opt: any) => opt[props.valueKey])
  
  if (checked) {
    // Add all group values that aren't already selected
    const newVals = [...internalValue.value]
    groupVals.forEach((val: any) => {
      if (!newVals.includes(val)) newVals.push(val)
    })
    internalValue.value = newVals
  } else {
    // Remove all group values
    internalValue.value = internalValue.value.filter((val: any) => !groupVals.includes(val))
  }
}
</script>
