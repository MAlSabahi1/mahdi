<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.initial_seeding')" />

    <div class="space-y-6 text-start" dir="rtl">
      <!-- Premium Title & Stepper Banner -->
      <div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-white/[0.03]">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div>
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white">معالج الاستيراد والتأسيس الأولي الذكي</h1>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">قم برفع كشوفات البيانات وفحصها بصرامة وتصحيحها لحظياً قبل اعتمادها.</p>
          </div>
          <!-- Stepper -->
          <div class="flex items-center gap-2">
            <div 
              v-for="step in [1, 2, 3, 4]" 
              :key="step"
              class="flex items-center"
            >
              <div 
                class="flex h-10 w-10 items-center justify-center rounded-full font-bold text-sm transition-all duration-500 ease-out relative"
                :class="[
                  currentStep === step 
                    ? 'bg-gradient-to-br from-blue-500 to-blue-700 text-white shadow-[0_0_15px_rgba(59,130,246,0.5)] ring-4 ring-blue-500/30 scale-110' 
                    : currentStep > step 
                    ? 'bg-gradient-to-br from-emerald-400 to-emerald-600 text-white shadow-md' 
                    : 'bg-gray-100 text-gray-400 dark:bg-gray-800 dark:text-gray-600 border border-gray-200 dark:border-gray-700'
                ]"
              >
                <!-- Pulse effect for active step -->
                <div v-if="currentStep === step" class="absolute inset-0 rounded-full animate-ping bg-blue-400 opacity-20"></div>
                <Check v-if="currentStep > step" class="w-5 h-5 animate-in zoom-in" />
                <span v-else>{{ step }}</span>
              </div>
              <div 
                v-if="step < 4" 
                class="h-1 w-8 sm:w-12 transition-all duration-500 rounded-full overflow-hidden relative bg-gray-200 dark:bg-gray-800 mx-1"
              >
                <div class="absolute inset-y-0 left-0 transition-all duration-700 bg-gradient-to-r from-blue-500 to-emerald-500"
                     :style="`width: ${currentStep > step ? '100%' : '0%'}`"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Seeding Notice & Context -->
        <div class="rounded-xl border border-amber-100 bg-amber-50/50 p-4 dark:border-amber-900/30 dark:bg-amber-950/20 text-xs sm:text-sm text-amber-800 dark:text-amber-300 flex items-start gap-3">
          <AlertTriangle class="w-5 h-5 shrink-0 text-amber-500 mt-0.5" />
          <div>
            <span class="font-bold">تنبيه هام للوضع الإنتاجي:</span>
            هذه الشاشة تمثل بوابة استيراد استثنائية لتأسيس قاعدة بيانات النظام. كافة العمليات البرمجية تخضع للتدقيق الصارم (Strict Validation) لضمان عدم تمرير أي حقول غير معرفة في القواميس المرجعية، وسيتم تصفية الصلاحيات الجغرافية تلقائياً بحسب نطاق المحافظة الخاص بمدير النظام النشط.
          </div>
        </div>
      </div>

      <!-- Main Step Container -->
      <div v-if="isLoading" class="flex flex-col items-center justify-center py-20 bg-white dark:bg-white/[0.03] rounded-2xl border border-gray-200 dark:border-gray-800">
        <Loader2 class="w-12 h-12 text-blue-600 animate-spin" />
        <span class="mt-4 text-sm font-bold text-gray-600 dark:text-gray-400">جاري معالجة البيانات وتحليلها... يرجى الانتظار</span>
      </div>

      <div v-else>
        <!-- STEP 1: UPLOAD FILE -->
        <div v-if="currentStep === 1" class="space-y-6">
          <div class="rounded-2xl border-2 border-dashed border-gray-300 dark:border-gray-700 bg-white dark:bg-white/[0.03] p-12 text-center transition-all duration-300 hover:border-blue-500 hover:bg-blue-50/30 dark:hover:bg-blue-950/10 flex flex-col items-center justify-center group relative overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-tr from-blue-500/5 via-transparent to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
            
            <div class="relative h-20 w-20 flex items-center justify-center mb-6">
              <div class="absolute inset-0 bg-blue-100 dark:bg-blue-900/30 rounded-full animate-ping opacity-20 group-hover:opacity-40 transition-opacity duration-300"></div>
              <div class="h-16 w-16 rounded-2xl bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/40 dark:to-blue-800/40 text-blue-600 dark:text-blue-400 flex items-center justify-center transition-transform duration-500 group-hover:scale-110 group-hover:shadow-lg shadow-blue-500/20 z-10">
                <UploadCloud class="w-8 h-8 group-hover:-translate-y-1 transition-transform duration-300" />
              </div>
            </div>

            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2 relative z-10">قم بسحب وإفلات ملف كشف البيانات هنا</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-8 relative z-10 max-w-md mx-auto">يدعم النظام ملفات Excel فقط (.xlsx, .xls) بحد أقصى 20 ميجابايت، يرجى التأكد من خلو الملف من التنسيقات المعقدة.</p>
            
            <input 
              type="file" 
              accept=".xlsx, .xls" 
              class="absolute inset-0 opacity-0 cursor-pointer z-20" 
              @change="handleFileUpload" 
            />

            <button class="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-bold text-sm px-8 py-3 rounded-xl shadow-[0_4px_14px_0_rgba(37,99,235,0.39)] hover:shadow-[0_6px_20px_rgba(37,99,235,0.23)] hover:-translate-y-0.5 transition-all duration-300 flex items-center gap-2 relative z-10">
              <FileSpreadsheet class="w-4 h-4" />
              تصفح الملفات من الجهاز
            </button>
          </div>

          <div v-if="uploadedFile" class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-white/[0.03] flex items-center justify-between">
            <div class="flex items-center gap-4">
              <div class="h-12 w-12 rounded-xl bg-green-50 dark:bg-green-950/30 text-green-600 dark:text-green-400 flex items-center justify-center">
                <FileSpreadsheet class="w-6 h-6" />
              </div>
              <div>
                <h4 class="font-bold text-gray-900 dark:text-white">{{ uploadedFile.name }}</h4>
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{{ formatBytes(uploadedFile.size) }}</p>
              </div>
            </div>
            <button 
              @click="removeFile" 
              class="text-red-500 hover:bg-red-50 dark:hover:bg-red-950/20 p-2 rounded-xl transition-colors"
            >
              <Trash2 class="w-5 h-5" />
            </button>
          </div>

          <div class="flex justify-end" v-if="uploadedFile">
            <button 
              @click="goToStep2" 
              class="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm px-8 py-3 rounded-xl shadow-md transition-all flex items-center gap-2"
            >
              متابعة لمطابقة الأعمدة
              <ArrowLeft class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- STEP 2: COLUMN MAPPING -->
        <div v-if="currentStep === 2" class="space-y-6">
          <div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-white/[0.03]">
            <div class="flex items-center justify-between border-b border-gray-100 dark:border-gray-800 pb-4 mb-6">
              <div>
                <h3 class="text-lg font-bold text-gray-900 dark:text-white">مطابقة أعمدة الملف مع حقول قاعدة البيانات</h3>
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">قم بتحديد هوية كل عمود من القوائم العلوية ليتطابق مع حقول النظام، أو اختر تجاهل.</p>
              </div>
              <button 
                @click="autoMapColumns" 
                class="text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-950/20 px-4 py-2 rounded-lg font-bold text-xs flex items-center gap-1.5 transition-colors"
              >
                <RefreshCw class="w-3.5 h-3.5" />
                إعادة المطابقة التلقائية
              </button>
            </div>

            <!-- Horizontal Data Mapping Table Grid -->
            <div class="rounded-xl border border-gray-200 bg-white dark:border-gray-800 overflow-hidden shadow-inner">
              <div class="overflow-x-auto max-h-[60vh] custom-scrollbar">
                <table class="w-full text-right border-collapse min-w-full">
                  <thead class="bg-gray-50 dark:bg-gray-900/50 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-10 shadow-sm">
                    <tr>
                      <th class="p-3 border-l border-gray-200 dark:border-gray-800 w-12 text-center text-gray-400 dark:text-gray-500 font-medium">#</th>
                      <th 
                        v-for="(header, idx) in previewData.headers" 
                        :key="idx" 
                        class="p-3 border-l border-gray-200 dark:border-gray-800 min-w-[220px] align-top text-start"
                      >
                        <div class="flex flex-col gap-2">
                          <!-- Original Excel Column Header -->
                          <div class="text-xs font-bold text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 truncate" :title="header">
                            {{ header || `عمود ${idx + 1}` }}
                          </div>

                          <!-- Mapping select -->
                          <div class="relative">
                            <select 
                              v-model="columnMapping[header]"
                              class="w-full text-xs p-2.5 rounded-lg border focus:outline-none focus:ring-2 focus:ring-blue-500/20 font-bold transition-all"
                              :class="[
                                columnMapping[header] 
                                  ? 'bg-blue-50/50 border-blue-200 text-blue-700 dark:bg-blue-950/20 dark:border-blue-900/50 dark:text-blue-300' 
                                  : 'bg-white border-gray-300 dark:bg-gray-800 dark:border-gray-700 text-gray-600 dark:text-gray-400'
                              ]"
                            >
                              <option v-for="col in SYSTEM_COLUMNS" :key="col.id" :value="col.id">
                                {{ col.label }}
                              </option>
                            </select>
                          </div>
                        </div>
                      </th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-100 dark:divide-gray-800 bg-white dark:bg-transparent">
                    <tr 
                      v-for="(row, rowIdx) in previewData.rows" 
                      :key="rowIdx"
                      class="hover:bg-blue-50/10 dark:hover:bg-blue-950/5 transition-colors"
                    >
                      <td class="p-3 text-center text-xs text-gray-400 dark:text-gray-500 font-mono bg-gray-50/50 dark:bg-gray-900/20 border-l border-gray-200 dark:border-gray-800">
                        {{ rowIdx + 1 }}
                      </td>
                      <td 
                        v-for="(header, colIdx) in previewData.headers" 
                        :key="colIdx" 
                        class="p-3 text-xs border-l border-gray-100 dark:border-gray-800 last:border-0"
                        :class="[columnMapping[header] ? 'text-gray-800 dark:text-gray-200' : 'text-gray-400 dark:text-gray-600 italic']"
                      >
                        <div class="truncate max-w-[200px]" :title="String(row[colIdx] || '')">
                          {{ row[colIdx] !== null && row[colIdx] !== undefined ? row[colIdx] : '-' }}
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div class="bg-gray-50 dark:bg-gray-900/30 p-3 text-center text-xs text-gray-500 dark:text-gray-400 border-t border-gray-200 dark:border-gray-800">
                يتم عرض أول {{ previewData.rows.length }} صفوف كمعاينة للمطابقة. سيتم فحص كامل ملف الجداول عند بدء الفحص الصارم.
              </div>
            </div>
          </div>

          <div class="flex items-center justify-between">
            <button 
              @click="currentStep = 1" 
              class="border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 font-bold text-sm px-6 py-3 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-900 transition-all flex items-center gap-2"
            >
              <ArrowRight class="w-4 h-4" />
              السابق
            </button>
            
            <button 
              @click="validateFileContent" 
              class="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm px-8 py-3 rounded-xl shadow-md transition-all flex items-center gap-2"
            >
              بدء الفحص الصارم
              <ArrowLeft class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- STEP 3: VALIDATION GRID -->
        <div v-if="currentStep === 3" class="space-y-6">
          
          <!-- Summary Cards Banner (Premium Redesign) -->
          <div class="grid gap-4 sm:grid-cols-4">
            <!-- Total Rows -->
            <div class="relative overflow-hidden rounded-2xl border border-blue-100 bg-gradient-to-br from-blue-50/40 to-indigo-50/10 p-5 shadow-sm dark:border-blue-900/40 dark:from-blue-950/25 dark:to-indigo-950/5 group hover:shadow-md transition-all duration-300">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-blue-600 dark:text-blue-400 tracking-wide uppercase">إجمالي السجلات</span>
                <div class="p-2 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 group-hover:scale-110 transition-transform duration-300">
                  <Layers class="w-5 h-5" />
                </div>
              </div>
              <h3 class="text-3xl font-extrabold text-gray-900 dark:text-white mt-3 leading-none">{{ validationResult.total_rows }}</h3>
              <p class="text-[10px] text-gray-400 dark:text-gray-500 mt-2">سجلاً تم تحليلها من ملف الإكسل</p>
            </div>
            
            <!-- Valid Rows -->
            <div class="relative overflow-hidden rounded-2xl border border-emerald-100 bg-gradient-to-br from-emerald-50/40 to-green-50/10 p-5 shadow-sm dark:border-emerald-900/40 dark:from-emerald-950/20 dark:to-green-950/5 group hover:shadow-md transition-all duration-300">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-emerald-600 dark:text-emerald-400 tracking-wide uppercase">السجلات السليمة</span>
                <div class="p-2 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 group-hover:scale-110 transition-transform duration-300">
                  <CheckSquare class="w-5 h-5" />
                </div>
              </div>
              <h3 class="text-3xl font-extrabold text-emerald-600 dark:text-emerald-400 mt-3 leading-none">{{ validationResult.valid_rows }}</h3>
              <p class="text-[10px] text-emerald-600/80 dark:text-emerald-500 mt-2">جاهزة للاعتماد النهائي مباشرة</p>
            </div>

            <!-- Erroneous Rows -->
            <div class="relative overflow-hidden rounded-2xl border border-rose-100 bg-gradient-to-br from-rose-50/40 to-red-50/10 p-5 shadow-sm dark:border-rose-900/40 dark:from-rose-950/20 dark:to-red-950/5 group hover:shadow-md transition-all duration-300">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-rose-600 dark:text-rose-400 tracking-wide uppercase">سجلات بها أخطاء</span>
                <div class="p-2 rounded-xl bg-rose-500/10 text-rose-600 dark:text-rose-400 group-hover:scale-110 transition-transform duration-300" :class="{'animate-pulse': (validationResult.errors || []).length > 0}">
                  <ShieldAlert class="w-5 h-5" />
                </div>
              </div>
              <h3 class="text-3xl font-extrabold text-rose-600 dark:text-rose-400 mt-3 leading-none">{{ (validationResult.errors || []).length }}</h3>
              <p class="text-[10px] text-rose-600/80 dark:text-rose-500 mt-2">تحتاج إلى مراجعة وتعديل يدوي</p>
            </div>

            <!-- Total Errors -->
            <div class="relative overflow-hidden rounded-2xl border border-amber-100 bg-gradient-to-br from-amber-50/40 to-orange-50/10 p-5 shadow-sm dark:border-amber-900/40 dark:from-amber-950/20 dark:to-orange-950/5 group hover:shadow-md transition-all duration-300">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-amber-600 dark:text-amber-400 tracking-wide uppercase">إجمالي الأخطاء</span>
                <div class="p-2 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400 group-hover:scale-110 transition-transform duration-300">
                  <AlertTriangle class="w-5 h-5" />
                </div>
              </div>
              <h3 class="text-3xl font-extrabold text-amber-600 dark:text-amber-400 mt-3 leading-none">{{ validationResult.error_count }}</h3>
              <p class="text-[10px] text-amber-600/80 dark:text-amber-500 mt-2">حقول غير متطابقة أو قيم غير معرّفة</p>
            </div>
          </div>

          <!-- Premium Action Toolbar & Control Hub -->
          <div class="rounded-2xl border border-gray-200 bg-white/70 dark:bg-white/[0.02] backdrop-blur-md p-4 shadow-sm dark:border-gray-800 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <!-- Left Side: Status Toggles & Global Search -->
            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 flex-1 max-w-2xl">
              <!-- Grid Toggle -->
              <div class="flex items-center bg-gray-100 dark:bg-gray-800 p-1 rounded-xl shrink-0">
                <button 
                  @click="showErrorsOnly = false; currentPage = 1"
                  class="px-4 py-1.5 rounded-lg text-xs font-bold transition-all duration-200 flex items-center gap-1.5"
                  :class="[!showErrorsOnly ? 'bg-white dark:bg-gray-700 text-blue-600 dark:text-white shadow-sm' : 'text-gray-600 dark:text-gray-400 hover:text-gray-900']"
                >
                  <Database class="w-3.5 h-3.5" />
                  الكل ({{ allRowsData.length }})
                </button>
                <button 
                  @click="showErrorsOnly = true; currentPage = 1"
                  class="px-4 py-1.5 rounded-lg text-xs font-bold transition-all duration-200 flex items-center gap-1.5"
                  :class="[showErrorsOnly ? 'bg-red-500 text-white shadow-sm' : 'text-red-500 hover:bg-red-500/5']"
                >
                  <ShieldAlert class="w-3.5 h-3.5" />
                  أخطاء فقط ({{ (validationResult.errors || []).length }})
                </button>
              </div>

              <!-- Global Search Input -->
              <div class="relative flex-1">
                <span class="absolute inset-y-0 right-3 flex items-center text-gray-400">
                  <Search class="w-4 h-4" />
                </span>
                <input 
                  type="text" 
                  v-model="globalSearchQuery"
                  @input="currentPage = 1"
                  placeholder="بحث سريع برقم عسكري، اسم، رتبة، أو أي قيمة..."
                  class="w-full text-xs pr-9 pl-4 py-2.5 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-gray-950 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 transition-all duration-200 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/10"
                />
                <button 
                  v-if="globalSearchQuery" 
                  @click="globalSearchQuery = ''; currentPage = 1"
                  class="absolute inset-y-0 left-3 flex items-center text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
                >
                  <X class="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            <!-- Right Side: Action Operations -->
            <div class="flex items-center flex-wrap gap-2 shrink-0">
              <button 
                @click="refreshDictionaries"
                class="border border-blue-200 text-blue-700 hover:bg-blue-50/50 dark:border-blue-800/60 dark:text-blue-400 dark:hover:bg-blue-950/20 font-bold text-xs px-4 py-2.5 rounded-xl flex items-center gap-1.5 transition-all"
                title="تحديث قواميس النظام وجداول المراجع من السيرفر"
              >
                <RefreshCw class="w-3.5 h-3.5" />
                تحديث القواميس
              </button>

              <button 
                @click="handleBulkCleanMilitaryNumbers"
                class="border border-emerald-200 text-emerald-700 hover:bg-emerald-50/50 dark:border-emerald-800/60 dark:text-emerald-400 dark:hover:bg-emerald-950/20 font-bold text-xs px-4 py-2.5 rounded-xl flex items-center gap-1.5 transition-all"
                title="تفريغ الرقم العسكري الصحيح إذا طابق الرقم العسكري الأساسي"
              >
                <Trash2 class="w-3.5 h-3.5" />
                تنظيف المتطابقات
              </button>

              <button 
                @click="revalidateEdits"
                class="bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs px-4 py-2.5 rounded-xl flex items-center gap-1.5 shadow-sm hover:shadow transition-all"
              >
                <RefreshCw class="w-3.5 h-3.5" />
                إعادة فحص التعديلات
              </button>

              <div class="relative group">
                <button 
                  @click="commitSeeding"
                  :disabled="(validationResult.errors || []).length > 0"
                  class="font-bold text-xs px-5 py-2.5 rounded-xl flex items-center gap-1.5 transition-all shadow-md"
                  :class="[
                    (validationResult.errors || []).length > 0
                      ? 'bg-gray-100 text-gray-400 dark:bg-gray-800 dark:text-gray-600 cursor-not-allowed border dark:border-gray-800'
                      : 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-emerald-500/10 hover:shadow-lg animate-pulse-subtle'
                  ]"
                >
                  <FileCheck class="w-4 h-4" />
                  حفظ واعتماد التأسيس نهائياً
                </button>
                <div v-if="(validationResult.errors || []).length > 0" class="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-[10px] p-2 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-50 shadow-xl">
                  يجب إصلاح جميع الأخطاء أولاً لتفعيل الاعتماد
                </div>
              </div>
            </div>
          </div>

          <!-- Data Grid & Premium Table -->
          <div class="rounded-2xl border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-white/[0.02] overflow-hidden flex flex-col">
            <div class="overflow-x-auto max-w-full custom-scrollbar">
              <table class="w-full text-right border-collapse min-w-[2100px]">
                <thead class="bg-gray-50/80 dark:bg-gray-900/50 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-20 backdrop-blur-md">
                  <tr>
                    <!-- Row number header -->
                    <th class="p-4 text-center font-bold text-xs w-16 border-l border-b border-gray-200 dark:border-gray-800 text-gray-500">رقم الصف</th>
                    
                    <!-- Column Headers -->
                    <th 
                      v-for="col in errorColumns" 
                      :key="col"
                      class="p-3 font-bold text-xs border-l border-b border-gray-200 dark:border-gray-800 group hover:bg-gray-100/50 dark:hover:bg-gray-800/30 transition-colors relative min-w-[230px]"
                    >
                      <div class="flex flex-col gap-2">
                        <div class="flex items-center justify-between gap-1.5 text-gray-700 dark:text-gray-300">
                          <span class="truncate" :title="col">{{ col }}</span>
                          <!-- Bulk change trigger -->
                          <button 
                            @click="openBulkChange(col)"
                            class="text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 opacity-0 group-hover:opacity-100 transition-all duration-200"
                            title="تعديل هذا العمود لجميع السجلات دفعة واحدة"
                          >
                            <Copy class="w-3.5 h-3.5" />
                          </button>
                        </div>
                        
                        <div class="relative flex items-center">
                          <button 
                            @click.stop="openFilterCol = openFilterCol === col ? null : col"
                            class="w-full text-[11px] p-1.5 px-2.5 rounded-lg border focus:outline-none flex justify-between items-center transition-all duration-200 font-semibold"
                            :class="[
                              columnFilters[col]?.length > 0
                                ? 'bg-blue-600 border-blue-600 text-white shadow-sm hover:bg-blue-700'
                                : 'bg-gray-50 dark:bg-gray-900 border-gray-200 dark:border-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
                            ]"
                          >
                            <span class="truncate">
                              {{ columnFilters[col]?.length > 0 ? `مفلتر (${columnFilters[col].length})` : 'تصفية (الكل)' }}
                            </span>
                            <Filter class="w-3 h-3 ml-1 shrink-0" />
                          </button>
                          
                          <!-- Multi-Select Popover/Dropdown Menu (With click.stop and values search) -->
                          <div 
                            v-if="openFilterCol === col"
                            @click.stop
                            class="absolute top-full mt-1.5 right-0 w-[260px] bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 shadow-2xl rounded-2xl z-50 max-h-80 flex flex-col overflow-hidden text-right animate-fade-in"
                          >
                            <!-- Popover Header -->
                            <div class="p-3 bg-gray-50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center sticky top-0 z-10">
                              <span class="text-xs font-extrabold text-gray-800 dark:text-gray-200">خيارات التصفية</span>
                              <button 
                                @click="columnFilters[col] = []; currentPage = 1; openFilterCol = null"
                                class="text-[10px] font-bold text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/20 px-2 py-1 rounded-lg transition-colors"
                              >
                                إعادة تعيين
                              </button>
                            </div>
                            
                            <!-- Search inside filter popover -->
                            <div class="p-2 border-b border-gray-100 dark:border-gray-800/50 bg-white dark:bg-gray-900">
                              <div class="relative">
                                <span class="absolute inset-y-0 right-2.5 flex items-center text-gray-400">
                                  <Search class="w-3 h-3" />
                                </span>
                                <input 
                                  type="text" 
                                  v-model="filterSearchQueries[col]"
                                  placeholder="بحث في القيم المتاحة..."
                                  class="w-full text-[10px] pr-7 pl-2 py-1.5 rounded-lg border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none focus:border-blue-500"
                                />
                              </div>
                            </div>
                            
                            <!-- Scrollable Options List -->
                            <div class="overflow-y-auto p-2 flex flex-col gap-0.5 text-[11px] text-gray-700 dark:text-gray-300 custom-scrollbar">
                              <!-- System Filters -->
                              <label class="flex items-center gap-2.5 p-2 hover:bg-gray-50 dark:hover:bg-gray-800/40 rounded-lg cursor-pointer transition-colors">
                                <input 
                                  type="checkbox" 
                                  class="rounded text-blue-600 focus:ring-blue-500/20 w-3.5 h-3.5 border-gray-300 dark:border-gray-700 dark:bg-gray-800"
                                  :checked="columnFilters[col]?.includes('__errors__') || false"
                                  @change="(e) => {
                                    const current = columnFilters[col] || []
                                    columnFilters[col] = (e.target as HTMLInputElement).checked ? [...current, '__errors__'] : current.filter(x => x !== '__errors__')
                                    currentPage = 1
                                  }"
                                />
                                <span class="font-bold text-red-600 dark:text-red-400 flex items-center gap-1">
                                  <AlertTriangle class="w-3.5 h-3.5 shrink-0" />
                                  الأخطاء ({{ getColumnStats(col).errorsCount }})
                                </span>
                              </label>
                              
                              <label class="flex items-center gap-2.5 p-2 hover:bg-gray-50 dark:hover:bg-gray-800/40 rounded-lg cursor-pointer transition-colors">
                                <input 
                                  type="checkbox" 
                                  class="rounded text-blue-600 focus:ring-blue-500/20 w-3.5 h-3.5 border-gray-300 dark:border-gray-700 dark:bg-gray-800"
                                  :checked="columnFilters[col]?.includes('__valid__') || false"
                                  @change="(e) => {
                                    const current = columnFilters[col] || []
                                    columnFilters[col] = (e.target as HTMLInputElement).checked ? [...current, '__valid__'] : current.filter(x => x !== '__valid__')
                                    currentPage = 1
                                  }"
                                />
                                <span class="font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                                  <CheckCircle2 class="w-3.5 h-3.5 shrink-0" />
                                  الصحيحة ({{ getColumnStats(col).validCount }})
                                </span>
                              </label>

                              <label class="flex items-center gap-2.5 p-2 hover:bg-gray-50 dark:hover:bg-gray-800/40 rounded-lg cursor-pointer transition-colors">
                                <input 
                                  type="checkbox" 
                                  class="rounded text-blue-600 focus:ring-blue-500/20 w-3.5 h-3.5 border-gray-300 dark:border-gray-700 dark:bg-gray-800"
                                  :checked="columnFilters[col]?.includes('__empty__') || false"
                                  @change="(e) => {
                                    const current = columnFilters[col] || []
                                    columnFilters[col] = (e.target as HTMLInputElement).checked ? [...current, '__empty__'] : current.filter(x => x !== '__empty__')
                                    currentPage = 1
                                  }"
                                />
                                <span class="font-bold text-gray-500 flex items-center gap-1">
                                  <X class="w-3.5 h-3.5 shrink-0" />
                                  فارغة ({{ getColumnStats(col).emptyCount }})
                                </span>
                              </label>

                              <label class="flex items-center gap-2.5 p-2 hover:bg-gray-50 dark:hover:bg-gray-800/40 rounded-lg cursor-pointer transition-colors">
                                <input 
                                  type="checkbox" 
                                  class="rounded text-blue-600 focus:ring-blue-500/20 w-3.5 h-3.5 border-gray-300 dark:border-gray-700 dark:bg-gray-800"
                                  :checked="columnFilters[col]?.includes('__has_value__') || false"
                                  @change="(e) => {
                                    const current = columnFilters[col] || []
                                    columnFilters[col] = (e.target as HTMLInputElement).checked ? [...current, '__has_value__'] : current.filter(x => x !== '__has_value__')
                                    currentPage = 1
                                  }"
                                />
                                <span class="font-bold text-blue-600 dark:text-blue-400 flex items-center gap-1">
                                  <Database class="w-3.5 h-3.5 shrink-0" />
                                  معبأة ({{ getColumnStats(col).hasValueCount }})
                                </span>
                              </label>
                              
                              <!-- Military correction matches if valid column -->
                              <template v-if="col === 'الرقم العسكري الصحيح'">
                                <label class="flex items-center gap-2.5 p-2 hover:bg-gray-50 dark:hover:bg-gray-800/40 rounded-lg cursor-pointer transition-colors">
                                  <input 
                                    type="checkbox" 
                                    class="rounded text-blue-600 focus:ring-blue-500/20 w-3.5 h-3.5 border-gray-300 dark:border-gray-700 dark:bg-gray-800"
                                    :checked="columnFilters[col]?.includes('__match_mil__') || false"
                                    @change="(e) => {
                                      const current = columnFilters[col] || []
                                      columnFilters[col] = (e.target as HTMLInputElement).checked ? [...current, '__match_mil__'] : current.filter(x => x !== '__match_mil__')
                                      currentPage = 1
                                    }"
                                  />
                                  <span class="font-bold text-green-600 dark:text-green-400 flex items-center gap-1">
                                    <Check class="w-3.5 h-3.5 shrink-0" />
                                    مطابق للأساسي ({{ getColumnStats(col).matchCount }})
                                  </span>
                                </label>
                                
                                <label class="flex items-center gap-2.5 p-2 hover:bg-gray-50 dark:hover:bg-gray-800/40 rounded-lg cursor-pointer transition-colors">
                                  <input 
                                    type="checkbox" 
                                    class="rounded text-blue-600 focus:ring-blue-500/20 w-3.5 h-3.5 border-gray-300 dark:border-gray-700 dark:bg-gray-800"
                                    :checked="columnFilters[col]?.includes('__diff_mil__') || false"
                                    @change="(e) => {
                                      const current = columnFilters[col] || []
                                      columnFilters[col] = (e.target as HTMLInputElement).checked ? [...current, '__diff_mil__'] : current.filter(x => x !== '__diff_mil__')
                                      currentPage = 1
                                    }"
                                  />
                                  <span class="font-bold text-red-600 dark:text-red-400 flex items-center gap-1">
                                    <AlertTriangle class="w-3.5 h-3.5 shrink-0" />
                                    مختلف عن الأساسي ({{ getColumnStats(col).diffCount }})
                                  </span>
                                </label>
                              </template>
                              
                              <div class="my-1.5 border-t border-gray-100 dark:border-gray-800/60"></div>
                              <div class="text-[9px] text-gray-400 dark:text-gray-500 mb-1 px-1 font-bold">القيم المكتشفة:</div>
                              
                              <!-- Distinct Values counts -->
                              <label 
                                v-for="[v, count] in getFilteredValueCounts(col)"
                                :key="v"
                                class="flex items-center gap-2 p-2 hover:bg-gray-50 dark:hover:bg-gray-800/40 rounded-lg cursor-pointer transition-colors"
                              >
                                <input 
                                  type="checkbox" 
                                  class="rounded text-blue-600 focus:ring-blue-500/20 w-3.5 h-3.5 border-gray-300 dark:border-gray-700 dark:bg-gray-800"
                                  :checked="columnFilters[col]?.includes(v) || false"
                                  @change="(e) => {
                                    const current = columnFilters[col] || []
                                    columnFilters[col] = (e.target as HTMLInputElement).checked ? [...current, v] : current.filter(x => x !== v)
                                    currentPage = 1
                                  }"
                                />
                                <span class="truncate max-w-[180px]" :title="v">
                                  {{ v || '(فارغ)' }}
                                  <span class="text-gray-400 dark:text-gray-500 font-normal">({{ count }})</span>
                                </span>
                              </label>
                              
                              <div v-if="getFilteredValueCounts(col).length === 0" class="text-center py-4 text-gray-400 dark:text-gray-500 text-[10px]">
                                لا توجد قيم تطابق البحث
                              </div>
                            </div>
                            
                            <!-- Popover Footer -->
                            <div class="p-2 border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-850 flex justify-center">
                              <button 
                                @click.stop="openFilterCol = null"
                                class="text-xs bg-blue-600 text-white w-full py-1.5 rounded-xl font-bold hover:bg-blue-700 transition-colors shadow-sm"
                              >
                                تطبيق وإغلاق
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
                  <tr 
                    v-for="row in paginatedRows" 
                    :key="row.rowIdx"
                    class="hover:bg-gray-50/50 dark:hover:bg-gray-800/10 transition-colors duration-150"
                    :class="[row.err ? 'bg-red-50/5 dark:bg-red-950/2' : '']"
                  >
                    <!-- Row Number cell -->
                    <td class="p-3 text-center border-l border-b border-gray-200 dark:border-gray-800 bg-gray-50/30 dark:bg-gray-900/10 font-mono text-xs font-bold shrink-0">
                      <span :class="[row.err ? 'text-red-500' : 'text-gray-500 dark:text-gray-400']">
                        {{ row.rowIdx + 2 }}
                      </span>
                    </td>

                    <!-- Values Cells -->
                    <td 
                      v-for="col in errorColumns" 
                      :key="col"
                      class="p-2 border-l border-b border-gray-200 dark:border-gray-800 align-top transition-colors duration-150"
                      :class="[getCellError(row, col) ? 'bg-red-50/15 dark:bg-red-950/5' : '']"
                    >
                      <div class="relative min-w-[190px]">
                        <!-- Render dynamic Select dropdowns based on field type -->
                        <select 
                          v-if="hasDropdownOptions(col)"
                          v-model="row.rowData[col]"
                          @change="handleCellChange(row.rowIdx, col, row.rowData[col])"
                          class="w-full text-xs p-2 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-gray-950 dark:text-gray-100 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500/20 cursor-pointer hover:border-gray-300 dark:hover:border-gray-700 focus:border-blue-500 focus:bg-white dark:focus:bg-gray-950"
                          :class="[getCellError(row, col) ? 'border-red-300 dark:border-red-900/60 bg-red-50/20 dark:bg-red-950/10 text-red-950 dark:text-red-200' : '']"
                        >
                          <option value="">-- اختر القيمة --</option>
                          <option 
                            v-if="isOptionUnknown(row.rowData[col], col)"
                            :value="row.rowData[col]"
                            class="text-red-600 dark:text-red-400 font-bold bg-red-50 dark:bg-red-950/30"
                          >
                            [غير معرّف]: {{ row.rowData[col] }}
                          </option>
                          
                           <!-- Groups for CD, Branches, Police -->
                           <template v-if="col === 'جهة_العمل' || col === 'الإدارة_السرية'">
                             <optgroup label="الإدارات المركزية">
                               <option v-for="opt in getFilteredCDs(row.rowData)" :key="opt.id" :value="opt.name">{{ opt.name }}</option>
                             </optgroup>
                             <optgroup label="الفروع">
                               <option v-for="opt in getFilteredBranches(row.rowData)" :key="opt.id" :value="opt.name">{{ opt.name }}</option>
                             </optgroup>
                             <optgroup label="شرطة المديرية">
                               <option v-for="opt in getFilteredDistrictPolice(row.rowData)" :key="opt.id" :value="opt.name">{{ opt.name }}</option>
                             </optgroup>
                           </template>
                          
                          <!-- Standard Options -->
                          <template v-else>
                            <option 
                              v-for="opt in getDropdownOptions(col, row.rowData)" 
                              :key="opt.id" 
                              :value="opt.name"
                            >
                              {{ opt.name }}
                            </option>
                          </template>
                        </select>

                        <!-- Render dynamic Date picker -->
                        <input 
                          v-else-if="isDateColumn(col)"
                          type="date"
                          v-model="row.rowData[col]"
                          @change="handleCellChange(row.rowIdx, col, row.rowData[col])"
                          class="w-full text-xs p-2 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-gray-950 dark:text-gray-100 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500/20 hover:border-gray-300 dark:hover:border-gray-700 focus:border-blue-500"
                          :class="[getCellError(row, col) ? 'border-red-300 dark:border-red-900/60 bg-red-50/20 dark:bg-red-950/10 text-red-950 dark:text-red-200' : '']"
                        />

                        <!-- Fallback normal text input -->
                        <input 
                          v-else
                          type="text"
                          v-model="row.rowData[col]"
                          @blur="handleCellChange(row.rowIdx, col, row.rowData[col])"
                          class="w-full text-xs p-2 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-gray-950 dark:text-gray-100 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500/20 hover:border-gray-300 dark:hover:border-gray-700 focus:border-blue-500"
                          :class="[getCellError(row, col) ? 'border-red-300 dark:border-red-900/60 bg-red-50/20 dark:bg-red-950/10 text-red-950 dark:text-red-200 font-semibold' : '']"
                        />

                        <!-- Error alert badge & quick-fix recommendations -->
                        <div v-if="getCellError(row, col)" class="mt-1.5 p-2 rounded-xl bg-red-50/80 dark:bg-red-950/20 border border-red-100/50 dark:border-red-950/40 flex flex-col gap-1.5 shadow-sm">
                          <span class="text-[10px] font-bold text-red-600 dark:text-red-400 flex items-start gap-1 leading-normal">
                            <AlertTriangle class="w-3.5 h-3.5 shrink-0 mt-0.5" />
                            {{ getCellError(row, col).message }}
                          </span>
                          
                          <!-- Quick Fix operations -->
                          <div v-if="col === 'الرقم العسكري الصحيح' && getCellError(row, col).message.includes('يوجد اختلاف')" class="flex gap-1 border-t border-red-100/30 pt-1 mt-0.5">
                            <button 
                              @click="applyQuickFix(row.rowIdx, 'الرقم العسكري', row.rowData['الرقم العسكري الصحيح'], 'الرقم العسكري الصحيح', '')"
                              class="bg-emerald-600 hover:bg-emerald-700 text-white px-2 py-0.5 rounded-lg text-[9px] font-bold transition-colors"
                            >
                              اعتماد وتصحيح
                            </button>
                            <button 
                              @click="applyQuickFix(row.rowIdx, 'الرقم العسكري الصحيح', '', null, null)"
                              class="bg-gray-200 hover:bg-gray-300 text-gray-800 dark:bg-gray-800 dark:hover:bg-gray-700 dark:text-gray-300 px-2 py-0.5 rounded-lg text-[9px] font-semibold transition-colors"
                            >
                              تجاهل
                            </button>
                          </div>
                        </div>
                      </div>
                    </td>
                  </tr>
                  
                  <!-- Empty search state -->
                  <tr v-if="paginatedRows.length === 0">
                    <td :colspan="errorColumns.length + 1" class="text-center py-12 text-gray-500 dark:text-gray-400 bg-gray-50/20 dark:bg-gray-900/5">
                      <div class="max-w-md mx-auto flex flex-col items-center gap-3">
                        <Database class="w-10 h-10 text-gray-300 dark:text-gray-700" />
                        <h4 class="font-extrabold text-sm text-gray-700 dark:text-gray-300">لا توجد سجلات تطابق عوامل التصفية الحالية</h4>
                        <p class="text-xs text-gray-400">جرب البحث بكلمات مختلفة أو إزالة الفلاتر النشطة من عناوين الأعمدة.</p>
                        <button 
                          v-if="globalSearchQuery || Object.values(columnFilters).some(v => v.length > 0)"
                          @click="globalSearchQuery = ''; columnFilters = {}; currentPage = 1"
                          class="mt-2 text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline"
                        >
                          إلغاء كافة الفلاتر والبحث
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Pagination Footer Controls (Premium Redesign) -->
            <div v-if="totalPages > 1" class="flex flex-col sm:flex-row items-center justify-between px-6 py-4 bg-gray-50/80 dark:bg-gray-900/20 border-t border-gray-150 dark:border-gray-800 gap-4">
              <span class="text-xs text-gray-500 dark:text-gray-400">
                عرض الصفوف من <span class="font-bold text-gray-900 dark:text-white">{{ (currentPage - 1) * itemsPerPage + 1 }}</span> إلى <span class="font-bold text-gray-900 dark:text-white">{{ Math.min(currentPage * itemsPerPage, filteredRowsCount) }}</span> من أصل <span class="font-bold text-gray-900 dark:text-white">{{ filteredRowsCount }}</span> سجل
              </span>
              <div class="flex items-center gap-1.5">
                <button 
                  @click="currentPage = 1" 
                  :disabled="currentPage === 1"
                  class="p-2 border border-gray-200 dark:border-gray-850 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 disabled:opacity-40 transition-colors"
                >
                  <ChevronsRight class="w-4 h-4 text-gray-600 dark:text-gray-400" />
                </button>
                <button 
                  @click="currentPage--" 
                  :disabled="currentPage === 1"
                  class="px-3.5 py-1.5 border border-gray-200 dark:border-gray-850 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 disabled:opacity-40 text-xs font-bold text-gray-600 dark:text-gray-400 transition-colors"
                >
                  السابق
                </button>
                <div class="px-4 text-xs font-bold text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-800 py-1.5 rounded-lg">
                  صفحة {{ currentPage }} من {{ totalPages }}
                </div>
                <button 
                  @click="currentPage++" 
                  :disabled="currentPage === totalPages"
                  class="px-3.5 py-1.5 border border-gray-200 dark:border-gray-850 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 disabled:opacity-40 text-xs font-bold text-gray-600 dark:text-gray-400 transition-colors"
                >
                  التالي
                </button>
                <button 
                  @click="currentPage = totalPages" 
                  :disabled="currentPage === totalPages"
                  class="p-2 border border-gray-200 dark:border-gray-850 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 disabled:opacity-40 transition-colors"
                >
                  <ChevronsLeft class="w-4 h-4 text-gray-600 dark:text-gray-400" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- STEP 4: SUCCESS SUMMARY -->
        <div v-if="currentStep === 4" class="max-w-xl mx-auto text-center space-y-6 py-12">
          <div class="h-20 w-20 rounded-full bg-green-50 dark:bg-green-950/20 text-green-600 dark:text-green-400 flex items-center justify-center mx-auto shadow-lg shadow-green-500/10">
            <CheckCircle2 class="w-12 h-12" />
          </div>

          <div>
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white">تم الاستيراد التأسيسي بنجاح!</h2>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">تمت مزامنة كافة كشوفات البيانات وحفظها في قاعدة بيانات النظام بنجاح تام.</p>
          </div>

          <div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-white/[0.03] space-y-4 text-right">
            <h4 class="font-bold text-gray-900 dark:text-white border-b pb-2">تفاصيل الاستيراد:</h4>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">السجلات الجديدة المنشأة:</span>
              <span class="font-bold text-green-600">{{ successStats.created }} سجل</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">تصحيحات الأسماء المطبقة:</span>
              <span class="font-bold text-amber-600">{{ successStats.name_corrections }} عملية</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">المتغيرات المالية الشهرية المرتبطة:</span>
              <span class="font-bold text-blue-600">{{ successStats.monthly_vars }} قيد</span>
            </div>
          </div>

          <button 
            @click="resetWizard" 
            class="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm px-8 py-3 rounded-xl shadow-md transition-all"
          >
            العودة للواجهة الرئيسية للتأسيس
          </button>
        </div>
      </div>
    </div>

    <!-- BULK EDIT MODAL -->
    <div v-if="bulkEditColumn" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 animate-fade-in">
      <div class="bg-white dark:bg-gray-900 border dark:border-gray-800 rounded-2xl shadow-2xl max-w-md w-full overflow-hidden text-right">
        <div class="flex items-center justify-between p-4 border-b dark:border-gray-800 bg-gray-50 dark:bg-gray-800/50">
          <h3 class="font-bold text-gray-800 dark:text-gray-200">التعديل الجماعي لعمود: {{ bulkEditColumn }}</h3>
          <button @click="closeBulkChange" class="text-gray-400 hover:text-red-500">
            <X class="w-5 h-5" />
          </button>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-2">القيم الخاطئة المرصودة في هذا العمود:</label>
            <div class="max-h-40 overflow-y-auto border border-red-200 dark:border-red-950 rounded-xl p-3 bg-red-50/20 dark:bg-red-950/10 space-y-1.5">
              <div 
                v-for="val in getBulkDistinctErroneousValues()" 
                :key="val"
                class="flex items-center gap-2"
              >
                <input 
                  type="checkbox"
                  v-model="bulkEditTargetValues"
                  :value="val"
                  class="rounded text-blue-600 focus:ring-blue-500 w-4 h-4"
                />
                <span class="text-xs text-red-700 dark:text-red-400">{{ val || '(فارغ)' }}</span>
              </div>
            </div>
          </div>

          <div>
            <label class="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-2">استبدالها بالقيمة المرجعية الصحيحة:</label>
            
            <select 
              v-if="hasDropdownOptions(bulkEditColumn)"
              v-model="bulkEditNewValue"
              class="w-full text-sm p-3 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200"
            >
              <option value="">-- اختر القيمة البديلة --</option>
              
              <!-- Groups for CDs, Branches, Police -->
              <template v-if="bulkEditColumn === 'جهة_العمل' || bulkEditColumn === 'الإدارة_السرية'">
                <optgroup label="الإدارات المركزية">
                  <option v-for="opt in getFilteredCDs(null)" :key="opt.id" :value="opt.name">{{ opt.name }}</option>
                </optgroup>
                <optgroup label="الفروع">
                  <option v-for="opt in getFilteredBranches(null)" :key="opt.id" :value="opt.name">{{ opt.name }}</option>
                </optgroup>
                <optgroup label="شرطة المديرية">
                  <option v-for="opt in getFilteredDistrictPolice(null)" :key="opt.id" :value="opt.name">{{ opt.name }}</option>
                </optgroup>
              </template>
              
              <template v-else>
                <option 
                  v-for="opt in getDropdownOptions(bulkEditColumn, null)" 
                  :key="opt.id" 
                  :value="opt.name"
                >
                  {{ opt.name }}
                </option>
              </template>
            </select>

            <input 
              v-else
              type="text"
              v-model="bulkEditNewValue"
              placeholder="اكتب القيمة الجديدة هنا"
              class="w-full text-sm p-3 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200"
            />
          </div>
        </div>
        <div class="p-4 border-t dark:border-gray-800 flex justify-end gap-2 bg-gray-50 dark:bg-gray-800/20">
          <button 
            @click="closeBulkChange" 
            class="px-4 py-2 border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 text-xs font-bold rounded-lg"
          >
            إلغاء
          </button>
          <button 
            @click="applyBulkChange" 
            :disabled="!bulkEditNewValue || bulkEditTargetValues.length === 0"
            class="px-5 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-100 disabled:text-gray-400 dark:disabled:bg-gray-800 dark:disabled:text-gray-600 text-white text-xs font-bold rounded-lg shadow-md"
          >
            تطبيق الاستبدال الجماعي
          </button>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import Swal from 'sweetalert2'
