<template>
  <admin-layout>
    <div class="h-full bg-gray-50 dark:bg-gray-900 pb-20 overflow-x-hidden">
      
      <!-- Official Print Header (Hidden on screen) -->
      <ReportHeader title="التقارير الرسومية التحليلية" />

      <!-- Premium Animated Header -->
      <div class="bg-white px-6 py-8 border-b border-gray-200 dark:bg-gray-800 dark:border-gray-700 shadow-sm relative overflow-hidden print:hidden">
        <div class="absolute top-0 right-0 -mt-16 -mr-16 w-64 h-64 bg-brand-50 rounded-full opacity-50 blur-3xl dark:bg-brand-900/20 pointer-events-none"></div>
        <div class="absolute bottom-0 left-0 -mb-16 -ml-16 w-64 h-64 bg-success-50 rounded-full opacity-50 blur-3xl dark:bg-success-900/20 pointer-events-none"></div>
        
        <div class="mx-auto max-w-[1500px] flex flex-col md:flex-row items-center justify-between gap-4 relative z-10">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-brand-100 rounded-2xl text-brand-600 dark:bg-brand-500/20 dark:text-brand-400">
              <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div>
              <h1 class="text-3xl font-bold text-gray-900 dark:text-white">التقارير الرسومية الشاملة</h1>
              <p class="mt-2 text-sm text-gray-500 dark:text-gray-400 font-medium">
                لوحة قيادة تفاعلية مخصصة لدعم القرار وعرض إحصائيات القوة العاملة بشكل دقيق.
              </p>
            </div>
          </div>
          <div class="flex gap-3 print:hidden">
            <button @click="printDashboard" class="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700 dark:text-gray-300 rounded-lg shadow-theme-sm transition-colors font-bold">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
              طباعة اللوحة
            </button>
            <button
            @click="refreshData"
            :disabled="loading"
            class="flex items-center gap-2 rounded-xl bg-white border border-gray-200 px-6 py-3 text-sm font-bold text-gray-700 shadow-sm hover:bg-gray-50 hover:border-brand-300 hover:text-brand-600 transition-all focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:border-brand-500 dark:hover:text-brand-400 cursor-pointer"
          >
            <svg :class="{'animate-spin': loading}" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            تحديث المؤشرات
          </button>
          </div>
        </div>
      </div>

      <div class="mx-auto max-w-[1500px] px-6 py-8 space-y-8 print:p-0 print:m-0 print:space-y-4">
        
        <!-- Premium KPIs -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 print:grid-cols-4 print:gap-4 print:page-break-inside-avoid">
          <!-- KPI 1 -->
          <div class="bg-gradient-to-br from-white to-gray-50 rounded-2xl p-6 border border-gray-200 shadow-theme-sm relative overflow-hidden group hover:shadow-theme-md transition-all dark:from-gray-800 dark:to-gray-800/80 dark:border-gray-700">
            <div class="absolute right-0 top-0 w-1 h-full bg-brand-500"></div>
            <div class="flex justify-between items-start">
              <div>
                <p class="text-sm font-bold text-gray-500 dark:text-gray-400">إجمالي القوة</p>
                <div class="mt-2 text-3xl font-black text-gray-900 dark:text-white group-hover:text-brand-600 transition-colors">
                  {{ formatNumber(stats.total_personnel || 0) }}
                </div>
              </div>
              <div class="p-3 rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-900/30 dark:text-brand-400 group-hover:scale-110 transition-transform shadow-sm">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
              </div>
            </div>
            <div class="mt-4 text-xs font-bold text-gray-500 bg-white border border-gray-100 inline-block px-3 py-1.5 rounded-lg shadow-sm dark:bg-gray-900 dark:border-gray-800 dark:text-gray-400">شاملة جميع الرتب والتصنيفات</div>
          </div>

          <!-- KPI 2 -->
          <div class="bg-gradient-to-br from-white to-gray-50 rounded-2xl p-6 border border-gray-200 shadow-theme-sm relative overflow-hidden group hover:shadow-theme-md transition-all dark:from-gray-800 dark:to-gray-800/80 dark:border-gray-700">
            <div class="absolute right-0 top-0 w-1 h-full bg-blue-500"></div>
            <div class="flex justify-between items-start">
              <div>
                <p class="text-sm font-bold text-gray-500 dark:text-gray-400">الإدارات والفروع</p>
                <div class="mt-2 text-3xl font-black text-gray-900 dark:text-white group-hover:text-blue-600 transition-colors">
                  {{ formatNumber(stats.active_branches || 0) }}
                </div>
              </div>
              <div class="p-3 rounded-xl bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400 group-hover:scale-110 transition-transform shadow-sm">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
              </div>
            </div>
            <div class="mt-4 text-xs font-bold text-blue-600 bg-white border border-blue-100 inline-block px-3 py-1.5 rounded-lg shadow-sm dark:bg-gray-900 dark:border-gray-800 dark:text-blue-400">وحدات تنظيمية مسجلة</div>
          </div>

          <!-- KPI 3 -->
          <div class="bg-gradient-to-br from-white to-gray-50 rounded-2xl p-6 border border-gray-200 shadow-theme-sm relative overflow-hidden group hover:shadow-theme-md transition-all dark:from-gray-800 dark:to-gray-800/80 dark:border-gray-700">
            <div class="absolute right-0 top-0 w-1 h-full bg-success-500"></div>
            <div class="flex justify-between items-start">
              <div>
                <p class="text-sm font-bold text-gray-500 dark:text-gray-400">ملفات مكتملة كلياً</p>
                <div class="mt-2 text-3xl font-black text-gray-900 dark:text-white group-hover:text-success-600 transition-colors">
                  {{ formatNumber(stats.completed_profiles || 0) }}
                </div>
              </div>
              <div class="p-3 rounded-xl bg-success-50 text-success-600 dark:bg-success-900/30 dark:text-success-400 group-hover:scale-110 transition-transform shadow-sm">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              </div>
            </div>
            <div class="mt-4 text-xs font-bold text-success-600 bg-white border border-success-100 inline-block px-3 py-1.5 rounded-lg shadow-sm dark:bg-gray-900 dark:border-gray-800 dark:text-success-400">موثوقية البيانات 100%</div>
          </div>

          <!-- KPI 4 -->
          <div class="bg-gradient-to-br from-white to-gray-50 rounded-2xl p-6 border border-gray-200 shadow-theme-sm relative overflow-hidden group hover:shadow-theme-md transition-all dark:from-gray-800 dark:to-gray-800/80 dark:border-gray-700">
            <div class="absolute right-0 top-0 w-1 h-full bg-error-500"></div>
            <div class="flex justify-between items-start">
              <div>
                <p class="text-sm font-bold text-gray-500 dark:text-gray-400">نواقص حرجة</p>
                <div class="mt-2 text-3xl font-black text-gray-900 dark:text-white group-hover:text-error-600 transition-colors">
                  {{ formatNumber(stats.critical_alerts || 0) }}
                </div>
              </div>
              <div class="p-3 rounded-xl bg-error-50 text-error-600 dark:bg-error-900/30 dark:text-error-400 group-hover:scale-110 transition-transform shadow-sm">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
              </div>
            </div>
            <div class="mt-4 text-xs font-bold text-error-600 bg-white border border-error-100 inline-block px-3 py-1.5 rounded-lg shadow-sm dark:bg-gray-900 dark:border-gray-800 dark:text-error-400">تتطلب المراجعة الفورية</div>
          </div>
        </div>

        <!-- MAIN CHART: Departments by Rank (Horizontal Stacked Bar) -->
        <!-- Moved to Horizontal Stacked Bar to prevent squishing and clipping of department names -->
        <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 overflow-hidden">
          <div class="px-8 py-6 border-b border-gray-100 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-800/50 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <h3 class="text-xl font-black text-gray-900 dark:text-white flex items-center gap-2">
                <div class="p-2 bg-brand-100 text-brand-600 rounded-lg dark:bg-brand-500/20 dark:text-brand-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                </div>
                الخلاصة الإجمالية: الإدارات والمديريات والفروع بحسب الرتب
              </h3>
              <p class="text-sm text-gray-500 dark:text-gray-400 font-medium mt-2">يعرض هذا المخطط الهيكل التنظيمي مفصلاً بالرتب بأسلوب أفقي لتسهيل القراءة والمقارنة.</p>
            </div>
            
            <div class="flex items-center gap-2 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-600 rounded-xl p-1 shadow-sm transition-all hover:border-brand-500">
              <svg class="w-5 h-5 text-brand-500 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path></svg>
              <select v-model="workforceLevel" @change="fetchWorkforceData" class="bg-transparent border-none text-sm font-bold text-gray-700 dark:text-gray-200 focus:ring-0 cursor-pointer pr-8 w-64">
                <option value="all">عرض كل شيء (إدارات + فروع + مديريات)</option>
                <option value="central">عرض الإدارات المركزية فقط</option>
                <option value="branch">عرض الفروع فقط</option>
                <option value="district">عرض المديريات فقط</option>
              </select>
            </div>
          </div>
          
          <div class="p-6 overflow-hidden">
            <div v-if="loadingWorkforce" class="flex h-[550px] items-center justify-center">
              <div class="flex flex-col items-center gap-4">
                <svg class="h-10 w-10 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
                <span class="text-sm font-bold text-gray-500">جاري تحليل البيانات...</span>
              </div>
            </div>
            <!-- Dynamic height based on number of labels so bars are never squished horizontally -->
            <div v-else-if="workforceSeries.length" class="w-full relative">
              <apexchart type="bar" :height="dynamicWorkforceHeight" :options="workforceChartOptions" :series="workforceSeries"></apexchart>
            </div>
            <div v-else class="flex h-[500px] flex-col items-center justify-center text-gray-500">
              <svg class="w-16 h-16 text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path></svg>
              <span class="font-bold text-lg">لا توجد إدارات أو بيانات للعرض في هذا النطاق</span>
            </div>
          </div>
        </div>

        <!-- Advanced Analytics Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          
          <!-- Officers vs NCOs (New Donut Chart) -->
          <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 relative flex flex-col hover:shadow-theme-md transition-all">
            <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-800/30">
              <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-100 text-indigo-600 dark:bg-indigo-900/40 dark:text-indigo-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                </span>
                نسبة الضباط والأفراد
              </h3>
            </div>
            <div class="p-4 flex-1 flex flex-col items-center justify-center min-h-[380px]">
              <div v-if="loadingAnalytics" class="flex justify-center"><svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg></div>
              <apexchart v-else-if="officersNcosSeries.length && officersNcosSeries.some(v=>v>0)" type="donut" width="100%" height="320" :options="officersNcosChartOptions" :series="officersNcosSeries"></apexchart>
              <div v-else class="text-gray-400 font-bold flex flex-col items-center">
                <svg class="w-10 h-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                لا توجد بيانات متاحة
              </div>
            </div>
          </div>

          <!-- Classification (Pie) -->
          <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 relative flex flex-col hover:shadow-theme-md transition-all">
            <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-800/30">
              <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-100 text-teal-600 dark:bg-teal-900/40 dark:text-teal-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                </span>
                التصنيف الوظيفي (الفئة)
              </h3>
            </div>
            <div class="p-4 flex-1 flex flex-col items-center justify-center min-h-[380px]">
              <div v-if="loadingAnalytics" class="flex justify-center"><svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg></div>
              <apexchart v-else-if="classificationSeries.length && classificationSeries.some(v=>v>0)" type="pie" width="100%" height="320" :options="classificationChartOptions" :series="classificationSeries"></apexchart>
              <div v-else class="text-gray-400 font-bold flex flex-col items-center">
                <svg class="w-10 h-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                لا توجد بيانات متاحة
              </div>
            </div>
          </div>

          <!-- Status (Donut) -->
          <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 relative flex flex-col hover:shadow-theme-md transition-all">
            <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-800/30">
              <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-rose-100 text-rose-600 dark:bg-rose-900/40 dark:text-rose-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                </span>
                توزيع القوة حسب الحالة
              </h3>
            </div>
            <div class="p-4 flex-1 flex flex-col items-center justify-center min-h-[380px]">
              <div v-if="loadingAnalytics" class="flex justify-center"><svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg></div>
              <apexchart v-else-if="statusSeries.length && statusSeries.some(v=>v>0)" type="donut" width="100%" height="320" :options="statusChartOptions" :series="statusSeries"></apexchart>
              <div v-else class="text-gray-400 font-bold flex flex-col items-center">
                <svg class="w-10 h-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                لا توجد بيانات متاحة
              </div>
            </div>
          </div>

          
          <!-- Trend (Area) -->
          <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 relative flex flex-col xl:col-span-2 lg:col-span-2 sm:col-span-1 hover:shadow-theme-md transition-all">
            <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-800/30">
              <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-100 text-blue-600 dark:bg-blue-900/40 dark:text-blue-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                </span>
                معدل التسجيل والإضافة (الاتجاه الزمني)
              </h3>
            </div>
            <div class="p-4 flex-1 flex flex-col justify-center min-h-[380px] w-full">
              <div v-if="loadingAnalytics" class="flex justify-center"><svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg></div>
              <apexchart v-else-if="trendSeries[0]?.data?.length" type="area" width="100%" height="320" :options="trendChartOptions" :series="trendSeries"></apexchart>
              <div v-else class="text-gray-400 font-bold flex flex-col items-center">
                <svg class="w-10 h-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                لا توجد بيانات متاحة
              </div>
            </div>
          </div>

          <!-- 100% Stacked Bar -->
          <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 relative flex flex-col xl:col-span-2 lg:col-span-2 sm:col-span-1 hover:shadow-theme-md transition-all">
            <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-800/30">
              <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-100 text-emerald-600 dark:bg-emerald-900/40 dark:text-emerald-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                </span>
                معدل التأطير (نسبة الضباط للأفراد بالإدارات)
              </h3>
            </div>
            <div class="p-4 flex-1 flex flex-col justify-center min-h-[380px] w-full">
              <div v-if="loadingWorkforce" class="flex justify-center"><svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg></div>
              <apexchart v-else-if="deptOfficerNcoSeries[0]?.data?.length" type="bar" width="100%" :height="Math.max(320, workforceLabels.length * 40)" :options="deptOfficerNcoChartOptions" :series="deptOfficerNcoSeries"></apexchart>
              <div v-else class="text-gray-400 font-bold flex flex-col items-center">
                <svg class="w-10 h-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                لا توجد بيانات متاحة
              </div>
            </div>
          </div>

          <!-- Heatmap -->
          <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 relative flex flex-col xl:col-span-2 lg:col-span-2 sm:col-span-1 hover:shadow-theme-md transition-all">
            <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-800/30">
              <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-rose-100 text-rose-600 dark:bg-rose-900/40 dark:text-rose-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
                </span>
                الخريطة الحرارية (تركز الرتب بالإدارات)
              </h3>
            </div>
            <div class="p-4 flex-1 flex flex-col justify-center min-h-[380px] w-full">
              <div v-if="loadingWorkforce" class="flex justify-center"><svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg></div>
              <apexchart v-else-if="workforceSeries[0]?.data?.length" type="heatmap" width="100%" :height="Math.max(400, workforceLabels.length * 35)" :options="heatmapChartOptions" :series="workforceSeries"></apexchart>
              <div v-else class="text-gray-400 font-bold flex flex-col items-center">
                <svg class="w-10 h-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                لا توجد بيانات متاحة
              </div>
            </div>
          </div>

          
          <!-- Geographic Distribution -->
          <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 relative flex flex-col xl:col-span-2 lg:col-span-2 sm:col-span-1 hover:shadow-theme-md transition-all">
            <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-800/30">
              <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-100 text-teal-600 dark:bg-teal-900/40 dark:text-teal-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </span>
                التوزيع الجغرافي (حسب المحافظة)
              </h3>
            </div>
            <div class="p-4 flex-1 flex flex-col justify-center min-h-[380px]">
              <div v-if="loadingAnalytics" class="flex justify-center"><svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg></div>
              <apexchart v-else-if="geoSeries[0]?.data?.length" type="bar" width="100%" height="320" :options="geoChartOptions" :series="geoSeries"></apexchart>
              <div v-else class="text-gray-400 font-bold flex flex-col items-center">
                <svg class="w-10 h-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                لا توجد بيانات متاحة
              </div>
            </div>
          </div>

          <!-- Data Quality -->
          <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 relative flex flex-col hover:shadow-theme-md transition-all">
            <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-800/30">
              <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-100 text-emerald-600 dark:bg-emerald-900/40 dark:text-emerald-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </span>
                مؤشرات جودة البيانات
              </h3>
            </div>
            <div class="p-4 flex-1 flex flex-col justify-center min-h-[380px]">
              <div v-if="loadingAnalytics" class="flex justify-center"><svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg></div>
              <apexchart v-else-if="dqSeries.length" type="radialBar" width="100%" height="320" :options="dqChartOptions" :series="dqSeries"></apexchart>
              <div v-else class="text-gray-400 font-bold flex flex-col items-center">
                <svg class="w-10 h-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                لا توجد بيانات متاحة
              </div>
            </div>
          </div>

          <!-- Qualifications -->
          <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 relative flex flex-col hover:shadow-theme-md transition-all">
            <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-800/30">
              <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-orange-100 text-orange-600 dark:bg-orange-900/40 dark:text-orange-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path></svg>
                </span>
                التوزيع حسب المؤهل العلمي
              </h3>
            </div>
            <div class="p-4 flex-1 flex flex-col justify-center min-h-[380px]">
              <div v-if="loadingAnalytics" class="flex justify-center"><svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg></div>
              <apexchart v-else-if="qualSeries.length" type="donut" width="100%" height="320" :options="qualChartOptions" :series="qualSeries"></apexchart>
              <div v-else class="text-gray-400 font-bold flex flex-col items-center">
                <svg class="w-10 h-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                لا توجد بيانات متاحة
              </div>
            </div>
          </div>

          <!-- Expenses -->
          <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 relative flex flex-col hover:shadow-theme-md transition-all">
            <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-800/30">
              <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-yellow-100 text-yellow-600 dark:bg-yellow-900/40 dark:text-yellow-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </span>
                الموقف المالي والنفقات
              </h3>
            </div>
            <div class="p-4 flex-1 flex flex-col justify-center min-h-[380px]">
              <div v-if="loadingAnalytics" class="flex justify-center"><svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg></div>
              <apexchart v-else-if="expSeries.length" type="pie" width="100%" height="320" :options="expChartOptions" :series="expSeries"></apexchart>
              <div v-else class="text-gray-400 font-bold flex flex-col items-center">
                <svg class="w-10 h-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                لا توجد بيانات متاحة
              </div>
            </div>
          </div>

          <!-- Overall Ranks (Bar) -->
          <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 relative flex flex-col hover:shadow-theme-md transition-all">
            <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-800/30">
              <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-amber-100 text-amber-600 dark:bg-amber-900/40 dark:text-amber-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path></svg>
                </span>
                إجمالي الأعداد بكل رتبة
              </h3>
            </div>
            <div class="p-4 flex-1 flex flex-col justify-center min-h-[380px] w-full">
              <div v-if="loadingAnalytics" class="flex justify-center"><svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg></div>
              <apexchart v-else-if="overallRanksSeries[0]?.data?.length" type="bar" width="100%" :height="Math.max(320, overallRanksLabels.length * 35)" :options="overallRanksChartOptions" :series="overallRanksSeries"></apexchart>
              <div v-else class="text-gray-400 font-bold flex flex-col items-center">
                <svg class="w-10 h-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                لا توجد بيانات متاحة
              </div>
            </div>
          </div>

        </div>

      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import ReportHeader from '@/components/reports/ReportHeader.vue'
