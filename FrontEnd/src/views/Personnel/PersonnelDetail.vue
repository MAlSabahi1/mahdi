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
        <div class="relative overflow-hidden rounded-[24px] bg-white ring-1 ring-inset ring-gray-200 shadow-sm dark:bg-gray-900 dark:ring-gray-800">
          
          <div class="p-6 md:p-8">
            <div class="flex flex-col xl:flex-row xl:items-center justify-between gap-8">
              
              <!-- Left Side: Identity & Meta -->
              <div class="flex flex-col md:flex-row items-center md:items-start gap-6 w-full xl:w-auto">
                
                <!-- Avatar: Soft & Elegant -->
                <div class="relative flex h-20 w-20 sm:h-24 sm:w-24 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-50 to-brand-100/50 text-brand-600 dark:from-gray-800 dark:to-gray-800/50 dark:text-brand-400 ring-1 ring-inset ring-brand-100/50 dark:ring-gray-700 shadow-inner">
                  <span class="text-3xl sm:text-4xl font-bold tracking-tighter">{{ person.full_name?.substring(0, 1) || '؟' }}</span>
                </div>

                <!-- Core Information -->
                <div class="flex flex-col items-center md:items-start text-center md:text-start flex-1 min-w-0">
                  
                  <!-- Name & Tags -->
                  <div class="mb-4 flex flex-col md:flex-row items-center md:items-center gap-3">
                    <h1 class="text-2xl sm:text-[28px] font-bold text-gray-900 dark:text-white leading-tight tracking-tight truncate max-w-xl">
                      {{ person.full_name }}
                    </h1>
                    <div class="flex items-center gap-2 mt-1 md:mt-0">
                      <!-- Status Badge -->
                      <span class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-bold uppercase tracking-wide bg-gray-50 text-gray-700 dark:bg-gray-800 dark:text-gray-300 ring-1 ring-inset ring-gray-200 dark:ring-gray-700">
                        <span class="h-1.5 w-1.5 rounded-full" :class="getStatusColor(person.status?.classification).split(' ')[0]"></span>
                        {{ person.status?.name || $t('personnel.unspecified') || 'غير محدد' }}
                      </span>
                      <!-- Rank Badge -->
                      <span v-if="person.rank?.name" class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-bold uppercase tracking-wide bg-gray-50 text-gray-700 dark:bg-gray-800 dark:text-gray-300 ring-1 ring-inset ring-gray-200 dark:ring-gray-700">
                        <svg class="h-3.5 w-3.5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                        </svg>
                        {{ person.rank.name }}
                      </span>
                    </div>
                  </div>

                  <!-- Data Row -->
                  <div class="flex flex-wrap items-center justify-center md:justify-start gap-x-8 gap-y-4">
                    <!-- Data Block 1 -->
                    <div class="flex flex-col items-center md:items-start">
                      <dt class="text-[11px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-1.5">{{ $t('personnel.military_number') }}</dt>
                      <dd class="flex items-center gap-2 text-sm font-semibold text-gray-900 dark:text-gray-100">
                        <svg class="h-4 w-4 text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" />
                        </svg>
                        {{ person.military_number }}
                      </dd>
                    </div>

                    <div class="hidden md:block h-8 w-px bg-gray-200 dark:bg-gray-800"></div>

                    <!-- Data Block 2 -->
                    <div class="flex flex-col items-center md:items-start">
                      <dt class="text-[11px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-1.5">{{ $t('personnel.details.workplace') }}</dt>
                      <dd class="flex items-center gap-2 text-sm font-semibold text-gray-900 dark:text-gray-100">
                        <svg class="h-4 w-4 text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1v1H9V7zm5 0h1v1h-1V7zm-5 4h1v1H9v-1zm5 0h1v1h-1v-1zm-5 4h1v1H9v-1zm5 0h1v1h-1v-1z" />
                        </svg>
                        <span class="truncate max-w-xs xl:max-w-md">{{ person.branch_name || person.security_admin_name || $t('common.unspecified') }}</span>
                      </dd>
                    </div>
                  </div>

                </div>
              </div>

              <!-- Right Side: Actions -->
              <div class="flex flex-wrap items-center justify-center xl:justify-end gap-3 w-full xl:w-auto print-hide mt-2 xl:mt-0 pt-6 xl:pt-0 border-t border-gray-100 dark:border-gray-800 xl:border-0">
                <button @click="printProfile" class="flex items-center justify-center rounded-lg border border-gray-200 bg-white h-10 w-10 text-gray-500 shadow-theme-xs hover:bg-gray-50 hover:text-gray-700 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-300 transition-colors" title="طباعة">
                  <svg class="h-4.5 w-4.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                  </svg>
                </button>
                <button @click="openSettlementModal" class="flex items-center gap-2 rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors">
                  <svg class="h-4 w-4 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
                  </svg>
                  {{ $t('settlements.request_settlement') || 'تسوية' }}
                </button>
                <button @click="router.push(`/personnel/${person.military_number}/edit`)" class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors">
                  <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                  {{ $t('personnel.edit_profile') }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="print-hide mt-8">
          <div class="flex items-center gap-2 overflow-x-auto rounded-xl bg-gray-50/50 p-1.5 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-800/60 shadow-theme-xs">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              class="relative flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-bold transition-all duration-300 ease-out whitespace-nowrap"
              :class="[
                activeTab === tab.id
                  ? 'bg-white text-brand-600 shadow-theme-xs ring-1 ring-gray-900/5 dark:bg-gray-700 dark:text-brand-400 dark:ring-white/10'
                  : 'text-gray-500 hover:bg-white/60 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-800/60 dark:hover:text-gray-300'
              ]"
            >
              <!-- Icons -->
              <svg v-if="tab.id === 'basic'" class="h-5 w-5" :class="activeTab === tab.id ? 'text-brand-600 dark:text-brand-400' : 'text-gray-400'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
              <svg v-else-if="tab.id === 'events'" class="h-5 w-5" :class="activeTab === tab.id ? 'text-brand-600 dark:text-brand-400' : 'text-gray-400'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              <svg v-else-if="tab.id === 'docs'" class="h-5 w-5" :class="activeTab === tab.id ? 'text-brand-600 dark:text-brand-400' : 'text-gray-400'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
              <svg v-else-if="tab.id === 'corrections'" class="h-5 w-5" :class="activeTab === tab.id ? 'text-brand-600 dark:text-brand-400' : 'text-gray-400'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
              
              <span>{{ tab.id === 'basic' ? ($t('personnel.tabs.basic_info') || 'التفاصيل الشاملة') : tab.name }}</span>
              
              <span v-if="tab.badge !== undefined && tab.id !== 'basic'" 
                class="ms-1.5 flex h-5 min-w-[20px] items-center justify-center rounded-full px-1.5 text-[10px] font-bold"
                :class="activeTab === tab.id ? 'bg-brand-100 text-brand-700 dark:bg-brand-500/20 dark:text-brand-400' : 'bg-gray-200 text-gray-600 dark:bg-gray-700 dark:text-gray-300'">
                {{ tab.badge }}
              </span>
            </button>
          </div>
        </div>

        <!-- Tab Content -->
        <div class="mt-6">
          
          <!-- Tab 1: Comprehensive Details -->
          <div v-if="activeTab === 'basic'" class="space-y-6 animate-in fade-in duration-500">
            
            <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
              <!-- Card 1: Personal Information -->
              <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden flex flex-col">
                <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-800 flex items-center gap-3 bg-gray-50/50 dark:bg-gray-800/20">
                  <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-400">
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
                  </div>
                  <h3 class="text-base font-bold text-gray-900 dark:text-white">{{ $t('personnel.tabs.basic_info') || 'البيانات الشخصية' }}</h3>
                  <div class="ms-auto flex items-center gap-2" title="جودة البيانات">
                    <div class="h-1.5 w-16 bg-gray-200 rounded-full overflow-hidden dark:bg-gray-700">
                      <div class="h-full rounded-full transition-all duration-1000" :class="getQualityScoreColor(person.data_quality_score)" :style="{ width: `${person.data_quality_score}%` }"></div>
                    </div>
                    <span class="text-xs font-bold" :class="getQualityScoreTextColor(person.data_quality_score)">{{ person.data_quality_score }}%</span>
                  </div>
                </div>
                <div class="p-6 grid grid-cols-1 sm:grid-cols-2 gap-y-6 gap-x-8 flex-1">
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.national_id') || 'الرقم الوطني' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white flex items-center gap-2">
                      {{ person.national_id || 'غير متوفر' }}
                      <span v-if="person.national_id_status_display" class="text-[10px] px-2 py-0.5 rounded-md font-bold" :class="person.national_id_status === 'verified' ? 'bg-success-50 text-success-600 dark:bg-success-500/10' : 'bg-warning-50 text-warning-600 dark:bg-warning-500/10'">
                        {{ person.national_id_status_display }}
                      </span>
                    </dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.birth_date') || 'تاريخ الميلاد' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">
                      {{ person.birth_date ? new Date(person.birth_date).toLocaleDateString('ar-SA') : 'غير متوفر' }}
                    </dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.phone_number') || 'رقم الهاتف' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white flex items-center gap-2">
                      <span dir="ltr">{{ person.phone_number || 'غير متوفر' }}</span>
                    </dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.qualification') || 'المؤهل العلمي' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">
                      {{ person.qualification_name || 'غير متوفر' }}
                    </dd>
                  </div>
                </div>
              </div>

              <!-- Card 2: Military & Job Information -->
              <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden flex flex-col">
                <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-800 flex items-center gap-3 bg-gray-50/50 dark:bg-gray-800/20">
                  <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600 dark:bg-indigo-500/10 dark:text-indigo-400">
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
                  </div>
                  <h3 class="text-base font-bold text-gray-900 dark:text-white">{{ $t('personnel.military_info') || 'البيانات العسكرية والوظيفية' }}</h3>
                </div>
                <div class="p-6 grid grid-cols-1 sm:grid-cols-2 gap-y-6 gap-x-8 flex-1">
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.military_number') || 'الرقم العسكري' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">{{ person.military_number || 'غير متوفر' }}</dd>
                  </div>
                  <div v-if="person.old_military_number">
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.old_military_number') || 'الرقم العسكري القديم' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">{{ person.old_military_number }}</dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.rank') || 'الرتبة' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">
                      {{ person.rank?.name || person.rank_name || $t('personnel.unspecified') || 'غير متوفر' }}
                      <span v-if="person.pending_rank_name" class="ms-2 text-xs text-warning-600 dark:text-warning-400">({{ $t('personnel.pending_promotion') || 'معلق:' }} {{ person.pending_rank_name }})</span>
                    </dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.force_classification') || 'تصنيف القوة' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">{{ person.force_classification_name || $t('personnel.unspecified') || 'غير متوفر' }}</dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.category') || 'الفئة' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">{{ person.category_name || $t('personnel.unspecified') || 'غير متوفر' }}</dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.job_title') || 'المسمى الوظيفي' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">{{ person.job_title_name || $t('personnel.unspecified') || 'غير متوفر' }}</dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.position') || 'المنصب' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">{{ person.position_name || $t('personnel.unspecified') || 'غير متوفر' }}</dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.join_date') || 'تاريخ الالتحاق' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">{{ person.join_date ? new Date(person.join_date).toLocaleDateString('ar-SA') : ($t('personnel.unspecified') || 'غير متوفر') }}</dd>
                  </div>
                </div>
              </div>

              <!-- Card 3: Assignment & Workplace -->
              <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden flex flex-col">
                <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-800 flex items-center gap-3 bg-gray-50/50 dark:bg-gray-800/20">
                  <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-teal-50 text-teal-600 dark:bg-teal-500/10 dark:text-teal-400">
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1v1H9V7zm5 0h1v1h-1V7zm-5 4h1v1H9v-1zm5 0h1v1h-1v-1zm-5 4h1v1H9v-1zm5 0h1v1h-1v-1z" /></svg>
                  </div>
                  <h3 class="text-base font-bold text-gray-900 dark:text-white">{{ $t('personnel.workplace') || 'جهة العمل' }}</h3>
                </div>
                <div class="p-6 grid grid-cols-1 sm:grid-cols-2 gap-y-6 gap-x-8 flex-1">
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.security_admin') || 'الإدارة الأمنية' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">{{ person.security_admin_name || $t('personnel.unspecified') || 'غير متوفر' }}</dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.central_department') || 'الإدارة المركزية' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">{{ person.central_department_name || $t('personnel.unspecified') || 'غير متوفر' }}</dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.branch') || 'الفرع' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">{{ person.branch_name || $t('personnel.unspecified') || 'غير متوفر' }}</dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.district_police') || 'شرطة المحافظة/المديرية' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">{{ person.district_police_name || $t('personnel.unspecified') || 'غير متوفر' }}</dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.division') || 'القسم' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">{{ person.division_name || $t('personnel.unspecified') || 'غير متوفر' }}</dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.unit') || 'الوحدة' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">{{ person.unit_name || $t('personnel.unspecified') || 'غير متوفر' }}</dd>
                  </div>
                </div>
              </div>

              <!-- Card 4: Additional Info -->
              <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden flex flex-col">
                <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-800 flex items-center gap-3 bg-gray-50/50 dark:bg-gray-800/20">
                  <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-amber-600 dark:bg-amber-500/10 dark:text-amber-400">
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  </div>
                  <h3 class="text-base font-bold text-gray-900 dark:text-white">{{ $t('personnel.additional_info') || 'معلومات إضافية' }}</h3>
                </div>
                <div class="p-6 grid grid-cols-1 sm:grid-cols-2 gap-y-6 gap-x-8 flex-1">
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.status') || 'الحالة الحالية' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">
                      <span class="inline-flex items-center rounded-full px-2 py-1 text-xs font-medium" :class="getStatusColor(person.status?.classification || person.status_classification)">
                        {{ person.status?.name || person.status_name || $t('personnel.unspecified') || 'غير محدد' }}
                      </span>
                    </dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.expense_status') || 'حالة النفقات' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">
                      {{ person.expense_status_display || 'غير متوفر' }}
                    </dd>
                  </div>
                  <div class="sm:col-span-2">
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.appointment_info') || 'معلومات التعيين' }}</dt>
                    <dd class="text-sm font-bold text-gray-900 dark:text-white">{{ person.appointment_info || $t('personnel.unspecified') || 'لا يوجد' }}</dd>
                  </div>
                  <div class="sm:col-span-2">
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ $t('personnel.notes') || 'ملاحظات' }}</dt>
                    <dd class="text-sm text-gray-700 dark:text-gray-300">{{ person.notes || $t('personnel.unspecified') || 'لا يوجد ملاحظات' }}</dd>
                  </div>
                </div>
              </div>

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
  </div>

    <!-- Rank Settlement Modal -->
    <div v-if="showSettlementModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 print-hide">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity dark:bg-gray-900/80" @click="showSettlementModal = false"></div>
      
      <!-- Modal Panel -->
      <div class="relative w-full max-w-2xl transform overflow-hidden rounded-2xl bg-white text-start shadow-theme-xl transition-all dark:bg-gray-900 border border-gray-100 dark:border-gray-800 flex flex-col max-h-[90vh]">
        
        <!-- Header -->
        <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-800/20 flex items-center justify-between">
          <h3 class="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <svg class="h-5 w-5 text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
            {{ $t('settlements.request_settlement') || 'تقديم طلب تسوية' }}
          </h3>
          <button @click="showSettlementModal = false" class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 transition-colors">
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        
        <!-- Body -->
        <div class="overflow-y-auto flex-1 p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-5">
            <div class="md:col-span-2">
              <label class="mb-1.5 block text-sm font-bold text-gray-700 dark:text-gray-300">{{ $t('settlements.settlement_type') }} <span class="text-error-500">*</span></label>
              <select v-model="settlementForm.settlement_type" v-field-error="'settlement_type'" required class="w-full rounded-xl border border-gray-300 bg-gray-50/50 px-4 py-3 text-sm text-gray-900 transition-colors focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-500/20 dark:border-gray-700 dark:bg-gray-800/50 dark:text-white dark:focus:bg-gray-800">
                <option value="same_class_promotion">{{ $t('settlements.types.same_class_promotion') }}</option>
                <option value="personnel_to_officer">{{ $t('settlements.types.personnel_to_officer') }}</option>
                <option value="demotion">{{ $t('settlements.types.demotion') }}</option>
              </select>
            </div>

            <div class="bg-gray-50/50 dark:bg-gray-800/20 p-4 rounded-xl border border-gray-100 dark:border-gray-800/60 flex flex-col justify-center">
              <label class="mb-1 block text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">{{ $t('settlements.from_rank') }}</label>
              <div class="text-sm font-bold text-gray-900 dark:text-white">{{ person.rank?.name || person.rank_name || 'غير متوفر' }}</div>
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-bold text-gray-700 dark:text-gray-300">{{ $t('settlements.to_rank') }} <span class="text-error-500">*</span></label>
              <select v-model="settlementForm.to_rank" v-field-error="'to_rank'" required class="w-full rounded-xl border border-gray-300 bg-gray-50/50 px-4 py-3 text-sm text-gray-900 transition-colors focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-500/20 dark:border-gray-700 dark:bg-gray-800/50 dark:text-white dark:focus:bg-gray-800">
                <option :value="null">{{ $t('personnel.unspecified') || 'اختيار الرتبة...' }}</option>
                <option v-for="r in coreStore.ranks" :key="r.id" :value="r.id">{{ r.name }}</option>
              </select>
            </div>

            <div v-if="settlementForm.settlement_type === 'personnel_to_officer'" class="md:col-span-2">
              <label class="mb-1.5 block text-sm font-bold text-gray-700 dark:text-gray-300">{{ $t('settlements.new_military_number') }} <span class="text-error-500">*</span></label>
              <input v-model="settlementForm.new_military_number" v-field-error="'new_military_number'" type="text" required placeholder="مثال: 60..." class="w-full rounded-xl border border-gray-300 bg-gray-50/50 px-4 py-3 text-sm text-gray-900 transition-colors focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-500/20 dark:border-gray-700 dark:bg-gray-800/50 dark:text-white dark:focus:bg-gray-800" />
              <p class="mt-1.5 text-xs text-brand-600 dark:text-brand-400 flex items-center gap-1">
                <svg class="h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                {{ $t('settlements.new_mil_hint') }}
              </p>
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-bold text-gray-700 dark:text-gray-300">
                {{ $t('settlements.decision_number') }} <span class="text-error-500">*</span>
              </label>
              <input v-model="settlementForm.decision_number" v-field-error="'decision_number'" required type="text" class="w-full rounded-xl border border-gray-300 bg-gray-50/50 px-4 py-3 text-sm text-gray-900 transition-colors focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-500/20 dark:border-gray-700 dark:bg-gray-800/50 dark:text-white dark:focus:bg-gray-800" />
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-bold text-gray-700 dark:text-gray-300">
                {{ $t('settlements.decision_date') }} <span class="text-error-500">*</span>
              </label>
              <input v-model="settlementForm.decision_date" v-field-error="'decision_date'" required type="date" class="w-full rounded-xl border border-gray-300 bg-gray-50/50 px-4 py-3 text-sm text-gray-900 transition-colors focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-500/20 dark:border-gray-700 dark:bg-gray-800/50 dark:text-white dark:focus:bg-gray-800" />
            </div>

            <div class="md:col-span-2">
              <label class="mb-1.5 block text-sm font-bold text-gray-700 dark:text-gray-300">
                {{ $t('settlements.supporting_document') || 'المستند الداعم' }} <span class="text-error-500">*</span>
              </label>
              <select v-model="settlementForm.supporting_document" v-field-error="'supporting_document'" required class="w-full rounded-xl border border-gray-300 bg-gray-50/50 px-4 py-3 text-sm text-gray-900 transition-colors focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-500/20 dark:border-gray-700 dark:bg-gray-800/50 dark:text-white dark:focus:bg-gray-800">
                <option :value="null">{{ $t('personnel.unspecified') || 'اختيار المستند...' }}</option>
                <option v-for="doc in person?.documents" :key="doc.id" :value="doc.id">
                  {{ doc.document_type_display || doc.document_type }} - {{ doc.original_filename || doc.file_name || 'مستند' }}
                </option>
              </select>
              <p class="mt-1.5 text-xs text-gray-500 dark:text-gray-400">{{ $t?.('settlements.upload_doc_first') }}</p>
            </div>

            <div class="md:col-span-2">
              <label class="mb-1.5 block text-sm font-bold text-gray-700 dark:text-gray-300">{{ $t('personnel.notes') }}</label>
              <textarea v-model="settlementForm.notes" rows="2" placeholder="ملاحظات إضافية..." class="w-full rounded-xl border border-gray-300 bg-gray-50/50 px-4 py-3 text-sm text-gray-900 transition-colors focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-500/20 dark:border-gray-700 dark:bg-gray-800/50 dark:text-white dark:focus:bg-gray-800"></textarea>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="px-6 py-4 border-t border-gray-100 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-800/20 flex justify-end gap-3">
          <button @click="showSettlementModal = false" class="rounded-xl border border-gray-300 bg-white px-5 py-2.5 text-sm font-bold text-gray-700 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-all">
            {{ $t?.('common.cancel') || 'إلغاء' }}
          </button>
          <button @click="submitSettlement" :disabled="settlementLoading" class="rounded-xl bg-brand-600 px-5 py-2.5 text-sm font-bold text-white shadow-theme-xs hover:bg-brand-700 focus:ring-2 focus:ring-brand-500/50 transition-all disabled:opacity-50 flex items-center gap-2">
            <svg v-if="settlementLoading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            {{ $t?.('settlements.submit_request') || 'تقديم' }}
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
    errorMsg.value = t('personnel.missing_military_number') || 'الرقم العسكري غير متوفر.'
    loading.value = false
    return
  }

  try {
    const data = await personnelStore.getPersonnelById(militaryNumber)
    person.value = data
  } catch (err: any) {
    errorMsg.value = err.response?.data?.error || t('personnel.fetch_error') || 'حدث خطأ أثناء محاولة جلب بيانات الفرد.'
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
    Swal.fire({ toast: true, position: 'top-end', icon: 'error', title: t('settlements.new_mil_num_required') || 'يجب إدخال الرقم العسكري الجديد للترقية لضابط', showConfirmButton: false, timer: 3000 })
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
      icon: 'success', title: t('settlements.settlement_success') || 'تم تقديم طلب تسوية الرتبة بنجاح',
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
