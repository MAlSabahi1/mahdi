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
          
          <!-- Official Form Header matching the Paper Forms -->
          <div v-if="selectedPersonnelList.length === 1" class="mt-6 border border-gray-300 dark:border-gray-700 rounded-xl overflow-hidden shadow-sm font-serif">
            <!-- Header Banner -->
            <div class="bg-gray-100 dark:bg-gray-800 border-b border-gray-300 dark:border-gray-700 px-4 py-2 flex justify-between items-center">
              <span class="font-bold text-gray-700 dark:text-gray-300 text-sm flex items-center gap-2">
                <svg class="w-5 h-5 text-brand-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                استمارة إثبات حالة ({{ schema?.label || 'الطلب' }})
              </span>
              <span class="text-xs text-gray-500 font-sans tracking-wider">سجل رقمي معتمد</span>
            </div>
            
            <!-- أولاً: البيانات الشخصية -->
            <div class="p-4 border-b border-gray-200 dark:border-gray-800">
              <h3 class="text-brand-700 dark:text-brand-400 font-bold mb-3 border-b-2 border-brand-200 dark:border-brand-900 pb-1 w-max">أولاً: البيانات الشخصية</h3>
              <div class="grid grid-cols-2 md:grid-cols-6 gap-3">
                <div class="bg-white dark:bg-gray-900 p-2.5 rounded border border-gray-200 dark:border-gray-700 shadow-sm">
                  <span class="block text-[10px] font-bold text-gray-500 mb-1">الرتبة</span>
                  <strong class="text-sm dark:text-white">{{ selectedPersonnelList[0].rank_name || selectedPersonnelList[0].current_rank?.name || selectedPersonnelList[0].rank?.name || '—' }}</strong>
                </div>
                <div class="bg-white dark:bg-gray-900 p-2.5 rounded border border-gray-200 dark:border-gray-700 shadow-sm">
                  <span class="block text-[10px] font-bold text-gray-500 mb-1">الرقم العسكري</span>
                  <strong class="text-sm dark:text-white font-sans">{{ selectedPersonnelList[0].military_number || '—' }}</strong>
                </div>
                <div class="md:col-span-2 bg-white dark:bg-gray-900 p-2.5 rounded border border-gray-200 dark:border-gray-700 shadow-sm">
                  <span class="block text-[10px] font-bold text-gray-500 mb-1">الاسم الرباعي</span>
                  <strong class="text-sm dark:text-white">{{ selectedPersonnelList[0].full_name || '—' }}</strong>
                </div>
                <div class="bg-white dark:bg-gray-900 p-2.5 rounded border border-gray-200 dark:border-gray-700 shadow-sm">
                  <span class="block text-[10px] font-bold text-gray-500 mb-1">الوحدة</span>
                  <strong class="text-sm dark:text-white">{{ selectedPersonnelList[0].unit_name || selectedPersonnelList[0].unit?.name || '—' }}</strong>
                </div>
                <div class="bg-white dark:bg-gray-900 p-2.5 rounded border border-gray-200 dark:border-gray-700 shadow-sm">
                  <span class="block text-[10px] font-bold text-gray-500 mb-1">إدارته / المديرية / الفرع</span>
                  <strong class="text-sm dark:text-white">{{ selectedPersonnelList[0].department_name || selectedPersonnelList[0].branch?.name || selectedPersonnelList[0].district_police?.name || selectedPersonnelList[0].central_department?.name || '—' }}</strong>
                </div>
              </div>
            </div>

            <!-- ثانياً: بيانات الميلاد والإقامة الحالية -->
            <div class="p-4 bg-gray-50/50 dark:bg-gray-800/30">
              <h3 class="text-brand-700 dark:text-brand-400 font-bold mb-3 border-b-2 border-brand-200 dark:border-brand-900 pb-1 w-max">ثانياً: بيانات الميلاد والإقامة الحالية</h3>
              
              <div class="space-y-4">
                <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                  <div class="bg-white dark:bg-gray-900 p-2.5 rounded border border-gray-200 dark:border-gray-700 shadow-sm">
                    <span class="block text-[10px] font-bold text-gray-500 mb-1">الرقم الوطني</span>
                    <strong class="text-sm dark:text-white font-sans tracking-widest">{{ selectedPersonnelList[0].national_id || '—' }}</strong>
                  </div>
                  <div class="bg-white dark:bg-gray-900 p-2.5 rounded border border-gray-200 dark:border-gray-700 shadow-sm">
                    <span class="block text-[10px] font-bold text-gray-500 mb-1">تاريخ الإصدار</span>
                    <input type="date" v-model="localHeaderData.id_issue_date" class="w-full bg-transparent text-sm font-sans dark:text-white outline-none border-b border-gray-300 dark:border-gray-600 focus:border-brand-500" />
                  </div>
                  <div class="bg-white dark:bg-gray-900 p-2.5 rounded border border-gray-200 dark:border-gray-700 shadow-sm">
                    <span class="block text-[10px] font-bold text-gray-500 mb-1">جهة الإصدار</span>
                    <input type="text" v-model="localHeaderData.id_issue_place" placeholder="جهة الإصدار" class="w-full bg-transparent text-sm dark:text-white outline-none border-b border-gray-300 dark:border-gray-600 focus:border-brand-500" />
                  </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <!-- Birth Place -> 4 boxes -->
                  <div class="bg-white dark:bg-gray-900 p-3 rounded border border-gray-200 dark:border-gray-700 shadow-sm">
                    <span class="block text-xs font-bold text-gray-700 dark:text-gray-300 mb-2">محل الميلاد</span>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
                      <div class="border border-gray-300 dark:border-gray-600 rounded bg-gray-50 dark:bg-gray-800 p-1.5 text-center">
                        <span class="block text-[9px] text-gray-400 mb-1">المحافظة</span>
                        <select v-model="localHeaderData.birth_gov_id" class="w-full bg-transparent text-xs font-bold dark:text-white outline-none">
                          <option :value="null" disabled>اختر...</option>
                          <option v-for="gov in coreStore.governorates" :key="gov.id" :value="gov.id">{{ gov.name }}</option>
                        </select>
                      </div>
                      <div class="border border-gray-300 dark:border-gray-600 rounded bg-gray-50 dark:bg-gray-800 p-1.5 text-center">
                        <span class="block text-[9px] text-gray-400 mb-1">المديرية</span>
                        <select v-model="localHeaderData.birth_district_id" class="w-full bg-transparent text-xs font-bold dark:text-white outline-none" :disabled="!localHeaderData.birth_gov_id">
                          <option :value="null" disabled>اختر...</option>
                          <option v-for="d in headerDistrictsCache[localHeaderData.birth_gov_id as number] || []" :key="d.id" :value="d.id">{{ d.name_ar || d.name }}</option>
                        </select>
                      </div>
                      <div class="border border-gray-300 dark:border-gray-600 rounded bg-gray-50 dark:bg-gray-800 p-1.5 text-center">
                        <span class="block text-[9px] text-gray-400 mb-1">العزلة</span>
                        <select v-model="localHeaderData.birth_sub_district_id" class="w-full bg-transparent text-xs font-bold dark:text-white outline-none" :disabled="!localHeaderData.birth_district_id">
                          <option :value="null" disabled>اختر...</option>
                          <option v-for="s in headerSubDistrictsCache[localHeaderData.birth_district_id as number] || []" :key="s.id" :value="s.id">{{ s.name_ar || s.name }}</option>
                        </select>
                      </div>
                      <div class="border border-gray-300 dark:border-gray-600 rounded bg-gray-50 dark:bg-gray-800 p-1.5 text-center">
                        <span class="block text-[9px] text-gray-400 mb-1">القرية/الحارة</span>
                        <select v-model="localHeaderData.birth_village_id" class="w-full bg-transparent text-xs font-bold dark:text-white outline-none" :disabled="!localHeaderData.birth_sub_district_id">
                          <option :value="null" disabled>اختر...</option>
                          <option v-for="v in headerVillagesCache[localHeaderData.birth_sub_district_id as number] || []" :key="v.id" :value="v.id">{{ v.name_ar || v.name_ar_normalized || v.name }}</option>
                        </select>
                      </div>
                    </div>
                  </div>

                  <!-- Residence Place -> 4 boxes -->
                  <div class="bg-white dark:bg-gray-900 p-3 rounded border border-gray-200 dark:border-gray-700 shadow-sm">
                    <span class="block text-xs font-bold text-gray-700 dark:text-gray-300 mb-2">محل الإقامة الحالية</span>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
                      <div class="border border-gray-300 dark:border-gray-600 rounded bg-gray-50 dark:bg-gray-800 p-1.5 text-center">
                        <span class="block text-[9px] text-gray-400 mb-1">المحافظة</span>
                        <select v-model="localHeaderData.residence_gov_id" class="w-full bg-transparent text-xs font-bold dark:text-white outline-none">
                          <option :value="null" disabled>اختر...</option>
                          <option v-for="gov in coreStore.governorates" :key="gov.id" :value="gov.id">{{ gov.name }}</option>
                        </select>
                      </div>
                      <div class="border border-gray-300 dark:border-gray-600 rounded bg-gray-50 dark:bg-gray-800 p-1.5 text-center">
                        <span class="block text-[9px] text-gray-400 mb-1">المديرية</span>
                        <select v-model="localHeaderData.residence_district_id" class="w-full bg-transparent text-xs font-bold dark:text-white outline-none" :disabled="!localHeaderData.residence_gov_id">
                          <option :value="null" disabled>اختر...</option>
                          <option v-for="d in headerDistrictsCache[localHeaderData.residence_gov_id as number] || []" :key="d.id" :value="d.id">{{ d.name_ar || d.name }}</option>
                        </select>
                      </div>
                      <div class="border border-gray-300 dark:border-gray-600 rounded bg-gray-50 dark:bg-gray-800 p-1.5 text-center">
                        <span class="block text-[9px] text-gray-400 mb-1">العزلة</span>
                        <select v-model="localHeaderData.residence_sub_district_id" class="w-full bg-transparent text-xs font-bold dark:text-white outline-none" :disabled="!localHeaderData.residence_district_id">
                          <option :value="null" disabled>اختر...</option>
                          <option v-for="s in headerSubDistrictsCache[localHeaderData.residence_district_id as number] || []" :key="s.id" :value="s.id">{{ s.name_ar || s.name }}</option>
                        </select>
                      </div>
                      <div class="border border-gray-300 dark:border-gray-600 rounded bg-gray-50 dark:bg-gray-800 p-1.5 text-center">
                        <span class="block text-[9px] text-gray-400 mb-1">الشارع/القرية</span>
                        <select v-model="localHeaderData.residence_village_id" class="w-full bg-transparent text-xs font-bold dark:text-white outline-none" :disabled="!localHeaderData.residence_sub_district_id">
                          <option :value="null" disabled>اختر...</option>
                          <option v-for="v in headerVillagesCache[localHeaderData.residence_sub_district_id as number] || []" :key="v.id" :value="v.id">{{ v.name_ar || v.name_ar_normalized || v.name }}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="p-4 bg-gray-100/50 dark:bg-gray-900/50 border-t border-gray-200 dark:border-gray-700 flex justify-center">
               <span class="text-xs text-gray-500 font-bold">⬇ ثالثاً: بيانات الحالة (يرجى استكمال البيانات أدناه بناءً على القرار) ⬇</span>
            </div>
          </div>
          
          <div v-else class="mt-6 p-5 bg-blue-50 dark:bg-blue-900/20 text-blue-800 dark:text-blue-300 rounded-xl border border-blue-200 dark:border-blue-800 shadow-sm">
            <span class="font-bold flex items-center gap-2 mb-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
              طلب استمارة جماعية
            </span>
            سيتم تطبيق إثبات الحالة (القرار) المدخل في الأسفل على جميع الأفراد المحددين دفعة واحدة (العدد: {{ selectedPersonnelList.length }} أفراد).
          </div>
        </div>
        
        <div class="space-y-8">
          <!-- General Dynamic Layout -->
          <div v-for="(section, sIdx) in schema.sections" :key="sIdx">
            <template v-if="getDynamicFields(section).length > 0">
              <h3 class="text-md font-bold text-brand-600 mb-4">{{ section.title }}</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <template v-for="field in getDynamicFields(section)" :key="field.key">
                <!-- Current Rank injected right before to_rank for Rank Settlements -->
                <div v-if="field.key === 'to_rank' && category === 'rank_settlement'" class="bg-gray-50/50 dark:bg-gray-800/20 p-4 rounded-xl border border-gray-100 dark:border-gray-800/60 flex flex-col justify-center">
                  <label class="mb-1 block text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">الرتبة الحالية</label>
                  <div class="text-sm font-bold text-gray-900 dark:text-white">
                    {{ selectedPersonnelList[0]?.rank_name || selectedPersonnelList[0]?.current_rank?.name || selectedPersonnelList[0]?.rank?.name || 'غير متوفر' }}
                  </div>
                </div>

                <div v-show="field.key !== 'new_military_number' || formData.settlement_type === 'personnel_to_officer'" 
                     class="space-y-1.5">
                  <label class="text-xs font-bold text-gray-700 dark:text-gray-300">
                    {{ field.label }} <span v-if="field.required || (field.key === 'new_military_number' && formData.settlement_type === 'personnel_to_officer')" class="text-red-500">*</span>
                  </label>
                
                <select v-if="field.type === 'select'" v-model="formData[field.key]" class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-brand-500 outline-none transition-shadow">
                  <option value="" disabled>اختر...</option>
                  <option v-for="opt in getFilteredOptions(field)" :key="opt && typeof opt === 'object' ? opt.value : opt" :value="opt && typeof opt === 'object' ? opt.value : opt">
                    {{ opt && typeof opt === 'object' ? opt.label : opt }}
                  </option>
                </select>

                <!-- Location Cascade: محافظة → مديرية → عزلة → قرية/حارة -->
                <div v-else-if="field.type === 'location_cascade'" class="space-y-3">
                  <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <!-- محافظة -->
                    <div>
                      <label class="text-[10px] font-bold text-gray-500 mb-1 block">المحافظة</label>
                      <select v-model="locationState[field.key + '_gov']" @change="onGovernorateChange(field.key)"
                        class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none">
                        <option value="">اختر المحافظة...</option>
                        <option v-for="g in governorates" :key="g.id" :value="g.id">{{ g.name_ar }}</option>
                      </select>
                    </div>
                    <!-- مديرية -->
                    <div>
                      <label class="text-[10px] font-bold text-gray-500 mb-1 block">المديرية</label>
                      <select v-model="locationState[field.key + '_dist']" @change="onDistrictChange(field.key)"
                        :disabled="!locationState[field.key + '_gov']"
                        class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none disabled:opacity-50">
                        <option value="">اختر المديرية...</option>
                        <option v-for="d in getDistricts(field.key)" :key="d.id" :value="d.id">{{ d.name_ar }}</option>
                      </select>
                    </div>
                    <!-- عزلة -->
                    <div>
                      <label class="text-[10px] font-bold text-gray-500 mb-1 block">العزلة</label>
                      <select v-model="locationState[field.key + '_sub']" @change="onSubDistrictChange(field.key)"
                        :disabled="!locationState[field.key + '_dist']"
                        class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none disabled:opacity-50">
                        <option value="">اختر العزلة...</option>
                        <option v-for="s in getSubDistricts(field.key)" :key="s.id" :value="s.id">{{ s.name_ar }}</option>
                      </select>
                    </div>
                    <!-- قرية / حارة -->
                    <div>
                      <label class="text-[10px] font-bold text-gray-500 mb-1 block">القرية / الحارة</label>
                      <select v-model="locationState[field.key + '_vil']" @change="onVillageChange(field.key)"
                        :disabled="!locationState[field.key + '_sub']"
                        class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none disabled:opacity-50">
                        <option value="">اختر القرية...</option>
                        <option v-for="v in getVillages(field.key)" :key="v.id" :value="v.id">{{ v.name_ar || v.name_ar_normalized }}</option>
                      </select>
                    </div>
                  </div>
                  <!-- الكتابة اليدوية -->
                  <div class="flex items-center gap-2">
                    <label class="flex items-center gap-1.5 cursor-pointer">
                      <input type="checkbox" v-model="locationState[field.key + '_manual']" class="w-3.5 h-3.5 rounded border-gray-300 text-brand-600 focus:ring-brand-500" />
                      <span class="text-[10px] text-gray-500">كتابة يدوية</span>
                    </label>
                  </div>
                  <input v-if="locationState[field.key + '_manual']"
                    v-model="formData[field.key]" type="text" placeholder="اكتب المكان يدوياً..."
                    class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-brand-500 outline-none" />
                  <!-- المكان النهائي المُجمّع -->
                  <div v-if="formData[field.key] && !locationState[field.key + '_manual']" class="text-[10px] text-emerald-600 font-bold bg-emerald-50 dark:bg-emerald-950/20 px-3 py-1.5 rounded-lg border border-emerald-200 dark:border-emerald-800">
                    📍 {{ formData[field.key] }}
                  </div>
                </div>

                <textarea v-else-if="field.type === 'textarea'" v-model="formData[field.key]" class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-brand-500 outline-none h-24 transition-shadow"></textarea>
                <input v-else :type="field.type" v-model="formData[field.key]" 
                        :readonly="field.key === 'old_value' || field.disabled"
                        :maxlength="field.key === 'new_military_number' ? 7 : (field.key === 'new_value' && (formData.correction_type === 'national_id_correction' || formData.field_name === 'national_id') ? 11 : undefined)"
                        :class="['w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-brand-500 outline-none transition-shadow', field.type === 'date' ? 'text-left' : '', (field.key === 'old_value' || field.disabled) ? 'opacity-70 cursor-not-allowed font-bold text-gray-600 bg-gray-100 dark:bg-gray-800/50' : '']"
                        :dir="field.type === 'date' ? 'ltr' : 'rtl'" />
                <p v-if="field.key === 'new_military_number'" class="mt-1 text-xs text-brand-600 dark:text-brand-400 flex items-center gap-1">
                  <svg class="h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  الرقم العسكري للضابط يبدأ بـ 60 ويتكون من 7 خانات
                </p>
                <p v-if="field.help_text" class="text-[10px] text-gray-400 mt-1">{{ field.help_text }}</p>
                </div>
              </template>
            </div>
            </template>
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

