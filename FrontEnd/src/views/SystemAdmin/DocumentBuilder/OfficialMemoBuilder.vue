<template>
  <AdminLayout>
    <div class="space-y-6 pb-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6" dir="rtl">
      
      <!-- Top Action Bar -->
      <div class="flex justify-between items-center bg-white rounded-2xl border border-gray-200 p-5 shadow-sm dark:bg-gray-900 dark:border-gray-800 sticky top-4 z-40">
        <div>
          <h1 class="text-xl font-bold text-gray-900 dark:text-white">
            {{ route.query.type === 'ATTENTION_NOTICE' ? 'منشئ لفت نظر / عقوبة' : route.query.type === 'WORK_COMMENCEMENT' ? 'منشئ مباشرة عمل' : route.query.type === 'CIRCULAR' ? 'منشئ تعميم' : route.query.type === 'MEMO' ? 'منشئ مذكرة تغطية' : 'منشئ المذكرات الرسمية' }}
          </h1>
          <p class="text-sm text-gray-500 dark:text-gray-400">التصميم الحكومي الاحترافي المعتمد للخطابات والتعاميم</p>
        </div>
        <div class="flex gap-2 flex-wrap">
          <button @click="resetForm"
            class="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 transition-colors dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 cursor-pointer">
            إفراغ الحقول
          </button>
          <button @click="createNewTemplate"
            class="flex items-center gap-1 rounded-lg border border-brand-200 bg-brand-50 px-3 py-2 text-sm font-medium text-brand-700 shadow-theme-xs hover:bg-brand-100 transition-colors dark:border-brand-800/50 dark:bg-brand-900/30 dark:text-brand-300 dark:hover:bg-brand-900/50 cursor-pointer">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
            مسودة جديدة
          </button>
          <button @click="saveAsNewTemplate"
            class="flex items-center gap-1 rounded-lg bg-brand-600 px-3 py-2 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-700 transition-colors cursor-pointer">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path></svg>
            حفظ كقالب جديد
          </button>
          <button @click="saveExistingTemplate"
            class="flex items-center gap-1 rounded-lg bg-indigo-600 px-3 py-2 text-sm font-medium text-white shadow-theme-xs hover:bg-indigo-700 transition-colors cursor-pointer">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path></svg>
            حفظ التعديلات
          </button>
          <button @click="previewMemo"
            class="flex items-center gap-1 rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white shadow-theme-xs hover:bg-black transition-colors cursor-pointer">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
            معاينة
          </button>
        </div>
      </div>

      <!-- Document Type Selection -->
      <div v-if="!route.query.type" class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900 shadow-sm relative overflow-visible">
        <h3 class="mb-5 text-lg font-bold text-gray-900 dark:text-white border-b border-gray-100 pb-3 dark:border-gray-800">نوع المذكرة وتخصيصاتها</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">اختر نوع الوثيقة</label>
            <div class="relative z-20 bg-transparent">
              <select v-model="form.documentType" @change="handleDocumentTypeChange" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                <option value="MEMO">مذكرة عادية / تغطية</option>
                <option value="CIRCULAR">تعميم</option>
                <option value="PERSONNEL_MEMO">مذكرة لأفراد</option>
                <option value="CORRECTION">مذكرة تصحيح بيانات</option>
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
                <div class="flex-1 flex gap-2">
                  <input v-model="item.name" type="text" placeholder="الجهة أو الشخص (يمكنك الكتابة أو البحث)" class="block w-full h-11 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500">
                  <button type="button" @click="showEntityModalForIndex = Number(index)" class="shrink-0 h-11 px-4 rounded-lg border border-brand-200 bg-brand-50 text-brand-700 hover:bg-brand-100 hover:border-brand-300 transition-colors flex items-center gap-2 font-bold text-xs dark:bg-brand-900/20 dark:border-brand-800 dark:text-brand-300 dark:hover:bg-brand-900/40">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                    دليل الجهات
                  </button>
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
                  <button v-if="form.addressees.length > 1" @click="removeAddressee(Number(index))" class="h-11 px-3 rounded-lg border border-gray-300 bg-white text-gray-500 hover:text-error-600 hover:bg-error-50 hover:border-error-300 transition-colors dark:border-gray-700 dark:bg-gray-900 dark:hover:bg-error-900/30 shadow-theme-xs flex items-center justify-center">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Involved Personnel (Table for Memos that involve Personnel) -->
          <div v-if="['ATTENTION_NOTICE', 'WORK_COMMENCEMENT', 'PERSONNEL_MEMO', 'CORRECTION'].includes(form.documentType)" class="rounded-xl border border-warning-200 bg-warning-50/50 p-4 dark:border-warning-900/30 dark:bg-warning-900/10 mt-6">
            <div class="flex items-center justify-between mb-4">
              <div>
                <label class="block text-sm font-bold text-warning-800 dark:text-warning-200">الأفراد المعنيون (الجدول المخصص)</label>
                <p class="text-xs text-warning-600 dark:text-warning-400 mt-1">سيتم عرض هؤلاء الأفراد في جدول رسمي أعلى نص المذكرة مباشرة.</p>
              </div>
              <div class="flex gap-2" v-if="form.documentType !== 'CORRECTION'">
                <button type="button" @click="showPersonnelModal = true" class="text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 flex items-center gap-1 px-3 py-2 rounded-lg shadow-sm transition-colors cursor-pointer">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                  البحث في النظام
                </button>

                <button type="button" @click="addInvolvedPersonnel" class="text-xs font-bold text-warning-700 hover:text-warning-800 dark:text-warning-400 flex items-center gap-1 bg-white dark:bg-gray-800 px-3 py-2 rounded-lg border border-warning-300 dark:border-warning-700 shadow-sm transition-colors cursor-pointer">
                  + إضافة يدوية
                </button>
              </div>
            </div>
            
            <!-- Dynamic Columns Selector -->
            <div v-if="['PERSONNEL_MEMO', 'CORRECTION'].includes(form.documentType)" class="bg-white dark:bg-gray-800 rounded-lg p-3 mb-4 border border-warning-200 dark:border-warning-800 shadow-sm">
              <div class="flex items-center justify-between mb-3 border-b border-gray-100 dark:border-gray-700 pb-3">
                <h4 class="text-xs font-bold text-gray-700 dark:text-gray-300 flex items-center gap-1">
                  <svg class="w-4 h-4 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"></path></svg>
                  الأعمدة الظاهرة في الجدول (اختر ما تريد طباعته)
                </h4>
                <label class="flex items-center gap-2 cursor-pointer bg-brand-50 dark:bg-brand-900/30 px-3 py-1.5 rounded-lg border border-brand-200 dark:border-brand-800">
                  <input type="checkbox" v-model="form.includeTable" class="w-4 h-4 text-brand-600 rounded border-gray-300 focus:ring-brand-500 cursor-pointer">
                  <span class="text-xs font-bold text-brand-800 dark:text-brand-300">تضمين وطباعة الجدول داخل المذكرة</span>
                </label>
              </div>
              <div class="flex flex-wrap gap-2 select-none" :class="{'opacity-50 pointer-events-none': form.includeTable === false}" v-if="form.documentType === 'PERSONNEL_MEMO'">
                <label class="flex items-center gap-1.5 cursor-pointer px-2.5 py-1.5 rounded-md text-xs font-bold border transition-colors" :class="form.visibleColumns.militaryId ? 'bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800' : 'bg-gray-50 border-gray-200 text-gray-500 dark:bg-gray-800 dark:border-gray-700'">
                  <input type="checkbox" v-model="form.visibleColumns.militaryId" class="hidden"> الرقم العسكري
                </label>
                <label class="flex items-center gap-1.5 cursor-pointer px-2.5 py-1.5 rounded-md text-xs font-bold border transition-colors" :class="form.visibleColumns.rank ? 'bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800' : 'bg-gray-50 border-gray-200 text-gray-500 dark:bg-gray-800 dark:border-gray-700'">
                  <input type="checkbox" v-model="form.visibleColumns.rank" class="hidden"> الرتبة
                </label>
                <label class="flex items-center gap-1.5 cursor-pointer px-2.5 py-1.5 rounded-md text-xs font-bold border transition-colors bg-brand-50 border-brand-200 text-brand-700 opacity-80 cursor-not-allowed">
                  <input type="checkbox" :checked="true" disabled class="hidden"> الاسم (إلزامي)
                </label>
                <label class="flex items-center gap-1.5 cursor-pointer px-2.5 py-1.5 rounded-md text-xs font-bold border transition-colors" :class="form.visibleColumns.nationalId ? 'bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800' : 'bg-gray-50 border-gray-200 text-gray-500 dark:bg-gray-800 dark:border-gray-700'">
                  <input type="checkbox" v-model="form.visibleColumns.nationalId" class="hidden"> الرقم الوطني
                </label>
                <label class="flex items-center gap-1.5 cursor-pointer px-2.5 py-1.5 rounded-md text-xs font-bold border transition-colors" :class="form.visibleColumns.workplace ? 'bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800' : 'bg-gray-50 border-gray-200 text-gray-500 dark:bg-gray-800 dark:border-gray-700'">
                  <input type="checkbox" v-model="form.visibleColumns.workplace" class="hidden"> مكان العمل
                </label>
                <label class="flex items-center gap-1.5 cursor-pointer px-2.5 py-1.5 rounded-md text-xs font-bold border transition-colors" :class="form.visibleColumns.serviceLocation ? 'bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800' : 'bg-gray-50 border-gray-200 text-gray-500 dark:bg-gray-800 dark:border-gray-700'">
                  <input type="checkbox" v-model="form.visibleColumns.serviceLocation" class="hidden"> محل الخدمة
                </label>
                <label class="flex items-center gap-1.5 cursor-pointer px-2.5 py-1.5 rounded-md text-xs font-bold border transition-colors" :class="form.visibleColumns.status ? 'bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800' : 'bg-gray-50 border-gray-200 text-gray-500 dark:bg-gray-800 dark:border-gray-700'">
                  <input type="checkbox" v-model="form.visibleColumns.status" class="hidden"> الحالة
                </label>
                <label class="flex items-center gap-1.5 cursor-pointer px-2.5 py-1.5 rounded-md text-xs font-bold border transition-colors" :class="form.visibleColumns.jobTitle ? 'bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800' : 'bg-gray-50 border-gray-200 text-gray-500 dark:bg-gray-800 dark:border-gray-700'">
                  <input type="checkbox" v-model="form.visibleColumns.jobTitle" class="hidden"> المسمى الوظيفي
                </label>
                <label class="flex items-center gap-1.5 cursor-pointer px-2.5 py-1.5 rounded-md text-xs font-bold border transition-colors" :class="form.visibleColumns.position ? 'bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800' : 'bg-gray-50 border-gray-200 text-gray-500 dark:bg-gray-800 dark:border-gray-700'">
                  <input type="checkbox" v-model="form.visibleColumns.position" class="hidden"> المنصب
                </label>
                <label class="flex items-center gap-1.5 cursor-pointer px-2.5 py-1.5 rounded-md text-xs font-bold border transition-colors" :class="form.visibleColumns.qualification ? 'bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800' : 'bg-gray-50 border-gray-200 text-gray-500 dark:bg-gray-800 dark:border-gray-700'">
                  <input type="checkbox" v-model="form.visibleColumns.qualification" class="hidden"> المؤهل
                </label>
                <label class="flex items-center gap-1.5 cursor-pointer px-2.5 py-1.5 rounded-md text-xs font-bold border transition-colors" :class="form.visibleColumns.joinDate ? 'bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800' : 'bg-gray-50 border-gray-200 text-gray-500 dark:bg-gray-800 dark:border-gray-700'">
                  <input type="checkbox" v-model="form.visibleColumns.joinDate" class="hidden"> تاريخ التجنيد
                </label>
                <label class="flex items-center gap-1.5 cursor-pointer px-2.5 py-1.5 rounded-md text-xs font-bold border transition-colors" :class="form.visibleColumns.commencementDate ? 'bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800' : 'bg-gray-50 border-gray-200 text-gray-500 dark:bg-gray-800 dark:border-gray-700'">
                  <input type="checkbox" v-model="form.visibleColumns.commencementDate" class="hidden"> تاريخ المباشرة
                </label>
                <label class="flex items-center gap-1.5 cursor-pointer px-2.5 py-1.5 rounded-md text-xs font-bold border transition-colors" :class="form.visibleColumns.phone ? 'bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800' : 'bg-gray-50 border-gray-200 text-gray-500 dark:bg-gray-800 dark:border-gray-700'">
                  <input type="checkbox" v-model="form.visibleColumns.phone" class="hidden"> الهاتف
                </label>
                <label class="flex items-center gap-1.5 cursor-pointer px-2.5 py-1.5 rounded-md text-xs font-bold border transition-colors" :class="form.visibleColumns.clarification ? 'bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800' : 'bg-gray-50 border-gray-200 text-gray-500 dark:bg-gray-800 dark:border-gray-700'">
                  <input type="checkbox" v-model="form.visibleColumns.clarification" class="hidden"> الإيضاح
                </label>
                <label class="flex items-center gap-1.5 cursor-pointer px-2.5 py-1.5 rounded-md text-xs font-bold border transition-colors" :class="form.visibleColumns.notes ? 'bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800' : 'bg-gray-50 border-gray-200 text-gray-500 dark:bg-gray-800 dark:border-gray-700'">
                  <input type="checkbox" v-model="form.visibleColumns.notes" class="hidden"> الملاحظات
                </label>
                <!-- أعمدة التصحيح -->
                
                
                
              </div>
            </div>
            <div v-if="form.involvedPersonnel.length === 0" class="text-center py-6 text-warning-500 text-sm border-2 border-dashed border-warning-200 rounded-lg dark:border-warning-800/50">
              لم يتم إضافة أي أفراد بعد. اضغط على "البحث في النظام" للبدء.
            </div>
            
            <div v-else class="space-y-3">
              <div v-for="(person, index) in form.involvedPersonnel" :key="index" class="flex flex-col md:flex-row gap-3 items-center bg-white dark:bg-gray-800 p-2.5 rounded-lg border border-warning-200 dark:border-warning-800/50 shadow-sm">
                
                <div class="flex flex-col md:flex-row gap-3 items-center" v-if="form.documentType !== 'CORRECTION'">
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
                      <input v-model="person.commencementDate" type="text" placeholder="تاريخ المباشرة" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
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


                <!-- CORRECTION Custom Layout -->
                <div v-if="form.documentType === 'CORRECTION'">
                  <div class="grid grid-cols-1 md:grid-cols-6 gap-3 mt-2">
                    <div class="col-span-1">
                      <label class="block text-[0.65rem] font-bold text-gray-500 mb-1">الرقم العسكري</label>
                      <input v-model="person.militaryId" type="text" placeholder="أدخل الرقم" class="block w-full h-9 rounded border border-gray-300 bg-gray-50 px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-900">
                    </div>
                    <div class="col-span-1">
                      <label class="block text-[0.65rem] font-bold text-gray-500 mb-1">الرتبة</label>
                      <input v-model="person.rank" type="text" placeholder="الرتبة" class="block w-full h-9 rounded border border-gray-300 bg-gray-50 px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-900">
                    </div>
                    <div class="col-span-2">
                      <label class="block text-[0.65rem] font-bold text-brand-600 mb-1">الاسم الصحيح (المعتمد)</label>
                      <input v-model="person.correctName" type="text" placeholder="الاسم الصحيح" class="block w-full h-9 rounded border border-brand-300 bg-brand-50 px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-brand-700 dark:bg-brand-900/20 font-bold">
                    </div>
                    <div class="col-span-2">
                      <label class="block text-[0.65rem] font-bold text-error-600 mb-1">الاسم الخطأ (القديم)</label>
                      <input v-model="person.wrongName" type="text" placeholder="الاسم الخطأ" class="block w-full h-9 rounded border border-error-300 bg-error-50 px-2 py-1 text-xs focus:border-error-500 focus:ring-1 focus:ring-error-500 dark:border-error-700 dark:bg-error-900/20">
                    </div>
                    <div class="col-span-3">
                      <label class="block text-[0.65rem] font-bold text-gray-500 mb-1">المطلوب تصحيحه</label>
                      <input v-model="person.correctionTarget" type="text" placeholder="مثال: الاسم الثاني، اللقب..." class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                    </div>
                    <div class="col-span-3">
                      <label class="block text-[0.65rem] font-bold text-gray-500 mb-1">ملاحظات إضافية</label>
                      <input v-model="person.notes" type="text" placeholder="ملاحظات" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                    </div>
                  </div>
                </div>
                <div class="flex flex-wrap gap-2 w-full mt-2 bg-gray-50 dark:bg-gray-900/50 p-2 rounded border border-gray-200 dark:border-gray-700" v-else-if="form.documentType === 'PERSONNEL_MEMO'">
                  <div class="w-full md:w-32 shrink-0" v-if="form.visibleColumns.nationalId">
                    <input v-model="person.nationalId" type="text" placeholder="الرقم الوطني" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                  </div>
                  <div class="w-full md:w-32 shrink-0" v-if="form.visibleColumns.status">
                    <input v-model="person.status" type="text" placeholder="الحالة" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                  </div>
                  <div class="w-full md:w-32 shrink-0" v-if="form.visibleColumns.jobTitle">
                    <input v-model="person.jobTitle" type="text" placeholder="المسمى الوظيفي" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                  </div>
                  <div class="w-full md:w-32 shrink-0" v-if="form.visibleColumns.position">
                    <input v-model="person.position" type="text" placeholder="المنصب" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                  </div>
                  <div class="w-full md:w-32 shrink-0" v-if="form.visibleColumns.qualification">
                    <input v-model="person.qualification" type="text" placeholder="المؤهل" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                  </div>
                  <div class="w-full md:w-32 shrink-0" v-if="form.visibleColumns.joinDate">
                    <input v-model="person.joinDate" type="text" placeholder="تاريخ التجنيد" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                  </div>
                  <div class="w-full md:w-32 shrink-0" v-if="form.visibleColumns.workplace">
                    <input v-model="person.workplace" type="text" placeholder="مكان العمل" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                  </div>
                  <div class="w-full md:w-32 shrink-0" v-if="form.visibleColumns.serviceLocation">
                    <input v-model="person.serviceLocation" type="text" placeholder="محل الخدمة" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                  </div>
                  <div class="w-full md:w-32 shrink-0" v-if="form.visibleColumns.commencementDate">
                    <input v-model="person.commencementDate" type="text" placeholder="تاريخ المباشرة" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                  </div>
                  <div class="w-full md:w-32 shrink-0" v-if="form.visibleColumns.phone">
                    <input v-model="person.phone" type="text" placeholder="الهاتف" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                  </div>
                  <div class="w-full md:w-48 shrink-0" v-if="form.visibleColumns.clarification">
                    <input v-model="person.clarification" type="text" placeholder="الإيضاح" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                  </div>
                  
                  <div class="w-full md:w-48 shrink-0" v-if="form.visibleColumns.wrongName">
                    <input v-model="person.wrongName" type="text" placeholder="الاسم الخطأ" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-error-500 focus:ring-1 focus:ring-error-500 dark:border-gray-600 dark:bg-gray-800">
                  </div>
                  
                  <div class="flex-1 min-w-[200px]" v-if="form.visibleColumns.notes">
                    <input v-model="person.secondaryNotes" type="text" placeholder="ملاحظات" class="block w-full h-9 rounded border border-gray-300 bg-white px-2 py-1 text-xs focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-800">
                  </div>
                </div>

                <div class="w-full sm:w-auto flex justify-end shrink-0">
                  <button type="button" @click="removeInvolvedPersonnel(Number(index))" class="p-2 text-error-500 hover:bg-error-50 rounded-md transition-colors cursor-pointer">
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
        <div class="flex justify-between items-center mb-2 border-b border-gray-100 pb-3 dark:border-gray-800">
          <div>
            <h3 class="text-lg font-bold text-gray-900 dark:text-white">التوقيعات والاعتمادات (أسفل المذكرة)</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">يتم إدراج بيانات المعتمدين والمراجعين هنا لتظهر بخطوط رسمية دقيقة في ذيل الصفحة.</p>
          </div>
          <button @click="addSignature" class="bg-brand-50 hover:bg-brand-100 text-brand-600 font-bold py-2 px-4 rounded-lg text-sm transition-colors border border-brand-200">
            + إضافة توقيع جديد
          </button>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mt-5">
          <div v-for="(sig, index) in form.signatures" :key="index" class="rounded-xl border border-gray-100 bg-gray-50/50 p-4 dark:border-gray-800 dark:bg-gray-800/20 relative group">
            <button @click="removeSignature(Number(index))" class="absolute top-3 left-3 text-red-500 hover:text-red-700 bg-red-50 hover:bg-red-100 rounded-full w-8 h-8 flex items-center justify-center transition-colors opacity-0 group-hover:opacity-100">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
            </button>
            <h4 class="font-bold text-gray-800 dark:text-gray-200 mb-4 border-b border-gray-200 dark:border-gray-700 pb-2 text-center pr-8">جهة التوقيع رقم {{ Number(index) + 1 }}</h4>
            <div class="space-y-4">
              <!-- Design 1 (Classic) Inputs -->
              <template v-if="form.signatureSettings.showLabels !== false">
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الصفة</label>
                  <input v-model="sig.title" type="text" placeholder="مثال: مدير الإدارة" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الرتبة</label>
                  <input v-model="sig.rank" type="text" placeholder="مثال: عقيد" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الاسم</label>
                  <input v-model="sig.name" type="text" placeholder="مثال: فلان بن فلان الفلاني" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
                </div>
              </template>

              <!-- Design 2 (Free Text) Inputs -->
              <template v-else>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-brand-700 dark:text-brand-400">مربع النص الحر (محرر متقدم)</label>
                  <div class="rounded-lg border border-brand-300 overflow-hidden shadow-theme-xs dark:border-brand-700">
                    <CKEditorComponent v-model="sig.freeText" height="150px" placeholder="مثال:&#10;عقيد&#10;مهدي مهدي ابوعلي&#10;وزير التربية" :toolbar="['fontFamily', 'fontSize', 'fontColor', '|', 'bold', 'alignment', '|', 'undo', 'redo']" />
                  </div>
                  <p class="text-xs text-brand-600 mt-2 font-semibold">استخدم هذا المحرر لتغيير الخط والمحاذاة لكل سطر بشكل مستقل!</p>
                </div>
              </template>
              <div class="pt-2">
                <label class="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" v-model="sig.showSeal" class="w-5 h-5 text-brand-600 rounded focus:ring-brand-500 border-gray-300">
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300">إظهار الختم الرسمي هنا</span>
                </label>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Additional Signature Layout Options -->
        <div class="mt-6 p-4 rounded-xl border border-gray-200 bg-gray-50/50 dark:border-gray-800 dark:bg-gray-800/30 flex flex-col md:flex-row gap-6 items-start md:items-center justify-between">
          <div>
            <h4 class="font-bold text-gray-800 dark:text-gray-200 mb-1">تصميم وشكل التوقيعات</h4>
            <p class="text-xs text-gray-500 dark:text-gray-400">اختر التصميم المناسب لقوالب التوقيع</p>
          </div>
          <div class="flex flex-col gap-3 w-full md:w-auto">
            
            <div class="flex flex-wrap gap-4 p-1.5 bg-gray-200/50 dark:bg-gray-700/50 rounded-lg w-full md:w-fit">
              <label class="flex-1 md:flex-none flex items-center justify-center gap-2 cursor-pointer px-4 py-2 rounded-md transition-colors" :class="form.signatureSettings.showLabels !== false ? 'bg-white shadow-sm dark:bg-gray-800' : 'hover:bg-gray-200 dark:hover:bg-gray-700'">
                <input type="radio" v-model="form.signatureSettings.showLabels" :value="true" class="hidden">
                <span class="text-sm font-bold" :class="form.signatureSettings.showLabels !== false ? 'text-brand-600 dark:text-brand-400' : 'text-gray-600 dark:text-gray-400'">تصميم 1 (الرسمي - مربعات ونقاط)</span>
              </label>
              <label class="flex-1 md:flex-none flex items-center justify-center gap-2 cursor-pointer px-4 py-2 rounded-md transition-colors" :class="form.signatureSettings.showLabels === false ? 'bg-white shadow-sm dark:bg-gray-800' : 'hover:bg-gray-200 dark:hover:bg-gray-700'">
                <input type="radio" v-model="form.signatureSettings.showLabels" :value="false" class="hidden">
                <span class="text-sm font-bold" :class="form.signatureSettings.showLabels === false ? 'text-brand-600 dark:text-brand-400' : 'text-gray-600 dark:text-gray-400'">تصميم 2 (سادة - نص حر بدون نقاط)</span>
              </label>
            </div>

            <label class="flex items-center gap-2 cursor-pointer bg-white dark:bg-gray-900 px-4 py-2.5 rounded-lg border border-gray-200 dark:border-gray-700 shadow-theme-xs hover:border-brand-300 transition-colors w-fit self-end">
              <input type="checkbox" v-model="form.signatureSettings.showFrame" class="w-4 h-4 text-brand-600 rounded focus:ring-brand-500 border-gray-300">
              <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">إظهار الإطار الخارجي (التوقيعات والاعتمادات)</span>
            </label>

          </div>
        </div>
      </div>

    </div>

    <!-- Typography Settings (Admin Only) -->
    <div v-if="authStore.user?.authz_profile?.role_code === 'SYSTEM_ADMIN' || authStore.user?.is_superuser" class="mb-8 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-brand-200 dark:border-brand-900/50 overflow-hidden mt-6">
      <div class="p-5 border-b border-brand-100 dark:border-brand-800 bg-brand-50/30 dark:bg-brand-900/10 flex justify-between items-center">
        <h3 class="text-lg font-bold text-brand-900 dark:text-brand-300 flex items-center gap-2">
          <svg class="w-6 h-6 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z"></path></svg>
          مكتبة القوالب الجاهزة وإعدادات التنسيق المتقدمة
        </h3>
      </div>
      
      <!-- Preset Management -->
      <div class="p-4 border-b border-gray-100 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-800/50 flex flex-wrap gap-4 items-end">
        <div class="flex-1 min-w-[200px]">
          <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">حفظ كقالب جديد</label>
          <div class="flex gap-2">
            <input v-model="newPresetName" type="text" placeholder="اسم القالب (مثل: مذكرة رسمية للوزير)" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
            <button @click="savePreset" class="bg-brand-600 text-white px-4 rounded-lg font-bold hover:bg-brand-700 whitespace-nowrap">حفظ الإعدادات</button>
          </div>
        </div>
        <div class="flex-1 min-w-[200px]">
          <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">تحميل قالب محفوظ</label>
          <div class="flex gap-2">
            <select v-model="selectedPresetIndex" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
              <option value="">-- اختر قالباً لتحميله --</option>
              <option v-for="(preset, idx) in savedPresets" :key="idx" :value="idx">{{ preset.name }}</option>
            </select>
            <button @click="loadPreset" class="bg-gray-800 dark:bg-gray-700 text-white px-4 rounded-lg font-bold hover:bg-gray-900 whitespace-nowrap">تطبيق</button>
          </div>
        </div>
        <div>
          <button @click="resetTypography" class="h-10 px-4 rounded-lg border border-red-200 text-red-600 hover:bg-red-50 font-bold bg-white dark:bg-gray-800 dark:border-red-900 dark:text-red-400 dark:hover:bg-red-900/20 whitespace-nowrap">استعادة الافتراضي</button>
        </div>
      </div>

      <div class="p-6">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          <!-- Addressees -->
          <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl border border-gray-200 dark:border-gray-700 flex flex-col">
            <h4 class="font-bold text-gray-800 dark:text-gray-200 mb-3 border-b pb-2 flex justify-between items-center">
              <span>خط الجهات (الإخوة /)</span>
              <label class="flex items-center gap-2 text-sm font-normal cursor-pointer">
                <input type="checkbox" v-model="form.typography.addressee.underline" class="w-4 h-4 text-brand-600 rounded focus:ring-brand-500">
                <span>وضع خط تحت النص</span>
              </label>
            </h4>
            <div class="grid grid-cols-2 gap-3 mb-4">
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">نوع الخط</label>
                <select v-model="form.typography.addressee.family" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
                  <option v-for="font in fontOptions" :key="font.value" :value="font.value">{{ font.label }}</option>
                </select>
              </div>
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">وزن الخط (السماكة)</label>
                <select v-model="form.typography.addressee.weight" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
                  <option value="font-normal">عادي (Normal)</option>
                  <option value="font-bold">عريض (Bold)</option>
                  <option value="font-black">عريض جداً (Black)</option>
                </select>
              </div>
              <div class="col-span-2">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300 flex justify-between">
                  <span>حجم الخط:</span>
                  <span class="text-brand-600">{{ form.typography.addressee.size }}rem</span>
                </label>
                <input type="range" v-model.number="form.typography.addressee.size" min="0.8" max="2.5" step="0.05" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-brand-600">
              </div>
            </div>
            <div class="mt-auto bg-white dark:bg-gray-800 p-3 rounded border border-dashed border-gray-300 flex items-end justify-between overflow-hidden" dir="rtl">
               <div class="leading-none flex items-baseline text-gray-900 dark:text-gray-100" :class="[form.typography.addressee.weight, { 'underline underline-offset-4': form.typography.addressee.underline }]" :style="{ fontSize: form.typography.addressee.size + 'rem', fontFamily: form.typography.addressee.family }">
                 <span class="ml-2">الأخ /</span><span>مدير عام شرطة المحافظة</span>
               </div>
               <div class="text-gray-900 dark:text-gray-100" :class="[form.typography.addressee.weight, { 'underline underline-offset-4': form.typography.addressee.underline }]" :style="{ fontSize: form.typography.addressee.size + 'rem', fontFamily: form.typography.addressee.family }">المحترم</div>
            </div>
          </div>

          <!-- Greeting -->
          <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl border border-gray-200 dark:border-gray-700 flex flex-col">
            <h4 class="font-bold text-gray-800 dark:text-gray-200 mb-3 border-b pb-2 flex justify-between items-center">
              <span>خط التحية (تحية طيبة وبعد)</span>
              <label class="flex items-center gap-2 text-sm font-normal cursor-pointer">
                <input type="checkbox" v-model="form.typography.greeting.underline" class="w-4 h-4 text-brand-600 rounded focus:ring-brand-500">
                <span>وضع خط تحت النص</span>
              </label>
            </h4>
            <div class="grid grid-cols-2 gap-3 mb-4">
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">نوع الخط</label>
                <select v-model="form.typography.greeting.family" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
                  <option v-for="font in fontOptions" :key="font.value" :value="font.value">{{ font.label }}</option>
                </select>
              </div>
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">وزن الخط (السماكة)</label>
                <select v-model="form.typography.greeting.weight" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
                  <option value="font-normal">عادي (Normal)</option>
                  <option value="font-bold">عريض (Bold)</option>
                  <option value="font-black">عريض جداً (Black)</option>
                </select>
              </div>
              <div class="col-span-2">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300 flex justify-between">
                  <span>حجم الخط:</span>
                  <span class="text-brand-600">{{ form.typography.greeting.size }}rem</span>
                </label>
                <input type="range" v-model.number="form.typography.greeting.size" min="0.8" max="2.5" step="0.05" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-brand-600">
              </div>
            </div>
            <div class="mt-auto bg-white dark:bg-gray-800 p-3 rounded border border-dashed border-gray-300 flex items-center justify-center overflow-hidden text-center" dir="rtl">
               <span class="text-gray-900 dark:text-gray-100" :class="[form.typography.greeting.weight, { 'underline underline-offset-4': form.typography.greeting.underline }]" :style="{ fontSize: form.typography.greeting.size + 'rem', fontFamily: form.typography.greeting.family }">
                 تحية طيبة وبعد ،،،
               </span>
            </div>
          </div>

          <!-- Subject -->
          <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl border border-gray-200 dark:border-gray-700 flex flex-col">
            <h4 class="font-bold text-gray-800 dark:text-gray-200 mb-3 border-b pb-2 flex justify-between items-center">
              <span>خط العنوان (الموضوع)</span>
              <label class="flex items-center gap-2 text-sm font-normal cursor-pointer">
                <input type="checkbox" v-model="form.typography.subject.underline" class="w-4 h-4 text-brand-600 rounded focus:ring-brand-500">
                <span>وضع خط تحت النص</span>
              </label>
            </h4>
            <div class="grid grid-cols-2 gap-3 mb-4">
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">نوع الخط</label>
                <select v-model="form.typography.subject.family" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
                  <option v-for="font in fontOptions" :key="font.value" :value="font.value">{{ font.label }}</option>
                </select>
              </div>
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">وزن الخط (السماكة)</label>
                <select v-model="form.typography.subject.weight" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
                  <option value="font-normal">عادي (Normal)</option>
                  <option value="font-bold">عريض (Bold)</option>
                  <option value="font-black">عريض جداً (Black)</option>
                </select>
              </div>
              <div class="col-span-2">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300 flex justify-between">
                  <span>حجم الخط:</span>
                  <span class="text-brand-600">{{ form.typography.subject.size }}rem</span>
                </label>
                <input type="range" v-model.number="form.typography.subject.size" min="0.8" max="2.5" step="0.05" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-brand-600">
              </div>
            </div>
            <div class="mt-auto bg-white dark:bg-gray-800 p-3 rounded border border-dashed border-gray-300 flex items-center justify-center overflow-hidden text-center" dir="rtl">
               <span class="tracking-tight pb-1 inline-block text-gray-900 dark:text-gray-100" :class="[form.typography.subject.weight, { 'border-b-[3px] border-black dark:border-white': form.typography.subject.underline }]" :style="{ fontSize: form.typography.subject.size + 'rem', fontFamily: form.typography.subject.family }">
                 الموضوع / {{ form.subject || 'هنا يكتب الموضوع' }}
               </span>
            </div>
          </div>

          <!-- Body Text -->
          <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl border border-gray-200 dark:border-gray-700 flex flex-col">
            <h4 class="font-bold text-gray-800 dark:text-gray-200 mb-3 border-b pb-2 flex justify-between items-center">
              <span>النص الأساسي (المحتوى)</span>
              <label class="flex items-center gap-2 text-sm font-normal cursor-pointer">
                <input type="checkbox" v-model="form.typography.body.underline" class="w-4 h-4 text-brand-600 rounded focus:ring-brand-500">
                <span>وضع خط تحت النص</span>
              </label>
            </h4>
            <div class="grid grid-cols-2 gap-3 mb-4">
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">نوع الخط</label>
                <select v-model="form.typography.body.family" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
                  <option v-for="font in fontOptions" :key="font.value" :value="font.value">{{ font.label }}</option>
                </select>
              </div>
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">وزن الخط (السماكة)</label>
                <select v-model="form.typography.body.weight" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
                  <option value="font-normal">عادي (Normal)</option>
                  <option value="font-bold">عريض (Bold)</option>
                </select>
              </div>
              <div class="col-span-2">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300 flex justify-between">
                  <span>حجم الخط:</span>
                  <span class="text-brand-600">{{ form.typography.body.size }}rem</span>
                </label>
                <input type="range" v-model.number="form.typography.body.size" min="0.8" max="2.5" step="0.05" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-brand-600">
              </div>
            </div>
            <div class="mt-auto bg-white dark:bg-gray-800 p-3 rounded border border-dashed border-gray-300 overflow-hidden text-justify text-gray-900 dark:text-gray-100" dir="rtl" style="text-justify: inter-word;" :class="[form.typography.body.weight, { 'underline underline-offset-4': form.typography.body.underline }]" :style="{ fontSize: form.typography.body.size + 'rem', fontFamily: form.typography.body.family }">
              هذا النص هو نموذج تجريبي لمعاينة التنسيق الخاص بالرسالة. يتم اختيار الخط والحجم المناسبين للتأكد من المظهر العام والمخرجات.
            </div>
          </div>

          <!-- Conclusion Separator (وعليه) -->
          <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl border border-gray-200 dark:border-gray-700 flex flex-col">
            <h4 class="font-bold text-gray-800 dark:text-gray-200 mb-3 border-b pb-2 flex justify-between items-center">
              <span>خط الفاصل (وعليه :)</span>
              <label class="flex items-center gap-2 text-sm font-normal cursor-pointer">
                <input type="checkbox" v-model="form.typography.conclusionSeparator.underline" class="w-4 h-4 text-brand-600 rounded focus:ring-brand-500">
                <span>وضع خط تحت النص</span>
              </label>
            </h4>
            <div class="grid grid-cols-2 gap-3 mb-4">
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">نوع الخط</label>
                <select v-model="form.typography.conclusionSeparator.family" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
                  <option v-for="font in fontOptions" :key="font.value" :value="font.value">{{ font.label }}</option>
                </select>
              </div>
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">وزن الخط (السماكة)</label>
                <select v-model="form.typography.conclusionSeparator.weight" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
                  <option value="font-normal">عادي (Normal)</option>
                  <option value="font-bold">عريض (Bold)</option>
                  <option value="font-black">عريض جداً (Black)</option>
                </select>
              </div>
              <div class="col-span-2">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300 flex justify-between">
                  <span>حجم الخط:</span>
                  <span class="text-brand-600">{{ form.typography.conclusionSeparator.size }}rem</span>
                </label>
                <input type="range" v-model.number="form.typography.conclusionSeparator.size" min="0.8" max="2.5" step="0.05" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-brand-600">
              </div>
            </div>
            <div class="mt-auto bg-white dark:bg-gray-800 p-3 rounded border border-dashed border-gray-300 overflow-hidden text-right text-gray-900 dark:text-gray-100" dir="rtl">
               <span class="tracking-tight pb-1 inline-block" :class="[form.typography.conclusionSeparator.weight, { 'border-b-[3px] border-black dark:border-white': form.typography.conclusionSeparator.underline }]" :style="{ fontSize: form.typography.conclusionSeparator.size + 'rem', fontFamily: form.typography.conclusionSeparator.family }">وعليه :</span>
            </div>
          </div>

          <!-- Conclusion Body -->
          <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl border border-gray-200 dark:border-gray-700 flex flex-col">
            <h4 class="font-bold text-gray-800 dark:text-gray-200 mb-3 border-b pb-2 flex justify-between items-center">
              <span>نص الختام (الإجراء المطلوب)</span>
              <label class="flex items-center gap-2 text-sm font-normal cursor-pointer">
                <input type="checkbox" v-model="form.typography.conclusionBody.underline" class="w-4 h-4 text-brand-600 rounded focus:ring-brand-500">
                <span>وضع خط تحت النص</span>
              </label>
            </h4>
            <div class="grid grid-cols-2 gap-3 mb-4">
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">نوع الخط</label>
                <select v-model="form.typography.conclusionBody.family" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
                  <option v-for="font in fontOptions" :key="font.value" :value="font.value">{{ font.label }}</option>
                </select>
              </div>
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">وزن الخط (السماكة)</label>
                <select v-model="form.typography.conclusionBody.weight" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
                  <option value="font-normal">عادي (Normal)</option>
                  <option value="font-bold">عريض (Bold)</option>
                  <option value="font-black">عريض جداً (Black)</option>
                </select>
              </div>
              <div class="col-span-2">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300 flex justify-between">
                  <span>حجم الخط:</span>
                  <span class="text-brand-600">{{ form.typography.conclusionBody.size }}rem</span>
                </label>
                <input type="range" v-model.number="form.typography.conclusionBody.size" min="0.8" max="2.5" step="0.05" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-brand-600">
              </div>
            </div>
            <div class="mt-auto bg-white dark:bg-gray-800 p-3 rounded border border-dashed border-gray-300 overflow-hidden text-justify text-gray-900 dark:text-gray-100" dir="rtl" style="text-justify: inter-word;" :class="[form.typography.conclusionBody.weight, { 'underline underline-offset-4': form.typography.conclusionBody.underline }]" :style="{ fontSize: form.typography.conclusionBody.size + 'rem', fontFamily: form.typography.conclusionBody.family }">
              يتم اتخاذ الإجراءات اللازمة حيال الموضوع المذكور أعلاه بشكل عاجل.
            </div>
          </div>

          <!-- Signatures (التوقيعات) -->
          <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl border border-gray-200 dark:border-gray-700 flex flex-col">
            <h4 class="font-bold text-gray-800 dark:text-gray-200 mb-3 border-b pb-2 flex justify-between items-center">
              <span>خط التوقيعات (ذيل الصفحة)</span>
              <label class="flex items-center gap-2 text-sm font-normal cursor-pointer">
                <input type="checkbox" v-model="form.typography.signatures.underline" class="w-4 h-4 text-brand-600 rounded focus:ring-brand-500">
                <span>وضع خط تحت النص</span>
              </label>
            </h4>
            <div class="grid grid-cols-2 gap-3 mb-4">
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">نوع الخط</label>
                <select v-model="form.typography.signatures.family" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
                  <option v-for="font in fontOptions" :key="font.value" :value="font.value">{{ font.label }}</option>
                </select>
              </div>
              <div class="col-span-2 sm:col-span-1">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300">وزن الخط (السماكة)</label>
                <select v-model="form.typography.signatures.weight" class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm h-10">
                  <option value="font-normal">عادي (Normal)</option>
                  <option value="font-bold">عريض (Bold)</option>
                  <option value="font-black">عريض جداً (Black)</option>
                </select>
              </div>
              <div class="col-span-2">
                <label class="block text-sm font-semibold mb-1 text-gray-700 dark:text-gray-300 flex justify-between">
                  <span>حجم الخط:</span>
                  <span class="text-brand-600">{{ form.typography.signatures.size }}rem</span>
                </label>
                <input type="range" v-model.number="form.typography.signatures.size" min="0.8" max="2.5" step="0.05" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-brand-600">
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
    
    <!-- Entities Directory Search Modal -->
    <div v-if="showEntityModalForIndex !== null" class="fixed inset-0 z-[100] flex items-center justify-center bg-gray-900/50 backdrop-blur-sm p-4">
      <div class="bg-white dark:bg-gray-800 rounded-2xl w-full max-w-3xl h-[80vh] flex flex-col shadow-2xl overflow-hidden animate-fade-in-up">
        <div class="flex justify-between items-center p-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <svg class="w-6 h-6 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
            دليل الجهات والإدارات
          </h3>
          <button @click="showEntityModalForIndex = null" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
        <div class="p-5 border-b border-gray-100 dark:border-gray-700 shrink-0">
          <div class="flex justify-between items-center mb-3">
            <span class="text-xs text-gray-400">
              [لأغراض تقنية] حساب المحافظة: {{ authStore.user?.authz_profile?.security_admin_id || 'غير محدد' }} | 
              إجمالي الفروع بالخادم: {{ coreStore.branches.length }} |
              إجمالي الإدارات بالخادم: {{ coreStore.centralDepartments.length }}
            </span>
          </div>
          <div class="relative">
            <input v-model="entitySearchQuery" type="text" placeholder="ابحث عن إدارة، قيادة، فرع، أو مسؤول..." class="w-full h-12 pl-4 pr-11 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 dark:text-white transition-all shadow-sm">
            <svg class="w-5 h-5 absolute top-3.5 right-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
          </div>
        </div>
        <div class="flex-1 overflow-y-auto p-5 bg-gray-50/50 dark:bg-gray-900/20">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-for="group in filteredMockEntities" :key="group.group" class="rounded-xl border border-gray-200 bg-white dark:bg-gray-800 dark:border-gray-700 overflow-hidden shadow-sm">
              <div class="bg-gray-100 dark:bg-gray-700 px-4 py-3 font-bold text-brand-800 dark:text-brand-300 border-b border-gray-200 dark:border-gray-600">
                {{ group.group }}
              </div>
              <ul class="divide-y divide-gray-100 dark:divide-gray-700">
                <li v-for="item in group.items" :key="item.name" class="hover:bg-brand-50 dark:hover:bg-brand-900/20 transition-colors">
                  <button @click="selectEntityFromDb(item)" class="w-full text-right px-4 py-3 flex justify-between items-center group">
                    <span class="font-medium text-gray-800 dark:text-gray-200">{{ item.name }}</span>
                    <span class="text-xs bg-brand-100 text-brand-700 px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity dark:bg-brand-800 dark:text-brand-200">اختيار</span>
                  </button>
                </li>
              </ul>
            </div>
            
            <div v-if="filteredMockEntities.length === 0" class="col-span-full py-12 text-center text-gray-500 dark:text-gray-400">
              <svg class="w-12 h-12 mx-auto mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              لا توجد نتائج مطابقة لبحثك. يمكنك كتابة الاسم يدوياً.
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
                <tr v-if="personnelStore.loading">
                  <td colspan="4" class="px-4 py-8 text-center text-gray-500">جاري البحث...</td>
                </tr>
                <tr v-else-if="personnelStore.records.length === 0">
                  <td colspan="4" class="px-4 py-8 text-center text-gray-500">لا توجد نتائج مطابقة</td>
                </tr>
                <tr v-for="dbPerson in personnelStore.records" :key="dbPerson.military_number" class="border-b dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600/50 transition-colors">
                  <td class="px-4 py-3 font-mono font-medium text-gray-900 dark:text-white">{{ dbPerson.military_number }}</td>
                  <td class="px-4 py-3">{{ dbPerson.rank_name }}</td>
                  <td class="px-4 py-3 font-medium text-gray-800 dark:text-gray-200">{{ dbPerson.full_name }}</td>
                  <td class="px-4 py-3">
                    <button @click="selectPersonFromDb(dbPerson)" class="text-xs bg-brand-100 text-brand-700 hover:bg-brand-200 px-3 py-1.5 rounded-lg font-bold transition-colors dark:bg-brand-900/30 dark:text-brand-300 dark:hover:bg-brand-900/50">
                      إضافة للمذكرة
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Service Data Import Modal -->
    <div v-if="showServiceImportModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-gray-900/50 backdrop-blur-sm p-4" dir="rtl">
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[90vh]">
        <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 bg-emerald-50 dark:bg-emerald-900/20 flex justify-between items-center shrink-0">
          <h3 class="text-lg font-bold text-emerald-800 dark:text-emerald-300 flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
            استيراد بيانات من كشف / خدمة
          </h3>
          <button @click="showServiceImportModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto flex-1 space-y-6">
          <!-- Service Selector -->
          <div>
            <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">اختر الخدمة / نوع الطلب</label>
            <div class="grid grid-cols-2 gap-3">
              <label class="flex items-center gap-3 p-3 border rounded-xl cursor-pointer transition-colors" :class="selectedServiceForImport === 'CORRECTION' ? 'border-emerald-500 bg-emerald-50 text-emerald-700 dark:bg-emerald-900/30' : 'border-gray-200 hover:bg-gray-50 text-gray-600 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-800'">
                <input type="radio" v-model="selectedServiceForImport" value="CORRECTION" class="w-4 h-4 text-emerald-600">
                <span class="font-bold">طلبات تصحيح البيانات</span>
              </label>
              <label class="flex items-center gap-3 p-3 border rounded-xl cursor-pointer transition-colors opacity-50 cursor-not-allowed border-gray-200 text-gray-400 dark:border-gray-700">
                <input type="radio" disabled class="w-4 h-4 text-gray-400">
                <span class="font-bold">خدمات التقاعد والإخلاء (قريباً)</span>
              </label>
            </div>
          </div>

          <!-- Fetch Actions -->
          <div v-if="selectedServiceForImport === 'CORRECTION'" class="space-y-4 bg-gray-50 dark:bg-gray-900/50 p-4 rounded-xl border border-gray-100 dark:border-gray-800">
            <div>
              <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">البحث برقم الطلب (CORR-ID)</label>
              <div class="flex gap-2">
                <input v-model="serviceImportSearchId" type="text" placeholder="مثال: 23" class="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2 text-sm focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500">
                <button @click="fetchServiceDataById" :disabled="serviceImportLoading" class="bg-emerald-600 hover:bg-emerald-700 text-white px-4 rounded-lg font-bold text-sm disabled:opacity-50 flex items-center gap-2 whitespace-nowrap cursor-pointer">
                  <svg v-if="serviceImportLoading" class="animate-spin h-4 w-4" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                  <span v-else>بحث واستيراد</span>
                </button>
              </div>
            </div>
            
            <div class="relative">
              <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-gray-300 dark:border-gray-700"></div>
              </div>
              <div class="relative flex justify-center">
                <span class="px-2 bg-gray-50 dark:bg-gray-900/50 text-sm text-gray-500">أو</span>
              </div>
            </div>
            
            <div>
              <button @click="fetchServiceDataRecent" :disabled="serviceImportLoading" class="w-full bg-white dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 py-2 rounded-lg font-bold text-sm transition-colors flex items-center justify-center gap-2 cursor-pointer">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                عرض أحدث الطلبات المعلقة للاختيار منها
              </button>
            </div>
          </div>
          
          <!-- Results Table -->
          <div v-if="serviceImportList.length > 0" class="border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden mt-6">
            <div class="max-h-60 overflow-y-auto">
              <table class="w-full text-sm text-right">
                <thead class="bg-gray-50 dark:bg-gray-800 text-gray-700 dark:text-gray-300 sticky top-0">
                  <tr>
                    <th class="px-4 py-2">رقم الطلب</th>
                    <th class="px-4 py-2">الاسم</th>
                    <th class="px-4 py-2">الرقم العسكري</th>
                    <th class="px-4 py-2">الإجراء</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
                  <tr v-for="item in serviceImportList" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                    <td class="px-4 py-2 font-mono font-bold">CORR-{{ String(item.id).padStart(5, '0') }}</td>
                    <td class="px-4 py-2">{{ item.personnel_name || item.full_name || '—' }}</td>
                    <td class="px-4 py-2 font-mono">{{ item.military_number || item.personnel_military_number || '—' }}</td>
                    <td class="px-4 py-2">
                      <button @click="importFromServiceList(item)" class="text-xs bg-emerald-100 text-emerald-700 hover:bg-emerald-200 px-3 py-1.5 rounded-md font-bold transition-colors cursor-pointer">
                        استيراد للمذكرة
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useCoreStore } from '@/stores/core'
import { useAuthStore } from '@/stores/auth'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import CKEditorComponent from '@/components/common/CKEditorComponent.vue'
import api from '@/lib/api'

