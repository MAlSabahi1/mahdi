<template>
  <admin-layout>
    <div class="pb-12" dir="rtl">
      <!-- Page Header -->
      <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <div class="p-2.5 bg-brand-50 dark:bg-brand-500/10 rounded-xl text-brand-600 dark:text-brand-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            معالج الاستيراد الآمن
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2 font-medium">
            منصة متقدمة لاستيراد وتحديث البيانات آلياً عبر محرك <span class="font-mono text-brand-500 dark:text-brand-400">Celery</span>
          </p>
        </div>
      </div>

      <!-- Horizontal Stepper -->
      <div class="mb-6 rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900 shadow-theme-xs overflow-hidden">
        <div class="px-6 py-5 sm:px-10">
          <div class="flex items-center justify-between">
            <template v-for="(step, index) in steps" :key="step.number">
              <!-- Step Item -->
              <div class="flex items-center gap-3 relative z-10 shrink-0">
                <!-- Step Circle -->
                <div 
                  class="h-10 w-10 shrink-0 rounded-full flex items-center justify-center font-bold text-sm transition-all duration-500 border-2"
                  :class="[
                    currentStep === step.number 
                      ? 'border-brand-500 bg-brand-500 text-white shadow-lg shadow-brand-500/30 dark:shadow-brand-500/20 scale-110' 
                      : currentStep > step.number 
                        ? 'border-brand-500 bg-brand-500 text-white' 
                        : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-400'
                  ]"
                >
                  <svg v-if="currentStep > step.number" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                  <span v-else>{{ step.number }}</span>
                </div>
                <!-- Step Text -->
                <div class="hidden sm:block">
                  <h4 
                    class="text-sm font-bold transition-colors duration-300" 
                    :class="currentStep >= step.number ? 'text-gray-900 dark:text-white' : 'text-gray-400 dark:text-gray-500'"
                  >{{ step.title }}</h4>
                  <p 
                    class="text-xs mt-0.5 transition-colors duration-300"
                    :class="currentStep >= step.number ? 'text-gray-500 dark:text-gray-400' : 'text-gray-300 dark:text-gray-600'"
                  >{{ step.desc }}</p>
                </div>
              </div>

              <!-- Connecting Line -->
              <div 
                v-if="index < steps.length - 1" 
                class="flex-1 h-[2px] mx-3 sm:mx-4 rounded-full transition-all duration-500"
                :class="currentStep > step.number ? 'bg-brand-500' : 'bg-gray-200 dark:bg-gray-700'"
              ></div>
            </template>
          </div>
        </div>
      </div>

      <!-- Main Content Card -->
      <div class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900 shadow-theme-xs min-h-[460px] flex flex-col overflow-hidden">
        
        <!-- Step Header -->
        <div class="border-b border-gray-100 dark:border-gray-800 px-6 py-5 sm:px-8 bg-gray-50/50 dark:bg-gray-800/20 flex items-center justify-between">
          <div>
            <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ steps[currentStep - 1].title }}</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1 font-medium">{{ steps[currentStep - 1].desc }}</p>
          </div>
          <span class="hidden sm:inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-400">
            المرحلة {{ currentStep }} من {{ steps.length }}
          </span>
        </div>

            <!-- Dynamic Step Content -->
            <div class="flex-1 p-6 md:p-8 flex flex-col bg-white dark:bg-gray-900">
              <transition name="fade-slide" mode="out-in">
                
                <!-- Step 1: Upload Dropzone -->
                <div v-if="currentStep === 1" class="flex-1 flex flex-col justify-center w-full" key="step1">
                  <div class="flex items-center justify-center w-full max-w-3xl mx-auto">
                    <label for="dropzone-file" class="flex flex-col items-center justify-center w-full h-[320px] border-2 border-gray-300 border-dashed rounded-xl cursor-pointer bg-gray-50 dark:hover:bg-gray-800 dark:bg-gray-800/50 hover:bg-gray-100 dark:border-gray-700 dark:hover:border-gray-600 transition-all duration-200"
                           :class="{ 'border-brand-500 bg-brand-50/50 dark:bg-brand-500/10 dark:border-brand-500': selectedFile }">
                      <div class="flex flex-col items-center justify-center pt-5 pb-6">
                        <div class="w-16 h-16 mb-5 rounded-full flex items-center justify-center transition-colors"
                             :class="selectedFile ? 'bg-brand-100 text-brand-600 dark:bg-brand-900/60 dark:text-brand-400 ring-4 ring-brand-50 dark:ring-brand-900/20' : 'text-gray-400 bg-white dark:bg-gray-800 shadow-sm border border-gray-100 dark:border-gray-700'">
                          <svg v-if="!selectedFile" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                        </div>
                        <h4 v-if="!selectedFile" class="mb-2 text-base font-bold text-gray-900 dark:text-white">اضغط لرفع الكشف أو قم بإفلاته هنا</h4>
                        <p v-if="!selectedFile" class="text-sm text-gray-500 dark:text-gray-400 mt-1 max-w-sm text-center leading-relaxed">يدعم النظام ملفات الإكسل بصيغة .xlsx فقط. تأكد من الاحتفاظ بالـ UUID المشفر في اسم الملف.</p>
                        
                        <div v-else class="text-center animate-fade-in-up">
                          <p class="text-base font-bold text-brand-600 dark:text-brand-400" dir="ltr">{{ selectedFile.name }}</p>
                          <p class="mt-3 inline-flex items-center gap-2 px-3 py-1 bg-white dark:bg-gray-800 rounded-lg text-xs font-medium text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-700 shadow-theme-xs">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                            حجم الملف: {{ (selectedFile.size / 1024 / 1024).toFixed(2) }} MB
                          </p>
                        </div>
                      </div>
                      <input id="dropzone-file" type="file" class="hidden" @change="handleFileChange" accept=".xlsx,.xls,.csv" />
                    </label>
                  </div>
                </div>

                <!-- Step 2: Validation & Structure -->
                <div v-else-if="currentStep === 2" class="flex-1 w-full flex flex-col justify-center" key="step2">
                  
                  <div v-if="isUploading" class="flex-1 flex flex-col items-center justify-center min-h-[300px]">
                    <div class="relative w-16 h-16 flex items-center justify-center mb-6">
                      <div class="absolute inset-0 border-4 border-gray-100 dark:border-gray-800 rounded-full"></div>
                      <div class="absolute inset-0 border-4 border-brand-500 rounded-full border-t-transparent animate-spin"></div>
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-brand-500 absolute" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                      </svg>
                    </div>
                    <h3 class="text-base font-bold text-gray-900 dark:text-white">جاري الاتصال بقاعدة البيانات ومطابقة الهيكل...</h3>
                    <p class="text-sm text-gray-500 mt-2 font-medium">النظام يطبق بروتوكولات الفحص الأمني للملف.</p>
                  </div>

                  <div v-else-if="uploadError" class="flex-1 flex items-center justify-center">
                    <div class="max-w-lg w-full bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/30 rounded-2xl p-8 text-center animate-fade-in-up">
                      <div class="w-14 h-14 bg-red-100 dark:bg-red-500/20 text-red-600 dark:text-red-400 rounded-full flex items-center justify-center mx-auto mb-5 shadow-sm">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                      </div>
                      <h4 class="text-base font-bold text-red-800 dark:text-red-400 mb-3">فشل فحص المطابقة</h4>
                      <p class="text-sm text-red-600 dark:text-red-300 font-medium leading-relaxed">{{ uploadError }}</p>
                    </div>
                  </div>

                  <div v-else class="flex-1 space-y-6">
                    <div class="bg-green-50 dark:bg-green-500/10 border border-green-200 dark:border-green-500/20 rounded-xl p-4 flex items-start gap-4">
                      <div class="p-2 bg-green-100 dark:bg-green-500/20 rounded-lg shrink-0">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-600 dark:text-green-400" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                        </svg>
                      </div>
                      <div>
                        <h3 class="text-sm font-bold text-green-800 dark:text-green-400">مطابقة هيكل الكشف المستورد (ناجح)</h3>
                        <p class="text-xs text-green-600 dark:text-green-500 mt-1 font-medium">تم فحص الأعمدة الحيوية لمطابقة القواعد التنظيمية والمالية الأساسية في الباك اند.</p>
                      </div>
                    </div>

                    <div class="overflow-hidden rounded-xl border border-gray-200 dark:border-gray-800 shadow-theme-xs">
                      <table class="w-full text-right text-sm">
                        <thead class="bg-gray-50 dark:bg-gray-800/80 border-b border-gray-200 dark:border-gray-700 text-gray-500 dark:text-gray-400">
                          <tr>
                            <th class="px-5 py-4 font-bold text-xs uppercase tracking-wider">اسم العمود بالكشف</th>
                            <th class="px-5 py-4 font-bold text-xs uppercase tracking-wider">حالة المطابقة الفنية</th>
                            <th class="px-5 py-4 font-bold text-xs uppercase tracking-wider">النوع المتوقع</th>
                            <th class="px-5 py-4 font-bold text-xs uppercase tracking-wider">التحقق الهيكلي</th>
                          </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100 dark:divide-gray-800 bg-white dark:bg-gray-900">
                          <tr class="animate-fade-in-up animation-delay-100 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                            <td class="px-5 py-4 font-mono text-gray-800 dark:text-gray-200 text-xs font-medium">military_number</td>
                            <td class="px-5 py-4 text-green-600 dark:text-green-400 font-bold flex items-center gap-1.5 text-xs">
                              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                              متطابق
                            </td>
                            <td class="px-5 py-4 font-mono text-xs text-gray-500">Integer (7-digits)</td>
                            <td class="px-5 py-4 text-gray-600 dark:text-gray-400 text-xs font-medium">الرقم العسكري (مفتاح أساسي)</td>
                          </tr>
                          <tr class="animate-fade-in-up animation-delay-200 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                            <td class="px-5 py-4 font-mono text-gray-800 dark:text-gray-200 text-xs font-medium">full_name</td>
                            <td class="px-5 py-4 text-green-600 dark:text-green-400 font-bold flex items-center gap-1.5 text-xs">
                              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                              متطابق
                            </td>
                            <td class="px-5 py-4 font-mono text-xs text-gray-500">String (max 255)</td>
                            <td class="px-5 py-4 text-gray-600 dark:text-gray-400 text-xs font-medium">الاسم الكامل المطابق للهوية</td>
                          </tr>
                          <tr class="animate-fade-in-up animation-delay-300 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                            <td class="px-5 py-4 font-mono text-gray-800 dark:text-gray-200 text-xs font-medium">base_salary</td>
                            <td class="px-5 py-4 text-green-600 dark:text-green-400 font-bold flex items-center gap-1.5 text-xs">
                              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                              متطابق
                            </td>
                            <td class="px-5 py-4 font-mono text-xs text-gray-500">Decimal (10,2)</td>
                            <td class="px-5 py-4 text-gray-600 dark:text-gray-400 text-xs font-medium">الراتب الأساسي المعتمد</td>
                          </tr>
                          <tr class="animate-fade-in-up animation-delay-400 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                            <td class="px-5 py-4 font-mono text-gray-800 dark:text-gray-200 text-xs font-medium">absent_days</td>
                            <td class="px-5 py-4 text-green-600 dark:text-green-400 font-bold flex items-center gap-1.5 text-xs">
                              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                              متطابق
                            </td>
                            <td class="px-5 py-4 font-mono text-xs text-gray-500">Integer</td>
                            <td class="px-5 py-4 text-gray-600 dark:text-gray-400 text-xs font-medium">أيام الغياب الفعلي</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>

                <!-- Step 3: Celery Processing -->
                <div v-else-if="currentStep === 3" class="flex-1 w-full flex flex-col justify-center items-center py-10" key="step3">
                  <div class="max-w-md w-full space-y-8 text-center bg-gray-50 dark:bg-gray-800/30 p-8 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-theme-xs">
                    <div class="w-20 h-20 bg-white dark:bg-gray-800 rounded-2xl mx-auto flex items-center justify-center border border-gray-200 dark:border-gray-700 shadow-sm">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-brand-600 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                    </div>
                    
                    <div>
                      <h3 class="text-base font-bold text-gray-900 dark:text-white">جاري الترحيل الآلي للبيانات</h3>
                      <p class="text-sm text-gray-500 dark:text-gray-400 mt-2 font-medium">محرك Celery يقوم بقراءة السجلات ومطابقتها وتخزينها بأمان.</p>
                    </div>

                    <!-- Clean Progress Bar -->
                    <div class="space-y-3 mt-6">
                      <div class="flex justify-between text-xs font-bold px-1">
                        <span class="text-brand-600 dark:text-brand-400">التقدم الفعلي</span>
                        <span class="text-gray-900 dark:text-white font-mono">{{ celeryProgress }}%</span>
                      </div>
                      <div class="h-3 w-full bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden shadow-inner">
                        <div 
                          class="h-full bg-brand-500 rounded-full transition-all duration-300 relative overflow-hidden"
                          :style="{ width: `${celeryProgress}%` }"
                        >
                          <div class="absolute inset-0 bg-white/20 animate-pulse"></div>
                        </div>
                      </div>
                    </div>

                    <div class="mt-6 inline-flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
                      <span class="w-2 h-2 rounded-full bg-brand-500 animate-pulse"></span>
                      <span class="text-xs text-gray-500 dark:text-gray-400 font-mono">Task: {{ currentTaskId }}</span>
                    </div>
                  </div>
                </div>

                <!-- Step 4: Final Results -->
                <div v-else-if="currentStep === 4" class="flex-1 w-full flex flex-col justify-center" key="step4">
                  
                  <div class="mb-8 rounded-2xl border p-6 flex flex-col sm:flex-row items-center sm:items-start gap-5 text-center sm:text-right"
                       :class="[errorRecords > 0 && processedRecords === 0 ? 'bg-red-50 border-red-200 dark:bg-red-500/10 dark:border-red-500/30' : 'bg-green-50 border-green-200 dark:bg-green-500/10 dark:border-green-500/30']">
                    <div class="p-4 rounded-full shrink-0 shadow-sm" 
                         :class="[errorRecords > 0 && processedRecords === 0 ? 'bg-red-100 text-red-600 dark:bg-red-500/20 dark:text-red-400' : 'bg-green-100 text-green-600 dark:bg-green-500/20 dark:text-green-400']">
                      <svg v-if="errorRecords > 0 && processedRecords === 0" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                      <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <div>
                      <h4 class="text-base font-bold mb-2" :class="[errorRecords > 0 && processedRecords === 0 ? 'text-red-800 dark:text-red-400' : 'text-green-800 dark:text-green-400']">
                        {{ errorRecords > 0 && processedRecords === 0 ? 'تعذر استيراد الملف - أخطاء هيكلية أو تلاعب' : 'اكتملت المعالجة بنجاح' }}
                      </h4>
                      <p class="text-sm font-medium leading-relaxed" :class="[errorRecords > 0 && processedRecords === 0 ? 'text-red-600 dark:text-red-300' : 'text-green-600 dark:text-green-300']">
                        {{ errorRecords > 0 && processedRecords === 0 
                           ? 'تم رفض كافة البيانات المرسلة لأنها تحتوي على أخطاء أو تلاعب في الأرقام العسكرية المحمية.' 
                           : (processedRecords === 0 
                              ? 'البيانات المرفوعة مطابقة تماماً للنسخة الحالية. لم يتم العثور على أي تعديلات جديدة.' 
                              : 'تم استخراج التعديلات الصالحة وتخزينها في شاشة المراجعة، وتم استبعاد السجلات الخاطئة (إن وجدت).') }}
                      </p>
                    </div>
                  </div>

                  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-800/50 p-6 flex flex-col justify-center items-center text-center shadow-sm">
                      <div class="w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-500 mb-4 flex items-center justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                      </div>
                      <span class="text-sm font-bold text-gray-500 dark:text-gray-400 mb-2">إجمالي السجلات المدخلة</span>
                      <span class="text-4xl font-black text-gray-900 dark:text-white">{{ totalRecords }}</span>
                    </div>
                    
                    <div class="rounded-2xl border border-green-200 bg-green-50/50 dark:border-green-500/30 dark:bg-green-500/10 p-6 flex flex-col justify-center items-center text-center shadow-sm relative overflow-hidden">
                      <div class="absolute -right-4 -top-4 w-16 h-16 bg-green-500/10 rounded-full blur-xl"></div>
                      <div class="w-10 h-10 rounded-full bg-green-100 dark:bg-green-500/20 text-green-600 dark:text-green-400 mb-4 flex items-center justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                      </div>
                      <span class="text-sm font-bold text-green-700 dark:text-green-500 mb-2">تعديلات صالحة (Staging)</span>
                      <span class="text-4xl font-black text-green-600 dark:text-green-400">{{ processedRecords }}</span>
                    </div>
                    
                    <div class="rounded-2xl border border-red-200 bg-red-50/50 dark:border-red-500/30 dark:bg-red-500/10 p-6 flex flex-col justify-center items-center text-center shadow-sm relative overflow-hidden">
                      <div class="absolute -left-4 -bottom-4 w-16 h-16 bg-red-500/10 rounded-full blur-xl"></div>
                      <div class="w-10 h-10 rounded-full bg-red-100 dark:bg-red-500/20 text-red-600 dark:text-red-400 mb-4 flex items-center justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                      </div>
                      <span class="text-sm font-bold text-red-700 dark:text-red-500 mb-2">تعديلات مرفوضة / خطأ</span>
                      <span class="text-4xl font-black text-red-600 dark:text-red-400">{{ errorRecords }}</span>
                    </div>
                  </div>
                  
                  <div class="mt-8 flex flex-col sm:flex-row justify-between items-center gap-4 bg-gray-50 dark:bg-gray-800/30 p-4 rounded-xl border border-gray-100 dark:border-gray-800">
                    <RouterLink v-if="errorRecords > 0" to="/services/rejections" class="text-sm font-bold text-red-600 hover:text-red-700 hover:underline flex items-center gap-2">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                      عرض تقرير المرفوضات التفصيلي
                    </RouterLink>
                    <span v-else></span>
                    
                    <RouterLink v-if="processedRecords > 0" to="/services/staging" class="flex items-center gap-2 rounded-lg bg-green-500 px-6 py-3 text-sm font-medium text-white shadow-theme-xs hover:bg-green-600 transition-colors w-full sm:w-auto justify-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                      مراجعة واعتماد التعديلات
                    </RouterLink>
                  </div>
                </div>
                
              </transition>
            </div>

            <!-- Wizard Footer -->
            <div class="border-t border-gray-100 dark:border-gray-800 p-6 flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/20">
              <button 
                v-if="currentStep < 4"
                @click="resetWizard"
                :disabled="isUploading || currentStep === 3"
                class="rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 transition-colors disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
              >
                إلغاء العملية
              </button>
              
              <button 
                v-if="currentStep === 1"
                :disabled="!selectedFile || isUploading"
                @click="startUpload"
                class="mr-auto flex items-center gap-2 rounded-lg bg-brand-500 px-8 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors disabled:opacity-50"
              >
                <svg v-if="isUploading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                رفع الملف والمتابعة
              </button>
              
              <button 
                v-else-if="currentStep === 4"
                @click="resetWizard"
                class="mr-auto rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 transition-colors dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
              >
                استيراد كشف آخر
              </button>
            </div>

      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useServicesStore } from '@/stores/services'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'

