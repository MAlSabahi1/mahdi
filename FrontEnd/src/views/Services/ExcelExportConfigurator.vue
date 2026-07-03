<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="تهيئة وتصدير النماذج المقيدة" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Page Header -->
      <div class="border-b border-gray-200 dark:border-gray-800 pb-5 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-gray-900 dark:text-white flex items-center gap-2">
            <svg class="w-7 h-7 text-brand-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            لوحة تهيئة وتصدير النماذج المقيدة
          </h1>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1.5 max-w-2xl leading-relaxed">
            المنصة المركزية لتوليد الكشوفات ونماذج الإدخال المخصصة للقطاعات الأمنية والمديريات. حدّد نطاق الإرسال المستهدف وعيّن حماية الأعمدة لمنع التعديل على الحقول السيادية.
          </p>
        </div>
        
        <!-- Live Counters -->
        <div class="flex gap-4 bg-gray-50 dark:bg-white/[0.02] p-3 rounded-2xl border border-gray-200 dark:border-gray-800/80">
          <div class="text-center px-4 border-l border-gray-200 dark:border-gray-850">
            <span class="block text-[10px] font-bold text-gray-400">حقول التصدير النشطة</span>
            <span class="text-lg font-black text-blue-600 dark:text-blue-400">{{ totalExportable }}</span>
          </div>
          <div class="text-center px-4">
            <span class="block text-[10px] font-bold text-gray-400">حقول القراءة فقط (المغلقة)</span>
            <span class="text-lg font-black text-red-600 dark:text-red-400">{{ totalLocked }}</span>
          </div>
        </div>
      </div>

      <!-- Main Configurator Layout -->
      <div class="grid gap-6 lg:grid-cols-12">
        
        <!-- Right Column: Target Scope Selector & Advanced Config (Width: 5/12) -->
        <div class="lg:col-span-5 space-y-6">
          
          <!-- Card 1: Target Scope Selector -->
          <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800/80 rounded-3xl p-5 shadow-sm space-y-5">
            <div>
              <h3 class="text-sm font-black text-gray-900 dark:text-white flex items-center gap-2">
                <span class="flex items-center justify-center w-5 h-5 rounded-full bg-brand-50 dark:bg-brand-950/30 text-brand-600 dark:text-brand-400 text-xs font-black">1</span>
                النطاق المستهدف لتوليد النموذج
              </h3>
              <p class="text-[10px] text-gray-450 dark:text-gray-400 mt-1">
                اختر إدارة أمن المحافظة والجهة المستهدفة بالتصدير لإصدار الكشف لصالحها وتوزيع النموذج عليها.
              </p>
            </div>

            <!-- Target Governorate / Security Administration -->
            <div class="space-y-2">
              <label class="block text-xs font-bold text-gray-700 dark:text-gray-300">إدارة أمن المحافظة:</label>
              
              <div v-if="!canExportAllGovernorates" class="p-3 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 text-xs text-gray-700 dark:text-gray-300 font-bold flex items-center justify-between">
                <span>{{ restrictedSecurityAdminName }}</span>
                <span class="text-[9px] px-2 py-0.5 bg-red-50 dark:bg-red-950/30 text-red-750 dark:text-red-400 rounded-lg">
                  نطاق الصلاحية الخاص بك
                </span>
              </div>
              
              <select 
                v-else
                v-model="selectedSecurityAdminId"
                class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-xl px-3 py-2.5 bg-gray-50/50 dark:bg-gray-900 text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-1 focus:ring-brand-500"
              >
                <option :value="null">-- اختر إدارة أمن المحافظة --</option>
                <option v-for="admin in coreStore.securityAdmins" :key="admin.id" :value="admin.id">
                  {{ admin.name }}
                </option>
              </select>
            </div>

            <!-- Sub-Unit selection level -->
            <div class="space-y-3">
              <label class="block text-xs font-bold text-gray-700 dark:text-gray-300">مستوى تصنيف الجهة الفرعية:</label>
              <div class="grid grid-cols-2 gap-2">
                <button 
                  v-for="type in subUnitTypes"
                  :key="type.value"
                  type="button"
                  :disabled="type.value !== 'all' && !selectedSecurityAdminId"
                  @click="selectedSubUnitType = type.value"
                  :class="[
                    selectedSubUnitType === type.value
                      ? 'bg-brand-600 text-white shadow-sm ring-2 ring-brand-500/20'
                      : 'bg-gray-50 dark:bg-gray-900/50 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed'
                  ]"
                  class="px-3 py-2 rounded-xl text-[11px] font-bold transition-all duration-200 text-center"
                >
                  {{ type.label }}
                </button>
              </div>
            </div>

            <!-- Specific Sub-Unit selection dropdown -->
            <div v-if="selectedSubUnitType !== 'all'" class="space-y-2">
              <label class="block text-xs font-bold text-gray-700 dark:text-gray-300">
                اختر {{ subUnitTypeLabel }}:
              </label>
              
              <select
                v-model="selectedSubUnitId"
                class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-xl px-3 py-2.5 bg-gray-50/50 dark:bg-gray-900 text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-1 focus:ring-brand-500"
              >
                <option :value="null">-- اختر {{ subUnitTypeLabel }} (الكل) --</option>
                <option v-for="item in filteredSubUnits" :key="item.id" :value="item.id">
                  {{ item.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- Card 2: Filter by Service Status (Optional) -->
          <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800/80 rounded-3xl p-5 shadow-sm space-y-4">
            <h3 class="text-sm font-black text-gray-900 dark:text-white flex items-center gap-2">
              <span class="flex items-center justify-center w-5 h-5 rounded-full bg-brand-50 dark:bg-brand-950/30 text-brand-600 dark:text-brand-400 text-xs font-black">2</span>
              فلترة الحالات الخدمية
            </h3>
            
            <!-- Description Box -->
            <div class="p-3 bg-blue-50/30 dark:bg-blue-950/10 border border-blue-100/30 dark:border-blue-900/20 rounded-2xl text-[10px] text-gray-500 dark:text-gray-400 leading-relaxed space-y-1">
              <span class="font-bold block text-blue-600 dark:text-blue-400">توضيح فلترة الحالات الخدمية:</span>
              <p>تتيح لك هذه الميزة اختيار فئات معينة من الأفراد فقط لتضمينهم في الكشف (مثلاً: تصدير الأفراد العاملين فقط، أو استبعاد المتقاعدين). إذا تركتها فارغة، سيتم تصدير كافة الحالات تلقائياً.</p>
            </div>

            <div class="border border-gray-150 dark:border-gray-800/60 rounded-2xl overflow-hidden bg-gray-50/20 dark:bg-transparent">
              <div class="flex justify-between items-center p-2.5 bg-gray-50/80 dark:bg-white/[0.01] border-b border-gray-150 dark:border-gray-800/60">
                <span class="text-[11px] font-bold text-gray-800 dark:text-gray-200 font-mono">تحديد الحالات المطلوبة</span>
                <div class="flex gap-2">
                  <button @click="selectAllStatuses" type="button" class="text-[9px] text-brand-600 hover:underline font-bold">الكل</button>
                  <span class="text-gray-300">|</span>
                  <button @click="clearAllStatuses" type="button" class="text-[9px] text-gray-400 hover:underline">مسح</button>
                </div>
              </div>
              <div class="p-3">
                <div class="max-h-[140px] overflow-y-auto space-y-1.5 custom-scrollbar pr-1">
                  <label v-for="item in coreStore.statuses" :key="item.id" class="flex items-center gap-2 p-1.5 rounded-lg hover:bg-gray-50 dark:hover:bg-white/[0.02] cursor-pointer text-right">
                    <input type="checkbox" :value="item.id" v-model="selectedStatuses" class="h-3.5 w-3.5 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
                    <span class="text-[11px] font-medium text-gray-700 dark:text-gray-300">{{ item.name }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Card 3: Advanced Options (Partition / Split By) -->
          <div v-if="isPartitioningAvailable" class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800/80 rounded-3xl p-5 shadow-sm space-y-4 animate-fadeIn">
            <div class="flex justify-between items-center">
              <h3 class="text-sm font-black text-gray-900 dark:text-white flex items-center gap-2">
                <span class="flex items-center justify-center w-5 h-5 rounded-full bg-brand-50 dark:bg-brand-950/30 text-brand-600 dark:text-brand-400 text-xs font-black">3</span>
                تبويب وتقسيم ملف الإكسل (Sheets)
              </h3>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="enablePartitioning" class="sr-only peer" />
                <div class="w-8 h-4.5 bg-gray-200 peer-focus:outline-none rounded-full peer dark:bg-gray-700 peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:right-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3.5 after:w-3.5 after:transition-all dark:border-gray-600 peer-checked:bg-brand-600"></div>
              </label>
            </div>
            
            <!-- Description Box -->
            <div class="p-3 bg-amber-50/30 dark:bg-amber-950/10 border border-amber-100/30 dark:border-amber-900/20 rounded-2xl text-[10px] text-gray-500 dark:text-gray-400 leading-relaxed space-y-1">
              <span class="font-bold block text-amber-600 dark:text-amber-400">توضيح تبويب صفحات الإكسل:</span>
              <p>تفعيل هذا الخيار سيقوم بفصل كشوفات الأفراد إلى صفحات متعددة (Sheets مستقلة) داخل ملف الإكسل المصدّر بناءً على نوع التبويب المختار (مثلاً: صفحة لكل أمن مديرية)، بدلاً من جعل كافة الأفراد في صفحة واحدة.</p>
            </div>

            <div v-if="enablePartitioning" class="space-y-3 pt-2">
              <label class="block text-xs font-bold text-gray-700 dark:text-gray-300">تقسيم الملف تلقائياً حسب:</label>
              <div class="grid grid-cols-1 gap-2">
                <label 
                  v-for="opt in splitOptions" 
                  :key="opt.value"
                  :class="[
                    splitBy === opt.value 
                      ? 'border-brand-500 bg-brand-50/20 dark:bg-brand-950/10' 
                      : 'border-gray-200 dark:border-gray-800 hover:bg-gray-50/50 dark:hover:bg-gray-900/20'
                  ]"
                  class="flex items-start gap-3 p-3 border rounded-2xl cursor-pointer transition-all duration-200"
                >
                  <input 
                    type="radio" 
                    name="split_by" 
                    :value="opt.value" 
                    v-model="splitBy"
                    class="mt-1 text-brand-600 focus:ring-brand-500 cursor-pointer"
                  />
                  <div>
                    <span class="block text-xs font-bold text-gray-900 dark:text-white">{{ opt.label }}</span>
                    <span class="block text-[9px] text-gray-400 mt-0.5 leading-relaxed">{{ opt.description }}</span>
                  </div>
                </label>
              </div>
            </div>
          </div>

          <!-- Trigger Export Button -->
          <button
            @click="triggerExport"
            :disabled="loading"
            class="w-full bg-brand-600 hover:bg-brand-700 disabled:opacity-50 disabled:cursor-not-allowed text-white text-xs font-black py-3.5 rounded-2xl transition-all duration-200 cursor-pointer shadow-sm hover:shadow flex items-center justify-center gap-2"
          >
            <span v-if="loading" class="h-4.5 w-4.5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            <svg v-else class="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            تصدير وتوليد نموذج الكشف المقيد المعتمد
          </button>

        </div>

        <!-- Left Column: Columns Protection Grid Configurator (Width: 7/12) -->
        <div class="lg:col-span-7 bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800/80 rounded-3xl p-5 shadow-sm space-y-5">
          
          <!-- Column Matrix Header -->
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-gray-150 dark:border-gray-800/80 pb-4">
            <div>
              <h3 class="text-sm font-black text-gray-900 dark:text-white">إعداد وتخصيص الأعمدة ومستويات الحماية</h3>
              <p class="text-[10px] text-gray-455 mt-1">حدّد الأعمدة التي تود تضمينها في الكشف المصدّر، وعيّن حالة القفل لمنع تعديل خلاياها داخل الإكسل.</p>
            </div>
            
            <div class="flex items-center gap-2 bg-gray-50 dark:bg-white/[0.02] p-1.5 rounded-xl border border-gray-100 dark:border-gray-855">
              <button @click="resetToDefaultLocks" type="button" class="text-[9px] text-brand-600 hover:text-brand-700 font-bold px-2 py-1 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors">
                الوضع الافتراضي
              </button>
            </div>
          </div>

          <!-- Quick Actions & Global Setup Bar -->
          <div class="bg-gray-50/50 dark:bg-white/[0.01] p-3 rounded-2xl border border-gray-150 dark:border-gray-800 flex flex-wrap gap-2.5 items-center justify-between">
            <span class="text-[10px] font-bold text-gray-455">التحكم الدفعي الجماعي:</span>
            <div class="flex flex-wrap gap-1.5">
              <button @click="bulkExport(true)" type="button" class="text-[9.5px] font-bold px-2.5 py-1.5 bg-blue-50 hover:bg-blue-100 dark:bg-blue-950/20 text-blue-700 dark:text-blue-400 border border-blue-200/50 dark:border-blue-900/30 rounded-lg transition-all">
                تضمين كافة الحقول
              </button>
              <button @click="bulkExport(false)" type="button" class="text-[9.5px] font-bold px-2.5 py-1.5 bg-gray-100 hover:bg-gray-200 dark:bg-gray-900 text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-800 rounded-lg transition-all">
                استبعاد كافة الاختياري
              </button>
              <span class="w-[1px] h-5 bg-gray-200 dark:bg-gray-800 self-center mx-1"></span>
              <button @click="bulkLock(true)" type="button" class="text-[9.5px] font-bold px-2.5 py-1.5 bg-red-50 hover:bg-red-100 dark:bg-red-950/20 text-red-700 dark:text-red-400 border border-red-200/50 dark:border-red-900/30 rounded-lg transition-all">
                قفل الأعمدة النشطة
              </button>
              <button @click="bulkLock(false)" type="button" class="text-[9.5px] font-bold px-2.5 py-1.5 bg-emerald-50 hover:bg-emerald-100 dark:bg-emerald-950/20 text-emerald-700 dark:text-emerald-400 border border-emerald-200/50 dark:border-emerald-900/30 rounded-lg transition-all">
                فتح الأعمدة النشطة
              </button>
            </div>
          </div>

          <!-- FIXED: Quick Unified Columns Configurator Card with Sticky Frozen Header -->
          <div class="bg-gray-50/40 dark:bg-white/[0.01] border border-gray-200 dark:border-gray-850 rounded-2xl p-4 space-y-3">
            <div class="flex justify-between items-center">
              <span class="text-xs font-black text-gray-950 dark:text-white">اللوحة السريعة لإدارة الأعمدة والحماية (تحديث مباشر)</span>
              <span class="text-[9px] text-gray-450 font-medium">تحديث تلقائي للمصفوفة بالأسفل دون الحاجة للتمرير</span>
            </div>

            <!-- Unified compact checkboxes table -->
            <div class="max-h-[240px] overflow-y-auto border border-gray-150 dark:border-gray-800 rounded-xl bg-white dark:bg-gray-900/20 custom-scrollbar relative">
              <table class="w-full text-right border-collapse table-fixed">
                <thead class="sticky top-0 bg-gray-50 dark:bg-gray-900 z-10 shadow-xs">
                  <tr class="border-b border-gray-150 dark:border-gray-800 text-[10px] text-gray-455 font-bold">
                    <th class="p-2.5 w-1/2 text-right bg-gray-50 dark:bg-gray-900">اسم العمود</th>
                    <th class="p-2.5 text-center w-1/4 bg-gray-50 dark:bg-gray-900">تضمين بالتصدير</th>
                    <th class="p-2.5 text-center w-1/4 bg-gray-50 dark:bg-gray-900">قفل (قراءة فقط)</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 dark:divide-gray-850 text-xs">
                  <tr v-for="col in allFlatColumns" :key="col.field" class="hover:bg-gray-50/30 dark:hover:bg-white/[0.01]">
                    <td class="p-2">
                      <span class="font-bold text-gray-800 dark:text-gray-200">{{ col.label }}</span>
                      <span class="block text-[9.5px] text-gray-400 font-mono mt-0.5">{{ col.field }}</span>
                    </td>
                    <td class="p-2 text-center">
                      <input 
                        type="checkbox" 
                        v-model="col.exportable" 
                        :disabled="col.alwaysExportable" 
                        class="h-3.5 w-3.5 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer" 
                      />
                    </td>
                    <td class="p-2 text-center">
                      <input 
                        type="checkbox" 
                        v-model="col.locked" 
                        :disabled="col.alwaysLocked || !col.exportable" 
                        class="h-3.5 w-3.5 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" 
                      />
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Matrix Search input -->
          <div class="relative">
            <input 
              v-model="searchFieldsQuery" 
              placeholder="ابحث عن حقول معينة في مصفوفة الأعمدة المرجعية للتفصيل..." 
              type="text" 
              class="w-full text-xs border border-gray-250 dark:border-gray-800 rounded-xl px-4 py-2.5 bg-gray-50/50 dark:bg-gray-900 text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-1 focus:ring-brand-500" 
            />
            <span class="absolute left-3.5 top-3 text-gray-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </span>
          </div>

          <!-- Columns Groups Matrix Detail Tables -->
          <div class="space-y-6">

            <!-- 1. Identity & Personal Info group -->
            <div v-if="filteredGroups.identity.length > 0" class="bg-gray-50/20 dark:bg-white/[0.01] border border-gray-150 dark:border-gray-800/80 rounded-3xl p-4 space-y-3">
              <h4 class="text-xs font-black text-gray-900 dark:text-white flex items-center gap-2 border-b border-gray-100 dark:border-gray-850 pb-2">
                <span class="w-2 h-4 bg-blue-500 rounded-full"></span>
                بيانات الهوية والبيانات الشخصية
              </h4>
              <div class="overflow-x-auto">
                <table class="w-full text-right border-collapse table-fixed">
                  <thead>
                    <tr class="text-[10px] text-gray-400 font-bold border-b border-gray-100 dark:border-gray-855">
                      <th class="pb-2 w-5/12 text-right">اسم العمود البرمجي</th>
                      <th class="pb-2 text-center w-3/12">حالة التضمين</th>
                      <th class="pb-2 text-center w-4/12">حماية قفل الخلايا</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-100 dark:divide-gray-800 text-xs">
                    <tr v-for="col in filteredGroups.identity" :key="col.field" class="hover:bg-gray-50/20 dark:hover:bg-white/[0.01]">
                      <td class="py-3">
                        <div class="flex items-center gap-2">
                          <span class="font-bold text-gray-850 dark:text-gray-250">{{ col.label }}</span>
                          <code class="px-1.5 py-0.5 bg-gray-50 dark:bg-gray-900 text-gray-450 dark:text-gray-400 font-mono text-[9px] rounded-md border border-gray-200/50 dark:border-gray-800/80 select-all">
                            {{ col.field }}
                          </code>
                        </div>
                      </td>
                      <td class="py-3 text-center">
                        <label class="inline-flex items-center gap-2 cursor-pointer">
                          <input type="checkbox" v-model="col.exportable" :disabled="col.alwaysExportable" class="h-3.5 w-3.5 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer" />
                          <span :class="col.exportable ? 'text-blue-600 bg-blue-50/60 dark:bg-blue-950/20' : 'text-gray-400 bg-gray-50 dark:bg-gray-900/20'" class="text-[9.5px] font-bold px-2 py-0.5 rounded-lg border border-transparent">
                            {{ col.exportable ? 'تصدير' : 'مستبعد' }}
                          </span>
                        </label>
                      </td>
                      <td class="py-3 text-center">
                        <label class="inline-flex items-center gap-2 cursor-pointer">
                          <input type="checkbox" v-model="col.locked" :disabled="col.alwaysLocked || !col.exportable" class="h-3.5 w-3.5 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
                          <span v-if="col.exportable" :class="col.locked ? 'text-red-650 bg-red-50/60 dark:bg-red-950/20 border-red-200/30' : 'text-emerald-650 bg-emerald-50/60 dark:bg-emerald-950/20 border-emerald-200/30'" class="text-[9.5px] font-bold px-2 py-0.5 rounded-lg border">
                            {{ col.locked ? 'مغلق' : 'مفتوح للتعديل' }}
                          </span>
                          <span v-else class="text-[9.5px] text-gray-400 font-bold bg-gray-50 dark:bg-gray-900/20 px-2 py-0.5 rounded-lg border border-transparent">
                            غير مدرج
                          </span>
                        </label>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- 2. Structure group -->
            <div v-if="filteredGroups.structure.length > 0" class="bg-gray-50/20 dark:bg-white/[0.01] border border-gray-150 dark:border-gray-800/80 rounded-3xl p-4 space-y-3">
              <h4 class="text-xs font-black text-gray-900 dark:text-white flex items-center gap-2 border-b border-gray-100 dark:border-gray-855 pb-2">
                <span class="w-2 h-4 bg-purple-500 rounded-full"></span>
                الهيكل التنظيمي والوظيفي
              </h4>
              <div class="overflow-x-auto">
                <table class="w-full text-right border-collapse table-fixed">
                  <thead>
                    <tr class="text-[10px] text-gray-400 font-bold border-b border-gray-100 dark:border-gray-855">
                      <th class="pb-2 w-5/12 text-right">اسم العمود البرمجي</th>
                      <th class="pb-2 text-center w-3/12">حالة التضمين</th>
                      <th class="pb-2 text-center w-4/12">حماية قفل الخلايا</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-100 dark:divide-gray-800 text-xs">
                    <tr v-for="col in filteredGroups.structure" :key="col.field" class="hover:bg-gray-50/20 dark:hover:bg-white/[0.01]">
                      <td class="py-3">
                        <div class="flex items-center gap-2">
                          <span class="font-bold text-gray-855 dark:text-gray-250">{{ col.label }}</span>
                          <code class="px-1.5 py-0.5 bg-gray-50 dark:bg-gray-900 text-gray-455 dark:text-gray-400 font-mono text-[9px] rounded-md border border-gray-200/50 dark:border-gray-800/80 select-all">
                            {{ col.field }}
                          </code>
                        </div>
                      </td>
                      <td class="py-3 text-center">
                        <label class="inline-flex items-center gap-2 cursor-pointer">
                          <input type="checkbox" v-model="col.exportable" :disabled="col.alwaysExportable" class="h-3.5 w-3.5 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer" />
                          <span :class="col.exportable ? 'text-blue-600 bg-blue-50/60 dark:bg-blue-950/20' : 'text-gray-400 bg-gray-50 dark:bg-gray-900/20'" class="text-[9.5px] font-bold px-2 py-0.5 rounded-lg border border-transparent font-mono">
                            {{ col.exportable ? 'تصدير' : 'مستبعد' }}
                          </span>
                        </label>
                      </td>
                      <td class="py-3 text-center">
                        <label class="inline-flex items-center gap-2 cursor-pointer">
                          <input type="checkbox" v-model="col.locked" :disabled="col.alwaysLocked || !col.exportable" class="h-3.5 w-3.5 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
                          <span v-if="col.exportable" :class="col.locked ? 'text-red-655 bg-red-50/60 dark:bg-red-950/20 border-red-200/30' : 'text-emerald-655 bg-emerald-50/60 dark:bg-emerald-950/20 border-emerald-200/30'" class="text-[9.5px] font-bold px-2 py-0.5 rounded-lg border">
                            {{ col.locked ? 'مغلق' : 'مفتوح للتعديل' }}
                          </span>
                          <span v-else class="text-[9.5px] text-gray-400 font-bold bg-gray-50 dark:bg-gray-900/20 px-2 py-0.5 rounded-lg border border-transparent">
                            غير مدرج
                          </span>
                        </label>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- 3. Status and Decisions group -->
            <div v-if="filteredGroups.statusAndDecisions.length > 0" class="bg-gray-50/20 dark:bg-white/[0.01] border border-gray-150 dark:border-gray-800/80 rounded-3xl p-4 space-y-3">
              <h4 class="text-xs font-black text-gray-900 dark:text-white flex items-center gap-2 border-b border-gray-100 dark:border-gray-855 pb-2">
                <span class="w-2 h-4 bg-amber-500 rounded-full"></span>
                الحالة الخدمية والقرارات
              </h4>
              <div class="overflow-x-auto">
                <table class="w-full text-right border-collapse table-fixed">
                  <thead>
                    <tr class="text-[10px] text-gray-400 font-bold border-b border-gray-100 dark:border-gray-855">
                      <th class="pb-2 w-5/12 text-right">اسم العمود البرمجي</th>
                      <th class="pb-2 text-center w-3/12">حالة التضمين</th>
                      <th class="pb-2 text-center w-4/12">حماية قفل الخلايا</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-100 dark:divide-gray-800 text-xs">
                    <tr v-for="col in filteredGroups.statusAndDecisions" :key="col.field" class="hover:bg-gray-50/20 dark:hover:bg-white/[0.01]">
                      <td class="py-3">
                        <div class="flex items-center gap-2">
                          <span class="font-bold text-gray-855 dark:text-gray-255">{{ col.label }}</span>
                          <code class="px-1.5 py-0.5 bg-gray-50 dark:bg-gray-900 text-gray-455 dark:text-gray-400 font-mono text-[9px] rounded-md border border-gray-200/50 dark:border-gray-800/80 select-all">
                            {{ col.field }}
                          </code>
                        </div>
                      </td>
                      <td class="py-3 text-center">
                        <label class="inline-flex items-center gap-2 cursor-pointer">
                          <input type="checkbox" v-model="col.exportable" :disabled="col.alwaysExportable" class="h-3.5 w-3.5 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer" />
                          <span :class="col.exportable ? 'text-blue-600 bg-blue-50/60 dark:bg-blue-950/20' : 'text-gray-400 bg-gray-50 dark:bg-gray-900/20'" class="text-[9.5px] font-bold px-2 py-0.5 rounded-lg border border-transparent font-mono">
                            {{ col.exportable ? 'تصدير' : 'مستبعد' }}
                          </span>
                        </label>
                      </td>
                      <td class="py-3 text-center">
                        <label class="inline-flex items-center gap-2 cursor-pointer">
                          <input type="checkbox" v-model="col.locked" :disabled="col.alwaysLocked || !col.exportable" class="h-3.5 w-3.5 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
                          <span v-if="col.exportable" :class="col.locked ? 'text-red-655 bg-red-50/60 dark:bg-red-950/20 border-red-200/30' : 'text-emerald-655 bg-emerald-50/60 dark:bg-emerald-950/20 border-emerald-200/30'" class="text-[9.5px] font-bold px-2 py-0.5 rounded-lg border">
                            {{ col.locked ? 'مغلق' : 'مفتوح للتعديل' }}
                          </span>
                          <span v-else class="text-[9.5px] text-gray-400 font-bold bg-gray-50 dark:bg-gray-900/20 px-2 py-0.5 rounded-lg border border-transparent">
                            غير مدرج
                          </span>
                        </label>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        </div>

      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { useCoreStore } from '@/stores/core'
import { useAuthStore } from '@/stores/auth'
import api from '@/lib/api'
import Swal from 'sweetalert2'

const coreStore = useCoreStore()
const authStore = useAuthStore()
const loading = ref(false)

// Role-based permissions to determine if user can configure/select all governorates
const canExportAllGovernorates = computed(() => {
  if (authStore.user?.is_superuser || authStore.user?.is_staff) {
    return true
  }
  const profile = authStore.user?.authz_profile
  if (profile?.supervises_all) {
    return true
  }
  return false
})

const isSecurityAdminRestricted = computed(() => !canExportAllGovernorates.value)

const restrictedSecurityAdminName = computed(() => {
  const profile = authStore.user?.authz_profile
  if (!profile || !profile.security_admin_id) return ''
  
  const found = coreStore.securityAdmins.find(a => a.id === profile.security_admin_id)
  return found ? found.name : `إدارة أمن رقم ${profile.security_admin_id}`
})

// 1. Target Scope Selection state
const selectedSecurityAdminId = ref<number | null>(null)
const selectedSubUnitType = ref<'all' | 'central_department' | 'branch' | 'district_police'>('all')
const selectedSubUnitId = ref<number | null>(null)

const subUnitTypes = [
  { value: 'all', label: 'كافة الأفراد بالمحافظة' },
  { value: 'central_department', label: 'إدارة مركزية' },
  { value: 'branch', label: 'فرع' },
  { value: 'district_police', label: 'أمن مديرية' }
] as const

const subUnitTypeLabel = computed(() => {
  switch (selectedSubUnitType.value) {
    case 'central_department': return 'الإدارة المركزية'
    case 'branch': return 'الفرع'
    case 'district_police': return 'أمن المديرية'
    default: return ''
  }
})

// Filter sub-units dynamically based on chosen security admin
const filteredSubUnits = computed(() => {
  if (!selectedSecurityAdminId.value) return []
  
  switch (selectedSubUnitType.value) {
    case 'central_department':
      return coreStore.centralDepartments.filter(dep => dep.security_admin === selectedSecurityAdminId.value)
    case 'branch':
      return coreStore.branches.filter(br => br.security_admin === selectedSecurityAdminId.value)
    case 'district_police':
      return coreStore.districtPolices.filter(dp => dp.security_admin === selectedSecurityAdminId.value)
    default:
      return []
  }
})

// Initialize restricted scope
function initGeographicScope() {
  const profile = authStore.user?.authz_profile
  if (isSecurityAdminRestricted.value && profile && profile.security_admin_id) {
    selectedSecurityAdminId.value = profile.security_admin_id
  }
}

watch(() => authStore.user, initGeographicScope, { immediate: true })

watch(selectedSecurityAdminId, () => {
  selectedSubUnitId.value = null
  selectedSubUnitType.value = 'all'
})

watch(selectedSubUnitType, () => {
  selectedSubUnitId.value = null
})

// 2. Additional Filters (Service Statuses)
const selectedStatuses = ref<number[]>([])

function selectAllStatuses() {
  selectedStatuses.value = coreStore.statuses.map(s => s.id)
}
function clearAllStatuses() {
  selectedStatuses.value = []
}

// 3. Advanced Excel Sheet Division option (Only active when exporting broad scopes like "كافة الأفراد بالمحافظة")
const isPartitioningAvailable = computed(() => {
  return selectedSubUnitType.value === 'all'
})

const enablePartitioning = ref(false)
const splitBy = ref('')
const splitOptions = [
  { value: 'central_department', label: 'مبوبة حسب الإدارة المركزية', description: 'تقسيم كشوفات الأفراد تلقائياً إلى صفحات منفصلة داخل ملف الإكسل (Sheet لكل إدارة مركزية).' },
  { value: 'branch', label: 'مبوبة حسب الفروع', description: 'تقسيم كشوفات الأفراد تلقائياً إلى صفحات منفصلة داخل ملف الإكسل (Sheet لكل فرع).' },
  { value: 'district_police', label: 'مبوبة حسب أمن المديريات', description: 'تقسيم كشوفات الأفراد تلقائياً إلى صفحات منفصلة داخل ملف الإكسل (Sheet لكل أمن مديرية).' }
]

// Automatically disable partitioning when not available
watch(isPartitioningAvailable, (newVal) => {
  if (!newVal) {
    enablePartitioning.value = false
    splitBy.value = ''
  }
})

// 4. Column Configurator matrix state
interface ColumnConfig {
  label: string
  field: string
  locked: boolean
  alwaysLocked: boolean
  exportable: boolean
  alwaysExportable: boolean
}

const columns = ref<{
  identity: ColumnConfig[]
  structure: ColumnConfig[]
  statusAndDecisions: ColumnConfig[]
}>({
  identity: [],
  structure: [],
  statusAndDecisions: []
})

const searchFieldsQuery = ref('')

// Flat columns helper for the top compact unified configurator table
const allFlatColumns = computed(() => {
  return [
    ...columns.value.identity,
    ...columns.value.structure,
    ...columns.value.statusAndDecisions
  ]
})

// Compute filtered columns by search query
const filteredGroups = computed(() => {
  const query = searchFieldsQuery.value.trim().toLowerCase()
  if (!query) return columns.value

  const filterFn = (col: ColumnConfig) => 
    col.label.toLowerCase().includes(query) || col.field.toLowerCase().includes(query)

  return {
    identity: columns.value.identity.filter(filterFn),
    structure: columns.value.structure.filter(filterFn),
    statusAndDecisions: columns.value.statusAndDecisions.filter(filterFn)
  }
})

const totalExportable = computed(() => {
  return allFlatColumns.value.filter(c => c.exportable).length
})

const totalLocked = computed(() => {
  return allFlatColumns.value.filter(c => c.exportable && c.locked).length
})

// Bulk operations
function bulkExport(enable: boolean) {
  allFlatColumns.value.forEach(c => {
    if (!c.alwaysExportable) {
      c.exportable = enable
    }
  })
}

function bulkLock(lock: boolean) {
  allFlatColumns.value.forEach(c => {
    if (c.exportable && !c.alwaysLocked) {
      c.locked = lock
    }
  })
}

function resetToDefaultLocks() {
  allFlatColumns.value.forEach(c => {
    c.locked = c.alwaysLocked || ['military_number', 'full_name', 'national_id', 'security_admin', 'current_rank', 'current_status', 'current_status_classification'].includes(c.field)
    c.exportable = true
  })
  Swal.fire({
    toast: true,
    position: 'top-end',
    icon: 'info',
    title: 'تمت إعادة ضبط التصدير والقفل الافتراضي',
    showConfirmButton: false,
    timer: 2000
  })
}

// Fetch columns matrix structure from backend
async function fetchExportFields() {
  try {
    loading.value = true
    const response = await api.get('/personnel/export-fields/')
    if (response.data && response.data.groups) {
      columns.value = response.data.groups
      
      // Update custom labels to match corrected terminology
      const renameFieldLabel = (fieldList: ColumnConfig[], fieldName: string, newLabel: string) => {
        const found = fieldList.find(c => c.field === fieldName)
        if (found) found.label = newLabel
      }
      renameFieldLabel(columns.value.structure, 'security_admin', 'إدارة أمن المحافظة')
      renameFieldLabel(columns.value.structure, 'central_department', 'الإدارة المركزية')
      renameFieldLabel(columns.value.structure, 'branch', 'الفرع')
      renameFieldLabel(columns.value.structure, 'district_police', 'أمن المديرية')
    }
  } catch (err) {
    console.error('Failed to fetch export fields:', err)
  } finally {
    loading.value = false
  }
}

// Trigger Excel Generation and Download
async function triggerExport() {
  try {
    loading.value = true
    
    // 1. Gather configured fields and locks
    const exportFields: string[] = []
    const lockedFields: string[] = []
    
    allFlatColumns.value.forEach(c => {
      if (c.exportable) {
        exportFields.push(c.field)
        if (c.locked) {
          lockedFields.push(c.field)
        }
      }
    })

    // 2. Set scope IDs based on selection type
    const queryParams: Record<string, any> = {
      columns: exportFields.join(','),
      locked_columns: lockedFields.join(','),
      statuses: selectedStatuses.value.join(',')
    }

    if (selectedSecurityAdminId.value) {
      queryParams.security_admins = selectedSecurityAdminId.value.toString()
    }

    if (selectedSubUnitType.value === 'central_department' && selectedSubUnitId.value) {
      queryParams.central_departments = selectedSubUnitId.value.toString()
    } else if (selectedSubUnitType.value === 'branch' && selectedSubUnitId.value) {
      queryParams.branches = selectedSubUnitId.value.toString()
    } else if (selectedSubUnitType.value === 'district_police' && selectedSubUnitId.value) {
      queryParams.district_polices = selectedSubUnitId.value.toString()
    }

    // 3. Set partitioning param if active
    if (enablePartitioning.value && splitBy.value) {
      queryParams.split_by = splitBy.value
    }

    const response = await api.get('/personnel/export_csv/', {
      params: queryParams,
      responseType: 'blob'
    })

    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const downloadUrl = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = downloadUrl
    
    // Custom filename
    a.download = `كشف_أفراد_مقيد.xlsx`
    
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(downloadUrl)
    document.body.removeChild(a)

    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: 'تم توليد وتصدير الكشف المعتمد بنجاح',
      showConfirmButton: false,
      timer: 3000
    })
  } catch (err) {
    console.error('Failed to export columns sheet:', err)
    Swal.fire({
      icon: 'error',
      title: 'فشل التصدير',
      text: 'حدث خطأ أثناء الاتصال بالخادم، يرجى المحاولة لاحقاً.'
    })
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (!authStore.user) {
    await authStore.fetchMe()
  }
  if (coreStore.securityAdmins.length === 0) {
    coreStore.fetchAllReferences()
  }
  fetchExportFields()
  initGeographicScope()
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 5px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #334155;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fadeIn {
  animation: fadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
</style>