const router = useRouter()
const route = useRoute()
const coreStore = useCoreStore()
const authStore = useAuthStore()

onMounted(() => {
  if (!coreStore.centralDepartments.length) {
    coreStore.fetchAllReferences()
  }
})
const showPersonnelModal = ref(false)
const searchQuery = ref('')
const editingPresetIndex = ref<number | null>(null)

const showEntityModalForIndex = ref<number | null>(null)
const entitySearchQuery = ref('')

const mockEntitiesDirectory = [
  { 
    group: 'القيادة العُليا', 
    items: [
      { name: 'وزير الداخلية', prefix: 'معالي /', suffix: 'المحترم' },
      { name: 'نائب وزير الداخلية', prefix: 'الأخ /', suffix: 'المحترم' },
      { name: 'وكيل قطاع الموارد البشرية والمالية', prefix: 'الأخ /', suffix: 'المحترم' },
      { name: 'وكيل قطاع الأمن والشرطة', prefix: 'الأخ /', suffix: 'المحترم' }
    ] 
  },
  { 
    group: 'الإدارات العامة', 
    items: [
      { name: 'مدير عام الإدارة العامة للقوى البشرية', prefix: 'الأخ /', suffix: 'المحترم' },
      { name: 'مدير عام الشؤون المالية', prefix: 'الأخ /', suffix: 'المحترم' },
      { name: 'مدير عام الرقابة والتفتيش', prefix: 'الأخ /', suffix: 'المحترم' },
      { name: 'مدير عام التوجيه المعنوي', prefix: 'الأخ /', suffix: 'المحترم' }
    ] 
  },
  { 
    group: 'قيادات المحافظة والفروع', 
    items: [
      { name: 'مدير عام شرطة المحافظة', prefix: 'الأخ /', suffix: 'المحترم' },
      { name: 'نائب مدير عام شرطة المحافظة', prefix: 'الأخ /', suffix: 'المحترم' },
      { name: 'قائد قوات الأمن الخاصة بالمحافظة', prefix: 'الأخ القائد /', suffix: 'المحترم' },
      { name: 'أركان حرب قوات النجدة', prefix: 'الأخ /', suffix: 'المحترم' }
    ] 
  },
  { 
    group: 'جهات عامة (جمع)', 
    items: [
      { name: 'مدراء إدارات أمن المحافظة', prefix: 'الإخوة /', suffix: 'المحترمون' },
      { name: 'مدراء أمن المديريات', prefix: 'الإخوة /', suffix: 'المحترمون' },
      { name: 'قادة الفروع والوحدات الأمنية', prefix: 'الإخوة /', suffix: 'المحترمون' }
    ] 
  }
]