const router = useRouter()
const servicesStore = useServicesStore()

const currentStep = ref(1)
const selectedFile = ref<File | null>(null)
const celeryProgress = ref(0)
let pollerInterval: any = null

const isUploading = ref(false)
const uploadError = ref('')
const currentTaskId = ref('')

const totalRecords = ref(0)
const processedRecords = ref(0)
const errorRecords = ref(0)

const steps = [
  { number: 1, title: 'رفع الكشف المالي', desc: 'تحميل ملف بصيغة xlsx' },
  { number: 2, title: 'الفحص والمطابقة', desc: 'تدقيق أمني للبيانات' },
  { number: 3, title: 'المعالجة والتخزين', desc: 'سحب السجلات عبر Celery' },
  { number: 4, title: 'تقرير النتيجة', desc: 'ملخص العمليات والاعتماد' }
]

function handleFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0]
  }
}

async function startUpload() {
  if (!selectedFile.value) return
  
  currentStep.value = 2
  isUploading.value = true
  uploadError.value = ''
  
  try {
    const response = await servicesStore.importSheet(selectedFile.value)
    
    // Simulate slight delay for loading UX
    setTimeout(() => {
      isUploading.value = false
      // Show the structure valid table briefly
      setTimeout(() => {
        if (response.async && response.task_id) {
          currentTaskId.value = response.task_id
          currentStep.value = 3
          pollTaskStatus(response.task_id)
        } else {
          const responseData = response.data || response
          const errorsList = responseData.errors || []
          errorRecords.value = errorsList.length
          processedRecords.value = responseData.stats?.changes_detected || 0
          totalRecords.value = errorRecords.value + processedRecords.value
          currentStep.value = 4
        }
      }, 1800)
    }, 800)
    
  } catch (err: any) {
    setTimeout(() => {
      isUploading.value = false
      uploadError.value = servicesStore.error || 'الملف غير صالح أو تم التلاعب به. تأكد من توافق الـ UUID الموجود في اسم الملف مع النظام.'
    }, 800)
  }
}

