<template>
  <admin-layout>
    <div class="space-y-6 pb-20">

      <!-- ─── Header ─────────────────────────────────────────────────── -->
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 class="text-2xl font-bold text-gray-800 dark:text-white/90">الإعدادات العامة للنظام</h2>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            إدارة سياسات التقاعد، الترقيات، الخدمات، والإعدادات التشغيلية — تنعكس فوراً على المحرك الاستباقي
          </p>
        </div>
        <div class="flex items-center gap-2 text-sm text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl px-4 py-2">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
          جميع التعديلات تُحفظ في قاعدة البيانات ولا تتطلب تعديل الكود
        </div>
      </div>

      <!-- ─── Layout: Tabs + Content ─────────────────────────────────── -->
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">

        <!-- Sidebar Tabs -->
        <div class="lg:col-span-1 space-y-1">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-right',
              activeTab === tab.id
                ? 'bg-brand-600 text-white shadow-theme-sm'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800'
            ]"
          >
            <span v-html="tab.icon" class="w-5 h-5 shrink-0"></span>
            <div class="flex-1 text-right">
              <div>{{ tab.label }}</div>
              <div class="text-xs opacity-60 mt-0.5 hidden sm:block">{{ getCount(tab.id) }} إعداد</div>
            </div>
            <span
              v-if="getCount(tab.id) === 0"
              class="shrink-0 px-1.5 py-0.5 text-[10px] rounded bg-gray-200 dark:bg-gray-700 text-gray-500"
            >فارغ</span>
          </button>
        </div>

        <!-- Settings Panel -->
        <div class="lg:col-span-3">
          <!-- Loading -->
          <div v-if="loading" class="flex items-center justify-center h-48 rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
            <svg class="h-8 w-8 animate-spin text-brand-500" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
          </div>

          <!-- Empty tab -->
          <div
            v-else-if="filteredSettings.length === 0"
            class="flex flex-col items-center justify-center h-48 rounded-2xl border border-dashed border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-center"
          >
            <svg class="w-10 h-10 text-gray-300 dark:text-gray-600 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
            </svg>
            <p class="text-sm text-gray-500 dark:text-gray-400">لا توجد إعدادات في هذا التصنيف بعد.</p>
            <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">سيتم إضافتها من الـ Backend عند الحاجة.</p>
          </div>

          <!-- Sub-tabs Header -->
          <div v-if="Object.keys(groupedSettings).length > 1" class="flex flex-wrap gap-2 mb-6 border-b border-gray-200 dark:border-gray-800 pb-4">
            <button
              v-for="(_, groupName) in groupedSettings"
              :key="groupName"
              @click="activeSubTab = groupName"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-bold transition-all',
                activeSubTab === groupName
                  ? 'bg-brand-50 text-brand-700 dark:bg-brand-900/30 dark:text-brand-400 border border-brand-200 dark:border-brand-800/50 shadow-sm'
                  : 'text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 border border-transparent'
              ]"
            >
              {{ groupName }}
            </button>
          </div>

          <!-- Settings Cards for Active Sub-tab -->
          <div v-if="groupedSettings[activeSubTab]" class="space-y-3">
            <div
              v-for="setting in groupedSettings[activeSubTab]"
              :key="setting.id"
              class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5 shadow-theme-xs hover:border-brand-200 dark:hover:border-brand-700 transition-colors"
            >
              <div class="flex items-start justify-between gap-6">
                <!-- Info -->
                <div class="flex-1 min-w-0">
                  <h3 class="font-bold text-gray-900 dark:text-white text-sm">{{ setting.title }}</h3>
                  <p v-if="setting.description" class="text-xs text-gray-500 dark:text-gray-400 mt-1 mb-4">{{ setting.description }}</p>

                  <!-- Input -->
                  <div class="flex items-center gap-3 mt-3">
                    <!-- Number -->
                    <input
                      v-if="setting.value_type === 'int' || setting.value_type === 'float'"
                      type="number"
                      v-model="setting._edit"
                      class="w-28 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 px-3 py-2 text-sm font-bold text-gray-900 dark:text-white shadow-theme-xs focus:border-brand-400 focus:ring-2 focus:ring-brand-500/10 outline-none"
                    />
                    <!-- Bool -->
                    <div v-else-if="setting.value_type === 'bool'" class="flex items-center gap-3">
                      <button
                        @click="setting._edit = 'True'"
                        :class="['px-4 py-2 rounded-lg text-sm font-bold border transition-all', setting._edit === 'True' ? 'bg-emerald-600 text-white border-emerald-600' : 'border-gray-300 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:border-emerald-400']"
                      >نعم</button>
                      <button
                        @click="setting._edit = 'False'"
                        :class="['px-4 py-2 rounded-lg text-sm font-bold border transition-all', setting._edit === 'False' ? 'bg-red-500 text-white border-red-500' : 'border-gray-300 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:border-red-400']"
                      >لا</button>
                    </div>
                    <!-- Text -->
                    <input
                      v-else
                      type="text"
                      v-model="setting._edit"
                      class="flex-1 max-w-sm rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 px-3 py-2 text-sm text-gray-900 dark:text-white shadow-theme-xs focus:border-brand-400 focus:ring-2 focus:ring-brand-500/10 outline-none"
                    />

                    <!-- Save button (appears when changed) -->
                    <button
                      v-if="String(setting._edit) !== String(setting.value)"
                      @click="saveSetting(setting)"
                      :disabled="saving === setting.id"
                      class="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-brand-600 hover:bg-brand-700 disabled:opacity-60 text-white text-xs font-bold shadow-theme-xs transition-all"
                    >
                      <svg v-if="saving === setting.id" class="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                      <svg v-else class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                      حفظ
                    </button>

                    <!-- Saved feedback -->
                    <transition enter-active-class="transition-all duration-200" enter-from-class="opacity-0 scale-90" leave-to-class="opacity-0">
                      <span v-if="savedId === setting.id" class="text-xs font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                        تم الحفظ
                      </span>
                    </transition>
                  </div>
                </div>

                <!-- Key Badge -->
                <div class="shrink-0 text-right">
                  <code class="inline-block text-[10px] bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 px-2 py-1 rounded-md font-mono">{{ setting.key }}</code>
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
import { ref, computed, onMounted, watch } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import api from '@/lib/api'

