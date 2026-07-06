<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('secretariat.attendance.title')" />
    <div class="space-y-6">
      <!-- Attendance Statistics Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="stat in stats" :key="stat.label" class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-3xl p-6 shadow-theme-sm flex items-center gap-4">
          <div :class="['p-4 rounded-2xl text-xl font-bold', stat.iconBg, stat.iconColor]">
            {{ stat.icon }}
          </div>
          <div>
            <span class="block text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-1">{{ stat.label }}</span>
            <span class="text-2xl font-bold text-gray-950 dark:text-white">{{ stat.value }}</span>
          </div>
        </div>
      </div>

      <!-- Filters & Action Bar -->
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between bg-white dark:bg-gray-900 p-5 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-theme-sm">
        <div class="flex flex-1 flex-col gap-4 sm:flex-row sm:items-center">
          <div class="w-full sm:w-48">
            <input
              v-model="dateFilter"
              type="date"
              class="w-full rounded-lg border border-gray-300 bg-gray-50 py-2.5 px-4 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              @change="fetchAttendance"
            />
          </div>
          <div class="w-full sm:w-48">
            <select
              v-model="statusFilter"
              class="w-full rounded-lg border border-gray-300 bg-gray-50 py-2.5 px-3 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              @change="fetchAttendance"
            >
              <option value="">الحالة: الكل</option>
              <option value="present">حاضر (Present)</option>
              <option value="absent">غائب (Absent)</option>
              <option value="late">متأخر (Late)</option>
              <option value="excused">مأذون (Excused)</option>
            </select>
          </div>
        </div>
        <button
          @click="showAddModal = true"
          class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white hover:bg-brand-600 transition shadow-theme-xs cursor-pointer"
        >
          + تسجيل حضور/غياب
        </button>
      </div>

      <!-- Attendance Table -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
          <thead class="bg-gray-50 dark:bg-gray-800/50">
            <tr>
              <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">المنتسب</th>
              <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">الرقم العسكري</th>
              <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">التاريخ</th>
              <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">الحالة</th>
              <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">وقت التحضير</th>
              <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">وقت الانصراف</th>
              <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">ملاحظات</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 dark:divide-gray-800 bg-white dark:bg-gray-900">
            <tr v-if="loading" class="text-center py-6"><td colspan="7" class="py-6 text-sm text-gray-500">جاري التحميل...</td></tr>
            <tr v-else-if="logs.length === 0" class="text-center py-6"><td colspan="7" class="py-6 text-sm text-gray-500">لا توجد سجلات دوام للتاريخ المحدد.</td></tr>
            <tr v-else v-for="log in logs" :key="log.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/30 transition">
              <td class="px-6 py-4 text-sm font-semibold text-gray-950 dark:text-white">{{ log.employee_name }}</td>
              <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{{ log.employee_military_number }}</td>
              <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{{ log.date }}</td>
              <td class="px-6 py-4 text-sm">
                <span
                  :class="[
                    'px-2.5 py-0.5 rounded-full text-xxs font-semibold',
                    log.status === 'present' ? 'bg-green-50 text-green-700 dark:bg-green-900/30' :
                    log.status === 'absent' ? 'bg-red-50 text-red-700 dark:bg-red-900/30' :
                    log.status === 'late' ? 'bg-amber-50 text-amber-700 dark:bg-amber-900/30' :
                    'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
                  ]"
                >
                  {{ log.status_display }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 font-medium">{{ log.check_in_time || '-' }}</td>
              <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 font-medium">{{ log.check_out_time || '-' }}</td>
              <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400 max-w-xs truncate">{{ log.notes || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Record Attendance Modal -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm">
      <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-2xl shadow-xl overflow-hidden border border-gray-200 dark:border-gray-800 animate-fade-in">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center bg-gray-50 dark:bg-gray-800/50">
          <h3 class="text-sm font-bold text-gray-900 dark:text-white">تسجيل حضور وانصراف يومي</h3>
          <button @click="showAddModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl font-bold cursor-pointer">&times;</button>
        </div>
        <form @submit.prevent="submitForm" class="p-6 space-y-4">
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">الموظف/المنتسب *</label>
            <select v-model="form.employee" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm">
              <option value="" disabled>اختر الموظف...</option>
              <option v-for="emp in employees" :key="emp.id" :value="emp.id">
                {{ emp.full_name }} ({{ emp.military_number }})
              </option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">التاريخ *</label>
              <input v-model="form.date" type="date" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">حالة الحضور *</label>
              <select v-model="form.status" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm">
                <option value="present">حاضر (Present)</option>
                <option value="absent">غائب (Absent)</option>
                <option value="late">متأخر (Late)</option>
                <option value="excused">مأذون (Excused)</option>
              </select>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-2" v-if="form.status === 'present' || form.status === 'late'">
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">وقت الحضور</label>
              <input v-model="form.check_in_time" type="time" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">وقت الانصراف</label>
              <input v-model="form.check_out_time" type="time" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
            </div>
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">ملاحظات</label>
            <textarea v-model="form.notes" rows="2" placeholder="أسباب التأخير، رقم الإذن المسبق، إلخ..." class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm"></textarea>
          </div>
          <div class="flex justify-end gap-2 pt-4 border-t border-gray-200 dark:border-gray-800">
            <button type="button" @click="showAddModal = false" class="px-4 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">إلغاء</button>
            <button type="submit" class="px-4 py-2 text-xs font-medium text-white bg-brand-500 rounded-lg hover:bg-brand-600">تسجيل</button>
          </div>
        </form>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useSecretariatStore } from '@/stores/secretariat'
