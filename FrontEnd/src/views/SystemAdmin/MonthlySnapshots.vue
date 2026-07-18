<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.monthly_snapshots')" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Top Header & Actions -->
      <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-6 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-gray-900 dark:text-white flex items-center gap-2">
            <DatabaseBackup class="w-7 h-7 text-emerald-500" />
            الأرشيف واللقطات الشهرية
          </h1>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            تجميد وتوثيق حالة القوة العاملة نهاية كل شهر كمرجع ثابت للرواتب والإحصائيات
          </p>
        </div>
        <div class="flex items-center gap-3">
          <button @click="openScheduleSettings" class="bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 px-4 py-2.5 rounded-xl text-sm font-bold flex items-center gap-2 transition-colors shrink-0 cursor-pointer">
            <Settings class="w-4 h-4" /> إعدادات الجدولة
          </button>
          <button 
            @click="generateSnapshot"
            :disabled="isGenerating"
            class="bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2.5 rounded-xl text-sm font-bold flex items-center gap-2 transition-all shrink-0 cursor-pointer disabled:opacity-70 disabled:cursor-not-allowed"
          >
            <Loader2 v-if="isGenerating" class="w-4 h-4 animate-spin" />
            <Camera v-else class="w-4 h-4" />
            {{ isGenerating ? 'جاري أخذ اللقطة...' : 'أخذ لقطة للشهر الحالي' }}
          </button>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-5 flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-blue-50 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400 shrink-0">
            <Archive class="w-6 h-6" />
          </div>
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400 font-bold mb-0.5">إجمالي اللقطات المؤرشفة</p>
            <h3 class="text-2xl font-black text-gray-900 dark:text-white">{{ snapshots.length }} لقطة</h3>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-5 flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-emerald-50 dark:bg-emerald-900/30 flex items-center justify-center text-emerald-600 dark:text-emerald-400 shrink-0">
            <HardDrive class="w-6 h-6" />
          </div>
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400 font-bold mb-0.5">المساحة المستهلكة</p>
            <h3 class="text-2xl font-black text-gray-900 dark:text-white">1.2 GB</h3>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-5 flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-amber-50 dark:bg-amber-900/30 flex items-center justify-center text-amber-600 dark:text-amber-400 shrink-0">
            <CalendarClock class="w-6 h-6" />
          </div>
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400 font-bold mb-0.5">موعد اللقطة التلقائية القادمة</p>
            <h3 class="text-lg font-black text-gray-900 dark:text-white mt-1" dir="ltr">2026-07-31 23:59</h3>
          </div>
        </div>
      </div>

      <!-- Snapshots Data Table -->
      <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 overflow-hidden shadow-sm">
        <div class="p-5 border-b border-gray-100 dark:border-gray-800 flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/20">
          <h3 class="font-bold text-gray-800 dark:text-gray-200 flex items-center gap-2">
            <History class="w-5 h-5 text-gray-400" />
            سجل اللقطات والأرشيف التاريخي
          </h3>
        </div>
        
        <DataTable
          :columns="columns"
          :data="snapshots"
          row-key="id"
          :search-placeholder="'ابحث عن لقطة بالاسم أو التاريخ...'"
        >
          <template #cell-status="{ row }">
            <span v-if="row.status === 'completed'" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-bold bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400">
              <CheckCircle class="w-3.5 h-3.5" />
              مكتمل ومعتمد
            </span>
            <span v-else-if="row.status === 'processing'" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-bold bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400">
              <Loader2 class="w-3.5 h-3.5 animate-spin" />
              جاري المعالجة
            </span>
          </template>

          <template #cell-actions="{ row }">
            <div class="flex items-center gap-2">
              <button @click="downloadSnapshot(row)" class="p-1.5 text-gray-400 hover:text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-900/30 rounded-lg transition-colors cursor-pointer" title="تنزيل نسخة Excel">
                <Download class="w-4 h-4" />
              </button>
              <button @click="viewSnapshot(row)" class="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-colors cursor-pointer" title="استعراض البيانات">
                <Eye class="w-4 h-4" />
              </button>
              <button @click="snapshotSettings(row)" class="p-1.5 text-gray-400 hover:text-amber-600 hover:bg-amber-50 dark:hover:bg-amber-900/30 rounded-lg transition-colors cursor-pointer" title="إعدادات اللقطة">
                <Settings2 class="w-4 h-4" />
              </button>
            </div>
          </template>
        </DataTable>
      </div>

      <!-- Schedule Settings Modal -->
      <div v-if="isScheduleModalOpen" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 sm:p-6">
        <div class="bg-white dark:bg-gray-900 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-800 w-full max-w-md overflow-hidden transform transition-all">
          <div class="p-5 border-b border-gray-100 dark:border-gray-800 flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/20">
            <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <Settings class="w-5 h-5 text-gray-500" />
              إعدادات الجدولة التلقائية
            </h3>
            <button @click="closeScheduleSettings" class="text-gray-400 hover:text-red-500 transition-colors">
              <X class="w-5 h-5" />
            </button>
          </div>
          
          <div class="p-5 space-y-5">
            <!-- Toggle Enable -->
            <label class="flex items-center justify-between cursor-pointer">
              <div>
                <span class="block text-sm font-bold text-gray-900 dark:text-white">تفعيل الأرشفة التلقائية</span>
                <span class="block text-xs text-gray-500 dark:text-gray-400 mt-0.5">سيقوم النظام بأخذ اللقطات دورياً دون تدخل بشري</span>
              </div>
              <div class="relative inline-flex items-center">
                <input type="checkbox" v-model="scheduleConfig.enabled" class="sr-only peer">
                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-emerald-300 dark:peer-focus:ring-emerald-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-emerald-600"></div>
              </div>
            </label>

            <!-- Day Selection -->
            <div>
              <label class="block text-sm font-bold text-gray-900 dark:text-white mb-2">يوم التنفيذ من كل شهر</label>
              <input type="number" min="1" max="28" v-model="scheduleConfig.schedule_day" :disabled="!scheduleConfig.enabled" class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 disabled:opacity-50 disabled:cursor-not-allowed">
              <p class="mt-1 text-xs text-gray-500">اختر يوماً بين 1 و 28</p>
            </div>

            <!-- Time Selection -->
            <div>
              <label class="block text-sm font-bold text-gray-900 dark:text-white mb-2">وقت التنفيذ</label>
              <input type="time" v-model="scheduleConfig.schedule_time" :disabled="!scheduleConfig.enabled" class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 disabled:opacity-50 disabled:cursor-not-allowed">
            </div>
          </div>

          <div class="p-4 border-t border-gray-100 dark:border-gray-800 flex justify-end gap-3 bg-gray-50/50 dark:bg-gray-800/20">
            <button @click="closeScheduleSettings" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:ring-4 focus:outline-none focus:ring-gray-200 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:text-white dark:focus:ring-gray-700 transition-colors">
              إلغاء
            </button>
            <button @click="saveScheduleSettings" :disabled="isSavingSchedule" class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 transition-colors disabled:opacity-70 disabled:cursor-not-allowed">
              <Loader2 v-if="isSavingSchedule" class="w-4 h-4 animate-spin" />
              حفظ الإعدادات
            </button>
          </div>
        </div>
      </div>

      <!-- Snapshot Details Modal -->
      <div v-if="isDetailsModalOpen" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 sm:p-6">
        <div class="bg-white dark:bg-gray-900 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-800 w-full max-w-5xl max-h-[85vh] flex flex-col overflow-hidden transform transition-all">
          <div class="p-5 border-b border-gray-100 dark:border-gray-800 flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/20 shrink-0">
            <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <Eye class="w-5 h-5 text-blue-500" />
              تفاصيل الأفراد - {{ selectedSnapshot?.snapshot_name }}
            </h3>
            <button @click="isDetailsModalOpen = false" class="text-gray-400 hover:text-red-500 transition-colors">
              <X class="w-5 h-5" />
            </button>
          </div>
          
          <div class="flex-1 overflow-hidden p-5">
            <div v-if="isLoadingDetails" class="flex flex-col items-center justify-center h-full">
              <Loader2 class="w-8 h-8 text-blue-500 animate-spin mb-4" />
              <p class="text-gray-500 dark:text-gray-400 font-bold">جاري تحميل بيانات اللقطة...</p>
            </div>
            <div v-else class="h-full border border-gray-100 dark:border-gray-800 rounded-xl overflow-auto">
              <table class="w-full text-start text-sm text-gray-500 dark:text-gray-400">
                <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-800 dark:text-gray-400 sticky top-0 z-10">
                  <tr>
                    <th scope="col" class="px-6 py-3" v-for="col in detailsColumns" :key="col.key">
                      {{ col.label }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="row in snapshotDetails" :key="row.id" class="bg-white border-b dark:bg-gray-900 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800">
                    <td class="px-6 py-4" v-for="col in detailsColumns" :key="col.key">
                      {{ row[col.key] || '—' }}
                    </td>
                  </tr>
                  <tr v-if="snapshotDetails.length === 0">
                    <td :colspan="detailsColumns.length" class="px-6 py-8 text-center text-gray-500">لا توجد بيانات للعرض</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import DataTable from '@/components/tables/DataTable.vue'
import Swal from 'sweetalert2'
import api from '@/lib/api'
import { 
  DatabaseBackup, Camera, Settings, Archive, HardDrive, CalendarClock, History, CheckCircle, Loader2, Download, Eye, Settings2, X
} from 'lucide-vue-next'

const { t } = useI18n()

const isGenerating = ref(false)

const columns = ref([
  { key: 'snapshot_name', label: 'اسم اللقطة', sortable: true },
  { key: 'snapshot_date', label: 'تاريخ اللقطة (الشهر)', sortable: true },
  { key: 'total_personnel', label: 'إجمالي الأفراد', sortable: true },
  { key: 'size', label: 'حجم البيانات', sortable: true },
  { key: 'status', label: 'الحالة', sortable: true },
  { key: 'actions', label: 'الإجراءات', sortable: false },
])

const snapshots = ref<any[]>([])

const isScheduleModalOpen = ref(false)
const isSavingSchedule = ref(false)
const scheduleSettingId = ref<number | null>(null)

const isDetailsModalOpen = ref(false)
const isLoadingDetails = ref(false)
const selectedSnapshot = ref<any>(null)
const snapshotDetails = ref<any[]>([])

const detailsColumns = ref([
  { key: 'military_number', label: 'الرقم العسكري', sortable: true },
  { key: 'name', label: 'الاسم', sortable: true },
  { key: 'rank', label: 'الرتبة', sortable: true },
  { key: 'status', label: 'الحالة', sortable: true },
  { key: 'unit', label: 'الجهة', sortable: true }
])
const scheduleConfig = ref({
  enabled: false,
  schedule_day: 28,
  schedule_time: '23:59'
})

const openScheduleSettings = async () => {
  isScheduleModalOpen.value = true
  try {
    const res = await api.get('/settings/')
    const setting = res.data?.results?.find((s: any) => s.key === 'snapshot_schedule_config') || res.data?.find?.((s: any) => s.key === 'snapshot_schedule_config')
    if (setting) {
      scheduleSettingId.value = setting.id
      scheduleConfig.value = setting.value
    } else {
      scheduleSettingId.value = null
      scheduleConfig.value = { enabled: false, schedule_day: 28, schedule_time: '23:59' }
    }
  } catch(e) {
    console.error('Failed to load schedule settings', e)
  }
}

const closeScheduleSettings = () => {
  isScheduleModalOpen.value = false
}

const saveScheduleSettings = async () => {
  isSavingSchedule.value = true
  try {
    const payload = {
      key: 'snapshot_schedule_config',
      value: scheduleConfig.value,
      category: 'general',
      description: 'إعدادات الجدولة التلقائية للقطات الشهرية'
    }
    
    if (scheduleSettingId.value) {
      await api.put(`/settings/${scheduleSettingId.value}/`, payload)
    } else {
      const res = await api.post('/settings/', payload)
      scheduleSettingId.value = res.data.id
    }
    
    Swal.fire({
      icon: 'success',
      title: 'تم الحفظ',
      text: 'تم تحديث إعدادات الجدولة التلقائية بنجاح',
      toast: true,
      position: 'top-end',
      timer: 3000,
      showConfirmButton: false
    })
    closeScheduleSettings()
  } catch(e) {
    Swal.fire('خطأ', 'حدث خطأ أثناء حفظ الإعدادات', 'error')
  } finally {
    isSavingSchedule.value = false
  }
}

const downloadSnapshot = async (row: any) => {
  Swal.fire({
    title: 'جاري تحضير الملف',
    text: `يتم الآن توليد ملف Excel لـ ${row.snapshot_name}، يرجى الانتظار...`,
    icon: 'info',
    showConfirmButton: false,
    allowOutsideClick: false
  })
  
  try {
    const response = await api.get(`/personnel/snapshots/?action=export&month=${row.snapshot_date}`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `snapshot_${row.snapshot_date}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    Swal.fire({
      title: 'تم التنزيل بنجاح',
      icon: 'success',
      toast: true,
      position: 'top-end',
      timer: 3000,
      showConfirmButton: false
    })
  } catch (error) {
    Swal.fire('خطأ', 'حدث خطأ أثناء تنزيل الملف', 'error')
  }
}

const viewSnapshot = async (row: any) => {
  selectedSnapshot.value = row
  isDetailsModalOpen.value = true
  isLoadingDetails.value = true
  
  try {
    const res = await api.get(`/personnel/snapshots/?action=details&month=${row.snapshot_date}`)
    snapshotDetails.value = res.data
  } catch (error) {
    Swal.fire('خطأ', 'حدث خطأ أثناء تحميل تفاصيل اللقطة', 'error')
  } finally {
    isLoadingDetails.value = false
  }
}

const snapshotSettings = (row: any) => {
  Swal.fire({
    title: 'إدارة اللقطة',
    text: `هل أنت متأكد من رغبتك في حذف ${row.snapshot_name} نهائياً؟`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#6b7280',
    confirmButtonText: 'نعم، احذف اللقطة',
    cancelButtonText: 'إلغاء'
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await api.delete(`/personnel/snapshots/?month=${row.snapshot_date}`)
        Swal.fire('تم الحذف', 'تم حذف اللقطة بنجاح', 'success')
        fetchSnapshots()
      } catch(e: any) {
        Swal.fire('خطأ', e.response?.data?.error || 'حدث خطأ أثناء الحذف', 'error')
      }
    }
  })
}

const fetchSnapshots = async () => {
  try {
    const res = await api.get('/personnel/snapshots/')
    snapshots.value = res.data.map((s: any, idx: number) => ({
      id: idx + 1,
      snapshot_name: `أرشيف شهر ${s.snapshot_date}`,
      snapshot_date: s.snapshot_date,
      total_personnel: s.total_personnel,
      size: '---', // Not provided by the current API grouping
      status: 'completed'
    }))
  } catch (e) {
    console.error('Error fetching snapshots', e)
  }
}

onMounted(() => {
  fetchSnapshots()
})

const generateSnapshot = () => {
  Swal.fire({
    title: 'تأكيد أخذ اللقطة',
    text: 'هل أنت متأكد من أخذ لقطة لتجميد بيانات القوة الحالية؟ ستعمل العملية في الخلفية ولن تعيق استخدامك للنظام.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#10b981',
    cancelButtonColor: '#d1d5db',
    confirmButtonText: 'نعم، ابدأ العملية',
    cancelButtonText: 'إلغاء'
  }).then((result) => {
    if (result.isConfirmed) {
      isGenerating.value = true
      
      // Start API call in background
      api.post('/personnel/snapshots/')
        .then(() => {
          isGenerating.value = false
          fetchSnapshots()
          Swal.fire({
            title: 'اكتملت اللقطة بنجاح',
            text: 'تم أرشفة لقطة الشهر الحالي في قاعدة البيانات.',
            icon: 'success',
            toast: true,
            position: 'top-end',
            timer: 4000,
            showConfirmButton: false
          })
        })
        .catch(err => {
          isGenerating.value = false
          Swal.fire({
            title: 'خطأ',
            text: err.response?.data?.error || 'حدث خطأ أثناء أخذ اللقطة',
            icon: 'error'
          })
        })

      // Notify user immediately that it started
      Swal.fire({
        title: 'جاري العمل في الخلفية',
        text: 'تم بدء أخذ اللقطة، سيتم إشعارك فور اكتمالها.',
        icon: 'info',
        timer: 3000,
        showConfirmButton: false
      })
    }
  })
}

</script>
