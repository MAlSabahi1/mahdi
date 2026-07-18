<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.compliance_tracker')" />
    
    <div class="space-y-6 text-start" dir="rtl">
      <!-- Overall Compliance Score -->
      <div class="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-900 flex flex-col md:flex-row items-center gap-8">
        <div class="flex-1">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">مؤشر الالتزام الكلي للمحافظات</h3>
          <p class="text-gray-500 dark:text-gray-400 text-sm leading-relaxed max-w-2xl">
            يقيس هذا المؤشر نسبة المحافظات التي التزمت برفع كشوفاتها وتحديث بياناتها في الوقت المحدد لهذا الشهر. المحافظات المتأخرة تؤثر سلباً على جودة التقارير المركزية.
          </p>
        </div>
        <div class="shrink-0 text-center">
          <div class="inline-flex items-center justify-center w-32 h-32 rounded-full border-8 border-emerald-500 bg-emerald-50 dark:bg-emerald-950/20 text-emerald-600 dark:text-emerald-400">
            <span class="text-3xl font-black">{{ totalScore }}%</span>
          </div>
          <p class="text-sm font-bold text-gray-500 dark:text-gray-400 mt-3">نسبة الإنجاز</p>
        </div>
        <div class="shrink-0 flex flex-col gap-3 border-r border-gray-100 dark:border-gray-800 pr-6">
          <div class="flex items-center gap-3">
            <div class="w-3 h-3 rounded-full bg-emerald-500"></div>
            <span class="text-sm text-gray-700 dark:text-gray-300">{{ compliantCount }} محافظة ملتزمة</span>
          </div>
          <div class="flex items-center gap-3">
            <div class="w-3 h-3 rounded-full bg-amber-500"></div>
            <span class="text-sm text-gray-700 dark:text-gray-300">{{ warningCount }} محافظة متأخرة</span>
          </div>
          <div class="flex items-center gap-3">
            <div class="w-3 h-3 rounded-full bg-red-500"></div>
            <span class="text-sm text-gray-700 dark:text-gray-300">{{ criticalCount }} محافظة حرجة</span>
          </div>
        </div>
      </div>

      <!-- Compliance Table -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
        <div class="p-4 border-b border-gray-100 dark:border-gray-800 flex items-center justify-between">
          <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <ListChecks class="w-5 h-5 text-gray-400" />
            سجل التزام المحافظات والقطاعات
          </h3>
          <button class="bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-xl text-sm font-bold transition-colors cursor-pointer">
            تصدير التقرير
          </button>
        </div>
        
        <DataTable
          :columns="columns"
          :data="complianceData"
          row-key="id"
          :search-placeholder="'ابحث عن محافظة أو قطاع...'"
        >
          <template #cell-status="{ row }">
            <span v-if="row.status === 'compliant'" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-bold bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400">
              <CheckCircle class="w-3.5 h-3.5" />
              ملتزم
            </span>
            <span v-else-if="row.status === 'warning'" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-bold bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400">
              <Clock class="w-3.5 h-3.5" />
              متأخر
            </span>
            <span v-else class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-bold bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400">
              <AlertOctagon class="w-3.5 h-3.5" />
              حرج
            </span>
          </template>

          <template #cell-dataQuality="{ row }">
            <div class="flex items-center gap-2">
              <div class="flex-1 h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden w-24">
                <div class="h-full rounded-full" 
                     :class="row.dataQuality >= 90 ? 'bg-emerald-500' : (row.dataQuality >= 70 ? 'bg-amber-500' : 'bg-red-500')"
                     :style="`width: ${row.dataQuality}%`">
                </div>
              </div>
              <span class="text-xs font-mono text-gray-500">{{ row.dataQuality }}%</span>
            </div>
          </template>

          <template #actions="{ row }">
            <button v-if="row.status !== 'compliant'" @click="sendReminder(row)" title="إرسال تذكير عاجل" class="p-2 text-amber-600 hover:bg-amber-50 rounded-lg dark:text-amber-400 dark:hover:bg-amber-900/20 transition-colors cursor-pointer">
              <BellRing class="w-4 h-4" />
            </button>
            <button title="التفاصيل" class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-lg dark:hover:text-gray-300 dark:hover:bg-gray-800 transition-colors cursor-pointer">
              <Eye class="w-4 h-4" />
            </button>
          </template>
        </DataTable>
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
import { ListChecks, CheckCircle, Clock, AlertOctagon, BellRing, Eye } from 'lucide-vue-next'
import api from '@/lib/api'

const { t } = useI18n()

const columns = ref([
  { key: 'name', label: 'الجهة / المحافظة', sortable: true },
  { key: 'lastUpdate', label: 'تاريخ آخر تحديث', sortable: true },
  { key: 'dataQuality', label: 'جودة البيانات', sortable: true },
  { key: 'status', label: 'حالة الالتزام', sortable: true }
])

const complianceData = ref<any[]>([])
const totalScore = ref(0)
const compliantCount = ref(0)
const warningCount = ref(0)
const criticalCount = ref(0)

const fetchCompliance = async () => {
  try {
    const res = await api.get('/personnel/dashboard/compliance/')
    if (res.data.compliance_by_region) {
      complianceData.value = res.data.compliance_by_region.map((r: any, idx: number) => {
        const quality = Math.round(r.avg_score || 0)
        let status = 'compliant'
        if (quality < 70) status = 'critical'
        else if (quality < 90) status = 'warning'
        
        return {
          id: idx,
          name: r.region || 'غير محدد',
          lastUpdate: 'اليوم',
          dataQuality: quality,
          status: status
        }
      })

      if (complianceData.value.length > 0) {
        const total = complianceData.value.reduce((acc, curr) => acc + curr.dataQuality, 0)
        totalScore.value = Math.round(total / complianceData.value.length)
        compliantCount.value = complianceData.value.filter(r => r.status === 'compliant').length
        warningCount.value = complianceData.value.filter(r => r.status === 'warning').length
        criticalCount.value = complianceData.value.filter(r => r.status === 'critical').length
      }
    }
  } catch (error) {
    console.error('Error fetching compliance data', error)
  }
}

onMounted(() => {
  fetchCompliance()
})

const sendReminder = (row: any) => {
  Swal.fire({
    title: 'إرسال تذكير عاجل',
    text: `هل أنت متأكد من إرسال إشعار تذكير عبر النظام و SMS لمدير ${row.name}؟`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#f59e0b',
    cancelButtonColor: '#d1d5db',
    confirmButtonText: 'نعم، إرسال التذكير',
    cancelButtonText: 'إلغاء'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: 'تم الإرسال',
        text: 'تم إرسال التذكير بنجاح.',
        icon: 'success',
        timer: 1500,
        showConfirmButton: false
      })
    }
  })
}
</script>
