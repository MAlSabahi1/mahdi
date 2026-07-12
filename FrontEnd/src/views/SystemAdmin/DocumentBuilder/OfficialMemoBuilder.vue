<template>
  <AdminLayout>
    <div class="space-y-6 pb-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6" dir="rtl">
      
      <!-- Top Action Bar -->
      <div class="flex justify-between items-center bg-white rounded-2xl border border-gray-200 p-5 shadow-sm dark:bg-gray-900 dark:border-gray-800 sticky top-4 z-40">
        <div>
          <h1 class="text-xl font-bold text-gray-900 dark:text-white">منشئ المذكرات الرسمية</h1>
          <p class="text-sm text-gray-500 dark:text-gray-400">التصميم الحكومي الاحترافي المعتمد للخطابات والتعاميم</p>
        </div>
        <div class="flex gap-3">
          <button @click="resetForm"
            class="rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 transition-colors dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 cursor-pointer">
            إفراغ الحقول
          </button>
          <button @click="previewMemo"
            class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors cursor-pointer">
            <svg class="h-4.5 w-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
            معاينة وطباعة المذكرة
          </button>
        </div>
      </div>

      <!-- Document Type Selection -->
      <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900 shadow-sm relative overflow-visible">
        <h3 class="mb-5 text-lg font-bold text-gray-900 dark:text-white border-b border-gray-100 pb-3 dark:border-gray-800">نوع المذكرة وتخصيصاتها</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">اختر نوع الوثيقة</label>
            <div class="relative z-20 bg-transparent">
              <select v-model="form.documentType" @change="handleDocumentTypeChange" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                <option value="MEMO">مذكرة عادية / تغطية</option>
                <option value="CIRCULAR">تعميم</option>
                <option value="ATTENTION_NOTICE">لفت نظر / عقوبة</option>
                <option value="WORK_COMMENCEMENT">مباشرة عمل</option>
              </select>
              <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
              </span>
            </div>
            <p class="mt-2 text-xs text-gray-500 dark:text-gray-400">يؤثر هذا الخيار على هيكل المذكرة (مثل إظهار جداول الأفراد للفت النظر).</p>
          </div>
        </div>
      </div>

      <!-- Section 1: Security and Metadata -->
      <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900 shadow-sm relative overflow-visible">
        <h3 class="mb-5 text-lg font-bold text-gray-900 dark:text-white border-b border-gray-100 pb-3 dark:border-gray-800">التوثيق والسرية (أعلى الترويسة)</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          
          <div class="lg:col-span-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">التصنيف الأمني (الختم الأوسط)</label>
            <div class="relative z-20 bg-transparent">
              <select v-model="form.securityLevel" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                <option value="NORMAL">عادي (بدون ختم)</option>
                <option value="SECRET">سري</option>
                <option value="TOP_SECRET">سري للغاية</option>
                <option value="URGENT">عاجل فوراً</option>
                <option value="CUSTOM">مخصص (كتابة حرة)</option>
              </select>
              <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
              </span>
            </div>
          </div>
          
          <template v-if="form.securityLevel === 'CUSTOM'">
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">النص المخصص للختم</label>
              <input v-model="form.securityCustomText" type="text" placeholder="مثال: مسودة" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500">
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">لون الختم</label>
              <input v-model="form.securityCustomColor" type="color" class="block w-full h-11 rounded-lg border border-gray-300 bg-transparent px-1 py-1 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:focus:border-brand-500 cursor-pointer">
            </div>
          </template>

          <div class="col-span-full border-t border-gray-100 dark:border-gray-800 my-2"></div>

          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الرقم / المرجع</label>
            <input v-model="form.referenceNo" type="text" placeholder="يترك فارغاً لليدوي" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500">
          </div>
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">التاريخ</label>
            <input v-model="form.docDate" type="text" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500">
          </div>
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الموافق</label>
            <input v-model="form.correspondingDate" type="text" placeholder="يترك فارغاً" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500">
          </div>
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">المرفقات</label>
            <input v-model="form.attachments" type="text" placeholder="يترك فارغاً" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500">
          </div>

          <div class="col-span-full">
            <label class="flex items-center cursor-pointer">
              <input v-model="form.bilingual" type="checkbox" class="h-5 w-5 rounded border-gray-300 text-brand-600 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-900 dark:focus:ring-brand-600 dark:ring-offset-gray-900">
              <span class="ml-2 rtl:mr-3 rtl:ml-0 text-sm font-medium text-gray-700 dark:text-gray-400">تفعيل الترويسة ثنائية اللغة (عربي / إنجليزي)</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Section 2: Issuer Override -->
      <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900 shadow-sm relative overflow-visible">
        <h3 class="mb-2 text-lg font-bold text-gray-900 dark:text-white">الجهة المُصدرة (يمين الترويسة)</h3>
        <p class="mb-5 text-sm text-gray-500 dark:text-gray-400 border-b border-gray-100 pb-3 dark:border-gray-800">اترك الحقول فارغة لاستخدام بيانات جهتك الافتراضية من النظام.</p>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">السطر الأول (الوزارة)</label>
            <input v-model="form.issuerLine1" type="text" placeholder="مثال: وزارة الداخلية" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500">
          </div>
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">السطر الثاني</label>
            <input v-model="form.issuerLine2" type="text" placeholder="مثال: قطاع الموارد البشرية" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500">
          </div>
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">السطر الثالث</label>
            <input v-model="form.issuerLine3" type="text" placeholder="مثال: الإدارة العامة للقوى البشرية" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500">
          </div>
        </div>
      </div>

      <!-- Section 3: Addressees and Content -->
      <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900 shadow-sm relative overflow-visible">
        <h3 class="mb-5 text-lg font-bold text-gray-900 dark:text-white border-b border-gray-100 pb-3 dark:border-gray-800">محتوى المذكرة</h3>
        
        <div class="space-y-6">
          <div class="rounded-xl border border-gray-100 bg-gray-50/50 p-4 dark:border-gray-800 dark:bg-gray-800/20">
            <div class="flex items-center justify-between mb-3">
              <label class="block text-sm font-bold text-gray-800 dark:text-gray-200">الجهات المرسل إليها</label>
              <button type="button" @click="addAddressee" class="text-xs font-medium text-brand-600 hover:text-brand-700 dark:text-brand-400 dark:hover:text-brand-300 flex items-center gap-1">
                <svg class="h-3 w-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
                إضافة جهة أخرى
              </button>
            </div>
            
            <datalist id="smart-addressees">
              <option value="المذكور أعلاه"></option>
              <option value="المدير العام للقوى البشرية"></option>
              <option value="مدير عام شرطة المحافظة"></option>
              <option value="قادة الفروع والوحدات الأمنية"></option>
              <option value="مدراء إدارات أمن المحافظة"></option>
              <option value="مدراء أمن المديريات"></option>
              <option value="معالي وزير الداخلية"></option>
            </datalist>

            <div class="space-y-3">
              <div v-for="(item, index) in form.addressees" :key="index" class="flex flex-col md:flex-row gap-3">
                <div class="w-full md:w-32 relative z-20 bg-transparent shrink-0">
                  <select v-model="item.prefix" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-white px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                    <option value="الأخ /">الأخ /</option>
                    <option value="الإخوة /">الإخوة /</option>
                    <option value="معالي /">معالي /</option>
                    <option value="الأخ القائد /">الأخ القائد /</option>
                    <option value="">بدون لقب</option>
                  </select>
                  <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                    <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                  </span>
                </div>
                <div class="flex-1">
                  <input v-model="item.name" list="smart-addressees" type="text" placeholder="الجهة أو الشخص (مثال: مدير الإدارة العامة للقوى البشرية)" class="block w-full h-11 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500">
                </div>
                <div class="w-full md:w-36 relative z-20 bg-transparent shrink-0">
                  <select v-model="item.suffix" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-white px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                    <option value="المحترم">المحترم</option>
                    <option value="المحترمون">المحترمون</option>
                    <option value="حفظه الله">حفظه الله</option>
                    <option value="المحترمة">المحترمة</option>
                    <option value="">بدون ختام</option>
                  </select>
                  <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                    <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                  </span>
                </div>
                <div>
                  <button v-if="form.addressees.length > 1" @click="removeAddressee(index)" class="h-11 px-3 rounded-lg border border-gray-300 bg-white text-gray-500 hover:text-error-600 hover:bg-error-50 hover:border-error-300 transition-colors dark:border-gray-700 dark:bg-gray-900 dark:hover:bg-error-900/30 shadow-theme-xs flex items-center justify-center">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Involved Personnel (Only for ATTENTION_NOTICE or WORK_COMMENCEMENT) -->
          <div v-if="['ATTENTION_NOTICE', 'WORK_COMMENCEMENT'].includes(form.documentType)" class="rounded-xl border border-warning-200 bg-warning-50/50 p-4 dark:border-warning-900/30 dark:bg-warning-900/10 mt-6">
            <div class="flex items-center justify-between mb-4">
              <div>
                <label class="block text-sm font-bold text-warning-800 dark:text-warning-200">الأفراد المعنيون (الجدول المخصص)</label>
                <p class="text-xs text-warning-600 dark:text-warning-400 mt-1">سيتم عرض هؤلاء الأفراد في جدول رسمي أعلى نص المذكرة مباشرة.</p>
              </div>
              <div class="flex gap-2">
                <button type="button" @click="showPersonnelModal = true" class="text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 flex items-center gap-1 px-3 py-2 rounded-lg shadow-sm transition-colors cursor-pointer">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                  البحث في النظام
                </button>
                <button type="button" @click="addInvolvedPersonnel" class="text-xs font-bold text-warning-700 hover:text-warning-800 dark:text-warning-400 flex items-center gap-1 bg-white dark:bg-gray-800 px-3 py-2 rounded-lg border border-warning-300 dark:border-warning-700 shadow-sm transition-colors cursor-pointer">
                  + إضافة يدوية
                </button>
              </div>
            </div>
            
            <div v-if="form.involvedPersonnel.length === 0" class="text-center py-6 text-warning-500 text-sm border-2 border-dashed border-warning-200 rounded-lg dark:border-warning-800/50">
              لم يتم إضافة أي أفراد بعد. اضغط على "إضافة فرد" للبدء.
            </div>
            
            <div v-else class="space-y-3">
              <div v-for="(person, index) in form.involvedPersonnel" :key="index" class="flex flex-col md:flex-row gap-3 items-center bg-white dark:bg-gray-800 p-2.5 rounded-lg border border-warning-200 dark:border-warning-800/50 shadow-sm">
                
                <div class="flex gap-2 w-full md:w-auto">
                  <div class="w-28 shrink-0">
                    <input v-model="person.militaryId" type="text" placeholder="الرقم العسكري" class="block w-full h-10 rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-700">
                  </div>
                  <div class="w-24 shrink-0">
                    <input v-model="person.rank" type="text" placeholder="الرتبة" class="block w-full h-10 rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-700">
                  </div>
                </div>
                
                <div class="flex-1 w-full min-w-[200px]">
                  <input v-model="person.name" type="text" placeholder="الاسم الرباعي أو الخماسي" class="block w-full h-10 rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-700">
                </div>

                <!-- Dynamic Columns -->
                <div class="flex gap-2 w-full md:w-auto" v-if="form.documentType === 'ATTENTION_NOTICE'">
                  <div class="w-full md:w-48 shrink-0">
                    <input v-model="person.clarification" type="text" placeholder="الإيضاح" class="block w-full h-10 rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-700">
                  </div>
                </div>

                <div class="flex flex-col gap-2 w-full md:w-auto" v-else-if="form.documentType === 'WORK_COMMENCEMENT'">
                  <!-- Top Row for Work Commencement -->
                  <div class="flex flex-col md:flex-row gap-2">
                    <div class="w-full md:w-32 shrink-0">
                      <input v-model="person.workplace" type="text" placeholder="مكان العمل" class="block w-full h-10 rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-700">
                    </div>
                    <div class="w-full md:w-32 shrink-0">
                      <input v-model="person.serviceLocation" type="text" placeholder="محل الخدمة" class="block w-full h-10 rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-700">
                    </div>
                    <div class="w-full md:w-32 shrink-0">
                      <input v-model="person.notes" type="text" placeholder="ملاحظات" class="block w-full h-10 rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-700">
                    </div>
                  </div>
                  <!-- Sub Row for Work Commencement -->
                  <div class="flex flex-col md:flex-row gap-2 bg-gray-50 dark:bg-gray-900/50 p-2 rounded border border-gray-200 dark:border-gray-700 mt-1">
                    <div class="w-full md:w-32 shrink-0">
                      <input v-model="person.commencementDate" type="date" placeholder="تاريخ المباشرة" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                    </div>
                    <div class="w-full md:w-32 shrink-0">
                      <input v-model="person.nationalId" type="text" placeholder="الرقم الوطني" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                    </div>
                    <div class="w-full md:w-32 shrink-0">
                      <input v-model="person.phone" type="text" placeholder="رقم التلفون" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                    </div>
                    <div class="flex-1 w-full shrink-0">
                      <input v-model="person.secondaryNotes" type="text" placeholder="ملاحظة إضافية" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                    </div>
                  </div>
                </div>

                <div class="w-full sm:w-auto flex justify-end shrink-0">
                  <button type="button" @click="removeInvolvedPersonnel(index)" class="p-2 text-error-500 hover:bg-error-50 rounded-md transition-colors cursor-pointer">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الموضوع الرئيسي (يظهر عريضاً في المنتصف)</label>
            <input v-model="form.subject" type="text" placeholder="مثال: تعميم بخصوص كذا وكذا" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-base font-bold text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500">
          </div>

          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">النص والتفاصيل</label>
            <div class="rounded-lg border border-gray-300 overflow-hidden shadow-theme-xs dark:border-gray-700">
              <CKEditorComponent v-model="form.body" height="300px" />
            </div>
          </div>

          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">القرار / الخلاصة (وعليه...)</label>
            <div class="rounded-lg border border-gray-300 overflow-hidden shadow-theme-xs dark:border-gray-700">
              <CKEditorComponent v-model="form.conclusion" height="200px" />
            </div>
          </div>
        </div>
      </div>

      <!-- Section 4: Signatures -->
      <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900 shadow-sm relative overflow-visible">
        <h3 class="mb-2 text-lg font-bold text-gray-900 dark:text-white">التوقيعات والاعتمادات (أسفل المذكرة)</h3>
        <p class="mb-5 text-sm text-gray-500 dark:text-gray-400 border-b border-gray-100 pb-3 dark:border-gray-800">يتم إدراج بيانات المعتمدين والمراجعين هنا لتظهر بخطوط رسمية دقيقة في ذيل الصفحة.</p>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <!-- Approver -->
          <div class="rounded-xl border border-gray-100 bg-gray-50/50 p-4 dark:border-gray-800 dark:bg-gray-800/20">
            <h4 class="font-bold text-gray-800 dark:text-gray-200 mb-4 border-b border-gray-200 dark:border-gray-700 pb-2 text-center">جهة الاعتماد (يسار)</h4>
            <div class="space-y-4">
              <div>
                <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الصفة</label>
                <input v-model="form.signatures.approver.title" type="text" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
              </div>
              <div>
                <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الرتبة</label>
                <input v-model="form.signatures.approver.rank" type="text" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
              </div>
              <div>
                <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الاسم</label>
                <input v-model="form.signatures.approver.name" type="text" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
              </div>
            </div>
          </div>

          <!-- Reviewer -->
          <div class="rounded-xl border border-gray-100 bg-gray-50/50 p-4 dark:border-gray-800 dark:bg-gray-800/20">
            <h4 class="font-bold text-gray-800 dark:text-gray-200 mb-4 border-b border-gray-200 dark:border-gray-700 pb-2 text-center">جهة المراجعة (وسط)</h4>
            <div class="space-y-4">
              <div>
                <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الصفة</label>
                <input v-model="form.signatures.reviewer.title" type="text" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
              </div>
              <div>
                <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الرتبة</label>
                <input v-model="form.signatures.reviewer.rank" type="text" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
              </div>
              <div>
                <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الاسم</label>
                <input v-model="form.signatures.reviewer.name" type="text" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
              </div>
            </div>
          </div>

          <!-- Preparer -->
          <div class="rounded-xl border border-gray-100 bg-gray-50/50 p-4 dark:border-gray-800 dark:bg-gray-800/20">
            <h4 class="font-bold text-gray-800 dark:text-gray-200 mb-4 border-b border-gray-200 dark:border-gray-700 pb-2 text-center">جهة الإعداد (يمين)</h4>
            <div class="space-y-4">
              <div>
                <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الصفة</label>
                <input v-model="form.signatures.preparer.title" type="text" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
              </div>
              <div>
                <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الرتبة</label>
                <input v-model="form.signatures.preparer.rank" type="text" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
              </div>
              <div>
                <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الاسم</label>
                <input v-model="form.signatures.preparer.name" type="text" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
              </div>
            </div>
          </div>

        </div>
      </div>

    </div>

    <!-- Personnel Search Modal -->
    <div v-if="showPersonnelModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-gray-900/50 backdrop-blur-sm">
      <div class="bg-white dark:bg-gray-800 rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden animate-fade-in-up">
        <div class="flex justify-between items-center p-5 border-b border-gray-100 dark:border-gray-700">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <svg class="w-6 h-6 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
            البحث في قاعدة بيانات الأفراد
          </h3>
          <button @click="showPersonnelModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
        <div class="p-5">
          <div class="mb-4">
            <div class="relative">
              <input v-model="searchQuery" type="text" placeholder="ابحث بالرقم العسكري أو الاسم..." class="w-full h-12 pl-4 pr-11 rounded-xl border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700/50 focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 dark:text-white transition-all">
              <svg class="w-5 h-5 absolute top-3.5 right-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>
          </div>
          <div class="max-h-[300px] overflow-y-auto border border-gray-200 dark:border-gray-700 rounded-lg">
            <table class="w-full text-sm text-right">
              <thead class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-300 sticky top-0">
                <tr>
                  <th class="px-4 py-3">الرقم العسكري</th>
                  <th class="px-4 py-3">الرتبة</th>
                  <th class="px-4 py-3">الاسم</th>
                  <th class="px-4 py-3">الإجراء</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="dbPerson in filteredMockPersonnel" :key="dbPerson.militaryId" class="border-b dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600/50 transition-colors">
                  <td class="px-4 py-3 font-mono font-medium text-gray-900 dark:text-white">{{ dbPerson.militaryId }}</td>
                  <td class="px-4 py-3">{{ dbPerson.rank }}</td>
                  <td class="px-4 py-3">{{ dbPerson.name }}</td>
                  <td class="px-4 py-3">
                    <button @click="selectPersonFromDb(dbPerson)" class="text-xs bg-brand-100 text-brand-700 hover:bg-brand-200 px-3 py-1.5 rounded font-bold transition-colors dark:bg-brand-900/30 dark:text-brand-300 dark:hover:bg-brand-900/50">
                      اختيار وإضافة
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import CKEditorComponent from '@/components/common/CKEditorComponent.vue'

