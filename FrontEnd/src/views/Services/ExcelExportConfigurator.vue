<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="إعداد وتصدير النماذج" />

    <div class="space-y-6" dir="rtl">
      
      <!-- Premium Page Header -->
      <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-theme-xs">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <div class="p-2.5 bg-brand-50 dark:bg-brand-500/10 rounded-xl text-brand-600 dark:text-brand-400">
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            لوحة تهيئة وتصدير النماذج المقيدة
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2 font-medium leading-relaxed">
            المنصة المركزية لتوليد الكشوفات ونماذج الإدخال المخصصة للقطاعات الأمنية والمديريات. حدّد نطاق الإرسال المستهدف وعيّن حماية الأعمدة لمنع التعديل على الحقول السيادية.
          </p>
        </div>
        
        <!-- Live Counters -->
        <div class="flex gap-5 flex-shrink-0">
          <div class="rounded-2xl border border-blue-200 bg-blue-50 p-4 shadow-theme-xs dark:border-blue-500/20 dark:bg-blue-500/5 text-center min-w-[120px]">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400">
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
              </div>
              <div class="text-start">
                <p class="text-xs font-medium text-blue-700 dark:text-blue-400">حقول التصدير</p>
                <h3 class="text-xl font-bold text-blue-900 dark:text-blue-300">{{ totalExportable }}</h3>
              </div>
            </div>
          </div>
          <div class="rounded-2xl border border-error-200 bg-error-50 p-4 shadow-theme-xs dark:border-error-500/20 dark:bg-error-500/5 text-center min-w-[120px]">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-error-100 text-error-600 dark:bg-error-500/20 dark:text-error-400">
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
              </div>
              <div class="text-start">
                <p class="text-xs font-medium text-error-700 dark:text-error-400">حقول مقفلة</p>
                <h3 class="text-xl font-bold text-error-900 dark:text-error-300">{{ totalLocked }}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Settings Cards Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Target Scope Card -->
        <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900 overflow-hidden flex flex-col group transition-all hover:shadow-theme-sm">
          <div class="border-b border-gray-100 bg-gray-50/80 px-6 py-4 dark:border-gray-800 dark:bg-gray-800/40 flex items-center gap-3">
            <div class="flex h-9 w-9 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/20 dark:text-brand-400 border border-brand-100 dark:border-brand-500/30 text-sm font-black">
              1
            </div>
            <div>
              <h3 class="text-sm font-bold text-gray-900 dark:text-white">النطاق المستهدف</h3>
              <p class="text-[10px] font-medium text-gray-500 dark:text-gray-400 mt-0.5">حدد نطاق التصدير الجغرافي</p>
            </div>
          </div>
          <div class="p-5 space-y-4 flex-1 flex flex-col">
            <div v-if="!canExportAllGovernorates" class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-200 dark:border-gray-700">
              <span class="text-sm font-bold text-gray-700 dark:text-gray-300">{{ restrictedSecurityAdminName }}</span>
              <span class="text-[10px] px-2 py-0.5 bg-error-50 text-error-700 dark:bg-error-500/10 dark:text-error-400 rounded-full font-bold border border-error-100 dark:border-error-500/20">صلاحيتك</span>
            </div>
            <BaseSelect
              v-else
              v-model="selectedSecurityAdminId"
              label="إدارة أمن المحافظة"
              :options="coreStore.securityAdmins"
              valueKey="id"
              labelKey="name"
              placeholder="-- اختر المحافظة --"
            />

            <div class="grid grid-cols-2 gap-2">
              <button 
                v-for="type in subUnitTypes" 
                :key="type.value" 
                type="button" 
                :disabled="type.value !== 'all' && !selectedSecurityAdminId" 
                @click="selectedSubUnitType = type.value" 
                :class="[
                  'px-3 py-2 rounded-lg text-xs font-bold transition-all border',
                  selectedSubUnitType === type.value 
                    ? 'bg-brand-600 text-white border-brand-600 shadow-theme-xs' 
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed'
                ]"
              >{{ type.label }}</button>
            </div>
            
            <div v-if="selectedSubUnitType !== 'all'">
              <BaseSelect
                v-model="selectedSubUnitId"
                :disabled="!selectedSecurityAdminId"
                :label="subUnitTypeLabel"
                :options="filteredSubUnits"
                valueKey="id"
                labelKey="name"
                :placeholder="'-- ' + subUnitTypeLabel + ' --'"
              />
              <p v-if="!selectedSecurityAdminId" class="text-xs text-warning-600 dark:text-warning-400 mt-1.5 font-medium flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
                يرجى اختيار المحافظة أولاً.
              </p>
            </div>
          </div>
        </div>

        <!-- Filter Statuses Card -->
        <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900 overflow-hidden flex flex-col group transition-all hover:shadow-theme-sm">
          <div class="border-b border-gray-100 bg-gray-50/80 px-6 py-4 dark:border-gray-800 dark:bg-gray-800/40 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="flex h-9 w-9 items-center justify-center rounded-xl bg-success-50 text-success-600 dark:bg-success-500/20 dark:text-success-400 border border-success-100 dark:border-success-500/30 text-sm font-black">
                2
              </div>
              <div>
                <h3 class="text-sm font-bold text-gray-900 dark:text-white">فلترة الحالات</h3>
                <p class="text-[10px] font-medium text-gray-500 dark:text-gray-400 mt-0.5">اختر الحالات المراد تصديرها</p>
              </div>
            </div>
            <div class="flex gap-2 items-center">
              <button @click="selectAllStatuses" type="button" class="text-xs text-brand-600 dark:text-brand-400 font-bold hover:underline transition-colors">الكل</button>
              <span class="text-gray-300 dark:text-gray-600">|</span>
              <button @click="clearAllStatuses" type="button" class="text-xs text-gray-400 dark:text-gray-500 hover:underline transition-colors">مسح</button>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col">
            <div class="border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50/50 dark:bg-gray-800/30 p-3 flex-grow overflow-hidden flex flex-col">
              <div class="overflow-y-auto max-h-[160px] space-y-1 custom-scrollbar pr-1 flex-grow">
                <label v-for="item in coreStore.statuses" :key="item.id" class="flex items-center gap-2.5 p-2 hover:bg-white dark:hover:bg-gray-800 rounded-lg cursor-pointer transition-colors">
                  <input type="checkbox" :value="item.id" v-model="selectedStatuses" class="h-3.5 w-3.5 text-brand-600 border-gray-300 dark:border-gray-600 rounded focus:ring-brand-500" />
                  <span class="text-xs text-gray-700 dark:text-gray-300 font-medium">{{ item.name }}</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Partitioning Card -->
        <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900 overflow-hidden flex flex-col group transition-all hover:shadow-theme-sm">
          <div class="border-b border-gray-100 bg-gray-50/80 px-6 py-4 dark:border-gray-800 dark:bg-gray-800/40 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="flex h-9 w-9 items-center justify-center rounded-xl bg-warning-50 text-warning-600 dark:bg-warning-500/20 dark:text-warning-400 border border-warning-100 dark:border-warning-500/30 text-sm font-black">
                3
              </div>
              <div>
                <h3 class="text-sm font-bold text-gray-900 dark:text-white">تبويب وتقسيم</h3>
                <p class="text-[10px] font-medium text-gray-500 dark:text-gray-400 mt-0.5">خيارات تقسيم الملف</p>
              </div>
            </div>
            <label v-if="isPartitioningAvailable" class="relative inline-flex items-center cursor-pointer flex-shrink-0">
              <input type="checkbox" v-model="enablePartitioning" class="sr-only peer" />
              <div class="w-9 h-5 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-brand-500/20 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all dark:border-gray-600 peer-checked:bg-brand-600"></div>
            </label>
          </div>
          <div class="p-5 flex-1 flex flex-col">
            <div v-if="enablePartitioning && isPartitioningAvailable" class="space-y-4 flex-1">
              <BaseSelect
                v-model="exportMode"
                label="نوع التصدير"
                :options="[{id: 'single', name: 'كشف واحد موحد للجميع'}, {id: 'multi', name: 'مبوبة بـ 4 أوراق (حسب التصنيف)'}]"
                valueKey="id"
                labelKey="name"
                :placeholder="false"
              />
              <BaseSelect
                v-model="splitBy"
                label="التقسيم المكاني"
                :options="[{id: '', name: 'بدون تقسيم مكاني إضافي'}, ...splitOptions.map(o => ({id: o.value, name: o.label}))]"
                valueKey="id"
                labelKey="name"
                :placeholder="false"
              />
            </div>
            <div v-else class="flex-1 flex flex-col items-center justify-center space-y-3 p-4 text-center">
              <div class="flex h-14 w-14 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800">
                <svg class="w-7 h-7 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
              </div>
              <p class="text-xs text-gray-400 dark:text-gray-500 font-medium">
                {{ isPartitioningAvailable ? 'فعّل التبويب لتقسيم الملف.' : 'سيتم التصدير كملف واحد موحد.' }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Live Table Columns Preview -->
      <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
        
        <div class="border-b border-gray-100 bg-gray-50/80 px-6 py-5 dark:border-gray-800 dark:bg-gray-800/40 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div class="flex items-center gap-4">
            <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/20 dark:text-brand-400 border border-brand-100 dark:border-brand-500/30">
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">معاينة حية وتخصيص الأعمدة</h3>
              <p class="text-xs font-medium text-gray-500 dark:text-gray-400 mt-1">
                قم بإدارة الأعمدة مباشرة: 
                <span class="inline-flex items-center gap-1 text-gray-600 dark:text-gray-300">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/></svg>
                  لإخفاء العمود
                </span>
                ·
                <span class="inline-flex items-center gap-1 text-gray-600 dark:text-gray-300">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
                  لقفل التعديل
                </span>
              </p>
            </div>
          </div>
          <div class="flex gap-2 flex-shrink-0">
            <!-- Hidden columns dropdown -->
            <div class="relative group">
              <BaseButton variant="outline" size="sm">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                إظهار المخفية ({{ hiddenColumns.length }})
              </BaseButton>
              <div class="absolute left-0 top-full mt-2 w-52 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-20 max-h-64 overflow-y-auto custom-scrollbar">
                <div v-if="hiddenColumns.length === 0" class="p-4 text-center text-xs text-gray-400 dark:text-gray-500 font-medium">لا توجد أعمدة مخفية</div>
                <button v-for="col in hiddenColumns" :key="col.field" @click="col.exportable = true" class="w-full text-right px-4 py-2.5 text-xs hover:bg-gray-50 dark:hover:bg-gray-800 font-medium border-b border-gray-100 dark:border-gray-800 last:border-0 flex items-center justify-between group/btn text-gray-700 dark:text-gray-300 transition-colors">
                  {{ col.label }}
                  <svg class="w-4 h-4 text-gray-300 dark:text-gray-600 group-hover/btn:text-brand-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
                </button>
              </div>
            </div>
            
            <BaseButton @click="resetToDefaultLocks" variant="secondary" size="sm">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
              إعادة الضبط
            </BaseButton>
          </div>
        </div>

        <!-- The Live Table -->
        <div class="overflow-x-auto custom-scrollbar relative">
          <table class="w-full text-right border-collapse whitespace-nowrap min-w-max">
            <thead>
              <tr>
                <th 
                  v-for="col in exportableColumns" 
                  :key="col.field"
                  class="border-b border-gray-200 dark:border-gray-800 p-3 min-w-[140px] relative group transition-colors duration-300"
                  :class="[
                    col.locked 
                      ? 'bg-blue-50/60 dark:bg-blue-900/10' 
                      : 'bg-emerald-50/60 dark:bg-emerald-900/10',
                    'border-l border-gray-200 dark:border-gray-800 last:border-l-0'
                  ]"
                >
                  <div class="flex flex-col gap-2.5">
                    <!-- Actions Row -->
                    <div class="flex items-center justify-between text-gray-400">
                      <!-- Hide Toggle -->
                      <button 
                        @click="col.exportable = false" 
                        :disabled="col.alwaysExportable" 
                        class="p-1.5 rounded-lg bg-white/60 dark:bg-black/20 hover:bg-white dark:hover:bg-gray-800 hover:shadow-sm hover:text-gray-700 dark:hover:text-gray-300 disabled:opacity-30 disabled:cursor-not-allowed transition-all" 
                        title="إخفاء العمود"
                      >
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/></svg>
                      </button>
                      
                      <!-- Lock Toggle -->
                      <button 
                        @click="col.locked = !col.locked" 
                        :disabled="col.alwaysLocked" 
                        class="p-1.5 rounded-lg bg-white/60 dark:bg-black/20 hover:bg-white dark:hover:bg-gray-800 hover:shadow-sm disabled:opacity-30 disabled:cursor-not-allowed transition-all" 
                        :class="[col.locked ? 'text-blue-600 hover:text-blue-700' : 'text-emerald-600 hover:text-emerald-700']"
                        :title="col.locked ? 'مقفل (قراءة فقط)' : 'مفتوح (قابل للتعديل)'"
                      >
                        <svg v-if="col.locked" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
                        <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z"/></svg>
                      </button>
                    </div>

                    <!-- Header Label -->
                    <div class="text-center">
                      <span class="block text-xs font-bold" :class="[col.locked ? 'text-blue-900 dark:text-blue-300' : 'text-emerald-900 dark:text-emerald-300']">
                        {{ col.label }}
                      </span>
                      <span class="block text-[9px] font-mono mt-1 opacity-60" :class="[col.locked ? 'text-blue-700 dark:text-blue-400' : 'text-emerald-700 dark:text-emerald-400']">
                        {{ col.field }}
                      </span>
                    </div>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              <template v-if="loadingPreview">
                <tr v-for="i in 4" :key="i" class="bg-white dark:bg-gray-900 border-b border-gray-100 dark:border-gray-800">
                  <td v-for="col in exportableColumns" :key="col.field" class="border-l border-gray-100 dark:border-gray-800 p-4 text-center">
                    <div class="h-2 w-16 rounded-full mx-auto animate-pulse" :class="[col.locked ? 'bg-gray-200 dark:bg-gray-800' : 'bg-emerald-100 dark:bg-emerald-900/20']"></div>
                  </td>
                </tr>
              </template>
              <template v-else-if="previewData.length > 0">
                <tr v-for="(row, idx) in previewData" :key="idx" class="bg-white dark:bg-gray-900 border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                  <td v-for="col in exportableColumns" :key="col.field" class="border-l border-gray-100 dark:border-gray-800 p-3 text-center text-xs font-medium text-gray-700 dark:text-gray-300">
                    <span v-if="col.field.startsWith('pseudo_') && col.field !== 'pseudo_status_type'" class="text-gray-300 dark:text-gray-600">--</span>
                    <span v-else>{{ getPreviewValue(row, col.field) }}</span>
                  </td>
                </tr>
              </template>
              <template v-else>
                <tr>
                  <td :colspan="exportableColumns.length" class="p-12 text-center bg-white dark:bg-gray-900">
                    <div class="flex flex-col items-center gap-3">
                      <div class="flex h-14 w-14 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800">
                        <svg class="h-7 w-7 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                      </div>
                      <p class="text-sm text-gray-400 dark:text-gray-500 font-medium">لا توجد بيانات مطابقة لهذه الفلترة لعرضها كمعاينة.</p>
                    </div>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Export Button -->
      <div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-theme-xs dark:border-gray-800 dark:bg-gray-900">
        <BaseButton
          @click="triggerExport"
          :disabled="loading"
          :loading="loading"
          variant="primary"
          size="lg"
          customClass="w-full rounded-xl font-bold"
        >
          <svg v-if="!loading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
          {{ loading ? 'جاري التوليد والتصدير...' : 'تصدير وتوليد نموذج الكشف المقيد المعتمد' }}
        </BaseButton>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import BaseSelect from '@/components/common/BaseSelect.vue'
