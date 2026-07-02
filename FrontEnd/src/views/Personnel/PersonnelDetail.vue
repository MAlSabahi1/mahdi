<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('personnel.profile_details') || 'تفاصيل ملف الفرد'" />
    <div class="space-y-6">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center p-12">
        <svg class="h-10 w-10 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      </div>

      <!-- Error State -->
      <div v-else-if="errorMsg" class="flex flex-col items-center justify-center rounded-2xl border border-gray-200 bg-white p-12 text-center shadow-theme-sm dark:border-gray-800 dark:bg-gray-900">
        <div class="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-error-50 text-error-500 dark:bg-error-500/10">
          <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('common.error_loading') || 'خطأ في تحميل البيانات' }}</h3>
        <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">{{ errorMsg }}</p>
        <button @click="router.push('/personnel')" class="mt-6 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors">
          {{ $t('common.back_to_list') || 'العودة لقائمة الأفراد' }}
        </button>
      </div>

      <!-- Main Content -->
      <div v-else-if="person" class="space-y-6">
        
        <!-- Top Profile Card -->
        <div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-theme-sm dark:border-gray-800 dark:bg-gray-900">
          <div class="flex flex-col gap-6 md:flex-row md:items-start md:justify-between">
            <div class="flex flex-col md:flex-row items-center md:items-start gap-5 text-center md:text-start">
              <!-- Avatar Placeholder -->
              <div class="flex h-24 w-24 shrink-0 items-center justify-center rounded-full border-4 border-white bg-brand-100 text-brand-600 shadow-theme-sm dark:border-gray-800 dark:bg-brand-500/20 dark:text-brand-400">
                <span class="text-2xl font-bold">{{ person.full_name?.substring(0, 1) || '؟' }}</span>
              </div>
              
              <div class="mt-2">
                <div class="flex flex-wrap items-center justify-center md:justify-start gap-3">
                  <h1 class="text-2xl font-bold text-gray-900 dark:text-white">{{ person.full_name }}</h1>
                  <span
                    class="inline-flex items-center rounded-full px-2.5 py-1.5 text-xs font-semibold"
                    :class="getStatusColor(person.status?.classification)"
                  >
                    {{ person.status?.name || 'غير محدد' }}
                  </span>
                </div>
                
                <div class="mt-3 flex flex-wrap items-center justify-center md:justify-start gap-x-6 gap-y-4 text-sm text-gray-500 dark:text-gray-400">
                  <div class="flex items-center gap-2 rounded-lg bg-gray-50 px-3 py-1.5 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-800">
                    <svg class="h-4.5 w-4.5 text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1v1H9V7zm5 0h1v1h-1V7zm-5 4h1v1H9v-1zm5 0h1v1h-1v-1zm-5 4h1v1H9v-1zm5 0h1v1h-1v-1z" />
                    </svg>
                    <span class="font-medium text-gray-700 dark:text-gray-300">{{ person.branch_name || person.security_admin_name || $t('common.unspecified') }}</span>
                  </div>

                  <div class="flex items-center gap-2.5">
                    <div class="flex h-9 w-9 items-center justify-center rounded-full bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-400">
                      <svg class="h-4.5 w-4.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" />
                      </svg>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">{{ $t('personnel.military_number') }}</p>
                      <div class="flex items-center gap-2">
                        <p class="font-semibold text-gray-900 dark:text-white">{{ person.military_number }}</p>
                        <span v-if="person.military_number_type" class="text-[10px] bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded dark:bg-gray-800 dark:text-gray-400">
                          {{ person.military_number_type.name_ar || person.military_number_type.name }}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div class="flex items-center gap-2.5">
                    <div class="flex h-9 w-9 items-center justify-center rounded-full bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-400">
                      <svg class="h-4.5 w-4.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                      </svg>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">{{ $t('personnel.current_rank') }}</p>
                      <p class="font-semibold text-gray-900 dark:text-white">{{ person.rank?.name || $t('common.unspecified') }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Top Actions -->
            <div class="flex items-center justify-center gap-3 print-hide">
              <button @click="printProfile" class="rounded-lg border border-gray-200 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors">
                <svg class="h-4.5 w-4.5 inline-block -mt-0.5 me-1 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                </svg>
                {{ $t('common.print') || 'طباعة' }}
              </button>
              <button @click="openSettlementModal" class="flex items-center gap-2 rounded-lg border border-gray-200 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors">
                <svg class="h-4.5 w-4.5 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
                </svg>
                {{ $t('settlements.request_settlement') || 'تقديم طلب تسوية' }}
              </button>
              <button @click="router.push('/personnel')" class="rounded-lg border border-gray-200 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors">
                {{ $t('common.back_to_list') || 'رجوع للقائمة' }}
              </button>
              <button @click="router.push(`/personnel/${person.military_number}/edit`)" class="flex items-center gap-2 rounded-lg bg-gray-900 px-4 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-gray-800 dark:bg-white dark:text-gray-900 dark:hover:bg-gray-100 transition-colors">
                <svg class="h-4.5 w-4.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                </svg>
                {{ $t('personnel.edit_profile') }}
              </button>
            </div>
          </div>

          <!-- Quality Score Progress -->
          <div class="mt-6 border-t border-gray-100 pt-5 dark:border-gray-800">
            <div class="flex items-center justify-between text-sm mb-2">
              <span class="font-medium text-gray-700 dark:text-gray-300">{{ $t('personnel.data_quality') }}</span>
              <span class="font-bold" :class="getQualityScoreTextColor(person.data_quality_score)">
                {{ person.data_quality_score }}%
              </span>
            </div>
            <div class="w-full bg-gray-100 rounded-full h-2 dark:bg-gray-800">
              <div 
                class="h-2 rounded-full transition-all duration-1000" 
                :class="getQualityScoreColor(person.data_quality_score)"
                :style="{ width: `${person.data_quality_score}%` }"
              ></div>
            </div>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="border-b border-gray-200 dark:border-gray-800 print-hide">
          <nav class="-mb-px flex space-x-6 rtl:space-x-reverse overflow-x-auto">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              class="whitespace-nowrap border-b-2 py-3 px-1 text-sm font-medium transition-colors"
              :class="[
                activeTab === tab.id
                  ? 'border-brand-500 text-brand-600 dark:text-brand-400'
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
              ]"
            >
              {{ tab.name }}
              <span v-if="tab.badge !== undefined" class="ms-2 rounded-full px-2 py-0.5 text-xs"
                :class="activeTab === tab.id ? 'bg-brand-100 text-brand-600 dark:bg-brand-500/20' : 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'">
                {{ tab.badge }}
              </span>
            </button>
          </nav>
        </div>

        <!-- Tab 1: Basic Info -->
        <div v-if="activeTab === 'basic'" class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-theme-sm dark:border-gray-800 dark:bg-gray-900">
            <h3 class="text-base font-bold text-gray-900 dark:text-white mb-4">{{ $t('personnel.tabs.basic_info') }}</h3>
            <dl class="divide-y divide-gray-100 dark:divide-gray-800 text-sm">
              <div class="flex justify-between py-3">
                <dt class="text-gray-500 dark:text-gray-400">{{ $t('personnel.national_id') }}</dt>
                <dd class="font-medium text-gray-900 dark:text-white flex items-center gap-2">
                  <span>{{ person.national_id || ($t('common.unspecified') || 'غير متوفر') }}</span>
                  <span v-if="person.national_id_status_display" class="text-xs px-2 py-0.5 rounded-full" :class="person.national_id_status === 'verified' ? 'bg-success-50 text-success-600 dark:bg-success-500/10' : 'bg-warning-50 text-warning-600 dark:bg-warning-500/10'">
                    {{ person.national_id_status_display }}
                  </span>
                </dd>
              </div>
              <div class="flex justify-between py-3">
                <dt class="text-gray-500 dark:text-gray-400">{{ $t('personnel.details.age') }}</dt>
                <dd class="font-medium text-gray-900 dark:text-white">{{ person.age ? `${person.age} ${$t('common.years') || 'سنة'}` : ($t('common.unspecified') || 'غير متوفر') }}</dd>
              </div>
              <div class="flex justify-between py-3">
                <dt class="text-gray-500 dark:text-gray-400">{{ $t('personnel.birth_date') }}</dt>
                <dd class="font-medium text-gray-900 dark:text-white">{{ person.birth_date || ($t('common.unspecified') || 'غير متوفر') }}</dd>
              </div>
              <div class="flex justify-between py-3">
                <dt class="text-gray-500 dark:text-gray-400">{{ $t('personnel.phone') }}</dt>
                <dd class="font-medium text-gray-900 dark:text-white">{{ person.phone_number || ($t('common.unspecified') || 'غير متوفر') }}</dd>
              </div>
              <div class="flex justify-between py-3">
                <dt class="text-gray-500 dark:text-gray-400">{{ $t('personnel.governorate') }}</dt>
                <dd class="font-medium text-gray-900 dark:text-white">{{ person.geo_location_name || ($t('common.unspecified') || 'غير متوفر') }}</dd>
              </div>
              <div class="flex justify-between py-3">
                <dt class="text-gray-500 dark:text-gray-400">{{ $t('personnel.qualification') }}</dt>
                <dd class="font-medium text-gray-900 dark:text-white">{{ person.qualification_detail?.name || ($t('common.unspecified') || 'غير متوفر') }}</dd>
              </div>
            </dl>
          </div>

          <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-theme-sm dark:border-gray-800 dark:bg-gray-900">
            <h3 class="text-base font-bold text-gray-900 dark:text-white mb-4">{{ $t('personnel.org_job_section') }}</h3>
            <dl class="divide-y divide-gray-100 dark:divide-gray-800 text-sm">
              <div class="flex justify-between py-3">
                <dt class="text-gray-500 dark:text-gray-400">{{ $t('personnel.details.workplace') }}</dt>
                <dd class="font-medium text-gray-900 dark:text-white">{{ person.branch_name || person.security_admin_name || ($t('personnel.unspecified') || 'غير محدد') }}</dd>
              </div>
              <div class="flex justify-between py-3">
                <dt class="text-gray-500 dark:text-gray-400">{{ $t('personnel.details.department') }}</dt>
                <dd class="font-medium text-gray-900 dark:text-white">{{ person.division_name || person.unit_name || ($t('personnel.unspecified') || 'غير محدد') }}</dd>
              </div>
              <div class="flex justify-between py-3">
                <dt class="text-gray-500 dark:text-gray-400">{{ $t('personnel.job_title') }}</dt>
                <dd class="font-medium text-gray-900 dark:text-white">{{ person.job_title_name || ($t('personnel.unspecified') || 'غير محدد') }}</dd>
              </div>
              <div class="flex justify-between py-3">
                <dt class="text-gray-500 dark:text-gray-400">{{ $t('personnel.position') }}</dt>
                <dd class="font-medium text-gray-900 dark:text-white">{{ person.position_name || ($t('personnel.unspecified') || 'غير محدد') }}</dd>
              </div>
              <div class="flex justify-between py-3">
                <dt class="text-gray-500 dark:text-gray-400">{{ $t('personnel.details.service_years') }}</dt>
                <dd class="font-medium text-gray-900 dark:text-white">{{ person.service_years !== null ? `${person.service_years} ${$t('common.years') || 'سنة'}` : ($t('common.unspecified') || 'غير متوفر') }}</dd>
              </div>
              <div class="flex justify-between py-3">
                <dt class="text-gray-500 dark:text-gray-400">{{ $t('personnel.join_date') }}</dt>
                <dd class="font-medium text-gray-900 dark:text-white">{{ person.join_date || ($t('common.unspecified') || 'غير متوفر') }}</dd>
              </div>
            </dl>
          </div>
          
          <!-- Notes Block -->
          <div v-if="person.notes" class="md:col-span-2 rounded-2xl border border-gray-200 bg-white p-5 shadow-theme-sm dark:border-gray-800 dark:bg-gray-900">
            <h3 class="text-sm font-bold text-gray-900 dark:text-white mb-2">{{ $t('personnel.notes') }}</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">{{ person.notes }}</p>
          </div>
        </div>

        <!-- Tab 2: Recent Events (Timeline) -->
        <div v-if="activeTab === 'events'" class="rounded-2xl border border-gray-200 bg-white p-5 shadow-theme-sm dark:border-gray-800 dark:bg-gray-900">
          <div v-if="person.recent_events && person.recent_events.length > 0" class="relative ms-4 border-s-2 border-gray-200 dark:border-gray-800">
            <div v-for="event in person.recent_events" :key="event.id" class="mb-8 ms-6 last:mb-0">
              <span class="absolute -start-3 flex h-6 w-6 items-center justify-center rounded-full bg-white ring-4 ring-white dark:bg-gray-900 dark:ring-gray-900">
                <div class="h-2 w-2 rounded-full bg-brand-500"></div>
              </span>
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-1">
                <h3 class="text-base font-bold text-gray-900 dark:text-white">{{ event.event_type_display }}</h3>
                <time class="mb-1 text-sm font-normal text-gray-400 sm:mb-0">{{ new Date(event.event_date).toLocaleDateString('ar-SA') }}</time>
              </div>
              <p class="text-sm font-normal text-gray-500 dark:text-gray-400 mt-2">{{ event.description || ($t('personnel.details.no_event_desc') || 'لا يوجد وصف متاح لهذا الحدث.') }}</p>
            </div>
          </div>
          <div v-else class="text-center py-10">
            <p class="text-gray-500 dark:text-gray-400 text-sm">{{ $t('personnel.details.no_events') }}</p>
          </div>
        </div>

        <!-- Tab 3: Documents -->
        <div v-if="activeTab === 'docs'">
          <DocumentsTab :person="person" />
        </div>

        <!-- Tab 4: Corrections -->
        <div v-if="activeTab === 'corrections'">
          <CorrectionTab :person="person" />
        </div>

      </div>
    </div>

    <!-- Rank Settlement Modal -->
    <div v-if="showSettlementModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 print-hide">
      <div class="absolute inset-0 bg-gray-900/50 transition-opacity dark:bg-gray-900/80" @click="showSettlementModal = false"></div>
      <div class="relative w-full max-w-2xl transform overflow-hidden rounded-2xl bg-white p-6 text-start align-middle shadow-xl transition-all dark:bg-gray-900 border border-gray-100 dark:border-gray-800 max-h-[90vh] flex flex-col">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-5 border-b border-gray-100 dark:border-gray-800 pb-3">
          {{ $t('settlements.request_settlement') || 'تقديم طلب تسوية' }}
        </h3>
        
        <div class="overflow-y-auto flex-1 pe-2">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div class="md:col-span-2">
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('settlements.settlement_type') }} <span class="text-error-500">*</span></label>
              <select v-model="settlementForm.settlement_type" v-field-error="'settlement_type'" required class="w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white">
                <option value="same_class_promotion">{{ $t('settlements.types.same_class_promotion') }}</option>
                <option value="personnel_to_officer">{{ $t('settlements.types.personnel_to_officer') }}</option>
                <option value="demotion">{{ $t('settlements.types.demotion') }}</option>
              </select>
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('settlements.from_rank') }}</label>
              <input :value="person.rank?.name" disabled type="text" class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-500 cursor-not-allowed dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400" />
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('settlements.to_rank') }} <span class="text-error-500">*</span></label>
              <select v-model="settlementForm.to_rank" v-field-error="'to_rank'" required class="w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white">
                <option :value="null">...</option>
                <option v-for="r in coreStore.ranks" :key="r.id" :value="r.id">{{ r.name }}</option>
              </select>
            </div>

            <div v-if="settlementForm.settlement_type === 'personnel_to_officer'" class="md:col-span-2">
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('settlements.new_military_number') }} <span class="text-error-500">*</span></label>
              <input v-model="settlementForm.new_military_number" v-field-error="'new_military_number'" type="text" required placeholder="مثال: 60..." class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white" />
              <p class="mt-1 text-xs text-brand-600 dark:text-brand-400">{{ $t('settlements.new_mil_hint') }}</p>
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('settlements.decision_number') }}</label>
              <input v-model="settlementForm.decision_number" type="text" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white" />
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('settlements.decision_date') }}</label>
              <input v-model="settlementForm.decision_date" type="date" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white" />
            </div>

            <div class="md:col-span-2">
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
                {{ $t('settlements.supporting_document') || 'المستند الداعم' }} <span class="text-error-500">*</span>
              </label>
              <select v-model="settlementForm.supporting_document" v-field-error="'supporting_document'" required class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white">
                <option :value="null">...</option>
                <option v-for="doc in person?.documents" :key="doc.id" :value="doc.id">
                  {{ doc.document_type_display || doc.document_type }} - {{ doc.original_filename || doc.file_name || 'مستند' }}
                </option>
              </select>
              <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">يجب رفع المستند أولاً من تبويب (المرفقات) قبل اختياره هنا.</p>
            </div>

            <div class="md:col-span-2">
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.notes') }}</label>
              <textarea v-model="settlementForm.notes" rows="2" class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"></textarea>
            </div>
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-3 border-t border-gray-100 dark:border-gray-800 pt-4">
          <button @click="showSettlementModal = false" class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors">
            إلغاء
          </button>
          <button @click="submitSettlement" :disabled="settlementLoading" class="rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-brand-700 transition-colors disabled:opacity-50 flex items-center gap-2">
            <svg v-if="settlementLoading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            تقديم الطلب
          </button>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { usePersonnelStore } from '@/stores/personnel'