const filterByAuth = (items: any[], type: string) => {
  const user = authStore.user
  const profile = user?.authz_profile
  
  // Defensively extract the user's assigned security_admin_id from anywhere possible
  const profileAdminId = profile?.security_admin_id || 
                         ((profile as any)?.security_admin && typeof (profile as any).security_admin === 'object' && (profile as any).security_admin !== null ? (profile as any).security_admin.id : (profile as any)?.security_admin) ||
                         (user as any)?.security_admin_id ||
                         (user as any)?.governorate_id;

  // If superuser explicitly set to supervise all, they see everything
  if (profile?.supervises_all && !profileAdminId) return items

  return items.filter(item => {
    if (type === 'branch' || type === 'district' || type === 'central') {
      
      const adminId = item.security_admin_id || 
                      (item.security_admin && typeof item.security_admin === 'object' && item.security_admin !== null ? item.security_admin.id : item.security_admin) || 
                      item.governorate_id || 
                      (item.governorate && typeof item.governorate === 'object' && item.governorate !== null ? item.governorate.id : item.governorate);
                      
      // 1. Match by explicit IDs (Best Case)
      if (adminId != null && profileAdminId != null && Number(adminId) === Number(profileAdminId)) return true;
      if (item.id != null && profileAdminId != null && Number(item.id) === Number(profileAdminId)) return true;
      
      // 2. Match if the user supervises this governorate
      if (adminId != null && Array.isArray(profile?.supervised_security_admins)) {
         if (profile.supervised_security_admins.map(Number).includes(Number(adminId))) return true
      }
      
      // 3. Strict specific level match
      const pBranchId = profile?.branch_id || ((profile as any)?.branch && typeof (profile as any).branch === 'object' && (profile as any).branch !== null ? (profile as any).branch.id : (profile as any)?.branch);
      const pDistrictId = profile?.district_police_id || ((profile as any)?.district_police && typeof (profile as any).district_police === 'object' && (profile as any).district_police !== null ? (profile as any).district_police.id : (profile as any)?.district_police);
      const pCentralId = profile?.central_department_id || ((profile as any)?.central_department && typeof (profile as any).central_department === 'object' && (profile as any).central_department !== null ? (profile as any).central_department.id : (profile as any)?.central_department);
      
      if (type === 'branch' && pBranchId && Number(item.id) === Number(pBranchId)) return true;
      if (type === 'district' && pDistrictId && Number(item.id) === Number(pDistrictId)) return true;
      if (type === 'central' && pCentralId && Number(item.id) === Number(pCentralId)) return true;
      
      // 4. HEURISTIC FALLBACK: If the user's account is missing IDs in the database, 
      // we guess their governorate based on their username or name (e.g. 'marib')
      if (!profileAdminId && user) {
        const adminName = item.security_admin_name || item.governorate_name || '';
        const searchTerms = [
          user.city || '', 
          user.full_name || '', 
          user.display_name || '',
          user.username?.includes('marib') ? 'مأرب' : '',
          user.username?.includes('sanaa') ? 'صنعاء' : '',
          user.username?.includes('aden') ? 'عدن' : '',
          user.username?.includes('taiz') ? 'تعز' : '',
          user.username?.includes('shabwah') ? 'شبوة' : '',
          user.username?.includes('hadramout') ? 'حضرموت' : ''
        ].filter(Boolean);

        for (const term of searchTerms) {
          if (term && adminName.includes(term)) return true;
        }
      }
      
      // 5. Superusers fallback (if they truly have no profile and no name matches)
      if (user?.is_superuser && !profileAdminId) return true;

      return false 
    }
    
    return false
  })
}

