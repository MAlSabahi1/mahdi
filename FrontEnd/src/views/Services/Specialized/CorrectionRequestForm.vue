<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="schema ? schema.label : 'تقديم طلب جديد'" />

    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-600"></div>
    </div>

    <div v-else-if="error || !schema" class="bg-red-50 text-red-600 p-6 rounded-2xl text-center font-bold">
      {{ error || 'لا يوجد هيكل لهذه الاستمارة أو أنها قيد التطوير.' }}
      <div class="mt-4">
        <RouterLink to="/services/directory" class="text-brand-600 underline">العودة لدليل الخدمات</RouterLink>
      </div>
    </div>

    <div v-else class="max-w-5xl mx-auto text-start" dir="rtl">
      <!-- #8 Professional Stepper -->
      <div class="mb-10 px-4">
        <div class="flex items-center justify-between relative">
          <!-- Progress bar background -->
          <div class="absolute left-0 right-0 top-6 h-1 bg-gray-200 dark:bg-gray-800 rounded-full -z-10"></div>
          <!-- Progress bar fill -->
          <div 
            class="absolute right-0 top-6 h-1 bg-gradient-to-l from-brand-600 to-emerald-500 rounded-full -z-10 transition-all duration-500 ease-out" 
            :style="{ width: ((step - 1) / 2) * 100 + '%' }"
          ></div>

          <div v-for="(s, idx) in stepLabels" :key="idx" class="relative flex flex-col items-center" style="min-width: 120px;">
            <div
              class="w-12 h-12 rounded-full flex items-center justify-center font-bold text-sm transition-all duration-500 shadow-sm border-2"
              :class="[
                step > idx + 1 ? 'bg-emerald-500 border-emerald-400 text-white scale-100' :
                step === idx + 1 ? 'bg-brand-600 border-brand-500 text-white scale-110 shadow-lg shadow-brand-500/30 ring-4 ring-brand-500/10' :
                'bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-700 text-gray-400 scale-100'
              ]"
            >
              <svg v-if="step > idx + 1" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
              <span v-else>{{ idx + 1 }}</span>
            </div>
            <p 
              class="mt-2.5 text-[11px] font-bold text-center transition-colors"
              :class="step >= idx + 1 ? 'text-gray-800 dark:text-gray-200' : 'text-gray-400 dark:text-gray-600'"
            >
              {{ s }}
            </p>
          </div>
        </div>
      </div>

      <!-- Step 1: Personnel Search & Selection -->
      <div v-if="step === 1" class="bg-white dark:bg-gray-900 border dark:border-gray-800 rounded-2xl p-6 shadow-sm">
        <div class="flex justify-between items-center mb-6 border-b border-gray-100 dark:border-gray-800 pb-4">
          <h2 class="text-lg font-black text-gray-900 dark:text-white">الخطوة 1: تحديد الأفراد المشمولين بالخدمة</h2>
          <span class="text-sm font-bold text-brand-600 bg-brand-50 dark:bg-brand-900/30 px-3 py-1 rounded-full">
            المحدد: {{ selectedPersonnelList.length }}
          </span>
        </div>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Search Area -->
          <div>
            <label class="block text-xs font-bold text-gray-700 dark:text-gray-300 mb-2">بحث عن طريق (الرقم العسكري، الاسم، الوحدة)</label>
            <div class="flex gap-2 mb-4">
              <input v-model="searchQuery" type="text" placeholder="مثال: محمد أحمد، أو 7348..." class="flex-1 bg-gray-50 border border-gray-200 dark:bg-gray-800 dark:border-gray-700 rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-500 outline-none text-sm" @keyup.enter="searchPersonnel" />
              <button @click="searchPersonnel" :disabled="personnelStore.loading" class="bg-gray-900 dark:bg-white dark:text-gray-900 text-white px-6 py-2.5 rounded-xl font-bold hover:bg-gray-800 disabled:opacity-50 transition-colors">بحث</button>
            </div>

            <!-- Search Results -->
            <div v-if="personnelStore.loading" class="py-8 flex justify-center">
              <span class="animate-spin h-6 w-6 border-2 border-brand-500 border-t-transparent rounded-full"></span>
            </div>
            <div v-else-if="searchResults.length > 0" class="border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden bg-white dark:bg-gray-900 max-h-64 overflow-y-auto">
              <div class="bg-gray-50 dark:bg-gray-800 px-4 py-2 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
                <span class="text-xs font-bold text-gray-500">نتائج البحث ({{ searchResults.length }})</span>
                <button @click="addAllSearchResults" class="text-xs font-bold text-brand-600 hover:text-brand-700">إضافة الكل</button>
              </div>
              <div v-for="person in searchResults" :key="person.military_number" class="p-3 border-b border-gray-100 dark:border-gray-800 flex justify-between items-center hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                <div>
                  <p class="font-bold text-sm text-gray-900 dark:text-white">{{ person.full_name }}</p>
                  <p class="text-xs text-gray-500">{{ person.rank_name || 'بدون رتبة' }} | {{ person.military_number }} | {{ person.unit_name || 'بدون جهة' }}</p>
                </div>
                <button 
                  @click="addPersonnel(person)" 
                  :disabled="isPersonnelSelected(person.military_number)"
                  :class="isPersonnelSelected(person.military_number) ? 'bg-gray-100 text-gray-400 dark:bg-gray-800' : 'bg-brand-50 text-brand-600 hover:bg-brand-100 dark:bg-brand-900/30 dark:hover:bg-brand-900/50'"
                  class="px-3 py-1.5 rounded-lg text-xs font-bold transition-colors"
                >
                  {{ isPersonnelSelected(person.military_number) ? 'مضاف' : 'إضافة' }}
                </button>
              </div>
            </div>
            <div v-else-if="searchPerformed && searchResults.length === 0" class="text-center py-8 text-gray-500 text-sm">
              لم يتم العثور على نتائج.
            </div>
          </div>

          <!-- Selected List -->
          <div class="bg-gray-50 dark:bg-gray-800/30 rounded-xl border border-gray-200 dark:border-gray-700 p-4 flex flex-col h-[350px]">
            <h3 class="text-sm font-bold text-gray-900 dark:text-white mb-4">قائمة المشمولين بالخدمة</h3>
            <div v-if="type === 'linked_military_swap'" class="bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs p-2 rounded mb-3 border border-blue-200 dark:border-blue-800">
              يرجى تحديد فردين (2) بالضبط لإجراء التبديل المترابط للأرقام العسكرية.
            </div>
            
            <div v-if="selectedPersonnelList.length === 0" class="flex-1 flex flex-col items-center justify-center text-gray-400">
              <svg class="w-12 h-12 mb-3 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
              <p class="text-sm">لم يتم تحديد أي فرد بعد.</p>
              <p class="text-xs mt-1">ابحث وقم بإضافة الأفراد من القائمة.</p>
            </div>

            <div v-else class="flex-1 overflow-y-auto space-y-2 pr-2 custom-scrollbar">
              <div v-for="person in selectedPersonnelList" :key="person.military_number" class="bg-white dark:bg-gray-900 p-3 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm flex justify-between items-center group">
                <div>
                  <p class="font-bold text-sm text-gray-900 dark:text-white">{{ person.full_name }}</p>
                  <p class="text-[11px] text-gray-500">{{ person.military_number }}</p>
                </div>
                <button @click="removePersonnel(person.military_number)" class="text-gray-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity p-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </button>
              </div>
            </div>

            <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 flex justify-end">
              <button 
                @click="goToStep2" 
                :disabled="selectedPersonnelList.length === 0 || (type === 'linked_military_swap' && selectedPersonnelList.length !== 2)" 
                class="bg-emerald-600 text-white px-8 py-2.5 rounded-xl font-bold hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md shadow-emerald-500/20"
              >
                التالي
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 2: Form Fields -->
      <div v-if="step === 2" class="bg-white dark:bg-gray-900 border dark:border-gray-800 rounded-2xl p-8 shadow-sm">
        <div class="mb-6 pb-4 border-b border-gray-100 dark:border-gray-800">
          <h2 class="text-lg font-black">الخطوة 2: تعبئة بيانات التصحيح</h2>
          <p class="text-sm text-gray-500 mt-1">يرجى التأكد من البيانات المدخلة بعناية حيث سيتم تعديل السجل المعتمد.</p>
        </div>
        
        <div class="space-y-8">
          <!-- Special Name Correction Table Layout -->
          <div v-if="type === 'name_correction'" class="space-y-6">
            <!-- Warning banner for pending name corrections -->
            <div v-if="hasPendingNameCorrection" class="p-4 rounded-xl bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/30 text-red-700 dark:text-red-400 space-y-2 text-xs">
              <div class="flex items-center gap-2 font-bold">
                <svg class="w-4.5 h-4.5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                <span>تنبيه: يوجد طلب تصحيح اسم معلق قيد الانتظار لهذا الفرد</span>
              </div>
              <p class="font-normal text-[11px] text-gray-600 dark:text-gray-400 leading-relaxed pr-6">
                لا يمكن تقديم طلب تصحيح اسم جديد لهذا الفرد لوجود طلب سابق قيد المراجعة حالياً بالاسم المقترح:
                <strong class="text-red-800 dark:text-red-350 font-black">"{{ pendingNameCorrectionDetails?.new_value }}"</strong>
                والذي تم تقديمه بتاريخ {{ pendingNameCorrectionDetails?.requested_at ? new Date(pendingNameCorrectionDetails.requested_at).toLocaleDateString('ar-EG') : '' }}.
                يرجى الانتظار حتى يتم البت في الطلب الحالي (موافقة أو رفض) قبل تقديم طلب جديد.
              </p>
            </div>

            <!-- The Correction Table Grid -->
            <div class="overflow-x-auto border border-gray-200 dark:border-gray-800 rounded-xl shadow-sm bg-white dark:bg-gray-900">
              <table class="w-full border-collapse text-right text-sm">
                <thead>
                  <tr class="bg-gray-50 dark:bg-gray-850 text-gray-700 dark:text-gray-300 font-bold">
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-12">م</th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-24">الرتبة</th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-32">الرقم العسكري</th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800">الاسم الخطأ (قاعدة البيانات)</th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 w-1/3">الاسم الصحيح (بحسب البطاقة)</th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 w-48">المطلوب تصحيحه</th>
                    <th class="p-3 border-b border-gray-200 dark:border-gray-800 w-48">ملاحظات</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="hover:bg-gray-50/50 dark:hover:bg-gray-800/20 transition-colors">
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center font-bold text-gray-400">1</td>
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center font-bold text-gray-600 dark:text-gray-300">
                      {{ selectedPersonnelList[0].rank_name || selectedPersonnelList[0].current_rank?.name || selectedPersonnelList[0].rank?.name || '—' }}
                    </td>
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center font-mono font-bold text-brand-600 dark:text-brand-400">
                      {{ selectedPersonnelList[0].military_number }}
                    </td>
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 font-bold text-red-500 line-through decoration-red-500/40">
                      {{ selectedPersonnelList[0].full_name }}
                    </td>
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800">
                      <div class="grid grid-cols-2 md:grid-cols-5 gap-1.5">
                        <input v-model="nameParts.first" @input="updateFullName" :disabled="hasPendingNameCorrection" type="text" placeholder="الأول" class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none disabled:opacity-50" />
                        <input v-model="nameParts.second" @input="updateFullName" :disabled="hasPendingNameCorrection" type="text" placeholder="الثاني" class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none disabled:opacity-50" />
                        <input v-model="nameParts.third" @input="updateFullName" :disabled="hasPendingNameCorrection" type="text" placeholder="الثالث" class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none disabled:opacity-50" />
                        <input v-model="nameParts.fourth" @input="updateFullName" :disabled="hasPendingNameCorrection" type="text" placeholder="الرابع" class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none disabled:opacity-50" />
                        <input v-model="nameParts.surname" @input="updateFullName" :disabled="hasPendingNameCorrection" type="text" placeholder="اللقب" class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none disabled:opacity-50" />
                      </div>
                      <!-- Preview & Validation -->
                      <div class="mt-2 flex items-center justify-between text-[9px] font-bold">
                        <div class="flex items-center gap-1" :class="isDifferentName ? 'text-emerald-500' : 'text-red-500'">
                          <span v-if="isDifferentName">✓ مختلف</span>
                          <span v-else>✗ يطابق القديم</span>
                        </div>
                        <div class="flex items-center gap-1" :class="hasFiveParts ? 'text-emerald-500' : 'text-red-500'">
                          <span v-if="hasFiveParts">✓ خماسي</span>
                          <span v-else>✗ ناقص</span>
                        </div>
                      </div>
                    </td>
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center">
                      <select v-model="formData.correction_targets" multiple :disabled="hasPendingNameCorrection" class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none h-16 custom-scrollbar disabled:opacity-50">
                        <option value="الاسم الأول">الاسم الأول</option>
                        <option value="الاسم الثاني">الاسم الثاني</option>
                        <option value="الاسم الثالث">الاسم الثالث</option>
                        <option value="الاسم الرابع">الاسم الرابع</option>
                        <option value="اللقب">اللقب</option>
                      </select>
                      <span class="text-[9px] text-gray-400 mt-1 block">حدد بمفتاح Ctrl لاختيار أكثر من جزء</span>
                    </td>
                    <td class="p-3 border-b border-gray-200 dark:border-gray-800 text-center">
                      <textarea v-model="notes" rows="2" :disabled="hasPendingNameCorrection" placeholder="أدخل أسباب التصحيح استناداً للمستند الرسمي..." class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none resize-none disabled:opacity-50"></textarea>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

          </div>

          <!-- Military Number Correction Table Layout -->
          <div v-else-if="type === 'military_number_correction'" class="space-y-6">
            <div class="overflow-x-auto border border-gray-200 dark:border-gray-800 rounded-xl shadow-sm bg-white dark:bg-gray-900">
              <table class="w-full border-collapse text-right text-sm">
                <thead>
                  <tr class="bg-gray-50 dark:bg-gray-850 text-gray-700 dark:text-gray-300 font-bold text-xs">
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-12">م</th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-48">الاسم</th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-32">الرقم العسكري الخاطئ</th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 w-48">الرقم العسكري الصحيح <span class="text-red-500">*</span></th>
                    <th class="p-3 border-b border-gray-200 dark:border-gray-800 w-48">أسباب التصحيح <span class="text-red-500">*</span></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(person, idx) in selectedPersonnelList" :key="person.military_number" class="hover:bg-gray-50/50 dark:hover:bg-gray-800/20 transition-colors">
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center font-bold text-gray-400">{{ idx + 1 }}</td>
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 font-bold text-gray-900 dark:text-white">
                      {{ person.full_name }}
                    </td>
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center font-mono font-bold text-red-500 line-through decoration-red-500/40">
                      {{ person.military_number }}
                    </td>
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center">
                      <input v-model="formData.new_values[person.military_number]" type="text" maxlength="7" pattern="\d*" placeholder="أدخل الرقم الصحيح" class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none font-mono text-center" />
                    </td>
                    <td class="p-3 border-b border-gray-200 dark:border-gray-800 text-center">
                      <textarea v-model="formData.notes[person.military_number]" rows="1" placeholder="أسباب التصحيح..." class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none resize-none"></textarea>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- National ID Correction Table Layout -->
          <div v-else-if="type === 'national_id_correction'" class="space-y-6">
            <div class="overflow-x-auto border border-gray-200 dark:border-gray-800 rounded-xl shadow-sm bg-white dark:bg-gray-900">
              <table class="w-full border-collapse text-right text-sm">
                <thead>
                  <tr class="bg-gray-50 dark:bg-gray-850 text-gray-700 dark:text-gray-300 font-bold text-xs">
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-12">م</th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-48">الاسم</th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-32">الرقم الوطني الخاطئ</th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 w-48">الرقم الوطني الصحيح <span class="text-red-500">*</span></th>
                    <th class="p-3 border-b border-gray-200 dark:border-gray-800 w-48">أسباب التصحيح <span class="text-red-500">*</span></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(person, idx) in selectedPersonnelList" :key="person.military_number" class="hover:bg-gray-50/50 dark:hover:bg-gray-800/20 transition-colors">
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center font-bold text-gray-400">{{ idx + 1 }}</td>
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 font-bold text-gray-900 dark:text-white">
                      {{ person.full_name }}
                    </td>
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center font-mono font-bold text-red-500 line-through decoration-red-500/40">
                      {{ person.national_id || 'غير مسجل' }}
                    </td>
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center" style="min-width: 320px;" dir="rtl">
                      <NationalIdWizard 
                        v-model="formData.new_values[person.military_number]"
                        :label="''"
                        :required="false"
                        :isValidating="nidState[person.military_number]?.isValidating"
                        :duplicateError="nidState[person.military_number]?.error"
                        @complete="(val) => verifyNidDuplicate(person.military_number, val)"
                        @update:modelValue="clearNidError(person.military_number)"
                      />
                    </td>
                    <td class="p-3 border-b border-gray-200 dark:border-gray-800 text-center">
                      <textarea v-model="formData.notes[person.military_number]" rows="1" placeholder="أسباب التصحيح..." class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none resize-none"></textarea>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Linked Military Swap Layout -->
          <div v-else-if="type === 'linked_military_swap' && selectedPersonnelList.length === 2" class="space-y-6">
            <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-xl border border-blue-200 dark:border-blue-800/50 mb-6 flex items-start gap-3">
              <svg class="w-6 h-6 text-blue-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path></svg>
              <div>
                <h4 class="font-bold text-blue-900 dark:text-blue-300 text-sm">عملية تبديل مترابط</h4>
                <p class="text-xs text-blue-700 dark:text-blue-400 mt-1">سيتم تبديل الأرقام العسكرية بين الفردين أدناه بشكل متزامن. يرجى التأكد من هوياتهم بشكل قاطع.</p>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 relative">
              <!-- Swap Icon Overlay -->
              <div class="hidden md:flex absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 w-12 h-12 bg-white dark:bg-gray-900 rounded-full border-2 border-gray-200 dark:border-gray-700 items-center justify-center shadow-lg">
                <svg class="w-6 h-6 text-brand-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path></svg>
              </div>

              <!-- Person 1 -->
              <div class="border border-gray-200 dark:border-gray-700 rounded-xl p-5 bg-white dark:bg-gray-900 shadow-sm relative overflow-hidden">
                <div class="absolute top-0 right-0 bg-brand-600 text-white text-[10px] font-bold px-3 py-1 rounded-bl-lg">الفرد 1</div>
                <div class="text-center mt-3 mb-4">
                  <div class="font-bold text-lg dark:text-white">{{ selectedPersonnelList[0].full_name }}</div>
                  <div class="text-sm text-gray-500 mt-1">{{ selectedPersonnelList[0].rank_name || 'بدون رتبة' }}</div>
                </div>
                <div class="bg-red-50 dark:bg-red-900/20 p-3 rounded-lg border border-red-100 dark:border-red-900/30 text-center mb-3">
                  <span class="block text-[10px] text-red-600 dark:text-red-400 font-bold mb-1">الرقم الحالي (سيُسحب منه)</span>
                  <span class="font-mono font-bold text-red-700 dark:text-red-300 line-through">{{ selectedPersonnelList[0].military_number }}</span>
                </div>
                <div class="bg-emerald-50 dark:bg-emerald-900/20 p-3 rounded-lg border border-emerald-100 dark:border-emerald-900/30 text-center">
                  <span class="block text-[10px] text-emerald-600 dark:text-emerald-400 font-bold mb-1">الرقم الجديد (الذي سيأخذه)</span>
                  <span class="font-mono font-bold text-emerald-700 dark:text-emerald-300">{{ selectedPersonnelList[1].military_number }}</span>
                </div>
              </div>

              <!-- Person 2 -->
              <div class="border border-gray-200 dark:border-gray-700 rounded-xl p-5 bg-white dark:bg-gray-900 shadow-sm relative overflow-hidden">
                <div class="absolute top-0 right-0 bg-brand-600 text-white text-[10px] font-bold px-3 py-1 rounded-bl-lg">الفرد 2</div>
                <div class="text-center mt-3 mb-4">
                  <div class="font-bold text-lg dark:text-white">{{ selectedPersonnelList[1].full_name }}</div>
                  <div class="text-sm text-gray-500 mt-1">{{ selectedPersonnelList[1].rank_name || 'بدون رتبة' }}</div>
                </div>
                <div class="bg-red-50 dark:bg-red-900/20 p-3 rounded-lg border border-red-100 dark:border-red-900/30 text-center mb-3">
                  <span class="block text-[10px] text-red-600 dark:text-red-400 font-bold mb-1">الرقم الحالي (سيُسحب منه)</span>
                  <span class="font-mono font-bold text-red-700 dark:text-red-300 line-through">{{ selectedPersonnelList[1].military_number }}</span>
                </div>
                <div class="bg-emerald-50 dark:bg-emerald-900/20 p-3 rounded-lg border border-emerald-100 dark:border-emerald-900/30 text-center">
                  <span class="block text-[10px] text-emerald-600 dark:text-emerald-400 font-bold mb-1">الرقم الجديد (الذي سيأخذه)</span>
                  <span class="font-mono font-bold text-emerald-700 dark:text-emerald-300">{{ selectedPersonnelList[0].military_number }}</span>
                </div>
              </div>
            </div>

            <div class="mt-4">
              <label class="block text-xs font-bold text-gray-700 dark:text-gray-300 mb-1.5">أسباب ومبررات التبديل المترابط <span class="text-red-500">*</span></label>
              <textarea v-model="formData.swap_notes" rows="2" placeholder="أدخل الأسباب التي أدت إلى خطأ الصرف المتبادل بين الفردين..." class="w-full text-xs p-3 border border-gray-300 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-900 focus:ring-2 focus:ring-brand-500 outline-none resize-none"></textarea>
            </div>
          </div>
        </div>

        <div class="mt-8 flex justify-between items-center pt-6 border-t border-gray-100 dark:border-gray-800">
          <button @click="step = 1" class="text-gray-500 font-bold hover:text-gray-800 dark:hover:text-white px-4 py-2 transition-colors">السابق</button>
          <button @click="validateAndGoToStep3" class="bg-brand-600 text-white px-8 py-2.5 rounded-xl font-bold hover:bg-brand-700 shadow-md shadow-brand-500/20 transition-all">التالي (المرفقات)</button>
        </div>
      </div>

      <!-- Step 3: Attachments & Submit -->
      <div v-if="step === 3" class="bg-white dark:bg-gray-900 border dark:border-gray-800 rounded-2xl p-8 shadow-sm">
        <div class="mb-6 pb-4 border-b border-gray-100 dark:border-gray-800">
          <h2 class="text-lg font-black">الخطوة 3: المرفقات والمستندات الإلزامية</h2>
          <p class="text-sm text-gray-500 mt-1">يجب إرفاق جميع المستندات المطلوبة لاعتماد الخدمة.</p>
        </div>
        
        <div class="space-y-4 mb-8">
          <div v-for="att in schema.attachments" :key="att.doc_type" class="p-4 border border-dashed rounded-xl transition-colors"
            :class="uploadedFiles[att.doc_type] ? 'border-emerald-400 bg-emerald-50/50 dark:bg-emerald-950/20' : 'border-gray-300 dark:border-gray-700'"
          >
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <p class="font-bold text-sm flex items-center gap-2 text-gray-900 dark:text-white">
                  {{ att.label }} <span v-if="att.required" class="text-red-500">*</span>
                  <span v-if="uploadedFiles[att.doc_type]" class="text-emerald-600 text-[10px] bg-emerald-100 dark:bg-emerald-900/50 px-2 py-0.5 rounded font-bold border border-emerald-200 dark:border-emerald-800">✓ تم الرفع</span>
                </p>
                <p class="text-xs text-gray-400 mt-1">صيغ مدعومة: PDF, JPG, PNG (الحد الأقصى 5MB)</p>
                <p v-if="att.label.includes('البطاقة العسكرية') || att.label.includes('البطاقة الوطنية') || att.label.includes('البطاقة الشخصية')" class="text-[10px] text-brand-600 dark:text-brand-400 mt-1 font-bold">
                  💡 ملاحظة: إذا كان المرفق للبطاقة، فيمكنك رفع صورة دمجت فيها الجهتين، أو ملف PDF يحتوي على صورتي الوجهين معاً.
                </p>
                <p v-if="uploadedFiles[att.doc_type]" class="text-xs text-emerald-600 mt-1.5 font-mono bg-white dark:bg-gray-900 inline-block px-2 py-1 rounded border border-emerald-100 dark:border-emerald-900/30">{{ uploadedFiles[att.doc_type].name }}</p>
              </div>
              <div class="flex items-center gap-3 self-end sm:self-auto">
                <label :for="'file-' + att.doc_type" class="cursor-pointer bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 text-xs font-bold px-4 py-2.5 rounded-lg transition-colors shadow-sm">
                  {{ uploadedFiles[att.doc_type] ? 'تغيير الملف' : 'اختيار ملف' }}
                </label>
                <input :id="'file-' + att.doc_type" type="file" @change="handleFileUpload(att.doc_type, $event)" class="hidden" accept=".pdf,.jpg,.jpeg,.png" />
                <span v-if="uploadingDoc === att.doc_type" class="animate-spin h-5 w-5 border-2 border-brand-500 border-t-transparent rounded-full"></span>
              </div>
            </div>
          </div>
          <div v-if="schema.attachments?.length === 0" class="text-center py-6 text-gray-500 text-sm border border-dashed rounded-xl border-gray-200 dark:border-gray-800">
            لا توجد مرفقات مطلوبة لهذه الخدمة.
          </div>
        </div>

        <div class="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-xl border border-gray-100 dark:border-gray-800 mb-8">
          <p class="text-sm font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <svg class="w-5 h-5 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            ملخص العملية
          </p>
          <p class="text-xs text-gray-600 dark:text-gray-400 mt-2">
            سيتم إنشاء الطلب / القرار وتطبيقه على عدد (<span class="font-bold text-brand-600">{{ selectedPersonnelList.length }}</span>) من الأفراد. بعد الاعتماد سيتم حفظ السجلات وتوجيه الطلب حسب مسار الموافقة المعتمد.
          </p>
        </div>

        <!-- Submission Progress overlay -->
        <div v-if="isSubmitting" class="fixed inset-0 z-50 bg-gray-900/50 backdrop-blur-sm flex items-center justify-center">
          <div class="bg-white dark:bg-gray-900 p-8 rounded-2xl shadow-2xl max-w-sm w-full text-center border border-gray-100 dark:border-gray-800">
            <div class="relative w-20 h-20 mx-auto mb-6">
              <svg class="animate-spin text-gray-200 dark:text-gray-700 w-full h-full" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              <span class="absolute inset-0 flex items-center justify-center text-sm font-bold text-brand-600">{{ Math.round((submittedCount / selectedPersonnelList.length) * 100) }}%</span>
            </div>
            <h3 class="text-lg font-black text-gray-900 dark:text-white mb-2">جاري المعالجة...</h3>
            <p class="text-sm text-gray-500">تم تقديم {{ submittedCount }} من أصل {{ selectedPersonnelList.length }} طلب.</p>
          </div>
        </div>

        <div class="mt-8 flex justify-between items-center pt-6 border-t border-gray-100 dark:border-gray-800">
          <button @click="step = 2" class="text-gray-500 font-bold hover:text-gray-800 dark:hover:text-white px-4 py-2 transition-colors" :disabled="isSubmitting">السابق</button>
          <button @click="submitBulk" :disabled="isSubmitting" class="bg-emerald-600 text-white px-8 py-3 rounded-xl font-black hover:bg-emerald-700 shadow-lg shadow-emerald-500/20 transition-all flex items-center gap-2">
            اعتماد وتقديم الطلب
          </button>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { useServicesStore } from '@/stores/services'