import { useRankSettlementStore } from '@/stores/rankSettlement'
import { useCoreStore } from '@/stores/core'
import { validateFormFields } from '@/stores/validation'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import Swal from 'sweetalert2'

const route = useRoute()
const router = useRouter()
const personnelStore = usePersonnelStore()
const settlementStore = useRankSettlementStore()
const coreStore = useCoreStore()

const { t } = useI18n()

function printProfile() {
  window.print()
}

import CorrectionTab from './components/CorrectionTab.vue'
import DocumentsTab from './components/DocumentsTab.vue'

const loading = ref(true)
const errorMsg = ref('')
const person = ref<any>(null)

const activeTab = ref('basic')

const tabs = computed(() => [
  { id: 'basic', name: t('personnel.tabs.basic_info') || 'البيانات الشخصية' },
  { id: 'events', name: t('personnel.tabs.events') || 'السجل التاريخي', badge: person.value?.recent_events?.length || 0 },
  { id: 'docs', name: t('personnel.tabs.documents') || 'المرفقات', badge: person.value?.documents?.length || 0 },
  { id: 'corrections', name: t('personnel.tabs.corrections') || 'تصحيح البيانات', badge: person.value?.pending_corrections?.length || 0 },
])

async function loadPersonnelDetail() {
  const militaryNumber = route.params.id as string
  if (!militaryNumber) {
    errorMsg.value = 'الرقم العسكري غير متوفر.'
    loading.value = false
    return
  }

  try {
    const data = await personnelStore.getPersonnelById(militaryNumber)
    person.value = data
  } catch (err: any) {
    errorMsg.value = err.response?.data?.error || 'حدث خطأ أثناء محاولة جلب بيانات الفرد.'
  } finally {
    loading.value = false
  }
}

