<template>
  <admin-layout>
    <div class="space-y-6 pb-20">

      <!-- ─── Page Header ─────────────────────────────────────────────── -->
      <div class="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h2 class="text-2xl font-bold text-gray-800 dark:text-white/90">لوحة الإنذارات المبكرة</h2>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            المحرك الاستباقي — يفحص قاعدة البيانات حالياً ويحسب الأعمار والمدد من سجلات الأفراد
          </p>
        </div>
        <div class="flex items-center gap-2">
          <!-- Filter by warning type -->
          <select
            v-model="activeFilter"
            class="h-10 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-700 shadow-theme-xs focus:border-brand-300 focus:outline-none focus:ring-2 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-300"
          >
            <option value="">جميع الإنذارات</option>
            <option value="exceeded">تجاوزوا السن / المدة 🔴</option>
            <option value="critical">أقل من شهر ⛔</option>
            <option value="high">أقل من 3 أشهر 🔴</option>
            <option value="medium">أقل من 6 أشهر 🟠</option>
            <option value="low">أقل من سنة 🟡</option>
            <option value="info">بيانات ناقصة ⚠️</option>
          </select>

          <button
            @click="runEngine"
            :disabled="loading"
            class="flex items-center gap-2 h-10 rounded-lg bg-brand-600 hover:bg-brand-700 disabled:opacity-60 px-4 text-sm font-semibold text-white shadow-theme-xs transition-all"
          >
            <svg :class="['w-4 h-4', loading && 'animate-spin']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ loading ? 'جاري الفحص...' : 'تشغيل محرك الفحص' }}
          </button>
        </div>
      </div>

      <!-- ─── Stats Cards ────────────────────────────────────────────── -->
      <div v-if="stats" class="grid grid-cols-2 md:grid-cols-5 gap-4">
        <!-- تجاوزوا السن -->
        <div
          @click="activeFilter = activeFilter === 'exceeded' ? '' : 'exceeded'"
          :class="['cursor-pointer rounded-2xl border p-4 transition-all', activeFilter === 'exceeded' ? 'border-red-400 ring-2 ring-red-200 dark:ring-red-800' : 'border-red-100 dark:border-red-900/40']"
          class="bg-gradient-to-br from-red-50 to-red-100/50 dark:from-red-950/30 dark:to-red-900/20"
        >
          <div class="flex items-center gap-2 mb-3">
            <div class="w-8 h-8 rounded-full bg-red-100 dark:bg-red-900/50 flex items-center justify-center">
              <svg class="w-4 h-4 text-red-600 dark:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
            </div>
            <span class="text-xs font-semibold text-red-700 dark:text-red-400">تجاوزوا السن / المدة</span>
          </div>
          <div class="text-3xl font-black text-red-700 dark:text-red-300">{{ stats.exceeded_age + stats.exceeded_service }}</div>
          <p class="text-xs text-red-600/70 dark:text-red-400/60 mt-1">{{ stats.exceeded_age }} بلغوا السن • {{ stats.exceeded_service }} أتمّوا المدة</p>
        </div>

        <!-- مقتربون -->
        <div
          @click="activeFilter = activeFilter === 'medium' ? '' : 'medium'"
          :class="['cursor-pointer rounded-2xl border p-4 transition-all', activeFilter === 'medium' ? 'border-orange-400 ring-2 ring-orange-200 dark:ring-orange-800' : 'border-orange-100 dark:border-orange-900/40']"
          class="bg-gradient-to-br from-orange-50 to-amber-100/50 dark:from-orange-950/30 dark:to-amber-900/20"
        >
          <div class="flex items-center gap-2 mb-3">
            <div class="w-8 h-8 rounded-full bg-orange-100 dark:bg-orange-900/50 flex items-center justify-center">
              <svg class="w-4 h-4 text-orange-600 dark:text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
            <span class="text-xs font-semibold text-orange-700 dark:text-orange-400">إنذار تقاعد مبكر</span>
          </div>
          <div class="text-3xl font-black text-orange-700 dark:text-orange-300">{{ stats.approaching }}</div>
          <p class="text-xs text-orange-600/70 dark:text-orange-400/60 mt-1">أقل من {{ settings?.warning_months || 6 }} أشهر على التقاعد</p>
        </div>

        <!-- حالات مؤقتة -->
        <div
          @click="activeFilter = activeFilter === 'temp' ? '' : 'temp'"
          :class="['cursor-pointer rounded-2xl border p-4 transition-all', activeFilter === 'temp' ? 'border-purple-400 ring-2 ring-purple-200 dark:ring-purple-800' : 'border-purple-100 dark:border-purple-900/40']"
          class="bg-gradient-to-br from-purple-50 to-purple-100/50 dark:from-purple-950/30 dark:to-purple-900/20"
        >
          <div class="flex items-center gap-2 mb-3">
            <div class="w-8 h-8 rounded-full bg-purple-100 dark:bg-purple-900/50 flex items-center justify-center">
              <svg class="w-4 h-4 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
            </div>
            <span class="text-xs font-semibold text-purple-700 dark:text-purple-400">حالات مؤقتة منتهية</span>
          </div>
          <div class="text-3xl font-black text-purple-700 dark:text-purple-300">{{ stats.temp_status_ending }}</div>
          <p class="text-xs text-purple-600/70 dark:text-purple-400/60 mt-1">دراسة / سجن / انتداب / مرافقة</p>
        </div>

        <!-- بيانات ناقصة -->
        <div
          @click="activeFilter = activeFilter === 'info' ? '' : 'info'"
          :class="['cursor-pointer rounded-2xl border p-4 transition-all', activeFilter === 'info' ? 'border-yellow-400 ring-2 ring-yellow-200 dark:ring-yellow-800' : 'border-yellow-100 dark:border-yellow-900/40']"
          class="bg-gradient-to-br from-yellow-50 to-amber-100/50 dark:from-yellow-950/30 dark:to-amber-900/20"
        >
          <div class="flex items-center gap-2 mb-3">
            <div class="w-8 h-8 rounded-full bg-yellow-100 dark:bg-yellow-900/50 flex items-center justify-center">
              <svg class="w-4 h-4 text-yellow-600 dark:text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
            <span class="text-xs font-semibold text-yellow-700 dark:text-yellow-400">بيانات ناقصة</span>
          </div>
          <div class="text-3xl font-black text-yellow-700 dark:text-yellow-300">{{ stats.missing_data }}</div>
          <p class="text-xs text-yellow-600/70 dark:text-yellow-400/60 mt-1">المحرك عاجز عن تقييمهم</p>
        </div>

        <!-- الإجمالي -->
        <div class="rounded-2xl border border-brand-100 dark:border-brand-900/40 bg-gradient-to-br from-brand-50 to-brand-100/50 dark:from-brand-950/30 dark:to-brand-900/20 p-4">
          <div class="flex items-center gap-2 mb-3">
            <div class="w-8 h-8 rounded-full bg-brand-100 dark:bg-brand-900/50 flex items-center justify-center">
              <svg class="w-4 h-4 text-brand-600 dark:text-brand-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
            </div>
            <span class="text-xs font-semibold text-brand-700 dark:text-brand-400">إجمالي الإنذارات</span>
          </div>
          <div class="text-3xl font-black text-brand-700 dark:text-brand-300">{{ stats.total }}</div>
          <p class="text-xs text-brand-600/70 dark:text-brand-400/60 mt-1">من الأفراد النشطين</p>
        </div>
      </div>

      <!-- ─── Active Settings Info ───────────────────────────────────── -->
      <div v-if="settings" class="flex flex-wrap gap-3">
        <div class="flex items-center gap-2 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 px-4 py-2.5 text-sm text-gray-600 dark:text-gray-400">
          <svg class="w-4 h-4 text-brand-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/></svg>
          سن التقاعد: <strong class="text-gray-900 dark:text-white">{{ settings.retirement_age }} سنة</strong>
        </div>
        <div class="flex items-center gap-2 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 px-4 py-2.5 text-sm text-gray-600 dark:text-gray-400">
          <svg class="w-4 h-4 text-brand-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
          الحد الأدنى للخدمة: <strong class="text-gray-900 dark:text-white">{{ settings.min_service_years }} سنة</strong>
        </div>
        <div class="flex items-center gap-2 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 px-4 py-2.5 text-sm text-gray-600 dark:text-gray-400">
          <svg class="w-4 h-4 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          نافذة الإنذار: <strong class="text-gray-900 dark:text-white">{{ settings.warning_months }} أشهر</strong>
        </div>
        <div class="flex items-center gap-2 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 px-4 py-2.5 text-sm text-gray-600 dark:text-gray-400">
          <svg class="w-4 h-4 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
          تنبيه الحالات المؤقتة: <strong class="text-gray-900 dark:text-white">{{ settings.temp_warning_days }} يوم</strong>
        </div>
        <router-link to="/settings" class="flex items-center gap-2 rounded-xl bg-brand-50 dark:bg-brand-900/20 border border-brand-200 dark:border-brand-700 px-4 py-2.5 text-sm text-brand-700 dark:text-brand-400 hover:bg-brand-100 dark:hover:bg-brand-900/40 transition-colors">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
          تعديل الإعدادات
        </router-link>
      </div>

      <!-- ─── DataTable ──────────────────────────────────────────────── -->
      <DataTable
        :columns="columns"
        :data="filteredWarnings"
        row-key="military_number"
        :loading="loading"
        :error="error"
        :has-actions="true"
        :has-filters="false"
        :total-count="filteredWarnings.length"
        :total-pages="1"
        :current-page="1"
        search-placeholder="ابحث برقم عسكري أو اسم..."
        empty-title="لا توجد إنذارات"
        empty-description="لم يُعثر على أي إنذارات بناءً على إعدادات النظام الحالية."
        @refresh="runEngine"
        @search="onSearch"
      >
        <!-- urgency badge -->
        <template #cell-urgency="{ value }">
          <span :class="urgencyClass(value)" class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-bold">
            <span class="w-1.5 h-1.5 rounded-full inline-block" :class="urgencyDotClass(value)"></span>
            {{ urgencyLabel(value) }}
          </span>
        </template>

        <!-- warning type -->
        <template #cell-warning_type="{ value }">
          <span class="inline-flex items-center gap-1.5 rounded-md bg-gray-100 dark:bg-gray-800 px-2 py-1 text-xs text-gray-700 dark:text-gray-300">
            {{ warningTypeLabel(value) }}
          </span>
        </template>

        <!-- age -->
        <template #cell-age_years="{ row }">
          <span v-if="row.age_years !== null" class="text-sm text-gray-900 dark:text-white font-medium">
            {{ row.age_years }} سنة <span class="text-gray-400 text-xs">{{ row.age_months > 0 ? `و ${row.age_months} شهر` : '' }}</span>
          </span>
          <span v-else class="text-xs text-yellow-600 dark:text-yellow-400 font-medium">غير محسوب</span>
        </template>

        <!-- service -->
        <template #cell-service_years="{ row }">
          <span v-if="row.service_years !== null" class="text-sm text-gray-900 dark:text-white font-medium">
            {{ row.service_years }} سنة <span class="text-gray-400 text-xs">{{ row.service_months > 0 ? `و ${row.service_months} شهر` : '' }}</span>
          </span>
          <span v-else class="text-xs text-yellow-600 dark:text-yellow-400 font-medium">غير محسوب</span>
        </template>

        <!-- message -->
        <template #cell-message="{ value }">
          <p class="text-sm text-gray-600 dark:text-gray-300 max-w-xs leading-snug">{{ value }}</p>
        </template>

        <!-- Actions -->
        <template #actions="{ row }">
          <router-link
            :to="`/personnel/${row.military_number}`"
            class="flex items-center gap-1.5 rounded-lg bg-brand-50 hover:bg-brand-100 dark:bg-brand-500/10 dark:hover:bg-brand-500/20 border border-brand-200 dark:border-brand-500/30 px-3 py-1.5 text-xs font-bold text-brand-700 dark:text-brand-400 transition-colors"
          >
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
            ملف الفرد
          </router-link>
        </template>
      </DataTable>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import DataTable from '@/components/tables/DataTable.vue'
