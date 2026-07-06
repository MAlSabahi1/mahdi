<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('secretariat.meetings.title')" />
    <div class="space-y-6">
      <!-- Search & Filters -->
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between bg-white dark:bg-gray-900 p-5 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-theme-sm">
        <div class="flex flex-1 flex-col gap-4 sm:flex-row sm:items-center">
          <div class="relative max-w-xs w-full">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="البحث في المحاضر والقرارات..."
              class="w-full rounded-lg border border-gray-300 bg-gray-50 py-2.5 px-4 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              @input="onSearch"
            />
          </div>
          <div class="w-full sm:w-48">
            <input
              v-model="dateFilter"
              type="date"
              class="w-full rounded-lg border border-gray-300 bg-gray-50 py-2.5 px-4 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              @change="fetchMeetings"
            />
          </div>
        </div>
        <div class="flex justify-end">
          <button
            @click="showAddModal = true"
            class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white hover:bg-brand-600 shadow-theme-xs cursor-pointer transition"
          >
            <span class="text-lg font-bold">+</span>
            {{ $t('secretariat.meetings.add') }}
          </button>
        </div>
      </div>

      <!-- Meeting Minutes List -->
      <div v-if="loading" class="text-center py-12 text-gray-500">
        {{ $t('common.loading') }}
      </div>
      <div v-else-if="meetings.length === 0" class="text-center py-12 text-gray-500 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-3xl">
        {{ $t('common.no_data') }}
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6 animate-fade-in">
        <div
          v-for="meeting in meetings"
          :key="meeting.id"
          class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-3xl p-6 shadow-theme-sm hover:shadow-md transition flex flex-col justify-between"
        >
          <div>
            <div class="flex justify-between items-start gap-4 mb-3">
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ meeting.title }}</h3>
              <span class="text-xs bg-brand-50 text-brand-700 dark:bg-brand-900/30 dark:text-brand-300 px-2.5 py-1 rounded-full font-semibold whitespace-nowrap">
                {{ meeting.date }}
              </span>
            </div>

            <!-- Content preview -->
            <div class="space-y-4 my-4">
              <div>
                <span class="block text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-1">وقائع المحضر والاجتماع</span>
                <p class="text-sm text-gray-700 dark:text-gray-300 line-clamp-3 bg-gray-50 dark:bg-gray-800/30 p-3 rounded-xl border border-gray-100 dark:border-gray-800/80 leading-relaxed">
                  {{ meeting.content }}
                </p>
              </div>

              <div v-if="meeting.decisions">
                <span class="block text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-1">القرارات والتوصيات</span>
                <p class="text-sm text-emerald-700 dark:text-emerald-300 font-medium bg-emerald-50/50 dark:bg-emerald-950/20 p-3 rounded-xl border border-emerald-100 dark:border-emerald-900/40 line-clamp-2 leading-relaxed">
                  {{ meeting.decisions }}
                </p>
              </div>
            </div>
          </div>

          <div class="mt-4 pt-4 border-t border-gray-100 dark:border-gray-800 flex justify-between items-center text-xs text-gray-500 dark:text-gray-400">
            <div>
              <span class="font-semibold text-gray-600 dark:text-gray-300">الحاضرين: </span>
              {{ meeting.attendees_details?.length || 0 }} منتسبين
              <span v-if="meeting.external_attendees"> + حضور خارجي</span>
            </div>
            <button
              @click="openDetails(meeting)"
              class="text-brand-500 hover:text-brand-600 dark:text-brand-400 font-bold hover:underline cursor-pointer"
            >
              عرض التفاصيل الكاملة
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Meeting Modal -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm">
      <div class="w-full max-w-3xl bg-white dark:bg-gray-900 rounded-3xl shadow-xl overflow-hidden border border-gray-200 dark:border-gray-800 animate-fade-in max-h-[90vh] flex flex-col">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center bg-gray-50 dark:bg-gray-800/50">
          <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('secretariat.meetings.add') }}</h3>
          <button @click="showAddModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl font-bold cursor-pointer">&times;</button>
        </div>
        <form @submit.prevent="submitForm" class="p-6 space-y-4 overflow-y-auto flex-1">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="md:col-span-2">
              <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">{{ $t('secretariat.meetings.meeting_title') }} *</label>
              <input
                v-model="form.title"
                type="text"
                required
                placeholder="مثال: اجتماع مناقشة خطة الربع الثالث، مناقشة تنظيم البريد"
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">{{ $t('secretariat.meetings.date') }} *</label>
              <input
                v-model="form.date"
                type="date"
                required
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">الحاضرين من المنتسبين (تحديد متعدد)</label>
              <div class="relative">
                <button
                  type="button"
                  @click="showAttendeesDropdown = !showAttendeesDropdown"
                  class="w-full text-right rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 dark:border-gray-700 dark:bg-gray-800 dark:text-white flex justify-between items-center cursor-pointer"
                >
                  <span>{{ form.attendees.length > 0 ? `${form.attendees.length} موظف محدد` : 'اختر الحاضرين...' }}</span>
                  <span class="text-xs">&#9662;</span>
                </button>
                <div v-if="showAttendeesDropdown" class="absolute z-10 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg max-h-48 overflow-y-auto p-2 space-y-1">
                  <div
                    v-for="emp in employees"
                    :key="emp.id"
                    @click="toggleAttendee(emp.id)"
                    class="flex items-center gap-2 p-1.5 hover:bg-gray-50 dark:hover:bg-gray-700 rounded cursor-pointer text-sm"
                  >
                    <input
                      type="checkbox"
                      :checked="form.attendees.includes(emp.id)"
                      class="rounded text-brand-500"
                    />
                    <span class="text-gray-900 dark:text-white">{{ emp.full_name }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">{{ $t('secretariat.meetings.external_attendees') }}</label>
              <textarea
                v-model="form.external_attendees"
                rows="2"
                placeholder="أسماء الحاضرين من خارج الإدارة (مفصولة بفاصلة أو سطر جديد)..."
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              ></textarea>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">{{ $t('secretariat.meetings.content') }} *</label>
              <textarea
                v-model="form.content"
                rows="5"
                required
                placeholder="تغطية كامل تفاصيل النقاشات، المقترحات والمداولات..."
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              ></textarea>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">{{ $t('secretariat.meetings.decisions') }}</label>
              <textarea
                v-model="form.decisions"
                rows="3"
                placeholder="التكليفات، القرارات المعتمدة، والتوصيات التي تم الاتفاق عليها..."
                class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3.5 py-2 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
              ></textarea>
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

    <!-- View Meeting Details Modal -->
    <div v-if="selectedMeeting" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm">
      <div class="w-full max-w-3xl bg-white dark:bg-gray-900 rounded-3xl shadow-xl overflow-hidden border border-gray-200 dark:border-gray-800 animate-fade-in max-h-[90vh] flex flex-col">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center bg-gray-50 dark:bg-gray-800/50">
          <h3 class="text-lg font-bold text-gray-900 dark:text-white">تفاصيل محضر الاجتماع</h3>
          <button @click="selectedMeeting = null" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl font-bold cursor-pointer">&times;</button>
        </div>
        <div class="p-6 space-y-6 overflow-y-auto flex-1">
          <div class="flex flex-wrap justify-between items-center gap-4">
            <h2 class="text-xl font-extrabold text-gray-900 dark:text-white">{{ selectedMeeting.title }}</h2>
            <span class="text-sm font-bold bg-brand-50 text-brand-700 dark:bg-brand-900/30 dark:text-brand-300 px-3 py-1 rounded-full">
              {{ selectedMeeting.date }}
            </span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 bg-gray-50 dark:bg-gray-800/30 p-4 rounded-2xl border border-gray-100 dark:border-gray-800">
            <div>
              <span class="block text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-1">الحاضرين من المنتسبين</span>
              <div v-if="!selectedMeeting.attendees_details || selectedMeeting.attendees_details.length === 0" class="text-sm text-gray-500">
                لم يتم تسجيل أي حضور من المنتسبين.
              </div>
              <ul v-else class="list-disc list-inside text-sm text-gray-800 dark:text-gray-300 space-y-1">
                <li v-for="att in selectedMeeting.attendees_details" :key="att.id">
                  {{ att.full_name }} ({{ att.military_number }})
                </li>
              </ul>
            </div>
            <div>
              <span class="block text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-1">حاضرين من خارج الإدارة</span>
              <p class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-line leading-relaxed">
                {{ selectedMeeting.external_attendees || 'لا يوجد حضور خارجي.' }}
              </p>
            </div>
          </div>

          <div>
            <span class="block text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-1">نص وتفاصيل المحضر</span>
            <p class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-line leading-relaxed bg-gray-50 dark:bg-gray-800/20 p-4 rounded-2xl border border-gray-150 dark:border-gray-800/80">
              {{ selectedMeeting.content }}
            </p>
          </div>

          <div v-if="selectedMeeting.decisions">
            <span class="block text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-1">القرارات والتوصيات</span>
            <p class="text-sm text-emerald-800 dark:text-emerald-300 font-semibold whitespace-pre-line leading-relaxed bg-emerald-50/50 dark:bg-emerald-950/20 p-4 rounded-2xl border border-emerald-100 dark:border-emerald-900/40">
              {{ selectedMeeting.decisions }}
            </p>
          </div>
        </div>
        <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-800 flex justify-end bg-gray-50 dark:bg-gray-800/50">
          <button
            @click="selectedMeeting = null"
            class="px-5 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 dark:bg-gray-850 dark:text-gray-300 dark:border-gray-700 dark:hover:bg-gray-800 transition cursor-pointer"
          >
            إغلاق
          </button>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useSecretariatStore } from '@/stores/secretariat'
