<template>
  <admin-layout>
    <PageBreadcrumb pageTitle="دليل الخدمات والاستمارات المعتمدة" />

    <div class="space-y-6 text-start pb-20" dir="rtl">
      
      <!-- Premium Page Header -->
      <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-theme-xs">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <div class="p-2.5 bg-brand-50 dark:bg-brand-500/10 rounded-xl text-brand-600 dark:text-brand-400">
              <LayoutGrid class="h-6 w-6 stroke-[1.5]" />
            </div>
            دليل الخدمات والاستمارات المعتمدة
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2 font-medium leading-relaxed">
            المنصة المركزية لإدارة واستعراض كافة الخدمات والاستمارات الرسمية المعتمدة. اختر الخدمة المطلوبة وقدّم الطلب إلكترونياً.
          </p>
        </div>

        <!-- Live Counters -->
        <div class="flex gap-4 flex-shrink-0 flex-wrap">
          <div v-for="stat in headerStats" :key="stat.label" class="rounded-2xl border p-4 shadow-theme-xs text-center min-w-[110px]"
            :class="stat.borderClass">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-full" :class="stat.iconClass">
                <component :is="stat.icon" class="h-5 w-5" />
              </div>
              <div class="text-start">
                <p class="text-xs font-medium" :class="stat.labelClass">{{ stat.label }}</p>
                <h3 class="text-xl font-bold" :class="stat.valueClass">{{ stat.value }}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Control Bar: Tabs & Search -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
        <div class="flex flex-col lg:flex-row gap-4 items-center justify-between p-4">
          <!-- Tabs -->
          <nav class="flex gap-1 overflow-x-auto custom-scrollbar w-full lg:w-auto">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="selectedTab = tab.id"
              :class="[
                selectedTab === tab.id
                  ? 'bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-400 font-bold'
                  : 'text-gray-600 hover:bg-gray-50 dark:text-gray-400 dark:hover:bg-gray-800 font-medium',
                'whitespace-nowrap rounded-lg px-4 py-2.5 text-sm transition-colors flex items-center gap-2'
              ]"
            >
              <component :is="tab.icon" class="w-4 h-4" />
              {{ tab.label }}
              <span v-if="tab.count > 0" class="rounded-md bg-white dark:bg-gray-700 px-1.5 py-0.5 text-[10px] font-bold border border-gray-100 dark:border-gray-600">{{ tab.count }}</span>
            </button>
          </nav>

          <!-- Search -->
          <div class="relative w-full lg:w-80 shrink-0">
            <span class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-gray-400">
              <Search class="h-4 w-4" />
            </span>
            <input v-model="searchQuery" type="text" placeholder="البحث بالاسم أو الوصف..."
              class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border bg-transparent pr-10 pl-8 py-2.5 text-sm shadow-theme-xs placeholder:text-gray-400 focus:outline-hidden focus:ring-3 transition-colors border-gray-300 text-gray-800 focus:border-brand-300 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800" />
            <button v-if="searchQuery" @click="searchQuery = ''"
              class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400 hover:text-gray-600 cursor-pointer">×</button>
          </div>
        </div>
      </div>

      <!-- Clean Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        <div v-for="card in filteredCards" :key="card.id"
          class="group flex flex-col overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-theme-xs transition-all duration-300 ease-out hover:border-gray-300 hover:shadow-theme-sm hover:-translate-y-0.5 dark:border-gray-800 dark:bg-gray-900 dark:hover:border-gray-700 min-h-[250px]">
          
          <!-- Header: Icon & Status -->
          <div class="flex items-start justify-between p-5 pb-0">
            <!-- Icon Box -->
            <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-400 border border-brand-100 dark:border-brand-500/30 transition-transform duration-300 group-hover:scale-110">
              <component :is="card.icon" class="h-6 w-6 stroke-[1.5]" />
            </div>
            
            <!-- Code & Status -->
            <div class="flex flex-col items-end gap-1.5 rtl:text-left text-left">
              <span class="text-[10px] font-mono font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest">{{ card.code }}</span>
              <span v-if="card.is_locked" class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-error-50 text-error-600 border border-error-200 dark:bg-error-500/10 dark:text-error-400 dark:border-error-500/20">
                <Lock class="w-3 h-3" /> مقفلة
              </span>
              <span v-else-if="card.is_active" class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-success-50 text-success-600 border border-success-200 dark:bg-success-500/10 dark:text-success-400 dark:border-success-500/20">
                <span class="h-1.5 w-1.5 rounded-full bg-success-500 animate-pulse"></span> نشطة
              </span>
              <span v-else class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-gray-50 text-gray-500 border border-gray-200 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-700">غير نشطة</span>
            </div>
          </div>

          <!-- Body: Title & Desc -->
          <div class="flex-1 p-5 pt-3 text-start">
            <div class="mb-3 inline-flex items-center rounded-md bg-gray-50 px-2 py-0.5 text-[10px] font-bold text-gray-500 border border-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400">
              {{ card.service_type_display }}
            </div>
            <h3 class="mb-2 text-base font-bold text-gray-900 dark:text-white group-hover:text-brand-600 dark:group-hover:text-brand-400 transition-colors duration-300 leading-snug">{{ card.title }}</h3>
            <p class="text-[13px] text-gray-500 dark:text-gray-400 line-clamp-2 leading-relaxed" :title="card.desc">{{ card.desc }}</p>
          </div>

          <!-- Footer: Meta & Actions -->
          <div class="px-5 pb-5 mt-auto">
            
            <!-- Info Box -->
            <div class="mb-4 space-y-2 rounded-xl bg-gray-50 p-3 text-xs text-gray-600 border border-gray-100 dark:bg-gray-800/50 dark:border-gray-700/50 dark:text-gray-300">
              <div class="flex items-center justify-between">
                <span class="text-gray-500 dark:text-gray-400">آلية الموافقة:</span>
                <span class="font-bold flex items-center gap-1.5 text-gray-700 dark:text-gray-200">
                  <ExternalLink v-if="card.approval_type === 'external'" class="w-3.5 h-3.5 text-amber-500" />
                  <UserCheck v-else-if="card.approval_type === 'internal'" class="w-3.5 h-3.5 text-blue-500" />
                  <CheckCircle v-else class="w-3.5 h-3.5 text-emerald-500" />
                  {{ card.approval_type === 'external' ? 'خارجية' : card.approval_type === 'internal' ? 'داخلية' : 'تلقائية' }}
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-500 dark:text-gray-400">طبيعة الخدمة:</span>
                <span class="font-bold flex items-center gap-1.5 text-gray-700 dark:text-gray-200">
                  <Repeat v-if="card.is_repeatable" class="w-3.5 h-3.5 text-gray-400" />
                  <Hash v-else class="w-3.5 h-3.5 text-gray-400" />
                  {{ card.is_repeatable ? 'متكررة' : 'مرة واحدة' }}
                </span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center gap-2">
              <button
                v-if="card.form_type"
                @click="$router.push(`/services/transactions?tab=internal&type=${card.form_type}`)"
                class="flex items-center justify-center h-10 w-12 shrink-0 rounded-xl border border-gray-200 bg-white text-gray-500 hover:bg-gray-50 hover:text-brand-600 hover:border-brand-200 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 transition-all duration-300"
                title="سجل الطلبات"
              >
                <ListFilter class="h-4 w-4" />
              </button>

              <RouterLink
                v-if="card.form_type && card.is_active && !card.is_locked"
                :to="getServiceRoute(card)"
                class="flex flex-1 items-center justify-center gap-2 h-10 rounded-xl bg-brand-600 px-4 text-sm font-bold text-white hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 transition-all duration-300 shadow-sm shadow-brand-500/20"
              >
                طلب الخدمة
              </RouterLink>
              
              <button
                v-else-if="card.is_locked"
                disabled
                class="flex flex-1 items-center justify-center gap-2 h-10 rounded-xl bg-error-50 text-sm font-bold text-error-500 border border-error-100 dark:bg-error-500/10 dark:border-error-500/20 dark:text-error-400 cursor-not-allowed"
              >
                <Lock class="h-4 w-4" /> مقفلة
              </button>
              
              <button
                v-else
                disabled
                class="flex flex-1 items-center justify-center gap-2 h-10 rounded-xl bg-gray-50 border border-gray-200 text-sm font-bold text-gray-400 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-500 cursor-not-allowed"
              >
                قيد التطوير
              </button>
            </div>
          </div>
          
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredCards.length === 0" class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
        <div class="flex flex-col items-center justify-center py-20 text-center">
          <div class="flex h-16 w-16 items-center justify-center rounded-2xl bg-gray-100 dark:bg-gray-800 text-gray-400 dark:text-gray-500 mb-4">
            <LayoutGrid class="h-8 w-8" />
          </div>
          <h3 class="text-sm font-bold text-gray-600 dark:text-gray-300 mb-1">لا توجد نتائج مطابقة</h3>
          <p class="text-xs text-gray-400 dark:text-gray-500 max-w-xs">لم نتمكن من العثور على أي خدمات تطابق بحثك الحالي.</p>
        </div>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import {
  Search, LayoutGrid, ListFilter, Lock, CheckCircle,
  UserCheck, ExternalLink, Repeat, Hash,
  // Service icons
  Award, TrendingUp, LogOut, PauseCircle, MapPin, Percent, Activity,
  HeartHandshake, Binary, GraduationCap, CalendarCheck, History, ShieldCheck,
  Briefcase, Reply, Globe, FileText, FileX, UserPlus, ShieldAlert, AlertTriangle,
  AlertOctagon, Download, GitCompare, UserX, Users, ArrowDown,
  // Tab icons
  Layers, FileEdit, ChevronUp, ShieldOff, Gavel
} from 'lucide-vue-next'
import { useServicesStore } from '@/stores/services'

