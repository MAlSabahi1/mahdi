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
            <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900 shadow-sm relative overflow-visible">
              <div class="absolute top-0 right-0 w-2 h-full bg-brand-500 rounded-r-2xl"></div>
              <h3 class="mb-5 text-lg font-bold text-gray-900 dark:text-white border-b border-gray-100 pb-3 dark:border-gray-800">أولاً: البيانات الشخصية</h3>
              
              <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الرتبة</label>
                  <input type="text" :value="selectedPersonnelList[0].rank_name || selectedPersonnelList[0].current_rank?.name || selectedPersonnelList[0].rank?.name || '—'" disabled class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:outline-none dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300" />
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الرقم العسكري</label>
                  <input type="text" :value="selectedPersonnelList[0].military_number || '—'" disabled class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs font-sans focus:outline-none dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300" />
                </div>
                <div class="md:col-span-2">
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الاسم الرباعي</label>
                  <input type="text" :value="selectedPersonnelList[0].full_name || '—'" disabled class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:outline-none dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300" />
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الوحدة</label>
                  <input type="text" :value="selectedPersonnelList[0].security_admin_name || selectedPersonnelList[0].unit_name || '—'" disabled class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:outline-none dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300" />
                </div>
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الإدارة / الفرع</label>
                  <input type="text" :value="selectedPersonnelList[0].central_department_name || selectedPersonnelList[0].branch_name || selectedPersonnelList[0].district_police_name || selectedPersonnelList[0].division_name || '—'" disabled class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:outline-none dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300" />
                </div>
              </div>
            </div>

            <!-- ثانياً: بيانات الميلاد والإقامة الحالية -->
            <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900 shadow-sm relative overflow-visible mt-6">
              <div class="absolute top-0 right-0 w-2 h-full bg-indigo-500 rounded-r-2xl"></div>
              <h3 class="mb-5 text-lg font-bold text-gray-900 dark:text-white border-b border-gray-100 pb-3 dark:border-gray-800">ثانياً: بيانات الميلاد والإقامة الحالية</h3>
              
              <div v-if="!isHeaderDataComplete" class="mb-6 bg-yellow-50 dark:bg-yellow-900/30 border-r-4 border-yellow-400 p-4 rounded-lg flex gap-3">
                <svg class="w-6 h-6 text-yellow-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                <div>
                  <h3 class="text-sm font-bold text-yellow-800 dark:text-yellow-200">بيانات الفرد الأساسية غير مكتملة</h3>
                  <p class="text-xs text-yellow-700 dark:text-yellow-400 mt-1">يجب استكمال جميع بيانات الميلاد والإقامة والبطاقة الخاصة بالفرد في هذه الاستمارة لكي يتم حفظها والتتمكن من تقديم الطلب.</p>
                </div>
              </div>

              <div class="space-y-6">
                <!-- ID Details -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                  <div>
                    <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الرقم الوطني</label>
                    <input type="text" :value="selectedPersonnelList[0].national_id || '—'" disabled class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300" />
                  </div>
                  <div>
                    <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400" :class="{'text-error-600': headerValidationErrors.id_issue_date}">تاريخ إصدار البطاقة</label>
                    <flat-pickr v-model="localHeaderData.id_issue_date" :config="flatpickrConfig" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500" :class="{'border-error-500 focus:border-error-500': headerValidationErrors.id_issue_date}" />
                    <p v-if="headerValidationErrors.id_issue_date" class="mt-1 text-xs text-error-500">{{ headerValidationErrors.id_issue_date }}</p>
                  </div>
                  <div>
                    <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">جهة الإصدار</label>
                    <input type="text" v-model="localHeaderData.id_issue_place" placeholder="مثال: صنعاء، تعز، ..." class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500" />
                  </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <!-- Birth Location -->
                  <div class="space-y-4 p-4 rounded-xl border border-gray-100 bg-gray-50/30 dark:border-gray-800 dark:bg-gray-800/10">
                    <h4 class="font-bold text-sm text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
                      <svg class="w-4 h-4 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                      محل الميلاد
                    </h4>
                    <div class="grid grid-cols-2 gap-4">
                      <!-- Governorate -->
                      <div>
                        <label class="mb-1.5 block text-xs font-medium text-gray-600 dark:text-gray-400">المحافظة</label>
                        <div class="relative bg-transparent">
                          <select v-model="localHeaderData.birth_gov_id" class="w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm text-gray-800 focus:border-brand-300 focus:outline-hidden dark:border-gray-700 dark:bg-gray-900 dark:text-white/90">
                            <option :value="null">اختر...</option>
                            <option v-for="gov in coreStore.governorates" :key="gov.id" :value="gov.id">{{ gov.name }}</option>
                          </select>
                        </div>
                      </div>
                      <!-- District -->
                      <div>
                        <label class="mb-1.5 block text-xs font-medium text-gray-600 dark:text-gray-400">المديرية</label>
                        <div class="relative bg-transparent">
                          <select v-model="localHeaderData.birth_district_id" :disabled="!localHeaderData.birth_gov_id" class="w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm text-gray-800 focus:border-brand-300 focus:outline-hidden dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 disabled:opacity-50">
                            <option :value="null">اختر...</option>
                            <option v-for="d in headerDistrictsCache[localHeaderData.birth_gov_id as number] || []" :key="d.id" :value="d.id">{{ d.name_ar || d.name }}</option>
                          </select>
                        </div>
                      </div>
                      <!-- Sub District -->
                      <div>
                        <label class="mb-1.5 block text-xs font-medium text-gray-600 dark:text-gray-400">العزلة</label>
                        <div class="relative bg-transparent">
                          <select v-model="localHeaderData.birth_sub_district_id" :disabled="!localHeaderData.birth_district_id" class="w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm text-gray-800 focus:border-brand-300 focus:outline-hidden dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 disabled:opacity-50">
                            <option :value="null">اختر...</option>
                            <option v-for="s in headerSubDistrictsCache[localHeaderData.birth_district_id as number] || []" :key="s.id" :value="s.id">{{ s.name_ar || s.name }}</option>
                          </select>
                        </div>
                      </div>
                      <!-- Village -->
                      <div>
                        <label class="mb-1.5 block text-xs font-medium text-gray-600 dark:text-gray-400">القرية/الحارة</label>
                        <div class="relative bg-transparent">
                          <select v-model="localHeaderData.birth_village_id" :disabled="!localHeaderData.birth_sub_district_id" class="w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm text-gray-800 focus:border-brand-300 focus:outline-hidden dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 disabled:opacity-50">
                            <option :value="null">اختر...</option>
                            <option v-for="v in headerVillagesCache[localHeaderData.birth_sub_district_id as number] || []" :key="v.id" :value="v.id">{{ v.name_ar || v.name_ar_normalized || v.name }}</option>
                          </select>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Residence Location -->
                  <div class="space-y-4 p-4 rounded-xl border border-gray-100 bg-gray-50/30 dark:border-gray-800 dark:bg-gray-800/10">
                    <h4 class="font-bold text-sm text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
                      <svg class="w-4 h-4 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
                      محل الإقامة الحالية
                    </h4>
                    <div class="grid grid-cols-2 gap-4">
                      <!-- Governorate -->
                      <div>
                        <label class="mb-1.5 block text-xs font-medium text-gray-600 dark:text-gray-400">المحافظة</label>
                        <div class="relative bg-transparent">
                          <select v-model="localHeaderData.residence_gov_id" class="w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm text-gray-800 focus:border-brand-300 focus:outline-hidden dark:border-gray-700 dark:bg-gray-900 dark:text-white/90">
                            <option :value="null">اختر...</option>
                            <option v-for="gov in coreStore.governorates" :key="gov.id" :value="gov.id">{{ gov.name }}</option>
                          </select>
                        </div>
                      </div>
                      <!-- District -->
                      <div>
                        <label class="mb-1.5 block text-xs font-medium text-gray-600 dark:text-gray-400">المديرية</label>
                        <div class="relative bg-transparent">
                          <select v-model="localHeaderData.residence_district_id" :disabled="!localHeaderData.residence_gov_id" class="w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm text-gray-800 focus:border-brand-300 focus:outline-hidden dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 disabled:opacity-50">
                            <option :value="null">اختر...</option>
                            <option v-for="d in headerDistrictsCache[localHeaderData.residence_gov_id as number] || []" :key="d.id" :value="d.id">{{ d.name_ar || d.name }}</option>
                          </select>
                        </div>
                      </div>
                      <!-- Sub District -->
                      <div>
                        <label class="mb-1.5 block text-xs font-medium text-gray-600 dark:text-gray-400">العزلة</label>
                        <div class="relative bg-transparent">
                          <select v-model="localHeaderData.residence_sub_district_id" :disabled="!localHeaderData.residence_district_id" class="w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm text-gray-800 focus:border-brand-300 focus:outline-hidden dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 disabled:opacity-50">
                            <option :value="null">اختر...</option>
                            <option v-for="s in headerSubDistrictsCache[localHeaderData.residence_district_id as number] || []" :key="s.id" :value="s.id">{{ s.name_ar || s.name }}</option>
                          </select>
                        </div>
                      </div>
                      <!-- Village -->
                      <div>
                        <label class="mb-1.5 block text-xs font-medium text-gray-600 dark:text-gray-400">الشارع/القرية</label>
                        <div class="relative bg-transparent">
                          <select v-model="localHeaderData.residence_village_id" :disabled="!localHeaderData.residence_sub_district_id" class="w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm text-gray-800 focus:border-brand-300 focus:outline-hidden dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 disabled:opacity-50">
                            <option :value="null">اختر...</option>
                            <option v-for="v in headerVillagesCache[localHeaderData.residence_sub_district_id as number] || []" :key="v.id" :value="v.id">{{ v.name_ar || v.name_ar_normalized || v.name }}</option>
                          </select>
                        </div>
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
        
        <div class="space-y-8 mt-6">
          <!-- General Dynamic Layout -->
          <div v-for="(section, sIdx) in schema.sections" :key="sIdx">
            <template v-if="getDynamicFields(section).length > 0">
              <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900 shadow-sm relative overflow-visible">
                <div class="absolute top-0 right-0 w-2 h-full bg-emerald-500 rounded-r-2xl"></div>
                <h3 class="mb-5 text-lg font-bold text-gray-900 dark:text-white border-b border-gray-100 pb-3 dark:border-gray-800">{{ section.title }}</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <template v-for="field in getDynamicFields(section)" :key="field.key">
                <!-- Current Rank injected right before to_rank for Rank Settlements -->
                <div v-if="field.key === 'to_rank' && category === 'rank_settlement'" class="bg-gray-50/50 dark:bg-gray-800/20 p-4 rounded-xl border border-gray-100 dark:border-gray-800/60 flex flex-col justify-center">
                  <label class="mb-1 block text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">الرتبة الحالية</label>
                  <div class="text-sm font-bold text-gray-900 dark:text-white">
                    {{ selectedPersonnelList[0]?.rank_name || selectedPersonnelList[0]?.current_rank?.name || selectedPersonnelList[0]?.rank?.name || 'غير متوفر' }}
                  </div>
                </div>

                <div v-show="(field.key !== 'new_military_number' || formData.settlement_type === 'personnel_to_officer') && field.type !== 'hidden'" 
                     class="space-y-1.5">
                  <label class="text-xs font-bold text-gray-700 dark:text-gray-300">
                    {{ field.label }} <span v-if="field.required || (field.key === 'new_military_number' && formData.settlement_type === 'personnel_to_officer')" class="text-red-500">*</span>
                  </label>
                
                <div v-if="field.type === 'select'" class="relative z-20 bg-transparent">
                  <select v-model="formData[field.key]" :disabled="field.disabled" class="w-full appearance-none bg-transparent border border-gray-300 dark:border-gray-700 rounded-lg px-4 py-2.5 text-sm text-gray-800 dark:text-white shadow-theme-xs focus:ring-3 focus:ring-brand-500/10 focus:border-brand-500 outline-none transition-shadow ltr:pr-11 rtl:pl-11 disabled:opacity-50 disabled:bg-gray-100 dark:disabled:bg-gray-800 disabled:cursor-not-allowed">
                    <option value="" disabled>اختر...</option>
                    <option v-for="opt in getFilteredOptions(field)" :key="opt && typeof opt === 'object' ? opt.value : opt" :value="opt && typeof opt === 'object' ? opt.value : opt">
                      {{ opt && typeof opt === 'object' ? opt.label : opt }}
                    </option>
                  </select>
                  <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                    <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                  </span>
                </div>

                <!-- Location Cascade: محافظة → مديرية → عزلة → قرية/حارة -->
                <div v-else-if="field.type === 'location_cascade'" class="md:col-span-2 space-y-4 p-4 rounded-xl border border-gray-100 bg-gray-50/30 dark:border-gray-800 dark:bg-gray-800/10">
                  <h4 class="font-bold text-sm text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
                    <svg class="w-4 h-4 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                    {{ field.label }} <span v-if="field.required" class="text-red-500">*</span>
                  </h4>
                  <div class="grid grid-cols-2 gap-4">
                    <!-- محافظة -->
                    <div>
                      <label class="mb-1.5 block text-xs font-medium text-gray-600 dark:text-gray-400">المحافظة</label>
                      <div class="relative bg-transparent">
                        <select v-model="locationState[field.key + '_gov']" @change="onGovernorateChange(field.key)"
                          class="w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm text-gray-800 focus:border-brand-300 focus:outline-hidden dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 rtl:pl-8">
                          <option value="">اختر المحافظة...</option>
                          <option v-for="g in governorates" :key="g.id" :value="g.id">{{ g.name_ar }}</option>
                        </select>
                        <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none rtl:left-2.5 top-1/2 dark:text-gray-400">
                          <svg class="stroke-current" width="16" height="16" viewBox="0 0 20 20" fill="none"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                        </span>
                      </div>
                    </div>
                    <!-- مديرية -->
                    <div>
                      <label class="mb-1.5 block text-xs font-medium text-gray-600 dark:text-gray-400">المديرية</label>
                      <div class="relative bg-transparent">
                        <select v-model="locationState[field.key + '_dist']" @change="onDistrictChange(field.key)"
                          :disabled="!locationState[field.key + '_gov']"
                          class="w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm text-gray-800 focus:border-brand-300 focus:outline-hidden dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 rtl:pl-8 disabled:opacity-50">
                          <option value="">اختر المديرية...</option>
                          <option v-for="d in getDistricts(field.key)" :key="d.id" :value="d.id">{{ d.name_ar }}</option>
                        </select>
                        <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none rtl:left-2.5 top-1/2 dark:text-gray-400">
                          <svg class="stroke-current" width="16" height="16" viewBox="0 0 20 20" fill="none"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                        </span>
                      </div>
                    </div>
                    <!-- عزلة -->
                    <div>
                      <label class="mb-1.5 block text-xs font-medium text-gray-600 dark:text-gray-400">العزلة</label>
                      <div class="relative bg-transparent">
                        <select v-model="locationState[field.key + '_sub']" @change="onSubDistrictChange(field.key)"
                          :disabled="!locationState[field.key + '_dist']"
                          class="w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm text-gray-800 focus:border-brand-300 focus:outline-hidden dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 rtl:pl-8 disabled:opacity-50">
                          <option value="">اختر العزلة...</option>
                          <option v-for="s in getSubDistricts(field.key)" :key="s.id" :value="s.id">{{ s.name_ar }}</option>
                        </select>
                        <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none rtl:left-2.5 top-1/2 dark:text-gray-400">
                          <svg class="stroke-current" width="16" height="16" viewBox="0 0 20 20" fill="none"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                        </span>
                      </div>
                    </div>
                    <!-- قرية / حارة -->
                    <div>
                      <label class="mb-1.5 block text-xs font-medium text-gray-600 dark:text-gray-400">القرية / الحارة</label>
                      <div class="relative bg-transparent">
                        <select v-model="locationState[field.key + '_vil']" @change="onVillageChange(field.key)"
                          :disabled="!locationState[field.key + '_sub']"
                          class="w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-3 py-2 text-sm text-gray-800 focus:border-brand-300 focus:outline-hidden dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 rtl:pl-8 disabled:opacity-50">
                          <option value="">اختر القرية...</option>
                          <option v-for="v in getVillages(field.key)" :key="v.id" :value="v.id">{{ v.name_ar || v.name_ar_normalized }}</option>
                        </select>
                        <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none rtl:left-2.5 top-1/2 dark:text-gray-400">
                          <svg class="stroke-current" width="16" height="16" viewBox="0 0 20 20" fill="none"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                        </span>
                      </div>
                    </div>
                  </div>
                  <!-- الكتابة اليدوية -->
                  <div class="flex items-center gap-2 mt-2">
                    <label class="flex items-center gap-1.5 cursor-pointer">
                      <input type="checkbox" v-model="locationState[field.key + '_manual']" class="w-4 h-4 rounded border-gray-300 text-brand-600 focus:ring-brand-500" />
                      <span class="text-xs font-medium text-gray-700 dark:text-gray-300">إدخال المكان يدوياً</span>
                    </label>
                  </div>
                  <input v-if="locationState[field.key + '_manual']"
                    v-model="formData[field.key]" type="text" placeholder="اكتب تفاصيل المكان هنا..."
                    class="w-full bg-transparent border border-gray-300 dark:border-gray-700 rounded-lg px-4 py-2.5 text-sm text-gray-900 dark:text-white shadow-theme-xs focus:ring-3 focus:ring-brand-500/10 focus:border-brand-500 outline-none mt-2" />
                  <!-- المكان النهائي المُجمّع -->
                  <div v-if="formData[field.key] && !locationState[field.key + '_manual']" class="mt-2 text-xs text-emerald-700 font-bold bg-emerald-50 dark:bg-emerald-950/20 px-3 py-2 rounded-lg border border-emerald-200 dark:border-emerald-800 flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                    {{ formData[field.key] }}
                  </div>
                </div>
                <div v-else-if="field.type === 'date_range'" class="md:col-span-2 space-y-4 p-4 rounded-xl border border-gray-100 bg-gray-50/30 dark:border-gray-800 dark:bg-gray-800/10 mt-2 mb-2">
                  <h4 class="font-bold text-sm text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
                    <svg class="w-4 h-4 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                    {{ field.label }} <span v-if="field.required" class="text-red-500">*</span>
                  </h4>
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <label class="mb-1.5 block text-xs font-medium text-gray-600 dark:text-gray-400">من تاريخ</label>
                      <flat-pickr v-model="formData['duration_from']" :config="flatpickrConfig" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500" />
                    </div>
                    <div>
                      <label class="mb-1.5 block text-xs font-medium text-gray-600 dark:text-gray-400">إلى تاريخ</label>
                      <flat-pickr v-model="formData['duration_to']" :config="flatpickrConfig" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500" />
                    </div>
                  </div>
                </div>
                <div v-else-if="field.type === 'duration_picker'" class="flex gap-3 mt-1">
                  <!-- سنوات -->
                  <div class="flex-1 flex flex-col relative">
                    <label class="text-[10px] text-gray-500 mb-1 font-bold">سنوات</label>
                    <input type="number" min="0" max="30" class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none text-center" 
                           @input="updateDurationPicker(field.key, 'years', $event)" :value="getDurationPart(field.key, 'years')" />
                  </div>
                  <!-- أشهر -->
                  <div class="flex-1 flex flex-col relative">
                    <label class="text-[10px] text-gray-500 mb-1 font-bold">أشهر</label>
                    <input type="number" min="0" max="11" class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none text-center" 
                           @input="updateDurationPicker(field.key, 'months', $event)" :value="getDurationPart(field.key, 'months')" />
                  </div>
                  <!-- أيام -->
                  <div class="flex-1 flex flex-col relative">
                    <label class="text-[10px] text-gray-500 mb-1 font-bold">أيام</label>
                    <input type="number" min="0" max="30" class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none text-center" 
                           @input="updateDurationPicker(field.key, 'days', $event)" :value="getDurationPart(field.key, 'days')" />
                  </div>
                </div>

                <textarea v-else-if="field.type === 'textarea'" v-model="formData[field.key]" class="w-full bg-transparent border border-gray-300 dark:border-gray-700 rounded-lg px-4 py-2.5 text-sm text-gray-900 dark:text-white shadow-theme-xs focus:ring-3 focus:ring-brand-500/10 focus:border-brand-500 outline-none h-24 transition-shadow"></textarea>
                <div v-else-if="selectedPersonnelList.length > 1 && (field.source === 'personnel_master' || field.key === 'age')">
                  <div class="w-full bg-blue-50/50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800/50 rounded-xl px-4 py-2.5 text-sm flex items-center gap-2 text-blue-700 dark:text-blue-300">
                    <svg class="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    سيتم سحب بيانات كل فرد تلقائياً
                  </div>
                </div>
                <div v-else>
                  <template v-if="field.type === 'date'">
                    <div class="relative">
                      <flat-pickr v-model="formData[field.key]"
                                :config="flatpickrConfig"
                                :readonly="field.key === 'old_value' || field.disabled"
                                class="w-full bg-gray-50 dark:bg-gray-800 border rounded-xl px-4 py-2.5 text-sm focus:ring-2 outline-none transition-shadow text-left cursor-pointer"
                                :class="[(field.key === 'old_value' || field.disabled) ? 'opacity-70 cursor-not-allowed font-bold text-gray-600 bg-gray-100 dark:bg-gray-800/50' : '', formDataErrors[field.key] ? 'border-error-500 focus:ring-error-500' : 'border-gray-200 dark:border-gray-700 focus:ring-brand-500']"
                                dir="ltr" />
                      <span class="absolute text-gray-500 -translate-y-1/2 pointer-events-none right-3 top-1/2 dark:text-gray-400">
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                      </span>
                    </div>
                  </template>
                  <template v-else>
                    <input :type="field.key === 'age' ? 'number' : field.type" v-model="formData[field.key]" 
                            :readonly="field.key === 'old_value' || field.disabled || field.key === 'age'"
                            :maxlength="field.key === 'new_military_number' ? 7 : (field.key === 'new_value' && (formData.correction_type === 'national_id_correction' || formData.field_name === 'national_id') ? 11 : undefined)"
                            :placeholder="field.key === 'age' ? 'يُحسب تلقائياً من تاريخ الميلاد' : ''"
                            :class="['w-full bg-gray-50 dark:bg-gray-800 border rounded-xl px-4 py-2.5 text-sm focus:ring-2 outline-none transition-shadow', (field.key === 'old_value' || field.disabled || field.key === 'age') ? 'opacity-70 cursor-not-allowed font-bold text-gray-600 bg-gray-100 dark:bg-gray-800/50' : '', formDataErrors[field.key] ? 'border-error-500 focus:ring-error-500' : 'border-gray-200 dark:border-gray-700 focus:ring-brand-500']"
                            dir="rtl" />
                  </template>
                  <p v-if="formDataErrors[field.key]" class="text-[10px] text-error-600 font-bold mt-1.5 flex items-center gap-1"><svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg> {{ formDataErrors[field.key] }}</p>
                  <p v-else-if="formDataInfo[field.key]" class="text-[10px] text-blue-600 font-bold mt-1.5 flex items-center gap-1">
                    <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    {{ formDataInfo[field.key] }}
                  </p>
                </div>
                <p v-if="field.key === 'new_military_number'" class="mt-1 text-xs text-brand-600 dark:text-brand-400 flex items-center gap-1">
                  <svg class="h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  الرقم العسكري للضابط يبدأ بـ 60 ويتكون من 7 خانات
                </p>
                <p v-if="field.help_text" class="text-[10px] text-gray-400 mt-1">{{ field.help_text }}</p>
                </div>
              </template>
            </div>
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
import { ref, reactive, computed, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import { Arabic } from 'flatpickr/dist/l10n/ar.js'
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

const flatpickrConfig = {
  dateFormat: 'Y-m-d',
  locale: Arabic,
  altInput: true,
  altFormat: 'Y-m-d',
  disableMobile: true,
  allowInput: true,
}

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

const isInitializingHeaderGeo = ref(false)

watch(() => localHeaderData.birth_gov_id, (newGov, oldVal) => {
  if (isInitializingHeaderGeo.value) return; // Ignore programmatic updates
  localHeaderData.birth_district_id = null;
  localHeaderData.birth_sub_district_id = null;
  localHeaderData.birth_village_id = null;
  if (newGov) fetchHeaderDistricts(newGov);
})
watch(() => localHeaderData.residence_gov_id, (newGov, oldVal) => {
  if (isInitializingHeaderGeo.value) return; // Ignore programmatic updates
  localHeaderData.residence_district_id = null;
  localHeaderData.residence_sub_district_id = null;
  localHeaderData.residence_village_id = null;
  if (newGov) fetchHeaderDistricts(newGov);
})
watch(() => localHeaderData.birth_district_id, (newDist, oldVal) => {
  if (isInitializingHeaderGeo.value) return; // Ignore programmatic updates
  localHeaderData.birth_sub_district_id = null;
  localHeaderData.birth_village_id = null;
  if (newDist) fetchHeaderSubDistricts(newDist);
})
watch(() => localHeaderData.residence_district_id, (newDist, oldVal) => {
  if (isInitializingHeaderGeo.value) return; // Ignore programmatic updates
  localHeaderData.residence_sub_district_id = null;
  localHeaderData.residence_village_id = null;
  if (newDist) fetchHeaderSubDistricts(newDist);
})
watch(() => localHeaderData.birth_sub_district_id, (newSub, oldVal) => {
  if (isInitializingHeaderGeo.value) return; // Ignore programmatic updates
  localHeaderData.birth_village_id = null;
  if (newSub) fetchHeaderVillages(newSub);
})
watch(() => localHeaderData.residence_sub_district_id, (newSub, oldVal) => {
  if (isInitializingHeaderGeo.value) return; // Ignore programmatic updates
  localHeaderData.residence_village_id = null;
  if (newSub) fetchHeaderVillages(newSub);
})

watch(selectedPersonnelList, async (newVal) => {
  if (newVal && newVal.length > 0) {
    isInitializingHeaderGeo.value = true;
    const p = newVal[0];
    
    try {
      const promises = [];
      if (p.birth_gov_id) promises.push(fetchHeaderDistricts(p.birth_gov_id));
      if (p.birth_district_id) promises.push(fetchHeaderSubDistricts(p.birth_district_id));
      if (p.birth_sub_district_id) promises.push(fetchHeaderVillages(p.birth_sub_district_id));
      
      if (p.residence_gov_id) promises.push(fetchHeaderDistricts(p.residence_gov_id));
      if (p.residence_district_id) promises.push(fetchHeaderSubDistricts(p.residence_district_id));
      if (p.residence_sub_district_id) promises.push(fetchHeaderVillages(p.residence_sub_district_id));
      
      await Promise.all(promises);
      
      localHeaderData.birth_gov_id = p.birth_gov_id || null;
      localHeaderData.birth_district_id = p.birth_district_id || null;
      localHeaderData.birth_sub_district_id = p.birth_sub_district_id || null;
      localHeaderData.birth_village_id = p.birth_village_id || null;
      localHeaderData.residence_gov_id = p.residence_gov_id || null;
      localHeaderData.residence_district_id = p.residence_district_id || null;
      localHeaderData.residence_sub_district_id = p.residence_sub_district_id || null;
      localHeaderData.residence_village_id = p.residence_village_id || null;
      localHeaderData.id_issue_date = p.id_issue_date || '';
      localHeaderData.id_issue_place = p.id_issue_place || '';

    } finally {
      await nextTick();
      setTimeout(() => {
        isInitializingHeaderGeo.value = false;
      }, 150);
    }
  }
}, { deep: true })

const isHeaderDataComplete = computed(() => {
  return localHeaderData.birth_gov_id && localHeaderData.birth_district_id && 
    localHeaderData.birth_sub_district_id && localHeaderData.birth_village_id &&
    localHeaderData.residence_gov_id && localHeaderData.residence_district_id && 
    localHeaderData.residence_sub_district_id && localHeaderData.residence_village_id &&
    localHeaderData.id_issue_date && localHeaderData.id_issue_place
})

const headerValidationErrors = reactive<Record<string, string>>({})

watch([() => localHeaderData.id_issue_date, () => selectedPersonnelList.value[0]?.birth_date], ([idDate, birthDate]) => {
  if (idDate) {
    const issueDateObj = new Date(idDate)
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    
    if (issueDateObj > today) {
      headerValidationErrors.id_issue_date = 'لا يمكن أن يكون تاريخ الإصدار في المستقبل'
    } else if (birthDate) {
      const birthDateObj = new Date(birthDate)
      if (issueDateObj <= birthDateObj) {
        headerValidationErrors.id_issue_date = 'تاريخ الإصدار يجب أن يكون بعد تاريخ الميلاد'
      } else {
        headerValidationErrors.id_issue_date = ''
      }
    } else {
      headerValidationErrors.id_issue_date = ''
    }
  } else {
    headerValidationErrors.id_issue_date = ''
  }
})

// Step 2 & 3 State
const formData = ref<any>({})
const formDataErrors = reactive<Record<string, string>>({})
const formDataInfo = reactive<Record<string, string>>({})

watch(() => formData.value.birth_date, (newVal) => {
  if (newVal && schema.value?.sections?.some((s:any) => s.fields?.some((f:any) => f.key === 'age'))) {
    const bdate = new Date(newVal)
    const today = new Date()
    if (!isNaN(bdate.getTime()) && bdate < today) {
      let calcAge = today.getFullYear() - bdate.getFullYear()
      const m = today.getMonth() - bdate.getMonth()
      if (m < 0 || (m === 0 && today.getDate() < bdate.getDate())) {
        calcAge--
      }
      formData.value.age = Math.max(0, calcAge)
    } else {
      formData.value.age = ''
    }
  }
})

watch(() => formData.value, (newVal) => {
  if (!schema.value?.sections) return
  const allFields = schema.value.sections.flatMap((s:any) => s.fields || [])
  const today = new Date().toISOString().split('T')[0]
  const allowedFuture = ['end_date', 'due_date']

  for (const f of allFields) {
    if (f.type === 'date') {
      const val = newVal[f.key]
      validateDateField(f, val)
    }
  }

  // --- الحساب التلقائي لمدة الدراسة ---
  if (type === 'study_leave') {
    if (newVal.start_date && newVal.end_date) {
      const sDate = new Date(newVal.start_date)
      const eDate = new Date(newVal.end_date)
      if (!isNaN(sDate.getTime()) && !isNaN(eDate.getTime()) && eDate > sDate) {
        const diffTime = Math.abs(eDate.getTime() - sDate.getTime())
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
        
        const y = Math.floor(diffDays / 365.25)
        const m = Math.floor((diffDays % 365.25) / 30)
        const d = Math.floor((diffDays % 365.25) % 30)
        
        const parts = []
        if (y > 0) parts.push(`${y} سنة`)
        if (m > 0) parts.push(`${m} شهر`)
        if (d > 0) parts.push(`${d} يوم`)
        
        newVal.duration = parts.length > 0 ? parts.join(' و ') : '0 يوم'
      } else {
        newVal.duration = ''
      }
    }
  }

}, { deep: true })

// فتح التقويم عند النقر على الحقل
function openDatePicker(event: Event) {
  const target = event.target as any
  if (target && typeof target.showPicker === 'function') {
    try {
      target.showPicker()
    } catch (e) {
      // Ignore if browser doesn't support or throws error
    }
  }
}

// يُستدعى للتحقق اللحظي من التواريخ (تم تحديثه ليدعم flatpickr)
function validateDateField(field: any, val: string) {
  const rawValue = val || ''
  const allowedFuture = ['start_date', 'end_date', 'due_date']
  const today = new Date().toISOString().split('T')[0]

  if (!rawValue) {
    if (field.required) {
      formDataErrors[field.key] = 'تاريخ غير صالح أو الحقل فارغ'
    } else {
      formDataErrors[field.key] = ''
    }
  } else if (!allowedFuture.includes(field.key) && rawValue > today) {
    formDataErrors[field.key] = 'تاريخ غير صالح: لا يمكن أن يكون في المستقبل'
  } else {
    // ── الفحص اللحظي المتقدم للشهداء والمتوفين ──
    if (['martyrdom_date', 'death_date'].includes(field.key)) {
      const person = selectedPersonnelList.value[0];
      if (person) {
        const joinDateStr = person.join_date;
        const birthDateStr = person.birth_date;
        
        if (birthDateStr) {
          const mDate = new Date(rawValue);
          const bDate = new Date(birthDateStr);
          const ageInYears = (mDate.getTime() - bDate.getTime()) / (1000 * 60 * 60 * 24 * 365.25);
          
          if (ageInYears < 0) {
            formDataErrors[field.key] = 'خطأ منطقي: التاريخ مستحيل (يسبق تاريخ ميلاد الفرد)';
            return;
          } else if (ageInYears < 18) {
            formDataErrors[field.key] = `خطأ منطقي: العمر عند هذا التاريخ سيكون (${ageInYears.toFixed(1)} سنة) وهو أقل من الحد الأدنى المقبول (18)`;
            return;
          }
        }

        if (joinDateStr && rawValue < joinDateStr) {
          formDataErrors[field.key] = `خطأ منطقي: التاريخ مستحيل (قبل تاريخ التجنيد: ${joinDateStr})`;
          return;
        }
      }
    }
    
    // ── الفحص اللحظي للانتداب ──
    if (['start_date', 'end_date'].includes(field.key) && formData.value) {
      if (field.key === 'start_date' && formData.value.end_date) {
        if (rawValue >= formData.value.end_date) {
          formDataErrors[field.key] = 'خطأ منطقي: تاريخ البدء يجب أن يسبق تاريخ الانتهاء'
          return
        }
        formDataErrors['end_date'] = '' // Clear end_date error if any
      }
      
      if (field.key === 'end_date' && formData.value.start_date) {
        if (rawValue <= formData.value.start_date) {
          formDataErrors[field.key] = 'خطأ منطقي: تاريخ الانتهاء يجب أن يكون بعد تاريخ البدء'
          return
        }
        
        // حساب المدة
        const startD = new Date(formData.value.start_date)
        const endD = new Date(rawValue)
        const diffTime = Math.abs(endD.getTime() - startD.getTime())
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
        const diffYears = (diffDays / 365.25).toFixed(1)
        
        // Just show info, backend enforces the max limit based on settings
        let durationText = 'المدة المحسوبة'
        let durationLimitText = 'المدة'
        
        if (type === 'study_leave') {
          durationText = 'مدة الدراسة المحسوبة'
          durationLimitText = 'الدراسة'
        } else if (type === 'escort') {
          durationText = 'مدة المرافقة المحسوبة'
          durationLimitText = 'المرافقة'
        } else if (type === 'seconded') {
          durationText = 'مدة الانتداب المحسوبة'
          durationLimitText = 'الانتداب'
        }
        
        let maxAllowedYears = 4; // Default for secondment
        const studyType = formData.value.study_type;
        if (type === 'study_leave') {
          if (studyType === 'بكالوريوس') maxAllowedYears = 6;
          else if (studyType === 'ماجستير') maxAllowedYears = 3;
          else if (studyType === 'دكتوراه') maxAllowedYears = 5;
          else if (studyType === 'دبلوم' || studyType === 'دورة تخصصية') maxAllowedYears = 2;
          else maxAllowedYears = 6;
        }

        // Beautiful text calculation
        const y = Math.floor(diffDays / 365.25);
        const m = Math.floor((diffDays % 365.25) / 30);
        const d = Math.floor((diffDays % 365.25) % 30);
        
        const parts = [];
        if (y > 0) parts.push(`${y} سنة`);
        if (m > 0) parts.push(`${m} شهر`);
        if (d > 0) parts.push(`${d} يوم`);
        const beautifulDuration = parts.length > 0 ? parts.join(' و ') : '0 يوم';

        if (diffDays > (maxAllowedYears * 365)) {
          formDataInfo[field.key] = `تنبيه: مدة ${durationLimitText} المطلوبة (${beautifulDuration}) تتجاوز الحد الأقصى المسموح لـ ${studyType ? `درجة (${studyType})` : 'هذه الخدمة'} وهو (${maxAllowedYears} سنوات). قد يتم رفض الطلب.`
        } else {
          formDataInfo[field.key] = `${durationText}: ${beautifulDuration}`
        }
        formDataErrors[field.key] = '' // Clear error
        formDataErrors['start_date'] = '' // Clear start_date error if any
      }
    }
    
    // إذا لم تكن هناك أخطاء متقدمة ولم يتم تحديد خطأ للانتداب
    if (!['start_date', 'end_date'].includes(field.key)) {
      formDataErrors[field.key] = ''
    }
  }
}

const documentIds = ref<number[]>([])
const uploadedFiles = ref<Record<string, File>>({})
const uploadingDoc = ref<string | null>(null)

// Submission State
const isSubmitting = ref(false)
const submittedCount = ref(0)

// Location Cascade State
const locationState = reactive<Record<string, any>>({})
const durationState = ref<Record<string, {years: number, months: number, days: number}>>({})

function getDurationPart(key: string, part: 'years'|'months'|'days') {
  if (!durationState.value[key]) {
    durationState.value[key] = { years: 0, months: 0, days: 0 }
  }
  return durationState.value[key][part] || ''
}

function updateDurationPicker(key: string, part: 'years'|'months'|'days', event: Event) {
  const val = parseInt((event.target as HTMLInputElement).value) || 0
  if (!durationState.value[key]) {
    durationState.value[key] = { years: 0, months: 0, days: 0 }
  }
  durationState.value[key][part] = val
  
  // Format string: e.g. "سنة و 5 أشهر و 4 أيام"
  const y = durationState.value[key].years
  const m = durationState.value[key].months
  const d = durationState.value[key].days
  
  const parts = []
  
  if (y > 0) {
    if (y === 1) parts.push('سنة')
    else if (y === 2) parts.push('سنتين')
    else if (y >= 3 && y <= 10) parts.push(`${y} سنوات`)
    else parts.push(`${y} سنة`)
  }
  
  if (m > 0) {
    if (m === 1) parts.push('شهر')
    else if (m === 2) parts.push('شهرين')
    else if (m >= 3 && m <= 10) parts.push(`${m} أشهر`)
    else parts.push(`${m} شهر`)
  }
  
  if (d > 0) {
    if (d === 1) parts.push('يوم')
    else if (d === 2) parts.push('يومين')
    else if (d >= 3 && d <= 10) parts.push(`${d} أيام`)
    else parts.push(`${d} يوم`)
  }
  
  formData.value[key] = parts.length > 0 ? parts.join(' و ') : ''
}
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
  
  const hardcodedKeys = ['military_number', 'full_name', 'current_rank', 'rank', 'unit', 'national_id', 'governorate', 'residence_gov_id']
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
  
  // [FE-001] منع أي معاملة لفرد في حالة خروج نهائي (شهيد، متوفى، متقاعد، مفصول)
  // الشهيد والمتوفى لا يعودان للخدمة بأي شكل. لا توجد استثناءات.
  let statusStr = person.status_name || person.current_status_name || '';
  if (!statusStr && person.current_status) {
    if (typeof person.current_status === 'object') {
      statusStr = person.current_status.name || '';
    } else if (typeof person.current_status === 'string') {
      statusStr = person.current_status;
    }
  }
  statusStr = String(statusStr || '');

  // التحقق من الحالة النهائية — الشهيد والمتوفى لا استثناء لهما أبداً
  const terminalKeywords = [
    'شهيد', 'شهد', 'متوفى', 'متوفي', 'وفيات', 'وفاة', 'وفاه',
    'تقاعد', 'متقاعد', 'إنهاء المدة', 'مفصول', 'فصل', 'خروج نهائي'
  ];
  const isTerminal = terminalKeywords.some(kw => statusStr.includes(kw));
  const isDeceasedOrMartyr = ['شهيد', 'شهد', 'متوفى', 'متوفي', 'وفيات', 'وفاة', 'وفاه'].some(kw => statusStr.includes(kw));

  if (isTerminal) {
    // الشهيد والمتوفى: لا يُقبل منهم أي طلب مطلقاً إلا التصحيح
    // المتقاعد والمفصول: يُقبل منهم تصحيح أو إعادة للخدمة فقط
    if (category !== 'correction' && type !== 'return_to_service') {
      const isMartyred = statusStr.includes('شهيد') || statusStr.includes('شهد');
      Swal.fire({
        icon: 'error',
        title: 'إجراء غير مسموح به',
        html: `
          <div class="text-right space-y-3 p-2">
            <div class="flex items-start gap-3 p-3 bg-red-50 border border-red-200 rounded-xl">
              <span class="text-2xl mt-0.5">${isMartyred ? '🕊️' : '🛑'}</span>
              <div>
                <p class="font-bold text-red-800 mb-1">
                  الفرد: <span class="font-black">${person.full_name}</span>
                </p>
                <p class="text-sm text-red-700">
                  مسجّل في النظام بحالة: <b class="bg-red-100 px-2 py-0.5 rounded font-bold">${statusStr}</b>
                </p>
              </div>
            </div>
            <p class="text-sm text-gray-700 leading-relaxed">
              ${isMartyred
                ? 'الشهيد <b>لا يمكن تقديم أي خدمة أو معاملة له</b> بعد تسجيل استشهاده في النظام. هذا القيد نهائي وغير قابل للتجاوز.'
                : isDeceasedOrMartyr
                  ? 'المتوفى <b>لا يمكن تقديم أي خدمة أو معاملة له</b> بعد تسجيل وفاته في النظام.'
                  : 'الفرد ذو حالة الخروج النهائي (تقاعد/فصل/إنهاء مدة) <b>لا يمكن تقديم خدمات أو معاملات جديدة له</b> باستثناء إعادة الخدمة أو التصحيح.'
              }
            </p>
            <p class="text-xs text-gray-500 bg-gray-50 p-2 rounded-lg border">
              إذا كانت هناك حاجة لتصحيح بيانات أرشيفية، الرجاء استخدام طلبات التصحيح.
            </p>
          </div>
        `,
        confirmButtonText: 'فهمت',
        confirmButtonColor: '#dc2626',
      })
      return
    }
  }

  // 1.5 منع إعادة خدمة لمن هو في الخدمة بالفعل، أو تحديد سبب الإعادة آلياً
  if (type === 'return_to_service') {
    const isActive = statusStr.includes('في الخدمة') || statusStr.includes('عامل') || statusStr.includes('ميدان');
    if (isActive) {
      Swal.fire({
        icon: 'error',
        title: 'لا يمكن عمل إعادة خدمة',
        text: `الفرد المختار متواجد بالفعل على رأس العمل (حالته: ${statusStr}). إعادة الخدمة تتم للمنقطعين والفصل والسجن فقط.`
      })
      return
    }
    
    // Auto-select reason based on status
    if (statusStr.includes('سجن') || statusStr.includes('مسجون')) {
      formData.value.return_reason = 'sentence_end' // انتهاء محكومية/سجن
    } else if (statusStr.includes('فصل') || statusStr.includes('مفصول') || statusStr.includes('فرار') || statusStr.includes('منقطع')) {
      formData.value.return_reason = 'committee' // قرار لجنة
    } else if (statusStr.includes('أسر') || statusStr.includes('أسير')) {
      formData.value.return_reason = 'amnesty' // عفو أو تحرير
    }

    // Disable the reason field if auto-selected
    if (formData.value.return_reason && schema.value?.sections?.[0]?.fields) {
      const reasonField = schema.value.sections[0].fields.find((f: any) => f.key === 'return_reason')
      if (reasonField) reasonField.disabled = true
    }
  }

  // 1.8 التحقق الاستباقي الخاص باستمارة "إنهاء مدة"
  if (type === 'end_of_service') {
    const joinDateStr = person.join_date;
    const birthDateStr = person.birth_date;
    
    if (joinDateStr) {
      const jDate = new Date(joinDateStr);
      const todayDate = new Date();
      
      let serviceYears = todayDate.getFullYear() - jDate.getFullYear();
      let serviceMonths = todayDate.getMonth() - jDate.getMonth();
      if (todayDate.getMonth() < jDate.getMonth() || (todayDate.getMonth() === jDate.getMonth() && todayDate.getDate() < jDate.getDate())) {
        serviceYears--;
        serviceMonths += 12;
      }
      
      if (serviceYears < 20) {
        Swal.fire({
          icon: 'error',
          title: 'لم يكمل شرط الخدمة',
          html: `
            <div class="text-right p-2">
              <p class="mb-2 text-gray-800">الخدمة الفعلية للفرد هي <b>(${serviceYears} سنوات و ${serviceMonths} أشهر)</b> فقط.</p>
              <p class="text-sm text-gray-500">الحد الأدنى لإنهاء المدة هو <b>20 سنة خدمة فعلية</b>.</p>
            </div>
          `,
          confirmButtonText: 'فهمت',
          confirmButtonColor: '#dc2626'
        });
        return;
      }
      
      if (birthDateStr) {
        const bDate = new Date(birthDateStr);
        let ageAtJoin = jDate.getFullYear() - bDate.getFullYear();
        if (jDate.getMonth() < bDate.getMonth() || (jDate.getMonth() === bDate.getMonth() && jDate.getDate() < bDate.getDate())) {
          ageAtJoin--;
        }
        
        if (ageAtJoin < 15) {
          Swal.fire({
            icon: 'error',
            title: 'عمر التجنيد غير منطقي',
            text: `تاريخ الالتحاق المسجل في الأرشيف غير منطقي. عمر الفرد عند الالتحاق كان (${ageAtJoin}) سنة. يجب أن يكون 15 سنة على الأقل.`
          });
          return;
        }
      }
    }
  }

  // 1.9 التحقق الاستباقي الخاص باستمارة "مفرغ للدراسة" و "مرافق / معيات"
  if (type === 'study_leave' || type === 'escort') {
    const isActive = statusStr.includes('في الخدمة') || statusStr.includes('عامل') || statusStr.includes('ميدان');
    if (!isActive) {
      Swal.fire({
        icon: 'error',
        title: 'غير مصرح بالخدمة',
        text: `الفرد المختار حالته الحالية (${statusStr}). هذه الخدمة مسموحة فقط للأفراد العاملين على رأس العمل.`
      });
      return;
    }
  }

  // 1.10 التحقق الاستباقي الخاص باستمارة "بلوغ السن القانوني"
  if (type === 'retirement_age') {
    const joinDateStr = person.join_date;
    const birthDateStr = person.birth_date;
    let hasReachedRetirement = false;

    if (joinDateStr) {
      const jDate = new Date(joinDateStr);
      const todayDate = new Date();
      let serviceYears = todayDate.getFullYear() - jDate.getFullYear();
      if (todayDate.getMonth() < jDate.getMonth() || (todayDate.getMonth() === jDate.getMonth() && todayDate.getDate() < jDate.getDate())) {
        serviceYears--;
      }
      if (serviceYears >= 35) {
        hasReachedRetirement = true;
      }
    }

    if (!hasReachedRetirement && birthDateStr) {
      const bDate = new Date(birthDateStr);
      const todayDate = new Date();
      let currentAge = todayDate.getFullYear() - bDate.getFullYear();
      if (todayDate.getMonth() < bDate.getMonth() || (todayDate.getMonth() === bDate.getMonth() && todayDate.getDate() < bDate.getDate())) {
        currentAge--;
      }
      if (currentAge >= 60) {
        hasReachedRetirement = true;
      }
    }

    if (joinDateStr && birthDateStr && !hasReachedRetirement) {
      Swal.fire({
        icon: 'error',
        title: 'لم يبلغ السن القانوني',
        html: `
          <div class="text-right p-2">
            <p class="mb-2 text-gray-800">الفرد لم يستوفِ شروط التقاعد القانونية المبكرة أو العمرية.</p>
            <p class="text-sm text-gray-500">يجب أن يكمل <b>35 سنة خدمة</b> أو يبلغ <b>60 عاماً</b> من العمر لتمرير الاستمارة.</p>
          </div>
        `,
        confirmButtonText: 'فهمت',
        confirmButtonColor: '#dc2626'
      });
      return;
    }
  }

  // 1.11 التحقق العام من جودة البيانات
  if (category !== 'correction' && person.data_quality_score !== undefined && person.data_quality_score < 50) {
    Swal.fire({
      icon: 'error',
      title: 'جودة البيانات متدنية',
      html: `
        <div class="text-right p-2">
          <p class="mb-2 text-gray-800">جودة بيانات الفرد منخفضة جداً <b>(${person.data_quality_score}%)</b>.</p>
          <p class="text-sm text-gray-500">لا يمكن تقديم الخدمات الرسمية إلا بنسبة جودة <b>50%</b> فما فوق. الرجاء استكمال الملف عبر طلبات التصحيح أولاً.</p>
        </div>
      `,
      confirmButtonText: 'فهمت',
      confirmButtonColor: '#dc2626'
    });
    return;
  }

  // 2. التحقق من الباك إند إذا كانت هناك معاملة معلقة لأي نوع
  if (category === 'form' || category === 'rank_settlement') {
    // [FE-002] التحقق من أن الفرد لا يمتلك الحالة المستهدفة بالفعل
    if (category === 'form' && schema.value?.target_status) {
      const targetStatus = schema.value.target_status;
      const currentStatus = statusStr;
      const normalize = (str: string) => (str || '').replace(/(^|\s)ال/g, '$1').trim();
      const normTarget = normalize(targetStatus);
      const normCurrent = normalize(currentStatus);
      
      const targetWords = normTarget.split(/\s+/).filter(w => w.length >= 3);
      const currentWords = normCurrent.split(/\s+/).filter(w => w.length >= 3);
      
      let isSameStatus = false;
      if (normTarget === normCurrent) isSameStatus = true;
      else {
        for (const w of targetWords) if (normCurrent.includes(w)) isSameStatus = true;
        for (const w of currentWords) if (normTarget.includes(w)) isSameStatus = true;
      }
      
      if (isSameStatus) {
        Swal.fire({
          icon: 'error',
          title: 'حالة مكررة',
          html: `
            <div class="text-right p-2">
              <p class="mb-2 text-gray-800">الفرد المختار يمتلك هذه الحالة <b>(${currentStatus})</b> مسبقاً في النظام.</p>
              <p class="text-sm text-gray-500">لا يمكنك تقديم استمارة لنفس الحالة التي هو عليها الآن. يتم تقديم الاستمارات لتغيير الحالة فقط.</p>
            </div>
          `,
          confirmButtonText: 'فهمت',
          confirmButtonColor: '#dc2626'
        })
        return
      }
    }

    try {
      const checkRes = await api.get('/service-cycle/forms/check_pending/', { params: { personnel_id: person.military_number } })
      if (checkRes.data?.has_pending) {
        const pendingId = checkRes.data.pending_id
        const pendingType = checkRes.data.form_type
        Swal.fire({
          icon: 'warning',
          title: 'طلب قيد الإجراء',
          html: `<p class="text-sm text-gray-700 text-right mb-3">لا يمكن إنشاء معاملة جديدة: يوجد معاملة سابقة (نوع: ${pendingType}) قيد الإجراء لهذا الفرد.</p><p class="text-xs font-mono text-gray-500 text-right">رقم المعاملة: <b class="text-blue-600">TX-${String(pendingId).padStart(6, '0')}</b></p>`,
          confirmButtonText: 'عرض المعاملة المعلقة',
          showCancelButton: true,
          cancelButtonText: 'إلغاء',
          confirmButtonColor: '#2563eb',
        }).then(r => {
          if (r.isConfirmed) router.push(`/services/forms/${pendingId}`)
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
        if (field.source === 'personnel_master' || ['birth_date', 'join_date'].includes(field.key)) {
          formData.value[field.key] = person[field.key] || ''
        }
      })
    })
  }
  
  step.value = 2
}