import api from '@/lib/api'
import VueApexCharts from 'vue3-apexcharts'

// UI State
const loading = ref(true)
const loadingAnalytics = ref(true)

const printDashboard = () => {
  window.print()
}

const geoLabels = ref<string[]>([])
const geoSeries = ref<any[]>([])

const qualLabels = ref<string[]>([])
const qualSeries = ref<any[]>([])

const expLabels = ref<string[]>([])
const expSeries = ref<any[]>([])

const dqSeries = ref<any[]>([])

const trendSeries = ref<any[]>([])
const trendLabels = ref<string[]>([])
const deptOfficerNcoSeries = ref<any[]>([])

const loadingWorkforce = ref(true)
const isDarkMode = computed(() => document.documentElement.classList.contains('dark'))

// Data State
const stats = ref<any>({})
const workforceLevel = ref('all')

// --- Workforce Summary (Departments by Ranks) ---
const workforceSeries = ref<any[]>([])
const workforceLabels = ref<string[]>([])
const dynamicWorkforceHeight = computed(() => {
  return Math.max(150, workforceLabels.value.length * 60)
})

// --- Analytics Charts ---
const classificationSeries = ref<number[]>([])
const classificationLabels = ref<string[]>([])

const statusSeries = ref<number[]>([])
const statusLabels = ref<string[]>([])