// Helpers for UI styling
function getStatusColor(classification: string | undefined) {
  switch (classification) {
    case 'active': return 'bg-success-50 text-success-700 dark:bg-success-500/10 dark:text-success-400'
    case 'leave': return 'bg-warning-50 text-warning-700 dark:bg-warning-500/10 dark:text-warning-400'
    case 'absent': return 'bg-error-50 text-error-700 dark:bg-error-500/10 dark:text-error-400'
    case 'inactive': return 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400'
    default: return 'bg-brand-50 text-brand-700 dark:bg-brand-500/10 dark:text-brand-400'
  }
}

function getQualityScoreColor(score: number | undefined) {
  if (score === undefined) return 'bg-gray-300'
  if (score >= 80) return 'bg-success-500'
  if (score >= 50) return 'bg-warning-500'
  return 'bg-error-500'
}

function getQualityScoreTextColor(score: number | undefined) {
  if (score === undefined) return 'text-gray-500'
  if (score >= 80) return 'text-success-600 dark:text-success-400'
  if (score >= 50) return 'text-warning-600 dark:text-warning-400'
  return 'text-error-600 dark:text-error-400'
}

onMounted(async () => {
  if (coreStore.ranks.length === 0) {
    coreStore.fetchAllReferences()
  }
  loadPersonnelDetail()
})