import { usePersonnelStore } from '@/stores/personnel'

const store = useSecretariatStore()
const personnelStore = usePersonnelStore()

const loading = ref(true)
const showAddModal = ref(false)

const logs = ref<any[]>([])
const employees = ref<any[]>([])

const dateFilter = ref(new Date().toISOString().split('T')[0])
const statusFilter = ref('')

const form = ref({
  employee: '',
  date: new Date().toISOString().split('T')[0],
  status: 'present',
  check_in_time: '08:00',
  check_out_time: '14:00',
  notes: ''
})

async function fetchAttendance() {
  loading.value = true
  try {
    const params: any = { date: dateFilter.value }
    if (statusFilter.value) params.status = statusFilter.value
    const res = await store.fetchAttendanceLogs(params)
    logs.value = res.results || []
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Compute statistics counts
const stats = computed(() => {
  const present = logs.value.filter(l => l.status === 'present').length
  const absent = logs.value.filter(l => l.status === 'absent').length
  const late = logs.value.filter(l => l.status === 'late').length
  const excused = logs.value.filter(l => l.status === 'excused').length

  return [
    { label: 'حاضرون اليوم', value: present, icon: '✓', iconBg: 'bg-green-50 dark:bg-green-950/20', iconColor: 'text-green-600 dark:text-green-400' },
    { label: 'غياب بدون عذر', value: absent, icon: '✗', iconBg: 'bg-red-50 dark:bg-red-950/20', iconColor: 'text-red-600 dark:text-red-400' },
    { label: 'متأخرون عن الدوام', value: late, icon: '⏰', iconBg: 'bg-amber-50 dark:bg-amber-950/20', iconColor: 'text-amber-600 dark:text-amber-400' },
    { label: 'إجازات ومأذونين', value: excused, icon: '✉', iconBg: 'bg-blue-50 dark:bg-blue-950/20', iconColor: 'text-blue-600 dark:text-blue-400' }
  ]
})

async function submitForm() {
  try {
    const data: any = { ...form.value }
    // Clean check times if absent/excused
    if (data.status === 'absent' || data.status === 'excused') {
      data.check_in_time = null
      data.check_out_time = null
    }
    await store.createAttendanceLog(data)
    showAddModal.value = false
    // reset form
    form.value = {
      employee: '',
      date: new Date().toISOString().split('T')[0],
      status: 'present',
      check_in_time: '08:00',
      check_out_time: '14:00',
      notes: ''
    }
    fetchAttendance()
  } catch (err) {
    console.error(err)
  }
}

onMounted(async () => {
  fetchAttendance()
  // Fetch employees
  await personnelStore.fetchPersonnel()
  employees.value = personnelStore.records || []
})
</script>
