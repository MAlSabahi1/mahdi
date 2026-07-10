<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.regions_config')" />
    
    <div class="space-y-6 text-start" dir="rtl">
      <!-- Action Bar -->
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white dark:bg-gray-900 p-4 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
          <Map class="w-5 h-5 text-blue-500" />
          إدارة المحافظات والمديريات
        </h3>
        <button @click="handleAddRegion" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-sm font-bold flex items-center gap-2 transition-colors shadow-sm cursor-pointer">
          <Plus class="w-4 h-4" />
          إضافة محافظة جديدة
        </button>
      </div>

      <!-- Master-Detail Layout -->
      <div class="flex flex-col lg:flex-row gap-6">
        <!-- Sidebar List (Master) -->
        <div class="w-full lg:w-1/3 space-y-4">
          <!-- Search -->
          <div class="relative">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="ابحث عن محافظة..." 
              class="w-full pl-10 pr-10 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            >
            <Search class="w-5 h-5 text-gray-400 absolute top-3.5 right-3" />
          </div>

          <!-- Regions List -->
          <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm overflow-hidden flex flex-col h-[600px]">
            <div class="p-4 border-b border-gray-100 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-800/50">
              <span class="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">قائمة المحافظات ({{ filteredRegions.length }})</span>
            </div>
            <div class="overflow-y-auto flex-1 p-2 space-y-1">
              <button 
                v-for="region in filteredRegions" 
                :key="region.id"
                @click="selectedRegion = region"
                class="w-full flex items-center justify-between p-3 rounded-xl text-right transition-all cursor-pointer"
                :class="selectedRegion?.id === region.id ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 font-bold' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800/50'"
              >
                <div class="flex items-center gap-3">
                  <MapPin class="w-4 h-4" :class="selectedRegion?.id === region.id ? 'text-blue-500' : 'text-gray-400'" />
                  <span>{{ region.name }}</span>
                </div>
                <span class="text-xs px-2 py-1 rounded-md" :class="selectedRegion?.id === region.id ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300' : 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'">
                  {{ region.districts.length }}
                </span>
              </button>
            </div>
          </div>
        </div>

        <!-- Detail View -->
        <div class="w-full lg:w-2/3">
          <div v-if="selectedRegion" class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm overflow-hidden h-full flex flex-col">
            <!-- Header -->
            <div class="p-6 border-b border-gray-100 dark:border-gray-800 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-gradient-to-l from-transparent to-gray-50/50 dark:to-gray-800/20">
              <div>
                <h2 class="text-2xl font-black text-gray-900 dark:text-white flex items-center gap-2">
                  {{ selectedRegion.name }}
                </h2>
                <div class="flex items-center gap-4 mt-2 text-sm text-gray-500 dark:text-gray-400">
                  <span class="flex items-center gap-1"><Hash class="w-4 h-4" /> كود: {{ selectedRegion.code }}</span>
                  <span class="flex items-center gap-1"><Users class="w-4 h-4" /> الكثافة: {{ selectedRegion.population }}</span>
                </div>
              </div>
              <div class="flex items-center gap-2 shrink-0">
                <button @click="handleEditRegion(selectedRegion)" class="p-2 text-blue-600 hover:bg-blue-50 dark:text-blue-400 dark:hover:bg-blue-900/20 rounded-xl transition-colors cursor-pointer" title="تعديل المحافظة">
                  <Edit class="w-5 h-5" />
                </button>
                <button @click="handleDeleteRegion(selectedRegion.id)" class="p-2 text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20 rounded-xl transition-colors cursor-pointer" title="حذف المحافظة">
                  <Trash2 class="w-5 h-5" />
                </button>
              </div>
            </div>

            <!-- Districts List -->
            <div class="p-6 flex-1 overflow-y-auto">
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-bold text-gray-900 dark:text-white text-lg">المديريات التابعة ({{ selectedRegion.districts.length }})</h3>
                <button @click="handleAddDistrict" class="text-sm font-bold text-emerald-600 bg-emerald-50 hover:bg-emerald-100 dark:bg-emerald-900/20 dark:text-emerald-400 dark:hover:bg-emerald-900/40 px-3 py-1.5 rounded-lg flex items-center gap-1 transition-colors cursor-pointer">
                  <Plus class="w-4 h-4" /> إضافة مديرية
                </button>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-for="district in selectedRegion.districts" :key="district.id" class="border border-gray-100 dark:border-gray-800 rounded-xl p-4 hover:border-blue-200 dark:hover:border-blue-800/50 transition-colors bg-gray-50/30 dark:bg-gray-800/20 flex flex-col group">
                  <div class="flex justify-between items-start mb-2">
                    <h4 class="font-bold text-gray-900 dark:text-white flex items-center gap-1.5">
                      <Building2 class="w-4 h-4 text-gray-400" />
                      {{ district.name }}
                    </h4>
                    <div class="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1">
                      <button @click="handleEditDistrict(district)" class="p-1 text-gray-400 hover:text-blue-500 rounded cursor-pointer">
                        <Edit class="w-3.5 h-3.5" />
                      </button>
                      <button @click="handleDeleteDistrict(district.id)" class="p-1 text-gray-400 hover:text-red-500 rounded cursor-pointer">
                        <Trash2 class="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                  <div class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-3 mt-auto pt-2 border-t border-gray-100 dark:border-gray-800">
                    <span class="flex items-center gap-1"><Users class="w-3 h-3" /> أفراد: {{ district.personnelCount }}</span>
                    <span class="flex items-center gap-1"><Shield class="w-3 h-3" /> قطاعات: {{ district.sectors }}</span>
                  </div>
                </div>
              </div>

              <div v-if="selectedRegion.districts.length === 0" class="text-center py-12 text-gray-400">
                لا توجد مديريات مسجلة لهذه المحافظة.
              </div>
            </div>
          </div>
          <div v-else class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm flex flex-col items-center justify-center h-[600px] text-gray-400">
            <Map class="w-16 h-16 mb-4 opacity-20" />
            <p class="font-bold text-lg text-gray-500">الرجاء اختيار محافظة من القائمة لعرض تفاصيلها</p>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import Swal from 'sweetalert2'