import BaseButton from '@/components/common/BaseButton.vue'
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
const exportMode = ref('single')
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

const previewData = ref<any[]>([])
const loadingPreview = ref(false)

async function fetchPreviewData() {
  loadingPreview.value = true
  try {
    const params: Record<string, any> = { limit: 4 }
    
    if (selectedSecurityAdminId.value) params.security_admin = selectedSecurityAdminId.value
    if (selectedSubUnitType.value === 'branch' && selectedSubUnitId.value) params.branch = selectedSubUnitId.value
    if (selectedSubUnitType.value === 'central_department' && selectedSubUnitId.value) params.central_department = selectedSubUnitId.value
    if (selectedSubUnitType.value === 'district_police' && selectedSubUnitId.value) params.district_police = selectedSubUnitId.value
    
    const res = await api.get('/personnel/', { params })
    previewData.value = res.data.results || []
  } catch (err) {
    console.error('Preview fetch error:', err)
  } finally {
    loadingPreview.value = false
  }
}

watch([selectedSecurityAdminId, selectedSubUnitId, selectedSubUnitType], () => {
  fetchPreviewData()
})

function getPreviewValue(row: any, field: string) {
  if (field === 'security_admin') {
    if (row.security_admin && typeof row.security_admin === 'object') return row.security_admin.name;
    const found = coreStore.securityAdmins?.find(i => i.id === row.security_admin);
    return found ? found.name : '—';
  }
  if (field === 'central_department_or_branch') {
    if (row.central_department_name) return row.central_department_name;
    if (row.branch_name) return row.branch_name;
    if (row.district_police_name) return row.district_police_name;
    
    if (row.central_department) {
      if (typeof row.central_department === 'object') return row.central_department.name;
      const found = coreStore.centralDepartments?.find(i => i.id === row.central_department);
      if (found) return found.name;
    }
    if (row.branch) {
      if (typeof row.branch === 'object') return row.branch.name;
      const found = coreStore.branches?.find(i => i.id === row.branch);
      if (found) return found.name;
    }
    if (row.district_police) {
      if (typeof row.district_police === 'object') return row.district_police.name;
      const found = coreStore.districtPolices?.find(i => i.id === row.district_police);
      if (found) return found.name;
    }
    return '—';
  }
  if (field === 'district_police_or_division') {
    if (row.division_name) return row.division_name;

    if (row.division) {
      if (typeof row.division === 'object') return row.division.name;
      const found = coreStore.divisions?.find(i => i.id === row.division);
      if (found) return found.name;
    }
    return '—';
  }
  
  const val = row[field]
  
  if (val && typeof val === 'object' && val.name) return val.name
  
  // Map IDs to names
  if (field === 'current_rank') {
    const found = coreStore.ranks?.find(i => i.id === val)
    if (found) return found.name
  }
  if (field === 'category') {
    const found = coreStore.jobCategories?.find(i => i.id === val)
    if (found) return found.name
  }
  if (field === 'qualification') {
    const found = coreStore.qualifications?.find(i => i.id === val)
    if (found) return found.name
  }
  if (field === 'position') {
    const found = coreStore.positions?.find(i => i.id === val)
    if (found) return found.name
  }
  if (field === 'job_title') {
    const found = coreStore.jobTitles?.find(i => i.id === val)
    if (found) return found.name
  }
  if (field === 'force_classification') {
    const found = coreStore.forceTypes?.find(i => i.id === val)
    if (found) return found.name
  }
  if (field === 'current_status') {
    const found = coreStore.statuses?.find(i => i.id === val)
    if (found) return found.name
  }
  if (field === 'pseudo_status_type') {
    if (row.status_classification === 'active_full') return 'قوة عاملة فعلية'
    if (row.status_classification === 'active_part') return 'قوة عاملة غير فعلية'
    if (row.status_classification === 'inactive_temp') return 'قوة غير عاملة مؤقتاً'
    if (row.status_classification === 'inactive_perm') return 'قوة غير عاملة نهائياً'
    return row.status_classification || '—'
  }
  
  return val || '—'
}

const searchFieldsQuery = ref('')

// Flat columns helper for the top compact unified configurator table
const allFlatColumns = computed(() => {
  return [
    ...columns.value.identity,
    ...columns.value.structure,
    ...columns.value.statusAndDecisions
  ]
})

const exportableColumns = computed(() => {
  return allFlatColumns.value.filter(c => c.exportable)
})

const hiddenColumns = computed(() => {
  return allFlatColumns.value.filter(c => !c.exportable)
})

const totalExportable = computed(() => {
  return exportableColumns.value.length
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
    if (enablePartitioning.value) {
      queryParams.mode = exportMode.value
      if (splitBy.value) {
        queryParams.split_by = splitBy.value
      }
    } else {
      queryParams.mode = 'single'
    }

    const response = await api.get('/service-cycle/export/', {
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
  fetchPreviewData()
  initGeographicScope()
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 5px;
  height: 5px;
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
</style>