const activeTab = ref('retirement')
const activeSubTab = ref('')
const loading = ref(false)
const saving = ref<number | null>(null)
const savedId = ref<number | null>(null)
const allSettings = ref<any[]>([])

const tabs = [
  {
    id: 'retirement',
    label: 'إعدادات التقاعد',
    icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>',
  },
  {
    id: 'promotions',
    label: 'إعدادات الترقيات',
    icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>',
  },
  {
    id: 'services',
    label: 'إعدادات الخدمات',
    icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>',
  },
  {
    id: 'holidays',
    label: 'إعدادات الإجازات',
    icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>',
  },
  {
    id: 'system',
    label: 'إعدادات عامة',
    icon: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/></svg>',
  },
]

const filteredSettings = computed(() =>
  allSettings.value.filter(s => s.category === activeTab.value)
)

const groupedSettings = computed(() => {
  const groups: Record<string, any[]> = {}
  filteredSettings.value.forEach(s => {
    let g = 'إعدادات عامة'
    const k = s.key.toLowerCase()
    
    // Services grouping
    if (k.startsWith('study_leave')) g = 'سياسات التفريغ الدراسي'
    else if (k.includes('attachment')) g = 'إعدادات المرفقات والملفات'
    else if (k.includes('form') || k.includes('submission')) g = 'إعدادات سير عمل الاستمارات'
    
    // System / Holidays / Retirement grouping
    else if (k.includes('leave') || k.includes('absence')) g = 'سياسات الإجازات والغياب'
    else if (k.includes('retirement') || k.includes('pension')) g = 'سياسات التقاعد'
    else if (k.includes('warning') || k.includes('alert')) g = 'إعدادات التنبيهات والإشعارات'
    else if (k.includes('print')) g = 'إعدادات الطباعة والتقارير'
    else if (k.includes('session') || k.includes('audit')) g = 'إعدادات الحماية والتدقيق'

    if (!groups[g]) groups[g] = []
    groups[g].push(s)
  })
  
  // Sort groups: Put "إعدادات عامة" at the end if it exists
  const sortedGroups: Record<string, any[]> = {}
  Object.keys(groups).sort((a, b) => {
    if (a === 'إعدادات عامة') return 1;
    if (b === 'إعدادات عامة') return -1;
    return a.localeCompare(b);
  }).forEach(key => {
    sortedGroups[key] = groups[key];
  });
  
  return sortedGroups
})

watch(groupedSettings, (newGroups) => {
  const keys = Object.keys(newGroups)
  if (keys.length > 0 && !keys.includes(activeSubTab.value)) {
    activeSubTab.value = keys[0]
  }
}, { immediate: true })

const getCount = (tabId: string) =>
  allSettings.value.filter(s => s.category === tabId).length

const fetchSettings = async () => {
  loading.value = true
  try {
    const res = await api.get('/dictionaries/system-settings/?limit=1000')
    const data = res.data.results ?? res.data
    allSettings.value = data.map((s: any) => ({
      ...s,
      _edit: String(s.value),
    }))
  } catch (e) {
    console.error('Failed to load settings', e)
  } finally {
    loading.value = false
  }
}

const saveSetting = async (setting: any) => {
  saving.value = setting.id
  try {
    await api.patch(`/dictionaries/system-settings/${setting.id}/`, { value: setting._edit })
    setting.value = setting._edit
    savedId.value = setting.id
    setTimeout(() => { savedId.value = null }, 2500)
  } catch (e) {
    console.error('Failed to save', e)
  } finally {
    saving.value = null
  }
}

onMounted(fetchSettings)
</script>
