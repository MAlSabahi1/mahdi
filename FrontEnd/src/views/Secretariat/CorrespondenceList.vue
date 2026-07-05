<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('secretariat.correspondences.title')" />
    <div class="space-y-6">
      <!-- Top Action Bar & Filters -->
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between bg-white dark:bg-gray-900 p-5 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-theme-sm">
        <div class="flex flex-1 flex-col gap-4 sm:flex-row sm:items-center">
          <!-- Search input -->
          <div class="relative max-w-xs w-full">
            <input
              v-model="searchQuery"
              type="text"
              :placeholder="$t('common.search')"
              class="w-full rounded-lg border border-gray-300 bg-gray-50 py-2.5 pl-4 pr-10 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-brand-500"
              @input="onSearch"
            />
          </div>
          <!-- Type Filter -->
          <div class="w-full sm:w-40">
            <select
              v-model="typeFilter"
              class="w-full rounded-lg border border-gray-300 bg-gray-50 py-2.5 px-3 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              @change="fetchData"
            >
              <option value="">{{ $t('secretariat.correspondences.type') }}: الكل</option>
              <option value="incoming">وارد (Incoming)</option>
              <option value="outgoing">صادر (Outgoing)</option>
            </select>
          </div>
          <!-- Status Filter -->
          <div class="w-full sm:w-40">
            <select
              v-model="statusFilter"
              class="w-full rounded-lg border border-gray-300 bg-gray-50 py-2.5 px-3 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              @change="fetchData"
            >
              <option value="">الحالة: الكل</option>
              <option value="new">جديد</option>
              <option value="in_progress">قيد المتابعة</option>
              <option value="completed">مكتمل/مؤرشف</option>
            </select>
          </div>
        </div>
        <div class="flex justify-end">
          <button
            @click="showAddModal = true"
            class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white hover:bg-brand-600 shadow-theme-xs cursor-pointer transition"
          >
            <span class="text-lg font-bold">+</span>
            {{ $t('secretariat.correspondences.add') }}
          </button>
        </div>
      </div>

      <!-- Correspondence Table -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
            <thead class="bg-gray-50 dark:bg-gray-800/50">
              <tr>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400">{{ $t('secretariat.correspondences.reference') }}</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400">{{ $t('secretariat.correspondences.subject') }}</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400">{{ $t('secretariat.correspondences.type') }}</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400">المرسل / المستقبل</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400">التاريخ</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400">{{ $t('secretariat.correspondences.status') }}</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400">{{ $t('common.actions') }}</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 bg-white dark:divide-gray-800 dark:bg-gray-900">
              <tr v-if="loading">
                <td colspan="7" class="px-6 py-8 text-center text-sm text-gray-500">{{ $t('common.loading') }}</td>
              </tr>
              <tr v-else-if="correspondences.length === 0">
                <td colspan="7" class="px-6 py-8 text-center text-sm text-gray-500">{{ $t('common.no_data') }}</td>
              </tr>
              <tr
                v-else
                v-for="item in correspondences"
                :key="item.id"
                class="hover:bg-gray-50 dark:hover:bg-gray-800/30 transition cursor-pointer"
                @click="goToDetail(item.id)"
              >
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  {{ item.reference_number }}
                </td>
                <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 font-medium">
                  {{ item.subject }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                  <span
                    :class="[
                      'px-2.5 py-1 rounded-full text-xs font-semibold',
                      item.type === 'incoming'
                        ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'
                        : 'bg-indigo-50 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300'
                    ]"
                  >
                    {{ item.type_display }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                  <div v-if="item.type === 'incoming'">
                    <span class="font-medium text-gray-600 dark:text-gray-300">من:</span> {{ item.sender }}
                  </div>
                  <div v-else>
                    <span class="font-medium text-gray-600 dark:text-gray-300">إلى:</span> {{ item.receiver }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ item.date }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                  <span
                    :class="[
                      'px-2.5 py-1 rounded-full text-xs font-medium',
                      item.status === 'new' ? 'bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300' :
                      item.status === 'in_progress' ? 'bg-amber-50 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300' :
                      'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
                    ]"
                  >
                    {{ item.status_display }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400" @click.stop>
                  <router-link
                    :to="`/secretariat/correspondences/${item.id}`"
                    class="text-brand-500 hover:text-brand-600 dark:text-brand-400 font-medium hover:underline"
                  >
                    {{ $t('secretariat.correspondences.details') }}
                  </router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Add Correspondence Modal -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm">
      <div class="w-full max-w-2xl bg-white dark:bg-gray-900 rounded-2xl shadow-xl overflow-hidden border border-gray-200 dark:border-gray-800 animate-fade-in">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center bg-gray-50 dark:bg-gray-800/50">
          <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('secretariat.correspondences.add') }}</h3>
          <button @click="showAddModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl font-bold cursor-pointer">&times;</button>
        </div>
        <form @submit.prevent="submitForm" class="p-6 space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">{{ $t('secretariat.correspondences.reference') }} *</label>
              <input
                v-model="form.reference_number"
                type="text"
                required
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">{{ $t('secretariat.correspondences.type') }} *</label>
              <select
                v-model="form.type"
                required
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              >
                <option value="incoming">وارد (Incoming)</option>
                <option value="outgoing">صادر (Outgoing)</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">{{ $t('secretariat.correspondences.subject') }} *</label>
              <input
                v-model="form.subject"
                type="text"
                required
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">{{ $t('secretariat.correspondences.sender') }}</label>
              <input
                v-model="form.sender"
                type="text"
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">{{ $t('secretariat.correspondences.receiver') }}</label>
              <input
                v-model="form.receiver"
                type="text"
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">{{ $t('secretariat.correspondences.date') }} *</label>
              <input
                v-model="form.date"
                type="date"
                required
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">الحالة *</label>
              <select
                v-model="form.status"
                required
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              >
                <option value="new">جديد</option>
                <option value="in_progress">قيد المتابعة</option>
                <option value="completed">مكتمل/مؤرشف</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">{{ $t('secretariat.correspondences.notes') }}</label>
              <textarea
                v-model="form.notes"
                rows="3"
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              ></textarea>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">مرفق المعاملة / صورة المذكرة الورقية</label>
              <input
                type="file"
                @change="onFileChange"
                accept="image/*,application/pdf"
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              />
            </div>
          </div>
          <div class="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-800">
            <button
              type="button"
              @click="showAddModal = false"
              class="px-4.5 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700 dark:hover:bg-gray-700 transition cursor-pointer"
            >
              {{ $t('common.cancel') }}
            </button>
            <button
              type="submit"
              :disabled="saving"
              class="px-5 py-2 text-sm font-medium text-white bg-brand-500 rounded-lg hover:bg-brand-600 transition disabled:opacity-50 cursor-pointer"
            >
              {{ saving ? $t('common.loading') : $t('common.save') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { useSecretariatStore } from '@/stores/secretariat'

const { t } = useI18n()
const store = useSecretariatStore()
const router = useRouter()

const loading = ref(true)
const saving = ref(false)
const correspondences = ref<any[]>([])

const searchQuery = ref('')
const typeFilter = ref('')
const statusFilter = ref('')

const showAddModal = ref(false)
const selectedFile = ref<File | null>(null)

function onFileChange(e: any) {
  const file = e.target.files[0]
  if (file) {
    selectedFile.value = file
  }
}

const form = ref({
  reference_number: '',
  subject: '',
  type: 'incoming',
  sender: '',
  receiver: '',
  date: new Date().toISOString().split('T')[0],
  status: 'new',
  notes: ''
})

async function fetchData() {
  loading.value = true
  try {
    const params: any = {}
    if (searchQuery.value) params.search = searchQuery.value
    if (typeFilter.value) params.type = typeFilter.value
    if (statusFilter.value) params.status = statusFilter.value
    
    const res = await store.fetchCorrespondences(params)
    correspondences.value = res.results || []
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

function goToDetail(id: number) {
  router.push(`/secretariat/correspondences/${id}`)
}

async function submitForm() {
  saving.value = true
  try {
    const res = await store.createCorrespondence(form.value)
    
    // If a file was selected, upload it immediately
    if (selectedFile.value && res && res.id) {
      const formData = new FormData()
      formData.append('correspondence', res.id.toString())
      formData.append('file', selectedFile.value)
      formData.append('title', 'صورة المرفق المرفوعة عند التقييد')
      await store.uploadAttachment(formData)
    }

    showAddModal.value = false
    selectedFile.value = null
    
    // reset form
    form.value = {
      reference_number: '',
      subject: '',
      type: 'incoming',
      sender: '',
      receiver: '',
      date: new Date().toISOString().split('T')[0],
      status: 'new',
      notes: ''
    }
    fetchData()
  } catch (err) {
    console.error(err)
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