const overallRanksSeries = ref<any[]>([])
const overallRanksLabels = ref<string[]>([])

const officersNcosSeries = ref<number[]>([])
const officersNcosLabels = ref(['الضباط', 'الأفراد'])

// Ordering list for ranks to keep the chart organized hierarchically
const officerRanksList = [
  "فريق أول", "فريق", "لواء", "عميد", "عقيد", "مقدم", "رائد", "نقيب", "ملازم أول", "ملازم ثاني"
]
const ncoRanksList = [
  "مساعد أول", "مساعد ثاني", "مساعد", "رقيب أول", "رقيب ثاني", "رقيب", "عريف", "جندي", "حارس", "مدني", "طالب"
]
const rankHierarchy = [...officerRanksList, ...ncoRanksList, "بدون"]

const fetchAllData = async () => {
  loading.value = true
  await Promise.all([
    fetchStatsAndAnalytics(),
    fetchWorkforceData()
  ])
  loading.value = false
}

const refreshData = () => {
  fetchAllData()
}

const fetchStatsAndAnalytics = async () => {
  loadingAnalytics.value = true
  try {
    const [statsRes, analyticsRes] = await Promise.all([
      api.get('/personnel/dashboard/stats/'),
      api.get('/personnel/dashboard/analytics/')
    ])
    
    stats.value = statsRes.data
    const a = analyticsRes.data

    // 1. Classification (Pie)
    if (a.force_distribution && a.force_distribution.length) {
      classificationLabels.value = a.force_distribution.map((i: any) => i.name || 'غير مصنف')
      classificationSeries.value = a.force_distribution.map((i: any) => i.value)
    } else {
      classificationSeries.value = []
    }

    // 2. Status (Donut)
    if (a.status_distribution && a.status_distribution.length) {
      statusLabels.value = a.status_distribution.map((i: any) => i.name || 'غير محدد')
      statusSeries.value = a.status_distribution.map((i: any) => i.value)
    } else {
      statusSeries.value = []
    }

    // 3. Overall Ranks & Officers vs NCOs
    if (a.rank_distribution && a.rank_distribution.length) {
      const sortedRanks = [...a.rank_distribution]
      sortedRanks.sort((a, b) => {
        let i = rankHierarchy.indexOf(a.name || 'بدون')
        let j = rankHierarchy.indexOf(b.name || 'بدون')
        if (i === -1) i = 99
        if (j === -1) j = 99
        return i - j
      })
      
      overallRanksLabels.value = sortedRanks.map((i: any) => i.name || 'غير محدد')
      overallRanksSeries.value = [{
        name: 'إجمالي الأفراد',
        data: sortedRanks.map((i: any) => ({
          x: i.name || 'غير محدد',
          y: i.value
        }))
      }]

      // Compute Officers vs NCOs
      let officersCount = 0
      let ncosCount = 0
      sortedRanks.forEach((i: any) => {
        const rankName = i.name || ''
        if (officerRanksList.includes(rankName)) {
          officersCount += i.value
        } else {
          ncosCount += i.value
        }
      })
      officersNcosSeries.value = [officersCount, ncosCount]

      if (a.trend && a.trend.length) {
        trendSeries.value = [{ name: 'التسجيل', data: a.trend.map((i: any) => i.count) }]
        trendLabels.value = a.trend.map((i: any) => {
          const d = new Date(i.date)
          return d.toLocaleDateString('ar-SA', { month: 'short', day: 'numeric' })
        })
      }

      if (a.geographic_distribution && a.geographic_distribution.length) {
        geoLabels.value = a.geographic_distribution.map((i: any) => i.name || 'غير محدد')
        geoSeries.value = [{ name: 'الأفراد', data: a.geographic_distribution.map((i: any) => i.value) }]
      }
      
      if (a.qualification_distribution && a.qualification_distribution.length) {
        qualLabels.value = a.qualification_distribution.map((i: any) => i.name || 'بدون')
        qualSeries.value = a.qualification_distribution.map((i: any) => i.value)
      }
      
      if (a.expense_distribution && a.expense_distribution.length) {
        const translateExp = (val: string) => {
          if (val === 'has_expenses' || val === 'expenses') return 'يستلم نفقات'
          if (val === 'no_expenses') return 'بدون نفقات'
          return 'غير محدد'
        }
        expLabels.value = a.expense_distribution.map((i: any) => translateExp(i.name))
        expSeries.value = a.expense_distribution.map((i: any) => i.value)
      }
      
      if (a.data_quality_stats) {
        const dq = a.data_quality_stats
        const total = dq.complete_profiles + dq.incomplete_profiles || 1
        const completePct = Math.round((dq.complete_profiles / total) * 100)
        const cleanPct = Math.round((dq.clean_data / total) * 100)
        dqSeries.value = [completePct, cleanPct, Math.round(dq.average_score)]
      }

    } else {
      overallRanksSeries.value = []
      officersNcosSeries.value = []
    }
  } catch (error) {
    console.error('Error fetching analytics:', error)
  } finally {
    loadingAnalytics.value = false
  }
}

