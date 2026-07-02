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
                class="flex h-10 w-10 items-center justify-center rounded-full font-bold text-sm transition-all duration-300"
                :class="[
                  currentStep === step 
                    ? 'bg-blue-600 text-white shadow-lg ring-4 ring-blue-500/20' 
                    : currentStep > step 
                    ? 'bg-green-500 text-white' 
                    : 'bg-gray-100 text-gray-400 dark:bg-gray-800 dark:text-gray-600'
                ]"
              >
                <Check v-if="currentStep > step" class="w-5 h-5" />
                <span v-else>{{ step }}</span>
              </div>
              <div 
                v-if="step < 4" 
                class="h-1 w-8 sm:w-12 transition-all duration-300"
                :class="[currentStep > step ? 'bg-green-500' : 'bg-gray-200 dark:bg-gray-800']"
              ></div>
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
          <div class="rounded-2xl border-2 border-dashed border-gray-300 dark:border-gray-700 bg-white dark:bg-white/[0.03] p-12 text-center transition-all hover:border-blue-500 flex flex-col items-center justify-center group relative overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-tr from-blue-50/10 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            
            <div class="h-16 w-16 rounded-2xl bg-blue-50 dark:bg-blue-950/30 text-blue-600 dark:text-blue-400 flex items-center justify-center mb-4 transition-transform group-hover:scale-110">
              <UploadCloud class="w-8 h-8" />
            </div>

            <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">قم بسحب وإفلات ملف كشف البيانات هنا</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">يدعم النظام ملفات Excel فقط (.xlsx, .xls) بحد أقصى 20 ميجابايت</p>
            
            <input 
              type="file" 
              accept=".xlsx, .xls" 
              class="absolute inset-0 opacity-0 cursor-pointer" 
              @change="handleFileUpload" 
            />

            <button class="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm px-6 py-2.5 rounded-xl shadow-md transition-all flex items-center gap-2">
              <FileSpreadsheet class="w-4 h-4" />
              تصفح الملفات
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
          <!-- Summary Cards banner -->
          <div class="grid gap-4 sm:grid-cols-4">
            <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-white/[0.03]">
              <span class="text-xs text-gray-500 dark:text-gray-400 font-medium">إجمالي السجلات</span>
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mt-1">{{ validationResult.total_rows }}</h3>
            </div>
            
            <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-white/[0.03]">
              <span class="text-xs text-gray-500 dark:text-gray-400 font-medium">السجلات السليمة</span>
              <h3 class="text-2xl font-bold text-green-600 mt-1">{{ validationResult.valid_rows }}</h3>
            </div>

            <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-white/[0.03]">
              <span class="text-xs text-gray-500 dark:text-gray-400 font-medium">السجلات التي تحتوي على أخطاء</span>
              <h3 class="text-2xl font-bold text-red-600 mt-1">{{ validationResult.errors.length }}</h3>
            </div>

            <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-white/[0.03]">
              <span class="text-xs text-gray-500 dark:text-gray-400 font-medium">إجمالي الأخطاء المرصودة</span>
              <h3 class="text-2xl font-bold text-red-500 mt-1">{{ validationResult.error_count }}</h3>
            </div>
          </div>

          <!-- Controls Panel -->
          <div class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-white/[0.03] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div class="flex items-center gap-3">
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">عرض:</span>
              <button 
                @click="showErrorsOnly = false"
                class="px-4 py-1.5 rounded-lg text-xs font-bold transition-all"
                :class="[!showErrorsOnly ? 'bg-blue-600 text-white shadow-sm' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400']"
              >
                الكل ({{ allRowsData.length }})
              </button>
              <button 
                @click="showErrorsOnly = true"
                class="px-4 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1"
                :class="[showErrorsOnly ? 'bg-red-600 text-white shadow-sm' : 'bg-red-50 dark:bg-red-950/20 text-red-600']"
              >
                أخطاء فقط ({{ validationResult.errors.length }})
              </button>
            </div>

            <div class="flex items-center gap-2">
              <button 
                @click="revalidateEdits"
                class="bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs px-4 py-2 rounded-lg flex items-center gap-1.5 shadow-sm transition-all"
              >
                <RefreshCw class="w-3.5 h-3.5" />
                إعادة فحص التعديلات
              </button>

              <button 
                @click="commitSeeding"
                :disabled="validationResult.errors.length > 0"
                class="font-bold text-xs px-5 py-2 rounded-lg flex items-center gap-1.5 shadow-md transition-all"
                :class="[
                  validationResult.errors.length > 0
                    ? 'bg-gray-100 text-gray-400 dark:bg-gray-800 dark:text-gray-600 cursor-not-allowed'
                    : 'bg-green-600 hover:bg-green-700 text-white shadow-green-500/10'
                ]"
              >
                <CheckCircle2 class="w-3.5 h-3.5" />
                اعتماد وحفظ السجلات نهائياً
              </button>
            </div>
          </div>

          <!-- Data Grid -->
          <div class="rounded-2xl border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-white/[0.03] overflow-hidden">
            <div class="overflow-x-auto max-w-full custom-scrollbar">
              <table class="w-full text-right border-collapse min-w-[2000px]">
                <thead class="bg-gray-50/80 dark:bg-gray-900/50 border-b border-gray-100 dark:border-gray-800">
                  <tr>
                    <th class="p-3 text-center font-bold text-sm w-16 border-l border-gray-200 dark:border-gray-800">رقم الصف</th>
                    <th 
                      v-for="col in errorColumns" 
                      :key="col"
                      class="p-3 font-bold text-sm border-l border-gray-200 dark:border-gray-800 group hover:bg-gray-100/50 transition-colors relative"
                    >
                      <div class="flex items-center justify-between gap-2">
                        <span>{{ col }}</span>
                        <!-- Bulk change trigger -->
                        <button 
                          @click="openBulkChange(col)"
                          class="text-gray-400 hover:text-blue-600 p-1 rounded hover:bg-white dark:hover:bg-gray-800 opacity-0 group-hover:opacity-100 transition-all"
                          title="تعديل هذا العمود لجميع السجلات دفعة واحدة"
                        >
                          <Copy class="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
                  <tr 
                    v-for="row in paginatedRows" 
                    :key="row.rowIdx"
                    class="hover:bg-gray-50/40 dark:hover:bg-gray-900/20 transition-colors"
                  >
                    <!-- Row Number -->
                    <td class="p-3 text-center border-l border-gray-100 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-900/20 font-mono text-xs font-bold">
                      <span :class="[row.err ? 'text-red-600' : 'text-gray-600 dark:text-gray-400']">
                        {{ row.rowIdx + 2 }}
                      </span>
                    </td>

                    <!-- Cells -->
                    <td 
                      v-for="col in errorColumns" 
                      :key="col"
                      class="p-2 border-l border-gray-100 dark:border-gray-800 align-top"
                      :class="[getCellError(row, col) ? 'bg-red-50/20 dark:bg-red-950/10' : '']"
                    >
                      <div class="relative min-w-[160px]">
                        <!-- Render dynamic Select dropdowns based on field type -->
                        <select 
                          v-if="hasDropdownOptions(col)"
                          v-model="row.rowData[col]"
                          @change="handleCellChange(row.rowIdx, col, row.rowData[col])"
                          class="w-full text-xs p-2 rounded-lg border bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 transition-all focus:outline-none focus:ring-2 focus:ring-blue-500/20 cursor-pointer"
                          :class="[getCellError(row, col) ? 'border-red-300 dark:border-red-900 text-red-900 dark:text-red-300' : 'border-transparent hover:border-gray-200 dark:hover:border-gray-700']"
                        >
                          <option value="">-- اختر القيمة --</option>
                          <option 
                            v-if="isOptionUnknown(row.rowData[col], col)"
                            :value="row.rowData[col]"
                            class="text-red-600 font-bold bg-red-50"
                          >
                            [غير معرّف]: {{ row.rowData[col] }}
                          </option>
                          
                          <!-- Groups for CD, Branches, Police -->
                          <template v-if="col === 'جهة_العمل' || col === 'الإدارة_السرية'">
                            <optgroup label="🏢 الإدارات المركزية">
                              <option v-for="opt in getFilteredCDs(row.rowData)" :key="opt.id" :value="opt.name">{{ opt.name }}</option>
                            </optgroup>
                            <optgroup label="🏢 الفروع">
                              <option v-for="opt in getFilteredBranches(row.rowData)" :key="opt.id" :value="opt.name">{{ opt.name }}</option>
                            </optgroup>
                            <optgroup label="🏛️ شرطة المديرية">
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
                          class="w-full text-xs p-2 rounded-lg border bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 transition-all focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                          :class="[getCellError(row, col) ? 'border-red-300 dark:border-red-900 text-red-900 dark:text-red-300' : 'border-transparent hover:border-gray-200 dark:hover:border-gray-700']"
                        />

                        <!-- Fallback normal text input -->
                        <input 
                          v-else
                          type="text"
                          v-model="row.rowData[col]"
                          @blur="handleCellChange(row.rowIdx, col, row.rowData[col])"
                          class="w-full text-xs p-2 rounded-lg border bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 transition-all focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                          :class="[getCellError(row, col) ? 'border-red-300 dark:border-red-900 text-red-900 dark:text-red-300 font-bold' : 'border-transparent hover:border-gray-200 dark:hover:border-gray-700']"
                        />

                        <!-- Error tooltip & quick-fix suggestions -->
                        <div v-if="getCellError(row, col)" class="mt-1 flex flex-col gap-1">
                          <span class="text-[10px] font-bold text-red-500 flex items-start gap-1">
                            <AlertTriangle class="w-3.5 h-3.5 shrink-0" />
                            {{ getCellError(row, col).message }}
                          </span>
                          
                          <!-- Custom suggestions helper -->
                          <div v-if="col === 'الرقم العسكري الصحيح' && getCellError(row, col).message.includes('يوجد اختلاف')" class="flex gap-1">
                            <button 
                              @click="applyQuickFix(row.rowIdx, 'الرقم العسكري', row.rowData['الرقم العسكري الصحيح'], 'الرقم العسكري الصحيح', '')"
                              class="bg-green-100 hover:bg-green-200 text-green-700 dark:bg-green-950/30 dark:text-green-400 px-2 py-0.5 rounded text-[10px] font-bold"
                            >
                              اعتماد وتصحيح
                            </button>
                            <button 
                              @click="applyQuickFix(row.rowIdx, 'الرقم العسكري الصحيح', '', null, null)"
                              class="bg-gray-100 hover:bg-gray-200 text-gray-700 dark:bg-gray-800 dark:text-gray-400 px-2 py-0.5 rounded text-[10px]"
                            >
                              تجاهل
                            </button>
                          </div>
                        </div>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Pagination controls -->
            <div v-if="totalPages > 1" class="flex items-center justify-between px-6 py-4 bg-gray-50/80 dark:bg-gray-900/10 border-t border-gray-100 dark:border-gray-800">
              <span class="text-xs text-gray-500">
                عرض الصفوف من <span class="font-bold">{{ (currentPage - 1) * itemsPerPage + 1 }}</span> إلى <span class="font-bold">{{ Math.min(currentPage * itemsPerPage, filteredRowsCount) }}</span> من أصل <span class="font-bold">{{ filteredRowsCount }}</span> سجل
              </span>
              <div class="flex items-center gap-1">
                <button 
                  @click="currentPage = 1" 
                  :disabled="currentPage === 1"
                  class="p-2 border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                >
                  <ChevronsRight class="w-4 h-4" />
                </button>
                <button 
                  @click="currentPage--" 
                  :disabled="currentPage === 1"
                  class="px-3 py-1.5 border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50 text-xs font-bold"
                >
                  السابق
                </button>
                <div class="px-4 text-xs font-bold text-gray-700 dark:text-gray-300">
                  صفحة {{ currentPage }} من {{ totalPages }}
                </div>
                <button 
                  @click="currentPage++" 
                  :disabled="currentPage === totalPages"
                  class="px-3 py-1.5 border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50 text-xs font-bold"
                >
                  التالي
                </button>
                <button 
                  @click="currentPage = totalPages" 
                  :disabled="currentPage === totalPages"
                  class="p-2 border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                >
                  <ChevronsLeft class="w-4 h-4" />
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
                <optgroup label="🏢 الإدارات المركزية">
                  <option v-for="opt in getFilteredCDs(null)" :key="opt.id" :value="opt.name">{{ opt.name }}</option>
                </optgroup>
                <optgroup label="🏢 الفروع">
                  <option v-for="opt in getFilteredBranches(null)" :key="opt.id" :value="opt.name">{{ opt.name }}</option>
                </optgroup>
                <optgroup label="🏛️ شرطة المديرية">
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
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import Swal from 'sweetalert2'
import { 
  UploadCloud, FileSpreadsheet, CheckCircle2, AlertTriangle, 
  ArrowLeft, ArrowRight, Trash2, RefreshCw, Loader2, Check, 
  Copy, ChevronsRight, ChevronsLeft, X 
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

// Load constants on mount
onMounted(async () => {
  try {
    constants.value = await fetchAllConstants()
  } catch (error) {
    console.error('Failed to load constants dictionaries', error)
  }
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
  validationResult.value.errors.forEach(e => {
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
  // Cascading dependency clears
  if (col === 'الوحدة') {
    // Reset workplace, division, unit
    allRowsData.value[rowIdx]['جهة_العمل'] = ''
    allRowsData.value[rowIdx]['القسم'] = ''
    allRowsData.value[rowIdx]['الوحدة_الفرعية'] = ''
  } else if (col === 'جهة_العمل' || col === 'الإدارة_السرية') {
    allRowsData.value[rowIdx]['القسم'] = ''
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
}

// Post edited JSON to validation endpoint
async function revalidateEdits() {
  isLoading.value = true
  try {
    const res = await validateInitialSeedJson(allRowsData.value)
    if (res.success && res.data) {
      validationResult.value = res.data
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
  if (!col || !validationResult.value.errors) return []
  
  const values = new Set<string>()
  validationResult.value.errors.forEach(errRow => {
    const hasErr = errRow.errors.some((e: any) => e.field === col)
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
      allRowsData.value[idx][col] = bulkEditNewValue.value
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

// Reset entire flow
function resetWizard() {
  removeFile()
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
</style>