import { 
  UploadCloud, FileSpreadsheet, CheckCircle2, AlertTriangle, 
  ArrowLeft, ArrowRight, Trash2, RefreshCw, Loader2, Check, 
  Copy, ChevronsRight, ChevronsLeft, X, Filter,
  Layers, Search, CheckSquare, ShieldAlert, FileCheck, Database
} from 'lucide-vue-next'

import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'

import { fetchAllConstants } from '@/services/constantsApi'
import type { ConstantsState, ConstantOption } from '@/services/constantsApi'
import { 
  previewInitialSeed, validateInitialSeed, validateInitialSeedJson, 
  commitInitialSeedJson, type SeedRowError, type PreviewSeedResponse, 
  type ValidateSeedResponse, type CommitSeedResponse 
} from '@/services/initialSeedApi'

const { t } = useI18n()

// Steps State
const currentStep = ref(1)
const isLoading = ref(false)
const uploadedFile = ref<File | null>(null)

// Step 1 Preview Data
const previewData = ref<PreviewSeedResponse>({ headers: [], rows: [] })

// Step 2 Mapping Data
const columnMapping = ref<Record<string, string>>({})

const SYSTEM_COLUMNS = [
  { id: '', label: '-- تجاهل هذا العمود --' },
  { id: '__monthly_variable__', label: '⭐ تعيين كمتغير شهري (Monthly Variable)' },
  { id: 'الرقم العسكري', label: 'الرقم العسكري (أساسي)' },
  { id: 'الرقم العسكري القديم', label: 'الرقم العسكري القديم' },
  { id: 'الرقم العسكري الصحيح', label: 'الرقم العسكري الصحيح' },
  { id: 'الاسم', label: 'الاسم الكامل (أساسي)' },
  { id: 'تصحيح الاسم من واقع البطاقة', label: 'تصحيح الاسم من واقع البطاقة' },
  { id: 'الرتبة', label: 'الرتبة (أساسي)' },
  { id: 'الحالة', label: 'الحالة (التصنيف العام: 4 خيارات)' },
  { id: 'نوع الحالة', label: 'نوع الحالة (الحالة التفصيلية: الجرحى، منزل...)' },
  { id: 'الرقم الوطني', label: 'الرقم الوطني' },
  { id: 'نوع العمل', label: 'نوع العمل (التخصص)' },
  { id: 'الفئة', label: 'الفئة' },
  { id: 'المنصب', label: 'المنصب' },
  { id: 'تصنيف القوة', label: 'تصنيف القوة' },
  { id: 'المؤهل', label: 'المؤهل' },
  { id: 'الوحدة', label: 'الوحدة (الإدارة الأمنية)' },
  { id: 'جهة_العمل', label: 'جهة العمل (الادارة / الفرع)' },
  { id: 'القسم_فرع السرية', label: 'القسم / الفرع' },
  { id: 'التعيينات', label: 'التعيينات' },
  { id: 'تاريخ الميلاد', label: 'تاريخ الميلاد' },
  { id: 'تاريخ الألتحاق', label: 'تاريخ الالتحاق' },
  { id: 'تاريخ صدور القرار', label: 'تاريخ صدور القرار' },
  { id: 'تاريخ التصدور الينا', label: 'تاريخ التصدير إلينا' },
  { id: 'رقم التليفون', label: 'رقم التليفون' },
  { id: 'حالة النفقات', label: 'حالة النفقات' },
  { id: 'الملاحظات', label: 'الملاحظات' }
]

