<template>
  <admin-layout>
    <div class="space-y-6 print:space-y-0 print:m-0 print:p-0">
      <!-- Toolbar & Page Header -->
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 print:hidden">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-slate-100 dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700">
            <svg class="h-8 w-8 text-slate-700 dark:text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div>
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white">تصدير الخدمات والكشوفات الشهرية</h2>
            <p class="text-sm font-medium text-slate-500 dark:text-slate-400 mt-1">تصدير كشوفات الإجراءات والخدمات الشهرية وتحديد الأعمدة المراد عرضها</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button @click="printReport" class="flex items-center gap-2 rounded-lg bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors focus:outline-none print:hidden">
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" /></svg>
            طباعة الكشف
          </button>
          <button @click="$router.push('/reports')" class="flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm hover:bg-slate-50 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700 transition-all focus:outline-none print:hidden">
            <svg class="h-4.5 w-4.5 rtl:rotate-180" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            عودة للوحة التقارير
          </button>
        </div>
      </div>

      <!-- Monthly Exports Dashboard -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 print:hidden">
        
        <!-- Card 1: Official Excel -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden relative p-6 flex flex-col justify-between hover:shadow-md transition-shadow">
          <!-- Top Accent Line -->
          <div class="absolute top-0 right-0 left-0 h-1 bg-brand-600"></div>
          
          <div>
            <div class="flex items-start gap-4 mb-4">
              <div class="flex-shrink-0 flex items-center justify-center w-12 h-12 rounded-xl bg-brand-50 dark:bg-brand-900/30 text-brand-600 dark:text-brand-400">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-bold text-gray-900 dark:text-white">الكشف الموحد (Excel)</h3>
                <p class="text-gray-500 dark:text-gray-400 text-sm mt-1 leading-relaxed">
                  تصدير الكشف الشهري الرسمي المكون من 4 أوراق (قوة عاملة، غير عاملة، كاملة، غياب).
                </p>
              </div>
            </div>
          </div>
          
          <div class="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700 space-y-3">
            <div>
              <label class="block text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1.5">نطاق التصدير</label>
              <select v-model="officialExportDirectorate" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm text-gray-900 dark:text-white focus:border-brand-500 focus:ring-brand-500 shadow-sm transition-colors cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-600">
                <option value="">جميع الإدارات (كشف واحد)</option>
                <option v-for="dept in coreStore.centralDepartments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1.5">شهر التصدير</label>
              <input type="month" v-model="officialExportMonth" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm text-gray-900 dark:text-white focus:border-brand-500 focus:ring-brand-500 shadow-sm transition-colors cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-600" />
            </div>
            <button @click="handleOfficialExport" :disabled="servicesStore.loading || !officialExportMonth" class="mt-4 w-full flex items-center justify-center gap-2 rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-bold text-white shadow-sm hover:bg-brand-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
              <svg v-if="servicesStore.loading" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
              <svg v-else class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
              تصدير الإكسل الرسمي
            </button>
          </div>
        </div>

        <!-- Card 2: PDFs and Attachments -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden relative p-6 flex flex-col justify-between hover:shadow-md transition-shadow">
          <!-- Top Accent Line -->
          <div class="absolute top-0 right-0 left-0 h-1 bg-amber-500"></div>
          
          <div>
            <div class="flex items-start gap-4 mb-4">
              <div class="flex-shrink-0 flex items-center justify-center w-12 h-12 rounded-xl bg-amber-50 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-bold text-gray-900 dark:text-white">السجلات والمرفقات (PDF)</h3>
                <p class="text-gray-500 dark:text-gray-400 text-sm mt-1 leading-relaxed">
                  تصدير قرارات الإجراءات مع دمج كافة الوثائق والمرفقات الخاصة بكل فرد في ملف موحد.
                </p>
              </div>
            </div>
          </div>
          
          <div class="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700 space-y-2.5">
            <button @click="handlePdfExport('corrections')" :disabled="servicesStore.loading || !officialExportMonth" class="w-full flex items-center justify-between gap-3 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 px-4 py-3 text-sm font-bold text-gray-700 dark:text-gray-200 shadow-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed group">
              <span class="flex items-center gap-2">
                <div class="w-1.5 h-1.5 rounded-full bg-amber-500"></div>
                كشوفات التصحيح مع المرفقات
              </span>
              <svg class="h-4 w-4 text-gray-400 group-hover:text-amber-500 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
            </button>
            <button @click="handlePdfExport('all')" :disabled="servicesStore.loading || !officialExportMonth" class="w-full flex items-center justify-between gap-3 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 px-4 py-3 text-sm font-bold text-gray-700 dark:text-gray-200 shadow-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed group">
              <span class="flex items-center gap-2">
                <div class="w-1.5 h-1.5 rounded-full bg-amber-500"></div>
                كل الإجراءات مع المرفقات
              </span>
              <svg class="h-4 w-4 text-gray-400 group-hover:text-amber-500 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
            </button>
          </div>
        </div>

        <!-- Card 3: Summaries -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden relative p-6 flex flex-col justify-between hover:shadow-md transition-shadow">
          <!-- Top Accent Line -->
          <div class="absolute top-0 right-0 left-0 h-1 bg-teal-500"></div>
          
          <div>
            <div class="flex items-start gap-4 mb-4">
              <div class="flex-shrink-0 flex items-center justify-center w-12 h-12 rounded-xl bg-teal-50 dark:bg-teal-900/30 text-teal-600 dark:text-teal-400">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-bold text-gray-900 dark:text-white">الخلاصات الإحصائية</h3>
                <p class="text-gray-500 dark:text-gray-400 text-sm mt-1 leading-relaxed">
                  النماذج الإحصائية (1، 2، 3) المعتمدة للخلاصات العددية والفئوية.
                </p>
              </div>
            </div>
          </div>
          
          <div class="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700 space-y-2.5">
            <router-link to="/reports/workforce-summary" class="w-full flex items-center justify-between gap-3 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 px-4 py-2.5 text-sm font-bold text-gray-700 dark:text-gray-200 shadow-sm transition-colors group">
              <span class="flex items-center gap-2">
                <div class="w-1.5 h-1.5 rounded-full bg-teal-500"></div>
                نموذج 1 (خلاصة عددية عامة)
              </span>
              <svg class="h-4 w-4 text-gray-400 group-hover:text-teal-500 rtl:rotate-180 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
            </router-link>
            <router-link to="/reports/inactive-force" class="w-full flex items-center justify-between gap-3 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 px-4 py-2.5 text-sm font-bold text-gray-700 dark:text-gray-200 shadow-sm transition-colors group">
              <span class="flex items-center gap-2">
                <div class="w-1.5 h-1.5 rounded-full bg-teal-500"></div>
                نموذج 2 (قوة غير عاملة)
              </span>
              <svg class="h-4 w-4 text-gray-400 group-hover:text-teal-500 rtl:rotate-180 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
            </router-link>
            <router-link to="/reports/workforce-categorical" class="w-full flex items-center justify-between gap-3 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 px-4 py-2.5 text-sm font-bold text-gray-700 dark:text-gray-200 shadow-sm transition-colors group">
              <span class="flex items-center gap-2">
                <div class="w-1.5 h-1.5 rounded-full bg-teal-500"></div>
                نموذج 3 (خلاصة الفئات)
              </span>
              <svg class="h-4 w-4 text-gray-400 group-hover:text-teal-500 rtl:rotate-180 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
            </router-link>
          </div>
        </div>
        
      </div>
      
      <!-- Section Divider -->
      <div class="flex items-center gap-4 mb-4 mt-8 print:hidden">
        <h3 class="text-lg font-bold text-gray-800 dark:text-gray-200 whitespace-nowrap">سجل الإجراءات والخدمات الفردية</h3>
        <div class="h-px bg-gray-200 dark:bg-gray-800 w-full"></div>
      </div>

      <!-- Advanced Filters Panel -->
      <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900 shadow-sm relative overflow-visible print:hidden">
        <div class="flex items-center justify-between mb-5 border-b border-gray-100 pb-3 dark:border-gray-800">
          <h3 class="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <svg class="h-5 w-5 text-brand-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            تخصيص البيانات والفلترة المتقدمة
            <span v-if="activeAdvancedFilterCount > 0" class="inline-flex items-center justify-center h-5 px-2 rounded-full bg-brand-50 text-brand-600 dark:bg-brand-900/30 dark:text-brand-400 text-xs font-bold border border-brand-200 dark:border-brand-800">{{ activeAdvancedFilterCount }} فلاتر نشطة</span>
          </h3>
          <div class="flex items-center gap-3">
            <button @click="resetAllFilters" class="text-sm px-4 py-2 rounded-lg border border-gray-200 bg-white text-gray-700 shadow-theme-xs hover:bg-gray-50 transition-colors dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 font-medium">
              إفراغ الحقول
            </button>
            <button @click="showAdvancedFilters = !showAdvancedFilters" class="text-sm px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2" :class="showAdvancedFilters ? 'bg-brand-50 text-brand-700 border border-brand-200 dark:bg-brand-900/20 dark:text-brand-300 dark:border-brand-800' : 'bg-gray-100 text-gray-700 border border-transparent dark:bg-gray-800 dark:text-gray-300'">
              {{ showAdvancedFilters ? 'إخفاء الفلاتر التفصيلية' : 'إظهار الفلاتر التفصيلية' }}
              <svg class="h-4 w-4 transition-transform" :class="showAdvancedFilters && 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" /></svg>
            </button>
          </div>
        </div>

        <div class="space-y-6">
          <!-- Main Filters Group -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الشهر</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="selectedMonth" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option value="">كل الأشهر</option>
                  <option v-for="m in 12" :key="m" :value="m">{{ m }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                </span>
              </div>
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">السنة</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="selectedYear" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option value="">كل السنوات</option>
                  <option v-for="y in availableYears" :key="y" :value="y">{{ y }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                </span>
              </div>
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">حالة الطلب</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="selectedStatus" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option value="all">الكل</option>
                  <option value="draft">مسودة</option>
                  <option value="pending">قيد المراجعة</option>
                  <option value="approved">معتمد نهائياً</option>
                  <option value="rejected">مرفوض</option>
                  <option value="committed">منفذ في النظام</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                </span>
              </div>
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الرتبة</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="filterRank" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option value="">جميع الرتب</option>
                  <option v-for="r in coreStore.ranks" :key="r.id" :value="r.id">{{ r.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                </span>
              </div>
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الفئة</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="filterCategory" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option value="">جميع الفئات</option>
                  <option v-for="c in coreStore.jobCategories" :key="c.id" :value="c.id">{{ c.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                </span>
              </div>
            </div>
          </div>

          <!-- Advanced Filters (collapsible) -->
          <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="max-h-0 opacity-0" enter-to-class="max-h-[1000px] opacity-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="max-h-[1000px] opacity-100" leave-to-class="max-h-0 opacity-0">
            <div v-if="showAdvancedFilters" class="overflow-hidden">
              <div class="h-px bg-gray-100 dark:bg-gray-800 my-6"></div>
              <h4 class="text-sm font-bold text-gray-700 dark:text-gray-300 mb-4">بيانات جهة العمل والمناصب</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">إدارة الأمن (الوحدة الرئيسية)</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterSecurityAdmin" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                      <option value="">الكل</option>
                      <option v-for="sa in availableSecurityAdmins" :key="sa.id" :value="sa.id">{{ sa.name }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الإدارة المركزية (المديرية/السرية)</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterCentralDept" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                      <option value="">الكل</option>
                      <option v-for="d in coreStore.centralDepartments" :key="d.id" :value="d.id">{{ d.name }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الفرع (الوحدة التابعة)</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterBranch" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                      <option value="">الكل</option>
                      <option v-for="b in coreStore.branches" :key="b.id" :value="b.id">{{ b.name }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">مركز الشرطة</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterDistrict" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                      <option value="">الكل</option>
                      <option v-for="dp in coreStore.districtPolices" :key="dp.id" :value="dp.id">{{ dp.name }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>
              </div>

              <h4 class="text-sm font-bold text-gray-700 dark:text-gray-300 mb-4">التفاصيل الفردية</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">المنصب</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterPosition" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                      <option value="">الكل</option>
                      <option v-for="p in coreStore.positions" :key="p.id" :value="p.id">{{ p.name }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">المؤهل</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterQualification" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                      <option value="">الكل</option>
                      <option v-for="q in coreStore.qualifications" :key="q.id" :value="q.id">{{ q.name }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">تصنيف القوة</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterForceClass" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                      <option value="">الكل</option>
                      <option value="active">قوة عاملة</option>
                      <option value="inactive">قوة غير عاملة</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">البحث بالرقم العسكري</label>
                  <input v-model="filterMilitaryNumber" type="text" placeholder="الرقم العسكري..." class="block w-full h-11 rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500">
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">البحث بالاسم</label>
                  <input v-model="filterName" type="text" placeholder="اسم الفرد..." class="block w-full h-11 rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500">
                </div>
              </div>
            </div>
          </transition>

          <!-- Actions -->
          <div class="flex items-center gap-4 pt-4 border-t border-gray-100 dark:border-gray-800">
            <button @click="fetchData" class="flex items-center gap-2 rounded-lg bg-brand-600 px-6 py-2.5 text-sm font-bold text-white shadow-theme-xs hover:bg-brand-700 transition-colors">
              <svg class="h-4.5 w-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
              تطبيق الفلاتر واستخراج البيانات
            </button>
            <span v-if="reportData.length > 0" class="text-sm font-bold text-gray-500 dark:text-gray-400">
              تم العثور على <span class="text-brand-600 dark:text-brand-400">{{ reportData.length }}</span> نتيجة مطابقة
            </span>
          </div>
        </div>
      </div>

      <!-- Print Columns Selector -->
      <div class="bg-white dark:bg-gray-900 p-5 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-800 print:hidden relative overflow-hidden">
        <div class="absolute top-0 right-0 w-32 h-32 bg-brand-50 dark:bg-brand-900/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3 z-0"></div>
        <div class="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between mb-4 border-b border-gray-100 dark:border-gray-800 pb-3 gap-3">
          <div>
            <h4 class="text-base font-bold text-gray-800 dark:text-gray-200 flex items-center gap-2">
              <svg class="h-5 w-5 text-brand-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              تخصيص أعمدة الطباعة
            </h4>
            <p class="text-xs text-gray-500 mt-1">تحديد الحقول التي ستظهر في كشف التصدير الرسمي ({{ printSelectedKeys.length }} من أصل {{ allColumns.length }})</p>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <button @click="selectAllPrintCols" class="text-xs px-4 py-1.5 rounded-lg bg-brand-50 border border-brand-200 text-brand-700 hover:bg-brand-100 dark:bg-brand-900/30 dark:border-brand-800 dark:text-brand-300 dark:hover:bg-brand-900/50 font-bold transition-all shadow-theme-xs">تحديد الكل</button>
            <button @click="deselectAllPrintCols" class="text-xs px-4 py-1.5 rounded-lg bg-gray-50 border border-gray-200 text-gray-600 hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 font-bold transition-all shadow-theme-xs">إلغاء الكل</button>
          </div>
        </div>
        <div class="relative z-10 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3">
          <label
            v-for="col in allColumns"
            :key="col.key"
            class="relative flex items-center justify-between px-3 py-2.5 rounded-xl border-2 cursor-pointer transition-all text-sm font-bold shadow-theme-xs select-none group"
            :class="printSelectedKeys.includes(col.key)
              ? 'border-brand-500 bg-brand-50 text-brand-700 dark:border-brand-500/50 dark:bg-brand-500/10 dark:text-brand-300'
              : 'border-gray-200 bg-white text-gray-600 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 hover:border-brand-300 hover:bg-gray-50 dark:hover:bg-gray-800'"
          >
            <input type="checkbox" :value="col.key" v-model="printSelectedKeys" class="hidden" />
            <span class="truncate pr-1">{{ col.label }}</span>
            <div class="shrink-0 flex items-center justify-center w-5 h-5 rounded-md border transition-all"
                 :class="printSelectedKeys.includes(col.key) ? 'bg-brand-500 border-brand-500 text-white' : 'border-gray-300 bg-white dark:border-gray-600 dark:bg-gray-900 group-hover:border-brand-400'">
              <svg v-if="printSelectedKeys.includes(col.key)" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" /></svg>
            </div>
          </label>
        </div>
      </div>

      <!-- Unified DataTable Component -->
      <div class="printable-area print:border-2 print:border-black print:p-1 print:m-0 print:w-full print:shadow-none print:bg-transparent">
        
        <!-- Official Print Header (Hidden in Screen, Visible in Print) -->
        <div class="hidden print:block mb-2 w-full">
          <report-header 
            :title="`الكشف الشهري للخدمات والإجراءات - شهر ${selectedMonth || '-'} / ${selectedYear || '-'}`" 
            :subtitle="`البيانات المستخرجة للإجراءات وتعديلات الحالة - حالة الطلبات: ${getStatusLabel(selectedStatus)}`" 
            reportType="report_4"
          />
        </div>

        <DataTable
          :columns="activePrintColumns"
          :data="filteredData"
          rowKey="index"
          :loading="loading"
          :hasActions="false"
          :hasFilters="false"
          :pageSize="50"
          searchPlaceholder="بحث في المخرجات..."
          emptyTitle="لا توجد بيانات مصدرة"
          emptyDescription="لا توجد إجراءات أو خدمات تطابق معايير البحث المحددة."
          @search="(q) => searchQuery = q"
          @refresh="fetchData"
          @export="exportExcel"
        />

        <!-- Official Print Footer -->
        <div class="mt-2 hidden print:block w-full">
          <report-footer />
        </div>

      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import DataTable from '@/components/tables/DataTable.vue'
import ReportHeader from '@/components/reports/ReportHeader.vue'
import ReportFooter from '@/components/reports/ReportFooter.vue'
import { exportToCSV } from "@/utils/export"
import { useServicesStore } from '@/stores/services'
import { useCoreStore } from '@/stores/core'
import { useAuthStore } from '@/stores/auth'
import Swal from 'sweetalert2'

const printReport = () => {
  window.print()
}

const servicesStore = useServicesStore()
const coreStore = useCoreStore()
const authStore = useAuthStore()

const availableSecurityAdmins = computed(() => {
  if (!authStore.user) return coreStore.securityAdmins
  if (authStore.isAdmin || authStore.user.authz_profile?.supervises_all) {
    return coreStore.securityAdmins
  }
  const myAdminId = authStore.user.authz_profile?.security_admin_id
  const supervised = authStore.user.authz_profile?.supervised_security_admins || []
  const allowedIds = new Set([...supervised, myAdminId].filter(Boolean))
  
  if (allowedIds.size > 0) {
    return coreStore.securityAdmins.filter(sa => allowedIds.has(sa.id))
  }
  return coreStore.securityAdmins
})

const currentYear = new Date().getFullYear()
const availableYears = [currentYear, currentYear - 1, currentYear - 2, currentYear - 3]

const selectedMonth = ref<number | ''>(new Date().getMonth() + 1)
const selectedYear = ref<number | ''>(currentYear)
const selectedStatus = ref('all')
const searchQuery = ref('')
const loading = ref(false)
const reportData = ref<any[]>([])

// Advanced filter state
const showAdvancedFilters = ref(false)
const filterRank = ref<number | ''>('')
const filterCategory = ref<number | ''>('')
const filterSecurityAdmin = ref<number | ''>('')
const filterCentralDept = ref<number | ''>('')
const filterBranch = ref<number | ''>('')
const filterDistrict = ref<number | ''>('')
const filterPosition = ref<number | ''>('')
const filterQualification = ref<number | ''>('')
const filterForceClass = ref('')
const filterMilitaryNumber = ref('')
const filterName = ref('')

const activeAdvancedFilterCount = computed(() => {
  let count = 0
  if (selectedMonth.value) count++
  if (selectedYear.value) count++
  if (selectedStatus.value !== 'all') count++
  if (filterRank.value) count++
  if (filterCategory.value) count++
  if (filterSecurityAdmin.value) count++
  if (filterCentralDept.value) count++
  if (filterBranch.value) count++
  if (filterDistrict.value) count++
  if (filterPosition.value) count++
  if (filterQualification.value) count++
  if (filterForceClass.value) count++
  if (filterMilitaryNumber.value) count++
  if (filterName.value) count++
  return count
})

const resetAllFilters = () => {
  selectedMonth.value = ''
  selectedYear.value = ''
  selectedStatus.value = 'all'
  filterRank.value = ''
  filterCategory.value = ''
  filterSecurityAdmin.value = ''
  filterCentralDept.value = ''
  filterBranch.value = ''
  filterDistrict.value = ''
  filterPosition.value = ''
  filterQualification.value = ''
  filterForceClass.value = ''
  filterMilitaryNumber.value = ''
  filterName.value = ''
  fetchData()
}

// Official Export State
const officialExportDirectorate = ref<number | ''>('')
const currentMonthStr = `${new Date().getFullYear()}-${String(new Date().getMonth() + 1).padStart(2, '0')}`
const officialExportMonth = ref(currentMonthStr)

const allColumns = [
  { key: 'index', label: 'م', printWidth: '2%' },
  { key: 'rank', label: 'الرتبة', printWidth: '4%' },
  { key: 'military_number', label: 'الرقم العسكري', printWidth: '5%' },
  { key: 'national_id', label: 'الرقم الوطني', printWidth: '5%' },
  { key: 'full_name', label: 'الاسم الرباعي واللقب', printWidth: '12%' },
  { key: 'unit', label: 'الوحدة', printWidth: '5%' },
  { key: 'directorate', label: 'السرية / الإدارة / المديرية', printWidth: '6%' },
  { key: 'department', label: 'القسم_فرع السرية', printWidth: '5%' },
  { key: 'affiliated_unit', label: 'الوحدة التابعة', printWidth: '5%' },
  { key: 'position', label: 'المنصب', printWidth: '5%' },
  { key: 'job_title', label: 'المسمى الوظيفي', printWidth: '5%' },
  { key: 'category', label: 'الفئة', printWidth: '4%' },
  { key: 'status', label: 'الحالة', printWidth: '4%' },
  { key: 'status_type', label: 'نوع الحالة', printWidth: '5%' },
  { key: 'force_classification', label: 'تصنيف القوة', printWidth: '5%' },
  { key: 'qualification', label: 'المؤهل', printWidth: '4%' },
  { key: 'phone', label: 'رقم الهاتف', printWidth: '5%' },
  { key: 'old_military_number', label: 'الرقم العسكري السابق', printWidth: '5%' },
  { key: 'expense_status', label: 'حالة النفقات', printWidth: '4%' },
  { key: 'appointment_info', label: 'معلومات التعيين', printWidth: '6%' },
  { key: 'quality', label: 'الجودة', printWidth: '3%' },
  { key: 'join_date', label: 'تاريخ التجنيد', printWidth: '5%' }
]

// Print column selection state
const printSelectedKeys = ref<string[]>(allColumns.map(c => c.key))

const activePrintColumns = computed(() => 
  allColumns.filter(c => printSelectedKeys.value.includes(c.key))
)

const selectAllPrintCols = () => {
  printSelectedKeys.value = allColumns.map(c => c.key)
}
const deselectAllPrintCols = () => {
  printSelectedKeys.value = []
}

const getStatusLabel = (val: string) => {
  const map: Record<string, string> = {
    'all': 'الكل',
    'draft': 'مسودة',
    'pending': 'قيد المراجعة',
    'approved': 'معتمد نهائياً',
    'rejected': 'مرفوض',
    'committed': 'منفذ في النظام'
  }
  return map[val] || val
}

const filteredData = computed(() => {
  if (!searchQuery.value) return reportData.value
  const q = searchQuery.value.toLowerCase()
  return reportData.value.filter(item => 
    item.full_name?.toLowerCase().includes(q) ||
    item.military_number?.includes(q) ||
    item.service_type?.toLowerCase().includes(q)
  )
})

const fetchData = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (selectedMonth.value) params.month = selectedMonth.value
    if (selectedYear.value) params.year = selectedYear.value
    if (selectedStatus.value !== 'all') params.status = selectedStatus.value
    
    // Advanced filters
    if (filterRank.value) params.rank = filterRank.value
    if (filterCategory.value) params.category = filterCategory.value
    if (filterSecurityAdmin.value) params.security_admin = filterSecurityAdmin.value
    if (filterCentralDept.value) params.central_department = filterCentralDept.value
    if (filterBranch.value) params.branch = filterBranch.value
    if (filterDistrict.value) params.district_police = filterDistrict.value
    if (filterPosition.value) params.position = filterPosition.value
    if (filterQualification.value) params.qualification = filterQualification.value
    if (filterForceClass.value) params.force_classification = filterForceClass.value
    if (filterMilitaryNumber.value) params.military_number = filterMilitaryNumber.value
    if (filterName.value) params.name = filterName.value

    const res = await api.get('/reports/detailed-reports/monthly-services/', { params })
    // Format date in client
    reportData.value = (res.data.data || []).map((item: any) => ({
      ...item,
      created_at: item.created_at ? new Date(item.created_at).toLocaleDateString('ar-SA') : '-'
    }))
  } catch (error) {
    console.error('Failed to fetch monthly services report', error)
  } finally {
    loading.value = false
  }
}

const exportExcel = () => {
  exportToCSV(activePrintColumns.value, filteredData.value, 'MonthlyServicesReport_Export.csv')
}

const handleOfficialExport = async () => {
  if (!officialExportMonth.value) return
  
  try {
    // Both specific directorate or "All" will now be handled by exportSheet natively
    // Assuming backend ExcelExportService supports directorate_id='' or missing as "All"
    await servicesStore.exportSheet(officialExportDirectorate.value ? Number(officialExportDirectorate.value) : '', officialExportMonth.value)
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم تصدير الكشف بنجاح', showConfirmButton: false, timer: 3000 })
  } catch (err: any) {
    Swal.fire('خطأ', servicesStore.error || 'فشل عملية التصدير', 'error')
  }
}

const handlePdfExport = async (type: string) => {
  if (!officialExportMonth.value) return
  
  try {
    await servicesStore.exportPdf(officialExportMonth.value, officialExportDirectorate.value, type)
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم تصدير المرفقات كملف PDF بنجاح', showConfirmButton: false, timer: 3000 })
  } catch (err: any) {
    Swal.fire('خطأ', servicesStore.error || 'فشل توليد ملف PDF', 'error')
  }
}

onMounted(() => {
  coreStore.fetchAllReferences()
  fetchData()
})
</script>

<style>
@media print {
  /* ═══ Page setup: zero browser margins, full landscape ═══ */
  @page {
    size: A4 landscape;
    margin: 0 !important;
  }

  /* ═══ Global resets ═══ */
  * {
    box-shadow: none !important;
  }
  body > *:not(#app) { display: none !important; }
  html, body, #app {
    width: 100% !important;
    height: auto !important;
    min-height: auto !important;
    overflow: visible !important;
    position: static !important;
    margin: 0 !important;
    padding: 0 !important;
  }

  /* ═══ Kill ALL layout wrappers padding/margin ═══ */
  .admin-layout-content,
  [class*="admin-layout"],
  main,
  .flex-1,
  .p-4,
  .md\:p-6,
  .space-y-5,
  .space-y-6 {
    padding: 0 !important;
    margin: 0 !important;
    max-width: none !important;
    width: 100% !important;
    height: auto !important;
    min-height: auto !important;
    overflow: visible !important;
    position: static !important;
  }

  .print\:hidden {
    display: none !important;
  }

  /* ═══ Printable area: minimal padding ═══ */
  .printable-area {
    display: block !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 2mm !important;
    border: 2px solid #000 !important;
    border-radius: 0 !important;
    background: #fff !important;
  }

  /* ═══ Table: fill entire width, fixed layout ═══ */
  .printable-area table {
    width: 100% !important;
    table-layout: fixed !important;
    border-collapse: collapse !important;
    border: 2px solid #000 !important;
    font-size: 6px !important;
    line-height: 1.2 !important;
  }

  /* ═══ All cells: tight padding, word-wrap ═══ */
  .printable-area th,
  .printable-area td {
    border: 1px solid #000 !important;
    color: #000 !important;
    padding: 1px 2px !important;
    text-align: center !important;
    vertical-align: middle !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
    white-space: normal !important;
    overflow: visible !important;
    max-width: none !important;
    font-size: 6px !important;
    line-height: 1.2 !important;
  }

  .printable-area th {
    background-color: #e5e7eb !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    font-weight: bold !important;
    font-size: 6.5px !important;
  }

  /* ═══ Override inner <p> tags ═══ */
  .printable-area td p,
  .printable-area th p {
    font-size: 6px !important;
    line-height: 1.2 !important;
    margin: 0 !important;
    padding: 0 !important;
    white-space: normal !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
    overflow: visible !important;
    text-overflow: clip !important;
    max-width: none !important;
  }

  /* ═══ Remove minWidth from th in print ═══ */
  .printable-area th[style] {
    min-width: 0 !important;
  }

  /* ═══ Table scroll container: no overflow clip ═══ */
  .printable-area .max-w-full,
  .printable-area .overflow-x-auto,
  .printable-area [class*="overflow"] {
    overflow: visible !important;
    max-width: none !important;
  }

  /* ═══ Actions column: hide in print ═══ */
  .printable-area th:last-child,
  .printable-area td:last-child {
    /* only if actions column exists */
  }

  /* ═══ Sort icons: hide ═══ */
  .printable-area th svg {
    display: none !important;
  }

  /* ═══ Print header/footer spacing ═══ */
  .printable-area .hidden.print\:block {
    display: block !important;
    margin-bottom: 2mm !important;
  }
}
</style>