const dbEntities = computed(() => {
  const groups = []
  
  const filteredCentrals = filterByAuth(coreStore.centralDepartments, 'central')
  if (filteredCentrals && filteredCentrals.length > 0) {
    groups.push({
      group: 'الإدارات العامة (قاعدة البيانات)',
      items: filteredCentrals.map(d => ({
        name: d.name || d.name_ar,
        prefix: 'الأخ / مدير',
        suffix: 'المحترم'
      }))
    })
  }
  
  const filteredDistricts = filterByAuth(coreStore.districtPolices, 'district')
  if (filteredDistricts && filteredDistricts.length > 0) {
    groups.push({
      group: 'إدارات أمن المديريات (قاعدة البيانات)',
      items: filteredDistricts.map(d => ({
        name: d.name || d.name_ar,
        prefix: 'الأخ / مدير',
        suffix: 'المحترم'
      }))
    })
  }
  
  const filteredBranches = filterByAuth(coreStore.branches, 'branch')
  if (filteredBranches && filteredBranches.length > 0) {
    groups.push({
      group: 'الفروع (قاعدة البيانات)',
      items: filteredBranches.map(d => ({
        name: d.name || d.name_ar,
        prefix: 'الأخ / قائد',
        suffix: 'المحترم'
      }))
    })
  }
  
  return groups
})