const router = useRouter()
const showPersonnelModal = ref(false)
const searchQuery = ref('')

const mockDatabasePersonnel = [
  { militaryId: '7001234', rank: 'رائد', name: 'أحمد علي عبدالله صالح', nationalId: '10203040506', phone: '777123456' },
  { militaryId: '7009876', rank: 'ملازم أول', name: 'محمد حسين سالم', nationalId: '10987654321', phone: '733987654' },
  { militaryId: '8004567', rank: 'نقيب', name: 'خالد سعيد القحطاني', nationalId: '10555666777', phone: '711223344' },
  { militaryId: '9001122', rank: 'مساعد', name: 'عبدالله يحيى محمد', nationalId: '10111222333', phone: '700998877' }
]

const filteredMockPersonnel = computed(() => {
  if (!searchQuery.value) return mockDatabasePersonnel
  return mockDatabasePersonnel.filter(p => 
    p.name.includes(searchQuery.value) || p.militaryId.includes(searchQuery.value)
  )
})

const selectPersonFromDb = (dbPerson: any) => {
  if (!form.value.involvedPersonnel) form.value.involvedPersonnel = []
  form.value.involvedPersonnel.push({
    militaryId: dbPerson.militaryId,
    rank: dbPerson.rank,
    name: dbPerson.name,
    clarification: '',
    workplace: '',
    serviceLocation: '',
    notes: '',
    secondaryNotes: '',
    commencementDate: '',
    nationalId: dbPerson.nationalId,
    phone: dbPerson.phone
  })
  showPersonnelModal.value = false
  searchQuery.value = ''
}