import { usePersonnelStore } from '@/stores/personnel'
import { useCorrectionStore } from '@/stores/correction'
import { useRankSettlementStore } from '@/stores/rankSettlement'
import { useDisciplinaryStore } from '@/stores/disciplinary'
import { useCoreStore } from '@/stores/core'
import { useAuthStore } from '@/stores/auth'
import api from '@/lib/api'
import NationalIdWizard from '@/components/common/NationalIdWizard.vue'

const authStore = useAuthStore()
const coreStore = useCoreStore()
const route = useRoute()
const router = useRouter()
const servicesStore = useServicesStore()
const personnelStore = usePersonnelStore()
const correctionStore = useCorrectionStore()
const rankSettlementStore = useRankSettlementStore()
const disciplinaryStore = useDisciplinaryStore()

const type = route.query.type as string
const category = (route.query.category as string) || 'form'
const schema = ref<any>(null)
const loading = ref(true)
const error = ref('')

const step = ref(1)
const stepLabels = ['تحديد الأفراد', 'تعبئة البيانات', 'المرفقات والتقديم']

// Step 1 State
const searchQuery = ref('')
const searchResults = ref<any[]>([])
const searchPerformed = ref(false)
const selectedPersonnelList = ref<any[]>([])

// Header Data
const localHeaderData = reactive({
  birth_gov_id: null as number | null,
  birth_district_id: null as number | null,
  birth_sub_district_id: null as number | null,
  birth_village_id: null as number | null,
  residence_gov_id: null as number | null,
  residence_district_id: null as number | null,
  residence_sub_district_id: null as number | null,
  residence_village_id: null as number | null,
  id_issue_date: '',
  id_issue_place: ''
})