const allEntitiesDirectory = computed(() => {
  return [...mockEntitiesDirectory, ...dbEntities.value]
})

const filteredMockEntities = computed(() => {
  if (!entitySearchQuery.value) return allEntitiesDirectory.value
  
  return allEntitiesDirectory.value.map(group => {
    const filteredItems = group.items.filter(item => (item.name || '').includes(entitySearchQuery.value))
    return { ...group, items: filteredItems }
  }).filter(group => group.items.length > 0)
})

const selectEntityFromDb = (entity: any) => {
  if (showEntityModalForIndex.value !== null) {
    const idx = showEntityModalForIndex.value
    form.value.addressees[idx].name = entity.name
    form.value.addressees[idx].prefix = entity.prefix
    form.value.addressees[idx].suffix = entity.suffix
  }
  showEntityModalForIndex.value = null
  entitySearchQuery.value = ''
}

import { usePersonnelStore } from '@/stores/personnel'
import { useCorrectionStore } from '@/stores/correction'

const personnelStore = usePersonnelStore()
const correctionStore = useCorrectionStore()

// === Service Data Import Logic ===
const showServiceImportModal = ref(false)
const selectedServiceForImport = ref('CORRECTION')
const serviceImportSearchId = ref('')
const serviceImportLoading = ref(false)
const serviceImportList = ref<any[]>([])

