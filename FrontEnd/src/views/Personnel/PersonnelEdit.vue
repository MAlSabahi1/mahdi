<template>
  <admin-layout>
    <div class="space-y-6">
      <!-- Header Section -->
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div class="flex items-center gap-3">
          <button @click="router.push(`/personnel/${route.params.id}`)"
            class="flex h-10 w-10 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-500 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 transition-colors">
            <svg class="h-5 w-5 rtl:rotate-180" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>
          <div>
            <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ $t('personnel.edit_profile') || 'تعديل بيانات الفرد' }}</h2>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
              تحديث المعلومات والبيانات الوظيفية
            </p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <button @click="router.push(`/personnel/${route.params.id}`)"
            class="rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 transition-colors dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700">
            {{ $t('common.cancel') }}
          </button>
          <button @click="handleSubmit" :disabled="loading || isNationalIdDuplicate"
            class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors disabled:opacity-50">
            <svg v-if="loading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            <svg v-else class="h-4.5 w-4.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            {{ $t('common.save') }}
          </button>
        </div>
      </div>

      <div v-if="coreStore.loading || fetching" class="flex justify-center p-12">
        <svg class="h-10 w-10 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      </div>

      <div v-else class="space-y-6">
        <!-- Error Alert -->
        <div v-if="errorMsg" class="flex items-start gap-3 rounded-lg border border-error-200 bg-error-50 p-4 dark:border-error-500/30 dark:bg-error-500/10">
          <div class="mt-0.5 text-error-600 dark:text-error-400">
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div class="flex-1">
            <h3 class="text-sm font-medium text-error-800 dark:text-error-400">{{ $t('common.error') }}</h3>
            <p class="mt-1 text-sm text-error-700 dark:text-error-300">{{ errorMsg }}</p>
          </div>
        </div>

        <!-- Section 1: Basic Info -->
        <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900">
          <h3 class="mb-5 text-lg font-bold text-gray-900 dark:text-white border-b border-gray-100 pb-3 dark:border-gray-800">{{ $t('personnel.basic_info_section') }}</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.military_number') }} <span class="text-error-500">*</span></label>
              <input v-model="form.military_number" v-field-error="'military_number'" type="text" maxlength="7" disabled class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-500 shadow-theme-xs dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 cursor-not-allowed">
            </div>
            <div class="lg:col-span-2">
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.full_name') }} <span class="text-error-500">*</span></label>
              <input v-model="form.full_name" v-field-error="'full_name'" type="text" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500" placeholder="..." required>
            </div>
            
            <div class="relative">
              <div class="flex items-center justify-between mb-1.5">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.national_id') }}</label>
                <button 
                  v-if="form.military_number"
                  @click="showUpdateNidModal = true" 
                  type="button" 
                  class="text-xs font-medium text-brand-600 hover:text-brand-700 dark:text-brand-400 dark:hover:text-brand-300 flex items-center gap-1"
                >
                  <svg class="h-3 w-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  تحديث آمن
                </button>
              </div>
              <input 
                v-model="form.national_id" v-field-error="'national_id'" 
                type="text" 
                disabled
                class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-500 shadow-theme-xs focus:outline-none dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 cursor-not-allowed" 
                placeholder="سيتم التحديث عبر النافذة الآمنة..."
              >
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.phone') }}</label>
              <input v-model="form.phone_number" v-field-error="'phone_number'" type="text" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500" placeholder="...">
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.governorate') }}</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="form.geo_location" v-field-error="'geo_location'" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option :value="null">...</option>
                  <option v-for="gov in coreStore.governorates" :key="gov.id" :value="gov.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ gov.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.birth_date') }}</label>
              <input v-model="form.birth_date" v-field-error="'birth_date'" type="date" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.join_date') }}</label>
              <input v-model="form.join_date" v-field-error="'join_date'" type="date" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.qualification') }}</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="form.qualification" v-field-error="'qualification'" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option :value="null">...</option>
                  <option v-for="q in coreStore.qualifications" :key="q.id" :value="q.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ q.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Section 2: Service Info -->
        <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900">
          <h3 class="mb-5 text-lg font-bold text-gray-900 dark:text-white border-b border-gray-100 pb-3 dark:border-gray-800">{{ $t('personnel.service_info_section') }}</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.current_rank') }} <span class="text-error-500">*</span></label>
              <div class="relative z-20 bg-transparent">
                <select v-model="form.current_rank" v-field-error="'current_rank'" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800" required>
                  <option :value="null">...</option>
                  <option v-for="r in coreStore.ranks" :key="r.id" :value="r.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ r.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.current_status') }} <span class="text-error-500">*</span></label>
              <div class="relative z-20 bg-transparent">
                <select v-model="form.current_status" v-field-error="'current_status'" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800" required>
                  <option :value="null">...</option>
                  <option v-for="s in coreStore.statuses" :key="s.id" :value="s.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ s.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Section 3: Organization & Job -->
        <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900">
          <h3 class="mb-5 text-lg font-bold text-gray-900 dark:text-white border-b border-gray-100 pb-3 dark:border-gray-800">{{ $t('personnel.org_job_section') }}</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- Organization Structure -->
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.security_admin') }}</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="form.security_admin" v-field-error="'security_admin'" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option :value="null">...</option>
                  <option v-for="admin in coreStore.securityAdmins" :key="admin.id" :value="admin.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ admin.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.central_department') }}</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="form.central_department" v-field-error="'central_department'" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option :value="null">...</option>
                  <option v-for="dept in coreStore.centralDepartments" :key="dept.id" :value="dept.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ dept.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.branch') }}</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="form.branch" v-field-error="'branch'" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option :value="null">...</option>
                  <option v-for="branch in coreStore.branches" :key="branch.id" :value="branch.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ branch.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.district_police') }}</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="form.district_police" v-field-error="'district_police'" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option :value="null">...</option>
                  <option v-for="police in coreStore.districtPolices" :key="police.id" :value="police.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ police.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.division') }}</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="form.division" v-field-error="'division'" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option :value="null">...</option>
                  <option v-for="div in filteredDivisions" :key="div.id" :value="div.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ div.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.unit') }}</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="form.unit" v-field-error="'unit'" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option :value="null">...</option>
                  <option v-for="unit in filteredUnits" :key="unit.id" :value="unit.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ unit.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </div>

            <div class="col-span-full border-t border-gray-100 dark:border-gray-800 my-2"></div>

            <!-- Job Info -->
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.job_title') }}</label>
              <div class="relative z-20 bg-transparent" :class="{'opacity-50 cursor-not-allowed': form.position}">
                <select v-model="form.job_title" :disabled="!!form.position" v-field-error="'job_title'" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800 disabled:bg-gray-100 dark:disabled:bg-gray-800">
                  <option :value="null">...</option>
                  <option v-for="job in coreStore.jobTitles" :key="job.id" :value="job.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ job.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.position') }}</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="form.position" v-field-error="'position'" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option :value="null">...</option>
                  <option v-for="pos in filteredPositions" :key="pos.id" :value="pos.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ pos.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الفئة الوظيفية</label>
              <input :value="computedCategoryName" type="text" readonly disabled class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-500 shadow-theme-xs dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 cursor-not-allowed" placeholder="تتحدد تلقائياً">
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.force_classification') }}</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="form.force_classification" v-field-error="'force_classification'" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option :value="null">...</option>
                  <option v-for="f in coreStore.forceClassifications" :key="f.id" :value="f.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ f.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </div>
          </div>
        </div>

        <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900">
          <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.notes') }}</label>
          <textarea v-model="form.notes" v-field-error="'notes'" rows="3" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500"></textarea>
        </div>

      </div>
    </div>

    <!-- Modals -->
    <UpdateNationalIdModal 
      v-if="showUpdateNidModal"
      :military-number="form.military_number"
      @close="showUpdateNidModal = false"
      @success="handleNationalIdSuccess"
    />
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useCoreStore } from '@/stores/core'
import { usePersonnelStore } from '@/stores/personnel'
import { validateFormFields } from '@/stores/validation'
import Swal from 'sweetalert2'
import UpdateNationalIdModal from './components/UpdateNationalIdModal.vue'