// Step 3 Validation & Editing Grid Data
const validationResult = ref<ValidateSeedResponse>({
  total_rows: 0,
  valid_rows: 0,
  error_count: 0,
  is_valid: false,
  errors: []
})
const allRowsData = ref<Record<string, any>[]>([])
const constants = ref<ConstantsState | null>(null)

// Filtering & Pagination
const showErrorsOnly = ref(false)
const currentPage = ref(1)
const itemsPerPage = ref(15)
const columnFilters = ref<Record<string, string[]>>({})
const openFilterCol = ref<string | null>(null)
const globalSearchQuery = ref('')
const filterSearchQueries = ref<Record<string, string>>({})

function getFilteredValueCounts(col: string) {
  const stats = getColumnStats(col)
  const query = (filterSearchQueries.value[col] || '').trim().toLowerCase()
  if (!query) return stats.valueCounts
  return stats.valueCounts.filter(([v]) => String(v).toLowerCase().includes(query))
}

// Bulk Edit State
const bulkEditColumn = ref<string | null>(null)
const bulkEditTargetValues = ref<string[]>([])
const bulkEditNewValue = ref('')

// Step 4 Statistics
const successStats = ref<CommitSeedResponse>({
  created: 0,
  name_corrections: 0,
  monthly_vars: 0
})