const fetchWorkforceData = async () => {
  loadingWorkforce.value = true
  try {
    const res = await api.get(`/personnel/reports/workforce-summary/?level=${workforceLevel.value}`)
    const data = res.data.data // Array of units

    const allRanksSet = new Set<string>()
    data.forEach((unit: any) => {
      Object.keys(unit.ranks).forEach(rank => allRanksSet.add(rank))
    })

    const sortedRanks = Array.from(allRanksSet).sort((a, b) => {
      let i = rankHierarchy.indexOf(a)
      let j = rankHierarchy.indexOf(b)
      if (i === -1) i = 99
      if (j === -1) j = 99
      return i - j
    })

    workforceLabels.value = data.map((d: any) => d.unit_name)

    const seriesData = sortedRanks.map(rank => {
      return {
        name: rank,
        data: data.map((unit: any) => ({
          x: unit.unit_name,
          y: unit.ranks[rank] || 0
        }))
      }
    })

    workforceSeries.value = seriesData

    // Compute 100% Stacked Bar for Dept Officers vs NCOs
    const officersData = data.map((unit: any) => {
      let count = 0
      Object.keys(unit.ranks).forEach(rank => {
        if (officerRanksList.includes(rank)) count += unit.ranks[rank]
      })
      return { x: unit.unit_name, y: count }
    })
    const ncosData = data.map((unit: any) => {
      let count = 0
      Object.keys(unit.ranks).forEach(rank => {
        if (!officerRanksList.includes(rank)) count += unit.ranks[rank]
      })
      return { x: unit.unit_name, y: count }
    })
    deptOfficerNcoSeries.value = [
      { name: 'الضباط', data: officersData },
      { name: 'الأفراد', data: ncosData }
    ]


  } catch (error) {
    console.error('Error fetching workforce summary:', error)
  } finally {
    loadingWorkforce.value = false
  }
}

