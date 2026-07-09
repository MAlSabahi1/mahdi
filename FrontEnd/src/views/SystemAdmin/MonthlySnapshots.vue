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
          <button class="bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 px-4 py-2.5 rounded-xl text-sm font-bold flex items-center gap-2 transition-colors shrink-0 cursor-pointer">
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
              <button class="p-1.5 text-gray-400 hover:text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-900/30 rounded-lg transition-colors cursor-pointer" title="تنزيل نسخة Excel">
                <Download class="w-4 h-4" />
              </button>
              <button class="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-colors cursor-pointer" title="استعراض البيانات">
                <Eye class="w-4 h-4" />
              </button>
              <button class="p-1.5 text-gray-400 hover:text-amber-600 hover:bg-amber-50 dark:hover:bg-amber-900/30 rounded-lg transition-colors cursor-pointer" title="إعدادات اللقطة">
                <Settings2 class="w-4 h-4" />
              </button>
            </div>
          </template>
        </DataTable>
      </div>

    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import DataTable from '@/components/tables/DataTable.vue'
import Swal from 'sweetalert2'
import { 
  DatabaseBackup, Camera, Settings, Archive, HardDrive, CalendarClock, History, CheckCircle, Loader2, Download, Eye, Settings2
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

const snapshots = ref([
  { id: 1, snapshot_name: 'أرشيف شهر يونيو 2026', snapshot_date: '2026-06-30', total_personnel: '25,430', size: '245 MB', status: 'completed' },
  { id: 2, snapshot_name: 'أرشيف شهر مايو 2026', snapshot_date: '2026-05-31', total_personnel: '25,210', size: '242 MB', status: 'completed' },
  { id: 3, snapshot_name: 'أرشيف شهر أبريل 2026', snapshot_date: '2026-04-30', total_personnel: '24,800', size: '238 MB', status: 'completed' },
  { id: 4, snapshot_name: 'أرشيف شهر مارس 2026', snapshot_date: '2026-03-31', total_personnel: '24,750', size: '236 MB', status: 'completed' },
  { id: 5, snapshot_name: 'أرشيف شهر فبراير 2026', snapshot_date: '2026-02-28', total_personnel: '24,500', size: '232 MB', status: 'completed' },
])

const generateSnapshot = () => {
  Swal.fire({
    title: 'تأكيد أخذ اللقطة',
    text: 'هل أنت متأكد من أخذ لقطة لتجميد بيانات القوة الحالية؟ (هذه العملية قد تستغرق بعض الوقت وتستهلك موارد النظام)',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#10b981',
    cancelButtonColor: '#d1d5db',
    confirmButtonText: 'نعم، ابدأ العملية',
    cancelButtonText: 'إلغاء'
  }).then((result) => {
    if (result.isConfirmed) {
      isGenerating.value = true
      
      // Simulate API call
      setTimeout(() => {
        snapshots.value.unshift({
          id: Date.now(),
          snapshot_name: 'لقطة استثنائية - يوليو 2026',
          snapshot_date: new Date().toISOString().split('T')[0],
          total_personnel: '25,600',
          size: '250 MB',
          status: 'completed'
        })
        isGenerating.value = false
        
        Swal.fire({
          title: 'تم بنجاح',
          text: 'تم إنشاء اللقطة وأرشفتها بنجاح.',
          icon: 'success',
          timer: 2000,
          showConfirmButton: false
        })
      }, 3000)
    }
  })
}

</script>