import { usePersonnelStore } from '@/stores/personnel'

const store = useSecretariatStore()
const personnelStore = usePersonnelStore()

const loading = ref(true)
const saving = ref(false)
const meetings = ref<any[]>([])
const employees = ref<any[]>([])

const searchQuery = ref('')
const dateFilter = ref('')

const showAddModal = ref(false)
const showAttendeesDropdown = ref(false)
const selectedMeeting = ref<any | null>(null)

const form = ref({
  title: '',
  date: new Date().toISOString().split('T')[0],
  attendees: [] as number[],
  external_attendees: '',
  content: '',
  decisions: ''
})

async function fetchMeetings() {
  loading.value = true
  try {
    const params: any = {}
    if (searchQuery.value) params.search = searchQuery.value
    if (dateFilter.value) params.date = dateFilter.value
    
    const res = await store.fetchMeetings(params)
    meetings.value = res.results || []
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
    fetchMeetings()
  }, 350)
}

function openDetails(meeting: any) {
  selectedMeeting.value = meeting
}

function toggleAttendee(id: number) {
  const index = form.value.attendees.indexOf(id)
  if (index > -1) {
    form.value.attendees.splice(index, 1)
  } else {
    form.value.attendees.push(id)
  }
}

async function submitForm() {
  saving.value = true
  try {
    await store.createMeeting(form.value)
    showAddModal.value = false
    // reset form
    form.value = {
      title: '',
      date: new Date().toISOString().split('T')[0],
      attendees: [],
      external_attendees: '',
      content: '',
      decisions: ''
    }
    fetchMeetings()
  } catch (err) {
    console.error(err)
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  fetchMeetings()
  // Fetch employees list
  await personnelStore.fetchPersonnel()
  employees.value = personnelStore.records || []
})
</script>