const headerDistrictsCache = ref<Record<number, any[]>>({})
const headerSubDistrictsCache = ref<Record<number, any[]>>({})
const headerVillagesCache = ref<Record<number, any[]>>({})

async function fetchHeaderDistricts(govId: number) {
  if (!govId || headerDistrictsCache.value[govId]) return;
  try {
    const res = await api.get(`/dictionaries/geo/districts/?governorate=${govId}&page_size=1000`)
    headerDistrictsCache.value[govId] = res.data?.results || res.data || []
  } catch { headerDistrictsCache.value[govId] = [] }
}

async function fetchHeaderSubDistricts(distId: number) {
  if (!distId || headerSubDistrictsCache.value[distId]) return;
  try {
    const res = await api.get(`/dictionaries/geo/sub-districts/?district=${distId}&page_size=1000`)
    headerSubDistrictsCache.value[distId] = res.data?.results || res.data || []
  } catch { headerSubDistrictsCache.value[distId] = [] }
}

async function fetchHeaderVillages(subDistId: number) {
  if (!subDistId || headerVillagesCache.value[subDistId]) return;
  try {
    const res = await api.get(`/dictionaries/geo/villages/?sub_district=${subDistId}&page_size=1000`)
    headerVillagesCache.value[subDistId] = res.data?.results || res.data || []
  } catch { headerVillagesCache.value[subDistId] = [] }
}

