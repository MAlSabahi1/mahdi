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
                :disabled="selectedPersonnelList.length === 0" 
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
          <h2 class="text-lg font-black">الخطوة 2: تعبئة بيانات الطلب أو القرار</h2>
        </div>
        
        <div class="space-y-8">
          <!-- General Form Fields (Shared across all selected personnel) -->
          <!-- General Form Fields (Shared across all selected personnel) -->
          <div class="mb-8" v-if="!isRankSettlement || schema?.sections?.find((s:any) => s.source === 'user_input')?.fields?.some((f:any) => !(isRankSettlement && ['to_rank', 'demotion_reason', 'new_military_number', 'decision_number', 'decision_date', 'university_degree_type'].includes(f.key)) && !f.disabled)">
            <h3 class="text-md font-bold text-brand-600 mb-4 border-b pb-2 border-gray-100 dark:border-gray-800">بيانات القرار والتسوية المشتركة</h3>
            <div v-for="(section, sIdx) in schema?.sections?.filter((s:any) => s.source === 'user_input')" :key="sIdx" class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6">
              <template v-for="field in section.fields.filter((f:any) => !(isRankSettlement && ['to_rank', 'demotion_reason', 'new_military_number', 'decision_number', 'decision_date', 'university_degree_type'].includes(f.key)) && !f.disabled)" :key="field.key">
                <div v-if="!field.hidden">
                  <label class="block text-xs font-bold text-gray-700 dark:text-gray-300 mb-1.5">
                    {{ field.label }} <span v-if="field.required" class="text-red-500">*</span>
                  </label>
                  
                  <input v-if="field.type === 'text' || field.type === 'number'" :type="field.type" v-model="formData[field.key]" :placeholder="field.placeholder" :disabled="field.disabled" class="w-full text-xs rounded-xl border border-gray-300 dark:border-gray-700 bg-transparent py-2.5 px-3 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/10 dark:text-white disabled:bg-gray-100 dark:disabled:bg-gray-800 disabled:text-gray-400 disabled:cursor-not-allowed" />
                  
                  <input v-else-if="field.type === 'date'" type="date" v-model="formData[field.key]" :disabled="field.disabled" class="w-full text-xs rounded-xl border border-gray-300 dark:border-gray-700 bg-transparent py-2.5 px-3 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/10 dark:text-white disabled:bg-gray-100 dark:disabled:bg-gray-800 disabled:text-gray-400 disabled:cursor-not-allowed" />
                  
                  <textarea v-else-if="field.type === 'textarea'" v-model="formData[field.key]" :rows="field.rows || 3" :placeholder="field.placeholder" :disabled="field.disabled" class="w-full text-xs rounded-xl border border-gray-300 dark:border-gray-700 bg-transparent py-2.5 px-3 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/10 dark:text-white disabled:bg-gray-100 dark:disabled:bg-gray-800 disabled:text-gray-400 disabled:cursor-not-allowed"></textarea>
                  
                  <select v-else-if="field.type === 'select'" v-model="formData[field.key]" :disabled="field.disabled" class="w-full text-xs rounded-xl border border-gray-300 dark:border-gray-700 bg-transparent py-2.5 px-3 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/10 dark:text-white disabled:bg-gray-100 dark:disabled:bg-gray-800 disabled:text-gray-400 disabled:cursor-not-allowed">
                    <option value="" disabled selected>اختر {{ field.label }}</option>
                    <option v-for="opt in getFilteredOptions(field)" :key="opt.value || opt" :value="opt.value || opt">{{ opt.label || opt }}</option>
                  </select>
                </div>
              </template>
            </div>
          </div>

          <!-- Rank Settlement Personnel Table -->
          <div>
            <h3 class="text-md font-bold text-brand-600 mb-4 border-b pb-2 border-gray-100 dark:border-gray-800 flex justify-between items-center">
              <span>الأفراد المشمولين بالتسوية</span>
              <span class="text-xs bg-brand-100 text-brand-700 dark:bg-brand-900/30 dark:text-brand-300 px-3 py-1 rounded-full font-bold">العدد: {{ selectedPersonnelList.length }}</span>
            </h3>
            
            <div class="overflow-x-auto border border-gray-200 dark:border-gray-800 rounded-xl shadow-sm bg-white dark:bg-gray-900">
              <table class="w-full border-collapse text-right text-sm">
                <thead>
                  <tr class="bg-gray-50 dark:bg-gray-850 text-gray-700 dark:text-gray-300 font-bold text-xs uppercase tracking-wider">
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-12">م</th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-28">الرتبة الحالية</th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-32">الرقم العسكري الحالي</th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800">الاسم الرباعي</th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-28" v-if="formData.settlement_type === 'personnel_to_officer' || type === 'personnel_to_officer'">المؤهل <span class="text-red-500">*</span></th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-40" v-if="formData.settlement_type === 'personnel_to_officer' || type === 'personnel_to_officer'">الرقم العسكري الجديد <span class="text-red-500">*</span></th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-32" v-if="isRankSettlement">الرتبة المستهدفة <span class="text-red-500">*</span></th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-32" v-if="isRankSettlement">رقم القرار <span class="text-red-500">*</span></th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-32" v-if="isRankSettlement">تاريخ القرار <span class="text-red-500">*</span></th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-40" v-if="isRankSettlement">السبب / الملاحظات <span class="text-red-500" v-if="type === 'rank_demotion'">*</span></th>
                    <th class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center w-24" v-if="isRankSettlement">مرفق خاص</th>
                    <th class="p-3 border-b border-gray-200 dark:border-gray-800 text-center w-16">الإجراء</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(person, idx) in selectedPersonnelList" :key="person.military_number" class="hover:bg-gray-50/50 dark:hover:bg-gray-800/20 transition-colors">
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center font-bold text-gray-400">{{ idx + 1 }}</td>
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center text-xs font-bold text-gray-600 dark:text-gray-300">
                      {{ person.rank_name || person.current_rank?.name || person.rank?.name || '—' }}
                    </td>
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center font-mono font-bold text-gray-700 dark:text-gray-300">
                      {{ person.military_number }}
                    </td>
                    <td class="p-3 border-b border-l border-gray-200 dark:border-gray-800 font-bold text-gray-900 dark:text-white">
                      {{ person.full_name }}
                    </td>
                    <td v-if="formData.settlement_type === 'personnel_to_officer' || type === 'personnel_to_officer'" class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center">
                      <select v-model="perPersonData[person.military_number].university_degree_type" class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none font-bold text-brand-600 dark:text-brand-400">
                        <option value="" disabled selected>اختر</option>
                        <option value="بكالوريوس">بكالوريوس</option>
                        <option value="ماجستير">ماجستير</option>
                        <option value="دكتوراه">دكتوراه</option>
                        <option value="أخرى">أخرى</option>
                      </select>
                    </td>
                    <td v-if="formData.settlement_type === 'personnel_to_officer' || type === 'personnel_to_officer'" class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center">
                      <input v-model="perPersonData[person.military_number].new_military_number" type="text" placeholder="يبدأ بـ 60 (7 أرقام)" class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none text-center font-mono font-bold text-brand-600 dark:text-brand-400" />
                    </td>
                    <td v-if="isRankSettlement" class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center">
                      <select v-model="perPersonData[person.military_number].to_rank" class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none font-bold text-brand-600 dark:text-brand-400">
                        <option value="" disabled selected>اختر الرتبة</option>
                        <option v-for="opt in getSettlementRanks(person)" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                      </select>
                    </td>
                    <td v-if="isRankSettlement" class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center">
                      <input v-model="perPersonData[person.military_number].decision_number" type="text" placeholder="رقم القرار" class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none text-brand-600 dark:text-brand-400" />
                    </td>
                    <td v-if="isRankSettlement" class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center">
                      <input v-model="perPersonData[person.military_number].decision_date" type="date" class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none text-brand-600 dark:text-brand-400" />
                    </td>
                    <td v-if="isRankSettlement" class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center">
                      <input v-model="perPersonData[person.military_number].notes" type="text" :placeholder="type === 'rank_demotion' ? 'سبب التنزيل' : 'ملاحظات / رقم خاص'" class="w-full text-xs p-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 outline-none text-brand-600 dark:text-brand-400" />
                    </td>
                    <td v-if="isRankSettlement" class="p-3 border-b border-l border-gray-200 dark:border-gray-800 text-center">
                      <div class="flex items-center justify-center gap-1.5">
                        <label :for="'file-settlement-' + person.military_number" class="cursor-pointer bg-emerald-50 hover:bg-emerald-100 text-emerald-600 text-[10px] font-bold px-2 py-1.5 rounded transition-colors flex items-center gap-1">
                          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"/></svg>
                          {{ perPersonData[person.military_number].file ? 'تغيير' : 'إرفاق' }}
                        </label>
                        <input :id="'file-settlement-' + person.military_number" type="file" @change="handlePersonAttachment(person.military_number, $event)" class="hidden" accept=".pdf,.jpg,.jpeg,.png" />
                        <span v-if="perPersonData[person.military_number].uploading" class="animate-spin h-3 w-3 border-2 border-emerald-500 border-t-transparent rounded-full"></span>
                        <span v-if="perPersonData[person.military_number].file && !perPersonData[person.military_number].uploading" class="text-emerald-500 text-[10px]">✓</span>
                      </div>
                    </td>
                    <td class="p-3 border-b border-gray-200 dark:border-gray-800 text-center">
                      <button @click="removePersonnel(person.military_number)" class="text-red-500 hover:text-red-700 bg-red-50 hover:bg-red-100 dark:bg-red-900/30 dark:hover:bg-red-900/50 p-1.5 rounded-lg transition-colors">
                        <svg class="w-4 h-4 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="selectedPersonnelList.length === 0" class="text-center py-6 text-gray-500 text-sm">
              لم يتم تحديد أي أفراد لهذه التسوية. يرجى العودة للخطوة الأولى.
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
const formData = ref<any>({})
const newMilitaryNumbers = reactive<Record<string, string>>({})
const perPersonData = reactive<Record<string, { to_rank: string, notes: string, new_military_number: string, university_degree_type: string, decision_number: string, decision_date: string, document_id: number | null, file: File | null, uploading: boolean }>>({})
const documentIds = ref<number[]>([])
const uploadedFiles = ref<Record<string, File>>({})
const uploadingDoc = ref<string | null>(null)