// Settlement Modal Logic
const showSettlementModal = ref(false)
const settlementLoading = ref(false)
const settlementForm = ref({
  settlement_type: 'same_class_promotion',
  to_rank: null,
  new_military_number: '',
  decision_number: '',
  decision_date: '',
  supporting_document: null,
  notes: ''
})

function openSettlementModal() {
  settlementForm.value = {
    settlement_type: 'same_class_promotion',
    to_rank: null,
    new_military_number: '',
    decision_number: '',
    decision_date: '',
    supporting_document: null,
    notes: ''
  }
  showSettlementModal.value = true
}

async function submitSettlement() {
  if (!validateFormFields()) return

  if (settlementForm.value.settlement_type === 'personnel_to_officer' && !settlementForm.value.new_military_number) {
    Swal.fire({ toast: true, position: 'top-end', icon: 'error', title: 'يجب إدخال الرقم العسكري الجديد للترقية لضابط', showConfirmButton: false, timer: 3000 })
    return
  }

  settlementLoading.value = true
  try {
    const payload = {
      ...settlementForm.value,
      personnel: person.value.military_number,
      from_rank: person.value.rank?.id,
      new_military_number: settlementForm.value.settlement_type === 'personnel_to_officer' ? settlementForm.value.new_military_number : null
    }

    await settlementStore.createSettlement(payload)
    Swal.fire({
      toast: true, position: 'top-end',
      icon: 'success', title: 'تم تقديم طلب تسوية الرتبة بنجاح',
      showConfirmButton: false, timer: 3000
    })
    showSettlementModal.value = false
  } catch (err: any) {
    // Handled globally
  } finally {
    settlementLoading.value = false
  }
}
</script>

<style scoped>
@media print {
  .print-hide {
    display: none !important;
  }
}
</style>