async function fetchServiceDataById() {
  if (!serviceImportSearchId.value) return
  serviceImportLoading.value = true
  try {
    if (selectedServiceForImport.value === 'CORRECTION') {
      const item = await correctionStore.fetchCorrectionById(serviceImportSearchId.value)
      serviceImportList.value = item ? [item] : []
    }
  } catch (e) {
    alert('لم يتم العثور على طلب بهذا الرقم.')
    serviceImportList.value = []
  } finally {
    serviceImportLoading.value = false
  }
}

async function fetchServiceDataRecent() {
  serviceImportLoading.value = true
  try {
    if (selectedServiceForImport.value === 'CORRECTION') {
      const list = await correctionStore.fetchAllPendingCorrections(1)
      serviceImportList.value = list
    }
  } catch (e) {
    serviceImportList.value = []
  } finally {
    serviceImportLoading.value = false
  }
}

function importFromServiceList(item: any) {
  if (selectedServiceForImport.value === 'CORRECTION') {
    let target = '—'
    let rawNotes = item.notes || item.reason || ''
    if (typeof rawNotes === 'string') {
      const targetMatch = rawNotes.match(/المطلوب تصحيح[هة]:\s*([\s\S]*?)(?=\s*المبررات:|$)/)
      if (targetMatch && targetMatch[1]) target = targetMatch[1].trim()
    }
    if (target === '—') {
      if (item.field_name === 'full_name' || item.correction_type === 'name_correction') target = 'تصحيح الاسم'
      else if (item.field_name === 'national_id' || item.correction_type === 'national_id_correction') target = 'تصحيح الرقم الوطني'
      else if (item.field_name === 'military_number' || item.correction_type === 'military_number_correction') target = 'تصحيح الرقم العسكري'
      else target = item.field_name || item.correction_type || 'تحديث بيانات'
    }

    if (!form.value.involvedPersonnel) form.value.involvedPersonnel = []
    
    // Check if already imported
    const exists = form.value.involvedPersonnel.some((p: any) => 
      p.militaryId === (item.military_number || item.personnel_military_number) && 
      p.name === (item.full_name || item.personnel_name)
    )
    
    if (!exists) {
      form.value.involvedPersonnel.push({
        militaryId: item.military_number || item.personnel_military_number || '',
        rank: item.rank || item.personnel_rank || '',
        name: item.full_name || item.personnel_name || item.old_value || '',
        correctName: item.correct_name || item.new_value || '',
        correctionTarget: target,
        nationalId: '', status: '', jobTitle: '', position: '', qualification: '', joinDate: '', workplace: '', serviceLocation: '', commencementDate: '', phone: '', clarification: '', notes: '', secondaryNotes: '', wrongName: ''
      })
    }

    form.value.visibleColumns.correctName = true
    form.value.visibleColumns.correctionTarget = true
    form.value.referenceNo = 'CORR-' + String(item.id).padStart(5, '0')
  }
  
  showServiceImportModal.value = false
  alert('تم استيراد البيانات بنجاح وإضافتها إلى جدول الأفراد المعنيين!')
}