onMounted(() => {
  fetchAllData()
})

const formatNumber = (num: number) => {
  return new Intl.NumberFormat('en-US').format(num)
}

// --- Dynamic Charts Options ---
const fontFamily = 'Tajawal, "Cairo", sans-serif'
const getGridColor = () => isDarkMode.value ? '#374151' : '#f3f4f6'
const getLabelColor = () => isDarkMode.value ? '#9ca3af' : '#6b7280'

const commonChartConfig = {
  fontFamily,
  background: 'transparent',
  animations: {
    enabled: true,
    easing: 'easeinout',
    speed: 800,
    animateGradually: { enabled: true, delay: 150 },
    dynamicAnimation: { enabled: true, speed: 350 }
  }
}

// 1. Stacked Bar Chart (Workforce) - Changed to HORIZONTAL for best layout with many departments
const workforceChartOptions = computed(() => ({
  chart: {
    type: 'bar',
    stacked: true,
    ...commonChartConfig,
    toolbar: { show: true, tools: { download: true, selection: true, zoom: true, pan: true } }
  },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  plotOptions: {
    bar: { horizontal: true, borderRadius: 2, barHeight: '75%' },
  },
  // Official Military/Formal Palette (Blues, Greens, Grays, Golds)
  colors: ['#1e3a8a', '#1d4ed8', '#0369a1', '#14532d', '#166534', '#15803d', '#b45309', '#d97706', '#78350f', '#9a3412', '#b91c1c', '#334155', '#475569', '#0f766e', '#047857', '#0e7490', '#111827'],
  xaxis: {
    labels: { 
      style: { colors: getLabelColor(), fontSize: '13px', fontFamily, fontWeight: 'bold' },
      formatter: (val: any) => Math.round(val)
    },
    axisBorder: { show: false }
  },
  yaxis: {
    title: { text: 'الكثافة العددية', style: { color: getLabelColor(), fontFamily, fontWeight: 'bold' } },
    labels: { style: { colors: getLabelColor(), fontFamily, fontSize: '13px', fontWeight: 'bold' }, minWidth: 150 }
  },
  legend: { position: 'top', horizontalAlign: 'right', fontFamily, labels: { colors: isDarkMode.value ? '#e5e7eb' : '#374151' }, itemMargin: { horizontal: 10, vertical: 5 } },
  fill: { opacity: 0.95 },
  dataLabels: {
    enabled: true,
    formatter: function (val: number) {
      return val > 0 ? formatNumber(val) : ''
    },
    style: { fontSize: '12px', fontFamily, fontWeight: 'bold' }
  },
  grid: { borderColor: getGridColor(), strokeDashArray: 4, xaxis: { lines: { show: true } }, yaxis: { lines: { show: false } } },
  tooltip: { theme: isDarkMode.value ? 'dark' : 'light', y: { formatter: (val: number) => formatNumber(val) } }
}))