const router = useRouter()
const route = useRoute()
const { t } = useI18n()
const coreStore = useCoreStore()
const personnelStore = usePersonnelStore()

const loading = ref(false)
const fetching = ref(true)
const errorMsg = ref('')

const isNationalIdDuplicate = ref(false)
const isValidatingNid = ref(false)
let nidTimeout: ReturnType<typeof setTimeout> | null = null

const initialNationalId = ref<string | null>(null)

const form = reactive({
  military_number: '',
  full_name: '',
  national_id: null as string | null,
  phone_number: null as string | null,
  birth_date: null as string | null,
  join_date: null as string | null,
  geo_location: null as number | null,
  qualification: null as number | null,
  
  current_rank: null as number | null,
  current_status: null as number | null,
  
  security_admin: null as number | null,
  central_department: null as number | null,
  branch: null as number | null,
  district_police: null as number | null,
  division: null as number | null,
  unit: null as number | null,
  
  job_title: null as number | null,
  position: null as number | null,
  force_classification: null as number | null,
  
  notes: null as string | null,
})

const filteredDivisions = computed(() => {
  if (!form.central_department && !form.branch && !form.district_police) {
    return coreStore.divisions
  }
  return coreStore.divisions.filter((d: any) => 
    (form.central_department && d.central_department === form.central_department) ||
    (form.branch && d.branch === form.branch) ||
    (form.district_police && d.district_police === form.district_police)
  )
})