watch(() => localHeaderData.birth_gov_id, (newGov) => {
  localHeaderData.birth_district_id = null;
  localHeaderData.birth_sub_district_id = null;
  localHeaderData.birth_village_id = null;
  if (newGov) fetchHeaderDistricts(newGov);
})
watch(() => localHeaderData.residence_gov_id, (newGov) => {
  localHeaderData.residence_district_id = null;
  localHeaderData.residence_sub_district_id = null;
  localHeaderData.residence_village_id = null;
  if (newGov) fetchHeaderDistricts(newGov);
})
watch(() => localHeaderData.birth_district_id, (newDist) => {
  localHeaderData.birth_sub_district_id = null;
  localHeaderData.birth_village_id = null;
  if (newDist) fetchHeaderSubDistricts(newDist);
})
watch(() => localHeaderData.residence_district_id, (newDist) => {
  localHeaderData.residence_sub_district_id = null;
  localHeaderData.residence_village_id = null;
  if (newDist) fetchHeaderSubDistricts(newDist);
})
watch(() => localHeaderData.birth_sub_district_id, (newSub) => {
  localHeaderData.birth_village_id = null;
  if (newSub) fetchHeaderVillages(newSub);
})
watch(() => localHeaderData.residence_sub_district_id, (newSub) => {
  localHeaderData.residence_village_id = null;
  if (newSub) fetchHeaderVillages(newSub);
})

watch(selectedPersonnelList, (newVal) => {
  if (newVal && newVal.length > 0) {
    const p = newVal[0];
    localHeaderData.birth_gov_id = p.birth_gov_id || null;
    localHeaderData.birth_district_id = null; // Normally map from DB if exists
    localHeaderData.birth_sub_district_id = null;
    localHeaderData.birth_village_id = null;
    localHeaderData.residence_gov_id = p.residence_gov_id || null;
    localHeaderData.residence_district_id = null;
    localHeaderData.residence_sub_district_id = null;
    localHeaderData.residence_village_id = null;
    localHeaderData.id_issue_date = p.id_issue_date || '';
    localHeaderData.id_issue_place = p.id_issue_place || '';
  }
}, { deep: true })

// Step 2 & 3 State
const formData = ref<any>({
  new_values: {},
  notes: {},
  correction_targets: []
})
const documentIds = ref<number[]>([])
const uploadedFiles = ref<Record<string, File>>({})
const uploadingDoc = ref<string | null>(null)

// Submission State
const isSubmitting = ref(false)
const submittedCount = ref(0)

// Location Cascade State
const locationState = reactive<Record<string, any>>({})
const governorates = ref<any[]>([])
const districtsCache = ref<Record<number, any[]>>({})
const subDistrictsCache = ref<Record<number, any[]>>({})
const villagesCache = ref<Record<number, any[]>>({})

async function loadGovernorates() {
  try {
    const res = await api.get('/dictionaries/geo/governorates/')
    governorates.value = res.data?.results || res.data || []
  } catch { governorates.value = [] }
}

function getFilteredOptions(field: any) {
  if (!field.options) return []
  if (field.key === 'to_rank') {
    const person = selectedPersonnelList.value[0]
    if (!person) return field.options

    const currentRankId = person.current_rank?.id || person.current_rank_id || person.current_rank
    if (!currentRankId) return field.options

    const currentRank = field.options.find((o: any) => String(o.value) === String(currentRankId))
    const currentRankOrder = currentRank ? currentRank.order : 999
    const currentRankIsOfficer = currentRank ? currentRank.is_officer : false

    const settlementType = formData.value.settlement_type

    if (settlementType === 'personnel_to_officer') {
      const officerRanks = field.options.filter((o: any) => o.is_officer)
      if (officerRanks.length === 0) return []
      const lowestOfficerRankOrder = Math.max(...officerRanks.map((r: any) => r.order))
      return officerRanks.filter((o: any) => o.order === lowestOfficerRankOrder)
    } else if (settlementType === 'same_class_promotion') {
      const sameClassRanks = field.options.filter((o: any) => o.is_officer === currentRankIsOfficer && o.order < currentRankOrder)
      if (sameClassRanks.length === 0) return []
      const immediateNextRankOrder = Math.max(...sameClassRanks.map((r: any) => r.order))
      return sameClassRanks.filter((o: any) => o.order === immediateNextRankOrder)
    } else if (settlementType === 'demotion') {
      const sameClassRanks = field.options.filter((o: any) => o.is_officer === currentRankIsOfficer && o.order > currentRankOrder)
      if (sameClassRanks.length === 0) return []
      const immediateLowerRankOrder = Math.min(...sameClassRanks.map((r: any) => r.order))
      return sameClassRanks.filter((o: any) => o.order === immediateLowerRankOrder)
    }
  }
  return field.options
}