async function pollTaskStatus(taskId: string) {
  celeryProgress.value = 10
  pollerInterval = setInterval(async () => {
    try {
      const res = await servicesStore.checkTaskStatus(taskId)
      if (res.data) {
        if (res.data.status === 'PROGRESS') {
          celeryProgress.value = res.data.progress || 50
        } else if (res.data.status === 'SUCCESS') {
          clearInterval(pollerInterval)
          celeryProgress.value = 100
          
          setTimeout(() => {
            const resultData = res.data.result || {}
            const errorsList = resultData.errors || []
            errorRecords.value = errorsList.length
            processedRecords.value = resultData.stats?.changes_detected || 0
            totalRecords.value = errorRecords.value + processedRecords.value
            currentStep.value = 4
          }, 800)
        } else if (res.data.status === 'FAILURE') {
          clearInterval(pollerInterval)
          uploadError.value = res.data.error || 'حدث فشل أثناء معالجة السجلات في السحابة.'
          currentStep.value = 2
        }
      }
    } catch (e) {
      clearInterval(pollerInterval)
      uploadError.value = 'فقدنا الاتصال بالخادم أثناء متابعة العملية.'
      currentStep.value = 2
    }
  }, 2000)
}

function resetWizard() {
  if (pollerInterval) clearInterval(pollerInterval)
  currentStep.value = 1
  selectedFile.value = null
  celeryProgress.value = 0
  totalRecords.value = 0
  processedRecords.value = 0
  errorRecords.value = 0
  uploadError.value = ''
  isUploading.value = false
  currentTaskId.value = ''
}

onUnmounted(() => {
  if (pollerInterval) clearInterval(pollerInterval)
})
</script>

<style>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

.animate-fade-in-up {
  opacity: 0;
  animation: fadeInUp 0.4s ease forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animation-delay-100 { animation-delay: 100ms; }
.animation-delay-200 { animation-delay: 200ms; }
.animation-delay-300 { animation-delay: 300ms; }
.animation-delay-400 { animation-delay: 400ms; }
</style>