import api from '@/lib/api'

// ─── State ─────────────────────────────────────────────────────────────────
const loading = ref(false)
const error = ref<string | null>(null)
const warnings = ref<any[]>([])
const stats = ref<any>(null)
const settings = ref<any>(null)
const activeFilter = ref('')
const searchQuery = ref('')

// ─── Columns ────────────────────────────────────────────────────────────────
const columns = [
  { key: 'urgency',        label: 'الخطورة',        minWidth: '120px' },
  { key: 'warning_type',   label: 'نوع الإنذار',    minWidth: '130px' },
  { key: 'military_number',label: 'الرقم العسكري',  minWidth: '100px' },
  { key: 'full_name',      label: 'الاسم الكامل',   minWidth: '160px' },
  { key: 'rank',           label: 'الرتبة',         minWidth: '90px'  },
  { key: 'security_admin', label: 'جهة الأمن',      minWidth: '120px' },
  { key: 'unit',           label: 'الوحدة',         minWidth: '110px' },
  { key: 'age_years',      label: 'العمر الحقيقي',  minWidth: '110px' },
  { key: 'service_years',  label: 'مدة الخدمة',     minWidth: '110px' },
  { key: 'message',        label: 'تفاصيل الإنذار', minWidth: '220px' },
]

// ─── Computed ───────────────────────────────────────────────────────────────
const filteredWarnings = computed(() => {
  let data = warnings.value
  if (activeFilter.value) {
    if (activeFilter.value === 'temp') {
      data = data.filter(w => w.warning_type === 'temp_status_ended' || w.warning_type === 'temp_status_ending_soon')
    } else {
      data = data.filter(w => w.urgency === activeFilter.value)
    }
  }
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    data = data.filter(w =>
      w.military_number?.toLowerCase().includes(q) ||
      w.full_name?.toLowerCase().includes(q) ||
      w.rank?.toLowerCase().includes(q) ||
      w.unit?.toLowerCase().includes(q)
    )
  }
  return data
})