// 2. Officers vs NCOs (Donut)
const officersNcosChartOptions = computed(() => ({
  chart: { type: 'donut', ...commonChartConfig, toolbar: { show: false } },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  labels: officersNcosLabels.value,
  colors: ['#0284c7', '#10b981'], // Blue for officers, Green for NCOs
  stroke: { show: isDarkMode.value, colors: ['#1f2937'], width: 2 },
  plotOptions: {
    pie: {
      donut: {
        size: '70%',
        labels: {
          show: true,
          name: { fontSize: '16px', fontFamily, color: getLabelColor() },
          value: { fontSize: '24px', fontWeight: 'bold', fontFamily, color: isDarkMode.value ? '#fff' : '#000' },
          total: { show: true, label: 'إجمالي القوة', color: getLabelColor(), formatter: function (w: any) {
            return formatNumber(w.globals.seriesTotals.reduce((a: number, b: number) => a + b, 0))
          }}
        }
      }
    }
  },
  dataLabels: { enabled: true, style: { fontFamily, fontSize: '14px', fontWeight: 'bold' }, dropShadow: { enabled: true, top: 1, left: 1, blur: 1, color: '#000', opacity: 0.45 } },
  legend: { position: 'bottom', fontFamily, fontSize: '14px', markers: { radius: 12 }, labels: { colors: isDarkMode.value ? '#e5e7eb' : '#374151' } },
  tooltip: { theme: isDarkMode.value ? 'dark' : 'light', y: { formatter: (val: number) => formatNumber(val) + ' فرد' } }
}))

// 3. Classification (Pie)
const classificationChartOptions = computed(() => ({
  chart: { type: 'pie', ...commonChartConfig, toolbar: { show: false } },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  labels: classificationLabels.value,
  colors: ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#64748b', '#ef4444'],
  stroke: { show: isDarkMode.value, colors: ['#1f2937'], width: 2 },
  dataLabels: { enabled: true, style: { fontFamily, fontSize: '13px', fontWeight: 'bold' }, dropShadow: { enabled: true, top: 1, left: 1, blur: 1, color: '#000', opacity: 0.45 } },
  legend: { position: 'bottom', fontFamily, fontSize: '13px', labels: { colors: isDarkMode.value ? '#e5e7eb' : '#374151' } },
  tooltip: { theme: isDarkMode.value ? 'dark' : 'light', y: { formatter: (val: number) => formatNumber(val) } }
}))

