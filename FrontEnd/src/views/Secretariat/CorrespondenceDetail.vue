<template>
  <admin-layout>
    <div class="mb-4">
      <router-link
        to="/secretariat/correspondences"
        class="inline-flex items-center gap-2 text-sm font-medium text-gray-500 hover:text-brand-500 transition dark:text-gray-400 dark:hover:text-brand-400"
      >
        <span>&larr;</span> العودة لقائمة المراسلات
      </router-link>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="text-gray-500 dark:text-gray-400">{{ $t('common.loading') }}</div>
    </div>

    <div v-else-if="!correspondence" class="text-center py-12">
      <div class="text-red-500 font-bold">المراسلة غير موجودة أو تم حذفها.</div>
    </div>

    <div v-else class="space-y-6">
      <!-- Header Card -->
      <div class="relative overflow-hidden bg-gradient-to-r from-brand-600 to-indigo-600 dark:from-brand-800 dark:to-indigo-800 rounded-3xl p-6 md:p-8 text-white shadow-lg">
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(255,255,255,0.15),transparent)] pointer-events-none"></div>
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-6 relative z-10">
          <div>
            <div class="flex items-center gap-3 mb-2">
              <span
                :class="[
                  'px-3 py-1 rounded-full text-xs font-bold border border-white/20 uppercase tracking-wider',
                  correspondence.type === 'incoming' ? 'bg-blue-500/30' : 'bg-emerald-500/30'
                ]"
              >
                {{ correspondence.type_display }}
              </span>
              <span class="text-white/80 text-sm font-medium">المرجع: {{ correspondence.reference_number }}</span>
            </div>
            <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight">{{ correspondence.subject }}</h1>
            <p class="text-white/70 text-sm mt-2">تاريخ القيد: {{ correspondence.date }}</p>
          </div>
          <div class="flex items-center gap-3">
            <span class="text-white/80 text-sm font-semibold">حالة المراسلة:</span>
            <select
              v-model="correspondence.status"
              @change="updateStatus"
              class="bg-white/10 backdrop-blur-md border border-white/20 text-white rounded-xl px-4 py-2 text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-white/50 cursor-pointer"
            >
              <option value="new" class="text-gray-900">جديد</option>
              <option value="in_progress" class="text-gray-900">قيد المتابعة</option>
              <option value="completed" class="text-gray-900">مكتمل/مؤرشف</option>
            </select>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Details Card -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Information Card -->
          <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-3xl p-6 shadow-theme-sm">
            <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-5 border-b border-gray-100 dark:border-gray-850 pb-3">تفاصيل المراسلة</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div v-if="correspondence.type === 'incoming'">
                <span class="block text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-1">الجهة المرسلة</span>
                <span class="text-gray-900 dark:text-white font-semibold text-base">{{ correspondence.sender || 'غير محدد' }}</span>
              </div>
              <div v-else>
                <span class="block text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-1">الجهة المستقبلة</span>
                <span class="text-gray-900 dark:text-white font-semibold text-base">{{ correspondence.receiver || 'غير محدد' }}</span>
              </div>
              <div>
                <span class="block text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-1">تاريخ المراسلة</span>
                <span class="text-gray-900 dark:text-white font-semibold text-base">{{ correspondence.date }}</span>
              </div>
              <div class="md:col-span-2">
                <span class="block text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-1">ملاحظات وشروحات</span>
                <p class="text-gray-700 dark:text-gray-300 text-sm whitespace-pre-line leading-relaxed bg-gray-50 dark:bg-gray-800/40 p-4 rounded-2xl border border-gray-100 dark:border-gray-800">
                  {{ correspondence.notes || 'لا توجد ملاحظات مدونة لهذه المراسلة.' }}
                </p>
              </div>
            </div>
          </div>

          <!-- Attachments Section (Archiving) -->
          <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-3xl p-6 shadow-theme-sm">
            <div class="flex justify-between items-center mb-5 border-b border-gray-100 dark:border-gray-850 pb-3">
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('secretariat.correspondences.attachments') }}</h3>
              <button
                @click="showUploadForm = !showUploadForm"
                class="text-xs font-bold text-brand-500 hover:text-brand-600 dark:text-brand-400 flex items-center gap-1 cursor-pointer"
              >
                <span>{{ showUploadForm ? 'إلغاء' : '+ إرفاق مستند' }}</span>
              </button>
            </div>

            <!-- Upload attachment form -->
            <div v-if="showUploadForm" class="mb-6 p-5 bg-gray-50 dark:bg-gray-800/40 border border-gray-200 dark:border-gray-800 rounded-2xl animate-fade-in">
              <form @submit.prevent="handleUpload" class="space-y-4">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">{{ $t('secretariat.correspondences.attachment_title') }} *</label>
                  <input
                    v-model="attachmentForm.title"
                    type="text"
                    required
                    placeholder="مثال: صورة المذكرة الرسمية، الرد الرسمي، إلخ"
                    class="w-full rounded-lg border border-gray-300 bg-white px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">الملف *</label>
                  <input
                    type="file"
                    required
                    @change="onFileSelected"
                    class="w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100 dark:file:bg-brand-900/30 dark:file:text-brand-300 cursor-pointer"
                  />
                </div>
                <div class="flex justify-end gap-2 pt-2">
                  <button
                    type="submit"
                    :disabled="uploading"
                    class="px-4 py-2 text-xs font-semibold text-white bg-brand-500 hover:bg-brand-600 rounded-lg shadow-theme-xs disabled:opacity-50 transition cursor-pointer"
                  >
                    {{ uploading ? 'جاري الرفع...' : 'رفع وحفظ' }}
                  </button>
                </div>
              </form>
            </div>

            <!-- Attachments list -->
            <div v-if="!correspondence.attachments || correspondence.attachments.length === 0" class="text-center py-6 text-sm text-gray-500">
              {{ $t('secretariat.correspondences.no_attachments') }}
            </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4 animate-fade-in">
              <div
                v-for="file in correspondence.attachments"
                :key="file.id"
                class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800/30 border border-gray-150 dark:border-gray-800 rounded-2xl hover:shadow-theme-xs transition"
              >
                <div class="flex items-center gap-3 overflow-hidden">
                  <div class="p-2.5 bg-brand-50 dark:bg-brand-900/20 text-brand-600 dark:text-brand-400 rounded-xl">
                    <!-- File icon representation -->
                    <span class="font-bold text-xs">PDF</span>
                  </div>
                  <div class="overflow-hidden">
                    <span class="block text-sm font-semibold text-gray-800 dark:text-white truncate" :title="file.title">
                      {{ file.title }}
                    </span>
                    <span class="block text-xxs text-gray-400 dark:text-gray-500 mt-0.5">
                      تم الرفع: {{ new Date(file.uploaded_at).toLocaleString('ar-YE') }}
                    </span>
                  </div>
                </div>
                <div class="flex items-center gap-2">
                  <a
                    :href="file.file"
                    target="_blank"
                    download
                    class="p-2 text-gray-500 hover:text-brand-500 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition"
                    title="تحميل"
                  >
                    &darr;
                  </a>
                  <button
                    @click="deleteFile(file.id)"
                    class="p-2 text-gray-500 hover:text-red-500 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition cursor-pointer"
                    title="حذف"
                  >
                    &times;
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar Actions & Linked Tasks -->
        <div class="space-y-6">
          <!-- Quick actions / stats -->
          <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-3xl p-6 shadow-theme-sm">
            <h3 class="text-sm font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-4">مسؤول المراسلة</h3>
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center font-bold text-gray-700 dark:text-gray-300">
                U
              </div>
              <div>
                <span class="block text-sm font-semibold text-gray-900 dark:text-white">بواسطة: {{ correspondence.created_by_name || 'مسؤول السكرتارية' }}</span>
                <span class="block text-xs text-gray-400 dark:text-gray-500">جهة الاختصاص: {{ correspondence.security_admin_name || 'إدارة الأمن' }}</span>
              </div>
            </div>
          </div>

          <!-- Tasks list and Add Task linked to correspondence -->
          <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-3xl p-6 shadow-theme-sm">
            <div class="flex justify-between items-center mb-4 border-b border-gray-100 dark:border-gray-850 pb-3">
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">مهام المتابعة المرتبطة</h3>
              <button
                @click="showTaskForm = !showTaskForm"
                class="text-xs font-bold text-brand-500 hover:text-brand-600 dark:text-brand-400 cursor-pointer"
              >
                {{ showTaskForm ? 'إلغاء' : '+ مهمة جديدة' }}
              </button>
            </div>

            <!-- Task Form -->
            <div v-if="showTaskForm" class="mb-5 p-4 bg-gray-50 dark:bg-gray-800/40 border border-gray-200 dark:border-gray-800 rounded-2xl animate-fade-in space-y-3">
              <div>
                <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">عنوان التكليف *</label>
                <input
                  v-model="taskForm.title"
                  type="text"
                  required
                  class="w-full rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                />
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">تفاصيل ومبررات المهمة</label>
                <textarea
                  v-model="taskForm.description"
                  rows="2"
                  class="w-full rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                ></textarea>
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">الموظف المسؤول *</label>
                <select
                  v-model="taskForm.assigned_to"
                  required
                  class="w-full rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                >
                  <option value="" disabled>اختر الموظف...</option>
                  <option v-for="emp in employees" :key="emp.id" :value="emp.id">
                    {{ emp.full_name }} ({{ emp.military_number }})
                  </option>
                </select>
              </div>
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">تاريخ الاستحقاق *</label>
                  <input
                    v-model="taskForm.due_date"
                    type="date"
                    required
                    class="w-full rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                  />
                </div>
                <div>
                  <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">الأولوية</label>
                  <select
                    v-model="taskForm.priority"
                    class="w-full rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                  >
                    <option value="low">منخفضة</option>
                    <option value="medium">متوسطة</option>
                    <option value="high">عالية</option>
                  </select>
                </div>
              </div>
              <div class="flex justify-end pt-1">
                <button
                  type="button"
                  @click="handleAddTask"
                  class="px-4 py-1.5 text-xs font-semibold text-white bg-brand-500 hover:bg-brand-600 rounded-lg cursor-pointer"
                >
                  حفظ المهمة
                </button>
              </div>
            </div>

            <!-- Linked Tasks list -->
            <div v-if="linkedTasks.length === 0" class="text-center py-4 text-xs text-gray-500">
              لا توجد مهام متابعة مرتبطة بهذه المراسلة حالياً.
            </div>
            <div v-else class="space-y-3">
              <div
                v-for="task in linkedTasks"
                :key="task.id"
                class="p-3 border border-gray-150 dark:border-gray-800 rounded-2xl bg-gray-50/50 dark:bg-gray-800/10"
              >
                <div class="flex justify-between items-start gap-2">
                  <span class="text-sm font-semibold text-gray-800 dark:text-white">{{ task.title }}</span>
                  <span
                    :class="[
                      'text-xxs px-2 py-0.5 rounded-full font-semibold',
                      task.status === 'completed' ? 'bg-green-50 text-green-700 dark:bg-green-900/30' :
                      task.status === 'in_progress' ? 'bg-amber-50 text-amber-700 dark:bg-amber-900/30' :
                      'bg-gray-100 text-gray-700 dark:bg-gray-850'
                    ]"
                  >
                    {{ task.status_display }}
                  </span>
                </div>
                <div class="mt-2 flex flex-col gap-1 text-xxs text-gray-400 dark:text-gray-500 font-medium">
                  <div>مكلف إلى: <span class="text-gray-600 dark:text-gray-300">{{ task.assigned_to_name }}</span></div>
                  <div class="flex justify-between">
                    <span>الاستحقاق: {{ task.due_date }}</span>
                    <span
                      :class="[
                        'font-bold uppercase',
                        task.priority === 'high' ? 'text-red-500' :
                        task.priority === 'medium' ? 'text-amber-500' : 'text-gray-400'
                      ]"
                    >
                      أولوية: {{ task.priority_display }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useSecretariatStore } from '@/stores/secretariat'