const defaultForm = {
  documentType: 'MEMO',
  referenceNo: '',
  docDate: new Date().toLocaleDateString('en-GB', { year: 'numeric', month: '2-digit', day: '2-digit' }).split('/').reverse().join('/') + 'م',
  correspondingDate: '',
  attachments: '',
  bilingual: false,
  securityLevel: 'NORMAL',
  securityCustomText: '',
  securityCustomColor: '#991b1b',
  issuerLine1: '',
  issuerLine2: '',
  issuerLine3: '',
  addressees: [
    { prefix: 'الأخ /', type: 'TEXT', entityId: null, name: 'مدير عام شرطة المحافظة', suffix: 'المحترم' }
  ],
  involvedPersonnel: [],
  subject: 'تعميم',
  body: '<p>في البدء نهديكم أطيب التحيات، راجين لكم التوفيق بمهام عملكم..</p><p>بصدد الموضوع أعلاه... (أكمل النص هنا)</p><p>لذلك لزم توجيهكم... وتقبلوا خالص التحيات.</p>',
  conclusion: '<p>وعليه، يتم اتخاذ الإجراءات اللازمة...</p>',
  signatures: {
    approver: {
      title: 'مدير عام شرطة المحافظة',
      rank: '',
      name: ''
    },
    reviewer: {
      title: 'مدير إدارة القوى البشرية',
      rank: '',
      name: ''
    },
    preparer: {
      title: 'قسم الخدمات',
      rank: '',
      name: ''
    }
  }
}