const closePopoverHandler = () => {
  openFilterCol.value = null
}

// Load constants on mount
onMounted(async () => {
  try {
    constants.value = await fetchAllConstants()
  } catch (error) {
    console.error('Failed to load constants dictionaries', error)
  }
  window.addEventListener('click', closePopoverHandler)
})

onUnmounted(() => {
  window.removeEventListener('click', closePopoverHandler)
})

// Bytes Formatting Helper
function formatBytes(bytes: number, decimals = 2) {
  if (!bytes) return '0 Bytes'
  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}

// ----------------------------------------------------
// Step 1: Upload Logic
// ----------------------------------------------------
function handleFileUpload(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    const file = target.files[0]
    if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
      Swal.fire({
        icon: 'error',
        title: 'خطأ في الصيغة',
        text: 'يرجى اختيار ملف Excel صحيح بصيغة .xlsx أو .xls'
      })
      return
    }
    uploadedFile.value = file
  }
}

// Remove current file
function removeFile() {
  uploadedFile.value = null
  previewData.value = { headers: [], rows: [] }
  columnMapping.value = {}
}

async function goToStep2() {
  if (!uploadedFile.value) return
  isLoading.value = true
  try {
    const res = await previewInitialSeed(uploadedFile.value)
    if (res.success && res.data) {
      previewData.value = res.data
      autoMapColumns()
      currentStep.value = 2
    } else {
      Swal.fire({
        icon: 'error',
        title: 'فشل تحليل الملف',
        text: res.message || 'فشل النظام في قراءة ملف الإكسل المرفوع.'
      })
    }
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

// Auto map columns from Excel headers to System Column IDs using name similarity (Fuzzy Matching)
function autoMapColumns() {
  const autoMapping: Record<string, string> = {}
  previewData.value.headers.forEach(header => {
    // Exact match check
    const exactMatch = SYSTEM_COLUMNS.find(c => c.id === header)
    if (exactMatch) {
      autoMapping[header] = exactMatch.id
    } else {
      // Fuzzy matches
      if (header.includes('اسم')) autoMapping[header] = 'الاسم'
      else if (header.includes('رتب')) autoMapping[header] = 'الرتبة'
      else if (header.includes('حالة')) autoMapping[header] = 'الحالة'
      else if (header.includes('رقم عسكري')) autoMapping[header] = 'الرقم العسكري'
      else if (header.includes('وحدة') || header.includes('ادارة')) autoMapping[header] = 'الوحدة'
      else if (header.includes('متغير')) autoMapping[header] = '__monthly_variable__'
      else autoMapping[header] = ''
    }
  })
  columnMapping.value = autoMapping
}

// ----------------------------------------------------
// Step 2: Validation Logic
// ----------------------------------------------------
async function validateFileContent() {
  if (!uploadedFile.value) return
  isLoading.value = true
  
  // Cleanup mapping to remove empty/unmapped entries, and tag monthly variable columns
  const cleanMapping: Record<string, string> = {}
  previewData.value.headers.forEach(k => {
    const val = columnMapping.value[k]
    if (val) {
      if (val === '__monthly_variable__') {
        cleanMapping[k] = k.startsWith('متغير') ? k : `متغير ${k}`
      } else {
        cleanMapping[k] = val
      }
    } else {
      cleanMapping[k] = '__ignore__'
    }
  })

  try {
    const res = await validateInitialSeed(uploadedFile.value, cleanMapping)
    if (res.success && res.data) {
      validationResult.value = res.data
      allRowsData.value = res.data.all_rows || []
      currentPage.value = 1
      currentStep.value = 3
    } else {
      Swal.fire({
        icon: 'error',
        title: 'فشل الفحص',
        text: res.message || 'حدث خطأ أثناء فحص البيانات.'
      })
    }
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

// ----------------------------------------------------
// Step 3: Validation & Inline Editing Grid
// ----------------------------------------------------

const errorColumns = computed(() => {
  const cols = new Set<string>()
  
  if (allRowsData.value && allRowsData.value.length > 0) {
    Object.keys(allRowsData.value[0]).forEach(k => {
      if (!k.startsWith('_')) cols.add(k)
    })
  }

  if (validationResult.value.errors) {
    validationResult.value.errors.forEach(r => {
      if (r.errors) {
        r.errors.forEach((e: any) => cols.add(e.field))
      }
    })
  }

  // Clean up duplicate/legacy columns if their modern equivalent exists
  if (cols.has('القسم_فرع السرية')) cols.delete('القسم')
  if (cols.has('جهة_العمل')) cols.delete('الإدارة_السرية')
  if (cols.has('الاسم')) cols.delete('الاسم الكامل')

  const logicalOrder = [
    'الرقم العسكري', 'الرقم العسكري القديم', 'الرقم العسكري الصحيح', 'الاسم', 'الاسم الكامل', 'تصحيح الاسم من واقع البطاقة', 'الرقم الوطني', 'الرتبة', 
    'الوحدة', 'جهة_العمل', 'الإدارة_السرية', 'القسم', 'القسم_فرع السرية', 'الوحدة_الفرعية',
    'الفئة', 'المنصب', 'نوع العمل',
    'الحالة', 'نوع الحالة', 'المؤهل', 'تصنيف القوة', 'التعيينات', 
    'تاريخ الميلاد', 'تاريخ الألتحاق', 'تاريخ صدور القرار', 'تاريخ التصدور الينا',
    'رقم التليفون', 'حالة النفقات', 'الملاحظات'
  ]

  return Array.from(cols).sort((a, b) => {
    const indexA = logicalOrder.indexOf(a)
    const indexB = logicalOrder.indexOf(b)
    if (indexA === -1 && indexB === -1) return 0
    if (indexA === -1) return 1
    if (indexB === -1) return -1
    return indexA - indexB
  })
})

// Client filter and pagination calculations
const filteredRows = computed(() => {
  const errorMap = new Map<number, SeedRowError>()
  const errors = validationResult.value?.errors || []
  errors.forEach(e => {
    errorMap.set(e.row - 2, e)
  })

  let rows = allRowsData.value.map((row, idx) => ({
    rowIdx: idx,
    rowData: row,
    err: errorMap.get(idx) || null
  }))

  if (showErrorsOnly.value) {
    rows = rows.filter(r => r.err !== null)
  }

  // Global search across all fields
  if (globalSearchQuery.value) {
    const q = globalSearchQuery.value.trim().toLowerCase()
    rows = rows.filter(r => {
      return Object.entries(r.rowData).some(([k, v]) => {
        if (k.startsWith('_')) return false
        return String(v || '').toLowerCase().includes(q)
      })
    })
  }

  // Apply Column Filters (Multi-Select)
  Object.entries(columnFilters.value).forEach(([col, filterValues]) => {
    if (filterValues && filterValues.length > 0) {
      rows = rows.filter(r => {
        const cellVal = String(r.rowData[col] || '')
        const hasErr = r.err?.errors?.some((e: any) => e.field === col) || false
        const isEmpty = !cellVal || cellVal.trim() === ''
        
        return filterValues.some(val => {
          if (val === '__errors__') return hasErr
          if (val === '__valid__') return !hasErr
          if (val === '__empty__') return isEmpty
          if (val === '__has_value__') return !isEmpty
          if (val === '__match_mil__') return !isEmpty && cellVal.trim() === String(r.rowData['الرقم العسكري'] || '').trim()
          if (val === '__diff_mil__') return !isEmpty && cellVal.trim() !== String(r.rowData['الرقم العسكري'] || '').trim()
          return cellVal === val
        })
      })
    }
  })

  return rows
})

const filteredRowsCount = computed(() => {
  return filteredRows.value.length
})

const totalPages = computed(() => {
  return Math.ceil(filteredRowsCount.value / itemsPerPage.value)
})

const paginatedRows = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredRows.value.slice(start, end)
})

// Check if cell has error
function getCellError(row: any, col: string) {
  if (!row.err) return null
  return row.err.errors.find((e: any) => e.field === col) || null
}

// Quick action fix helper
function applyQuickFix(rowIdx: number, targetCol: string, val: any, clearCol: string | null, clearVal: any) {
  allRowsData.value[rowIdx][targetCol] = val
  if (clearCol !== null) {
    allRowsData.value[rowIdx][clearCol] = clearVal
  }
  // Trigger client change validation flow
  handleCellChange(rowIdx, targetCol, val)
}

// Inline change flow
function handleCellChange(rowIdx: number, col: string, value: any) {
  // Update the field
  allRowsData.value[rowIdx][col] = value

  // Cascading dependency clears
  if (col === 'الوحدة') {
    allRowsData.value[rowIdx]['جهة_العمل'] = ''
    allRowsData.value[rowIdx]['القسم'] = ''
    allRowsData.value[rowIdx]['القسم_فرع السرية'] = ''
    allRowsData.value[rowIdx]['الوحدة_الفرعية'] = ''
  } else if (col === 'جهة_العمل' || col === 'الإدارة_السرية') {
    allRowsData.value[rowIdx]['القسم'] = ''
    allRowsData.value[rowIdx]['القسم_فرع السرية'] = ''
    allRowsData.value[rowIdx]['الوحدة_الفرعية'] = ''
  } else if (col === 'القسم' || col === 'القسم_فرع السرية') {
    allRowsData.value[rowIdx]['الوحدة_الفرعية'] = ''
  } else if (col === 'الفئة') {
    allRowsData.value[rowIdx]['المنصب'] = ''
    allRowsData.value[rowIdx]['نوع العمل'] = ''
  } else if (col === 'الحالة') {
    allRowsData.value[rowIdx]['نوع الحالة'] = ''
  }

  // Clean dates if modified
  if (isDateColumn(col) && typeof value === 'string' && value.length > 10) {
    allRowsData.value[rowIdx][col] = value.substring(0, 10)
  }

  // Auto-fill JobTitle based on Position (Business Rule)
  if (col === 'المنصب' && value && constants.value) {
    const normalizeAr = (t: string) => t.replace(/ال/g, '').replace(/\s+/g, '')
    const posNorm = normalizeAr(value)
    const matchingJob = constants.value.jobTitles.find(jt => normalizeAr(jt.name) === posNorm)
    if (matchingJob) {
      allRowsData.value[rowIdx]['نوع العمل'] = matchingJob.name
    }
  }

  // Instant Client-side Error Clearance for modified/cascaded fields
  if (validationResult.value.errors) {
    const clearedFields = [col]
    if (col === 'الوحدة') clearedFields.push('جهة_العمل', 'الإدارة_السرية', 'القسم', 'القسم_فرع السرية', 'الوحدة_الفرعية')
    else if (col === 'جهة_العمل' || col === 'الإدارة_السرية') clearedFields.push('القسم', 'القسم_فرع السرية', 'الوحدة_الفرعية')
    else if (col === 'القسم' || col === 'القسم_فرع السرية') clearedFields.push('الوحدة_الفرعية')
    else if (col === 'الفئة') clearedFields.push('المنصب', 'نوع العمل')
    else if (col === 'الحالة') clearedFields.push('نوع الحالة')

    validationResult.value.errors = validationResult.value.errors.map(r => {
      if (r.row - 2 === rowIdx) {
        return {
          ...r,
          errors: r.errors.filter((e: any) => !clearedFields.includes(e.field))
        }
      }
      return r
    }).filter(r => r.errors.length > 0)
    
    validationResult.value.error_count = validationResult.value.errors.reduce((acc, curr) => acc + curr.errors.length, 0)
    validationResult.value.valid_rows = validationResult.value.total_rows - validationResult.value.errors.length
    validationResult.value.is_valid = validationResult.value.errors.length === 0
  }
}

// Post edited JSON to validation endpoint
async function revalidateEdits() {
  isLoading.value = true
  try {
    const res = await validateInitialSeedJson(allRowsData.value)
    if (res.success && res.data) {
      validationResult.value = res.data
      allRowsData.value = res.data.all_rows || []
      Swal.fire({
        icon: res.data.is_valid ? 'success' : 'warning',
        title: res.data.is_valid ? 'تم الفحص بنجاح' : 'تنبيه الأخطاء',
        text: res.data.is_valid 
          ? 'تم تصحيح كافة الأخطاء والبيانات جاهزة للاعتماد.'
          : `تم إعادة الفحص، يتبقى ${res.data.errors.length} سجل يحتوي على أخطاء يجب إصلاحها.`
      })
    } else {
      Swal.fire({
        icon: 'error',
        title: 'فشل الفحص',
        text: res.message || 'حدث خطأ أثناء فحص البيانات.'
      })
    }
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

// Final Save
async function commitSeeding() {
  isLoading.value = true
  try {
    const res = await commitInitialSeedJson(allRowsData.value)
    if (res.success && res.data) {
      successStats.value = res.data
      currentStep.value = 4
    } else {
      Swal.fire({
        icon: 'error',
        title: 'فشل الاعتماد',
        text: res.message || 'حدث خطأ أثناء اعتماد وحفظ السجلات.'
      })
    }
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

// ----------------------------------------------------
// Dropdowns and Select Helpers
// ----------------------------------------------------
function isDateColumn(col: string) {
  return col.includes('تاريخ')
}

function hasDropdownOptions(col: string) {
  const dropdownCols = [
    'الرتبة', 'المنصب', 'الحالة', 'نوع الحالة', 'المؤهل', 
    'الفئة', 'نوع العمل', 'تصنيف القوة', 'الوحدة', 
    'جهة_العمل', 'الإدارة_السرية', 'القسم', 'القسم_فرع السرية', 
    'الوحدة_الفرعية', 'الموقع الجغرافي', 'حالة النفقات'
  ]
  return dropdownCols.includes(col)
}

function isOptionUnknown(value: any, col: string) {
  if (!value) return false
  if (col === 'الحالة' || col === 'حالة النفقات' || col === 'جهة_العمل' || col === 'الإدارة_السرية') return false
  
  const options = getDropdownOptions(col, null)
  return options.length > 0 && !options.some(opt => opt.name === String(value))
}

function getDropdownOptions(col: string, rowData: any | null): ConstantOption[] {
  if (!constants.value) return []
  
  if (col === 'الرتبة') {
    let list = constants.value.ranks || []
    if (rowData) {
      const milNum = String(rowData['الرقم العسكري'] || rowData['الرقم العسكري القديم'] || '')
      if (milNum.startsWith('60')) {
        const officerRanks = ["ملازم ثاني", "ملازم أول", "نقيب", "رائد", "مقدم", "عقيد", "عميد", "لواء", "فريق", "مشير"]
        list = list.filter(r => officerRanks.includes(r.name))
      } else if (milNum.startsWith('7') || milNum.startsWith('5')) {
        const officerRanks = ["ملازم ثاني", "ملازم أول", "نقيب", "رائد", "مقدم", "عقيد", "عميد", "لواء", "فريق", "مشير"]
        list = list.filter(r => !officerRanks.includes(r.name))
      }
    }
    return list
  }
  
  if (col === 'المنصب') {
    let list = constants.value.positions || []
    if (rowData && rowData['الفئة']) {
      list = list.filter((p: any) => {
        if (!p.allowed_categories || p.allowed_categories.length === 0) return true
        return p.allowed_categories.includes(rowData['الفئة'])
      })
    }
    return list
  }

  if (col === 'الحالة') {
    return [
      { id: 'active_full', name: 'قوة عاملة فعلية' },
      { id: 'active_part', name: 'قوة عاملة غير فعلية' },
      { id: 'inactive_temp', name: 'قوة غير عاملة مؤقتاً' },
      { id: 'inactive_perm', name: 'قوة غير عاملة نهائياً' }
    ]
  }

  if (col === 'نوع الحالة') {
    let list = constants.value.statuses || []
    if (rowData && rowData['الحالة']) {
      list = list.filter((s: any) => !s.classification_display || s.classification_display === rowData['الحالة'])
    }
    return list
  }

  if (col === 'المؤهل') return constants.value.qualifications || []
  if (col === 'الفئة') return constants.value.jobCategories || []
  
  if (col === 'نوع العمل') {
    let list = constants.value.jobTitles || []
    if (rowData && rowData['الفئة']) {
      list = list.filter((jt: any) => jt.category_name === rowData['الفئة'])
    }
    return list
  }

  if (col === 'تصنيف القوة') {
    let list = constants.value.forceTypes || []
    if (rowData && rowData['الرتبة']) {
      const officerRanks = ["ملازم ثاني", "ملازم أول", "نقيب", "رائد", "مقدم", "عقيد", "عميد", "لواء", "فريق", "مشير"]
      const isOfficer = officerRanks.includes(rowData['الرتبة'])
      if (isOfficer) {
        list = list.filter(ft => ft.name.includes('ضباط'))
      } else {
        list = list.filter(ft => ft.name.includes('أفراد') || ft.name.includes('صف'))
      }
    }
    return list
  }

  if (col === 'الوحدة') return constants.value.securityAdmins || []
  if (col === 'القسم' || col === 'القسم_فرع السرية') return getFilteredDivisions(rowData)
  if (col === 'الوحدة_الفرعية') return getFilteredUnits(rowData)
  if (col === 'الموقع الجغرافي') return constants.value.geoDistricts || []
  
  if (col === 'حالة النفقات') {
    return [
      { id: 'has', name: 'لديه نفقات' },
      { id: 'no', name: 'بدون نفقات' }
    ]
  }

  return []
}

// Cascading workplace filters
function getFilteredCDs(rowData: any | null) {
  if (!constants.value) return []
  const selectedUnitStr = rowData ? rowData['الوحدة'] : ''
  const selectedUnitObj = constants.value.securityAdmins.find(sa => sa.name === selectedUnitStr)
  
  return (constants.value.centralDepartments || []).filter(dep => !selectedUnitObj || dep.security_admin === selectedUnitObj.id)
}

function getFilteredBranches(rowData: any | null) {
  if (!constants.value) return []
  const selectedUnitStr = rowData ? rowData['الوحدة'] : ''
  const selectedUnitObj = constants.value.securityAdmins.find(sa => sa.name === selectedUnitStr)
  
  return (constants.value.branches || []).filter(br => !selectedUnitObj || br.security_admin === selectedUnitObj.id)
}

function getFilteredDistrictPolice(rowData: any | null) {
  if (!constants.value) return []
  const selectedUnitStr = rowData ? rowData['الوحدة'] : ''
  const selectedUnitObj = constants.value.securityAdmins.find(sa => sa.name === selectedUnitStr)
  
  return (constants.value.districtPolice || []).filter(dp => !selectedUnitObj || dp.security_admin === selectedUnitObj.id)
}

function getFilteredDivisions(rowData: any | null) {
  if (!constants.value) return []
  if (!rowData) return constants.value.divisions || []
  
  const selectedWorkplaceStr = rowData['جهة_العمل'] || rowData['الإدارة_السرية'] || ''
  const selectedUnitStr = rowData['الوحدة'] || ''
  const selectedUnitObj = constants.value.securityAdmins.find(sa => sa.name === selectedUnitStr)
  
  const cdObj = constants.value.centralDepartments.find(d => d.name === selectedWorkplaceStr && (!selectedUnitObj || d.security_admin === selectedUnitObj.id))
  const brObj = constants.value.branches.find(d => d.name === selectedWorkplaceStr && (!selectedUnitObj || d.security_admin === selectedUnitObj.id))
  const dpObj = constants.value.districtPolice.find(d => d.name === selectedWorkplaceStr && (!selectedUnitObj || d.security_admin === selectedUnitObj.id))
  
  let rawDivisions = constants.value.divisions || []
  if (cdObj) {
    rawDivisions = rawDivisions.filter(div => div.central_department === cdObj.id)
  } else if (brObj) {
    rawDivisions = rawDivisions.filter(div => div.branch === brObj.id)
  } else if (dpObj) {
    rawDivisions = rawDivisions.filter(div => div.district_police === dpObj.id)
  } else if (selectedWorkplaceStr) {
    rawDivisions = []
  }
  
  return rawDivisions
}

function getFilteredUnits(rowData: any | null) {
  if (!constants.value) return []
  if (!rowData) return constants.value.units || []
  
  const selectedDivisionStr = rowData['القسم'] || rowData['القسم_فرع السرية'] || ''
  const divObj = constants.value.divisions.find(d => d.name === selectedDivisionStr)
  
  let rawUnits = constants.value.units || []
  if (divObj) {
    rawUnits = rawUnits.filter(u => u.division === divObj.id)
  }
  
  return rawUnits
}

// ----------------------------------------------------
// Bulk Edit Modal Logic
// ----------------------------------------------------
function openBulkChange(col: string) {
  bulkEditColumn.value = col
  bulkEditTargetValues.value = []
  bulkEditNewValue.value = ''
}

function closeBulkChange() {
  bulkEditColumn.value = null
  bulkEditTargetValues.value = []
  bulkEditNewValue.value = ''
}

function getBulkDistinctErroneousValues() {
  const col = bulkEditColumn.value
  const errors = validationResult.value?.errors || []
  if (!col || errors.length === 0) return []
  
  const values = new Set<string>()
  errors.forEach(errRow => {
    const hasErr = errRow.errors?.some((e: any) => e.field === col) || false
    if (hasErr) {
      const idx = errRow.row - 2
      const val = allRowsData.value[idx]?.[col]
      values.add(String(val || ''))
    }
  })
  return Array.from(values).sort()
}

function applyBulkChange() {
  const col = bulkEditColumn.value
  if (!col || !bulkEditNewValue.value) return
  
  allRowsData.value.forEach((row, idx) => {
    const currentVal = String(row[col] || '')
    if (bulkEditTargetValues.value.includes(currentVal)) {
      // Clear downstream fields
      handleCellChange(idx, col, bulkEditNewValue.value)
    }
  })
  
  closeBulkChange()
  Swal.fire({
    icon: 'success',
    title: 'تم الاستبدال الجماعي',
    text: 'يرجى النقر على زر "إعادة فحص التعديلات" لتحديث تقرير الأخطاء.'
  })
}

// Get column validation stats and values counts for rendering headers' filter lists
function getColumnStats(col: string) {
  const total = allRowsData.value.length
  const errors = validationResult.value?.errors || []
  const errorsCount = errors.filter(r => r.errors?.some((e: any) => e.field === col) || false).length
  const validCount = total - errorsCount
  
  const valueCounts = new Map<string, number>()
  allRowsData.value.forEach(r => {
    const v = String(r[col] || '')
    if (v) {
      valueCounts.set(v, (valueCounts.get(v) || 0) + 1)
    }
  })
  
  const emptyCount = allRowsData.value.filter(r => !String(r[col] || '')).length
  const hasValueCount = total - emptyCount
  
  let matchCount = 0
  let diffCount = 0
  if (col === 'الرقم العسكري الصحيح') {
    allRowsData.value.forEach(r => {
      const v = String(r[col] || '').trim()
      const mil = String(r['الرقم العسكري'] || '').trim()
      if (v && v === mil) matchCount++
      else if (v && v !== mil) diffCount++
    })
  }
  
  // Sort values descending by frequency count
  const sortedValues = Array.from(valueCounts.entries()).sort((a, b) => b[1] - a[1])
  
  return {
    errorsCount,
    validCount,
    valueCounts: sortedValues,
    emptyCount,
    hasValueCount,
    matchCount,
    diffCount
  }
}

// Bulk clean matching correct military numbers
function handleBulkCleanMilitaryNumbers() {
  if (!allRowsData.value) return
  let modifiedCount = 0
  allRowsData.value.forEach((row, idx) => {
    const normalMil = String(row['الرقم العسكري'] || '').trim()
    const correctMil = String(row['الرقم العسكري الصحيح'] || '').trim()
    if (correctMil && normalMil === correctMil) {
      modifiedCount++
      handleCellChange(idx, 'الرقم العسكري الصحيح', '')
    }
  })
  
  if (modifiedCount > 0) {
    Swal.fire({
      icon: 'success',
      title: 'تنظيف المتطابقات',
      text: `تم تنظيف ${modifiedCount} سجلاً متطابقاً بنجاح. يرجى الضغط على زر "إعادة فحص التعديلات" لتحديث تقرير الأخطاء.`
    })
  } else {
    Swal.fire({
      icon: 'info',
      title: 'تنظيف المتطابقات',
      text: 'لم يتم العثور على أي سجلات متطابقة تحتاج إلى تنظيف.'
    })
  }
}

// Fetch fresh constants dictionaries from the server
async function refreshDictionaries() {
  isLoading.value = true
  try {
    constants.value = await fetchAllConstants()
    Swal.fire({
      icon: 'success',
      title: 'تحديث القواميس',
      text: 'تم جلب وتحديث قواميس وجداول مراجع النظام بنجاح.'
    })
  } catch (error) {
    console.error('Failed to load constants dictionaries', error)
    Swal.fire({
      icon: 'error',
      title: 'فشل التحديث',
      text: 'حدث خطأ أثناء محاولة جلب قواميس النظام الحديثة من الخادم.'
    })
  } finally {
    isLoading.value = false
  }
}

// Reset entire flow
function resetWizard() {
  removeFile()
  columnFilters.value = {}
  openFilterCol.value = null
  currentStep.value = 1
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  height: 8px;
  width: 8px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #475569;
}
@keyframes pulse-subtle {
  0%, 100% { transform: scale(1); box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.1), 0 2.5px 4px -1px rgba(16, 185, 129, 0.06); }
  50% { transform: scale(1.02); box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.2), 0 4px 6px -2px rgba(16, 185, 129, 0.1); }
}
.animate-pulse-subtle {
  animation: pulse-subtle 2.5s infinite ease-in-out;
}
</style>
