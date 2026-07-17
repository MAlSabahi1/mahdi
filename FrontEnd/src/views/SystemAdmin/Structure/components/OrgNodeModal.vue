<template>
  <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center z-50 p-4 sm:p-6" dir="rtl">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-gray-900/40 backdrop-blur-md transition-opacity" @click="handleClose"></div>

    <!-- Modal Content -->
    <div class="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl w-full max-w-2xl overflow-hidden relative z-10 flex flex-col border border-gray-100 dark:border-gray-800" 
         role="dialog" aria-modal="true">
      
      <!-- Header -->
      <div class="px-8 py-6 border-b border-gray-100 dark:border-gray-800 flex items-center justify-between bg-gray-50/50 dark:bg-gray-800/50">
        <div class="flex items-center gap-4">
          <div :class="`w-12 h-12 rounded-2xl flex items-center justify-center ${themeColorClass}`">
            <component :is="icon" class="w-6 h-6" />
          </div>
          <div>
            <h3 class="text-xl font-black text-gray-900 dark:text-white">{{ title }}</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ subtitle }}</p>
          </div>
        </div>
        <button @click="handleClose" class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-xl transition-colors cursor-pointer">
          <X class="w-6 h-6" />
        </button>
      </div>

      <!-- Body Form -->
      <div class="p-8 overflow-y-auto max-h-[70vh]">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          <!-- Name Field -->
          <div class="col-span-1 md:col-span-2">
            <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">الاسم <span class="text-red-500">*</span></label>
            <input type="text" v-model="formData.name" placeholder="أدخل اسم الجهة..." 
                   class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all">
          </div>

          <!-- Code Field -->
          <div>
            <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">الكود (اختياري)</label>
            <input type="text" v-model="formData.code" dir="ltr" placeholder="أدخل الكود..." 
                   class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white text-left focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all">
          </div>

          <!-- Order Field -->
          <div>
            <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">الترتيب الزمني / الهرمي</label>
            <input type="number" v-model="formData.order" min="0" placeholder="مثال: 1" 
                   class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all">
          </div>

          <!-- Head Position -->
          <div>
            <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">منصب المدير (إن وجد)</label>
            <input type="text" v-model="formData.head_position" placeholder="مثال: القائم بأعمال القسم" 
                   class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all">
          </div>

          <!-- Head (Personnel Master) -->
          <div class="relative">
            <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">مدير / رئيس الجهة</label>
            
            <div v-if="formData.head" class="w-full px-4 py-3 rounded-xl border border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-900/20 flex items-center justify-between">
              <div class="flex items-center gap-2 text-emerald-700 dark:text-emerald-400 font-bold">
                <Shield class="w-4 h-4" /> 
                <span>{{ selectedPersonnelName }}</span>
              </div>
              <button @click="clearPersonnelSelection" class="text-xs text-red-500 hover:text-red-700 bg-white dark:bg-gray-800 border border-red-200 dark:border-red-900/50 rounded-md px-2 py-1 transition-colors">تغيير</button>
            </div>
            
            <div v-else class="relative">
              <input type="text" v-model="managerSearchQuery" @input="handlePersonnelSearch" @focus="showPersonnelDropdown = true" placeholder="ابحث بالاسم أو الرقم العسكري..." 
                     class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all">
              <span v-if="isSearchingPersonnel" class="absolute left-3 top-3.5 w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></span>
            </div>
            
            <!-- Dropdown -->
            <div v-if="!formData.head && showPersonnelDropdown && (personnelSearchResults.length > 0 || managerSearchQuery)" class="absolute z-50 w-full mt-1 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 max-h-48 overflow-y-auto">
              <div v-if="personnelSearchResults.length === 0 && !isSearchingPersonnel" class="p-4 text-sm text-gray-500 text-center">لا توجد نتائج</div>
              <button v-for="person in personnelSearchResults" :key="person.military_number" @click="selectPersonnel(person)" type="button"
                      class="w-full text-right px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700 border-b border-gray-50 dark:border-gray-700/50 last:border-0 transition-colors">
                <div class="font-bold text-gray-800 dark:text-gray-200">{{ person.full_name }}</div>
                <div class="text-xs text-gray-500 mt-1 flex items-center gap-2">
                  <span class="bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 px-1.5 py-0.5 rounded">{{ person.military_number }}</span>
                  <span v-if="person.current_rank_name">{{ person.current_rank_name }}</span>
                </div>
              </button>
            </div>
          </div>

          <!-- Geo Governorate (For Sectors Only) -->
          <div v-if="requiresGeoGov" class="col-span-1 md:col-span-2">
            <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">المحافظة الجغرافية <span class="text-red-500">*</span></label>
            <select v-model="formData.geo_governorate" class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all cursor-pointer">
              <option value="">— اختر المحافظة الجغرافية —</option>
              <option v-for="gov in geoGovOptions" :key="gov.id" :value="gov.id">{{ gov.name_ar }}</option>
            </select>
          </div>
          
          <!-- Department Type (For Adding Depts to Sectors Only) -->
          <div v-if="isDeptSelection" class="col-span-1 md:col-span-2">
            <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">نوع الجهة <span class="text-red-500">*</span></label>
            <select v-model="formData.deptType" class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all cursor-pointer">
              <option value="central-departments">إدارة مركزية</option>
              <option value="branches">فرع</option>
              <option value="district-police">أمن مديرية / قسم شرطة</option>
            </select>
          </div>

          <!-- Is Active Toggle -->
          <div class="col-span-1 md:col-span-2 flex items-center justify-between mt-2 p-4 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-700">
            <div>
              <h4 class="font-bold text-gray-900 dark:text-white">حالة التفعيل</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">تحديد ما إذا كانت هذه الجهة نشطة ومفعلة ضمن الهيكل</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="formData.is_active" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer dark:bg-gray-700 peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:right-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-emerald-500"></div>
            </label>
          </div>

        </div>
        
        <!-- Error Message -->
        <div v-if="errorMessage" class="mt-6 p-4 rounded-xl bg-red-50 dark:bg-red-900/20 border border-red-100 dark:border-red-900/50 flex items-start gap-3">
          <AlertCircle class="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
          <p class="text-sm font-medium text-red-600 dark:text-red-400">{{ errorMessage }}</p>
        </div>
      </div>

      <!-- Footer -->
      <div class="px-8 py-5 border-t border-gray-100 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-800/50 flex items-center justify-end gap-3">
        <button @click="handleClose" class="px-5 py-2.5 rounded-xl text-sm font-bold text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors cursor-pointer">
          إلغاء
        </button>
        <button @click="handleSubmit" :disabled="isSubmitting" class="px-6 py-2.5 rounded-xl text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 active:scale-95 transition-all flex items-center gap-2 cursor-pointer disabled:opacity-70 disabled:cursor-not-allowed">
          <span v-if="isSubmitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
          <Save v-else class="w-4 h-4" />
          {{ mode === 'add' ? 'حفظ وإضافة' : 'حفظ التعديلات' }}
        </button>
      </div>
      
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { X, Save, Shield, Briefcase, Layers, Box, AlertCircle, Building } from 'lucide-vue-next'
import api from '@/lib/api'

