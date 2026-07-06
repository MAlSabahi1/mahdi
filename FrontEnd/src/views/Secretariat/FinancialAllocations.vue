<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('secretariat.finance.title')" />
    <div class="space-y-6">
      <!-- Finance Dashboard / Analytics -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Budget utilization tracker -->
        <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-3xl p-6 shadow-theme-sm md:col-span-2">
          <h3 class="text-sm font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-4">تحليل صرف الميزانية الشهرية (الحالية)</h3>
          <div v-if="activeAllocation" class="space-y-4">
            <div class="flex justify-between items-end">
              <div>
                <span class="block text-2xl font-black text-gray-950 dark:text-white">{{ formatCurrency(activeAllocation.total_amount) }}</span>
                <span class="text-xs text-gray-500">إجمالي الاعتماد المالي لشهر {{ activeAllocation.month }}/{{ activeAllocation.year }}</span>
              </div>
              <div class="text-end">
                <span class="block text-lg font-bold text-indigo-600 dark:text-indigo-400">{{ formatCurrency(activeAllocation.spent_amount) }}</span>
                <span class="text-xs text-gray-500">المصروف الفعلي ({{ getUtilizationPercent(activeAllocation) }}%)</span>
              </div>
            </div>
            <!-- Progress bar -->
            <div class="w-full bg-gray-100 dark:bg-gray-800 rounded-full h-3 overflow-hidden">
              <div
                class="bg-indigo-600 h-3 rounded-full transition-all duration-500"
                :style="{ width: `${Math.min(getUtilizationPercent(activeAllocation), 100)}%` }"
              ></div>
            </div>
            <div class="flex justify-between text-xs text-gray-500">
              <span>المتبقي: {{ formatCurrency(activeAllocation.remaining_amount) }}</span>
              <span>الحد الأقصى: 100%</span>
            </div>
          </div>
          <div v-else class="text-center py-6 text-sm text-gray-500">
            لا توجد اعتمادات مالية نشطة للشهر الحالي. يرجى تسجيل اعتماد مالي أولاً.
          </div>
        </div>

        <!-- Quick actions / stats -->
        <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-3xl p-6 shadow-theme-sm flex flex-col justify-between">
          <div>
            <h4 class="text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-2">إجمالي الاعتمادات والمصروفات المسجلة</h4>
            <div class="space-y-2 mt-4">
              <div class="flex justify-between text-sm">
                <span class="text-gray-500">مجموع الاعتمادات:</span>
                <span class="font-semibold text-gray-900 dark:text-white">{{ formatCurrency(totalAllocatedSum) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-500">مجموع المصروفات:</span>
                <span class="font-semibold text-gray-900 dark:text-white">{{ formatCurrency(totalSpentSum) }}</span>
              </div>
            </div>
          </div>
          <div class="flex gap-2 mt-6">
            <button
              @click="showAllocationModal = true"
              class="flex-1 py-2 px-3 text-xs font-bold text-gray-700 bg-gray-50 hover:bg-gray-100 border border-gray-200 dark:border-gray-800 dark:bg-gray-850 dark:text-gray-300 rounded-xl transition cursor-pointer"
            >
              + اعتماد شهري
            </button>
            <button
              @click="showExpenseModal = true"
              class="flex-1 py-2 px-3 text-xs font-bold text-white bg-brand-500 hover:bg-brand-600 rounded-xl transition cursor-pointer"
            >
              + تسجيل مصروف
            </button>
          </div>
        </div>
      </div>

      <!-- Tabs Selector -->
      <div class="flex gap-2 p-1 bg-gray-100 dark:bg-gray-800 rounded-2xl w-fit">
        <button
          v-for="t in ['expenses', 'allocations']"
          :key="t"
          @click="activeTab = t"
          :class="[
            'px-5 py-2 rounded-xl text-sm font-semibold transition cursor-pointer',
            activeTab === t
              ? 'bg-white dark:bg-gray-900 text-gray-900 dark:text-white shadow-theme-xs'
              : 'text-gray-500 hover:text-gray-900 dark:hover:text-white'
          ]"
        >
          {{ t === 'expenses' ? 'سندات المصروفات والمنصرف' : 'سجلات الاعتمادات الشهرية' }}
        </button>
      </div>

      <!-- Tab Content: Expense Vouchers -->
      <div v-if="activeTab === 'expenses'" class="space-y-6 animate-fade-in">
        <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
            <thead class="bg-gray-50 dark:bg-gray-800/50">
              <tr>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">رقم السند</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">التاريخ</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">التصنيف</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">المبلغ</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">المستفيد</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">البيان/الوصف</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-800 bg-white dark:bg-gray-900">
              <tr v-if="loading" class="text-center py-6"><td colspan="6" class="py-6 text-sm text-gray-500">جاري التحميل...</td></tr>
              <tr v-else-if="expenses.length === 0" class="text-center py-6"><td colspan="6" class="py-6 text-sm text-gray-500">لا توجد قسائم مصروفات مسجلة.</td></tr>
              <tr v-else v-for="exp in expenses" :key="exp.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/30 transition">
                <td class="px-6 py-4 text-sm font-semibold text-gray-950 dark:text-white">{{ exp.voucher_number }}</td>
                <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{{ exp.date }}</td>
                <td class="px-6 py-4 text-sm">
                  <span class="px-2 py-0.5 rounded-full text-xxs font-semibold bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300">
                    {{ exp.category_display }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm font-bold text-red-600 dark:text-red-400">{{ formatCurrency(exp.amount) }}</td>
                <td class="px-6 py-4 text-sm text-gray-900 dark:text-white font-medium">{{ exp.recipient_name }}</td>
                <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400 max-w-xs truncate" :title="exp.description">{{ exp.description }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tab Content: Monthly Allocations -->
      <div v-if="activeTab === 'allocations'" class="space-y-6 animate-fade-in">
        <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
            <thead class="bg-gray-50 dark:bg-gray-800/50">
              <tr>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">الشهر/السنة</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">المبلغ المعتمد</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">إجمالي المنصرف</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">المتبقي</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">نسبة الاستهلاك</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-800 bg-white dark:bg-gray-900">
              <tr v-if="loading" class="text-center py-6"><td colspan="5" class="py-6 text-sm text-gray-500">جاري التحميل...</td></tr>
              <tr v-else-if="allocations.length === 0" class="text-center py-6"><td colspan="5" class="py-6 text-sm text-gray-500">لا توجد اعتمادات مالية مسجلة.</td></tr>
              <tr v-else v-for="alloc in allocations" :key="alloc.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/30 transition">
                <td class="px-6 py-4 text-sm font-semibold text-gray-950 dark:text-white">{{ alloc.month }} / {{ alloc.year }}</td>
                <td class="px-6 py-4 text-sm font-bold text-gray-900 dark:text-white">{{ formatCurrency(alloc.total_amount) }}</td>
                <td class="px-6 py-4 text-sm font-semibold text-red-500">{{ formatCurrency(alloc.spent_amount) }}</td>
                <td class="px-6 py-4 text-sm font-semibold text-green-500">{{ formatCurrency(alloc.remaining_amount) }}</td>
                <td class="px-6 py-4 text-sm">
                  <div class="flex items-center gap-2">
                    <div class="w-24 bg-gray-150 dark:bg-gray-800 rounded-full h-2 overflow-hidden">
                      <div class="bg-indigo-500 h-2 rounded-full" :style="{ width: `${Math.min(getUtilizationPercent(alloc), 100)}%` }"></div>
                    </div>
                    <span class="text-xs font-bold text-gray-700 dark:text-gray-300">{{ getUtilizationPercent(alloc) }}%</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <!-- Add Monthly Allocation Modal -->
    <div v-if="showAllocationModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm">
      <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-2xl shadow-xl overflow-hidden border border-gray-200 dark:border-gray-800 animate-fade-in">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center bg-gray-50 dark:bg-gray-800/50">
          <h3 class="text-sm font-bold text-gray-900 dark:text-white">قيد اعتماد مالي شهري جديد</h3>
          <button @click="showAllocationModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl font-bold cursor-pointer">&times;</button>
        </div>
        <form @submit.prevent="submitAllocation" class="p-6 space-y-4">
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">الشهر (1 - 12) *</label>
              <input v-model.number="allocForm.month" type="number" required min="1" max="12" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">السنة *</label>
              <input v-model.number="allocForm.year" type="number" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
            </div>
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">المبلغ المعتمد (بالريال اليمني) *</label>
            <input v-model.number="allocForm.total_amount" type="number" required min="1" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">ملاحظات/شروحات</label>
            <textarea v-model="allocForm.notes" rows="2" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm"></textarea>
          </div>
          <div class="flex justify-end gap-2 pt-4 border-t border-gray-200 dark:border-gray-800">
            <button type="button" @click="showAllocationModal = false" class="px-4 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">إلغاء</button>
            <button type="submit" class="px-4 py-2 text-xs font-medium text-white bg-brand-500 rounded-lg hover:bg-brand-600">حفظ الاعتماد</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Add Expense Modal -->
    <div v-if="showExpenseModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm">
      <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-2xl shadow-xl overflow-hidden border border-gray-200 dark:border-gray-800 animate-fade-in">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center bg-gray-50 dark:bg-gray-800/50">
          <h3 class="text-sm font-bold text-gray-900 dark:text-white">تسجيل قسيمة مصروف جديد</h3>
          <button @click="showExpenseModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl font-bold cursor-pointer">&times;</button>
        </div>
        <form @submit.prevent="submitExpense" class="p-6 space-y-4">
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">الاعتماد المالي المرتبط *</label>
            <select v-model="expenseForm.allocation" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm">
              <option value="" disabled>اختر الاعتماد المالي...</option>
              <option v-for="alloc in allocations" :key="alloc.id" :value="alloc.id">
                شهر {{ alloc.month }}/{{ alloc.year }} - متوفر: {{ formatCurrency(alloc.remaining_amount) }}
              </option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">رقم السند/القسيمة *</label>
              <input v-model="expenseForm.voucher_number" type="text" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">التصنيف *</label>
              <select v-model="expenseForm.category" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm">
                <option value="supplies">قرطاسية ومستلزمات مكتبية</option>
                <option value="events">ضيافة واجتماعات</option>
                <option value="maintenance">صيانة وتشغيل</option>
                <option value="printing">مطبوعات وتصوير</option>
                <option value="other">أخرى</option>
              </select>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">المبلغ المصروف *</label>
              <input v-model.number="expenseForm.amount" type="number" required min="1" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">التاريخ *</label>
              <input v-model="expenseForm.date" type="date" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
            </div>
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">المستفيد (الجهة/الشخص) *</label>
            <input v-model="expenseForm.recipient_name" type="text" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">البيان/الوصف التفصيلي *</label>
            <textarea v-model="expenseForm.description" required rows="2" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm"></textarea>
          </div>
          <div class="flex justify-end gap-2 pt-4 border-t border-gray-200 dark:border-gray-800">
            <button type="button" @click="showExpenseModal = false" class="px-4 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">إلغاء</button>
            <button type="submit" class="px-4 py-2 text-xs font-medium text-white bg-brand-500 rounded-lg hover:bg-brand-600">تسجيل الصرف</button>
          </div>
        </form>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useSecretariatStore } from '@/stores/secretariat'
import Swal from 'sweetalert2'

const store = useSecretariatStore()

const loading = ref(true)
const activeTab = ref('expenses')

const allocations = ref<any[]>([])
const expenses = ref<any[]>([])

const showAllocationModal = ref(false)
const showExpenseModal = ref(false)

const allocForm = ref({
  month: new Date().getMonth() + 1,
  year: new Date().getFullYear(),
  total_amount: 0,
  notes: ''
})

const expenseForm = ref({
  allocation: '',
  voucher_number: '',
  category: 'supplies',
  amount: 0,
  date: new Date().toISOString().split('T')[0],
  recipient_name: '',
  description: ''
})

async function fetchAllocations() {
  loading.value = true
  try {
    const res = await store.fetchFinancialAllocations()
    allocations.value = res.results || []
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function fetchExpenses() {
  loading.value = true
  try {
    const res = await store.fetchExpenses()
    expenses.value = res.results || []
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Active allocation (current month or latest one)
const activeAllocation = computed(() => {
  if (allocations.value.length === 0) return null
  const currentMonth = new Date().getMonth() + 1
  const currentYear = new Date().getFullYear()
  
  // match current month/year
  const matched = allocations.value.find(a => a.month === currentMonth && a.year === currentYear)
  return matched || allocations.value[0]
})

const totalAllocatedSum = computed(() => {
  return allocations.value.reduce((sum, item) => sum + Number(item.total_amount || 0), 0)
})

const totalSpentSum = computed(() => {
  return allocations.value.reduce((sum, item) => sum + Number(item.spent_amount || 0), 0)
})

function formatCurrency(val: number | string) {
  const num = Number(val || 0)
  return new Intl.NumberFormat('ar-YE', { style: 'currency', currency: 'YER', maximumFractionDigits: 0 }).format(num)
}

function getUtilizationPercent(alloc: any) {
  if (!alloc.total_amount) return 0
  const pct = (Number(alloc.spent_amount) / Number(alloc.total_amount)) * 100
  return Math.round(pct * 10) / 10
}

async function submitAllocation() {
  try {
    await store.createFinancialAllocation(allocForm.value)
    showAllocationModal.value = false
    allocForm.value = { month: new Date().getMonth() + 1, year: new Date().getFullYear(), total_amount: 0, notes: '' }
    fetchAllocations()
    Swal.fire({
      icon: 'success',
      title: 'تم تسجيل الاعتماد بنجاح',
      timer: 1500,
      showConfirmButton: false
    })
  } catch (err: any) {
    console.error(err)
    let errorMsg = 'حدث خطأ غير متوقع أثناء تسجيل الاعتماد.'
    if (err.response?.data) {
      const data = err.response.data
      if (typeof data === 'object') {
        errorMsg = Object.values(data).flat().join('\n')
      } else if (typeof data === 'string') {
        errorMsg = data
      }
    }
    Swal.fire({
      icon: 'error',
      title: 'فشل حفظ الاعتماد',
      text: errorMsg,
      confirmButtonText: 'حسناً'
    })
  }
}

async function submitExpense() {
  try {
    await store.createExpense(expenseForm.value)
    showExpenseModal.value = false
    expenseForm.value = {
      allocation: '',
      voucher_number: '',
      category: 'supplies',
      amount: 0,
      date: new Date().toISOString().split('T')[0],
      recipient_name: '',
      description: ''
    }
    // refresh both because spent amount updates
    fetchExpenses()
    fetchAllocations()
    Swal.fire({
      icon: 'success',
      title: 'تم تسجيل المصروف بنجاح',
      timer: 1500,
      showConfirmButton: false
    })
  } catch (err: any) {
    console.error(err)
    let errorMsg = 'حدث خطأ غير متوقع أثناء تسجيل المصروف.'
    if (err.response?.data) {
      const data = err.response.data
      if (typeof data === 'object') {
        errorMsg = Object.values(data).flat().join('\n')
      } else if (typeof data === 'string') {
        errorMsg = data
      }
    }
    Swal.fire({
      icon: 'error',
      title: 'فشل تسجيل المصروف',
      text: errorMsg,
      confirmButtonText: 'حسناً'
    })
  }
}

watch(activeTab, (tab) => {
  if (tab === 'expenses') fetchExpenses()
  if (tab === 'allocations') fetchAllocations()
})

onMounted(() => {
  fetchAllocations()
  fetchExpenses()
})
</script>
