<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="دليل الأفراد والضباط الرئيسي (Personnel Master Directory Grid)" />

    <div class="space-y-4 text-start" dir="rtl">
      
      <!-- Top Action Bar -->
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 bg-white dark:bg-white/[0.03] p-4 rounded-xl border border-gray-200 dark:border-gray-800">
        <!-- Smart Search Shortcut Indicator -->
        <div class="flex items-center gap-2">
          <button
            @click="searchOpen = true"
            class="flex items-center gap-2 px-3 py-1.5 text-xs text-gray-500 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg hover:bg-gray-100 transition-colors w-64 shadow-theme-xs cursor-pointer"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <span class="flex-1 text-right">البحث الشامل في السجل...</span>
            <kbd class="inline-flex items-center gap-0.5 px-1.5 font-mono text-[9px] text-gray-400 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded shadow-theme-xs">
              ⌘F
            </kbd>
          </button>
        </div>

        <div class="flex items-center gap-2 w-full sm:w-auto justify-end">
          <button
            @click="exportData"
            class="flex items-center gap-2 rounded-lg border border-gray-200 bg-white px-3.5 py-1.5 text-xs font-bold text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-300 dark:hover:bg-gray-800 transition-colors cursor-pointer"
          >
            <svg class="h-4 w-4 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            تصدير الكشف (CSV)
          </button>
          
          <button
            @click="showFilters = !showFilters"
            class="flex items-center gap-2 rounded-lg border px-3.5 py-1.5 text-xs font-bold transition-colors cursor-pointer"
            :class="showFilters || hasActiveFilters ? 'border-brand-500 bg-brand-50 text-brand-700 dark:bg-brand-500/10 dark:text-brand-400' : 'border-gray-200 bg-white text-gray-700 hover:bg-gray-50 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-300 dark:hover:bg-gray-800'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            تصفية متقدمة
          </button>

          <RouterLink
            to="/personnel/create"
            class="flex items-center gap-1.5 rounded-lg bg-brand-600 px-3.5 py-1.5 text-xs font-bold text-white shadow-theme-xs hover:bg-brand-700 transition-colors cursor-pointer"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
            </svg>
            إضافة منتسب جديد
          </RouterLink>
        </div>
      </div>

      <!-- Advanced Filters Collapsible -->
      <div v-show="showFilters" class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-xl p-4 shadow-theme-xs">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="mb-1.5 block text-xs font-bold text-gray-500 dark:text-gray-400">الرتبة العسكرية</label>
            <select v-model="filters.current_rank" class="block w-full rounded-lg border border-gray-200 bg-white p-2 text-xs text-gray-900 focus:border-brand-500 dark:border-gray-800 dark:bg-gray-900 dark:text-white">
              <option :value="null">الكل</option>
              <option v-for="r in coreStore.ranks" :key="r.id" :value="r.id">{{ r.name }}</option>
            </select>
          </div>
          <div>
            <label class="mb-1.5 block text-xs font-bold text-gray-500 dark:text-gray-400">تصنيف الحالة الوظيفية</label>
            <select v-model="filters.current_status" class="block w-full rounded-lg border border-gray-200 bg-white p-2 text-xs text-gray-900 focus:border-brand-500 dark:border-gray-800 dark:bg-gray-900 dark:text-white">
              <option :value="null">الكل</option>
              <option v-for="s in coreStore.statuses" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
          <div>
            <label class="mb-1.5 block text-xs font-bold text-gray-500 dark:text-gray-400">المحافظة / النطاق الجغرافي</label>
            <select v-model="filters.governorate" class="block w-full rounded-lg border border-gray-200 bg-white p-2 text-xs text-gray-900 focus:border-brand-500 dark:border-gray-800 dark:bg-gray-900 dark:text-white">
              <option :value="null">الكل</option>
              <option v-for="g in coreStore.governorates" :key="g.id" :value="g.id">{{ g.name }}</option>
            </select>
          </div>
        </div>
        <div class="mt-4 flex justify-end gap-3 border-t border-gray-150 dark:border-gray-800 pt-3">
          <button @click="clearFilters" class="text-xs text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 cursor-pointer">إلغاء الفرز</button>
          <button @click="loadPersonnel(1)" class="rounded-lg bg-brand-600 px-4 py-1.5 text-xs font-bold text-white shadow-theme-xs hover:bg-brand-700 transition-colors cursor-pointer">تطبيق الفرز</button>
        </div>
      </div>

      <!-- Excel-like Spreadsheet DataGrid -->
      <div class="relative bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-xl shadow-theme-xs overflow-hidden">
        
        <!-- Loading overlay -->
        <div v-if="personnelStore.loading && personnelStore.records.length === 0" class="flex justify-center items-center py-16">
          <svg class="h-7 w-7 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          <span class="mr-2 text-xs font-bold text-gray-500">جاري تحميل السجل الموحد...</span>
        </div>

        <div v-else-if="personnelStore.error" class="p-8 text-center text-xs font-bold text-red-500">
          {{ personnelStore.error }}
        </div>

        <div v-else-if="personnelStore.records.length === 0" class="flex flex-col items-center justify-center py-16 px-4">
          <div class="mb-4 rounded-full bg-gray-50 dark:bg-gray-900 p-4 shadow-theme-xs border border-gray-100 dark:border-gray-800">
            <svg class="h-10 w-10 text-gray-400 dark:text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v16m8-8H4" />
            </svg>
          </div>
          <h3 class="text-sm font-black text-gray-900 dark:text-white">السجل فارغ تماماً</h3>
          <p class="mt-1 text-xs text-gray-500 dark:text-gray-400 text-center max-w-sm">لم يتم العثور على أفراد يطابقون معايير البحث الحالية.</p>
        </div>

        <!-- Excel Table Grid Container -->
        <div v-else class="overflow-x-auto w-full">
          <table class="w-full text-right border-collapse table-fixed text-[11px] font-medium min-w-[1400px]">
            
            <!-- Excel Header Groupings -->
            <thead>
              <tr class="bg-gray-100 dark:bg-gray-950 text-gray-600 dark:text-gray-400 border-b border-gray-250 dark:border-gray-800">
                <!-- Pinned Column space (right pin in RTL) -->
                <th class="sticky right-0 z-20 bg-gray-100 dark:bg-gray-950 border-l border-gray-250 dark:border-gray-800 px-3 py-1.5 w-[110px] text-center font-bold">العمليات</th>
                
                <th colspan="4" class="border-l border-gray-250 dark:border-gray-800 text-center font-bold px-3 py-1.5 bg-gray-150/70 dark:bg-gray-900/60">البيانات الأساسية للمنتسب</th>
                <th colspan="5" class="border-l border-gray-250 dark:border-gray-800 text-center font-bold px-3 py-1.5 bg-gray-100 dark:bg-gray-950/70">الرتبة والوحدة والتنظيم</th>
                <th colspan="3" class="border-l border-gray-250 dark:border-gray-800 text-center font-bold px-3 py-1.5 bg-gray-150/70 dark:bg-gray-900/60">الحالة الوظيفية والتعليمية</th>
                <th colspan="2" class="text-center font-bold px-3 py-1.5 bg-gray-100 dark:bg-gray-950/70">جودة وتاريخ السجل</th>
              </tr>
              
              <!-- Column Fields -->
              <tr class="bg-gray-50 dark:bg-gray-900/40 text-gray-500 dark:text-gray-400 border-b border-gray-250 dark:border-gray-800 text-[10px]">
                <!-- Pinned Actions header cell -->
                <th class="sticky right-0 z-20 bg-gray-50 dark:bg-gray-900/80 border-l border-gray-250 dark:border-gray-800 px-3 py-2 w-[110px] text-center">تعديل وملف</th>
                
                <!-- Basic Info -->
                <th class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 w-[160px]">الاسم الكامل</th>
                <th class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 w-[90px]">الرقم العسكري</th>
                <th class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 w-[110px]">الرقم الوطني</th>
                <th class="border-l border-gray-250 dark:border-gray-800 px-3 py-2 w-[100px]">رقم الهاتف</th>

                <!-- Rank & Unit -->
                <th class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 w-[90px]">الرتبة الحالية</th>
                <th class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 w-[110px]">الرتبة القادمة</th>
                <th class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 w-[140px]">المنصب / المسمى</th>
                <th class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 w-[130px]">الإدارة / المديرية</th>
                <th class="border-l border-gray-250 dark:border-gray-800 px-3 py-2 w-[120px]">القسم / الفرع</th>

                <!-- Status & Qualification -->
                <th class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 w-[95px]">تصنيف الحالة</th>
                <th class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 w-[100px]">نوع الحالة</th>
                <th class="border-l border-gray-250 dark:border-gray-800 px-3 py-2 w-[90px]">المؤهل العلمي</th>

                <!-- Quality & Date -->
                <th class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 w-[90px]">جودة السجل %</th>
                <th class="px-3 py-2 w-[100px]">تاريخ الالتحاق</th>
              </tr>
            </thead>

            <!-- Excel Cells Grid -->
            <tbody class="divide-y divide-gray-200 dark:divide-gray-800">
              <tr 
                v-for="person in personnelStore.records" 
                :key="person.military_number"
                class="hover:bg-brand-50/20 dark:hover:bg-brand-500/5 transition-colors group"
              >
                <!-- Pinned Action Column (RTL sticky right) -->
                <td class="sticky right-0 z-10 bg-white dark:bg-[#1a1a1a] border-l border-gray-250 dark:border-gray-800 px-2 py-1.5 w-[110px] text-center flex items-center justify-center gap-1.5 h-full">
                  <RouterLink
                    :to="`/personnel/${person.military_number}`"
                    class="p-1 rounded bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 text-gray-500 hover:text-brand-600 hover:bg-brand-50 transition-all cursor-pointer"
                    title="الملف"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                      <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                    </svg>
                  </RouterLink>
                  <RouterLink
                    :to="`/personnel/${person.military_number}/edit`"
                    class="p-1 rounded bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 text-gray-500 hover:text-blue-600 hover:bg-blue-50 transition-all cursor-pointer"
                    title="تعديل"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                    </svg>
                  </RouterLink>
                </td>

                <!-- Basic Info Cells -->
                <td class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 text-gray-900 dark:text-gray-100 font-bold truncate">
                  {{ person.full_name }}
                </td>
                <td class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 font-mono text-[10px] text-gray-500 dark:text-gray-400">
                  {{ person.military_number }}
                </td>
                <td class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 font-mono text-[10px] text-gray-500 dark:text-gray-400">
                  {{ person.national_id || '-' }}
                </td>
                <td class="border-l border-gray-250 dark:border-gray-800 px-3 py-2 font-mono text-[10px] text-gray-500 dark:text-gray-400">
                  {{ person.phone_number || '-' }}
                </td>

                <!-- Rank & Unit Cells -->
                <td class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 text-gray-700 dark:text-gray-300">
                  {{ person.rank_name || 'بدون رتبة' }}
                </td>
                <td class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 text-warning-600 dark:text-warning-400 font-semibold">
                  {{ person.pending_rank_name || '-' }}
                </td>
                <td class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 text-gray-700 dark:text-gray-300 truncate">
                  {{ person.position_name || 'بدون منصب' }}
                </td>
                <td class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 text-gray-700 dark:text-gray-300 truncate">
                  {{ person.security_admin_name || '-' }}
                </td>
                <td class="border-l border-gray-250 dark:border-gray-800 px-3 py-2 text-gray-700 dark:text-gray-300 truncate">
                  {{ person.branch_name || '-' }}
                </td>

                <!-- Status Cells -->
                <td class="border-l border-gray-200 dark:border-gray-800 px-2 py-1.5">
                  <span
                    class="inline-flex items-center gap-1 rounded px-2 py-0.5 text-[9px] font-bold"
                    :class="getStatusColor(person.status_classification)"
                  >
                    <span class="h-1.5 w-1.5 rounded-full" :class="getStatusDotColor(person.status_classification)"></span>
                    {{ person.status_classification === 'active' ? 'موجود' : 'غير موجود' }}
                  </span>
                </td>
                <td class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 text-gray-500 dark:text-gray-400 truncate">
                  {{ person.status_name || '-' }}
                </td>
                <td class="border-l border-gray-250 dark:border-gray-800 px-3 py-2 text-gray-500 dark:text-gray-400 truncate">
                  {{ person.qualification_name || '-' }}
                </td>

                <!-- Quality & Date Cells -->
                <td class="border-l border-gray-200 dark:border-gray-800 px-3 py-2 font-bold" :class="getQualityScoreTextColor(person.data_quality_score)">
                  {{ person.data_quality_score }}%
                </td>
                <td class="px-3 py-2 font-mono text-[10px] text-gray-500 dark:text-gray-400">
                  {{ person.join_date || '-' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Excel Grid Footer & Pagination -->
        <div v-if="!personnelStore.loading && personnelStore.records.length > 0" class="border-t border-gray-200 dark:border-gray-800 px-4 py-3 bg-gray-50 dark:bg-gray-950/20 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 text-xs font-bold text-gray-500">
          <p class="text-center sm:text-right">
            الصفحة <span class="text-gray-900 dark:text-white">{{ personnelStore.currentPage }}</span> من <span class="text-gray-900 dark:text-white">{{ personnelStore.totalPages }}</span>
            (إجمالي: {{ personnelStore.totalCount }} منتسب)
          </p>
          <div class="flex justify-center gap-1.5">
            <button
              :disabled="personnelStore.currentPage <= 1"
              @click="goToPage(personnelStore.currentPage - 1)"
              class="px-2.5 py-1 rounded border border-gray-200 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-800 dark:bg-gray-900 dark:text-gray-300 dark:hover:bg-gray-800 transition-colors cursor-pointer"
            >
              السابق
            </button>
            <button
              :disabled="personnelStore.currentPage >= personnelStore.totalPages"
              @click="goToPage(personnelStore.currentPage + 1)"
              class="px-2.5 py-1 rounded border border-gray-200 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-800 dark:bg-gray-900 dark:text-gray-300 dark:hover:bg-gray-800 transition-colors cursor-pointer"
            >
              التالي
            </button>
          </div>
        </div>
      </div>

    </div>

    <!-- Smart Search Overlay Drawer (⌘F Drawer) -->
    <div v-if="searchOpen" class="fixed inset-0 z-50 overflow-hidden flex items-start justify-center pt-24" role="dialog" aria-modal="true">
      <!-- Backdrop -->
      <div class="fixed inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity" @click="searchOpen = false"></div>

      <!-- Drawer Content -->
      <div class="relative bg-white dark:bg-gray-900 rounded-2xl max-w-2xl w-full mx-4 overflow-hidden border border-gray-200 dark:border-gray-800 shadow-2xl transition-all">
        <!-- Input section -->
        <div class="p-4 border-b border-gray-200 dark:border-gray-800 flex items-center gap-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            v-model="smartSearchQuery"
            @input="handleSmartSearch"
            type="text"
            placeholder="ابحث بالاسم، الرقم العسكري، أو الرقم الوطني..."
            class="w-full text-sm bg-transparent border-0 outline-none text-gray-900 dark:text-white placeholder-gray-400"
            ref="smartSearchInput"
          />
          <button @click="searchOpen = false" class="text-xs text-gray-400 hover:text-gray-600 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded-lg cursor-pointer">
            إغلاق (Esc)
          </button>
        </div>

        <!-- Results section -->
        <div class="max-h-96 overflow-y-auto divide-y divide-gray-150 dark:divide-gray-850">
          <div v-if="smartSearchResults.length === 0" class="p-8 text-center text-xs text-gray-400">
            {{ smartSearchQuery ? 'لا توجد نتائج مطابقة' : 'اكتب للبحث في قاعدة البيانات الموحدة...' }}
          </div>
          
          <div
            v-for="res in smartSearchResults"
            :key="res.military_number"
            class="p-4 hover:bg-gray-50 dark:hover:bg-gray-950 flex items-center justify-between cursor-pointer"
            @click="selectSearchResult(res)"
          >
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-full bg-brand-50 dark:bg-brand-950/40 text-brand-600 dark:text-brand-400 flex items-center justify-center font-bold text-xs shrink-0">
                {{ res.rank_name ? res.rank_name[0] : 'ف' }}
              </div>
              <div class="text-right">
                <h4 class="text-xs font-bold text-gray-900 dark:text-white">{{ res.full_name }}</h4>
                <p class="text-[10px] text-gray-400 mt-0.5">{{ res.rank_name || 'بدون رتبة' }} • الرقم العسكري: {{ res.military_number }}</p>
              </div>
            </div>
            
            <div class="text-left">
              <span class="text-[10px] font-mono text-gray-400 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded">
                {{ res.security_admin_name || 'غير محدد' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch, onUnmounted, nextTick } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { usePersonnelStore } from '@/stores/personnel'
import { useCoreStore } from '@/stores/core'
import Swal from 'sweetalert2'
import api from '@/lib/api'

const personnelStore = usePersonnelStore()
const coreStore = useCoreStore()

const showFilters = ref(false)
const searchOpen = ref(false)
const smartSearchQuery = ref('')
const smartSearchResults = ref<any[]>([])
const smartSearchInput = ref<HTMLInputElement | null>(null)

const filters = ref({
  current_rank: null as number | string | null,
  current_status: null as number | string | null,
  governorate: null as number | string | null
})

const hasActiveFilters = computed(() => {
  return filters.value.current_rank !== null || 
         filters.value.current_status !== null || 
         filters.value.governorate !== null
})

function clearFilters() {
  filters.value = { current_rank: null, current_status: null, governorate: null }
  loadPersonnel(1)
}

function loadPersonnel(page = 1) {
  personnelStore.fetchPersonnel({
    current_rank: filters.value.current_rank || undefined,
    current_status: filters.value.current_status || undefined,
    governorate: filters.value.governorate || undefined,
    page
  })
}

function goToPage(page: number) {
  if (page >= 1 && page <= personnelStore.totalPages) {
    loadPersonnel(page)
  }
}

// Global search handling
let searchTimer: any = null
function handleSmartSearch() {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(async () => {
    if (!smartSearchQuery.value) {
      smartSearchResults.value = []
      return
    }
    try {
      const res = await api.get('/personnel/', {
        params: { search: smartSearchQuery.value, page_size: 20 }
      })
      smartSearchResults.value = res.data.results || []
    } catch (err) {
      console.error('Fuzzy smart search failed:', err)
    }
  }, 300)
}

function selectSearchResult(person: any) {
  searchOpen.value = false
  smartSearchQuery.value = ''
  smartSearchResults.value = []
  
  // Directly fetch the specific records matching or display details
  Swal.fire({
    title: person.full_name,
    html: `
      <div class="text-right text-xs space-y-2" dir="rtl">
        <div><strong>الرقم العسكري:</strong> ${person.military_number}</div>
        <div><strong>الرقم الوطني:</strong> ${person.national_number || '-'}</div>
        <div><strong>الرتبة:</strong> ${person.rank_name || 'بدون رتبة'}</div>
        <div><strong>الإدارة:</strong> ${person.security_admin_name || '-'}</div>
        <div><strong>الحالة:</strong> ${person.status_name || '-'}</div>
        <div><strong>جودة البيانات:</strong> ${person.data_quality_score}%</div>
      </div>
    `,
    showCancelButton: true,
    confirmButtonText: 'عرض الملف الكامل',
    cancelButtonText: 'إغلاق',
    confirmButtonColor: '#3b82f6',
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.href = `/personnel/${person.military_number}`
    }
  })
}

// Global Hotkeys binding
function handleKeydown(e: KeyboardEvent) {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'f') {
    e.preventDefault()
    searchOpen.value = true
    nextTick(() => {
      smartSearchInput.value?.focus()
    })
  } else if (e.key === 'Escape') {
    searchOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
  if (coreStore.ranks.length === 0) {
    coreStore.fetchAllReferences()
  }
  loadPersonnel()
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})

async function exportData() {
  try {
    const params: any = {}
    if (filters.value.current_rank) params.current_rank = filters.value.current_rank
    if (filters.value.current_status) params.current_status = filters.value.current_status
    if (filters.value.governorate) params.governorate = filters.value.governorate
    
    const response = await api.get('/personnel/export_csv/', {
      params,
      responseType: 'blob'
    })
    
    const blob = new Blob([response.data], { type: 'text/csv;charset=utf-8;' })
    const downloadUrl = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = downloadUrl
    a.download = 'personnel.csv'
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(downloadUrl)
    document.body.removeChild(a)
    
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم التصدير بنجاح', showConfirmButton: false, timer: 2500 })
  } catch (err) {
    console.error('Failed to export:', err)
  }
}

function getStatusColor(classification: string | null) {
  switch (classification) {
    case 'active': return 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400'
    default: return 'bg-red-50 text-red-700 dark:bg-red-500/10 dark:text-red-400'
  }
}

function getStatusDotColor(classification: string | null) {
  switch (classification) {
    case 'active': return 'bg-emerald-500'
    default: return 'bg-red-500'
  }
}

function getQualityScoreTextColor(score: number) {
  if (score >= 80) return 'text-emerald-600 dark:text-emerald-400'
  if (score >= 50) return 'text-amber-600 dark:text-amber-400'
  return 'text-red-600 dark:text-red-400'
}
</script>