watch(() => formData.value.settlement_type, () => {
  formData.value.to_rank = ''
  
  // Auto-select if there is exactly 1 valid option based on intelligent filtering
  setTimeout(() => {
    const toRankField = schema.value?.sections?.find((s:any) => s.source === 'user_input')?.fields?.find((f:any) => f.key === 'to_rank')
    if (toRankField) {
      const filtered = getFilteredOptions(toRankField)
      if (filtered.length === 1) {
        formData.value.to_rank = filtered[0].value
      }
    }
  }, 50)
})

function getDistricts(fieldKey: string): any[] {
  const govId = locationState[fieldKey + '_gov']
  return govId ? (districtsCache.value[govId] || []) : []
}

function getSubDistricts(fieldKey: string): any[] {
  const distId = locationState[fieldKey + '_dist']
  return distId ? (subDistrictsCache.value[distId] || []) : []
}

function getVillages(fieldKey: string): any[] {
  const subId = locationState[fieldKey + '_sub']
  return subId ? (villagesCache.value[subId] || []) : []
}

async function onGovernorateChange(fieldKey: string) {
  locationState[fieldKey + '_dist'] = ''
  locationState[fieldKey + '_sub'] = ''
  locationState[fieldKey + '_vil'] = ''
  formData.value[fieldKey] = ''
  const govId = locationState[fieldKey + '_gov']
  if (!govId) return
  if (!districtsCache.value[govId]) {
    try {
      const res = await api.get(`/dictionaries/geo/districts/?governorate=${govId}`)
      districtsCache.value[govId] = res.data?.results || res.data || []
    } catch { districtsCache.value[govId] = [] }
  }
  // Set partial location
  const gov = governorates.value.find((g: any) => g.id === govId)
  if (gov) formData.value[fieldKey] = gov.name_ar
}

async function onDistrictChange(fieldKey: string) {
  locationState[fieldKey + '_sub'] = ''
  locationState[fieldKey + '_vil'] = ''
  const distId = locationState[fieldKey + '_dist']
  const govId = locationState[fieldKey + '_gov']
  if (!distId) return
  if (!subDistrictsCache.value[distId]) {
    try {
      const res = await api.get(`/dictionaries/geo/sub-districts/?district=${distId}`)
      subDistrictsCache.value[distId] = res.data?.results || res.data || []
    } catch { subDistrictsCache.value[distId] = [] }
  }
  const gov = governorates.value.find((g: any) => g.id === govId)
  const dist = (districtsCache.value[govId] || []).find((d: any) => d.id === distId)
  formData.value[fieldKey] = [gov?.name_ar, dist?.name_ar].filter(Boolean).join(' — ')
}

async function onSubDistrictChange(fieldKey: string) {
  locationState[fieldKey + '_vil'] = ''
  const govId = locationState[fieldKey + '_gov']
  const distId = locationState[fieldKey + '_dist']
  const subId = locationState[fieldKey + '_sub']
  
  if (!subId) return
  if (!villagesCache.value[subId]) {
    try {
      const res = await api.get(`/dictionaries/geo/villages/?sub_district=${subId}`)
      villagesCache.value[subId] = res.data?.results || res.data || []
    } catch { villagesCache.value[subId] = [] }
  }
  
  const gov = governorates.value.find((g: any) => g.id === govId)
  const dist = (districtsCache.value[govId] || []).find((d: any) => d.id === distId)
  const sub = (subDistrictsCache.value[distId] || []).find((s: any) => s.id === subId)
  formData.value[fieldKey] = [gov?.name_ar, dist?.name_ar, sub?.name_ar].filter(Boolean).join(' — ')
}

function onVillageChange(fieldKey: string) {
  const govId = locationState[fieldKey + '_gov']
  const distId = locationState[fieldKey + '_dist']
  const subId = locationState[fieldKey + '_sub']
  const vilId = locationState[fieldKey + '_vil']
  const gov = governorates.value.find((g: any) => g.id === govId)
  const dist = (districtsCache.value[govId] || []).find((d: any) => d.id === distId)
  const sub = (subDistrictsCache.value[distId] || []).find((s: any) => s.id === subId)
  const vil = (villagesCache.value[subId] || []).find((v: any) => v.id === vilId)
  formData.value[fieldKey] = [gov?.name_ar, dist?.name_ar, sub?.name_ar, vil?.name_ar || vil?.name_ar_normalized].filter(Boolean).join(' — ')
}

// Name Correction Special Fields
const nameParts = reactive({
  first: '',
  second: '',
  third: '',
  fourth: '',
  surname: ''
})
const notes = ref('')

const generatedFullName = computed(() => {
  const parts = [
    nameParts.first.trim(),
    nameParts.second.trim(),
    nameParts.third.trim(),
    nameParts.fourth.trim(),
    nameParts.surname.trim()
  ].filter(p => p !== '')
  return parts.join(' ')
})

const isValidArabic = computed(() => {
  if (!generatedFullName.value) return false
  const arRegex = /^[\u0621-\u064A\s]+$/
  return arRegex.test(generatedFullName.value)
})

const hasFiveParts = computed(() => {
  return (
    nameParts.first.trim() !== '' &&
    nameParts.second.trim() !== '' &&
    nameParts.third.trim() !== '' &&
    nameParts.fourth.trim() !== '' &&
    nameParts.surname.trim() !== ''
  )
})

const isDifferentName = computed(() => {
  if (selectedPersonnelList.value.length === 0 || !generatedFullName.value) return false
  return selectedPersonnelList.value[0].full_name !== generatedFullName.value
})

const hasPendingNameCorrection = computed(() => {
  if (selectedPersonnelList.value.length === 0) return false
  const person = selectedPersonnelList.value[0]
  if (!person.pending_corrections) return false
  return person.pending_corrections.some(
    (c: any) => c.field_name === 'full_name' && c.status === 'pending'
  )
})

const pendingNameCorrectionDetails = computed(() => {
  if (selectedPersonnelList.value.length === 0) return null
  const person = selectedPersonnelList.value[0]
  if (!person.pending_corrections) return null
  return person.pending_corrections.find(
    (c: any) => c.field_name === 'full_name' && c.status === 'pending'
  )
})

function updateFullName() {
  formData.value.new_value = generatedFullName.value
}

// National ID duplicate verification state
const nidState = ref<Record<string, { isValidating: boolean, error: string }>>({})

async function verifyNidDuplicate(militaryNumber: string, val: string) {
  if (!nidState.value[militaryNumber]) {
    nidState.value[militaryNumber] = { isValidating: false, error: '' }
  }
  nidState.value[militaryNumber].isValidating = true
  nidState.value[militaryNumber].error = ''
  
  try {
    const res = await personnelStore.checkNationalId(val)
    if (res.exists) {
      nidState.value[militaryNumber].error = `الرقم مسجل مسبقاً للفرد (${res.personnel?.full_name || res.personnel_name})`
      formData.value.new_values[militaryNumber] = null // invalid
    } else if (!res.valid_format) {
      nidState.value[militaryNumber].error = 'تنسيق الرقم غير صحيح أو يحتوي على قيم غير مسموحة'
      formData.value.new_values[militaryNumber] = null
    }
  } catch (err) {
    nidState.value[militaryNumber].error = 'حدث خطأ أثناء فحص التكرار السحابي'
  } finally {
    nidState.value[militaryNumber].isValidating = false
  }
}

function clearNidError(militaryNumber: string) {
  if (nidState.value[militaryNumber]) {
    nidState.value[militaryNumber].error = ''
  }
}

onMounted(async () => {
  if (coreStore.governorates.length === 0) {
    await coreStore.fetchAllReferences()
  }
  await loadGovernorates()

  if (!type) {
    error.value = 'الرجاء اختيار نوع الخدمة من الدليل.'
    loading.value = false
    return
  }
  
  try {
    const res = await servicesStore.fetchFormSchema(type)
    if (res) {
      schema.value = res
      // Initialize form data
      const userSection = res.sections?.find((s: any) => s.source === 'user_input')
      if (userSection) {
        userSection.fields.forEach((f: any) => {
          formData.value[f.key] = f.default !== undefined ? f.default : (f.value !== undefined ? f.value : '')
          // Auto-select if only one option
          if (f.type === 'select' && f.options?.length === 1) {
            formData.value[f.key] = f.options[0].value || f.options[0]
          }
        })
        // Load governorates if any location_cascade field exists
        const hasLocationField = userSection.fields.some((f: any) => f.type === 'location_cascade')
        if (hasLocationField) {
          loadGovernorates()
        }

        // Load ranks if any select field is to_rank
        const rankField = userSection.fields.find((f: any) => f.key === 'to_rank')
        if (rankField) {
          try {
            const ranksRes = await api.get('/dictionaries/ranks/?page_size=1000')
            const ranks = ranksRes.data?.results || ranksRes.data || []
            rankField.options = ranks.map((r: any) => ({
              value: r.id,
              label: r.name,
              order: r.order,
              is_officer: r.is_officer
            }))
          } catch (e) {
            console.error('Failed to load ranks:', e)
          }
        }
      }
    } else {
      error.value = 'هذه الاستمارة غير متاحة حالياً.'
    }
  } catch (err: any) {
    error.value = 'فشل جلب هيكل وتفاصيل الخدمة من قاعدة البيانات.'
  } finally {
    loading.value = false
  }
})

