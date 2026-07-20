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
          <!-- ══ Roster Mode Toggle ══ -->
          <div class="flex items-center gap-3 p-4 rounded-xl border-2 border-brand-200 bg-brand-50 dark:bg-brand-900/20 dark:border-brand-800">
            <svg class="h-5 w-5 text-brand-600 dark:text-brand-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 10h16M4 14h8M4 18h8" />
            </svg>
            <span class="text-sm font-bold text-brand-800 dark:text-brand-200 shrink-0">نوع الكشف:</span>
            <div class="flex items-center gap-2 flex-wrap">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" v-model="rosterMode" value="all" class="accent-brand-600" />
                <span class="text-sm font-semibold text-gray-800 dark:text-gray-200">📋 كشف شامل لكل الأفراد</span>
              </label>
              <span class="text-gray-300 dark:text-gray-600">|</span>
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" v-model="rosterMode" value="monthly_changes" class="accent-brand-600" />
                <span class="text-sm font-semibold text-gray-800 dark:text-gray-200">📝 تغييرات وإجراءات الشهر فقط</span>
              </label>
            </div>
            <span class="text-xs text-brand-600 dark:text-brand-400 bg-brand-100 dark:bg-brand-900/40 px-2 py-0.5 rounded-full font-medium shrink-0">
              {{ rosterMode === 'all' ? 'يعرض كل الأفراد المسجلين' : 'يعرض من لديهم إجراء معتمد هذا الشهر' }}
            </span>
          </div>

          <!-- Main Filters Group -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-6">
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
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الرتبة</label>
                  <MultiSelect v-model="filterRank" :options="coreStore.ranks" valueKey="id" labelKey="name" placeholder="جميع الرتب" />
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الفئة</label>
                  <MultiSelect v-model="filterCategory" :options="coreStore.jobCategories" valueKey="id" labelKey="name" placeholder="جميع الفئات" />
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">التصنيف العام للحالة</label>
              <MultiSelect 
                v-model="filterStatusClassification" 
                :options="[{id: 'active_full', name: 'قوة عاملة فعلية'}, {id: 'active_part', name: 'قوة عاملة غير فعلية'}, {id: 'inactive_temp', name: 'قوة غير عاملة مؤقتاً'}, {id: 'inactive_perm', name: 'قوة غير عاملة نهائياً'}]" 
                valueKey="id" 
                labelKey="name" 
                placeholder="جميع الحالات" 
              />
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">نوع الحالة المخصص</label>
              <MultiSelect 
                v-model="filterStatusIds" 
                :options="filteredStatuses" 
                valueKey="id" 
                labelKey="name" 
                placeholder="جميع الأنواع" 
                :disabled="filterStatusClassification.length === 0" 
                disabledPlaceholder="اختر التصنيف أولاً..." 
              />
            </div>
          </div>

          <!-- Advanced Filters (collapsible) -->
          <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="max-h-0 opacity-0" enter-to-class="max-h-[1500px] opacity-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="max-h-[1500px] opacity-100" leave-to-class="max-h-0 opacity-0">
            <div v-if="showAdvancedFilters" class="overflow-hidden">
              <div class="h-px bg-gray-100 dark:bg-gray-800 my-6"></div>
              
              <!-- المجموعة الجديدة: العمر ومدة الخدمة والوصول السريع -->
              <h4 class="text-sm font-bold text-gray-700 dark:text-gray-300 mb-4 text-brand-600 flex items-center gap-2">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                بيانات العمر ومدة الخدمة (التقاعد)
              </h4>
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                <div class="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-xl border border-gray-200 dark:border-gray-700/50">
                  <label class="mb-3 block text-sm font-bold text-gray-700 dark:text-gray-300">نطاق العمر (سنة)</label>
                  <div class="flex items-center gap-2">
                    <input type="number" v-model="filterAgeMin" placeholder="من (مثال: 60)" class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-900 dark:text-white" />
                    <span class="text-gray-400">-</span>
                    <input type="number" v-model="filterAgeMax" placeholder="إلى" class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-900 dark:text-white" />
                  </div>
                </div>
                
                <div class="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-xl border border-gray-200 dark:border-gray-700/50">
                  <label class="mb-3 block text-sm font-bold text-gray-700 dark:text-gray-300">مدة الخدمة (سنة)</label>
                  <div class="flex items-center gap-2">
                    <input type="number" v-model="filterServiceMin" placeholder="من (مثال: 35)" class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-900 dark:text-white" />
                    <span class="text-gray-400">-</span>
                    <input type="number" v-model="filterServiceMax" placeholder="إلى" class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-900 dark:text-white" />
                  </div>
                </div>
              </div>
              
              <div class="flex flex-wrap items-center gap-2 mb-8">
                <span class="text-sm font-bold text-gray-500 ml-2">فلاتر سريعة للتقاعد:</span>
                <button @click="applyQuickFilter('elderly_officers')" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-orange-50 text-orange-700 border border-orange-200 hover:bg-orange-100 dark:bg-orange-900/30 dark:border-orange-800 dark:text-orange-300 transition-colors">كبار السن (ضباط)</button>
                <button @click="applyQuickFilter('elderly_personnel')" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-yellow-50 text-yellow-700 border border-yellow-200 hover:bg-yellow-100 dark:bg-yellow-900/30 dark:border-yellow-800 dark:text-yellow-300 transition-colors">كبار السن (أفراد)</button>
                <button @click="applyQuickFilter('completed_service')" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-red-50 text-red-700 border border-red-200 hover:bg-red-100 dark:bg-red-900/30 dark:border-red-800 dark:text-red-300 transition-colors">أنهى مدة الخدمة القانونية</button>
              </div>

              <div class="h-px bg-gray-100 dark:bg-gray-800 my-6"></div>
              
              <!-- المجموعة الثانية: بيانات جهة العمل والمناصب -->
              <h4 class="text-sm font-bold text-gray-700 dark:text-gray-300 mb-4 text-brand-600 flex items-center gap-2">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
                بيانات جهة العمل والمناصب
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                <div class="lg:col-span-2">
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الإدارة الأمنية (المحافظات)</label>
                  <MultiSelect 
                    v-model="filterSecurityAdmin" 
                    :options="availableSecurityAdmins" 
                    valueKey="id" 
                    labelKey="name" 
                    placeholder="كل الإدارات الأمنية" 
                  />
                </div>
                <div class="lg:col-span-2">
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">جهة العمل التابعة (إدارة مركزية / فرع / مديرية)</label>
                  <MultiSelect 
                    v-model="filterWorkplaces" 
                    :options="groupedWorkplaces" 
                    valueKey="value" 
                    labelKey="label" 
                    placeholder="كل الجهات" 
                    :disabled="filterSecurityAdmin.length === 0"
                    disabledPlaceholder="اختر الإدارة الأمنية أولاً..."
                  />
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">القسم</label>
                  <MultiSelect 
                    v-model="filterDivision" 
                    :options="availableDivisions" 
                    valueKey="id" 
                    labelKey="name" 
                    placeholder="كل الأقسام" 
                    :disabled="filterWorkplaces.length === 0"
                    disabledPlaceholder="اختر جهة العمل أولاً..." 
                  />
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الوحدة</label>
                  <MultiSelect 
                    v-model="filterUnit" 
                    :options="availableUnits" 
                    valueKey="id" 
                    labelKey="name" 
                    placeholder="كل الوحدات" 
                    :disabled="filterDivision.length === 0"
                    disabledPlaceholder="اختر القسم أولاً..." 
                  />
                </div>
              </div>
              
              <h4 class="text-sm font-bold text-gray-700 dark:text-gray-300 mb-4 mt-6 text-brand-600 flex items-center gap-2">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                محل الميلاد
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">المحافظة</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterBirthGov" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                      <option value="">اختر...</option>
                      <option v-for="g in coreStore.governorates" :key="g.id" :value="g.id">{{ g.name }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">المديرية</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterBirthDist" :disabled="!filterBirthGov" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800 disabled:opacity-50 disabled:cursor-not-allowed">
                      <option value="">{{ !filterBirthGov ? 'اختر المحافظة أولاً...' : 'الكل' }}</option>
                      <option v-for="d in birthDistricts" :key="d.id" :value="d.id">{{ d.name_ar }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">العزلة</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterBirthSubDist" :disabled="!filterBirthDist" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800 disabled:opacity-50 disabled:cursor-not-allowed">
                      <option value="">{{ !filterBirthDist ? 'اختر المديرية أولاً...' : 'الكل' }}</option>
                      <option v-for="sd in birthSubDistricts" :key="sd.id" :value="sd.id">{{ sd.name_ar }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">القرية</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterBirthVillage" :disabled="!filterBirthSubDist" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800 disabled:opacity-50 disabled:cursor-not-allowed">
                      <option value="">{{ !filterBirthSubDist ? 'اختر العزلة أولاً...' : 'الكل' }}</option>
                      <option v-for="v in birthVillages" :key="v.id" :value="v.id">{{ v.name_ar }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>
              </div>

              <h4 class="text-sm font-bold text-gray-700 dark:text-gray-300 mb-4 mt-6 text-brand-600 flex items-center gap-2">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                محل الإقامة الحالي
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">المحافظة</label>
                  <MultiSelect v-model="filterResidenceGov" :options="coreStore.governorates" valueKey="id" labelKey="name" placeholder="كل المحافظات" />
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">المديرية</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterResDist" :disabled="!filterResidenceGov" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800 disabled:opacity-50 disabled:cursor-not-allowed">
                      <option value="">{{ filterResidenceGov.length === 0 ? 'اختر المحافظة أولاً...' : 'الكل' }}</option>
                      <option v-for="d in resDistricts" :key="d.id" :value="d.id">{{ d.name_ar }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">العزلة</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterResSubDist" :disabled="!filterResDist" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800 disabled:opacity-50 disabled:cursor-not-allowed">
                      <option value="">{{ !filterResDist ? 'اختر المديرية أولاً...' : 'الكل' }}</option>
                      <option v-for="sd in resSubDistricts" :key="sd.id" :value="sd.id">{{ sd.name_ar }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">القرية</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterResVillage" :disabled="!filterResSubDist" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800 disabled:opacity-50 disabled:cursor-not-allowed">
                      <option value="">{{ !filterResSubDist ? 'اختر العزلة أولاً...' : 'الكل' }}</option>
                      <option v-for="v in resVillages" :key="v.id" :value="v.id">{{ v.name_ar }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>
              </div>

              <h4 class="text-sm font-bold text-gray-700 dark:text-gray-300 mb-4 mt-6 text-brand-600 flex items-center gap-2">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path></svg>
                البيانات المهنية الإضافية
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">المؤهل</label>
                  <MultiSelect v-model="filterQualification" :options="coreStore.qualifications" valueKey="id" labelKey="name" placeholder="كل المؤهلات" />
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">المنصب</label>
                  <MultiSelect v-model="filterPosition" :options="coreStore.positions" valueKey="id" labelKey="name" placeholder="كل المناصب" />
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">تصنيف القوة</label>
                  <MultiSelect v-model="filterForceClass" :options="coreStore.forceTypes" valueKey="id" labelKey="name" placeholder="كل التصنيفات" />
                </div>
              </div>

              <!-- المجموعة الثالثة: البحث -->
              <h4 class="text-sm font-bold text-gray-700 dark:text-gray-300 mb-4 mt-6 text-brand-600 flex items-center gap-2">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                بحث دقيق بالهوية
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-2">
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
            <button @click="exportExcelData" :disabled="reportData.length === 0" class="flex items-center gap-2 px-4 py-2 rounded-lg bg-green-600 hover:bg-green-700 text-white font-bold transition-all shadow-theme-sm disabled:opacity-50 disabled:cursor-not-allowed">
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" /></svg>
              تصدير مخصص (Excel)
            </button>
            <div class="w-px h-6 bg-gray-200 dark:bg-gray-700 mx-1"></div>
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
      <div class="printable-area w-full">
        
        <!-- Official Print Header (Hidden in Screen, Visible in Print) -->
        <div class="hidden print:block mb-2 w-full">
          <report-header 
            title="الكشف الشهري للخدمات والإجراءات" 
            :selectedMonth="officialExportMonth"
            reportType="report_4"
          />
        </div>

        <DataTable
          class="print-no-outer-border print:min-h-0 print:mb-0"
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
          @export="exportExcelData"
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
import { ref, onMounted, computed, watch } from 'vue'
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import DataTable from '@/components/tables/DataTable.vue'
import MultiSelect from '@/components/common/MultiSelect.vue'
import ReportHeader from '@/components/reports/ReportHeader.vue'
import ReportFooter from '@/components/reports/ReportFooter.vue'
import { exportToExcel, exportToCSV } from "@/utils/export"
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

const filteredStatuses = computed(() => {
  if (filterStatusClassification.value.length > 0) {
    return coreStore.statuses.filter((s: any) => filterStatusClassification.value.includes(s.classification))
  }
  return []
})

const currentYear = new Date().getFullYear()
const availableYears = [currentYear, currentYear - 1, currentYear - 2, currentYear - 3]

const selectedMonth = ref<number | ''>(new Date().getMonth() + 1)
const selectedYear = ref<number | ''>(currentYear)
const searchQuery = ref('')
const loading = ref(false)
const reportData = ref<any[]>([])

// Roster Mode: 'all' = كل الأفراد, 'monthly_changes' = تغييرات الشهر فقط
const rosterMode = ref<'all' | 'monthly_changes'>('all')

// إعادة جلب البيانات تلقائياً عند تغيير نوع الكشف
watch(rosterMode, () => {
  fetchData()
})

// Advanced filter state
const showAdvancedFilters = ref(false)
const filterRank = ref<number[]>([])
const filterCategory = ref<number[]>([])
const filterStatusClassification = ref<string[]>([])
const filterStatusIds = ref<number[]>([])


const filterSecurityAdmin = ref<number[]>([])

watch(filterSecurityAdmin, () => {
  // Only keep workplaces that are still valid under the new security admin selection
  const validVals = groupedWorkplaces.value.flatMap((g: any) => g.options.map((o: any) => o.value))
  filterWorkplaces.value = filterWorkplaces.value.filter(val => validVals.includes(val))
})

const filterWorkplaces = ref<string[]>([])
const filterDivision = ref<number[]>([])
const filterUnit = ref<number[]>([])

const availableDivisions = computed(() => {
  if (filterWorkplaces.value.length === 0) return [] // Require workplace selection first
  
  const centrals = filterWorkplaces.value.filter(v => v.startsWith('central_')).map(v => parseInt(v.replace('central_', ''), 10))
  const branches = filterWorkplaces.value.filter(v => v.startsWith('branch_')).map(v => parseInt(v.replace('branch_', ''), 10))
  const districts = filterWorkplaces.value.filter(v => v.startsWith('district_')).map(v => parseInt(v.replace('district_', ''), 10))
  
  return coreStore.divisions.filter((div: any) => {
    if (div.central_department && centrals.includes(div.central_department)) return true
    if (div.branch && branches.includes(div.branch)) return true
    if (div.district_police && districts.includes(div.district_police)) return true
    return false
  })
})

const availableUnits = computed(() => {
  if (filterDivision.value.length === 0) return [] // Require division selection first
  return coreStore.units.filter((u: any) => filterDivision.value.includes(u.division))
})

watch(filterWorkplaces, () => {
  const validDivIds = availableDivisions.value.map((d: any) => d.id)
  filterDivision.value = filterDivision.value.filter(id => validDivIds.includes(id))
})

watch(filterDivision, () => {
  const validUnitIds = availableUnits.value.map((u: any) => u.id)
  filterUnit.value = filterUnit.value.filter(id => validUnitIds.includes(id))
})




watch(filterSecurityAdmin, () => {
  const validVals = groupedWorkplaces.value.flatMap(g => g.options.map((o: any) => o.value))
  filterWorkplaces.value = filterWorkplaces.value.filter(val => validVals.includes(val))
})

const groupedWorkplaces = computed(() => {
  const groups: any[] = []
  
  let centrals = coreStore.centralDepartments
  let branches = coreStore.branches
  let districts = coreStore.districtPolices

  // Filter based on selected Security Admins
  if (filterSecurityAdmin.value.length > 0) {
    centrals = centrals.filter((d: any) => filterSecurityAdmin.value.includes(d.security_admin))
    branches = branches.filter((b: any) => filterSecurityAdmin.value.includes(b.security_admin))
    districts = districts.filter((d: any) => filterSecurityAdmin.value.includes(d.security_admin))
  } else {
    // If no security admin is selected, do we show empty or all? The user says "لا تظهر الا ما يخص المحافظة".
    // Let's return empty groups to force selection first.
    return []
  }

  if (centrals.length) {
    groups.push({
      label: 'الإدارات المركزية / السرايا',
      options: centrals.map((d: any) => ({ value: `central_${d.id}`, label: d.name }))
    })
  }
  if (branches.length) {
    groups.push({
      label: 'الفروع',
      options: branches.map((b: any) => ({ value: `branch_${b.id}`, label: b.name }))
    })
  }
  if (districts.length) {
    groups.push({
      label: 'مراكز الشرطة / المديريات',
      options: districts.map((d: any) => ({ value: `district_${d.id}`, label: d.name_ar || d.name }))
    })
  }
  return groups
})

const filterPosition = ref<number[]>([])
const filterQualification = ref<number[]>([])
const filterForceClass = ref<number[]>([])
const filterMilitaryNumber = ref('')
const filterName = ref('')
const filterAgeMin = ref<number | ''>('')
const filterAgeMax = ref<number | ''>('')
const filterServiceMin = ref<number | ''>('')
const filterServiceMax = ref<number | ''>('')

const filterBirthGov = ref<number | ''>('')
const filterResidenceGov = ref<number[]>([])

const filterBirthDist = ref<number | ''>('')
const filterBirthSubDist = ref<number | ''>('')
const filterBirthVillage = ref<number | ''>('')
const filterResDist = ref<number | ''>('')
const filterResSubDist = ref<number | ''>('')
const filterResVillage = ref<number | ''>('')

const birthDistricts = ref<any[]>([])
const birthSubDistricts = ref<any[]>([])
const birthVillages = ref<any[]>([])

const resDistricts = ref<any[]>([])
const resSubDistricts = ref<any[]>([])
const resVillages = ref<any[]>([])

// Status Watcher
watch(filterStatusClassification, () => {
  filterStatusIds.value = []
  
})

// Birth Watchers
watch(filterBirthGov, async (newVal) => {
  filterBirthDist.value = ''
  filterBirthSubDist.value = ''
  filterBirthVillage.value = ''
  birthDistricts.value = []
  birthSubDistricts.value = []
  birthVillages.value = []
  if (newVal) {
    try {
      const res = await api.get(`/dictionaries/geo/districts/?governorate=${newVal}`)
      birthDistricts.value = res.data.results || res.data
    } catch(e) { console.error(e) }
  }
})
watch(filterBirthDist, async (newVal) => {
  filterBirthSubDist.value = ''
  filterBirthVillage.value = ''
  birthSubDistricts.value = []
  birthVillages.value = []
  if (newVal) {
    try {
      const res = await api.get(`/dictionaries/geo/sub-districts/?district=${newVal}`)
      birthSubDistricts.value = res.data.results || res.data
    } catch(e) { console.error(e) }
  }
})
watch(filterBirthSubDist, async (newVal) => {
  filterBirthVillage.value = ''
  birthVillages.value = []
  if (newVal) {
    try {
      const res = await api.get(`/dictionaries/geo/villages/?sub_district=${newVal}`)
      birthVillages.value = res.data.results || res.data
    } catch(e) { console.error(e) }
  }
})

// Residence Watchers
watch(filterResidenceGov, async (newVal) => {
  filterResDist.value = ''
  filterResSubDist.value = ''
  filterResVillage.value = ''
  resDistricts.value = []
  resSubDistricts.value = []
  resVillages.value = []
  if (newVal) {
    try {
      const res = await api.get(`/dictionaries/geo/districts/?governorate=${newVal}`)
      resDistricts.value = res.data.results || res.data
    } catch(e) { console.error(e) }
  }
})
watch(filterResDist, async (newVal) => {
  filterResSubDist.value = ''
  filterResVillage.value = ''
  resSubDistricts.value = []
  resVillages.value = []
  if (newVal) {
    try {
      const res = await api.get(`/dictionaries/geo/sub-districts/?district=${newVal}`)
      resSubDistricts.value = res.data.results || res.data
    } catch(e) { console.error(e) }
  }
})
watch(filterResSubDist, async (newVal) => {
  filterResVillage.value = ''
  resVillages.value = []
  if (newVal) {
    try {
      const res = await api.get(`/dictionaries/geo/villages/?sub_district=${newVal}`)
      resVillages.value = res.data.results || res.data
    } catch(e) { console.error(e) }
  }
})

const activeAdvancedFilterCount = computed(() => {
  let count = 0
  if (selectedMonth.value) count++
  if (selectedYear.value) count++
  if (filterRank.value.length > 0) count++
  if (filterCategory.value.length > 0) count++
  if (filterSecurityAdmin.value.length > 0) count++
  if (filterWorkplaces.value.length > 0) count++
  if (filterDivision.value.length > 0) count++
  if (filterUnit.value.length > 0) count++
  if (filterPosition.value.length > 0) count++
  if (filterQualification.value.length > 0) count++
  if (filterForceClass.value.length > 0) count++
  if (filterMilitaryNumber.value) count++
  if (filterName.value) count++
  if (filterBirthGov.value) count++
  if (filterBirthDist.value) count++
  if (filterBirthSubDist.value) count++
  if (filterBirthVillage.value) count++
  if (filterResidenceGov.value.length > 0) count++
  if (filterResDist.value) count++
  if (filterResSubDist.value) count++
  if (filterResVillage.value) count++
  if (filterStatusClassification.value.length > 0) count++
  if (filterStatusIds.value.length > 0) count++
  if (filterAgeMin.value || filterAgeMax.value) count++
  if (filterServiceMin.value || filterServiceMax.value) count++
  return count
})

const applyQuickFilter = (type: string) => {
  // Reset fields manually (without triggering fetchData yet)
  selectedMonth.value = ''
  selectedYear.value = ''
  filterRank.value = []
  filterCategory.value = []
  filterSecurityAdmin.value = []
  filterWorkplaces.value = []
  filterDivision.value = []
  filterUnit.value = []
  filterPosition.value = []
  filterQualification.value = []
  filterForceClass.value = []
  filterMilitaryNumber.value = ''
  filterName.value = ''
  filterBirthGov.value = ''
  filterBirthDist.value = ''
  filterBirthSubDist.value = ''
  filterBirthVillage.value = ''
  filterResidenceGov.value = []
  filterResDist.value = ''
  filterResSubDist.value = ''
  filterResVillage.value = ''
  filterStatusClassification.value = []
  filterStatusIds.value = []
  filterAgeMin.value = ''
  filterAgeMax.value = ''
  filterServiceMin.value = ''
  filterServiceMax.value = ''

  if (type === 'elderly_officers') {
    filterAgeMin.value = parseInt(systemSettings.value.retirement_age_officers) || 50
    const officerRanks = coreStore.ranks.filter(r => r.is_officer).map(r => r.id)
    filterRank.value = officerRanks
  } else if (type === 'elderly_personnel') {
    filterAgeMin.value = parseInt(systemSettings.value.retirement_age_general) || 50
    const nonOfficerRanks = coreStore.ranks.filter(r => !r.is_officer).map(r => r.id)
    filterRank.value = nonOfficerRanks
  } else if (type === 'completed_service') {
    filterServiceMin.value = parseInt(systemSettings.value.min_service_years) || 35
  }

  fetchData()
}

const resetAllFilters = () => {
  selectedMonth.value = ''
  selectedYear.value = ''
  filterRank.value = []
  filterCategory.value = []
  filterSecurityAdmin.value = []
  filterWorkplaces.value = []
  filterDivision.value = []
  filterUnit.value = []
  filterPosition.value = []
  filterQualification.value = []
  filterForceClass.value = []
  filterMilitaryNumber.value = ''
  filterName.value = ''
  filterBirthGov.value = ''
  filterBirthDist.value = ''
  filterBirthSubDist.value = ''
  filterBirthVillage.value = ''
  filterResidenceGov.value = []
  filterResDist.value = ''
  filterResSubDist.value = ''
  filterResVillage.value = ''
  filterStatusClassification.value = []
  filterStatusIds.value = []
  filterAgeMin.value = ''
  filterAgeMax.value = ''
  filterServiceMin.value = ''
  filterServiceMax.value = ''
  
  rosterMode.value = 'monthly_changes'
  fetchData()
}

// Official Export State
const officialExportDirectorate = ref<number | ''>('')
const currentMonthStr = `${new Date().getFullYear()}-${String(new Date().getMonth() + 1).padStart(2, '0')}`
const officialExportMonth = ref(currentMonthStr)

const allColumns = [
  { key: 'index', label: 'م', printWidth: '2%' },
  { key: 'officer_number', label: 'رقم الضابط', printWidth: '5%' },
  { key: 'rank', label: 'الرتبة', printWidth: '4%' },
  { key: 'military_number', label: 'الرقم العسكري', printWidth: '5%' },
  { key: 'national_id', label: 'الرقم الوطني', printWidth: '5%' },
  { key: 'full_name', label: 'الاسم', printWidth: '12%', tdClass: 'print-name-col' },
  { key: 'service_roster_type', label: 'نوع كشف الخدمات', printWidth: '5%' },
  { key: 'unit', label: 'الوحدة', printWidth: '5%' },
  { key: 'directorate', label: 'الإدارة / السرية', printWidth: '6%' },
  { key: 'affiliated_unit', label: 'القسم / فرع السرية', printWidth: '5%' },
  { key: 'position', label: 'المنصب', printWidth: '5%' },
  { key: 'job_title', label: 'نوع العمل', printWidth: '5%' },
  { key: 'category', label: 'الفئة', printWidth: '4%' },
  { key: 'status', label: 'الحالة', printWidth: '4%' },
  { key: 'status_type', label: 'نوع الحالة', printWidth: '5%' },
  { key: 'force_classification', label: 'تصنيف القوة', printWidth: '5%' },
  { key: 'qualification', label: 'المؤهل', printWidth: '4%' },
  { key: 'phone', label: 'رقم التليفون', printWidth: '5%' },
  { key: 'expense_status', label: 'حالة النفقات', printWidth: '4%' },
  { key: 'monthly_variables', label: 'متغيرات الشهر', printWidth: '6%' },
  { key: 'notes', label: 'ملاحظات', printWidth: '6%' },
  { key: 'appointment_info', label: 'معلومات التعيين', printWidth: '6%' },
  { key: 'quality', label: 'الجودة', printWidth: '3%' },
  { key: 'join_date', label: 'تاريخ التجنيد', printWidth: '5%' },
  { key: 'birth_governorate', label: 'محافظة الميلاد', printWidth: '5%' },
  { key: 'birth_district', label: 'مديرية الميلاد', printWidth: '5%' },
  { key: 'birth_sub_district', label: 'عزلة الميلاد', printWidth: '5%' },
  { key: 'birth_village', label: 'قرية الميلاد', printWidth: '5%' },
  { key: 'residence_governorate', label: 'محافظة الإقامة', printWidth: '5%' },
  { key: 'residence_district', label: 'مديرية الإقامة', printWidth: '5%' },
  { key: 'residence_sub_district', label: 'عزلة الإقامة', printWidth: '5%' },
  { key: 'residence_village', label: 'قرية الإقامة', printWidth: '5%' }
]

// Print column selection state
const printSelectedKeys = ref<string[]>(allColumns.slice(0, 21).map(c => c.key))

const activePrintColumns = computed(() => 
  allColumns.filter(c => printSelectedKeys.value.includes(c.key))
)

const selectAllPrintCols = () => {
  printSelectedKeys.value = allColumns.map(c => c.key)
}
const deselectAllPrintCols = () => {
  printSelectedKeys.value = []
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
    
    // Advanced filters
    if (filterRank.value.length > 0) params.rank = filterRank.value.join(',')
    if (filterCategory.value.length > 0) params.category = filterCategory.value.join(',')
    
    if (filterSecurityAdmin.value.length > 0) params.security_admin = filterSecurityAdmin.value.join(',')
    
    const centrals = filterWorkplaces.value.filter(v => v.startsWith('central_')).map(v => v.replace('central_', ''))
    if (centrals.length > 0) params.central_department = centrals.join(',')
    
    const branches = filterWorkplaces.value.filter(v => v.startsWith('branch_')).map(v => v.replace('branch_', ''))
    if (branches.length > 0) params.branch = branches.join(',')
    
    const districts = filterWorkplaces.value.filter(v => v.startsWith('district_')).map(v => v.replace('district_', ''))
    if (districts.length > 0) params.district_police = districts.join(',')

    if (filterDivision.value.length > 0) params.division = filterDivision.value.join(',')
    if (filterUnit.value.length > 0) params.unit = filterUnit.value.join(',')
    if (filterPosition.value.length > 0) params.position = filterPosition.value.join(',')
    if (filterQualification.value.length > 0) params.qualification = filterQualification.value.join(',')
    if (filterForceClass.value.length > 0) params.force_classification = filterForceClass.value.join(',')
    if (filterMilitaryNumber.value) params.military_number = filterMilitaryNumber.value
    if (filterName.value) params.name = filterName.value
    if (filterBirthGov.value) params.birth_governorate = filterBirthGov.value
    if (filterBirthDist.value) params.birth_district = filterBirthDist.value
    if (filterBirthSubDist.value) params.birth_sub_district = filterBirthSubDist.value
    if (filterBirthVillage.value) params.birth_village = filterBirthVillage.value
    
    if (filterResidenceGov.value.length > 0) params.residence_governorate = filterResidenceGov.value.join(',')
    if (filterResDist.value) params.residence_district = filterResDist.value
    if (filterResSubDist.value) params.residence_sub_district = filterResSubDist.value
    if (filterResVillage.value) params.residence_village = filterResVillage.value
    
    params.roster_mode = rosterMode.value  // 'all' | 'monthly_changes'
    if (filterStatusClassification.value.length > 0) params.status_classification = filterStatusClassification.value.join(',')
    if (filterStatusIds.value.length > 0) params.status_id = filterStatusIds.value.join(',')

    if (filterAgeMin.value) params.age_min = filterAgeMin.value
    if (filterAgeMax.value) params.age_max = filterAgeMax.value
    if (filterServiceMin.value) params.service_min = filterServiceMin.value
    if (filterServiceMax.value) params.service_max = filterServiceMax.value

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

const exportExcelData = async () => {
  const monthText = selectedMonth.value && selectedYear.value 
    ? `${selectedMonth.value}-${selectedYear.value}`
    : `${new Date().getMonth() + 1}-${new Date().getFullYear()}`; // Fallback to current month if not filtered
  const title = `الكشف الشهري لمتغيرات الخدمات لشهر ${monthText}`;

  const result = await Swal.fire({
    title: 'تنسيق التصدير',
    text: 'اختر شكل عرض الأعمدة في ملف الإكسل',
    icon: 'question',
    showCancelButton: true,
    showCloseButton: true,
    confirmButtonText: 'مضغوط (مُحكم ومناسب للطباعة)',
    cancelButtonText: 'واسع (كبير ومريح للنظر)',
    confirmButtonColor: '#0ea5e9',
    cancelButtonColor: '#64748b',
    reverseButtons: true
  });

  let isCompact = true;
  if (result.isConfirmed) {
    isCompact = true;
  } else if (result.dismiss === 'cancel') {
    isCompact = false;
  } else {
    return; // User closed the dialog
  }

  exportToExcel(activePrintColumns.value, filteredData.value, 'MonthlyServicesReport_Export.xlsx', title, isCompact)
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

const systemSettings = ref<any>({})

const fetchSystemSettings = async () => {
  try {
    const res = await api.get('/dictionaries/system-settings/')
    const data = res.data.results ?? res.data
    data.forEach((s: any) => {
      systemSettings.value[s.key] = s.value
    })
  } catch(e) {
    console.error('Failed to load system settings', e)
  }
}

onMounted(() => {
  coreStore.fetchAllReferences()
  fetchSystemSettings()
  fetchData()
})
</script>

<style scoped>
/* ═══ Screen View Styling (Clean layout) ═══ */
@media screen {
  .printable-area {
    width: 100%;
    overflow-x: auto;
  }
  :deep(.printable-area table th) {
    background-color: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    padding: 10px 8px !important;
  }
  :deep(.printable-area table th div) {
    justify-content: center !important;
    width: 100%;
  }
  :deep(.printable-area table th p) {
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #334155 !important;
    text-align: center !important;
    margin: 0 !important;
    width: 100%;
  }
  :deep(.printable-area table td p) {
    font-size: 11px !important;
    font-weight: 500 !important;
    color: #475569 !important;
    text-align: center !important;
    margin: 0 !important;
  }
  :deep(.printable-area table td) {
    border: 1px solid #e2e8f0 !important;
    padding: 8px 6px !important;
    text-align: center !important;
    vertical-align: middle !important;
  }
}

/* ═══ Print View Styling (Professional formatting) ═══ */
@media print {
  @page {
    size: A4 landscape !important;
    margin: 0 !important;
  }
  body * {
    visibility: hidden;
  }
  .printable-area, .printable-area * {
    visibility: visible;
  }
  
  /* Remove ANY borders/boxes around the main container or header */
  .printable-area {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    margin: 0 !important;
    padding: 3mm !important;
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
  }
  
  /* Remove DataTable's outer border ONLY in this report for print */
  :deep(.print-no-outer-border) {
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
  }

  /* Perfect Print Grid for Table ONLY */
  :deep(table) {
    width: max-content !important; /* Let the table be as wide as the text needs */
    min-width: 100% !important; /* But at least fill the page if there are few columns */
    max-width: none !important;
    table-layout: auto !important; /* Allow columns to naturally size based on content */
    border-collapse: collapse !important;
    border: 1px solid black !important;
    margin-top: 10px !important;
  }
  
  :deep(th), :deep(td) {
    padding: 3px 2px !important;
    border: 1px solid black !important;
    color: black !important;
    text-align: center !important;
    vertical-align: middle !important;
  }
  
  :deep(th) {
    background-color: #f3f4f6 !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    font-weight: 700 !important;
    font-size: 7px !important;
  }
  
  :deep(td) {
    font-size: 6.5px !important;
    font-weight: 500 !important;
    overflow: hidden !important;
    padding: 3px 2px !important;
  }
  
  :deep(tr) {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }
  
  :deep(thead) {
    display: table-header-group !important;
  }
  
  :deep(tfoot) {
    display: table-row-group !important;
  }
  
  /* Inner P tags styling to inherit perfect sizing and remove thickness */
  :deep(th div) {
    justify-content: center !important;
    align-items: center !important;
    width: 100%;
    display: flex !important;
  }
  :deep(th svg) {
    display: none !important;
  }
  :deep(th p) {
    font-size: 7px !important;
    font-weight: 700 !important;
    color: black !important;
    text-align: center !important;
    margin: 0 !important;
    width: 100%;
    white-space: normal !important;
    line-height: 1.2 !important;
  }
  
  :deep(td p) {
    font-size: 6.5px !important;
    font-weight: 500 !important;
    color: black !important;
    text-align: center !important;
    margin: 0 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: clip !important; /* Ellipsis causes RTL bleeding in Webkit print */
    line-height: 1.2 !important;
  }

  :deep(td.print-name-col p) {
    font-weight: 800 !important; /* Extra bold for name only */
    font-size: 7px !important;
  }

  /* Override Tailwind border classes inside print to guarantee thin 1px lines */
  :deep(.border-t) { border-top-width: 1px !important; border-color: black !important; }
  :deep(.border-b) { border-bottom-width: 1px !important; border-color: black !important; }
  :deep(.border-e) { border-inline-end-width: 1px !important; border-color: black !important; }
  :deep(.border-s) { border-inline-start-width: 1px !important; border-color: black !important; }
  :deep(.border), :deep(.border-2), :deep(.print\:border-2) {
    border-width: 1px !important;
    border-color: black !important;
  }
  :deep(.border-gray-200), :deep(.border-gray-300) { border-color: black !important; }
}
</style>
