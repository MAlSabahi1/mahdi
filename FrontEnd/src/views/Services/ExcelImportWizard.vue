<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="معالج الاستيراد الجماعي وتتبع مهام Celery" />

    <div class="space-y-6 max-w-5xl mx-auto pb-12" dir="rtl">
      
      <!-- Premium Page Header -->
      <div class="flex items-start justify-between border-b border-gray-200 dark:border-gray-800 pb-6">
        <div>
          <h1 class="text-2xl font-black text-gray-900 dark:text-white tracking-tight flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-brand-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            معالج الاستيراد الآمن
          </h1>
          <p class="text-[13px] text-gray-500 dark:text-gray-400 mt-2 font-medium max-w-2xl leading-relaxed">
            منصة متقدمة لاستيراد وتحديث البيانات آلياً عبر محرك <span class="font-mono text-brand-600 dark:text-brand-400">Celery</span>. 
            تضمن لك هذه الأداة مطابقة السجلات المرفوعة مع القواعد الأمنية والهيكلية للنظام قبل الترحيل المالي.
          </p>
        </div>
      </div>

      <!-- Clean & Harmonious Stepper -->
      <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl shadow-sm p-6 relative">
        <div class="flex items-center justify-between relative z-10 w-full px-4 md:px-8 text-center">
          <template v-for="(step, index) in steps" :key="step.number">
            
            <!-- Step Item -->
            <div class="flex flex-col items-center relative z-10 bg-white dark:bg-gray-900 px-2 group">
              <div 
                class="h-10 w-10 rounded-full flex items-center justify-center font-bold text-sm transition-all duration-500 border-2"
                :class="[
                  currentStep === step.number 
                    ? 'border-brand-600 bg-brand-50 dark:bg-brand-900/30 text-brand-700 dark:text-brand-400 shadow-sm' 
                    : currentStep > step.number 
                      ? 'border-emerald-500 bg-emerald-500 text-white' 
                      : 'border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-400'
                ]"
              >
                <svg v-if="currentStep > step.number" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <span v-else>{{ step.number }}</span>
              </div>
              <div class="mt-3 text-center">
                <h4 class="text-xs font-black" :class="currentStep >= step.number ? 'text-gray-900 dark:text-white' : 'text-gray-400'">{{ step.title }}</h4>
              </div>
            </div>

            <!-- Connecting Line -->
            <div v-if="index < steps.length - 1" class="hidden md:block flex-1 h-0.5 bg-gray-200 dark:bg-gray-800 -mt-8 relative overflow-hidden">
              <div class="h-full bg-emerald-500 transition-all duration-700 ease-out" :style="{ width: currentStep > step.number ? '100%' : '0%' }"></div>
            </div>

          </template>
        </div>
      </div>

      <!-- Main Interaction Area -->
      <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-8 shadow-sm min-h-[380px] flex flex-col">
        <transition name="fade-slide" mode="out-in">
          
          <!-- Step 1: Upload Dropzone -->
          <div v-if="currentStep === 1" class="flex-1 flex flex-col justify-center w-full max-w-2xl mx-auto" key="step1">
            <div 
              class="border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 relative group overflow-hidden"
              :class="[
                selectedFile 
                  ? 'border-brand-500 bg-brand-50/50 dark:bg-brand-900/10' 
                  : 'border-gray-300 dark:border-gray-700 hover:border-brand-400 hover:bg-gray-50 dark:hover:bg-gray-800/50 bg-white dark:bg-gray-900'
              ]"
            >
              <input type="file" @change="handleFileChange" accept=".xlsx,.xls,.csv" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" />
              
              <div class="relative z-0 pointer-events-none flex flex-col items-center">
                <div class="w-16 h-16 mb-4 rounded-full flex items-center justify-center transition-colors"
                     :class="selectedFile ? 'bg-brand-100 text-brand-600 dark:bg-brand-900/40 dark:text-brand-400' : 'bg-gray-100 text-gray-500 dark:bg-gray-800'">
                  <svg v-if="!selectedFile" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                
                <h3 class="text-base font-bold text-gray-900 dark:text-white" v-if="!selectedFile">انقر لاختيار الكشف أو قم بإفلاته هنا</h3>
                <div v-else class="text-center">
                  <h3 class="text-base font-bold text-brand-700 dark:text-brand-400" dir="ltr">{{ selectedFile.name }}</h3>
                  <span class="inline-block mt-2 px-3 py-1 bg-white dark:bg-gray-800 rounded-lg text-[11px] font-bold text-gray-500 border border-gray-200 dark:border-gray-700 shadow-sm">
                    حجم الملف: {{ (selectedFile.size / 1024 / 1024).toFixed(2) }} MB
                  </span>
                </div>
                
                <p class="text-[11px] text-gray-400 mt-4 max-w-sm leading-relaxed" v-if="!selectedFile">
                  يدعم النظام ملفات الإكسل بصيغة .xlsx فقط. تأكد من الاحتفاظ بالـ UUID المشفر في اسم الملف لضمان توافقه الأمني.
                </p>
              </div>
            </div>
          </div>

          <!-- Step 2: Validation & Structure -->
          <div v-else-if="currentStep === 2" class="flex-1 w-full flex flex-col" key="step2">
            
            <div v-if="isUploading" class="flex-1 flex flex-col items-center justify-center min-h-[300px]">
              <div class="relative w-16 h-16 flex items-center justify-center">
                <div class="absolute inset-0 border-4 border-gray-100 dark:border-gray-800 rounded-full"></div>
                <div class="absolute inset-0 border-4 border-brand-500 rounded-full border-t-transparent animate-spin"></div>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-brand-500 absolute" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 class="mt-6 text-sm font-bold text-gray-900 dark:text-white">جاري الاتصال بقاعدة البيانات ومطابقة الهيكل...</h3>
              <p class="text-[11px] text-gray-500 mt-1">النظام يطبق بروتوكولات الفحص الأمني للملف.</p>
            </div>

            <div v-else-if="uploadError" class="flex-1 flex items-center justify-center">
              <div class="max-w-lg w-full bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-900/30 rounded-xl p-6 text-center animate-fade-in-up">
                <div class="w-12 h-12 bg-red-100 dark:bg-red-900/50 text-red-600 dark:text-red-400 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <h4 class="text-sm font-bold text-red-900 dark:text-red-300 mb-2">فشل فحص المطابقة</h4>
                <p class="text-xs text-red-700 dark:text-red-400 leading-relaxed font-medium">{{ uploadError }}</p>
              </div>
            </div>

            <div v-else class="flex-1">
              <div class="mb-4">
                <h3 class="text-sm font-black text-gray-900 dark:text-white flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-emerald-500" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  مطابقة هيكل الكشف المستورد (ناجح)
                </h3>
                <p class="text-[11px] text-gray-500 mt-1 mr-7">تم فحص الأعمدة الحيوية لمطابقة القواعد التنظيمية والمالية الأساسية في الباك اند.</p>
              </div>

              <div class="border border-gray-200 dark:border-gray-800 rounded-xl overflow-hidden shadow-sm">
                <table class="w-full text-right text-xs">
                  <thead class="bg-gray-50 dark:bg-gray-800/50 text-gray-500 border-b border-gray-200 dark:border-gray-800">
                    <tr>
                      <th class="p-3 font-semibold">اسم العمود بالكشف</th>
                      <th class="p-3 font-semibold">حالة المطابقة الفنية</th>
                      <th class="p-3 font-semibold">النوع المتوقع</th>
                      <th class="p-3 font-semibold">التحقق الهيكلي</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-100 dark:divide-gray-800 bg-white dark:bg-gray-900">
                    <!-- Staggered animation classes applied statically for smooth appearance -->
                    <tr class="animate-fade-in-up animation-delay-100">
                      <td class="p-3 font-mono text-gray-800 dark:text-gray-200 font-medium">military_number</td>
                      <td class="p-3 text-emerald-600 dark:text-emerald-400 font-bold flex items-center gap-1">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                        متطابق
                      </td>
                      <td class="p-3 font-mono text-[10px] text-gray-400">Integer (7-digits)</td>
                      <td class="p-3 text-gray-600 dark:text-gray-400">الرقم العسكري (مفتاح أساسي مقفل)</td>
                    </tr>
                    <tr class="animate-fade-in-up animation-delay-200">
                      <td class="p-3 font-mono text-gray-800 dark:text-gray-200 font-medium">full_name</td>
                      <td class="p-3 text-emerald-600 dark:text-emerald-400 font-bold flex items-center gap-1">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                        متطابق
                      </td>
                      <td class="p-3 font-mono text-[10px] text-gray-400">String (max 255)</td>
                      <td class="p-3 text-gray-600 dark:text-gray-400">الاسم الكامل المطابق للهوية</td>
                    </tr>
                    <tr class="animate-fade-in-up animation-delay-300">
                      <td class="p-3 font-mono text-gray-800 dark:text-gray-200 font-medium">base_salary</td>
                      <td class="p-3 text-emerald-600 dark:text-emerald-400 font-bold flex items-center gap-1">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                        متطابق
                      </td>
                      <td class="p-3 font-mono text-[10px] text-gray-400">Decimal (10,2)</td>
                      <td class="p-3 text-gray-600 dark:text-gray-400">الراتب الأساسي المعتمد</td>
                    </tr>
                    <tr class="animate-fade-in-up animation-delay-400">
                      <td class="p-3 font-mono text-gray-800 dark:text-gray-200 font-medium">absent_days</td>
                      <td class="p-3 text-emerald-600 dark:text-emerald-400 font-bold flex items-center gap-1">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                        متطابق
                      </td>
                      <td class="p-3 font-mono text-[10px] text-gray-400">Integer</td>
                      <td class="p-3 text-gray-600 dark:text-gray-400">أيام الغياب الفعلي (مسموح بالتعديل)</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Step 3: Celery Processing -->
          <div v-else-if="currentStep === 3" class="flex-1 w-full flex flex-col justify-center items-center py-10" key="step3">
            <div class="max-w-md w-full space-y-6 text-center">
              <div class="w-16 h-16 bg-gray-50 dark:bg-gray-800 rounded-2xl mx-auto flex items-center justify-center border border-gray-200 dark:border-gray-700">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-brand-600 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </div>
              
              <div>
                <h3 class="text-base font-bold text-gray-900 dark:text-white">جاري الترحيل الآلي للبيانات</h3>
                <p class="text-xs text-gray-500 mt-1">محرك Celery يقوم بقراءة السجلات ومطابقتها وتخزينها بأمان.</p>
              </div>

              <!-- Clean Progress Bar -->
              <div class="space-y-2">
                <div class="flex justify-between text-xs font-bold px-1">
                  <span class="text-brand-600">التقدم الفعلي</span>
                  <span class="text-gray-900 dark:text-white">{{ celeryProgress }}%</span>
                </div>
                <div class="h-2 w-full bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                  <div 
                    class="h-full bg-brand-600 rounded-full transition-all duration-300"
                    :style="{ width: `${celeryProgress}%` }"
                  ></div>
                </div>
              </div>

              <div class="inline-flex items-center gap-1.5 px-3 py-1 bg-gray-50 dark:bg-gray-800 rounded-md border border-gray-200 dark:border-gray-700">
                <span class="w-1.5 h-1.5 rounded-full bg-brand-500 animate-pulse"></span>
                <span class="text-[10px] text-gray-500 font-mono">Task: {{ currentTaskId }}</span>
              </div>
            </div>
          </div>

          <!-- Step 4: Final Results -->
          <div v-else-if="currentStep === 4" class="flex-1 w-full" key="step4">
            
            <div class="mb-6 rounded-xl border p-5 flex items-center gap-4"
                 :class="[errorRecords > 0 && processedRecords === 0 ? 'bg-red-50 border-red-200 dark:bg-red-900/10 dark:border-red-900/30' : 'bg-emerald-50 border-emerald-200 dark:bg-emerald-900/10 dark:border-emerald-900/30']">
              <div class="p-3 rounded-full shrink-0" 
                   :class="[errorRecords > 0 && processedRecords === 0 ? 'bg-red-100 text-red-600 dark:bg-red-900/40 dark:text-red-400' : 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/40 dark:text-emerald-400']">
                <svg v-if="errorRecords > 0 && processedRecords === 0" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div>
                <h4 class="text-sm font-bold" :class="[errorRecords > 0 && processedRecords === 0 ? 'text-red-800 dark:text-red-400' : 'text-emerald-800 dark:text-emerald-400']">
                  {{ errorRecords > 0 && processedRecords === 0 ? 'تعذر استيراد الملف - أخطاء هيكلية أو تلاعب' : 'اكتملت المعالجة بنجاح' }}
                </h4>
                <p class="text-[11px] font-medium mt-1" :class="[errorRecords > 0 && processedRecords === 0 ? 'text-red-600 dark:text-red-500' : 'text-emerald-600 dark:text-emerald-500']">
                  {{ errorRecords > 0 && processedRecords === 0 
                     ? 'تم رفض كافة البيانات المرسلة لأنها تحتوي على أخطاء أو تلاعب في الأرقام العسكرية المحمية.' 
                     : (processedRecords === 0 
                        ? 'البيانات المرفوعة مطابقة تماماً للنسخة الحالية. لم يتم العثور على أي تعديلات جديدة.' 
                        : 'تم استخراج التعديلات الصالحة وتخزينها في شاشة المراجعة، وتم استبعاد السجلات الخاطئة (إن وجدت).') }}
                </p>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="border border-gray-200 dark:border-gray-800 rounded-xl p-5 flex flex-col justify-center items-center text-center bg-gray-50 dark:bg-gray-800/30">
                <span class="text-xs font-bold text-gray-500 dark:text-gray-400 mb-2">إجمالي السجلات المدخلة</span>
                <span class="text-3xl font-black text-gray-900 dark:text-white">{{ totalRecords }}</span>
              </div>
              <div class="border border-emerald-200 dark:border-emerald-900/50 rounded-xl p-5 flex flex-col justify-center items-center text-center bg-emerald-50/50 dark:bg-emerald-900/10">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-500 mb-2">تعديلات صالحة (Staging)</span>
                <span class="text-3xl font-black text-emerald-600">{{ processedRecords }}</span>
              </div>
              <div class="border border-red-200 dark:border-red-900/50 rounded-xl p-5 flex flex-col justify-center items-center text-center bg-red-50/50 dark:bg-red-900/10">
                <span class="text-xs font-bold text-red-700 dark:text-red-500 mb-2">تعديلات مرفوضة / خطأ</span>
                <span class="text-3xl font-black text-red-600">{{ errorRecords }}</span>
              </div>
            </div>
            
            <div class="mt-6 flex flex-col md:flex-row justify-between items-center gap-3">
              <RouterLink v-if="errorRecords > 0" to="/services/rejections" class="text-xs font-bold text-red-600 hover:text-red-700 hover:underline px-2 py-1">
                عرض تقرير المرفوضات التفصيلي ←
              </RouterLink>
              <span v-else></span>
              
              <RouterLink v-if="processedRecords > 0" to="/services/staging" class="text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 px-6 py-2.5 rounded-lg shadow-sm transition-colors">
                مراجعة واعتماد التعديلات
              </RouterLink>
            </div>
          </div>
          
        </transition>

        <!-- Common Wizard Footer -->
        <div class="mt-auto pt-6 border-t border-gray-100 dark:border-gray-800 flex justify-between items-center relative z-10">
          <button 
            v-if="currentStep < 4"
            @click="resetWizard"
            :disabled="isUploading || currentStep === 3"
            class="px-5 py-2 text-xs font-bold text-gray-500 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-700 rounded-lg transition-colors disabled:opacity-50"
          >
            إلغاء العملية
          </button>
          
          <button 
            v-if="currentStep === 1"
            :disabled="!selectedFile || isUploading"
            @click="startUpload"
            class="px-6 py-2 text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-lg disabled:opacity-50 transition-colors mr-auto"
          >
            رفع ومطابقة البيانات
          </button>
          
          <button 
            v-else-if="currentStep === 4"
            @click="resetWizard"
            class="px-6 py-2 text-xs font-bold text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 rounded-lg shadow-sm transition-colors mr-auto dark:bg-gray-800 dark:border-gray-600 dark:text-gray-200 dark:hover:bg-gray-700"
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