const form = ref(JSON.parse(JSON.stringify(defaultForm)))

const handleDocumentTypeChange = () => {
  if (form.value.documentType === 'ATTENTION_NOTICE') {
    form.value.subject = 'لفت نظر'
    form.value.addressees = [{ prefix: 'الأخ /', type: 'TEXT', entityId: null, name: 'المذكور أعلاه', suffix: 'المحترم' }]
    form.value.body = '<p>تحية طيبة وبعد،،</p><p>بناءً على التجاوزات المرفوعة...</p><p>وعليه، يتم لفت نظر المذكور أعلاه...</p>'
  } else if (form.value.documentType === 'CIRCULAR') {
    form.value.subject = 'تعميم'
    form.value.addressees = [{ prefix: 'الإخوة /', type: 'TEXT', entityId: null, name: 'قادة الفروع والوحدات الأمنية', suffix: 'المحترمون' }]
    form.value.body = '<p>تحية طيبة وبعد،،</p><p>إشارة إلى الموضوع أعلاه...</p><p>وعليه، يتم التوجيه بما يلي...</p>'
  } else if (form.value.documentType === 'WORK_COMMENCEMENT') {
    form.value.subject = 'مباشرة عمل'
    form.value.addressees = [{ prefix: 'الأخ /', type: 'TEXT', entityId: null, name: 'المدير العام للقوى البشرية', suffix: 'المحترم' }]
    form.value.body = '<p>تحية طيبة وبعد،،</p><p>نرفق لكم كشف بأسماء الأفراد المباشرين للعمل لدينا، راجين التكرم بالاطلاع واتخاذ اللازم.</p><p>وتقبلوا خالص التحيات.</p>'
  } else {
    form.value.subject = 'موضوع المذكرة'
    form.value.body = '<p>في البدء نهديكم أطيب التحيات، راجين لكم التوفيق بمهام عملكم..</p><p>بصدد الموضوع أعلاه... (أكمل النص هنا)</p><p>لذلك لزم توجيهكم... وتقبلوا خالص التحيات.</p>'
  }
}