import { Map, Plus, Search, MapPin, Hash, Users, Edit, Trash2, Building2, Shield } from 'lucide-vue-next'
import api from '@/lib/api'

const { t } = useI18n()

const regions = ref<any[]>([])
const isLoading = ref(true)
const searchQuery = ref('')
const selectedRegion = ref<any>(null)

const fetchRegions = async () => {
  isLoading.value = true
  try {
    const res = await api.get('/dictionaries/geo/governorates/')
    const govs = res.data.results || res.data || []
    
    // For each governorate, fetch its districts
    const regionsWithDistricts = await Promise.all(govs.map(async (gov: any) => {
      let districts: any[] = []
      try {
        const distRes = await api.get(`/dictionaries/geo/districts/?governorate=${gov.id}`)
        const distData = distRes.data.results || distRes.data || []
        districts = distData.map((d: any) => ({
          id: d.id,
          name: d.name_ar,
          personnelCount: 0,
          sectors: 0
        }))
      } catch (e) {
        // Districts fetch failed silently
      }
      return {
        id: gov.id,
        name: gov.name_ar,
        code: gov.phone_numbering_plan || '-',
        population: gov.capital_name_ar || '-',
        districts
      }
    }))
    
    regions.value = regionsWithDistricts
    if (regions.value.length > 0 && !selectedRegion.value) {
      selectedRegion.value = regions.value[0]
    }
  } catch (error) {
    console.error('Error fetching regions', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchRegions()
})

const filteredRegions = computed(() => {
  if (!searchQuery.value) return regions.value
  return regions.value.filter(r => r.name.includes(searchQuery.value) || r.code.includes(searchQuery.value.toUpperCase()))
})

// Actions
const handleAddRegion = () => {
  Swal.fire({
    title: 'إضافة محافظة جديدة',
    html: `
      <input id="swal-input1" class="swal2-input" placeholder="اسم المحافظة (مثال: الحديدة)" dir="rtl">
      <input id="swal-input2" class="swal2-input" placeholder="الاسم بالإنجليزي (اختياري)" dir="ltr">
    `,
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: 'حفظ',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#3b82f6',
    showLoaderOnConfirm: true,
    preConfirm: async () => {
      const name_ar = (document.getElementById('swal-input1') as HTMLInputElement).value
      const name_en = (document.getElementById('swal-input2') as HTMLInputElement).value
      if (!name_ar) { Swal.showValidationMessage('اسم المحافظة مطلوب'); return false }
      try {
        await api.post('/dictionaries/geo/governorates/', { name_ar, name_en })
        return true
      } catch (e: any) {
        Swal.showValidationMessage(e.response?.data?.name_ar?.[0] || 'حدث خطأ أثناء الحفظ')
        return false
      }
    },
    allowOutsideClick: () => !Swal.isLoading()
  }).then((result) => {
    if (result.isConfirmed) {
      fetchRegions()
      Swal.fire('تمت الإضافة', 'تم إضافة المحافظة بنجاح', 'success')
    }
  })
}

const handleEditRegion = (region: any) => {
  Swal.fire({
    title: 'تعديل بيانات المحافظة',
    html: `
      <input id="swal-input1" class="swal2-input" value="${region.name}" placeholder="اسم المحافظة" dir="rtl">
    `,
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: 'تحديث',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#3b82f6',
    showLoaderOnConfirm: true,
    preConfirm: async () => {
      const name_ar = (document.getElementById('swal-input1') as HTMLInputElement).value
      if (!name_ar) { Swal.showValidationMessage('اسم المحافظة مطلوب'); return false }
      try {
        await api.patch(`/dictionaries/geo/governorates/${region.id}/`, { name_ar })
        return true
      } catch (e: any) {
        Swal.showValidationMessage('حدث خطأ أثناء التحديث')
        return false
      }
    },
    allowOutsideClick: () => !Swal.isLoading()
  }).then((result) => {
    if (result.isConfirmed) {
      fetchRegions()
      Swal.fire('تم التحديث', 'تم تحديث بيانات المحافظة', 'success')
    }
  })
}

const handleDeleteRegion = (id: number) => {
  Swal.fire({
    title: 'تأكيد الحذف',
    text: 'هل أنت متأكد من حذف هذه المحافظة وكافة المديريات التابعة لها؟ (لا يمكن التراجع عن هذا الإجراء)',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#d1d5db',
    confirmButtonText: 'نعم، احذف',
    cancelButtonText: 'إلغاء',
    showLoaderOnConfirm: true,
    preConfirm: async () => {
      try {
        await api.delete(`/dictionaries/geo/governorates/${id}/`)
        return true
      } catch (e: any) {
        Swal.showValidationMessage('لا يمكن حذف هذه المحافظة — قد تكون مرتبطة بسجلات أخرى')
        return false
      }
    },
    allowOutsideClick: () => !Swal.isLoading()
  }).then((result) => {
    if (result.isConfirmed) {
      if (selectedRegion.value?.id === id) {
        selectedRegion.value = null
      }
      fetchRegions()
      Swal.fire('تم الحذف', 'تم حذف المحافظة بنجاح.', 'success')
    }
  })
}

const handleAddDistrict = () => {
  if (!selectedRegion.value) return
  Swal.fire({
    title: 'إضافة مديرية جديدة',
    input: 'text',
    inputPlaceholder: 'اسم المديرية',
    showCancelButton: true,
    confirmButtonText: 'إضافة',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#10b981',
    showLoaderOnConfirm: true,
    inputValidator: (value) => {
      if (!value) return 'اسم المديرية مطلوب!'
    },
    preConfirm: async (name_ar: string) => {
      try {
        await api.post('/dictionaries/geo/districts/', {
          name_ar,
          governorate: selectedRegion.value.id
        })
        return true
      } catch (e: any) {
        Swal.showValidationMessage(e.response?.data?.name_ar?.[0] || 'حدث خطأ أثناء الإضافة')
        return false
      }
    },
    allowOutsideClick: () => !Swal.isLoading()
  }).then((result) => {
    if (result.isConfirmed) {
      const selectedId = selectedRegion.value?.id
      fetchRegions().then(() => {
        selectedRegion.value = regions.value.find(r => r.id === selectedId) || regions.value[0]
      })
      Swal.fire('تمت الإضافة', 'تم إضافة المديرية بنجاح', 'success')
    }
  })
}

const handleEditDistrict = (district: any) => {
  Swal.fire({
    title: 'تعديل اسم المديرية',
    input: 'text',
    inputValue: district.name,
    showCancelButton: true,
    confirmButtonText: 'تحديث',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#3b82f6',
    showLoaderOnConfirm: true,
    inputValidator: (value) => {
      if (!value) return 'اسم المديرية مطلوب!'
    },
    preConfirm: async (name_ar: string) => {
      try {
        await api.patch(`/dictionaries/geo/districts/${district.id}/`, { name_ar })
        return true
      } catch (e: any) {
        Swal.showValidationMessage('حدث خطأ أثناء التحديث')
        return false
      }
    },
    allowOutsideClick: () => !Swal.isLoading()
  }).then((result) => {
    if (result.isConfirmed) {
      const selectedId = selectedRegion.value?.id
      fetchRegions().then(() => {
        selectedRegion.value = regions.value.find(r => r.id === selectedId) || regions.value[0]
      })
      Swal.fire('تم التحديث', 'تم تحديث اسم المديرية', 'success')
    }
  })
}

const handleDeleteDistrict = (id: number) => {
  Swal.fire({
    title: 'تأكيد الحذف',
    text: 'هل أنت متأكد من حذف هذه المديرية؟',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#d1d5db',
    confirmButtonText: 'نعم، احذف',
    cancelButtonText: 'إلغاء',
    showLoaderOnConfirm: true,
    preConfirm: async () => {
      try {
        await api.delete(`/dictionaries/geo/districts/${id}/`)
        return true
      } catch (e: any) {
        Swal.showValidationMessage('لا يمكن حذف هذه المديرية — قد تكون مرتبطة بسجلات أخرى')
        return false
      }
    },
    allowOutsideClick: () => !Swal.isLoading()
  }).then((result) => {
    if (result.isConfirmed) {
      const selectedId = selectedRegion.value?.id
      fetchRegions().then(() => {
        selectedRegion.value = regions.value.find(r => r.id === selectedId) || regions.value[0]
      })
      Swal.fire('تم الحذف', 'تم حذف المديرية بنجاح.', 'success')
    }
  })
}
</script>