// 4. Status (Donut)
const statusChartOptions = computed(() => ({
  chart: { type: 'donut', ...commonChartConfig, toolbar: { show: false } },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  labels: statusLabels.value,
  colors: ['#10b981', '#ef4444', '#f59e0b', '#8b5cf6', '#0ea5e9'],
  stroke: { show: isDarkMode.value, colors: ['#1f2937'], width: 2 },
  plotOptions: { pie: { donut: { size: '65%' } } },
  dataLabels: { enabled: true, style: { fontFamily, fontSize: '12px', fontWeight: 'bold' }, dropShadow: { enabled: true } },
  legend: { position: 'bottom', fontFamily, fontSize: '13px', labels: { colors: isDarkMode.value ? '#e5e7eb' : '#374151' } },
  tooltip: { theme: isDarkMode.value ? 'dark' : 'light', y: { formatter: (val: number) => formatNumber(val) } }
}))


const averageOverallRank = computed(() => {
  if (!overallRanksSeries.value[0]?.data) return 0
  const total = overallRanksSeries.value[0].data.reduce((acc: number, curr: any) => acc + curr.y, 0)
  const len = overallRanksSeries.value[0].data.length
  return len > 0 ? (total / len).toFixed(1) : 0
})

// 5. Overall Ranks (Bar)
const overallRanksChartOptions = computed(() => ({
  chart: { type: 'bar', ...commonChartConfig, toolbar: { show: false } },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  colors: ['#1e3a8a', '#1d4ed8', '#0369a1', '#14532d', '#166534', '#15803d', '#b45309', '#d97706', '#78350f', '#9a3412', '#b91c1c', '#334155', '#475569', '#0f766e', '#047857', '#0e7490', '#111827'],
  plotOptions: {
    bar: { horizontal: true, borderRadius: 4, barHeight: '70%', distributed: true }
  },
  legend: { show: false },
  dataLabels: {
    enabled: true,
    style: { fontSize: '13px', colors: ['#fff'] },
    dropShadow: { enabled: true, top: 1, left: 1, blur: 1, color: '#000', opacity: 0.45 },
    formatter: (val: number) => formatNumber(val)
  },
  annotations: {
    xaxis: [
      {
        x: averageOverallRank.value,
        borderColor: '#ef4444',
        strokeDashArray: 4,
        label: {
          borderColor: '#ef4444',
          style: { color: '#fff', background: '#ef4444', fontWeight: 'bold' },
          text: `المتوسط: ${averageOverallRank.value}`
        }
      }
    ]
  },
  xaxis: {
    labels: { 
      style: { colors: getLabelColor(), fontFamily, fontSize: '12px', fontWeight: 'bold' },
      formatter: (val: any) => Math.round(val)
    },
    axisBorder: { show: false }
  },
  yaxis: {
    labels: { style: { colors: getLabelColor(), fontFamily, fontSize: '11px' } }
  },
  grid: { borderColor: getGridColor(), strokeDashArray: 4, xaxis: { lines: { show: true } }, yaxis: { lines: { show: false } } },
  tooltip: { theme: isDarkMode.value ? 'dark' : 'light', y: { formatter: (val: number) => formatNumber(val) } }
}))

// 6. Trend (Area Chart)
const trendChartOptions = computed(() => ({
  chart: { type: 'area', ...commonChartConfig, toolbar: { show: true, tools: { download: true, zoom: false, pan: false, selection: false } } },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  colors: ['#0369a1'],
  fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.4, opacityTo: 0.05, stops: [0, 100] } },
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth', width: 3 },
  xaxis: {
    categories: trendLabels.value,
    labels: { style: { colors: getLabelColor(), fontFamily, fontSize: '11px' } },
    axisBorder: { show: false }
  },
  yaxis: {
    labels: { style: { colors: getLabelColor(), fontFamily, fontSize: '12px', fontWeight: 'bold' }, formatter: (val: any) => Math.round(val) }
  },
  grid: { borderColor: getGridColor(), strokeDashArray: 4, xaxis: { lines: { show: true } }, yaxis: { lines: { show: true } } },
  tooltip: { theme: isDarkMode.value ? 'dark' : 'light', y: { formatter: (val: number) => formatNumber(val) } }
}))

// 7. 100% Stacked Bar (Officers vs NCOs per Dept)
const deptOfficerNcoChartOptions = computed(() => ({
  chart: { type: 'bar', stacked: true, stackType: '100%', ...commonChartConfig, toolbar: { show: true } },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  colors: ['#1d4ed8', '#166534'], // Navy for officers, Forest Green for NCOs
  plotOptions: { bar: { horizontal: true, borderRadius: 2, barHeight: '75%' } },
  xaxis: { labels: { style: { colors: getLabelColor(), fontFamily, fontWeight: 'bold' }, formatter: (val: any) => val + '%' } },
  yaxis: { labels: { style: { colors: getLabelColor(), fontFamily, fontSize: '12px', fontWeight: 'bold' }, minWidth: 150 } },
  dataLabels: { enabled: true, formatter: (val: any) => Math.round(val) + '%', style: { fontSize: '12px', colors: ['#fff'] }, dropShadow: { enabled: true } },
  legend: { position: 'top', fontFamily, labels: { colors: getLabelColor() } },
  tooltip: { theme: isDarkMode.value ? 'dark' : 'light', y: { formatter: (val: number) => val + ' فرد' } }
}))