// ─── Urgency Helpers ────────────────────────────────────────────────────────
const urgencyLabel = (v: string) => ({
  exceeded: 'تجاوز السن / المدة',
  critical: 'حرج — أقل من شهر',
  high:     'عالي — أقل من 3 أشهر',
  medium:   'متوسط — أقل من 6 أشهر',
  low:      'منخفض — أقل من سنة',
  info:     'بيانات ناقصة',
}[v] || v)

const urgencyClass = (v: string) => ({
  exceeded: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300',
  critical: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300',
  high:     'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300',
  medium:   'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300',
  low:      'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300',
  info:     'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300',
}[v] || 'bg-gray-100 text-gray-700')

const urgencyDotClass = (v: string) => ({
  exceeded: 'bg-red-500',
  critical: 'bg-red-500 animate-pulse',
  high:     'bg-orange-500',
  medium:   'bg-amber-500',
  low:      'bg-yellow-500',
  info:     'bg-blue-400',
}[v] || 'bg-gray-400')

const warningTypeLabel = (v: string) => ({
  age_exceeded:              '🔴 تجاوز السن',
  age_approaching:           '🕐 اقتراب من التقاعد',
  service_exceeded:          '📅 أكمل مدة الخدمة',
  missing_data:              '⚠️ بيانات ناقصة',
  temp_status_ended:         '🏚️ حالة مؤقتة منتهية',
  temp_status_ending_soon:   '⏳ حالة مؤقتة تنتهي قريباً',
}[v] || v)

// ─── Engine ─────────────────────────────────────────────────────────────────
const runEngine = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await api.get('/personnel/early-warnings/')
    warnings.value = res.data.results || []
    stats.value = res.data.stats || null
    settings.value = res.data.settings || null
  } catch (e: any) {
    error.value = e?.response?.data?.detail || 'فشل في تشغيل محرك الفحص'
  } finally {
    loading.value = false
  }
}

const onSearch = (q: string) => {
  searchQuery.value = q
}

onMounted(() => {
  runEngine()
})
</script>