const addAddressee = () => {
  form.value.addressees.push({ prefix: 'الأخ /', type: 'TEXT', entityId: null, name: '', suffix: 'المحترم' })
}

const removeAddressee = (index: number) => {
  form.value.addressees.splice(index, 1)
}

const addInvolvedPersonnel = () => {
  if (!form.value.involvedPersonnel) form.value.involvedPersonnel = []
  form.value.involvedPersonnel.push({ militaryId: '', rank: '', name: '', clarification: '', workplace: '', serviceLocation: '', notes: '', secondaryNotes: '', commencementDate: '', nationalId: '', phone: '' })
}

const removeInvolvedPersonnel = (index: number) => {
  form.value.involvedPersonnel.splice(index, 1)
}

const resetForm = () => {
  if(confirm('هل أنت متأكد من مسح جميع الحقول؟')) {
    form.value = JSON.parse(JSON.stringify(defaultForm))
  }
}

const previewMemo = () => {
  localStorage.setItem('official_memo_draft', JSON.stringify(form.value))
  window.open(router.resolve('/admin/documents/memo-preview').href, '_blank')
}

onMounted(() => {
  const draftStr = localStorage.getItem('official_memo_draft')
  if (draftStr) {
    try {
      const draft = JSON.parse(draftStr)
      form.value = { ...defaultForm, ...draft, signatures: { ...defaultForm.signatures, ...draft.signatures } }
      // Migration for older drafts
      if (!form.value.documentType) form.value.documentType = 'MEMO'
      if (!form.value.involvedPersonnel) form.value.involvedPersonnel = []
      if (form.value.addressees && form.value.addressees.length > 0) {
        if (!('prefix' in form.value.addressees[0])) {
          form.value.addressees = form.value.addressees.map((a: any) => ({
            prefix: a.name.startsWith('الإخوة') ? 'الإخوة /' : (a.name ? 'الأخ /' : ''),
            type: 'TEXT',
            entityId: null,
            name: a.name.replace(/^(الأخ |الإخوة |معالي )?\/?\s*/, ''), // Strip old prefix from name if any
            suffix: a.suffix || 'المحترم'
          }))
        }
      } else {
        form.value.addressees = [{ prefix: 'الأخ /', type: 'TEXT', entityId: null, name: draft.to_name || '', suffix: 'المحترم' }]
      }
    } catch(e) {}
  }
})
</script>