const props = defineProps<{
  isOpen: boolean
  mode: 'add' | 'edit'
  nodeType: 'sector' | 'dept' | 'division' | 'unit'
  initialData?: any
  geoGovOptions?: any[]
}>()

const emit = defineEmits(['close', 'submit'])

const isSubmitting = ref(false)
const errorMessage = ref('')

// Personnel Search State
const managerSearchQuery = ref('')
const personnelSearchResults = ref<any[]>([])
const isSearchingPersonnel = ref(false)
const showPersonnelDropdown = ref(false)
const selectedPersonnelName = ref('')
let searchTimeout: any = null

const formData = ref({
  name: '',
  code: '',
  order: 0,
  head: '', // Store military_number
  head_position: '',
  is_active: true,
  geo_governorate: '',
  deptType: 'central-departments'
})

// UI Helpers
const title = computed(() => {
  if (props.mode === 'add') {
    if (props.nodeType === 'sector') return 'إضافة قطاع أمني جديد'
    if (props.nodeType === 'dept') return 'إضافة إدارة جديدة'
    if (props.nodeType === 'division') return 'إضافة قسم / فرع جديد'
    if (props.nodeType === 'unit') return 'إضافة وحدة جديدة'
  } else {
    return 'تعديل بيانات الجهة'
  }
  return ''
})

const subtitle = computed(() => {
  return props.mode === 'add' ? 'قم بتعبئة بيانات الجهة لإدراجها في الهيكل التنظيمي' : 'تحديث التفاصيل الخاصة بهذه الجهة'
})

const icon = computed(() => {
  if (props.nodeType === 'sector') return Shield
  if (props.nodeType === 'dept') return Briefcase
  if (props.nodeType === 'division') return Layers
  if (props.nodeType === 'unit') return Box
  return Building
})