let searchTimeout: any = null
watch(searchQuery, (newVal) => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    personnelStore.fetchPersonnel({ search: newVal })
  }, 500)
})

watch(showPersonnelModal, (newVal) => {
  if (newVal && personnelStore.records.length === 0) {
    personnelStore.fetchPersonnel()
  }
})

const selectPersonFromDb = (dbPerson: any) => {
  if (!form.value.involvedPersonnel) form.value.involvedPersonnel = []
  form.value.involvedPersonnel.push({
    militaryId: dbPerson.military_number,
    rank: dbPerson.rank_name,
    name: dbPerson.full_name,
    clarification: '',
    workplace: dbPerson.central_department_name || dbPerson.branch_name || dbPerson.district_police_name || '',
    serviceLocation: dbPerson.division_name || dbPerson.unit_name || '',
    notes: '',
    secondaryNotes: '',
    commencementDate: '',
    nationalId: dbPerson.national_id || '',
    phone: dbPerson.phone_number || '',
    status: dbPerson.status_name || '',
    jobTitle: dbPerson.job_title_name || '',
    position: dbPerson.position_name || '',
    qualification: dbPerson.qualification_name || '',
    joinDate: dbPerson.join_date || ''
  })
  showPersonnelModal.value = false
  searchQuery.value = ''
}
const fontOptions = [
  { value: "'Cairo', sans-serif", label: "Cairo (حديث - مفضل)" },
  { value: "'Traditional Arabic', serif", label: "Traditional Arabic (رسمي جداً)" },
  { value: "'Simplified Arabic', sans-serif", label: "Simplified Arabic" },
  { value: "'Sakkal Majalla', serif", label: "Sakkal Majalla (رسمي للتقارير)" },
  { value: "'Aref Ruqaa', 'Amiri', serif", label: "خط الرقعة (مزخرف)" },
  { value: "'Amiri', 'Traditional Arabic', serif", label: "أميري (كلاسيكي)" },
  { value: "'Almarai', sans-serif", label: "المراعي (دقة عالية)" },
  { value: "'Noto Naskh Arabic', serif", label: "خط النسخ (Noto Naskh)" },
  { value: "'Noto Kufi Arabic', sans-serif", label: "الخط الكوفي (Noto Kufi)" },
  { value: "'Tajawal', sans-serif", label: "Tajawal" },
  { value: "'Changa', sans-serif", label: "Changa (هندسي)" },
  { value: "'El Messiri', sans-serif", label: "المسيري" },
  { value: "'Dubai', sans-serif", label: "Dubai" },
  { value: "'GE SS Two', sans-serif", label: "GE SS Two" },
  { value: "'Dancing Script', cursive", label: "Dancing Script" },
  { value: "'Noto Nastaliq Urdu', serif", label: "Noto Nastaliq Urdu" },
  { value: "Arial, sans-serif", label: "Arial" }
]

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
  visibleColumns: {
    militaryId: true,
    rank: true,
    name: true,
    nationalId: false,
    status: false,
    jobTitle: false,
    position: false,
    qualification: false,
    joinDate: false,
    workplace: true,
    serviceLocation: true,
    commencementDate: false,
    phone: false,
    clarification: true,
    notes: false,
    correctName: false,
    wrongName: false,
    correctionTarget: false
  },
  typography: {
    addressee: { family: "'Cairo', sans-serif", size: 1.3, weight: 'font-bold', underline: false },
    greeting: { family: "'Aref Ruqaa', 'Amiri', 'Traditional Arabic', serif", size: 1.6, weight: 'font-bold', underline: false },
    subject: { family: "'Cairo', sans-serif", size: 1.4, weight: 'font-black', underline: true },
    body: { family: "'Cairo', sans-serif", size: 1.1, weight: 'font-normal', underline: false },
    conclusionSeparator: { family: "'Cairo', sans-serif", size: 1.4, weight: 'font-black', underline: false },
    conclusionBody: { family: "'Cairo', sans-serif", size: 1.1, weight: 'font-normal', underline: false },
    signatures: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', underline: false },
    signatureRank: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', align: 'text-center', underline: false },
    signatureName: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', align: 'text-center', underline: false },
    signatureTitle: { family: "'Arial', 'Tajawal', sans-serif", size: 0.85, weight: 'font-bold', align: 'text-center', underline: false },
  },
  subject: 'تعميم',
  body: '<p>في البدء نهديكم أطيب التحيات، راجين لكم التوفيق بمهام عملكم..</p><p>بصدد الموضوع أعلاه... (أكمل النص هنا)</p><p>لذلك لزم توجيهكم... وتقبلوا خالص التحيات.</p>',
  conclusion: '<p>وعليه، يتم اتخاذ الإجراءات اللازمة...</p>',
  signatures: [
    { title: 'قسم الخدمات', rank: '', name: '', showSeal: false, freeText: '<p class="text-align-center"><span style="font-family:\'Amiri\', serif; font-size: 24px; color: #1a202c;"><strong>مـقــــــدم /</strong></span></p><p class="text-align-center"><span style="font-family:\'Cairo\', sans-serif; font-size: 26px; color: #000000;"><strong>أحـمـد عـلـي الـسـيـد</strong></span></p><p class="text-align-center"><span style="font-family:\'Cairo\', sans-serif; font-size: 18px; color: #4a5568;">مدير قسـم الخدمـات</span></p>' },
    { title: 'مدير إدارة القوى البشرية', rank: '', name: '', showSeal: false, freeText: '<p class="text-align-center"><span style="font-family:\'Amiri\', serif; font-size: 24px; color: #1a202c;"><strong>عـمـيـــــــد /</strong></span></p><p class="text-align-center"><span style="font-family:\'Cairo\', sans-serif; font-size: 26px; color: #000000;"><strong>عـبـدالله مـحـمـد</strong></span></p><p class="text-align-center"><span style="font-family:\'Cairo\', sans-serif; font-size: 18px; color: #4a5568;">مديـر إدارة القـوى البشـريـة</span></p>' },
    { title: 'مدير عام شرطة المحافظة', rank: '', name: '', showSeal: true, freeText: '<p class="text-align-center"><span style="font-family:\'Amiri\', serif; font-size: 26px; color: #1a202c;"><strong>لــــــــواء /</strong></span></p><p class="text-align-center"><span style="font-family:\'Cairo\', sans-serif; font-size: 28px; color: #000000;"><strong>يـحـيـى أحـمـد الـيـمـانـي</strong></span></p><p class="text-align-center"><span style="font-family:\'Cairo\', sans-serif; font-size: 20px; color: #4a5568;">مديـر عـام شـرطـة المـحـافـظـة</span></p>' }
  ],
  signatureSettings: {
    showFrame: true,
    showLabels: true,
  }
}

const form = ref(JSON.parse(JSON.stringify(defaultForm)))