// 8. Heatmap
const heatmapChartOptions = computed(() => ({
  chart: { type: 'heatmap', ...commonChartConfig, toolbar: { show: true } },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  plotOptions: {
    heatmap: {
      shadeIntensity: 0.5,
      radius: 4,
      useFillColorAsStroke: false,
      colorScale: {
        ranges: [
          { from: 0, to: 0, color: isDarkMode.value ? '#374151' : '#f3f4f6', name: 'لا يوجد' },
          { from: 1, to: 10, color: '#93c5fd', name: 'منخفض' },
          { from: 11, to: 50, color: '#3b82f6', name: 'متوسط' },
          { from: 51, to: 10000, color: '#1d4ed8', name: 'مرتفع' }
        ]
      }
    }
  },
  dataLabels: { enabled: true, style: { colors: ['#fff'] } },
  xaxis: { labels: { style: { colors: getLabelColor(), fontFamily, fontSize: '11px', fontWeight: 'bold' } } },
  yaxis: { labels: { style: { colors: getLabelColor(), fontFamily, fontSize: '12px', fontWeight: 'bold' }, minWidth: 120 } },
  tooltip: { theme: isDarkMode.value ? 'dark' : 'light' }
}))


// 9. Geographic Distribution (Bar)
const geoChartOptions = computed(() => ({
  chart: { type: 'bar', ...commonChartConfig, toolbar: { show: false } },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  colors: ['#0f766e'],
  plotOptions: { bar: { horizontal: false, borderRadius: 4, columnWidth: '50%' } },
  dataLabels: { enabled: true, style: { fontSize: '12px', colors: ['#fff'] }, formatter: (val: any) => formatNumber(val) },
  xaxis: { categories: geoLabels.value, labels: { style: { colors: getLabelColor(), fontFamily, fontWeight: 'bold' } } },
  yaxis: { labels: { style: { colors: getLabelColor(), fontFamily } } },
  tooltip: { theme: isDarkMode.value ? 'dark' : 'light' }
}))

// 10. Qualification (Donut)
const qualChartOptions = computed(() => ({
  chart: { type: 'donut', ...commonChartConfig, toolbar: { show: false } },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  labels: qualLabels.value,
  colors: ['#1e3a8a', '#1d4ed8', '#0369a1', '#14532d', '#b45309'],
  stroke: { show: isDarkMode.value, colors: ['#1f2937'], width: 2 },
  dataLabels: { enabled: true, style: { fontFamily, fontSize: '12px', fontWeight: 'bold' }, dropShadow: { enabled: true } },
  legend: { position: 'bottom', fontFamily, labels: { colors: getLabelColor() } },
  tooltip: { theme: isDarkMode.value ? 'dark' : 'light' }
}))

// 11. Expenses (Pie)
const expChartOptions = computed(() => ({
  chart: { type: 'pie', ...commonChartConfig, toolbar: { show: false } },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  labels: expLabels.value,
  colors: ['#15803d', '#b91c1c', '#d97706'],
  stroke: { show: isDarkMode.value, colors: ['#1f2937'], width: 2 },
  dataLabels: { enabled: true, style: { fontFamily, fontSize: '12px', fontWeight: 'bold' } },
  legend: { position: 'bottom', fontFamily, labels: { colors: getLabelColor() } },
  tooltip: { theme: isDarkMode.value ? 'dark' : 'light' }
}))

// 12. Data Quality (RadialBar)
const dqChartOptions = computed(() => ({
  chart: { type: 'radialBar', ...commonChartConfig, toolbar: { show: false } },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  colors: ['#10b981', '#3b82f6', '#8b5cf6'],
  plotOptions: {
    radialBar: {
      dataLabels: {
        name: { fontSize: '14px', fontFamily, color: getLabelColor() },
        value: { fontSize: '20px', fontWeight: 'bold', fontFamily, color: getLabelColor(), formatter: (val: any) => val + '%' },
        total: { show: true, label: 'متوسط الجودة', color: getLabelColor(), formatter: (w: any) => Math.round(w.globals.seriesTotals[2]) + '%' }
      }
    }
  },
  labels: ['اكتمال الملفات', 'نظافة البيانات', 'مؤشر الجودة'],
  legend: { show: true, position: 'bottom', fontFamily, labels: { colors: getLabelColor() } }
}))

</script>

<style scoped>
@media print {
  /* Reset page layout entirely for printing */
  @page {
    size: A4 portrait;
    margin: 1cm;
  }
  
  body {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    background: white !important;
  }

  /* Prevent grid from becoming a single messy column */
  .grid {
    display: flex !important;
    flex-direction: column !important;
    gap: 1.5rem !important;
  }
  
  /* Force cards to layout cleanly */
  .bg-white, .bg-gradient-to-br {
    border: 1px solid #e5e7eb !important;
    box-shadow: none !important;
    break-inside: avoid !important;
    page-break-inside: avoid !important;
    margin-bottom: 1rem !important;
    background: white !important;
  }

  /* Hide decorative elements */
  .absolute, .rounded-full.blur-3xl {
    display: none !important;
  }
  
  .shadow-theme-sm, .shadow-theme-md {
    box-shadow: none !important;
  }
  
  /* Fix ApexCharts resizing bug on print */
  :deep(.apexcharts-canvas) {
    width: 100% !important;
    height: auto !important;
    max-height: 280px !important;
  }
  
  :deep(.vue-apexcharts) {
    width: 100% !important;
    height: auto !important;
    max-height: 280px !important;
    min-height: unset !important;
    display: flex;
    justify-content: center;
  }

  /* Keep the header nice */
  .print\:flex {
    display: flex !important;
    break-inside: avoid !important;
    page-break-inside: avoid !important;
  }
}
</style>

<style scoped>
/* Scoped styles */
</style>