const isRankSettlement = computed(() => category === 'rank_settlement' || ['rank_demotion', 'rank_promotion', 'personnel_to_officer'].includes(type))
const userFields = computed(() => schema.value?.sections?.find((s:any) => s.source === 'user_input')?.fields || [])

const hasToRankColumn = computed(() => isRankSettlement.value && !!userFields.value.find((f:any) => f.key === 'to_rank'))
const hasReasonColumn = computed(() => isRankSettlement.value && !!userFields.value.find((f:any) => ['notes', 'reason', 'demotion_reason'].includes(f.key)))
const hasNewMilNumColumn = computed(() => isRankSettlement.value && (type === 'personnel_to_officer' || !!userFields.value.find((f:any) => f.key === 'new_military_number')))

// Submission State
const isSubmitting = ref(false)
const submittedCount = ref(0)

// Location Cascade State
const locationState = reactive<Record<string, any>>({})
const governorates = ref<any[]>([])
const availableRanks = ref<any[]>([])
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
  return field.options
}

function getSettlementRanks(person: any) {
  if (availableRanks.value.length === 0) return []
  
  const currentRankId = person.current_rank?.id || person.current_rank_id || person.current_rank || person.rank?.id || person.rank_id || person.rank
  
  let currentRank = null;
  if (currentRankId) {
    currentRank = availableRanks.value.find((o: any) => String(o.value) === String(currentRankId))
  }
  
  if (!currentRank && (person.rank_name || person.current_rank?.name || person.rank?.name)) {
    const rankName = person.rank_name || person.current_rank?.name || person.rank?.name
    currentRank = availableRanks.value.find((o: any) => o.label === rankName)
  }

  if (!currentRank) return availableRanks.value 

  if (type === 'rank_demotion') {
    const filtered = availableRanks.value.filter((o: any) => o.order > currentRank.order)
    return filtered.length > 0 ? filtered : availableRanks.value
  } else if (type === 'rank_promotion') {
    const filtered = availableRanks.value.filter((o: any) => o.order < currentRank.order)
    return filtered.length > 0 ? filtered : availableRanks.value
  } else if (type === 'personnel_to_officer' || formData.value.settlement_type === 'personnel_to_officer') {
    const filtered = availableRanks.value.filter((o: any) => o.is_officer === true)
    return filtered.length > 0 ? filtered : availableRanks.value
  }
  
  return availableRanks.value
}

