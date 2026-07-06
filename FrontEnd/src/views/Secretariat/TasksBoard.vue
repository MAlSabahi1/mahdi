<template>
  <admin-layout>
    <!-- Breadcrumbs -->
    <nav class="flex mb-6" aria-label="Breadcrumb">
      <ol class="flex items-center gap-2 text-xs font-bold text-slate-550 dark:text-slate-400">
        <li class="inline-flex items-center">
          <router-link to="/" class="hover:text-brand-500 dark:hover:text-brand-400 transition flex items-center gap-1.5">
            <Inbox class="w-3.5 h-3.5" />
            الرئيسية
          </router-link>
        </li>
        <li class="flex items-center gap-2">
          <ChevronRight class="w-3 h-3 text-slate-400 rtl:rotate-180" />
          <span class="text-slate-800 dark:text-slate-200">إدارة المهام والمتابعة</span>
        </li>
      </ol>
    </nav>

    <div class="space-y-6">
      <!-- Search & Filters Action Bar -->
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between bg-white dark:bg-gray-900 p-5 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-theme-sm">
        <div class="flex flex-1 flex-col gap-4 sm:flex-row sm:items-center">
          <!-- Search input -->
          <div class="relative max-w-xs w-full">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="البحث في المهام والتكليفات..."
              class="w-full rounded-lg border border-gray-300 bg-gray-50 py-2.5 pl-4 pr-10 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-brand-500"
              @input="onSearch"
            />
          </div>
          <!-- Priority Filter -->
          <div class="w-full sm:w-40">
            <select
              v-model="priorityFilter"
              class="w-full rounded-lg border border-gray-300 bg-gray-50 py-2.5 px-3 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white cursor-pointer"
              @change="fetchData"
            >
              <option value="">الأولوية: الكل</option>
              <option value="low">منخفضة</option>
              <option value="medium">متوسطة</option>
              <option value="high">عالية</option>
            </select>
          </div>
          <!-- Status Filter -->
          <div class="w-full sm:w-40">
            <select
              v-model="statusFilter"
              class="w-full rounded-lg border border-gray-300 bg-gray-50 py-2.5 px-3 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white cursor-pointer"
              @change="fetchData"
            >
              <option value="">الحالة: الكل</option>
              <option value="pending">قيد الانتظار</option>
              <option value="in_progress">قيد العمل</option>
              <option value="completed">مكتملة</option>
            </select>
          </div>
        </div>
        
        <!-- Add Task Action Button — only for task managers (secretariat) -->
        <div class="flex justify-end">
          <button
            v-if="authStore.hasPermission('secretariat.task.manage')"
            @click="openAddModal"
            class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white hover:bg-brand-600 shadow-theme-xs cursor-pointer transition duration-300"
          >
            <Plus class="w-4 h-4" />
            <span>تكليف بمهمة جديدة</span>
          </button>
        </div>
      </div>

      <!-- Main Tasks Grid / Table -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
            <thead class="bg-gray-50 dark:bg-gray-800/50">
              <tr>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400">التكليف / المهمة</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400">المسؤول المكلف</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400">المراسلة المرتبطة</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400">الأولوية</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400">تاريخ الاستحقاق</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400">الحالة</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400">إجراءات</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 bg-white dark:divide-gray-800 dark:bg-gray-900">
              <tr v-if="loading">
                <td colspan="7" class="px-6 py-12 text-center text-sm text-gray-500">
                  <div class="flex flex-col items-center justify-center space-y-2">
                    <div class="w-8 h-8 border-4 border-brand-500/20 border-t-brand-500 rounded-full animate-spin"></div>
                    <span>جاري تحميل قائمة المهام...</span>
                  </div>
                </td>
              </tr>
              <tr v-else-if="tasks.length === 0">
                <td colspan="7" class="px-6 py-12 text-center text-sm text-gray-500">
                  <FolderOpen class="w-12 h-12 mx-auto text-slate-350 dark:text-slate-700 mb-3" />
                  لا توجد مهام أو تكليفات مسجلة حالياً تطابق الفلاتر.
                </td>
              </tr>
              <tr
                v-else
                v-for="task in tasks"
                :key="task.id"
                class="hover:bg-gray-50 dark:hover:bg-gray-800/20 transition duration-150"
              >
                <!-- Task Title & Description -->
                <td class="px-6 py-4">
                  <div>
                    <span class="block text-sm font-bold text-slate-850 dark:text-white">{{ task.title }}</span>
                    <span v-if="task.description" class="block text-xxs text-slate-450 dark:text-slate-500 mt-1 max-w-xs truncate" :title="task.description">
                      {{ task.description }}
                    </span>
                    <span class="block text-xxs text-slate-400 dark:text-slate-600 mt-1">
                      بواسطة: {{ task.created_by_name || 'النظام' }}
                    </span>
                  </div>
                </td>
                
                <!-- Assigned To -->
                <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-700 dark:text-slate-300 font-bold">
                  <div class="flex items-center gap-2">
                    <div class="w-7 h-7 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-xs font-black text-slate-600 dark:text-slate-400">
                      {{ (task.assigned_to_name || 'غير محدد').charAt(0) }}
                    </div>
                    <span>{{ task.assigned_to_name || 'غير محدد' }}</span>
                  </div>
                </td>

                <!-- Related Correspondence -->
                <td class="px-6 py-4 text-xs">
                  <div v-if="task.related_correspondence">
                    <router-link
                      :to="`/secretariat/correspondences/${task.related_correspondence}`"
                      class="text-brand-500 hover:text-brand-600 dark:text-brand-400 font-bold hover:underline block truncate max-w-[180px]"
                      :title="task.related_correspondence_subject"
                    >
                      {{ task.related_correspondence_subject || 'معاملة رقمية' }}
                    </router-link>
                  </div>
                  <span v-else class="text-slate-400 dark:text-slate-600">-</span>
                </td>

                <!-- Priority Badge -->
                <td class="px-6 py-4 whitespace-nowrap text-xs">
                  <span
                    :class="[
                      'px-2.5 py-0.5 rounded-full text-xxs font-black uppercase',
                      task.priority === 'high' ? 'bg-red-50 text-red-700 dark:bg-red-950/30 dark:text-red-400' :
                      task.priority === 'medium' ? 'bg-amber-50 text-amber-700 dark:bg-amber-950/30 dark:text-amber-400' :
                      'bg-slate-100 text-slate-755 dark:bg-slate-800 dark:text-slate-400'
                    ]"
                  >
                    {{ task.priority_display }}
                  </span>
                </td>

                <!-- Due Date -->
                <td class="px-6 py-4 whitespace-nowrap text-xs text-slate-600 dark:text-slate-400 font-bold">
                  {{ task.due_date }}
                </td>

                <!-- Interactive Status Badge (Same Formal Styling as correspondences list) -->
                <td class="px-6 py-4 whitespace-nowrap text-xs" @click.stop>
                  <select
                    v-model="task.status"
                    @change="updateTaskStatus(task.id, task.status)"
                    :class="[
                      'px-2.5 py-1 rounded-full text-xs font-bold cursor-pointer focus:outline-none focus:ring-0 border-0 appearance-none text-center inline-block',
                      task.status === 'completed' ? 'bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300' :
                      task.status === 'in_progress' ? 'bg-amber-50 text-amber-750 dark:bg-amber-900/30 dark:text-amber-300' :
                      'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
                    ]"
                  >
                    <option value="pending" class="bg-white dark:bg-slate-900 text-gray-700">قيد الانتظار</option>
                    <option value="in_progress" class="bg-white dark:bg-slate-900 text-amber-750">قيد العمل</option>
                    <option value="completed" class="bg-white dark:bg-slate-900 text-green-700">مكتملة</option>
                  </select>
                </td>

                <!-- Actions (Delete) — only for task managers -->
                <td class="px-6 py-4 whitespace-nowrap text-xs" @click.stop>
                  <button
                    v-if="authStore.hasPermission('secretariat.task.manage')"
                    @click="deleteTaskItem(task.id)"
                    class="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/20 rounded-lg transition cursor-pointer"
                    title="حذف التكليف"
                  >
                    <Trash2 class="w-4 h-4" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Add Task Modal Dialog -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm">
      <div class="w-full max-w-lg bg-white dark:bg-gray-900 rounded-2xl shadow-xl overflow-hidden border border-gray-200 dark:border-gray-800 animate-fade-in">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center bg-gray-50 dark:bg-gray-800/50">
          <h3 class="text-base font-black text-gray-900 dark:text-white">تكليف بمهمة متابعة جديدة</h3>
          <button @click="showAddModal = false" class="text-gray-400 hover:text-gray-650 dark:hover:text-gray-200 text-xl font-bold cursor-pointer">&times;</button>
        </div>
        <form @submit.prevent="submitTaskForm" class="p-6 space-y-4">
          <!-- Title -->
          <div>
            <label class="block text-xs font-black text-gray-700 dark:text-gray-300 mb-1.5">عنوان التكليف أو الأمر *</label>
            <input
              v-model="form.title"
              type="text"
              required
              placeholder="مثال: التحقق من صحة المرفق في المعاملة رقم 8987"
              class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
            />
          </div>

          <!-- Description -->
          <div>
            <label class="block text-xs font-black text-gray-700 dark:text-gray-300 mb-1.5">تفاصيل وتوجيهات المهمة</label>
            <textarea
              v-model="form.description"
              rows="3"
              placeholder="اكتب التوجيهات التفصيلية للموظف المكلف..."
              class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
            ></textarea>
          </div>

          <!-- Assigned To -->
          <div>
            <label class="block text-xs font-black text-gray-700 dark:text-gray-300 mb-1.5">الموظف المكلف بالمسؤولية *</label>
            <select
              v-model="form.assigned_to"
              required
              class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white cursor-pointer"
            >
              <option value="" disabled>اختر الموظف المكلف...</option>
              <option v-for="emp in employees" :key="emp.military_number" :value="emp.military_number">
                {{ emp.full_name }} ({{ emp.military_number }})
              </option>
            </select>
          </div>

          <!-- Related Correspondence (Link optionally!) -->
          <div>
            <label class="block text-xs font-black text-gray-700 dark:text-gray-300 mb-1.5">ربط بمعاملة صادر أو وارد (اختياري)</label>
            <select
              v-model="form.related_correspondence"
              class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white cursor-pointer"
            >
              <option value="">غير مرتبط بمراسلة معينة</option>
              <option v-for="corr in correspondences" :key="corr.id" :value="corr.id">
                {{ corr.reference_number }} - {{ corr.subject }}
              </option>
            </select>
          </div>

          <!-- Priority & Due Date -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-black text-gray-700 dark:text-gray-300 mb-1.5">الأولوية *</label>
              <select
                v-model="form.priority"
                required
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white cursor-pointer"
              >
                <option value="low">منخفضة</option>
                <option value="medium">متوسطة</option>
                <option value="high">عالية</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-black text-gray-700 dark:text-gray-300 mb-1.5">تاريخ الاستحقاق *</label>
              <input
                v-model="form.due_date"
                type="date"
                required
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white cursor-pointer"
              />
            </div>
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-800">
            <button
              type="button"
              @click="showAddModal = false"
              class="px-4.5 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700 dark:hover:bg-gray-700 transition cursor-pointer"
            >
              إلغاء
            </button>
            <button
              type="submit"
              :disabled="saving"
              class="px-5 py-2 text-sm font-medium text-white bg-brand-500 rounded-lg hover:bg-brand-600 transition disabled:opacity-50 cursor-pointer"
            >
              {{ saving ? 'جاري الحفظ...' : 'إسناد وحفظ' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import Swal from 'sweetalert2'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useSecretariatStore } from '@/stores/secretariat'
import { usePersonnelStore } from '@/stores/personnel'
import { useAuthStore } from '@/stores/auth'

// Icons
import { 
  Inbox, ChevronRight, FolderOpen, Plus, Trash2, Edit 
} from 'lucide-vue-next'

const { t } = useI18n()
const store = useSecretariatStore()
const personnelStore = usePersonnelStore()
const authStore = useAuthStore()

const loading = ref(true)
const saving = ref(false)
const tasks = ref<any[]>([])
const employees = ref<any[]>([])
const correspondences = ref<any[]>([])

const searchQuery = ref('')
const priorityFilter = ref('')
const statusFilter = ref('')

const showAddModal = ref(false)

const form = ref({
  title: '',
  description: '',
  assigned_to: '',
  related_correspondence: '',
  priority: 'medium',
  due_date: new Date(Date.now() + 86400000 * 3).toISOString().split('T')[0] // 3 days ahead
})

async function fetchData() {
  loading.value = true
  try {
    const params: any = {}
    if (searchQuery.value) params.search = searchQuery.value
    if (priorityFilter.value) params.priority = priorityFilter.value
    if (statusFilter.value) params.status = statusFilter.value

    const res = await store.fetchTasks(params)
    tasks.value = res.results || []
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

let searchTimeout: any = null
function onSearch() {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchData()
  }, 350)
}

async function openAddModal() {
  showAddModal.value = true
  
  // Load dependencies if needed
  try {
    if (employees.value.length === 0) {
      await personnelStore.fetchPersonnel()
      employees.value = personnelStore.records || []
    }
    if (correspondences.value.length === 0) {
      const corrRes = await store.fetchCorrespondences({ limit: 100 })
      correspondences.value = corrRes.results || []
    }
  } catch (err) {
    console.error(err)
  }
}

async function submitTaskForm() {
  saving.value = true
  try {
    const payload: any = { ...form.value }
    if (!payload.related_correspondence) {
      delete payload.related_correspondence
    }
    await store.createTask(payload)
    showAddModal.value = false
    
    // reset form
    form.value = {
      title: '',
      description: '',
      assigned_to: '',
      related_correspondence: '',
      priority: 'medium',
      due_date: new Date(Date.now() + 86400000 * 3).toISOString().split('T')[0]
    }
    fetchData()
  } catch (err) {
    console.error(err)
  } finally {
    saving.value = false
  }
}

async function updateTaskStatus(id: number, status: string) {
  if (status === 'completed') {
    const { value: notes } = await Swal.fire({
      title: 'إكمال التكليف/المهمة',
      input: 'textarea',
      inputLabel: 'ملاحظات الإنجاز ونتائج العمل',
      inputPlaceholder: 'اكتب هنا ما تم إنجازه أو أي ملاحظات...',
      inputAttributes: {
        'aria-label': 'اكتب هنا ما تم إنجازه أو أي ملاحظات'
      },
      showCancelButton: true,
      confirmButtonText: 'تأكيد الإكمال وتوقيع الكشف',
      cancelButtonText: 'إلغاء',
      inputValidator: (value) => {
        if (!value) {
          return 'يجب كتابة ملاحظات الإنجاز لتأكيد اكتمال المهمة!'
        }
      }
    })

    if (!notes) {
      // Revert status in UI/data
      await fetchData()
      return
    }

    try {
      await store.updateTask(id, { status, notes })
      Swal.fire({
        icon: 'success',
        title: 'تم تأكيد إكمال المهمة بنجاح',
        timer: 1500,
        showConfirmButton: false
      })
      await fetchData()
    } catch (err: any) {
      console.error(err)
      Swal.fire({
        icon: 'error',
        title: 'حدث خطأ أثناء تحديث المهمة',
        text: err.response?.data?.error || ''
      })
      await fetchData()
    }
  } else {
    try {
      await store.updateTask(id, { status })
      await fetchData()
    } catch (err: any) {
      console.error(err)
      Swal.fire({
        icon: 'error',
        title: 'حدث خطأ أثناء تحديث المهمة',
        text: err.response?.data?.error || ''
      })
      await fetchData()
    }
  }
}

async function deleteTaskItem(id: number) {
  if (!confirm('هل أنت متأكد من رغبتك في حذف هذا التكليف؟')) return
  try {
    await store.deleteTask(id)
    await fetchData()
  } catch (err) {
    console.error(err)
  }
}

onMounted(() => {
  fetchData()
})
</script>
