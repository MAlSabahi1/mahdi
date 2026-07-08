<template>
  <admin-layout>
    <PageBreadcrumb pageTitle="دليل الخدمات والاستمارات المعتمدة" />

    <div class="space-y-8 text-start animate-fade-in" dir="rtl">

      <!-- Modern Hero Panel -->
      <div
        class="relative overflow-hidden rounded-3xl border border-gray-200 dark:border-gray-800 bg-gradient-to-br from-gray-900 via-gray-950 to-brand-950 p-8 text-white shadow-xl">
        <div
          class="absolute -right-20 -top-20 w-72 h-72 bg-brand-500/10 rounded-full blur-3xl pointer-events-none animate-pulse">
        </div>
        <div class="absolute left-10 bottom-0 w-60 h-60 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none">
        </div>
        <div class="relative flex flex-col md:flex-row justify-between items-start md:items-center gap-6 z-10">
          <div class="flex items-center gap-5">
            <div class="p-4 bg-white/10 backdrop-blur-md text-brand-400 rounded-2xl border border-white/10 shadow-lg">
              <LayoutGrid class="h-8 w-8 stroke-[1.5]" />
            </div>
            <div>
              <span
                class="text-[10px] font-bold tracking-widest text-brand-400 uppercase bg-brand-500/10 px-3 py-1 rounded-full border border-brand-500/20">
                بوابة الخدمات الرسمية
              </span>
              <h1 class="text-2xl font-black text-white mt-2">دليل الخدمات والاستمارات المعتمدة</h1>
              <p class="text-xs text-gray-400 mt-1 max-w-xl leading-relaxed">
                يضم جميع الخدمات والاستمارات والمعاملات المعتمدة رسمياً في النظام، مصنفة حسب النوع مع إمكانية تقديم الطلبات ومتابعتها.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div v-for="stat in stats" :key="stat.label"
          class="relative overflow-hidden bg-white dark:bg-gray-900 p-4 border border-gray-200 dark:border-gray-800 rounded-2xl shadow-sm hover:shadow-md transition-all duration-300 group">
          <div class="relative flex items-center justify-between">
            <div>
              <p class="text-[10px] font-bold text-gray-400 dark:text-gray-500 mb-1 uppercase tracking-wider">{{ stat.label }}</p>
              <p class="text-xl font-black text-gray-900 dark:text-white font-mono leading-none">{{ stat.value }}</p>
            </div>
            <div :class="[stat.colorClass]" class="p-2.5 rounded-xl border transition-all duration-300 group-hover:scale-110">
              <component :is="stat.icon" class="w-5 h-5" />
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs + Search Control Panel -->
      <div
        class="bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border border-gray-200 dark:border-gray-800 rounded-2xl p-4 shadow-sm flex flex-col gap-4 relative z-20">
        <!-- Tabs -->
        <div class="flex flex-wrap gap-2">
          <button v-for="tab in tabs" :key="tab.id" @click="selectedTab = tab.id" :class="[
            selectedTab === tab.id
              ? 'bg-brand-600 text-white shadow-md shadow-brand-500/20 border-brand-500/10'
              : 'bg-gray-50 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-750 border-gray-200/40 dark:border-gray-700/40'
          ]" class="px-4 py-2.5 text-xs font-black rounded-xl transition-all cursor-pointer border flex items-center gap-2">
            <component :is="tab.icon" class="w-3.5 h-3.5" />
            {{ tab.label }}
            <span v-if="tab.count > 0" class="text-[9px] opacity-70">({{ tab.count }})</span>
          </button>
        </div>

        <!-- Search -->
        <div class="relative w-full md:w-96 group">
          <span class="absolute inset-y-0 right-0 flex items-center pr-3.5 pointer-events-none text-gray-400 group-focus-within:text-brand-500 transition-colors">
            <Search class="h-4 w-4" />
          </span>
          <input v-model="searchQuery" type="text" placeholder="البحث بالاسم أو الرقم أو وصف الخدمة..."
            class="w-full text-xs pr-10 pl-4 py-2.5 border border-gray-200 dark:border-gray-800 rounded-xl bg-gray-50/50 dark:bg-gray-850 text-gray-700 dark:text-gray-300 focus:border-brand-500 focus:ring-4 focus:ring-brand-500/10 focus:bg-white dark:focus:bg-gray-900 transition-all outline-none" />
          <button v-if="searchQuery" @click="searchQuery = ''"
            class="absolute inset-y-0 left-0 flex items-center pl-3.5 text-gray-400 hover:text-gray-600">×</button>
        </div>
      </div>

      <!-- Cards Grid -->
      <div class="grid gap-5 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <div v-for="card in filteredCards" :key="card.id"
          class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-sm hover:shadow-xl hover:shadow-brand-500/5 hover:-translate-y-1 transition-all duration-500 ease-out group relative overflow-hidden flex flex-col h-full">
          <!-- Side color bar -->
          <div class="absolute right-0 top-1/2 -translate-y-1/2 w-1.5 h-12 rounded-l-full transition-all duration-500 group-hover:h-20"
            :class="getTypeColor(card.service_type, 'bar')"></div>

          <!-- Hover orb -->
          <div class="absolute -right-10 -bottom-10 w-24 h-24 rounded-full blur-2xl opacity-0 group-hover:opacity-20 transition-opacity duration-500 pointer-events-none"
            :class="getTypeColor(card.service_type, 'orb')"></div>

          <!-- Header -->
          <div class="flex justify-between items-start mb-4 relative z-10">
            <div class="w-12 h-12 rounded-2xl flex items-center justify-center border transition-all duration-300 group-hover:scale-105"
              :class="getTypeColor(card.service_type, 'icon')">
              <component :is="card.icon" class="w-5 h-5 stroke-[1.5]" />
            </div>
            <div class="flex flex-col items-end gap-1.5">
              <!-- Status badge -->
              <span v-if="card.is_locked" class="text-[9px] font-bold px-2 py-0.5 rounded-full bg-red-50 text-red-600 dark:bg-red-950/30 dark:text-red-400 flex items-center gap-1">
                <Lock class="w-2.5 h-2.5" /> مقفلة
              </span>
              <span v-else-if="card.is_active" class="text-[9px] font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-600 dark:bg-emerald-950/30 dark:text-emerald-400 flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span> نشطة
              </span>
              <span v-else class="text-[9px] font-bold px-2 py-0.5 rounded-full bg-gray-100 text-gray-500 dark:bg-gray-800 dark:text-gray-500">غير نشطة</span>
              <!-- Service type label -->
              <span class="text-[9px] font-bold px-2 py-0.5 rounded-full" :class="getTypeColor(card.service_type, 'badge')">
                {{ card.service_type_display }}
              </span>
            </div>
          </div>

          <!-- Body -->
          <div class="flex-1 relative z-10 flex flex-col justify-between">
            <div class="space-y-1.5">
              <h3 class="font-black text-sm text-gray-950 dark:text-white group-hover:text-brand-650 dark:group-hover:text-brand-400 transition-colors duration-300">
                {{ card.title }}
              </h3>
              <p class="text-[11px] text-gray-500 dark:text-gray-400 leading-relaxed line-clamp-2">{{ card.desc }}</p>
            </div>

            <!-- Meta Pills -->
            <div class="flex flex-wrap gap-1.5 mt-4 pt-3 border-t border-gray-100 dark:border-gray-850">
              <!-- Approval type -->
              <div class="flex items-center gap-1 px-2 py-0.5 rounded-lg text-[9px] font-bold"
                :class="card.approval_type === 'external' ? 'bg-amber-50 text-amber-700 dark:bg-amber-950/20 dark:text-amber-400' : card.approval_type === 'internal' ? 'bg-blue-50 text-blue-700 dark:bg-blue-950/20 dark:text-blue-400' : 'bg-gray-50 text-gray-500 dark:bg-gray-800 dark:text-gray-500'">
                <ExternalLink v-if="card.approval_type === 'external'" class="w-2.5 h-2.5" />
                <UserCheck v-else-if="card.approval_type === 'internal'" class="w-2.5 h-2.5" />
                {{ card.approval_type === 'external' ? 'موافقة خارجية' : card.approval_type === 'internal' ? 'موافقة داخلية' : 'بدون موافقة' }}
              </div>
              <!-- Repeatable -->
              <div class="flex items-center gap-1 px-2 py-0.5 rounded-lg bg-gray-50 dark:bg-gray-800/40 text-[9px] text-gray-500 dark:text-gray-400">
                <Repeat v-if="card.is_repeatable" class="w-2.5 h-2.5" />
                <Hash v-else class="w-2.5 h-2.5" />
                {{ card.is_repeatable ? 'متكررة' : 'مرة واحدة' }}
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="mt-4 pt-3 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between relative z-10">
            <!-- My Requests icon -->
            <button v-if="card.form_type" @click="$router.push(`/services/requests?type=${card.form_type}`)"
              class="flex items-center gap-1 text-[10px] text-gray-400 hover:text-brand-600 dark:hover:text-brand-400 transition-colors cursor-pointer" title="طلباتي">
              <ListFilter class="w-3.5 h-3.5" />
              <span>طلباتي</span>
            </button>
            <span v-else></span>

            <!-- Request button -->
            <RouterLink v-if="card.form_type && card.is_active && !card.is_locked" :to="getServiceRoute(card)"
              class="relative overflow-hidden inline-flex items-center gap-1.5 px-4 py-2 text-xs font-black rounded-xl border transition-all duration-300 cursor-pointer"
              :class="getTypeColor(card.service_type, 'btn')">
              <span>طلب الخدمة</span>
              <ArrowLeft class="w-3.5 h-3.5 transition-transform duration-300 group-hover:-translate-x-1" />
            </RouterLink>
            <div v-else-if="card.is_locked"
              class="inline-flex items-center gap-1.5 px-3 py-2 text-[10px] font-bold rounded-xl bg-red-50 text-red-500 border border-red-100 dark:bg-red-950/20 dark:border-red-900 cursor-not-allowed"
              :title="card.lock_reason || 'مقفلة'">
              <Lock class="w-3 h-3" /> مقفلة
            </div>
            <div v-else
              class="inline-flex items-center gap-1.5 px-3 py-2 text-[10px] font-bold rounded-xl bg-gray-50 text-gray-400 border border-gray-200 dark:bg-gray-800 dark:text-gray-500 dark:border-gray-700 cursor-not-allowed">
              قيد التطوير
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredCards.length === 0"
        class="flex flex-col items-center justify-center py-20 text-center border rounded-2xl bg-white dark:bg-gray-900 border-dashed dark:border-gray-800">
        <div class="w-16 h-16 rounded-full bg-brand-500/10 text-brand-600 flex items-center justify-center mb-4">
          <LayoutGrid class="w-8 h-8 opacity-80" />
        </div>
        <h3 class="text-lg font-black mb-2 text-gray-900 dark:text-white">لا توجد خدمات تطابق البحث</h3>
        <p class="text-xs text-gray-400 max-w-sm">جرب تغيير التبويب أو كتابة كلمة أخرى في شريط البحث.</p>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import {
  Search, ArrowLeft, LayoutGrid, ListFilter, Lock,
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

// Tabs matching m.md exactly
const tabs = computed(() => {
  const cards = serviceCards.value
  return [
    { id: 'all', label: 'الكل', icon: LayoutGrid, count: cards.length },
    { id: 'form', label: 'الاستمارات', icon: Layers, count: cards.filter(c => c.service_type === 'form').length },
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

const stats = computed(() => {
  const cards = serviceCards.value
  return [
    { label: 'إجمالي الخدمات', value: cards.length, icon: LayoutGrid, colorClass: 'bg-brand-500/10 text-brand-650 border-brand-500/20 dark:bg-brand-500/5 dark:text-brand-400 dark:border-brand-500/10' },
    { label: 'الاستمارات', value: cards.filter(c => c.service_type === 'form').length, icon: Layers, colorClass: 'bg-blue-500/10 text-blue-600 border-blue-500/20 dark:bg-blue-500/5 dark:text-blue-400 dark:border-blue-500/10' },
    { label: 'تصحيح البيانات', value: cards.filter(c => c.service_type === 'correction').length, icon: FileEdit, colorClass: 'bg-violet-500/10 text-violet-600 border-violet-500/20 dark:bg-violet-500/5 dark:text-violet-400 dark:border-violet-500/10' },
    { label: 'الترقيات', value: cards.filter(c => c.service_type === 'rank_settlement').length, icon: ChevronUp, colorClass: 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20 dark:bg-emerald-500/5 dark:text-emerald-400 dark:border-emerald-500/10' },
    { label: 'الأمان', value: cards.filter(c => c.service_type === 'security').length, icon: ShieldOff, colorClass: 'bg-amber-500/10 text-amber-600 border-amber-500/20 dark:bg-amber-500/5 dark:text-amber-400 dark:border-amber-500/10' },
    { label: 'الجزاءات', value: cards.filter(c => c.service_type === 'disciplinary').length, icon: Gavel, colorClass: 'bg-rose-500/10 text-rose-600 border-rose-500/20 dark:bg-rose-500/5 dark:text-rose-400 dark:border-rose-500/10' },
  ]
})

function getTypeColor(type: string, variant: 'bar' | 'orb' | 'icon' | 'badge' | 'btn') {
  const colors: Record<string, Record<string, string>> = {
    form: {
      bar: 'bg-blue-600 dark:bg-blue-500',
      orb: 'bg-blue-500',
      icon: 'bg-gradient-to-br from-blue-50 to-blue-100/50 border-blue-200/60 text-blue-600 dark:from-blue-950/20 dark:to-blue-900/5 dark:border-blue-900/40 dark:text-blue-400',
      badge: 'bg-blue-50 text-blue-700 dark:bg-blue-950/40 dark:text-blue-300',
      btn: 'bg-blue-500/5 border-blue-500/10 text-blue-600 dark:text-blue-450 hover:bg-blue-600 hover:text-white hover:border-transparent hover:shadow-lg hover:shadow-blue-500/20',
    },
    correction: {
      bar: 'bg-violet-600 dark:bg-violet-500',
      orb: 'bg-violet-500',
      icon: 'bg-gradient-to-br from-violet-50 to-violet-100/50 border-violet-200/60 text-violet-600 dark:from-violet-950/20 dark:to-violet-900/5 dark:border-violet-900/40 dark:text-violet-400',
      badge: 'bg-violet-50 text-violet-700 dark:bg-violet-950/40 dark:text-violet-300',
      btn: 'bg-violet-500/5 border-violet-500/10 text-violet-600 dark:text-violet-450 hover:bg-violet-600 hover:text-white hover:border-transparent hover:shadow-lg hover:shadow-violet-500/20',
    },
    rank_settlement: {
      bar: 'bg-emerald-600 dark:bg-emerald-500',
      orb: 'bg-emerald-500',
      icon: 'bg-gradient-to-br from-emerald-50 to-emerald-100/50 border-emerald-200/60 text-emerald-600 dark:from-emerald-950/20 dark:to-emerald-900/5 dark:border-emerald-900/40 dark:text-emerald-400',
      badge: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300',
      btn: 'bg-emerald-500/5 border-emerald-500/10 text-emerald-600 dark:text-emerald-450 hover:bg-emerald-600 hover:text-white hover:border-transparent hover:shadow-lg hover:shadow-emerald-500/20',
    },
    security: {
      bar: 'bg-amber-600 dark:bg-amber-500',
      orb: 'bg-amber-500',
      icon: 'bg-gradient-to-br from-amber-50 to-amber-100/50 border-amber-200/60 text-amber-600 dark:from-amber-950/20 dark:to-amber-900/5 dark:border-amber-900/40 dark:text-amber-400',
      badge: 'bg-amber-50 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300',
      btn: 'bg-amber-500/5 border-amber-500/10 text-amber-600 dark:text-amber-450 hover:bg-amber-600 hover:text-white hover:border-transparent hover:shadow-lg hover:shadow-amber-500/20',
    },
    disciplinary: {
      bar: 'bg-rose-600 dark:bg-rose-500',
      orb: 'bg-rose-500',
      icon: 'bg-gradient-to-br from-rose-50 to-rose-100/50 border-rose-200/60 text-rose-600 dark:from-rose-950/20 dark:to-rose-900/5 dark:border-rose-900/40 dark:text-rose-400',
      badge: 'bg-rose-50 text-rose-700 dark:bg-rose-950/40 dark:text-rose-300',
      btn: 'bg-rose-500/5 border-rose-500/10 text-rose-600 dark:text-rose-450 hover:bg-rose-600 hover:text-white hover:border-transparent hover:shadow-lg hover:shadow-rose-500/20',
    },
    other: {
      bar: 'bg-gray-500 dark:bg-gray-400',
      orb: 'bg-gray-500',
      icon: 'bg-gradient-to-br from-gray-50 to-gray-100/50 border-gray-200/60 text-gray-600 dark:from-gray-950/20 dark:to-gray-900/5 dark:border-gray-900/40 dark:text-gray-400',
      badge: 'bg-gray-50 text-gray-700 dark:bg-gray-950/40 dark:text-gray-300',
      btn: 'bg-gray-500/5 border-gray-500/10 text-gray-600 dark:text-gray-450 hover:bg-gray-600 hover:text-white hover:border-transparent hover:shadow-lg hover:shadow-gray-500/20',
    },
  }
  return colors[type]?.[variant] || colors.other[variant]
}
</script>
