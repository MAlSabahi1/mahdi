<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="إعداد وتصدير النماذج" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Page Header -->
      <div class="border-b border-gray-200 dark:border-gray-800 pb-5 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 class="text-2xl font-black text-gray-900 dark:text-white flex items-center gap-2">
            <svg class="w-7 h-7 text-brand-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            لوحة إعداد وتصدير النماذج الذكية
          </h1>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1.5 max-w-2xl leading-relaxed">
            منظومة التحكم بحماية حقول البيانات وتوليد نماذج الإدخال المؤتمتة للأفراد. يمكنك تحديد الإدارات والمديريات المستهدفة، وعزل الأعمدة الحساسة بقفل للحماية.
          </p>
        </div>
        
        <!-- Quick Stats -->
        <div class="flex gap-3 bg-gray-50 dark:bg-white/[0.02] p-3 rounded-2xl border border-gray-200 dark:border-gray-800/80">
          <div class="text-center px-4 border-l border-gray-200 dark:border-gray-800">
            <span class="block text-xs font-bold text-gray-400">الحقول المضمنة</span>
            <span class="text-lg font-black text-blue-600 dark:text-blue-400">{{ totalExportable }}</span>
          </div>
          <div class="text-center px-4">
            <span class="block text-xs font-bold text-gray-400">الحقول المقفلة</span>
            <span class="text-lg font-black text-red-600 dark:text-red-400">{{ totalLocked }}</span>
          </div>
        </div>
      </div>

      <!-- Main Layout -->
      <div class="grid gap-6 lg:grid-cols-12">
        
        <!-- Right Column: Smart Filter & Partition Control (Width: 4/12) -->
        <div class="lg:col-span-4 space-y-6">
          
          <!-- Section 1: Grouping/Partitioning -->
          <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800/80 rounded-3xl p-5 shadow-sm space-y-4">
            <h3 class="text-sm font-black text-gray-900 dark:text-white flex items-center gap-2">
              <span class="flex items-center justify-center w-5 h-5 rounded-full bg-brand-50 dark:bg-brand-950/30 text-brand-600 dark:text-brand-400 text-xs font-black">1</span>
              طريقة التصدير والتقسيم
            </h3>
            
            <div class="grid grid-cols-1 gap-2.5">
              <label 
                v-for="opt in splitOptions" 
                :key="opt.value"
                :class="[
                  splitBy === opt.value 
                    ? 'border-brand-500 bg-brand-50/20 dark:bg-brand-950/10' 
                    : 'border-gray-200 dark:border-gray-800 hover:bg-gray-50/50 dark:hover:bg-gray-900/20'
                ]"
                class="flex items-start gap-3 p-3.5 border rounded-2xl cursor-pointer transition-all duration-200"
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
                  <span class="block text-[10px] text-gray-400 mt-0.5 leading-relaxed">{{ opt.description }}</span>
                </div>
              </label>
            </div>
          </div>

          <!-- Section 2: Multi-select Scope Filters -->
          <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800/80 rounded-3xl p-5 shadow-sm space-y-4">
            <h3 class="text-sm font-black text-gray-900 dark:text-white flex items-center gap-2">
              <span class="flex items-center justify-center w-5 h-5 rounded-full bg-brand-50 dark:bg-brand-950/30 text-brand-600 dark:text-brand-400 text-xs font-black">2</span>
              فلاتر النطاق المستهدف
            </h3>

            <!-- Accordion/Tabs for filters -->
            <div class="space-y-4">
              <!-- Security Admins Filter -->
              <div class="border border-gray-150 dark:border-gray-800/60 rounded-2xl overflow-hidden bg-gray-50/30 dark:bg-transparent">
                <div class="flex justify-between items-center p-3 bg-gray-50/80 dark:bg-white/[0.01] border-b border-gray-150 dark:border-gray-800/60">
                  <span class="text-xs font-bold text-gray-800 dark:text-gray-200">إدارات أمن المحافظات / المديريات</span>
                  <div class="flex gap-2">
                    <button @click="selectAllAdmins" class="text-[9px] text-brand-600 hover:underline font-bold">الكل</button>
                    <span class="text-gray-300">|</span>
                    <button @click="clearAllAdmins" class="text-[9px] text-gray-400 hover:underline">مسح</button>
                  </div>
                </div>
                <div class="p-3 space-y-2">
                  <input v-model="searchAdmins" placeholder="بحث سريع..." type="text" class="w-full text-[11px] border border-gray-200 dark:border-gray-850 rounded-lg px-2.5 py-1.5 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-1 focus:ring-brand-500" />
                  <div class="max-h-[140px] overflow-y-auto space-y-1.5 custom-scrollbar pr-1">
                    <label v-for="item in filteredAdmins" :key="item.id" class="flex items-center gap-2 p-1.5 rounded-lg hover:bg-gray-50 dark:hover:bg-white/[0.02] cursor-pointer text-right">
                      <input type="checkbox" :value="item.id" v-model="selectedAdmins" class="h-3.5 w-3.5 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
                      <span class="text-[11px] font-medium text-gray-700 dark:text-gray-300">{{ item.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Central Departments Filter -->
              <div class="border border-gray-150 dark:border-gray-800/60 rounded-2xl overflow-hidden bg-gray-50/30 dark:bg-transparent">
                <div class="flex justify-between items-center p-3 bg-gray-50/80 dark:bg-white/[0.01] border-b border-gray-150 dark:border-gray-800/60">
                  <span class="text-xs font-bold text-gray-800 dark:text-gray-200">الجهات والدوائر المركزية</span>
                  <div class="flex gap-2">
                    <button @click="selectAllDepts" class="text-[9px] text-brand-600 hover:underline font-bold">الكل</button>
                    <span class="text-gray-300">|</span>
                    <button @click="clearAllDepts" class="text-[9px] text-gray-400 hover:underline">مسح</button>
                  </div>
                </div>
                <div class="p-3 space-y-2">
                  <input v-model="searchDepts" placeholder="بحث سريع..." type="text" class="w-full text-[11px] border border-gray-200 dark:border-gray-850 rounded-lg px-2.5 py-1.5 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-1 focus:ring-brand-500" />
                  <div class="max-h-[140px] overflow-y-auto space-y-1.5 custom-scrollbar pr-1">
                    <label v-for="item in filteredDepts" :key="item.id" class="flex items-center gap-2 p-1.5 rounded-lg hover:bg-gray-50 dark:hover:bg-white/[0.02] cursor-pointer text-right">
                      <input type="checkbox" :value="item.id" v-model="selectedDepts" class="h-3.5 w-3.5 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
                      <span class="text-[11px] font-medium text-gray-700 dark:text-gray-300">{{ item.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Branches Filter -->
              <div class="border border-gray-150 dark:border-gray-800/60 rounded-2xl overflow-hidden bg-gray-50/30 dark:bg-transparent">
                <div class="flex justify-between items-center p-3 bg-gray-50/80 dark:bg-white/[0.01] border-b border-gray-150 dark:border-gray-800/60">
                  <span class="text-xs font-bold text-gray-800 dark:text-gray-200">الفروع والمحاور</span>
                  <div class="flex gap-2">
                    <button @click="selectAllBranches" class="text-[9px] text-brand-600 hover:underline font-bold">الكل</button>
                    <span class="text-gray-300">|</span>
                    <button @click="clearAllBranches" class="text-[9px] text-gray-400 hover:underline">مسح</button>
                  </div>
                </div>
                <div class="p-3 space-y-2">
                  <input v-model="searchBranches" placeholder="بحث سريع..." type="text" class="w-full text-[11px] border border-gray-200 dark:border-gray-850 rounded-lg px-2.5 py-1.5 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-1 focus:ring-brand-500" />
                  <div class="max-h-[140px] overflow-y-auto space-y-1.5 custom-scrollbar pr-1">
                    <label v-for="item in filteredBranches" :key="item.id" class="flex items-center gap-2 p-1.5 rounded-lg hover:bg-gray-50 dark:hover:bg-white/[0.02] cursor-pointer text-right">
                      <input type="checkbox" :value="item.id" v-model="selectedBranches" class="h-3.5 w-3.5 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
                      <span class="text-[11px] font-medium text-gray-700 dark:text-gray-300">{{ item.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Statuses Filter -->
              <div class="border border-gray-150 dark:border-gray-800/60 rounded-2xl overflow-hidden bg-gray-50/30 dark:bg-transparent">
                <div class="flex justify-between items-center p-3 bg-gray-50/80 dark:bg-white/[0.01] border-b border-gray-150 dark:border-gray-800/60">
                  <span class="text-xs font-bold text-gray-800 dark:text-gray-200">الحالات الخدمية عسكرياً</span>
                  <div class="flex gap-2">
                    <button @click="selectAllStatuses" class="text-[9px] text-brand-600 hover:underline font-bold">الكل</button>
                    <span class="text-gray-300">|</span>
                    <button @click="clearAllStatuses" class="text-[9px] text-gray-400 hover:underline">مسح</button>
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

            <!-- Trigger Export Action -->
            <div class="pt-3 border-t border-gray-150 dark:border-gray-800">
              <button
                @click="triggerExport"
                :disabled="loading"
                class="w-full bg-brand-600 hover:bg-brand-700 disabled:opacity-50 disabled:cursor-not-allowed text-white text-xs font-black py-3 rounded-2xl transition-all duration-200 cursor-pointer shadow-sm hover:shadow flex items-center justify-center gap-2"
              >
                <span v-if="loading" class="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                <svg v-else class="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                تصدير نموذج الكشف المقفل المعتمد
              </button>
            </div>

          </div>

        </div>

        <!-- Left Column: Lock Column Configurator (Width: 8/12) -->
        <div class="lg:col-span-8 bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800/80 rounded-3xl p-5 shadow-sm space-y-5">
          
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-gray-150 dark:border-gray-800/80 pb-4">
            <div>
              <h3 class="text-sm font-black text-gray-900 dark:text-white">3. مصفوفة تحديد أعمدة التصدير وحمايتها</h3>
              <p class="text-[10px] text-gray-400 mt-1">حدّد الأعمدة المراد تضمينها في الملف، وحالة القفل الخاصة بكل عمود لمنع التعديل العشوائي في الملف المصدّر.</p>
            </div>
            
            <div class="flex items-center gap-3">
              <button @click="resetToDefaultLocks" class="text-[10px] text-brand-600 hover:underline font-bold cursor-pointer">
                إعادة تعيين الافتراضي
              </button>
              <span class="text-gray-300">|</span>
              <button @click="toggleSelectAllFields" class="text-[10px] text-blue-600 hover:underline font-bold cursor-pointer">
                {{ isAllFieldsSelected ? 'إلغاء تحديد حقول التصدير' : 'تحديد جميع حقول التصدير' }}
              </button>
            </div>
          </div>

          <!-- Quick Matrix Search -->
          <div class="relative">
            <input 
              v-model="searchFieldsQuery" 
              placeholder="ابحث عن حقول معينة في مصفوفة الأعمدة المرجعية..." 
              type="text" 
              class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-xl px-4 py-2.5 bg-gray-50/50 dark:bg-gray-900 text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-1 focus:ring-brand-500" 
            />
            <span class="absolute left-3.5 top-3.5 text-gray-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </span>
          </div>

          <!-- Loading state -->
          <div v-if="loading" class="py-16 flex flex-col items-center justify-center gap-3">
            <div class="h-8 w-8 border-4 border-brand-600 border-t-transparent rounded-full animate-spin"></div>
            <p class="text-xs text-gray-400">جاري تحميل مصفوفة الحقول وقواعد البيانات المعتمدة...</p>
          </div>

          <!-- Columns Groups Grid -->
          <div v-else class="space-y-6">
            
            <!-- Table Header Helper -->
            <div class="grid grid-cols-12 gap-2 px-4 py-2 bg-gray-50/60 dark:bg-gray-900/60 rounded-xl text-[10px] font-black text-gray-400">
              <span class="col-span-5 text-right">العمود المرجعي في قاعدة البيانات</span>
              <span class="col-span-4 text-center">حالة التصدير</span>
              <span class="col-span-3 text-center">حماية القفل</span>
            </div>

            <!-- Identity & Personal Info group -->
            <div v-if="filteredGroups.identity.length > 0">
              <h4 class="text-[11px] font-black text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-950/60 px-3 py-2 rounded-xl mb-3 flex items-center gap-2">
                <span class="w-1.5 h-3 bg-brand-500 rounded-full"></span>
                بيانات الهوية والبيانات الشخصية
              </h4>
              <div class="grid grid-cols-1 gap-2.5">
                <div v-for="col in filteredGroups.identity" :key="col.field" class="grid grid-cols-12 gap-2 items-center p-3 rounded-2xl border border-gray-100 dark:border-gray-800 bg-gray-50/10 dark:bg-gray-900/10 hover:bg-gray-50/50 dark:hover:bg-gray-900/20 transition-all duration-200">
                  <div class="col-span-5 text-right">
                    <span class="text-xs font-bold text-gray-800 dark:text-gray-200">{{ col.label }}</span>
                    <span class="block text-[9px] text-gray-450 font-mono mt-1 select-all">{{ col.field }}</span>
                  </div>
                  
                  <div class="col-span-4 flex items-center justify-center gap-3">
                    <span :class="col.exportable ? 'text-blue-600 bg-blue-50 dark:bg-blue-950/20 border-blue-200/50 dark:border-blue-900/30' : 'text-gray-400 bg-gray-50 dark:bg-gray-900/20 border-gray-200 dark:border-gray-800'" class="text-[9px] font-bold px-2 py-0.5 rounded-lg border min-w-[54px] text-center">
                      {{ col.exportable ? 'تصدير' : 'استبعاد' }}
                    </span>
                    <input type="checkbox" v-model="col.exportable" :disabled="col.alwaysExportable" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer" />
                  </div>

                  <div class="col-span-3 flex items-center justify-center gap-3">
                    <span :class="col.locked && col.exportable ? 'text-red-600 bg-red-50 dark:bg-red-950/20 border-red-200/50 dark:border-red-900/30' : 'text-emerald-600 bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200/50 dark:border-emerald-900/30'" class="text-[9px] font-bold px-2 py-0.5 rounded-lg border min-w-[54px] text-center">
                      {{ col.locked && col.exportable ? 'مغلق' : 'مفتوح' }}
                    </span>
                    <input type="checkbox" v-model="col.locked" :disabled="col.alwaysLocked || !col.exportable" class="h-4 w-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Structure group -->
            <div v-if="filteredGroups.structure.length > 0">
              <h4 class="text-[11px] font-black text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-950/60 px-3 py-2 rounded-xl mb-3 flex items-center gap-2">
                <span class="w-1.5 h-3 bg-brand-500 rounded-full"></span>
                الهيكل التنظيمي والوظيفي
              </h4>
              <div class="grid grid-cols-1 gap-2.5">
                <div v-for="col in filteredGroups.structure" :key="col.field" class="grid grid-cols-12 gap-2 items-center p-3 rounded-2xl border border-gray-100 dark:border-gray-800 bg-gray-50/10 dark:bg-gray-900/10 hover:bg-gray-50/50 dark:hover:bg-gray-900/20 transition-all duration-200">
                  <div class="col-span-5 text-right">
                    <span class="text-xs font-bold text-gray-800 dark:text-gray-200">{{ col.label }}</span>
                    <span class="block text-[9px] text-gray-455 font-mono mt-1 select-all">{{ col.field }}</span>
                  </div>
                  
                  <div class="col-span-4 flex items-center justify-center gap-3">
                    <span :class="col.exportable ? 'text-blue-600 bg-blue-50 dark:bg-blue-950/20 border-blue-200/50 dark:border-blue-900/30' : 'text-gray-400 bg-gray-50 dark:bg-gray-900/20 border-gray-200 dark:border-gray-800'" class="text-[9px] font-bold px-2 py-0.5 rounded-lg border min-w-[54px] text-center">
                      {{ col.exportable ? 'تصدير' : 'استبعاد' }}
                    </span>
                    <input type="checkbox" v-model="col.exportable" :disabled="col.alwaysExportable" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer" />
                  </div>

                  <div class="col-span-3 flex items-center justify-center gap-3">
                    <span :class="col.locked && col.exportable ? 'text-red-600 bg-red-50 dark:bg-red-950/20 border-red-200/50 dark:border-red-900/30' : 'text-emerald-600 bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200/50 dark:border-emerald-900/30'" class="text-[9px] font-bold px-2 py-0.5 rounded-lg border min-w-[54px] text-center">
                      {{ col.locked && col.exportable ? 'مغلق' : 'مفتوح' }}
                    </span>
                    <input type="checkbox" v-model="col.locked" :disabled="col.alwaysLocked || !col.exportable" class="h-4 w-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Status and Decisions group -->
            <div v-if="filteredGroups.statusAndDecisions.length > 0">
              <h4 class="text-[11px] font-black text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-950/60 px-3 py-2 rounded-xl mb-3 flex items-center gap-2">
                <span class="w-1.5 h-3 bg-brand-500 rounded-full"></span>
                الحالة الخدمية والقرارات
              </h4>
              <div class="grid grid-cols-1 gap-2.5">
                <div v-for="col in filteredGroups.statusAndDecisions" :key="col.field" class="grid grid-cols-12 gap-2 items-center p-3 rounded-2xl border border-gray-100 dark:border-gray-800 bg-gray-50/10 dark:bg-gray-900/10 hover:bg-gray-50/50 dark:hover:bg-gray-900/20 transition-all duration-200">
                  <div class="col-span-5 text-right">
                    <span class="text-xs font-bold text-gray-800 dark:text-gray-200">{{ col.label }}</span>
                    <span class="block text-[9px] text-gray-455 font-mono mt-1 select-all">{{ col.field }}</span>
                  </div>
                  
                  <div class="col-span-4 flex items-center justify-center gap-3">
                    <span :class="col.exportable ? 'text-blue-600 bg-blue-50 dark:bg-blue-950/20 border-blue-200/50 dark:border-blue-900/30' : 'text-gray-400 bg-gray-50 dark:bg-gray-900/20 border-gray-200 dark:border-gray-800'" class="text-[9px] font-bold px-2 py-0.5 rounded-lg border min-w-[54px] text-center">
                      {{ col.exportable ? 'تصدير' : 'استبعاد' }}
                    </span>
                    <input type="checkbox" v-model="col.exportable" :disabled="col.alwaysExportable" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer" />
                  </div>

                  <div class="col-span-3 flex items-center justify-center gap-3">
                    <span :class="col.locked && col.exportable ? 'text-red-600 bg-red-50 dark:bg-red-950/20 border-red-200/50 dark:border-red-900/30' : 'text-emerald-600 bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200/50 dark:border-emerald-900/30'" class="text-[9px] font-bold px-2 py-0.5 rounded-lg border min-w-[54px] text-center">
                      {{ col.locked && col.exportable ? 'مغلق' : 'مفتوح' }}
                    </span>
                    <input type="checkbox" v-model="col.locked" :disabled="col.alwaysLocked || !col.exportable" class="h-4 w-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500 cursor-pointer" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty Search state -->
            <div v-if="filteredGroups.identity.length === 0 && filteredGroups.structure.length === 0 && filteredGroups.statusAndDecisions.length === 0" class="py-12 text-center text-xs text-gray-400 bg-gray-50/50 dark:bg-white/[0.01] rounded-2xl border border-dashed border-gray-200 dark:border-gray-800">
              لا توجد أعمدة مطابقة لبحثك الحالي.
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
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { useCoreStore } from '@/stores/core'
import api from '@/lib/api'
import Swal from 'sweetalert2'

const coreStore = useCoreStore()
const loading = ref(false)

// Split Options
const splitBy = ref('')
const splitOptions = [
  { value: '', label: 'ورقة عمل موحدة', description: 'تصدير جميع الأفراد في كشف واحد مقفل داخل ورقة العمل الرئيسية.' },
  { value: 'security_admin', label: 'مبوبة حسب إدارة الأمن', description: 'تقسيم كشوفات الأفراد تلقائياً إلى صفحات منفصلة داخل ملف الإكسل (Sheet لكل إدارة أمن).' },
  { value: 'central_department', label: 'مبوبة حسب الإدارة العامة / الجهة', description: 'تقسيم كشوفات الأفراد تلقائياً إلى صفحات منفصلة داخل ملف الإكسل (Sheet لكل إدارة عامة).' },
  { value: 'branch', label: 'مبوبة حسب الفروع والمحاور', description: 'تقسيم كشوفات الأفراد تلقائياً إلى صفحات منفصلة داخل ملف الإكسل (Sheet لكل فرع).' }
]

// Scope Filter Selection
const selectedAdmins = ref<number[]>([])
const selectedDepts = ref<number[]>([])
const selectedBranches = ref<number[]>([])
const selectedStatuses = ref<number[]>([])

// Filter Search Queries
const searchAdmins = ref('')
const searchDepts = ref('')
const searchBranches = ref('')
const searchFieldsQuery = ref('')

// Compute filtered lists
const filteredAdmins = computed(() => {
  return coreStore.securityAdmins.filter(a => a.name.toLowerCase().includes(searchAdmins.value.toLowerCase()))
})
const filteredDepts = computed(() => {
  return coreStore.centralDepartments.filter(d => d.name.toLowerCase().includes(searchDepts.value.toLowerCase()))
})
const filteredBranches = computed(() => {
  return coreStore.branches.filter(b => b.name.toLowerCase().includes(searchBranches.value.toLowerCase()))
})

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

// Filter grid columns dynamically by search field query
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

// Stats computed properties
const totalExportable = computed(() => {
  return Object.values(columns.value).flat().filter(c => c.exportable).length
})

const totalLocked = computed(() => {
  return Object.values(columns.value).flat().filter(c => c.exportable && c.locked).length
})

// Select All Helpers for Filters
function selectAllAdmins() { selectedAdmins.value = coreStore.securityAdmins.map(a => a.id) }
function clearAllAdmins() { selectedAdmins.value = [] }

function selectAllDepts() { selectedDepts.value = coreStore.centralDepartments.map(d => d.id) }
function clearAllDepts() { selectedDepts.value = [] }

function selectAllBranches() { selectedBranches.value = coreStore.branches.map(b => b.id) }
function clearAllBranches() { selectedBranches.value = [] }

function selectAllStatuses() { selectedStatuses.value = coreStore.statuses.map(s => s.id) }
function clearAllStatuses() { selectedStatuses.value = [] }

// Select All Fields Matrix
const isAllFieldsSelected = computed(() => {
  const list = Object.values(columns.value).flat()
  if (list.length === 0) return false
  return list.every(c => c.exportable)
})

function toggleSelectAllFields() {
  const target = !isAllFieldsSelected.value
  Object.values(columns.value).flat().forEach(c => {
    if (!c.alwaysExportable) {
      c.exportable = target
    }
  })
}

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

function resetToDefaultLocks() {
  Object.values(columns.value).flat().forEach(c => {
    c.locked = c.alwaysLocked || ['military_number', 'full_name', 'national_id', 'security_admin', 'current_rank', 'current_status'].includes(c.field)
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

async function triggerExport() {
  try {
    loading.value = true
    
    // Assemble export fields & locked fields
    const exportFields: string[] = []
    const lockedFields: string[] = []
    
    Object.values(columns.value).flat().forEach(c => {
      if (c.exportable) {
        exportFields.push(c.field)
        if (c.locked) {
          lockedFields.push(c.field)
        }
      }
    })

    const response = await api.get('/personnel/export_csv/', {
      params: {
        columns: exportFields.join(','),
        locked_columns: lockedFields.join(','),
        security_admins: selectedAdmins.value.join(','),
        central_departments: selectedDepts.value.join(','),
        branches: selectedBranches.value.join(','),
        statuses: selectedStatuses.value.join(','),
        split_by: splitBy.value || undefined
      },
      responseType: 'blob'
    })

    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const downloadUrl = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = downloadUrl
    a.download = `نماذج_كشوفات_الأفراد_المقننة.xlsx`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(downloadUrl)
    document.body.removeChild(a)

    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: 'تم تصدير النموذج المقفل بنجاح',
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

onMounted(() => {
  if (coreStore.securityAdmins.length === 0) {
    coreStore.fetchAllReferences()
  }
  fetchExportFields()
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
</style>