const handleDocumentTypeChange = () => {
  if (!form.value.involvedPersonnel) form.value.involvedPersonnel = []

  if (['ATTENTION_NOTICE', 'WORK_COMMENCEMENT', 'PERSONNEL_MEMO'].includes(form.value.documentType)) {
    if (form.value.involvedPersonnel.length === 0) {
      form.value.involvedPersonnel.push({ militaryId: '', rank: '', name: '', clarification: '', workplace: '', serviceLocation: '', notes: '', secondaryNotes: '', commencementDate: '', nationalId: '', phone: '', correctName: '', wrongName: '', correctionTarget: '' })
    }
  }

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
  } else if (form.value.documentType === 'PERSONNEL_MEMO') {
    form.value.subject = 'مذكرة خاصة بالأفراد'
    form.value.addressees = [{ prefix: 'الأخ /', type: 'TEXT', entityId: null, name: '', suffix: 'المحترم' }]
    form.value.body = '<p>تحية طيبة وبعد،،</p><p>نرفق لكم كشف بأسماء الأفراد، راجين التكرم بالاطلاع واتخاذ اللازم.</p><p>وتقبلوا خالص التحيات.</p>'
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

const addSignature = () => {
  if (!form.value.signatures) form.value.signatures = []
  form.value.signatures.push({ 
    title: 'جهة جديدة', 
    rank: '', 
    name: '', 
    showSeal: false,
    freeText: '<p class="text-align-center"><span style="font-family:\'Amiri\', serif; font-size: 24px; color: #1a202c;"><strong>عـقـيـــــــد /</strong></span></p><p class="text-align-center"><span style="font-family:\'Cairo\', sans-serif; font-size: 26px; color: #000000;"><strong>الاسـم هـنـا</strong></span></p><p class="text-align-center"><span style="font-family:\'Cairo\', sans-serif; font-size: 18px; color: #4a5568;">الصـفـة هـنـا</span></p>'
  })
}

const removeSignature = (index: number) => {
  form.value.signatures.splice(index, 1)
}

const addInvolvedPersonnel = () => {
  if (!form.value.involvedPersonnel) form.value.involvedPersonnel = []
  form.value.involvedPersonnel.push({ militaryId: '', rank: '', name: '', clarification: '', workplace: '', serviceLocation: '', notes: '', secondaryNotes: '', commencementDate: '', nationalId: '', phone: '', correctName: '', wrongName: '', correctionTarget: '' })
}

const removeInvolvedPersonnel = (index: number) => {
  form.value.involvedPersonnel.splice(index, 1)
}

const resetForm = () => {
  if(confirm('هل أنت متأكد من مسح جميع الحقول؟')) {
    form.value = JSON.parse(JSON.stringify(defaultForm))
  }
}

// === Full Templates & Presets Management ===
const savedPresets = ref<any[]>([])
const selectedPresetIndex = ref('')
const newPresetName = ref('')

const fetchTemplates = async () => {
  try {
    const response = await api.get('/secretariat/memo-templates/')
    savedPresets.value = response.data.map((item: any) => ({
      id: item.id,
      name: item.name,
      fullTemplate: item.content
    }))
  } catch (error) {
    console.error('Failed to fetch memo templates:', error)
    // fallback to localStorage
    savedPresets.value = JSON.parse(localStorage.getItem('memoTypographyPresets') || '[]')
  }
}

const savePreset = async () => {
  if (!newPresetName.value) {
    alert('يرجى إدخال اسم للقالب أولاً')
    return
  }
  try {
    await api.post('/secretariat/memo-templates/', {
      name: newPresetName.value,
      document_type: form.value.documentType || 'MEMO',
      content: JSON.parse(JSON.stringify(form.value))
    })
    await fetchTemplates()
    newPresetName.value = ''
    alert('تم حفظ القالب بالكامل بنجاح في قاعدة البيانات!')
  } catch (error) {
    console.error('Failed to save template:', error)
    // fallback to localStorage
    const presets = JSON.parse(localStorage.getItem('memoTypographyPresets') || '[]')
    presets.push({
      name: newPresetName.value,
      typography: JSON.parse(JSON.stringify(form.value.typography)),
      fullTemplate: JSON.parse(JSON.stringify(form.value)) // Save the whole form!
    })
    localStorage.setItem('memoTypographyPresets', JSON.stringify(presets))
    savedPresets.value = presets
    newPresetName.value = ''
    alert('تم حفظ القالب محلياً في المتصفح!')
  }
}

const loadPreset = () => {
  if (selectedPresetIndex.value === '') return
  if(confirm('هل أنت متأكد من تحميل هذا القالب؟ سيتم استبدال محتوى المذكرة الحالي.')) {
    const idx = Number(selectedPresetIndex.value)
    const preset = savedPresets.value[idx]
    if (preset) {
      if (preset.fullTemplate) {
        // Load entire template if available
        form.value = JSON.parse(JSON.stringify(preset.fullTemplate))
      } else if (preset.typography) {
        // Fallback for old typography-only presets
        form.value.typography = JSON.parse(JSON.stringify(preset.typography))
      }
      editingPresetIndex.value = idx
      localStorage.setItem('official_memo_edit_index', idx.toString())
    }
  }
}

const resetTypography = () => {
  if(confirm('هل أنت متأكد من استعادة التنسيقات الافتراضية؟')) {
    form.value.typography = JSON.parse(JSON.stringify(defaultForm.typography))
  }
}

const previewMemo = () => {
  localStorage.setItem('official_memo_draft', JSON.stringify(form.value))
  window.open(router.resolve('/admin/documents/memo-preview').href, '_blank')
}


const saveAsNewTemplate = async () => {
  const name = prompt("أدخل اسماً للقالب الجديد (مثال: قالب تصحيح خاص):")
  if (!name) return
  try {
    const response = await api.post('/secretariat/memo-templates/', {
      name: name,
      document_type: form.value.documentType || 'MEMO',
      content: JSON.parse(JSON.stringify(form.value))
    })
    await fetchTemplates()
    const idx = savedPresets.value.findIndex((p: any) => p.id === response.data.id)
    if (idx !== -1) {
      editingPresetIndex.value = idx
      localStorage.setItem('official_memo_edit_index', idx.toString())
    }
    alert('تم حفظ القالب بنجاح في قاعدة البيانات!')
  } catch (error) {
    console.error('Failed to save as new template:', error)
    let presets = JSON.parse(localStorage.getItem('memoTypographyPresets') || '[]')
    presets.push({
      name: name,
      fullTemplate: JSON.parse(JSON.stringify(form.value))
    })
    localStorage.setItem('memoTypographyPresets', JSON.stringify(presets))
    editingPresetIndex.value = presets.length - 1
    localStorage.setItem('official_memo_edit_index', editingPresetIndex.value.toString())
    savedPresets.value = presets
    alert('تم حفظ القالب محلياً!')
  }
}

const saveExistingTemplate = async () => {
  if (editingPresetIndex.value === null) {
    await saveAsNewTemplate()
    return
  }
  const preset = savedPresets.value[editingPresetIndex.value]
  if (!preset) return

  if (preset.id) {
    try {
      await api.put(`/secretariat/memo-templates/${preset.id}/`, {
        name: preset.name,
        document_type: form.value.documentType || 'MEMO',
        content: JSON.parse(JSON.stringify(form.value))
      })
      await fetchTemplates()
      alert('تم حفظ التعديلات على القالب بنجاح في قاعدة البيانات!')
    } catch (error) {
      console.error('Failed to update template:', error)
      alert('حدث خطأ أثناء حفظ التعديلات على الخادم.')
    }
  } else {
    let presets = JSON.parse(localStorage.getItem('memoTypographyPresets') || '[]')
    if (presets[editingPresetIndex.value]) {
      presets[editingPresetIndex.value].fullTemplate = JSON.parse(JSON.stringify(form.value))
      localStorage.setItem('memoTypographyPresets', JSON.stringify(presets))
      savedPresets.value = presets
      alert('تم حفظ التعديلات محلياً!')
    }
  }
}


const createNewTemplate = () => {
  if(confirm('هل أنت متأكد من إنشاء قالب جديد؟ سيتم فقدان التعديلات الحالية غير المحفوظة.')) {
    localStorage.removeItem('official_memo_draft')
    localStorage.removeItem('official_memo_edit_index')
    editingPresetIndex.value = null
    form.value = JSON.parse(JSON.stringify(defaultForm))
  }
}

onMounted(async () => {
  await fetchTemplates()
  const editIdxStr = localStorage.getItem('official_memo_edit_index')
  if (editIdxStr !== null) {
    editingPresetIndex.value = parseInt(editIdxStr)
  }

  const draftStr = localStorage.getItem('official_memo_draft')
  if (draftStr) {
    try {
      const draft = JSON.parse(draftStr)
      if (draft.includeTable === undefined) draft.includeTable = true
      // Migrate correction personnel data
      if (draft.documentType === 'CORRECTION' && draft.involvedPersonnel) {
        draft.involvedPersonnel.forEach((p: any) => {
          if (!p.wrongName && p.name) {
            p.wrongName = p.name;
          }
        });
      }
      form.value = { ...defaultForm, ...draft }
      
      // Migrate old 'signers' array to 'signatures'
      if (draft.signers && Array.isArray(draft.signers) && draft.signers.length > 0) {
        form.value.signatures = draft.signers.map((s: any) => ({
          title: s.role || '',
          rank: s.rank || '',
          name: s.name || '',
          showSeal: s.id === 2 || s.role?.includes('مدير عام')
        }))
      } else if (draft.signatures && !Array.isArray(draft.signatures)) {
        // Migrate signatures if it's an old object format
        form.value.signatures = [
          { title: draft.signatures.preparer?.title || '', rank: draft.signatures.preparer?.rank || '', name: draft.signatures.preparer?.name || '', showSeal: false },
          { title: draft.signatures.reviewer?.title || '', rank: draft.signatures.reviewer?.rank || '', name: draft.signatures.reviewer?.name || '', showSeal: false },
          { title: draft.signatures.approver?.title || '', rank: draft.signatures.approver?.rank || '', name: draft.signatures.approver?.name || '', showSeal: true }
        ]
      } else if (draft.signatures && Array.isArray(draft.signatures)) {
        form.value.signatures = draft.signatures
      }
      
      if (!draft.signatureSettings) {
        form.value.signatureSettings = { showFrame: true, showLabels: true }
      }
      
      // Forcefully fix font size if it was saved as 1.1 from previous broken state
      if (form.value.typography?.signatures?.size === 1.1) {
        form.value.typography.signatures.size = 0.85
      }
      if (form.value.typography?.signatures?.family === "'Cairo', sans-serif") {
        form.value.typography.signatures.family = "'Arial', 'Tajawal', sans-serif"
      }
      
      // Ensure signatures typography exists for older drafts
      if (form.value.typography) {
        if (!form.value.typography.signatures) form.value.typography.signatures = JSON.parse(JSON.stringify(defaultForm.typography.signatures))
        if (!form.value.typography.signatureRank) form.value.typography.signatureRank = JSON.parse(JSON.stringify(defaultForm.typography.signatureRank))
        if (!form.value.typography.signatureName) form.value.typography.signatureName = JSON.parse(JSON.stringify(defaultForm.typography.signatureName))
        if (!form.value.typography.signatureTitle) form.value.typography.signatureTitle = JSON.parse(JSON.stringify(defaultForm.typography.signatureTitle))
      }
      
      // Migration for older drafts
      if (!form.value.documentType) form.value.documentType = 'MEMO'
      if (!form.value.involvedPersonnel) form.value.involvedPersonnel = []
      
      // Migrate old 'to' array to 'addressees'
      if (draft.to && Array.isArray(draft.to) && draft.to.length > 0 && (!draft.addressees || draft.addressees.length === 0)) {
        form.value.addressees = draft.to.map((a: any) => ({
          prefix: a.title?.startsWith('الإخوة') ? 'الإخوة /' : 'الأخ /',
          type: 'TEXT',
          entityId: null,
          name: a.title?.replace(/^(الأخ |الإخوة |معالي )?\/?\s*/, '') || '',
          suffix: a.honorific || 'المحترم'
        }))
      } else if (form.value.addressees && form.value.addressees.length > 0) {
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
  } else if (route.query.type) {
    // If no draft and we are creating a specific type from Library
    form.value.documentType = route.query.type as string
    handleDocumentTypeChange()
  }

  // Auto-populate issuer lines using coreStore
  const populateIssuerLines = () => {
    if (!form.value.issuerLine1) form.value.issuerLine1 = 'وزارة الداخلية'
    
    if (authStore.user?.authz_profile) {
      const profile = authStore.user.authz_profile
      
      // Line 2: Central Dept OR Sec Admin (Governorate)
      if (!form.value.issuerLine2) {
        if (profile.central_department_id) {
          const dept = coreStore.centralDepartments.find((d: any) => d.id === profile.central_department_id)
          if (dept) form.value.issuerLine2 = dept.name
        } else if (profile.security_admin_id) {
          const admin = coreStore.securityAdmins.find((a: any) => a.id === profile.security_admin_id)
          if (admin) form.value.issuerLine2 = admin.name
        }
      }
      
      // Line 3: Branch (for Central Depts) OR District (for Govs)
      if (!form.value.issuerLine3) {
        if (profile.branch_id) {
          const branch = coreStore.branches.find((b: any) => b.id === profile.branch_id)
          if (branch) form.value.issuerLine3 = branch.name
        } else if (profile.district_police_id) {
          const district = coreStore.districtPolices.find((d: any) => d.id === profile.district_police_id)
          if (district) form.value.issuerLine3 = district.name
        }
      }
    }
  }

  const loadCoreRefsAndPopulate = async () => {
    if (!coreStore.centralDepartments.length) {
      await coreStore.fetchAllReferences()
    }
    populateIssuerLines()
  }
  
  loadCoreRefsAndPopulate()
})
</script>