// === Step 2 Logic ===
async function validateAndGoToStep3() {
  const allFields = schema.value.sections?.flatMap((s: any) => s.fields || []) || []

  // 1. تحقق من بيانات الأساسية للفرد (الميلاد، الإقامة، البطاقة)
  if (!isHeaderDataComplete.value) {
    Swal.fire({
      icon: 'error',
      title: 'بيانات ناقصة',
      text: 'لا يمكن الانتقال للمرفقات. يرجى استكمال "بيانات الميلاد والإقامة الحالية" أولاً.'
    })
    return
  }

  // 2. تحقق من أخطاء التحقق الفورية للتواريخ
  const dateErrors = allFields.filter((f: any) => f.type === 'date' && formDataErrors[f.key])
  if (dateErrors.length > 0) {
    Swal.fire({
      icon: 'error',
      title: 'تاريخ غير صالح',
      html: dateErrors.map((f: any) => `<b>${f.label}</b>: ${formDataErrors[f.key]}`).join('<br>')
    })
    return
  }

  // 3. تحقق من الأخطاء المنطقية في التواريخ (مثل تاريخ الاستشهاد يسبق التجنيد)
  const logicalErrors = allFields.filter((f: any) => formDataErrors[f.key] && formDataErrors[f.key].includes('خطأ'))
  if (logicalErrors.length > 0) {
    Swal.fire({
      icon: 'error',
      title: 'يوجد خطأ منطقي في البيانات',
      html: logicalErrors.map((f: any) => `<b>${f.label}</b>: ${formDataErrors[f.key]}`).join('<br>')
    })
    return
  }

  // 2. تحقق من الحقول الإلزامية الفارغة
  if (allFields.length > 0) {
    const missing = allFields.filter((f: any) => {
      if (f.key === 'new_military_number') {
        return formData.value.settlement_type === 'personnel_to_officer' && !formData.value[f.key]
      }
      if (f.type === 'date' && f.required && !formData.value[f.key]) {
        if (!formDataErrors[f.key]) {
          formDataErrors[f.key] = 'تاريخ غير صالح أو الحقل فارغ'
        }
        return true
      }
      return f.required && !formData.value[f.key]
    })
    if (missing.length > 0) {
      const invalidDates = missing.filter((f: any) => f.type === 'date')
      const blankFields = missing.filter((f: any) => f.type !== 'date')
      if (invalidDates.length > 0) {
        Swal.fire({
          icon: 'error',
          title: 'تاريخ غير صالح',
          text: `الحقول التالية تحتوي على تاريخ غير صالح: ${invalidDates.map((f:any) => f.label).join('، ')}`
        })
        return
      }
      Swal.fire({
        icon: 'warning',
        title: 'بيانات ناقصة',
        text: `الرجاء تعبئة الحقول الإلزامية: ${blankFields.map((f:any) => f.label).join('، ')}`
      })
      return
    }
  }

  // 3. التحقق الخاص باستمارة "إنهاء مدة"
  if (type === 'end_of_service') {
    const joinDateStr = formData.value.join_date;
    const birthDateStr = formData.value.birth_date;
    
    if (joinDateStr && birthDateStr) {
      const jDate = new Date(joinDateStr);
      const bDate = new Date(birthDateStr);
      const todayDate = new Date();
      
      let ageAtJoin = jDate.getFullYear() - bDate.getFullYear();
      if (jDate.getMonth() < bDate.getMonth() || (jDate.getMonth() === bDate.getMonth() && jDate.getDate() < bDate.getDate())) {
        ageAtJoin--;
      }
      
      if (ageAtJoin < 15) {
        Swal.fire({
          icon: 'error',
          title: 'عمر التجنيد غير منطقي',
          text: `عمر الفرد عند الالتحاق كان (${ageAtJoin}) سنة. يجب أن يكون 15 سنة على الأقل.`
        });
        return;
      }
      
      let serviceYears = todayDate.getFullYear() - jDate.getFullYear();
      let serviceMonths = todayDate.getMonth() - jDate.getMonth();
      if (todayDate.getMonth() < jDate.getMonth() || (todayDate.getMonth() === jDate.getMonth() && todayDate.getDate() < jDate.getDate())) {
        serviceYears--;
        serviceMonths += 12;
      }
      
      if (serviceYears < 20) {
        Swal.fire({
          icon: 'error',
          title: 'لم يكمل شرط الخدمة',
          html: `الخدمة الفعلية للفرد هي <b>(${serviceYears} سنوات)</b> فقط.<br>الحد الأدنى لإنهاء المدة هو <b>20 سنة خدمة فعلية</b>.`
        });
        return;
      }
    }
  }

  // 4. التحقق من الترقية
  if (formData.value.settlement_type === 'personnel_to_officer' && formData.value.new_military_number) {
    const milNum = formData.value.new_military_number
    if (!milNum.startsWith('60') || milNum.length !== 7 || isNaN(Number(milNum))) {
      Swal.fire({ icon: 'warning', title: 'رقم عسكري غير صالح', text: 'الرقم العسكري الجديد للضابط يجب أن يبدأ بـ 60 ويتكون من 7 أرقام.' })
      return
    }
    try {
      const checkRes = await api.get('/personnel/check-military-number/', { params: { value: milNum } })
      if (checkRes.data?.exists) {
        Swal.fire({ icon: 'error', title: 'الرقم العسكري مستخدم', text: 'هذا الرقم العسكري مستخدم بالفعل في النظام.' })
        return
      }
    } catch (e) { console.error(e) }
  }

  // 4. التحقق من التصحيحات
  const currentField = formData.value.field_name || formData.value.correction_type || type
  if (currentField === 'national_id' || currentField === 'national_id_correction') {
    const val = formData.value.new_value
    if (!val || val.length !== 11 || !/^\d+$/.test(val)) {
      Swal.fire({ icon: 'warning', title: 'رقم وطني غير صالح', text: 'الرقم الوطني الجديد يجب أن يتكون من 11 رقماً.' })
      return
    }
    try {
      const checkRes = await api.get('/personnel/check-national-id/', { params: { value: val } })
      if (checkRes.data?.exists) {
        Swal.fire({ icon: 'error', title: 'الرقم الوطني مسجل مسبقاً', text: 'هذا الرقم الوطني مسجل بالفعل في النظام.' })
        return
      }
    } catch (e) { console.error(e) }
  }

  if (currentField === 'military_number' || currentField === 'military_number_correction') {
    const val = formData.value.new_value
    if (!val || !/^\d{7}$/.test(String(val))) {
      Swal.fire({ icon: 'warning', title: 'رقم عسكري غير صالح', text: 'الرقم العسكري يجب أن يتكون من 7 أرقام بالضبط.' })
      return
    }
    const oldVal = formData.value.old_value
    if (oldVal && String(val) === String(oldVal)) {
      Swal.fire({ icon: 'warning', title: 'لا يوجد تغيير', text: 'الرقم العسكري الجديد لا يمكن أن يكون نفس الرقم الحالي.' })
      return
    }
    try {
      const checkRes = await api.get('/personnel/check-military-number/', { params: { value: val } })
      if (checkRes.data?.exists) {
        Swal.fire({ icon: 'error', title: 'الرقم العسكري مستخدم', text: 'هذا الرقم العسكري مستخدم بالفعل في النظام. يرجى إدخال رقم مختلف.' })
        return
      }
    } catch (e) { console.error(e) }
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
    const docsHtml = missingDocs.map((a:any) => `<li class="flex items-center gap-2 text-red-700 text-sm font-medium"><span class="text-red-500">📎</span> ${a.label}</li>`).join('')
    Swal.fire({
      icon: 'error',
      title: 'مرفقات ناقصة',
      html: `
        <div class="text-right p-3 bg-red-50 rounded-xl border border-red-100">
          <p class="text-red-800 font-bold mb-3">الرجاء إرفاق المستندات الإلزامية التالية قبل تقديم الطلب:</p>
          <ul class="space-y-2 mb-2">
            ${docsHtml}
          </ul>
        </div>
      `,
      confirmButtonText: 'حسناً',
      confirmButtonColor: '#dc2626'
    })
    return
  }

  // Validate Header Data (Geographic & ID)
  if (
    !localHeaderData.birth_gov_id || !localHeaderData.birth_district_id || 
    !localHeaderData.birth_sub_district_id || !localHeaderData.birth_village_id ||
    !localHeaderData.residence_gov_id || !localHeaderData.residence_district_id || 
    !localHeaderData.residence_sub_district_id || !localHeaderData.residence_village_id ||
    !localHeaderData.id_issue_date || !localHeaderData.id_issue_place
  ) {
    Swal.fire({
      icon: 'error',
      title: 'بيانات ناقصة',
      text: 'لا يمكن تقديم الطلب إلا بعد استكمال بيانات الميلاد والإقامة والبطاقة الخاصة بالفرد.'
    })
    return
  }
  
  if (headerValidationErrors.id_issue_date) {
    Swal.fire({
      icon: 'error',
      title: 'تاريخ غير صالح',
      text: headerValidationErrors.id_issue_date
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
        if (formDataErrors[f.key]) {
          Swal.fire({
            icon: 'error',
            title: 'خطأ في التاريخ',
            text: `الحقل "${f.label}": ${formDataErrors[f.key]}`
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
  let errorMessage = ''

  let lastCorrectionId = null
  let lastFormId = null

  // Loop through all selected personnel and submit
  for (const person of selectedPersonnelList.value) {
    try {
      // Auto-Sync Personnel Geographic and ID Data
      // Only include fields with actual values to avoid overwriting existing DB data with null
      try {
        const geoPayload: Record<string, any> = {}
        if (localHeaderData.birth_gov_id)         geoPayload.birth_governorate        = localHeaderData.birth_gov_id
        if (localHeaderData.birth_district_id)    geoPayload.birth_district           = localHeaderData.birth_district_id
        if (localHeaderData.birth_sub_district_id) geoPayload.birth_sub_district      = localHeaderData.birth_sub_district_id
        if (localHeaderData.birth_village_id)     geoPayload.birth_village            = localHeaderData.birth_village_id
        if (localHeaderData.residence_gov_id)     geoPayload.residence_governorate    = localHeaderData.residence_gov_id
        if (localHeaderData.residence_district_id) geoPayload.residence_district      = localHeaderData.residence_district_id
        if (localHeaderData.residence_sub_district_id) geoPayload.residence_sub_district = localHeaderData.residence_sub_district_id
        if (localHeaderData.residence_village_id) geoPayload.residence_village        = localHeaderData.residence_village_id
        if (localHeaderData.id_issue_date)        geoPayload.id_issue_date            = localHeaderData.id_issue_date
        if (localHeaderData.id_issue_place)       geoPayload.id_issue_place           = localHeaderData.id_issue_place

        console.log('[GEO-SYNC] Payload to save:', geoPayload)
        if (Object.keys(geoPayload).length > 0) {
          await personnelStore.updatePersonnel(person.military_number, geoPayload)
        }
      } catch (syncErr) {
        console.error('Failed to sync personnel header data:', syncErr)
      }

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
    } catch (err: any) {
      console.error('Submission error for', person.military_number, err)
      const respData = err.response?.data

      // ── عرض أخطاء محرك قواعد الخدمات (Service Rules Engine) ──
      if (respData?.validation_errors && Array.isArray(respData.validation_errors) && respData.validation_errors.length > 0) {
        const errorsHtml = respData.validation_errors.map((e: any) => {
          const msg = typeof e === 'string' ? e : (e.message || '');
          const fieldTag = (typeof e === 'object' && e.field) ? `<span class="text-xs font-bold text-red-400 block mb-0.5">[${e.code || e.field}]</span>` : '';
          return `
          <div class="flex items-start gap-2 p-2 bg-red-50 border border-red-100 rounded-lg mb-2 text-right">
            <span class="text-red-500 mt-0.5 shrink-0">✗</span>
            <div>
              ${fieldTag}
              <p class="text-sm text-red-800 font-medium whitespace-pre-wrap leading-relaxed">${msg}</p>
            </div>
          </div>
          `
        }).join('')
        const warningsHtml = (respData.warnings || []).map((w: any) => `
          <div class="flex items-start gap-2 p-2 bg-amber-50 border border-amber-100 rounded-lg mb-2 text-right">
            <span class="text-amber-500 mt-0.5 shrink-0">⚠</span>
            <p class="text-sm text-amber-800">${w.message}</p>
          </div>
        `).join('')

        await Swal.fire({
          icon: 'error',
          title: respData.error || 'تعذّر تقديم الطلب',
          html: `
            <div class="text-right space-y-1 max-h-80 overflow-y-auto pr-1">
              <p class="text-xs text-gray-500 mb-3">الفرد: <b>${person.full_name}</b> — ${respData.validation_errors.length} خطأ يمنع التقديم:</p>
              ${errorsHtml}
              ${warningsHtml ? '<div class="mt-3 text-xs font-bold text-amber-600">تحذيرات:</div>' + warningsHtml : ''}
            </div>
          `,
          confirmButtonText: 'مراجعة البيانات',
          confirmButtonColor: '#dc2626',
          width: '600px',
        })
        isSubmitting.value = false
        return  // وقف العملية بالكامل لأن المحرك رفض الطلب
      }

      // ── رسائل الحالة النهائية (403 Forbidden) من الـ Backend ──
      if (err.response?.status === 403 && respData?.detail) {
        await Swal.fire({
          icon: 'error',
          title: respData.error || 'إجراء غير مسموح',
          html: `
            <div class="text-right p-2">
              <div class="flex items-center gap-3 p-3 bg-red-50 border border-red-200 rounded-xl mb-3">
                <span class="text-2xl">🚫</span>
                <div>
                  <p class="text-sm font-bold text-red-800">${respData.status_name || 'حالة خروج نهائي'}</p>
                </div>
              </div>
              <p class="text-sm text-gray-700 leading-relaxed">${respData.detail}</p>
            </div>
          `,
          confirmButtonText: 'فهمت',
          confirmButtonColor: '#dc2626',
        })
        isSubmitting.value = false
        return
      }

      // ── رسائل الخطأ العامة ──
      let msg = respData?.error || respData?.detail
      if (!msg && respData && typeof respData === 'object') {
        try {
          const extractErrors = (obj: any): string[] => {
            const errors: string[] = []
            for (const [key, val] of Object.entries(obj)) {
              if (typeof val === 'string') errors.push(`${key}: ${val}`)
              else if (Array.isArray(val)) errors.push(`${key}: ${val.join(', ')}`)
              else if (typeof val === 'object' && val !== null) Object.assign(errors, extractErrors(val))
            }
            return errors
          }
          msg = extractErrors(respData).join('<br/>') || JSON.stringify(respData)
        } catch(e) {
          msg = 'الرجاء التحقق من صحة البيانات المدخلة'
        }
      }
      errorMessage += `<div class="mb-1"><b>${person.full_name}:</b> ${msg || 'خطأ غير معروف'}</div>`
      errorCount++
    }
    submittedCount.value++
  }

  isSubmitting.value = false

  if (successCount > 0) {
    const isModel23 = type === 'name_correction' && successCount === 1;
    // فحص approval_type من السكيما ومن النتيجة الفعلية
    const approvalTypeFromSchema = schema.value?.approval_type
    const isExternalForm = (approvalTypeFromSchema === 'external') && successCount === 1;
    const showPrintButton = isModel23 || isExternalForm;
    
    // تحديد الوجهة الصحيحة بعد الإرسال
    const redirectTab = isExternalForm ? 'external' : 'internal'
    const redirectRoute = { path: '/services/transactions', query: { tab: redirectTab } }
    
    Swal.fire({
      icon: errorCount > 0 ? 'warning' : 'success',
      title: errorCount > 0 ? 'تم الإنجاز جزئياً' : 'تم تقديم الطلبات بنجاح',
      html: `تم رفع <b>${successCount}</b> طلب للمراجعة.<br/>
             ${errorCount > 0 ? `<div class="mt-3 text-xs text-right text-red-600 bg-red-50 p-3 rounded-lg border border-red-100">${errorMessage}</div>` : ''}`,
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
          const draft = {
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
          localStorage.setItem('official_memo_draft', JSON.stringify(draft))
          window.open('/admin/documents/memo-preview', '_blank')
          router.push(redirectRoute)
        } else if (isExternalForm && lastFormId) {
          // فتح منشئ المذكرات
          const person = selectedPersonnelList.value[0]
          const fType = schema.value?.name || ''
          const txNum2 = `TX-${String(lastFormId).padStart(6, '0')}`
          const dateNow2 = new Date().toLocaleDateString('ar-YE', { year: 'numeric', month: '2-digit', day: '2-digit' })
          const draft2 = {
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
          localStorage.setItem('official_memo_draft', JSON.stringify(draft2))
          window.open('/admin/documents/memo-preview', '_blank')
          router.push(redirectRoute)
        }
      } else {
        router.push(redirectRoute)
      }
    })
  } else {
    Swal.fire({
      icon: 'error',
      title: 'فشل العملية',
      html: `<div class="text-sm text-right text-red-600">${errorMessage || 'حدث خطأ أثناء محاولة تقديم الطلبات. يرجى مراجعة البيانات.'}</div>`
    })
  }
}
</script>