import { usePersonnelStore } from '@/stores/personnel'

const { t } = useI18n()
const store = useSecretariatStore()
const personnelStore = usePersonnelStore()
const route = useRoute()

const loading = ref(true)
const uploading = ref(false)
const correspondence = ref<any>(null)
const linkedTasks = ref<any[]>([])
const employees = ref<any[]>([])

const showUploadForm = ref(false)
const showTaskForm = ref(false)

const attachmentForm = ref({
  title: '',
  file: null as File | null
})

const taskForm = ref({
  title: '',
  description: '',
  assigned_to: '',
  priority: 'medium',
  due_date: new Date(Date.now() + 86400000 * 3).toISOString().split('T')[0], // 3 days in future
  related_correspondence: ''
})

async function fetchDetails() {
  loading.value = true
  try {
    const id = route.params.id as string
    const res = await store.fetchCorrespondenceById(id)
    correspondence.value = res
    
    // Fetch linked tasks
    const tasksRes = await store.fetchTasks({ related_correspondence: id })
    linkedTasks.value = tasksRes.results || []

    // Fetch personnel for task assignment
    if (employees.value.length === 0) {
      await personnelStore.fetchPersonnel()
      employees.value = personnelStore.records || []
    }
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function updateStatus() {
  try {
    const id = route.params.id as string
    await store.updateCorrespondence(id, { status: correspondence.value.status })
    // fetch again to update displays
    const res = await store.fetchCorrespondenceById(id)
    correspondence.value = res
  } catch (err) {
    console.error(err)
  }
}

function onFileSelected(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    attachmentForm.value.file = target.files[0]
  }
}

async function handleUpload() {
  if (!attachmentForm.value.file || !attachmentForm.value.title) return
  uploading.value = true
  try {
    const id = route.params.id as string
    const formData = new FormData()
    formData.append('correspondence', id)
    formData.append('title', attachmentForm.value.title)
    formData.append('file', attachmentForm.value.file)

    await store.uploadAttachment(formData)
    showUploadForm.value = false
    attachmentForm.value = { title: '', file: null }
    
    // Refresh
    const res = await store.fetchCorrespondenceById(id)
    correspondence.value = res
  } catch (err) {
    console.error(err)
  } finally {
    uploading.value = false
  }
}

async function deleteFile(fileId: number) {
  if (!confirm('هل أنت متأكد من رغبتك في حذف هذا الملف المرفق؟')) return
  try {
    await store.deleteAttachment(fileId)
    const id = route.params.id as string
    const res = await store.fetchCorrespondenceById(id)
    correspondence.value = res
  } catch (err) {
    console.error(err)
  }
}

async function handleAddTask() {
  if (!taskForm.value.title || !taskForm.value.assigned_to) return
  try {
    const id = route.params.id as string
    taskForm.value.related_correspondence = id
    await store.createTask(taskForm.value)
    
    // reset task form
    taskForm.value = {
      title: '',
      description: '',
      assigned_to: '',
      priority: 'medium',
      due_date: new Date(Date.now() + 86400000 * 3).toISOString().split('T')[0],
      related_correspondence: ''
    }
    showTaskForm.value = false
    
    // Refresh tasks list
    const tasksRes = await store.fetchTasks({ related_correspondence: id })
    linkedTasks.value = tasksRes.results || []
  } catch (err) {
    console.error(err)
  }
}

onMounted(() => {
  fetchDetails()
})
</script>