const filteredUnits = computed(() => {
  if (!form.division) return coreStore.units
  return coreStore.units.filter((u: any) => u.division === form.division)
})

const computedCategoryName = computed(() => {
  if (form.job_title) {
    const job = coreStore.jobTitles.find((j: any) => j.id === form.job_title)
    if (job && job.category) {
      const cat = coreStore.jobCategories.find((c: any) => c.id === job.category)
      return cat ? cat.name : 'غير محدد'
    }
  }
  return ''
})

const filteredPositions = computed(() => {
  if (!form.job_title) return coreStore.positions
  
  const job = coreStore.jobTitles.find((j: any) => j.id === form.job_title)
  if (!job || !job.category) return coreStore.positions
  
  return coreStore.positions.filter((p: any) => {
    if (p.allowed_categories && Array.isArray(p.allowed_categories)) {
      return p.allowed_categories.includes(job.category)
    }
    if (p.category) {
      return p.category === job.category
    }
    return true
  })
})

const showUpdateNidModal = ref(false)

function handleNationalIdSuccess() {
  showUpdateNidModal.value = false
  Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم تقديم طلب تحديث الرقم الوطني بنجاح', showConfirmButton: false, timer: 3000 })
  fetchPersonData() // Reload to get updated data or correction status
}

async function fetchPersonData() {
  const militaryNumber = route.params.id as string
  if (!militaryNumber) return

  try {
    const data = await personnelStore.getPersonnelById(militaryNumber)
    
    // Populate form
    form.military_number = data.military_number
    form.full_name = data.full_name
    form.national_id = data.national_id
    initialNationalId.value = data.national_id
    form.phone_number = data.phone_number
    form.birth_date = data.birth_date
    form.join_date = data.join_date
    form.geo_location = data.geo_location
    form.qualification = data.qualification
    form.current_rank = data.current_rank
    form.current_status = data.current_status
    form.security_admin = data.security_admin
    form.central_department = data.central_department
    form.branch = data.branch
    form.district_police = data.district_police
    form.division = data.division
    form.unit = data.unit
    form.job_title = data.job_title
    form.position = data.position
    form.force_classification = data.force_classification
    form.notes = data.notes

  } catch (err: any) {
    errorMsg.value = err.response?.data?.error || t('common.error_loading') || 'حدث خطأ أثناء جلب البيانات.'
  } finally {
    fetching.value = false
  }
}

async function handleSubmit() {
  if (!validateFormFields()) {
    errorMsg.value = t('common.required_fields_error') || 'الرجاء تعبئة جميع الحقول الإجبارية المشار إليها بالنجمة (*)'
    window.scrollTo({ top: 0, behavior: 'smooth' })
    return
  }

  if (isNationalIdDuplicate.value) {
    errorMsg.value = t('personnel.duplicate_national_id') || 'الرقم الوطني المدخل مسجل مسبقاً.'
    window.scrollTo({ top: 0, behavior: 'smooth' })
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    // Clean empty strings to null for API
    const payload = { ...form }
    Object.keys(payload).forEach(key => {
      if (payload[key as keyof typeof payload] === '') {
        (payload as any)[key] = null
      }
    })

    await personnelStore.updatePersonnel(form.military_number, payload)
    router.push(`/personnel/${form.military_number}`) // navigate back to detail view
  } catch (err: any) {
    errorMsg.value = personnelStore.error || t('common.error') || 'فشل الحفظ. تأكد من صحة البيانات.'
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (coreStore.ranks.length === 0) {
    coreStore.fetchAllReferences()
  }
  await fetchPersonData()
})
</script>