const themeColorClass = computed(() => {
  if (props.nodeType === 'sector') return 'bg-blue-100 text-blue-600 dark:bg-blue-900/50 dark:text-blue-400'
  if (props.nodeType === 'dept') return 'bg-amber-100 text-amber-600 dark:bg-amber-900/50 dark:text-amber-400'
  if (props.nodeType === 'division') return 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/50 dark:text-emerald-400'
  return 'bg-purple-100 text-purple-600 dark:bg-purple-900/50 dark:text-purple-400'
})

const requiresGeoGov = computed(() => props.nodeType === 'sector' && props.mode === 'add')
const isDeptSelection = computed(() => props.nodeType === 'dept' && props.mode === 'add')

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    errorMessage.value = ''
    if (props.mode === 'edit' && props.initialData) {
      formData.value = {
        name: props.initialData.name || '',
        code: props.initialData.code || '',
        order: props.initialData.order || 0,
        head: props.initialData.head || '',
        head_position: props.initialData.head_position || '',
        is_active: props.initialData.is_active !== undefined ? props.initialData.is_active : true,
        geo_governorate: props.initialData.geo_governorate || '',
        deptType: props.initialData.type || 'central-departments'
      }
      if (props.initialData.head) {
        selectedPersonnelName.value = props.initialData.head
      } else {
        selectedPersonnelName.value = ''
      }
      managerSearchQuery.value = ''
    } else {
      formData.value = {
        name: '',
        code: '',
        order: 0,
        head: '',
        head_position: '',
        is_active: true,
        geo_governorate: '',
        deptType: 'central-departments'
      }
      managerSearchQuery.value = ''
      selectedPersonnelName.value = ''
    }
  }
})

// Search Personnel Logic
const handlePersonnelSearch = () => {
  if (!managerSearchQuery.value.trim()) {
    personnelSearchResults.value = []
    return
  }
  
  clearTimeout(searchTimeout)
  isSearchingPersonnel.value = true
  
  searchTimeout = setTimeout(async () => {
    try {
      const res = await api.get(`/personnel/?search=${managerSearchQuery.value}`)
      personnelSearchResults.value = res.data.results || res.data || []
    } catch (e) {
      console.error('Search failed', e)
    } finally {
      isSearchingPersonnel.value = false
    }
  }, 500)
}

const selectPersonnel = (person: any) => {
  formData.value.head = person.military_number
  selectedPersonnelName.value = person.full_name
  managerSearchQuery.value = ''
  showPersonnelDropdown.value = false
  personnelSearchResults.value = []
  
  // Auto-fill head position if empty
  if (!formData.value.head_position) {
    if (person.current_status) formData.value.head_position = person.current_status
    else if (person.current_rank_name) formData.value.head_position = `مدير برتبة ${person.current_rank_name}`
  }
}

const clearPersonnelSelection = () => {
  formData.value.head = ''
  selectedPersonnelName.value = ''
}

// Close dropdown when clicking outside
document.addEventListener('click', (e: any) => {
  if (!e.target.closest('.relative')) {
    showPersonnelDropdown.value = false
  }
})

const handleClose = () => {
  if (!isSubmitting.value) emit('close')
}

const handleSubmit = async () => {
  if (!formData.value.name.trim()) {
    errorMessage.value = 'الاسم مطلوب للجهة'
    return
  }
  if (requiresGeoGov.value && !formData.value.geo_governorate) {
    errorMessage.value = 'المحافظة الجغرافية مطلوبة'
    return
  }
  
  errorMessage.value = ''
  isSubmitting.value = true
  
  try {
    const payload: any = {
      name: formData.value.name,
      code: formData.value.code || undefined,
      order: Number(formData.value.order) || 0,
      head: formData.value.head || undefined,
      head_position: formData.value.head_position || undefined,
      is_active: formData.value.is_active,
    }
    
    if (requiresGeoGov.value) {
      payload.geo_governorate = formData.value.geo_governorate
    }
    
    // We emit the submit, parent handles API logic
    await emit('submit', { 
      payload, 
      deptType: formData.value.deptType 
    })
    
  } catch (err: any) {
    errorMessage.value = err.message || 'حدث خطأ أثناء الحفظ'
  } finally {
    isSubmitting.value = false
  }
}

// Allow parent to set error explicitly
const setError = (msg: string) => {
  errorMessage.value = msg
  isSubmitting.value = false
}

defineExpose({ setError })
</script>