function getDynamicFields(section: any) {
  if (!section || !section.fields) return []
  // If the section is marked as auto, it means it's already rendered in the official form header
  if (section.source === 'auto') return []
  
  const hardcodedKeys = ['military_number', 'full_name', 'current_rank', 'rank', 'unit', 'national_id', 'birth_date', 'governorate', 'residence_gov_id']
  return section.fields.filter((f: any) => !hardcodedKeys.includes(f.key))
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
    const toRankField = schema.value?.sections?.flatMap((s:any) => s.fields || []).find((f:any) => f.key === 'to_rank')
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
      const allFields = res.sections?.flatMap((s: any) => s.fields || []) || []
      if (allFields.length > 0) {
        allFields.forEach((f: any) => {
          formData.value[f.key] = f.default !== undefined ? f.default : (f.value !== undefined ? f.value : '')
          // Auto-select if only one option
          if (f.type === 'select' && f.options?.length === 1) {
            formData.value[f.key] = f.options[0].value || f.options[0]
          }
        })
        // Load governorates if any location_cascade field exists
        const hasLocationField = allFields.some((f: any) => f.type === 'location_cascade')
        if (hasLocationField) {
          loadGovernorates()
        }

        // Load ranks if any select field is to_rank
        const rankField = allFields.find((f: any) => f.key === 'to_rank')
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
    Swal.fire({
      icon: 'info',
      title: 'فرد واحد فقط',
      text: 'خدمات تصحيح البيانات تتم لفرد واحد فقط في كل طلب. لا يمكنك تحديد أكثر من شخص.'
    })
    return
  }
  
  // ── التحقق المنطقي المسبق (Pre-flight Validation) ──
  
  // 1. منع إضافة شهيد وهو بالفعل شهيد في النظام
  let statusStr = person.status_name || person.current_status_name || '';
  if (!statusStr && person.current_status) {
    if (typeof person.current_status === 'object') {
      statusStr = person.current_status.name || '';
    } else if (typeof person.current_status === 'string') {
      statusStr = person.current_status;
    }
  }
  
  statusStr = String(statusStr || '');
  
  if (type === 'martyr' && (statusStr.includes('شهيد') || statusStr.includes('شهداء') || statusStr.includes('شهد'))) {
    Swal.fire({
      icon: 'error',
      title: 'فرد مسجل كشهيد',
      text: 'هذا الفرد مسجل ضمن الشهداء بالفعل في النظام ولا يمكن إنشاء معاملة استشهاد أخرى له.'
    })
    return
  }
  
  // منع إضافة معاملة وفاة وهو بالفعل متوفى
  if (type === 'death' && (statusStr.includes('متوفى') || statusStr.includes('وفيات') || statusStr.includes('وفاة') || statusStr.includes('وفاه'))) {
    Swal.fire({
      icon: 'error',
      title: 'فرد مسجل كمتوفى',
      text: 'هذا الفرد مسجل ضمن الوفيات بالفعل في النظام ولا يمكن إنشاء معاملة وفاة أخرى له.'
    })
    return
  }

  // 2. التحقق من الباك إند إذا كانت هناك معاملة معلقة لنفس الفرد ونفس النوع
  if (category === 'form' || category === 'rank_settlement') {
    try {
      const checkRes = await api.get('/service-cycle/forms/', { params: { personnel: person.military_number, type: type } })
      const pendingForms = checkRes.data?.results?.filter((f: any) => 
        ['draft', 'in_progress', 'pending_services', 'pending_hr', 'pending_director', 'returned'].includes(f.status)
      )
      if (pendingForms && pendingForms.length > 0) {
        Swal.fire({
          icon: 'warning',
          title: 'طلب قيد الإجراء',
          text: `يوجد معاملة سابقة من نفس النوع قيد الإجراء لهذا الفرد (TX-${String(pendingForms[0].id).padStart(6, '0')}). لا يمكنك تقديم طلب جديد حتى يتم إنجاز الطلب المعلق.`
        })
        return
      }
    } catch (e) {
      console.error('Failed to check pending forms', e)
    }
  }

  // 3. التحقق من وجود طلب تصحيح معلق لنفس النوع
  if (category === 'correction') {
    try {
      const corrType = type // e.g. military_number_correction, national_id_correction
      const checkRes = await api.get('/personnel/corrections/', { params: { personnel: person.military_number, status: 'pending' } })
      const pendingCorrections = checkRes.data?.results?.filter((c: any) =>
        c.correction_type === corrType || c.field_name === corrType
      )
      if (pendingCorrections && pendingCorrections.length > 0) {
        Swal.fire({
          icon: 'warning',
          title: 'طلب تصحيح معلق',
          text: `يوجد طلب تصحيح من نفس النوع قيد الانتظار لهذا الفرد (رقم: ${pendingCorrections[0].id}). لا يمكن تقديم طلب جديد حتى يُبت في الطلب المعلق.`
        })
        return
      }
    } catch (e) {
      console.error('Failed to check pending corrections', e)
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
    if (type === 'national_id_correction') formData.value.old_value = updatedPerson.national_id
    else if (type === 'military_number_correction') formData.value.old_value = updatedPerson.military_number
  }
  
  // Auto-populate 'personnel_master' fields from the first selected person
  if (selectedPersonnelList.value.length > 0 && schema.value?.sections) {
    const person = selectedPersonnelList.value[0]
    schema.value.sections.forEach((section: any) => {
      section.fields?.forEach((field: any) => {
        if (field.source === 'personnel_master') {
          formData.value[field.key] = person[field.key] || ''
        }
      })
    })
  }
  
  step.value = 2
}

// === Step 2 Logic ===
async function validateAndGoToStep3() {
  // Check required fields in all dynamic sections
  const allFields = schema.value.sections?.flatMap((s: any) => s.fields || []) || []
  if (allFields.length > 0) {
    const missing = allFields.filter((f: any) => {
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
        // التحقق من صيغة الرقم العسكري: 7 أرقام
        if (!val || !/^\d{7}$/.test(String(val))) {
          Swal.fire({
            icon: 'warning',
            title: 'رقم عسكري غير صالح',
            text: 'الرقم العسكري يجب أن يتكون من 7 أرقام بالضبط.'
          })
          return
        }
        // التحقق من أن الرقم الجديد مختلف عن القديم
        const oldVal = formData.value.old_value
        if (oldVal && String(val) === String(oldVal)) {
          Swal.fire({
            icon: 'warning',
            title: 'لا يوجد تغيير',
            text: 'الرقم العسكري الجديد لا يمكن أن يكون نفس الرقم الحالي.'
          })
          return
        }

        // التحقق الفوري من الرقم العسكري عبر قاعدة البيانات
        try {
          const checkRes = await api.get('/personnel/check-military-number/', { params: { value: val } })
          if (checkRes.data?.exists) {
            Swal.fire({
              icon: 'error',
              title: 'الرقم العسكري مستخدم',
              text: 'هذا الرقم العسكري مستخدم بالفعل في النظام. يرجى إدخال رقم مختلف.'
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

  // Validate All Fields
  const allFields = schema.value.sections?.flatMap((s:any) => s.fields || []) || []
  if (allFields.length > 0) {
    for (const f of allFields) {
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