// === Step 1 Logic ===
async function searchPersonnel() {
  if (!searchQuery.value) return
  searchPerformed.value = true
  await personnelStore.fetchPersonnel({ search: searchQuery.value, page: 1 })
  searchResults.value = personnelStore.records
}

function handlePersonnelSelection(personnel: any) {
  if (personnel) {
    if (!selectedPersonnelList.value.find(p => p.military_number === personnel.military_number)) {
      selectedPersonnelList.value.push(personnel)
    }
  }
}

function isPersonnelSelected(militaryNumber: string) {
  return selectedPersonnelList.value.some(p => p.military_number === militaryNumber)
}

async function addPersonnel(person: any) {
  if (category === 'correction' && selectedPersonnelList.value.length >= 1) {
    if (type !== 'linked_military_swap') {
      Swal.fire({
        icon: 'info',
        title: 'فرد واحد فقط',
        text: 'خدمات تصحيح البيانات تتم لفرد واحد فقط في كل طلب. لا يمكنك تحديد أكثر من شخص.'
      })
      return
    } else if (selectedPersonnelList.value.length >= 2) {
      Swal.fire({
        icon: 'info',
        title: 'فردين فقط',
        text: 'التبديل المترابط يتم بين فردين فقط.'
      })
      return
    }
  }
  
  if (!isPersonnelSelected(person.military_number)) {
    if (category === 'correction') {
      try {
        const res = await api.get(`/personnel/${person.military_number}/`)
        const detailedPerson = res.data?.data || res.data
        selectedPersonnelList.value.push(detailedPerson)
      } catch (err) {
        console.error('Failed to fetch detailed personnel info', err)
        selectedPersonnelList.value.push(person)
      }
    } else {
      selectedPersonnelList.value.push(person)
    }
  }
}

function removePersonnel(militaryNumber: string) {
  selectedPersonnelList.value = selectedPersonnelList.value.filter(p => p.military_number !== militaryNumber)
}

function addAllSearchResults() {
  if (category === 'correction') {
    Swal.fire({
      icon: 'info',
      title: 'غير مسموح',
      text: 'لا يمكن تقديم طلب تصحيح بشكل جماعي.'
    })
    return
  }
  searchResults.value.forEach(p => {
    addPersonnel(p)
  })
}

async function goToStep2() {
  if (selectedPersonnelList.value.length === 0) return
  
  if (selectedPersonnelList.value.length === 1 && category === 'correction') {
    const person = selectedPersonnelList.value[0]
    if (!person.pending_corrections) {
      try {
        const res = await api.get(`/personnel/${person.military_number}/`)
        const detailedPerson = res.data?.data || res.data
        selectedPersonnelList.value[0] = detailedPerson
      } catch (err) {
        console.error(err)
      }
    }
    
    const updatedPerson = selectedPersonnelList.value[0]
    if (type === 'name_correction') {
      formData.value.old_value = updatedPerson.full_name
      nameParts.first = ''
      nameParts.second = ''
      nameParts.third = ''
      nameParts.fourth = ''
      nameParts.surname = ''
      notes.value = ''
    }
    else if (type === 'national_id_correction') formData.value.old_value = updatedPerson.national_id
    else if (type === 'military_number_correction') formData.value.old_value = updatedPerson.military_number
  }
  
  step.value = 2
}

// === Step 2 Logic ===
async function validateAndGoToStep3() {
  if (type === 'name_correction') {
    if (hasPendingNameCorrection.value) {
      Swal.fire({
        icon: 'error',
        title: 'طلب معلق موجود',
        text: 'يوجد بالفعل طلب تصحيح اسم معلق لهذا الفرد.'
      })
      return
    }
    if (!hasFiveParts.value) {
      Swal.fire({
        icon: 'warning',
        title: 'الاسم غير مكتمل',
        text: 'الرجاء إدخال الاسم الجديد المكون من 5 أجزاء بالكامل.'
      })
      return
    }
    if (!isValidArabic.value) {
      Swal.fire({
        icon: 'warning',
        title: 'صيغة غير صحيحة',
        text: 'يجب أن يحتوي الاسم على أحرف عربية ومسافات فقط.'
      })
      return
    }
    if (!isDifferentName.value) {
      Swal.fire({
        icon: 'warning',
        title: 'تطابق الأسماء',
        text: 'الاسم الجديد يجب أن يكون مختلفاً عن الاسم الحالي.'
      })
      return
    }
    if (!notes.value.trim()) {
      Swal.fire({
        icon: 'warning',
        title: 'بيانات ناقصة',
        text: 'الرجاء إدخال أسباب ومبررات التعديل.'
      })
      return
    }
    
    formData.value.new_value = generatedFullName.value
    
    let finalReason = notes.value.trim()
    if (formData.value.correction_targets && formData.value.correction_targets.length > 0) {
      finalReason = `المطلوب تصحيحه: ${formData.value.correction_targets.join('، ')} \n المبررات: ${finalReason}`
    }
    
    formData.value.notes = finalReason
    formData.value.reason = finalReason
    step.value = 3
    return
  }

  if (category === 'correction') {
    if (type === 'linked_military_swap') {
      if (!formData.value.swap_notes) {
        Swal.fire({
          icon: 'warning',
          title: 'بيانات ناقصة',
          text: 'الرجاء إدخال أسباب ومبررات التبديل المترابط.'
        })
        return
      }
    } else if (type === 'national_id_correction') {
      for (const person of selectedPersonnelList.value) {
        const val = formData.value.new_values?.[person.military_number]
        const note = formData.value.notes?.[person.military_number]
        if (!val || val.length !== 11) {
          Swal.fire({ icon: 'warning', title: 'بيانات ناقصة', text: 'الرجاء كتابة الرقم الوطني الصحيح بالكامل (11 رقم) للفرد ' + person.full_name })
          return
        }
        if (nidState.value[person.military_number]?.error) {
          Swal.fire({ icon: 'error', title: 'رقم وطني غير صالح', text: `يوجد خطأ في الرقم الوطني للفرد ${person.full_name}: ${nidState.value[person.military_number].error}` })
          return
        }
        if (!note || note.trim().length < 5) {
          Swal.fire({ icon: 'warning', title: 'ملاحظات ناقصة', text: 'الرجاء إدخال أسباب التصحيح بشكل واضح للفرد ' + person.full_name })
          return
        }
      }
    } else if (type === 'military_number_correction') {
      for (const person of selectedPersonnelList.value) {
        const val = formData.value.new_values?.[person.military_number]
        const note = formData.value.notes?.[person.military_number]
        if (!val || !note) {
          Swal.fire({ icon: 'warning', title: 'بيانات ناقصة', text: 'الرجاء تعبئة جميع الحقول الإلزامية للفرد ' + person.full_name })
          return
        }
        if (val.length < 4 || isNaN(Number(val))) {
          Swal.fire({ icon: 'warning', title: 'رقم عسكري غير صالح', text: 'الرجاء إدخال رقم عسكري صالح للفرد ' + person.full_name })
          return
        }
        if (person.military_number === val) {
          Swal.fire({ icon: 'warning', title: 'رقم مطابق', text: 'الرقم العسكري الصحيح يجب أن يكون مختلفاً عن الرقم العسكري الخاطئ للفرد ' + person.full_name })
          return
        }

        const officerKeywords = ['ملازم', 'نقيب', 'رائد', 'مقدم', 'عقيد', 'عميد', 'لواء', 'فريق', 'مشير']
        const isOfficer = person.rank?.is_officer || person.current_rank?.is_officer || (person.rank_name && officerKeywords.some(r => person.rank_name.includes(r)))

        if (isOfficer) {
          if (!val.startsWith('60') || val.length !== 7) {
            Swal.fire({
              icon: 'warning',
              title: 'رقم عسكري غير صالح للضابط',
              text: `الرقم العسكري الجديد للضابط (${person.full_name}) يجب أن يبدأ بـ 60 ويتكون من 7 أرقام.`
            })
            return
          }
        } else {
          if (val.startsWith('60')) {
            Swal.fire({
              icon: 'warning',
              title: 'رقم عسكري غير صالح للأفراد',
              text: `الرقم العسكري الجديد للأفراد (${person.full_name}) لا يمكن أن يبدأ بـ 60 لأن رتبته (${person.rank_name || person.rank?.name || 'أفراد'}) لا تسمح بذلك.`
            })
            return
          }
        }
      }
    }
    step.value = 3
    return
  }

  // Check required fields in the user_input section
  const userSection = schema.value.sections?.find((s: any) => s.source === 'user_input')
  if (userSection) {
      const missing = userSection.fields.filter((f: any) => {
        if (f.key === 'new_military_number') {
          return formData.value.settlement_type === 'personnel_to_officer' && !formData.value[f.key]
        }
        return f.required && !formData.value[f.key]
      })
      if (missing.length > 0) {
        Swal.fire({
          icon: 'warning',
          title: 'بيانات ناقصة',
          text: `الرجاء تعبئة الحقول الإلزامية: ${missing.map((f:any) => f.label).join('، ')}`
        })
        return
      }

      // Rank Settlement validations
      if (formData.value.settlement_type === 'personnel_to_officer' && formData.value.new_military_number) {
        const milNum = formData.value.new_military_number
        if (!milNum.startsWith('60') || milNum.length !== 7 || isNaN(Number(milNum))) {
          Swal.fire({
            icon: 'warning',
            title: 'رقم عسكري غير صالح',
            text: 'الرقم العسكري الجديد للضابط يجب أن يبدأ بـ 60 ويتكون من 7 أرقام.'
          })
          return
        }

        // Live check military number
        try {
          const checkRes = await api.get('/personnel/check-military-number/', { params: { value: milNum } })
          if (checkRes.data?.exists) {
            Swal.fire({
              icon: 'error',
              title: 'الرقم العسكري مستخدم',
              text: 'هذا الرقم العسكري مستخدم بالفعل في النظام.'
            })
            return
          }
        } catch (e) {
          console.error(e)
        }
      }

    }
  step.value = 3
}

