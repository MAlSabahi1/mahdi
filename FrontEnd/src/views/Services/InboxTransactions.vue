<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="قائمة المعاملات والمهام الجارية" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Page Header -->
      <div class="border-b border-gray-200 dark:border-gray-800 pb-5">
        <h1 class="text-2xl font-black text-gray-900 dark:text-white">
          قائمة المعاملات والمهام (Transactions Inbox)
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          إدارة طلبات المعاملات وكروت الخدمات المرفوعة من المديريات، واعتمادها أو رفضها أو إقفالها نهائياً.
        </p>
      </div>

      <!-- Transactions Table Grid -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl shadow-theme-xs overflow-hidden">
        <div class="p-5 border-b border-gray-200 dark:border-gray-800 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
          <div>
            <h3 class="text-sm font-black text-gray-900 dark:text-white">جدول مراجعة الطلبات والاعتمادات الجارية</h3>
            <p class="text-[10px] text-gray-400 mt-0.5">الطلبات الحالية التي تتطلب المراجعة الفنية واعتماد لجان شؤون الأفراد والخدمات.</p>
          </div>
          
          <div class="flex gap-2">
            <select v-model="filterStatus" class="text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300">
              <option value="pending">بانتظار المراجعة (قيد الانتظار)</option>
              <option value="approved">المعتمدة تاريخياً</option>
              <option value="rejected">المرفوضة</option>
            </select>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-right border-collapse text-xs">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 text-[10px] font-bold text-gray-450 bg-gray-50/50 dark:bg-gray-950/20">
                <th class="px-5 py-3 w-[120px]">رقم المعاملة</th>
                <th class="px-5 py-3">نوع كرت الخدمة</th>
                <th class="px-5 py-3">تاريخ التقديم</th>
                <th class="px-5 py-3">المديرية المصدرة</th>
                <th class="px-5 py-3">الحالة الحالية</th>
                <th class="px-5 py-3 text-center w-[180px]">العمليات والإجراءات</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-150 dark:divide-gray-850">
              <tr v-if="transactions.length === 0">
                <td colspan="6" class="px-5 py-12 text-center text-gray-400 dark:text-gray-500">
                  لا توجد معاملات جارية بانتظار المراجعة والاعتماد حالياً.
                </td>
              </tr>
              <tr v-for="tx in filteredTransactions" :key="tx.id" class="hover:bg-gray-50/50 dark:hover:bg-gray-950/30">
                <td class="px-5 py-3 font-mono font-bold">{{ tx.txNumber }}</td>
                <td class="px-5 py-3 font-bold text-gray-800 dark:text-gray-200">{{ tx.title }}</td>
                <td class="px-5 py-3 font-mono text-gray-450">{{ tx.date }}</td>
                <td class="px-5 py-3">{{ tx.governorate }}</td>
                <td class="px-5 py-3">
                  <span class="inline-flex items-center gap-1 rounded px-2.5 py-0.5 text-[9px] font-bold bg-amber-50 text-amber-700 dark:bg-amber-950/20 dark:text-amber-400">
                    <span class="h-1 w-1 rounded-full bg-amber-500"></span>
                    {{ tx.statusLabel }}
                  </span>
                </td>
                <td class="px-5 py-3 flex items-center justify-center gap-2">
                  <button 
                    @click="approveTx(tx)"
                    class="bg-emerald-600 hover:bg-emerald-700 text-white text-[10px] font-bold px-2.5 py-1 rounded transition-colors cursor-pointer"
                  >
                    اعتماد
                  </button>
                  <button 
                    @click="rejectTx(tx)"
                    class="bg-red-600 hover:bg-red-700 text-white text-[10px] font-bold px-2.5 py-1 rounded transition-colors cursor-pointer"
                  >
                    رفض
                  </button>
                  <button 
                    @click="lockTx(tx)"
                    class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 text-[10px] font-bold px-2 py-1 rounded transition-colors cursor-pointer"
                    title="قفل المعاملة نهائياً"
                  >
                    🔒 قفل
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import Swal from 'sweetalert2'

const filterStatus = ref('pending')

interface Transaction {
  id: number
  txNumber: string
  title: string
  date: string
  governorate: string
  status: string
  statusLabel: string
}

// Strictly listing generic metadata, no fake human names
const transactions = ref<Transaction[]>([
  { id: 1, txNumber: 'TX-2026-0089', title: 'طلب تسوية رتبة عسكرية (كرت 01)', date: '2026-07-01', governorate: 'عدن', status: 'pending', statusLabel: 'مراجعة أمنية أولية' },
  { id: 2, txNumber: 'TX-2026-0092', title: 'طلب علاوة رتبة جديدة (كرت 02)', date: '2026-07-02', governorate: 'تعز', status: 'pending', statusLabel: 'مطابقة الكشوفات المالية' },
  { id: 3, txNumber: 'TX-2026-0095', title: 'طلب تعديل المديرية الجغرافية (كرت 05)', date: '2026-07-02', governorate: 'حضرموت', status: 'pending', statusLabel: 'انتظار الموافقة الثنائية' }
])

const filteredTransactions = computed(() => {
  return transactions.value.filter(t => t.status === filterStatus.value)
})

function approveTx(tx: Transaction) {
  Swal.fire({
    title: 'اعتماد المعاملة والبدء بالترحيل؟',
    text: `أنت بصدد الموافقة الفنية على المعاملة ${tx.txNumber}.`,
    icon: 'success',
    showCancelButton: true,
    confirmButtonText: 'نعم، اعتماد الكرت',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#10b981'
  }).then((result) => {
    if (result.isConfirmed) {
      transactions.value = transactions.value.filter(t => t.id !== tx.id)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم اعتماد المعاملة وترحيلها', showConfirmButton: false, timer: 2000 })
    }
  })
}

function rejectTx(tx: Transaction) {
  Swal.fire({
    title: 'رفض المعاملة وإحالتها لسجل المرفوضات؟',
    text: `الرجاء كتابة سبب الرفض الفني لإعادته للمديرية:`,
    input: 'text',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'تأكيد الرفض',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#ef4444'
  }).then((result) => {
    if (result.isConfirmed && result.value) {
      transactions.value = transactions.value.filter(t => t.id !== tx.id)
      Swal.fire({ toast: true, position: 'top-end', icon: 'warning', title: 'تم رفض المعاملة وإعادتها', showConfirmButton: false, timer: 2000 })
    }
  })
}

function lockTx(tx: Transaction) {
  Swal.fire({
    title: 'قفل المعاملة نهائياً؟',
    text: 'عملية قفل المعاملة تمنع إدخال أي تعديلات إضافية عليها مستقبلاً وتعتمدها كمسودة مقفلة أرشيفياً.',
    icon: 'info',
    showCancelButton: true,
    confirmButtonText: 'تأكيد القفل والأرشفة',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#6b7280'
  }).then((result) => {
    if (result.isConfirmed) {
      transactions.value = transactions.value.filter(t => t.id !== tx.id)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم قفل المعاملة بنجاح', showConfirmButton: false, timer: 2000 })
    }
  })
}
</script>