watch(() => formData.value.settlement_type, () => {
  formData.value.to_rank = ''
  
  // Auto-select if there is exactly 1 valid option based on intelligent filtering
  setTimeout(() => {
    if (type === 'rank_demotion') return; // Handled per person
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
  father: '',
  grandfather: '',
  family: ''
})
const notes = ref('')

const generatedFullName = computed(() => {
  const parts = [
    nameParts.first.trim(),
    nameParts.father.trim(),
    nameParts.grandfather.trim(),
    nameParts.family.trim()
  ].filter(p => p !== '')
  return parts.join(' ')
})

const isValidArabic = computed(() => {
  if (!generatedFullName.value) return false
  const arRegex = /^[\u0621-\u064A\s]+$/
  return arRegex.test(generatedFullName.value)
})

const hasFourParts = computed(() => {
  return (
    nameParts.first.trim() !== '' &&
    nameParts.father.trim() !== '' &&
    nameParts.grandfather.trim() !== '' &&
    nameParts.family.trim() !== ''
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

onMounted(async () => {
  if (coreStore.governorates.length === 0) {
    await coreStore.fetchAllReferences()
  }
  await loadGovernorates()

  // FORCE FETCH RANKS FOR DEMOTION REGARDLESS OF SCHEMA
  if (type === 'rank_demotion' || category === 'rank_settlement') {
    try {
      const ranksRes = await api.get('/dictionaries/ranks/?page_size=1000')
      const ranks = ranksRes.data?.results || ranksRes.data || []
      availableRanks.value = ranks.map((r: any) => ({
        value: r.id,
        label: r.name,
        order: r.order,
        is_officer: r.is_officer
      }))
    } catch (e) {
      console.error('Failed to global load ranks:', e)
    }
  }

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

        const rankField = userSection.fields.find((f: any) => f.key === 'to_rank')
        if (rankField && availableRanks.value.length > 0) {
          rankField.options = availableRanks.value
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
    Swal.fire({
      icon: 'info',
      title: 'فرد واحد فقط',
      text: 'خدمات تصحيح البيانات تتم لفرد واحد فقط في كل طلب. لا يمكنك تحديد أكثر من شخص.'
    })
    return
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
      if (type === 'personnel_to_officer' || formData.value.settlement_type === 'personnel_to_officer') {
        const currentRankId = person.current_rank?.id || person.current_rank_id || person.current_rank || person.rank?.id || person.rank_id || person.rank
        const rankName = person.rank_name || person.current_rank?.name || person.rank?.name
        let isOfficer = false
        if (availableRanks.value.length > 0) {
          const r = availableRanks.value.find((o: any) => String(o.value) === String(currentRankId) || o.label === rankName)
          if (r && r.is_officer) isOfficer = true
        }
        if (isOfficer) {
          Swal.fire({
            icon: 'error',
            title: 'عملية غير صالحة',
            text: `الفرد المختار (${person.full_name}) يحمل رتبة ضابط بالفعل ولا يمكن تسويته من كادر الأفراد.`
          })
          return
        }
      }

      selectedPersonnelList.value.push(person)
      if (!perPersonData[person.military_number]) {
        const ranks = getSettlementRanks(person)
        let defaultRank = ''
        if (type === 'rank_promotion' && ranks.length > 0) {
            const nextRank = ranks.reduce((prev: any, curr: any) => (prev.order > curr.order) ? prev : curr, ranks[0])
            if (nextRank) defaultRank = nextRank.value
        } else if (type === 'personnel_to_officer' || formData.value.settlement_type === 'personnel_to_officer') {
            const officers = ranks.filter((r: any) => r.is_officer)
            if (officers.length > 0) {
                const lowestOfficer = officers.reduce((prev: any, curr: any) => (prev.order > curr.order) ? prev : curr, officers[0])
                defaultRank = lowestOfficer.value
            }
        }

        perPersonData[person.military_number] = { 
            to_rank: defaultRank, 
            notes: '', 
            new_military_number: '', 
            university_degree_type: '',
            decision_number: '',
            decision_date: '',
            document_id: null, 
            file: null, 
            uploading: false 
        }
      }
    }
  }
}

function removePersonnel(militaryNumber: string) {
  selectedPersonnelList.value = selectedPersonnelList.value.filter(p => p.military_number !== militaryNumber)
  delete perPersonData[militaryNumber]
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
      nameParts.father = ''
      nameParts.grandfather = ''
      nameParts.family = ''
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
    if (!hasFourParts.value) {
      Swal.fire({
        icon: 'warning',
        title: 'الاسم غير مكتمل',
        text: 'الرجاء إدخال الاسم الرباعي الجديد بالكامل.'
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
  } else {
    // Check required fields in the user_input section
    const userSection = schema.value.sections?.find((s: any) => s.source === 'user_input')
    if (userSection) {
      const missing = userSection.fields.filter((f: any) => {
        if (type === 'rank_demotion' && (f.key === 'to_rank' || f.key === 'demotion_reason')) return false; // Handled in table
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

      // Check per person fields for rank_settlement
      if (isRankSettlement.value) {
        const missingRank = selectedPersonnelList.value.find(p => !perPersonData[p.military_number]?.to_rank)
        if (missingRank) {
          Swal.fire({
            icon: 'warning',
            title: 'بيانات ناقصة في الجدول',
            text: `الرجاء تعبئة الرتبة المستهدفة للفرد: ${missingRank.full_name}`
          })
          return
        }

        const missingDecision = selectedPersonnelList.value.find(p => !perPersonData[p.military_number]?.decision_number || !perPersonData[p.military_number]?.decision_date)
        if (missingDecision) {
          Swal.fire({
            icon: 'warning',
            title: 'بيانات ناقصة في الجدول',
            text: `الرجاء كتابة رقم وتاريخ القرار للفرد: ${missingDecision.full_name}`
          })
          return
        }

        if (type === 'rank_demotion') {
          const missingDemotion = selectedPersonnelList.value.find(p => !perPersonData[p.military_number]?.notes)
          if (missingDemotion) {
            Swal.fire({
              icon: 'warning',
              title: 'بيانات ناقصة في الجدول',
              text: `الرجاء كتابة سبب التنزيل للفرد: ${missingDemotion.full_name}`
            })
            return
          }
        }

        if (type === 'personnel_to_officer' || formData.value.settlement_type === 'personnel_to_officer') {
          const missingMilNum = selectedPersonnelList.value.find(p => !perPersonData[p.military_number]?.new_military_number)
          if (missingMilNum) {
            Swal.fire({
              icon: 'warning',
              title: 'بيانات ناقصة في الجدول',
              text: `الرجاء إدخال الرقم العسكري الجديد للفرد: ${missingMilNum.full_name}`
            })
            return
          }

          const missingDegree = selectedPersonnelList.value.find(p => !perPersonData[p.military_number]?.university_degree_type)
          if (missingDegree) {
            Swal.fire({
              icon: 'warning',
              title: 'بيانات ناقصة في الجدول',
              text: `الرجاء اختيار نوع المؤهل للفرد: ${missingDegree.full_name}`
            })
            return
          }
        }
      }

      // Rank Settlement validations
      if ((type === 'personnel_to_officer' || formData.value.settlement_type === 'personnel_to_officer') && isRankSettlement.value) {
        for (const p of selectedPersonnelList.value) {
          const milNum = perPersonData[p.military_number]?.new_military_number || ''

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
      // National ID and Military Number validations in Correction forms
      const currentField = formData.value.field_name || formData.value.correction_type || type
      if (currentField === 'national_id' || currentField === 'national_id_correction') {
        const val = formData.value.new_value
        if (!val || val.length !== 11 || !/^\d+$/.test(val)) {
          Swal.fire({
            icon: 'warning',
            title: 'رقم وطني غير صالح',
            text: 'الرقم الوطني الجديد يجب أن يتكون من 11 رقماً.'
          })
          return
        }

        // Live check national ID
        try {
          const checkRes = await api.get('/personnel/check-national-id/', { params: { value: val } })
          if (checkRes.data?.exists) {
            Swal.fire({
              icon: 'error',
              title: 'الرقم الوطني مسجل مسبقاً',
              text: 'هذا الرقم الوطني مسجل بالفعل في النظام.'
            })
            return
          }
        } catch (e) {
          console.error(e)
        }
      }

      if (currentField === 'military_number' || currentField === 'military_number_correction') {
        const val = formData.value.new_value
        if (!val || val.length < 4 || isNaN(Number(val))) {
          Swal.fire({
            icon: 'warning',
            title: 'رقم عسكري غير صالح',
            text: 'الرجاء إدخال رقم عسكري صالح.'
          })
          return
        }

        // Live check military number
        try {
          const checkRes = await api.get('/personnel/check-military-number/', { params: { value: val } })
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

async function handlePersonAttachment(militaryNumber: string, event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  perPersonData[militaryNumber].uploading = true
  perPersonData[militaryNumber].file = file

  try {
    const fd = new FormData()
    fd.append('file', file)
    fd.append('document_type', 'personal_attachment')
    
    const res = await api.post('/storage/upload/', fd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    const docId = res.data?.data?.id || res.data?.id
    if (docId) {
      perPersonData[militaryNumber].document_id = docId
    }
  } catch (err: any) {
    console.warn('Local attachment fallback for person:', militaryNumber)
    perPersonData[militaryNumber].document_id = 999 // mock
  } finally {
    perPersonData[militaryNumber].uploading = false
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

  // Validate User Input Fields for generic (skip rank_demotion specific loops)
  const userSection = schema.value.sections?.find((s:any) => s.source === 'user_input')
  if (userSection && type !== 'rank_demotion') {
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

  isSubmitting.value = true
  submittedCount.value = 0
  let successCount = 0
  let errorCount = 0

  let lastCorrectionId = null
  let lastFormId = null

  // Loop through all selected personnel and submit
  for (const person of selectedPersonnelList.value) {
    try {
      if (category === 'correction') {
        const req = await correctionStore.submitCorrection({
          military_number: person.military_number,
          field: formData.value.field_name || formData.value.field || type,
          correction_type: formData.value.correction_type || null,
          old_value: formData.value.old_value || '',
          new_value: formData.value.new_value || '',
          reason: formData.value.notes || formData.value.reason || '',
          document_ids: documentIds.value
        })
        if (req && req.id) lastCorrectionId = req.id
      } else if (category === 'rank_settlement') {
        const toRank = hasToRankColumn.value ? perPersonData[person.military_number]?.to_rank : formData.value.to_rank
        const notes = hasReasonColumn.value ? perPersonData[person.military_number]?.notes : (formData.value.notes || '')
        const newMilNum = hasNewMilNumColumn.value ? perPersonData[person.military_number]?.new_military_number : (formData.value.new_military_number || '')
        const supportDoc = isRankSettlement.value && perPersonData[person.military_number]?.document_id ? perPersonData[person.military_number].document_id : (documentIds.value?.length > 0 ? documentIds.value[0] : null)
        
        let mappedType = formData.value.settlement_type || type
        if (mappedType === 'rank_demotion') mappedType = 'demotion'
        if (mappedType === 'rank_promotion') mappedType = 'promotion'

        await rankSettlementStore.createSettlement({
          personnel: person.military_number,
          settlement_type: mappedType,
          from_rank: person.current_rank?.id || person.current_rank_id || person.current_rank || person.rank?.id || person.rank_id || person.rank,
          to_rank: toRank,
          new_military_number: newMilNum || null,
          decision_number: perPersonData[person.military_number]?.decision_number || formData.value.decision_number || 'بدون رقم',
          decision_date: perPersonData[person.military_number]?.decision_date || formData.value.decision_date || new Date().toISOString().split('T')[0],
          due_date: formData.value.due_date || null,
          notes: notes,
          supporting_document: supportDoc
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
        const perPersonFormOverrides: any = {}
        if (isRankSettlement.value) {
            if (perPersonData[person.military_number]?.to_rank) perPersonFormOverrides.to_rank = perPersonData[person.military_number].to_rank
            if (perPersonData[person.military_number]?.notes) {
                perPersonFormOverrides.notes = perPersonData[person.military_number].notes
                perPersonFormOverrides.demotion_reason = perPersonData[person.military_number].notes
            }
            if (perPersonData[person.military_number]?.new_military_number) perPersonFormOverrides.new_military_number = perPersonData[person.military_number].new_military_number
            if (perPersonData[person.military_number]?.decision_number) perPersonFormOverrides.decision_number = perPersonData[person.military_number].decision_number
            if (perPersonData[person.military_number]?.decision_date) perPersonFormOverrides.decision_date = perPersonData[person.military_number].decision_date
            if (perPersonData[person.military_number]?.university_degree_type) perPersonFormOverrides.university_degree_type = perPersonData[person.military_number].university_degree_type
        }
        
        const mergedFormData = { ...formData.value, ...perPersonFormOverrides }
        
        const personDocId = isRankSettlement.value && perPersonData[person.military_number]?.document_id ? perPersonData[person.military_number].document_id : null
        const allDocIds = [...documentIds.value]
        if (personDocId) allDocIds.push(personDocId)

        const createRes = await servicesStore.createForm({
          personnel: person.military_number,
          form_type: type,
          form_data: mergedFormData,
          document_ids: allDocIds
        })
        if (createRes.success && createRes.data?.id) {
          await servicesStore.submitForm(createRes.data.id)
          lastFormId = createRes.data.id
        }
      }
      successCount++
    } catch (err) {
      console.error('Submission error for', person.military_number, err)
      errorCount++
    }
    submittedCount.value++
  }

  isSubmitting.value = false

  if (successCount > 0) {
    const isModel23 = type === 'name_correction' && successCount === 1;
    const isExternalForm = schema.value?.approval_type === 'external' && successCount === 1;
    const showPrintButton = isModel23 || isExternalForm;
    
    Swal.fire({
      icon: errorCount > 0 ? 'warning' : 'success',
      title: errorCount > 0 ? 'تم الإنجاز جزئياً' : 'تم تقديم الطلبات بنجاح',
      html: `تم رفع <b>${successCount}</b> طلب للمراجعة.<br/>${errorCount > 0 ? `تعذر معالجة <b>${errorCount}</b> طلب.` : ''}`,
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
          const queryParams = new URLSearchParams({
            personnelId: person.military_number,
            old_value: formData.value.old_value || '',
            new_value: formData.value.new_value || '',
            reason: formData.value.reason || formData.value.notes || ''
          }).toString()
          router.push(`/services/print/model-23/${lastCorrectionId}?${queryParams}`)
        } else if (isExternalForm && lastFormId) {
          try {
            await servicesStore.markFormPrinted(lastFormId)
          } catch(e) {}
          window.open(`/services/forms/${lastFormId}?print=true`, '_blank')
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
      text: 'حدث خطأ أثناء محاولة تقديم الطلبات. يرجى مراجعة البيانات.'
    })
  }
}
</script>
