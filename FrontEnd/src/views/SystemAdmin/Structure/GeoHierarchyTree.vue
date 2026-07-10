<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.geo_tree')" />
    
    <div class="space-y-6 text-start" dir="rtl">
      <!-- Header & Search -->
      <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-6 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
        <div>
          <h2 class="text-xl font-black text-gray-900 dark:text-white flex items-center gap-2">
            <Network class="w-6 h-6 text-emerald-500" />
            شجرة الهيكل الجغرافي
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">تصفح وإدارة النطاقات والتقسيمات الجغرافية للنظام</p>
        </div>
        <div class="relative w-full md:w-96">
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="بحث في الهيكل الجغرافي..." 
            class="w-full pl-10 pr-10 py-2.5 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
          >
          <Search class="w-5 h-5 text-gray-400 absolute top-3 right-3" />
        </div>
      </div>

      <!-- Tree View -->
      <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-6 shadow-sm overflow-x-auto min-h-[500px]">
        
        <div class="min-w-[600px]">
          <!-- Level 1: Country -->
          <div v-for="country in filteredTree" :key="country.id" class="mb-4">
            <div class="flex items-center gap-2 p-3 rounded-xl bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors border border-gray-100 dark:border-gray-700">
              <button @click="country.expanded = !country.expanded" class="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg transition-colors cursor-pointer">
                <ChevronDown v-if="country.expanded" class="w-5 h-5 text-gray-500" />
                <ChevronLeft v-else class="w-5 h-5 text-gray-500" />
              </button>
              <Globe2 class="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
              <span class="font-black text-lg text-gray-900 dark:text-white">{{ country.name }}</span>
              <span class="mr-auto text-xs font-bold px-3 py-1 bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
                {{ country.children.length }} محافظات
              </span>
            </div>

            <!-- Level 2: Regions -->
            <div v-show="country.expanded" class="pr-8 mt-2 space-y-2 border-r-2 border-gray-100 dark:border-gray-800">
              <div v-for="region in country.children" :key="region.id" class="relative">
                <!-- Connector Line -->
                <div class="absolute right-[-32px] top-6 w-8 h-0.5 bg-gray-100 dark:bg-gray-800"></div>
                
                <div class="flex items-center gap-2 p-3 rounded-xl bg-white dark:bg-gray-900 hover:bg-blue-50/50 dark:hover:bg-blue-900/10 transition-colors border border-gray-100 dark:border-gray-800">
                  <button v-if="region.children && region.children.length > 0" @click="region.expanded = !region.expanded" class="p-1 hover:bg-blue-100 dark:hover:bg-blue-900/30 rounded-lg transition-colors cursor-pointer">
                    <ChevronDown v-if="region.expanded" class="w-4 h-4 text-blue-500" />
                    <ChevronLeft v-else class="w-4 h-4 text-gray-400" />
                  </button>
                  <div v-else class="w-6 h-6"></div> <!-- Spacer -->
                  <MapPin class="w-5 h-5 text-blue-500" />
                  <span class="font-bold text-gray-800 dark:text-gray-200">{{ region.name }}</span>
                  
                  <div class="mr-auto flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-500 bg-gray-50 dark:bg-gray-800 px-2 py-1 rounded-md">{{ region.code }}</span>
                    <button @click.stop="handleEditRegion(region)" class="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-colors cursor-pointer" title="تعديل">
                      <Settings2 class="w-4 h-4" />
                    </button>
                  </div>
                </div>

                <!-- Level 3: Districts -->
                <div v-show="region.expanded" class="pr-8 mt-2 space-y-2 border-r-2 border-gray-100 dark:border-gray-800">
                  <div v-for="district in region.children" :key="district.id" class="relative">
                    <div class="absolute right-[-32px] top-5 w-8 h-0.5 bg-gray-100 dark:bg-gray-800"></div>
                    
                    <div class="flex items-center gap-2 p-2.5 rounded-xl bg-gray-50/50 dark:bg-gray-800/20 hover:bg-gray-100 dark:hover:bg-gray-800/50 transition-colors border border-transparent hover:border-gray-200 dark:hover:border-gray-700 group">
                      <button v-if="district.children && district.children.length > 0" @click="district.expanded = !district.expanded" class="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg transition-colors cursor-pointer">
                        <ChevronDown v-if="district.expanded" class="w-4 h-4 text-emerald-500" />
                        <ChevronLeft v-else class="w-4 h-4 text-gray-400" />
                      </button>
                      <div v-else class="w-6 h-6"></div> <!-- Spacer -->
                      <Building2 class="w-4 h-4 text-gray-400" />
                      <span class="text-sm font-bold text-gray-700 dark:text-gray-300">{{ district.name }}</span>
                      
                      <div class="mr-auto flex items-center gap-4">
                        <span class="text-[10px] font-bold text-gray-500 flex items-center gap-1">
                          <Users class="w-3 h-3" /> {{ district.population }}
                        </span>
                        <div class="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1">
                          <button @click.stop="handleAddSubDistrict(district)" class="p-1 text-gray-400 hover:text-emerald-600 rounded cursor-pointer" title="إضافة عزلة"><Plus class="w-3.5 h-3.5" /></button>
                          <button @click.stop="handleEditDistrict(district)" class="p-1 text-gray-400 hover:text-blue-600 rounded cursor-pointer" title="إعدادات"><Settings2 class="w-3.5 h-3.5" /></button>
                        </div>
                      </div>
                    </div>

                    <!-- Level 4: Sub-Districts -->
                    <div v-show="district.expanded" class="pr-8 mt-2 space-y-2 border-r-2 border-gray-100 dark:border-gray-800">
                      <div v-for="sub in district.children" :key="sub.id" class="relative">
                        <div class="absolute right-[-32px] top-4 w-8 h-0.5 bg-gray-100 dark:bg-gray-800"></div>
                        <div class="flex items-center gap-2 p-2 rounded-xl bg-gray-50/30 dark:bg-gray-800/10 hover:bg-gray-100 dark:hover:bg-gray-800/50 transition-colors">
                          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                          <span class="text-sm text-gray-600 dark:text-gray-400">{{ sub.name }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

              </div>
            </div>

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
import { Network, Search, ChevronDown, ChevronLeft, Globe2, MapPin, Building2, Users, Settings2, Plus } from 'lucide-vue-next'
import Swal from 'sweetalert2'
import api from '@/lib/api'

const { t } = useI18n()
const searchQuery = ref('')
const isLoading = ref(true)

const treeData = ref<any[]>([])

const fetchTree = async () => {
  isLoading.value = true
  try {
    const res = await api.get('/dictionaries/geo/governorates/tree/')
    const govs = res.data.data || res.data.results || res.data || []
    
    treeData.value = [{
      id: 'root-1',
      name: 'الجمهورية اليمنية',
      expanded: true,
      children: govs.map((gov: any) => ({
        id: `gov-${gov.id}`,
        db_id: gov.id,
        name: gov.name_ar,
        code: gov.name_en || '-',
        expanded: false,
        children: (gov.districts || []).map((dist: any) => ({
          id: dist.id,
          name: dist.name_ar,
          population: 0,
          expanded: false,
          children: (dist.sub_districts || []).map((sub: any) => ({
            id: sub.id,
            name: sub.name_ar
          }))
        }))
      }))
    }]
  } catch (error) {
    console.error('Error fetching geo tree', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchTree()
})

// Basic deep filter implementation
const filteredTree = computed(() => {
  if (!searchQuery.value) return treeData.value

  const q = searchQuery.value.toLowerCase()
  
  return treeData.value.map(country => {
    if (country.name.toLowerCase().includes(q)) return { ...country, expanded: true }
    
    const filteredRegions = country.children.filter((region: any) => {
      if (region.name.toLowerCase().includes(q) || (region.code && region.code.toLowerCase().includes(q))) return true
      return region.children?.some((dist: any) => dist.name.toLowerCase().includes(q) || dist.children?.some((sub: any) => sub.name.toLowerCase().includes(q)))
    }).map((region: any) => {
      return {
        ...region,
        expanded: true,
        children: region.children?.filter((dist: any) => 
          region.name.toLowerCase().includes(q) || dist.name.toLowerCase().includes(q) || dist.children?.some((sub: any) => sub.name.toLowerCase().includes(q))
        ).map((dist: any) => ({
          ...dist,
          expanded: true,
          children: dist.children?.filter((sub: any) => 
            region.name.toLowerCase().includes(q) || dist.name.toLowerCase().includes(q) || sub.name.toLowerCase().includes(q)
          )
        }))
      }
    })

    if (filteredRegions.length > 0) {
      return { ...country, expanded: true, children: filteredRegions }
    }
    return null
  }).filter(Boolean) as any[]
})

const handleAddSubDistrict = (district: any) => {
  Swal.fire({
    title: `إضافة عزلة جديدة في ${district.name}`,
    input: 'text',
    inputPlaceholder: 'اسم العزلة',
    showCancelButton: true,
    confirmButtonText: 'إضافة',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#10b981',
    showLoaderOnConfirm: true,
    inputValidator: (value) => {
      if (!value) return 'اسم العزلة مطلوب!'
    },
    preConfirm: async (name_ar: string) => {
      try {
        await api.post('/dictionaries/geo/sub-districts/', {
          name_ar,
          district: district.id
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
      fetchTree()
      Swal.fire('تمت الإضافة', 'تم إضافة العزلة بنجاح', 'success')
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
      fetchTree()
      Swal.fire('تم التحديث', 'تم تحديث اسم المديرية', 'success')
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
        await api.patch(`/dictionaries/geo/governorates/${region.db_id}/`, { name_ar })
        return true
      } catch (e: any) {
        Swal.showValidationMessage('حدث خطأ أثناء التحديث')
        return false
      }
    },
    allowOutsideClick: () => !Swal.isLoading()
  }).then((result) => {
    if (result.isConfirmed) {
      fetchTree()
      Swal.fire('تم التحديث', 'تم تحديث بيانات المحافظة', 'success')
    }
  })
}

</script>