// === Step 3 Logic ===
async function handleFileUpload(docType: string, event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  uploadingDoc.value = docType
  uploadedFiles.value[docType] = file

  try {
    const fd = new FormData()
    fd.append('file', file)
    fd.append('document_type', docType)
    
    const res = await api.post('/storage/upload/', fd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    const docId = res.data?.data?.id || res.data?.id
    if (docId) {
      documentIds.value.push(docId)
    }
  } catch (err: any) {
    console.warn('Document API tracking file locally:', err.message)
    if (!documentIds.value.includes(1)) documentIds.value.push(1) // fallback mock
  } finally {
    uploadingDoc.value = null
  }
}

async function submitBulk() {
  if (selectedPersonnelList.value.length === 0) return

  // Validate required attachments
  const requiredDocs = schema.value.attachments?.filter((a:any) => a.required) || []
  const missingDocs = requiredDocs.filter((a:any) => !uploadedFiles.value[a.doc_type])
  
  if (missingDocs.length > 0) {
    Swal.fire({
      icon: 'error',
      title: 'مرفقات ناقصة',
      text: `الرجاء إرفاق المستندات الإلزامية: ${missingDocs.map((a:any) => a.label).join('، ')}`
    })
    return
  }

  isSubmitting.value = true

  // Validate User Input Fields
  if (category !== 'correction') {
    const userSection = schema.value.sections?.find((s:any) => s.source === 'user_input')
    if (userSection) {
      for (const f of userSection.fields) {
        const val = formData.value[f.key]
        
        // 1. Required Check
      if (f.required && !f.disabled && (val === undefined || val === null || val === '')) {
        Swal.fire({
          icon: 'error',
          title: 'بيانات غير مكتملة',
          text: `الرجاء تعبئة الحقل الإلزامي: ${f.label}`
        })
        return
      }

      // 2. National ID 11 digits Check
      if (val && (f.key === 'national_id' || (f.key === 'new_value' && (type === 'national_id_correction' || formData.value.correction_type === 'national_id_correction')))) {
        if (!/^\d{11}$/.test(String(val))) {
          Swal.fire({
            icon: 'error',
            title: 'خطأ في الإدخال',
            text: `الرقم الوطني (${f.label}) يجب أن يتكون من 11 رقماً بالضبط.`
          })
          return
        }
      }

      // 3. Date Check (No Future Dates except allowed)
      if (val && f.type === 'date') {
        const allowedFuture = ['end_date', 'due_date']
        const today = new Date().toISOString().split('T')[0]
        if (!allowedFuture.includes(f.key) && val > today) {
          Swal.fire({
            icon: 'error',
            title: 'تاريخ غير صالح',
            text: `تاريخ الحقل "${f.label}" لا يمكن أن يكون في المستقبل.`
          })
          return
        }
      }
      }
    }
  }

  isSubmitting.value = true
  submittedCount.value = 0
  let successCount = 0
  let errorCount = 0
  const errorMessages: string[] = []

  let lastCorrectionId = null
  let lastFormId = null
  for (const person of selectedPersonnelList.value) {
    try {
      if (category === 'correction') {
        let finalNewValue = formData.value.new_value || ''
        let finalReason = formData.value.notes || formData.value.reason || ''
        let finalField = formData.value.field_name || formData.value.field || type
        let finalCorrectionType = formData.value.correction_type || null

        if (type === 'national_id_correction' || type === 'military_number_correction') {
          finalNewValue = formData.value.new_values?.[person.military_number] || ''
          finalReason = formData.value.notes?.[person.military_number] || ''
          finalField = type
          finalCorrectionType = type
          
          if (!finalNewValue || !finalReason) {
            throw new Error(`Missing required fields for ${person.military_number}`)
          }
        } else if (type === 'linked_military_swap') {
          const otherPerson = selectedPersonnelList.value.find((p:any) => p.military_number !== person.military_number)
          if (otherPerson) {
            finalNewValue = otherPerson.military_number
          }
          finalReason = formData.value.swap_notes || ''
          finalField = 'military_number_correction'
          finalCorrectionType = 'military_number_correction'
          
          if (!finalNewValue || !finalReason) {
            throw new Error(`Missing required fields for swap`)
          }
        }

        const req = await correctionStore.submitCorrection({
          military_number: person.military_number,
          field: finalField,
          correction_type: finalCorrectionType,
          old_value: formData.value.old_value || '',
          new_value: finalNewValue,
          reason: finalReason,
          document_ids: documentIds.value
        })
        if (req && req.id) lastCorrectionId = req.id
      } else if (category === 'rank_settlement') {
        await rankSettlementStore.createSettlement({
          personnel_military_number_input: person.military_number,
          settlement_type: formData.value.settlement_type || type,
          from_rank: person.current_rank,
          to_rank: formData.value.to_rank,
          new_military_number: formData.value.new_military_number || null,
          decision_number: formData.value.decision_number || '',
          decision_date: formData.value.decision_date || null,
          due_date: formData.value.due_date || null,
          notes: formData.value.notes || '',
          supporting_document: documentIds.value?.length > 0 ? documentIds.value[0] : null
        })
      } else if (category === 'disciplinary') {
        await disciplinaryStore.createAction({
          personnel: person.military_number,
          action_type: formData.value.action_type || type,
          source_type: formData.value.source_type || 'direct_superior',
          issued_by_name: formData.value.issued_by_name || '',
          decision_ref: formData.value.decision_ref || '',
          issued_date: formData.value.issued_date || new Date().toISOString().split('T')[0],
          effective_date: formData.value.effective_date || new Date().toISOString().split('T')[0],
          duration_days: formData.value.duration_days || null,
          description: formData.value.description || formData.value.notes || '',
          document_ids: documentIds.value
        })
      } else {
        // Default: forms
        const createRes = await servicesStore.createForm({
          personnel: person.military_number,
          form_type: type,
          form_data: formData.value,
          document_ids: documentIds.value
        })
        if (createRes.success && createRes.data?.id) {
          await servicesStore.submitForm(createRes.data.id)
          lastFormId = createRes.data.id
        }
      }
      successCount++
    } catch (err: any) {
      console.error('Submission error for', person.military_number, err)
      
      // Extract specific backend error message
      let msg = 'حدث خطأ غير معروف'
      if (err.response?.data) {
        if (typeof err.response.data.error === 'string') {
          msg = err.response.data.error
        } else if (typeof err.response.data === 'object') {
          // Flatten DRF validation errors
          const errors = []
          for (const [key, value] of Object.entries(err.response.data)) {
            if (Array.isArray(value)) {
              errors.push(value[0])
            } else if (typeof value === 'string') {
              errors.push(value)
            }
          }
          if (errors.length > 0) msg = errors.join('<br>')
        }
      }
      errorMessages.push(`الفرد ${person.full_name}: ${msg}`)
      errorCount++
    }
    submittedCount.value++
  }

  isSubmitting.value = false

  if (successCount > 0) {
    const isModel23 = type === 'name_correction' && successCount === 1;
    const isExternalForm = schema.value?.approval_type === 'external' && successCount === 1;
    const showPrintButton = isModel23 || isExternalForm;
    
    let htmlContent = `تم رفع <b>${successCount}</b> طلب للمراجعة.`
    if (errorCount > 0) {
      htmlContent += `<br/><br/><span class="text-red-500">تعذر معالجة <b>${errorCount}</b> طلب:</span><br/>`
      htmlContent += `<div class="text-xs text-right mt-2 text-red-600 bg-red-50 p-2 rounded max-h-32 overflow-y-auto">${errorMessages.join('<br>')}</div>`
    }

    Swal.fire({
      icon: errorCount > 0 ? 'warning' : 'success',
      title: errorCount > 0 ? 'تم الإنجاز جزئياً' : 'تم تقديم الطلبات بنجاح',
      html: htmlContent,
      confirmButtonText: 'انتقال لقائمة الطلبات',
      showDenyButton: showPrintButton,
      denyButtonText: '<i class="fas fa-print ml-2"></i> طباعة النموذج',
      denyButtonColor: '#059669', // Emerald
      customClass: {
        denyButton: 'px-6 py-2.5 rounded-xl font-bold text-white',
        confirmButton: 'px-6 py-2.5 rounded-xl font-bold bg-brand-600 text-white'
      }
    }).then(async (result) => {
      if (result.isDenied) {
        if (isModel23 && lastCorrectionId) {
          const person = selectedPersonnelList.value[0]
          const corrType = schema.value?.name || 'طلب تصحيح'
          const txNum = `CORR-${String(lastCorrectionId).padStart(5, '0')}`
          const dateNow = new Date().toLocaleDateString('ar-YE', { year: 'numeric', month: '2-digit', day: '2-digit' })
          const corrTarget = (formData.value.correction_targets && formData.value.correction_targets.length > 0)
            ? formData.value.correction_targets.join('، ') : corrType
          let draft = {
            documentType: 'PERSONNEL_MEMO', securityLevel: 'NORMAL',
            referenceNo: txNum, docDate: dateNow, correspondingDate: '',
            attachments: 'نموذج رقم (23) — كشف المطابقة', bilingual: false,
            issuerLine1: '', issuerLine2: '', issuerLine3: '',
            addressees: [{ prefix: 'الأخ /', name: 'المدير العام للمحافظة', suffix: 'المحترم' }],
            involvedPersonnel: [{
              militaryId: person.military_number, rank: person.rank_name || '',
              name: person.full_name, nationalId: '',
              correctName: formData.value.new_value || '',
              wrongName: formData.value.old_value || '',
              correctionTarget: corrTarget,
              notes: formData.value.reason || formData.value.notes || '',
            }],
            subject: `طلب تصحيح بيانات — ${person.full_name}`,
            body: `<p>نحيط سيادتكم علماً بأنه ورد إلينا طلب تصحيح بيانات للمنتسب/المنتسبين الموضحين أعلاه.</p>
<p>نرفق لكم كشفاً بأسماء المطلوب تصحيح أسمائهم <strong>(كشف المطابقة — نموذج 23)</strong>، مع مرفقات كل فرد، وذلك لاتخاذ الإجراءات اللازمة.</p>`,
            conclusion: '<p>والله الموفق ،،،</p>',
            signatures: [
              { title: 'رئيس قسم الخدمات', rank: '', name: '', showSeal: false },
              { title: 'مدير إدارة القوى البشرية', rank: '', name: '', showSeal: true },
            ],
            signatureSettings: { showLabels: true, showFrame: true },
            visibleColumns: { militaryId: true, rank: true, nationalId: false, status: false, workplace: false, serviceLocation: false, jobTitle: false, position: false, qualification: false, joinDate: false, commencementDate: false, phone: false, clarification: false, notes: true, correctName: true, wrongName: true, correctionTarget: true },
            typography: {
              addressee: { family: 'Cairo', size: 1.1, weight: 'font-bold', underline: true },
              greeting: { family: 'Cairo', size: 1.0, weight: 'font-bold', underline: true },
              subject: { family: 'Cairo', size: 1.15, weight: 'font-black', underline: true },
              body: { family: 'Cairo', size: 1.0, weight: 'font-normal', underline: false },
              conclusionSeparator: { family: 'Cairo', size: 1.1, weight: 'font-bold', underline: true },
              conclusionBody: { family: 'Cairo', size: 1.0, weight: 'font-normal', underline: false },
              signatures: { family: 'Cairo', size: 0.95, weight: 'font-bold', underline: false },
            },
          }
                    const tplStr = localStorage.getItem('memo_template_CORRECTION');
          if (tplStr) {
            try {
              const tpl = JSON.parse(tplStr);
              draft = { ...draft, ...tpl, referenceNo: draft.referenceNo, docDate: draft.docDate, involvedPersonnel: [] };
            } catch(e) {}
          }
          localStorage.setItem('official_memo_draft', JSON.stringify(draft))
          window.open('/admin/documents/memo-preview', '_blank')
          router.push('/services/transactions?tab=internal')
        } else if (isExternalForm && lastFormId) {
          try { await servicesStore.markFormPrinted(lastFormId) } catch(_) {}
          // فتح منشئ المذكرات
          const person = selectedPersonnelList.value[0]
          const fType = schema.value?.name || ''
          const txNum2 = `TX-${String(lastFormId).padStart(6, '0')}`
          const dateNow2 = new Date().toLocaleDateString('ar-YE', { year: 'numeric', month: '2-digit', day: '2-digit' })
          let draft2 = {
            documentType: 'PERSONNEL_MEMO', securityLevel: 'NORMAL',
            referenceNo: txNum2, docDate: dateNow2, correspondingDate: '',
            attachments: 'نموذج إثبات حالة', bilingual: false,
            issuerLine1: '', issuerLine2: '', issuerLine3: '',
            addressees: [{ prefix: 'الأخ /', name: 'المدير العام للمحافظة', suffix: 'المحترم' }],
            involvedPersonnel: [{ militaryId: person?.military_number || '', rank: person?.rank_name || '', name: person?.full_name || '', nationalId: '', status: fType, notes: '' }],
            subject: `بخصوص طلب إثبات حالة (${fType}) — ${person?.full_name || ''}`,
            body: `<p>نحيط سيادتكم علماً بأنه تم اعتماد طلب إثبات حالة (${fType}) للمنتسب المذكور أعلاه.</p><p>رقم المعاملة: <strong>${txNum2}</strong></p>`,
            conclusion: '<p>والله الموفق ،،،</p>',
            signatures: [
              { title: 'رئيس قسم الخدمات', rank: '', name: '', showSeal: false },
              { title: 'مدير إدارة القوى البشرية', rank: '', name: '', showSeal: true },
            ],
            signatureSettings: { showLabels: true, showFrame: true },
            visibleColumns: { militaryId: true, rank: true, nationalId: false, status: true, workplace: false, serviceLocation: false, jobTitle: false, position: false, qualification: false, joinDate: false, commencementDate: false, phone: false, clarification: false, notes: true },
            typography: {
              addressee: { family: 'Cairo', size: 1.1, weight: 'font-bold', underline: true },
              greeting: { family: 'Cairo', size: 1.0, weight: 'font-bold', underline: true },
              subject: { family: 'Cairo', size: 1.15, weight: 'font-black', underline: true },
              body: { family: 'Cairo', size: 1.0, weight: 'font-normal', underline: false },
              conclusionSeparator: { family: 'Cairo', size: 1.1, weight: 'font-bold', underline: true },
              conclusionBody: { family: 'Cairo', size: 1.0, weight: 'font-normal', underline: false },
              signatures: { family: 'Cairo', size: 0.95, weight: 'font-bold', underline: false },
            },
          }
                    const tplStr = localStorage.getItem('memo_template_CORRECTION');
          if (tplStr) {
            try {
              const tpl = JSON.parse(tplStr);
              draft2 = { ...draft2, ...tpl, referenceNo: draft2.referenceNo, docDate: draft2.docDate, involvedPersonnel: [] };
            } catch(e) {}
          }
          localStorage.setItem('official_memo_draft', JSON.stringify(draft2))
          window.open('/admin/documents/memo-preview', '_blank')
          router.push(category === 'form' ? '/services/external-requests' : '/services/internal-requests')
        }
      } else {
        router.push(category === 'form' ? '/services/external-requests' : '/services/internal-requests')
      }
    })
  } else {
    Swal.fire({
      icon: 'error',
      title: 'فشل العملية',
      html: `حدث خطأ أثناء محاولة تقديم الطلبات:<br><div class="text-xs text-right mt-2 text-red-600 bg-red-50 p-2 rounded">${errorMessages.join('<br>')}</div>`
    })
  }
}
</script>