const servicesStore = useServicesStore()

const iconMap: any = {
  Award, TrendingUp, LogOut, PauseCircle, MapPin, Percent, Activity,
  HeartHandshake, Binary, GraduationCap, CalendarCheck, History, ShieldCheck,
  Briefcase, Reply, Globe, FileText, FileX, UserPlus, ShieldAlert, AlertTriangle,
  AlertOctagon, ExternalLink, Download, GitCompare, Lock, UserX, Users, ArrowDown
}

const selectedTab = ref('all')
const searchQuery = ref('')

interface ServiceCard {
  id: number
  code: string
  title: string
  desc: string
  category: string
  service_type: string
  service_type_display: string
  approval_type: string
  approval_type_display: string
  is_active: boolean
  is_repeatable: boolean
  is_locked: boolean
  lock_reason: string
  icon: any
  form_type: string | null
}

const serviceCards = ref<ServiceCard[]>([])

onMounted(async () => {
  try {
    const data = await servicesStore.fetchServiceCatalog()
    serviceCards.value = data.map((item: any) => ({
      id: item.id,
      code: item.code,
      title: item.name_ar,
      desc: item.description,
      category: item.category,
      service_type: item.service_type || 'other',
      service_type_display: item.service_type_display || getServiceTypeLabel(item.service_type),
      approval_type: item.approval_type || 'internal',
      approval_type_display: item.approval_type_display || '',
      is_active: item.is_active !== false,
      is_repeatable: item.is_repeatable !== false,
      is_locked: item.is_locked || false,
      lock_reason: item.lock_reason || '',
      icon: iconMap[item.icon] || Award,
      form_type: item.form_type
    }))
  } catch (e) {
    console.error('Failed to load catalog', e)
  }
})

function getServiceTypeLabel(t: string) {
  const map: Record<string, string> = {
    form: 'استمارة', correction: 'تصحيح بيانات', rank_settlement: 'ترقية / تسوية',
    disciplinary: 'جزاء تأديبي', security: 'أمان ومزامنة', other: 'أخرى'
  }
  return map[t] || 'أخرى'
}

function getServiceRoute(card: ServiceCard) {
  if (card.service_type === 'correction') return `/services/request/correction?type=${card.form_type}&category=${card.service_type}`
  if (card.service_type === 'rank_settlement') return `/services/request/rank-settlement?type=${card.form_type}&category=${card.service_type}`
  return `/services/request?type=${card.form_type}&category=${card.service_type}`
}

// Tabs matching logic
const tabs = computed(() => {
  const cards = serviceCards.value
  return [
    { id: 'all', label: 'كافة الخدمات', icon: LayoutGrid, count: cards.length },
    { id: 'form', label: 'الاستمارات الرسمية', icon: Layers, count: cards.filter(c => c.service_type === 'form').length },
    { id: 'correction', label: 'تصحيح البيانات', icon: FileEdit, count: cards.filter(c => c.service_type === 'correction').length },
    { id: 'rank_settlement', label: 'الترقيات والتسويات', icon: ChevronUp, count: cards.filter(c => c.service_type === 'rank_settlement').length },
    { id: 'security', label: 'المزامنة والأمان', icon: ShieldOff, count: cards.filter(c => c.service_type === 'security').length },
    { id: 'disciplinary', label: 'الجزاءات والانضباط', icon: Gavel, count: cards.filter(c => c.service_type === 'disciplinary').length },
  ]
})

const filteredCards = computed(() => {
  return serviceCards.value.filter(card => {
    const matchesTab = selectedTab.value === 'all' || card.service_type === selectedTab.value
    const matchesQuery = !searchQuery.value ||
      card.title.includes(searchQuery.value) ||
      card.desc.includes(searchQuery.value) ||
      card.code.includes(searchQuery.value)
    return matchesTab && matchesQuery
  })
})

const headerStats = computed(() => {
  const cards = serviceCards.value
  return [
    {
      label: 'إجمالي الخدمات', value: cards.length, icon: LayoutGrid,
      borderClass: 'border-blue-200 bg-blue-50 dark:border-blue-500/20 dark:bg-blue-500/5',
      iconClass: 'bg-blue-100 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400',
      labelClass: 'text-blue-700 dark:text-blue-400',
      valueClass: 'text-blue-900 dark:text-blue-300',
    },
    {
      label: 'خدمات نشطة', value: cards.filter(c => c.is_active && !c.is_locked).length, icon: CheckCircle,
      borderClass: 'border-success-200 bg-success-50 dark:border-success-500/20 dark:bg-success-500/5',
      iconClass: 'bg-success-100 text-success-600 dark:bg-success-500/20 dark:text-success-400',
      labelClass: 'text-success-700 dark:text-success-400',
      valueClass: 'text-success-900 dark:text-success-300',
    },
    {
      label: 'مقفلة حالياً', value: cards.filter(c => c.is_locked).length, icon: Lock,
      borderClass: 'border-error-200 bg-error-50 dark:border-error-500/20 dark:bg-error-500/5',
      iconClass: 'bg-error-100 text-error-600 dark:bg-error-500/20 dark:text-error-400',
      labelClass: 'text-error-700 dark:text-error-400',
      valueClass: 'text-error-900 dark:text-error-300',
    },
  ]
})
</script>
