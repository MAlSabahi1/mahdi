<template>
  <div class="space-y-6">
    <!-- Header Section -->
    <div class="flex justify-end gap-3 sticky top-4 z-40">
      <button @click="$emit('cancel')"
        class="rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 transition-colors dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 cursor-pointer">
        {{ $t('common.cancel') || 'إلغاء' }}
      </button>
      <button @click="handleSubmit" :disabled="loading || isNationalIdDuplicate"
        class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors disabled:opacity-50 cursor-pointer">
        <svg v-if="loading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
        <svg v-else class="h-4.5 w-4.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        {{ mode === 'edit' ? 'حفظ التعديلات' : ($t('personnel.save_personnel') || 'حفظ الفرد') }}
      </button>
    </div>

    <div v-if="coreStore.loading" class="flex justify-center p-12">
      <svg class="h-10 w-10 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
      </svg>
    </div>

    <div v-else class="space-y-6">
      <!-- Error Alert -->
      <div v-if="internalError" class="flex items-start gap-3 rounded-lg border border-error-200 bg-error-50 p-4 dark:border-error-500/30 dark:bg-error-500/10">
        <div class="mt-0.5 text-error-600 dark:text-error-400">
          <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <div class="flex-1">
          <h3 class="text-sm font-medium text-error-800 dark:text-error-400">{{ $t('common.error') || 'خطأ' }}</h3>
          <p class="mt-1 text-sm text-error-700 dark:text-error-300 whitespace-pre-line">{{ internalError }}</p>
        </div>
      </div>

      <!-- Section 1: Basic Info -->
      <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900 shadow-sm relative overflow-visible">
        <div class="absolute top-0 right-0 w-2 h-full bg-brand-500 rounded-r-2xl"></div>
        <h3 class="mb-5 text-lg font-bold text-gray-900 dark:text-white border-b border-gray-100 pb-3 dark:border-gray-800">{{ $t('personnel.basic_info_section') || 'البيانات الأساسية' }} (البيانات الأساسية)</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- Military Number -->
          <div class="lg:col-span-1">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
              {{ $t('personnel.military_number') || 'الرقم العسكري' }} <span class="text-error-500">*</span>
            </label>
            <input v-model="form.military_number" :disabled="mode === 'edit'" type="text" maxlength="7" 
              class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500 disabled:opacity-50 disabled:bg-gray-50" 
              :class="{'border-error-500': validationErrors.military_number}"
              placeholder="7 أرقام (مثال: 7000000)" required>
            <p v-if="validationErrors.military_number" class="mt-1 text-xs text-error-500">{{ validationErrors.military_number }}</p>
          </div>

          <!-- National ID Wizard Component -->
          <div class="lg:col-span-1 relative">
            <div v-if="mode === 'edit'" class="absolute -top-6 ltr:right-0 rtl:left-0 z-50">
              <button 
                @click="$emit('request-nid-correction')" 
                type="button" 
                class="text-xs font-medium text-brand-600 hover:text-brand-700 dark:text-brand-400 dark:hover:text-brand-300 flex items-center gap-1"
              >
                <svg class="h-3 w-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                {{ form.national_id ? 'تصحيح الرقم الوطني' : 'إضافة الرقم الوطني' }}
              </button>
            </div>
            <NationalIdWizard 
              v-model="form.national_id"
              :label="$t('personnel.national_id') || 'الرقم الوطني'"
              :required="true"
              :disabled="mode === 'edit'"
              :error="validationErrors.national_id"
              :checkDuplicateFn="checkDuplicateNationalId"
              @complete="onNationalIdComplete"
              @mismatch="onNationalIdMismatch"
            />
          </div>

          <!-- Phone Number -->
          <div class="lg:col-span-1">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
              {{ $t('personnel.phone') || 'رقم الهاتف' }}
            </label>
            <input v-model="form.phone_number" type="text" maxlength="9" dir="ltr"
              class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 text-left shadow-theme-xs placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder:text-gray-500 dark:focus:border-brand-500" 
              :class="{'border-error-500': validationErrors.phone_number}"
              placeholder="7xxxxxxxx">
            <p v-if="validationErrors.phone_number" class="mt-1 text-xs text-error-500">{{ validationErrors.phone_number }}</p>
          </div>

          <div class="lg:col-span-1">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.governorate') || 'المحافظة' }}</label>
            <div class="relative z-20 bg-transparent">
              <select v-model="form.geo_location" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                <option :value="null">...</option>
                <option v-for="gov in coreStore.governorates" :key="gov.id" :value="gov.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ gov.name }}</option>
              </select>
              <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
              </span>
            </div>
          </div>

          <!-- Full Name (5 Parts) -->
          <div class="lg:col-span-4 rounded-xl border border-gray-100 bg-gray-50/50 p-4 dark:border-gray-800 dark:bg-gray-800/20">
            <label class="mb-3 block text-sm font-bold text-gray-800 dark:text-gray-200">الاسم الخماسي (عربي فقط) <span class="text-error-500">*</span></label>
            <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
              <div>
                <input v-model="nameParts.first" type="text" @input="filterArabic($event, 'first')" class="block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white" :class="{'border-error-500': validationErrors.name_first}" placeholder="الاسم الأول">
                <p v-if="validationErrors.name_first" class="mt-1 text-xs text-error-500">{{ validationErrors.name_first }}</p>
              </div>
              <div>
                <input v-model="nameParts.second" type="text" @input="filterArabic($event, 'second')" class="block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white" :class="{'border-error-500': validationErrors.name_second}" placeholder="اسم الأب">
                <p v-if="validationErrors.name_second" class="mt-1 text-xs text-error-500">{{ validationErrors.name_second }}</p>
              </div>
              <div>
                <input v-model="nameParts.third" type="text" @input="filterArabic($event, 'third')" class="block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white" :class="{'border-error-500': validationErrors.name_third}" placeholder="اسم الجد">
                <p v-if="validationErrors.name_third" class="mt-1 text-xs text-error-500">{{ validationErrors.name_third }}</p>
              </div>
              <div>
                <input v-model="nameParts.fourth" type="text" @input="filterArabic($event, 'fourth')" class="block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white" :class="{'border-error-500': validationErrors.name_fourth}" placeholder="اسم إضافي (اختياري)">
                <p v-if="validationErrors.name_fourth" class="mt-1 text-xs text-error-500">{{ validationErrors.name_fourth }}</p>
              </div>
              <div>
                <input v-model="nameParts.surname" type="text" @input="filterArabic($event, 'surname')" class="block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white" :class="{'border-error-500': validationErrors.name_surname}" placeholder="اللقب">
                <p v-if="validationErrors.name_surname" class="mt-1 text-xs text-error-500">{{ validationErrors.name_surname }}</p>
              </div>
            </div>
          </div>

          <div v-if="!hiddenFields?.includes('birth_date')">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.birth_date') || 'تاريخ الميلاد' }}</label>
            <input v-model="form.birth_date" type="date" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
          </div>
          <div v-if="!hiddenFields?.includes('join_date')">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.join_date') || 'تاريخ التجنيد' }}</label>
            <input v-model="form.join_date" type="date" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500">
          </div>
          <div v-if="!hiddenFields?.includes('qualification')" class="lg:col-span-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.qualification') || 'المؤهل العلمي' }}</label>
            <div class="relative z-20 bg-transparent">
              <select v-model="form.qualification" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                <option :value="null">...</option>
                <option v-for="q in coreStore.qualifications" :key="q.id" :value="q.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ q.name }}</option>
              </select>
              <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Section 2: Service Info -->
      <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900 shadow-sm relative overflow-visible">
        <div class="absolute top-0 right-0 w-2 h-full bg-blue-500 rounded-r-2xl"></div>
        <h3 class="mb-5 text-lg font-bold text-gray-900 dark:text-white border-b border-gray-100 pb-3 dark:border-gray-800">{{ $t('personnel.service_info_section') || 'بيانات الخدمة' }} (الحالة والرتبة)</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
              {{ $t('personnel.current_rank') || 'الرتبة الحالية' }} <span class="text-error-500">*</span>
            </label>
            <div class="relative z-20 bg-transparent">
              <select v-model="form.current_rank" @change="validateRankLogic" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800"
                :class="{'border-error-500 focus:border-error-500 focus:ring-error-500/20': validationErrors.current_rank}">
                <option :value="null">...</option>
                <option v-for="r in coreStore.ranks" :key="r.id" :value="r.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ r.name }}</option>
              </select>
              <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
              </span>
            </div>
            <p v-if="validationErrors.current_rank" class="mt-1 text-xs text-error-500">{{ validationErrors.current_rank }}</p>
          </div>
          
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
              الحالة العامة (التصنيف) <span class="text-error-500">*</span>
            </label>
            <div class="relative z-20 bg-transparent">
              <select v-model="selectedClassification" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800"
                :class="{'border-error-500': validationErrors.current_status && !selectedClassification}">
                <option :value="null">...</option>
                <option v-for="c in statusClassifications" :key="c.value" :value="c.value" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ c.label }}</option>
              </select>
              <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
              </span>
            </div>
          </div>
          
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
              {{ $t('personnel.current_status') || 'الحالة الخدمية' }} (النوع التفصيلي) <span class="text-error-500">*</span>
            </label>
            <div class="relative z-20 bg-transparent">
              <select v-model="form.current_status" :disabled="!selectedClassification" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800 disabled:opacity-50 disabled:bg-gray-100"
                :class="{'border-error-500': validationErrors.current_status}">
                <option :value="null">...</option>
                <option v-for="s in filteredStatuses" :key="s.id" :value="s.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ s.name }}</option>
              </select>
              <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
              </span>
            </div>
            <p v-if="validationErrors.current_status" class="mt-1 text-xs text-error-500">{{ validationErrors.current_status }}</p>
          </div>

          <div>
            <label class="mb-1.5 flex items-center justify-between text-sm font-medium text-gray-700 dark:text-gray-400">
              <span>{{ $t('personnel.force_classification') || 'قوة السلاح' }}</span>
              <span v-if="filteredForceTypes.length > 0 && form.current_rank" class="text-xs text-gray-500">مفلتر حسب الرتبة</span>
            </label>
            <div class="relative z-20 bg-transparent">
              <select v-model="form.force_classification" @change="validateRankLogic" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800"
                :class="{'border-error-500 focus:border-error-500 focus:ring-error-500/20': validationErrors.force_classification}">
                <option :value="null">...</option>
                <option v-for="f in filteredForceTypes" :key="f.id" :value="f.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ f.name }}</option>
              </select>
              <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
              </span>
            </div>
            <p v-if="validationErrors.force_classification" class="mt-1 text-xs text-error-500">{{ validationErrors.force_classification }}</p>
          </div>

          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
              حالة النفقات
            </label>
            <div class="relative z-20 bg-transparent">
              <select v-model="form.expense_status" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                <option :value="null">...</option>
                <option value="has_expenses">لديه نفقات</option>
                <option value="no_expenses">بدون نفقات</option>
              </select>
              <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Section 3: Organization & Job -->
      <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900 shadow-sm relative overflow-visible">
        <div class="absolute top-0 right-0 w-2 h-full bg-emerald-500 rounded-r-2xl"></div>
        <h3 class="mb-5 text-lg font-bold text-gray-900 dark:text-white border-b border-gray-100 pb-3 dark:border-gray-800">{{ $t('personnel.org_job_section') || 'الهيكل والتوصيف' }} (الهيكل والتوصيف)</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Organization Structure (Grouped Dropdown) -->
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.security_admin') || 'الإدارة الأمنية' }}</label>
            <div class="relative z-20 bg-transparent">
              <select v-model="form.security_admin" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                <option :value="null">...</option>
                <option v-for="admin in coreStore.securityAdmins" :key="admin.id" :value="admin.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ admin.name }}</option>
              </select>
              <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
              </span>
            </div>
          </div>

          <div class="lg:col-span-2 relative z-[60]" ref="deptDropdownRef">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">جهة العمل الرئيسية (السرية/الإدارة)</label>
            <div class="relative bg-transparent">
              <input 
                type="text" 
                v-model="deptSearchQuery"
                @focus="showDeptDropdown = true"
                class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800"
                :class="{'border-error-500': validationErrors.department}"
                placeholder="ابحث عن اسم الإدارة أو الفرع أو المديرية..."
              />
              <span class="absolute text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              </span>
              
              <!-- Dropdown Menu -->
              <div v-show="showDeptDropdown" class="absolute left-0 mt-1 w-full rounded-lg bg-white shadow-xl border border-gray-100 dark:border-gray-700 dark:bg-gray-800 max-h-60 overflow-y-auto" style="z-index: 999;">
                <div v-for="group in filteredGroupedDepartments" :key="group.label">
                  <div v-if="group.options.length > 0" class="px-3 py-1.5 bg-gray-50 dark:bg-gray-900/50 text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider sticky top-0">{{ group.label }}</div>
                  <ul>
                    <li v-for="opt in group.options" :key="opt.value" 
                      @click.stop="selectDepartment(opt)"
                      class="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-brand-50 dark:hover:bg-brand-900/30 cursor-pointer transition-colors"
                      :class="{'bg-brand-50 dark:bg-brand-900/30 text-brand-700 dark:text-brand-400 font-medium': selectedDepartment === opt.value}">
                      {{ opt.label }}
                    </li>
                  </ul>
                </div>
                <div v-if="filteredGroupedDepartments.every(g => g.options.length === 0)" class="p-4 text-center text-sm text-gray-500">
                  لا توجد نتائج مطابقة للبحث
                </div>
              </div>
            </div>
            <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">يجب أن يتبع الفرد لجهة واحدة فقط (إدارة مركزية، أو فرع، أو مديرية) منعاً لتضارب القيود.</p>
            <p v-if="validationErrors.department" class="mt-1 text-xs text-error-500">{{ validationErrors.department }}</p>
          </div>

          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.division') || 'القسم/الإدارة الفرعية' }}</label>
            <div class="relative z-20 bg-transparent">
              <select v-model="form.division" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                <option :value="null">...</option>
                <option v-for="div in filteredDivisions" :key="div.id" :value="div.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ div.name }}</option>
              </select>
              <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
              </span>
            </div>
          </div>
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.unit') || 'الوحدة الميدانية' }}</label>
            <div class="relative z-20 bg-transparent">
              <select v-model="form.unit" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                <option :value="null">...</option>
                <option v-for="unit in filteredUnits" :key="unit.id" :value="unit.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ unit.name }}</option>
              </select>
              <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
              </span>
            </div>
          </div>

          <div class="col-span-full border-t border-gray-100 dark:border-gray-800 my-2"></div>

          <!-- Job Info with Auto-Locking -->
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.position') || 'المنصب الإداري' }}</label>
            <div class="relative z-20 bg-transparent">
              <select v-model="form.position" :disabled="!!form.job_title && filteredPositions.length === 0" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800 disabled:bg-gray-100 dark:disabled:bg-gray-800">
                <option :value="null">بدون منصب (ميداني غالباً)...</option>
                <option v-for="pos in filteredPositions" :key="pos.id" :value="pos.id" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">{{ pos.name }}</option>
              </select>
              <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
              </span>
            </div>
            <p v-if="form.job_title && filteredPositions.length === 0" class="mt-1 text-xs text-gray-500">مغلق: نوع العمل المختار لا يملك مناصب.</p>
          </div>

          <!-- Smart Job Title (Searchable Combobox) -->
          <div class="relative z-[50]" ref="jobDropdownRef">
            <label class="mb-1.5 flex items-center justify-between text-sm font-medium text-gray-700 dark:text-gray-400">
              <span>{{ $t('personnel.job_title') || 'نوع العمل' }}</span>
              <span class="text-xs text-brand-600 bg-brand-50 px-2 py-0.5 rounded dark:bg-brand-900/30 dark:text-brand-400">العدد: {{ coreStore.jobTitles.length }}</span>
            </label>
            <div class="relative bg-transparent" :class="{'opacity-60 cursor-not-allowed': form.position}">
              <input 
                type="text" 
                v-model="jobSearchQuery"
                @focus="showJobDropdown = true"
                @keydown.down.prevent="navigateJob(1)"
                @keydown.up.prevent="navigateJob(-1)"
                @keydown.enter.prevent="selectFocusedJob"
                :disabled="!!form.position"
                class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800 disabled:bg-gray-100 dark:disabled:bg-gray-800"
                placeholder="ابحث عن المسمى الوظيفي..."
                :class="{'border-error-500': validationErrors.job_title}"
              />
              <span class="absolute text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                <svg class="stroke-current h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              </span>
              
              <!-- Dropdown Menu -->
              <div v-show="showJobDropdown && !form.position" class="absolute left-0 mt-1 w-full rounded-lg bg-white shadow-xl border border-gray-100 dark:border-gray-700 dark:bg-gray-800 max-h-60 overflow-y-auto" style="z-index: 999;">
                <ul class="py-1">
                  <li v-for="(item, idx) in flatJobOptions" :key="item.isGroup ? 'g_'+item.label : 'o_'+item.value" 
                    @click.stop="!item.isGroup && selectJobTitle(item)"
                    :class="{
                      'px-3 py-1.5 bg-gray-50 dark:bg-gray-900/50 text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider sticky top-0': item.isGroup,
                      'px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-brand-50 dark:hover:bg-brand-900/30 cursor-pointer transition-colors': !item.isGroup,
                      'bg-brand-100 dark:bg-brand-900/50': !item.isGroup && focusedJobIndex === idx,
                      'bg-brand-50 dark:bg-brand-900/30 text-brand-700 dark:text-brand-400 font-medium': !item.isGroup && form.job_title === item.value && focusedJobIndex !== idx
                    }">
                    {{ item.label }}
                  </li>
                </ul>
                <div v-if="flatJobOptions.length === 0" class="p-4 text-center text-sm text-gray-500">
                  لا توجد نتائج مطابقة للبحث
                </div>
              </div>
            </div>
            <p v-if="form.position" class="mt-1 text-xs text-brand-600 dark:text-brand-400">يتم تحديده تلقائياً بناءً على المنصب المختار.</p>
            <p v-if="validationErrors.job_title" class="mt-1 text-xs text-error-500">{{ validationErrors.job_title }}</p>
          </div>

          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.job_category') || 'فئة العمل' }}</label>
            <input :value="computedCategoryName" type="text" readonly disabled class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm text-gray-500 shadow-theme-xs dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 cursor-not-allowed font-medium" :placeholder="$t('personnel.auto_determined') || 'تلقائي'">
          </div>
          
        </div>
      </div>

      <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900 shadow-sm">
        <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{{ $t('personnel.notes') || 'ملاحظات' }}</label>
        <textarea v-model="form.notes" rows="3" class="block w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-900 shadow-theme-xs focus:border-brand-500 focus:outline-none focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:focus:border-brand-500"></textarea>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useCoreStore } from '@/stores/core'
import { usePersonnelStore } from '@/stores/personnel'
import NationalIdWizard from '@/components/common/NationalIdWizard.vue'

const props = defineProps<{
  mode: 'create' | 'edit'
  initialData?: any
  loading?: boolean
  error?: string
  hiddenFields?: string[]
}>()

const emit = defineEmits(['submit', 'cancel', 'request-nid-correction'])

const { t } = useI18n()
const coreStore = useCoreStore()
const personnelStore = usePersonnelStore()

const internalError = ref('')
const isNationalIdDuplicate = ref(false)
const isValidatingNid = ref(false)

watch(() => props.error, (val) => {
  if (val) internalError.value = val
})

const validationErrors = reactive<Record<string, string>>({})

// Arabic Name Parts
const nameParts = reactive({
  first: '',
  second: '',
  third: '',
  fourth: '',
  surname: '',
})

// Prevent non-Arabic typing
function filterArabic(event: Event, key: keyof typeof nameParts) {
  const target = event.target as HTMLInputElement
  const value = target.value
  // Allow only arabic letters and spaces
  const filtered = value.replace(/[^\u0600-\u06FF\s]/g, '')
  nameParts[key] = filtered
  target.value = filtered
}

const form = reactive({
  military_number: '',
  full_name: '',
  national_id: null as string | null,
  national_id_confirm: null as string | null,
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
  
  expense_status: null as string | null,
  notes: null as string | null,
})

// Watch will be defined lower down

const selectedClassification = ref<string | null>(null)

// Extract unique classifications from coreStore
const statusClassifications = computed(() => {
  const map = new Map<string, string>()
  coreStore.statuses.forEach((s: any) => {
    if (s.classification && s.classification_display) {
      map.set(s.classification, s.classification_display)
    }
  })
  const arr = []
  for (const [val, label] of map.entries()) {
    arr.push({ value: val, label: label })
  }
  return arr
})

const filteredStatuses = computed(() => {
  if (!selectedClassification.value) return []
  return coreStore.statuses.filter((s: any) => s.classification === selectedClassification.value)
})

watch(selectedClassification, (newVal, oldVal) => {
  if (oldVal !== null && oldVal !== newVal) {
    form.current_status = null
  }
})

const selectedDepartment = ref<string | null>(null)
const deptDropdownRef = ref<HTMLElement | null>(null)
const showDeptDropdown = ref(false)
const deptSearchQuery = ref('')

// Smart Job Titles
const jobSearchQuery = ref('')
const showJobDropdown = ref(false)
const jobDropdownRef = ref<HTMLElement | null>(null)

// National ID Integration Logic
async function checkDuplicateNationalId(val: string): Promise<string | null> {
  if (props.mode === 'edit') return null
  const result = await personnelStore.checkNationalId(val)
  if (result.exists) {
    isNationalIdDuplicate.value = true
    if (result.owner) {
      return `مسجل مسبقاً للفرد: ${result.owner.full_name} (${result.owner.military_number})`
    }
    return 'هذا الرقم الوطني مسجل مسبقاً في النظام'
  }
  isNationalIdDuplicate.value = false
  return null
}

function onNationalIdComplete(val: string) {
  form.national_id = val
  form.national_id_confirm = val
  validationErrors.national_id = ''
}

function onNationalIdMismatch() {
  form.national_id_confirm = null
  isNationalIdDuplicate.value = false
}

function handleClickOutside(e: MouseEvent) {
  if (deptDropdownRef.value && !deptDropdownRef.value.contains(e.target as Node)) {
    showDeptDropdown.value = false
    // Restore query label if abandoned
    if (selectedDepartment.value) {
      let found = false
      for (const g of groupedDepartments.value) {
        const match = g.options.find(o => o.value === selectedDepartment.value)
        if (match) {
          deptSearchQuery.value = match.label
          found = true
          break
        }
      }
      if (!found) deptSearchQuery.value = ''
    } else {
      deptSearchQuery.value = ''
    }
  }

  if (jobDropdownRef.value && !jobDropdownRef.value.contains(e.target as Node)) {
    showJobDropdown.value = false
    // Restore query label if abandoned
    if (form.job_title) {
      const job = coreStore.jobTitles.find((j: any) => j.id === form.job_title)
      if (job) {
        jobSearchQuery.value = job.name
      } else {
        jobSearchQuery.value = ''
      }
    } else {
      jobSearchQuery.value = ''
    }
  }
}

const groupedDepartments = computed(() => {
  const groups = []
  if (coreStore.centralDepartments.length) {
    groups.push({
      label: 'الإدارات المركزية (قطاعات متخصصة)',
      options: coreStore.centralDepartments.map((d: any) => ({ value: `central_${d.id}`, label: d.name }))
    })
  }
  if (coreStore.branches.length) {
    groups.push({
      label: 'الفروع الرئيسية',
      options: coreStore.branches.map((b: any) => ({ value: `branch_${b.id}`, label: b.name }))
    })
  }
  if (coreStore.districtPolices.length) {
    groups.push({
      label: 'شرط المديريات والمناطق',
      options: coreStore.districtPolices.map((d: any) => ({ value: `district_${d.id}`, label: d.name }))
    })
  }
  return groups
})

const filteredGroupedDepartments = computed(() => {
  const query = deptSearchQuery.value.trim().toLowerCase()
  if (!query) return groupedDepartments.value
  
  return groupedDepartments.value.map(group => ({
    label: group.label,
    options: group.options.filter(o => o.label.toLowerCase().includes(query))
  }))
})

// Load initial data (placed here so variables are already initialized)
watch(() => props.initialData, (newVal) => {
  if (newVal) {
    Object.keys(form).forEach(key => {
      if (newVal[key] !== undefined) {
        (form as any)[key] = newVal[key]
      }
    })
    
    // Set national id confirm equal to original in edit mode
    if (props.mode === 'edit' && form.national_id) {
      form.national_id_confirm = form.national_id
    }

    if (newVal.full_name) {
      const parts = newVal.full_name.split(' ')
      nameParts.first = parts[0] || ''
      nameParts.second = parts[1] || ''
      nameParts.third = parts[2] || ''
      if (parts.length > 4) {
        nameParts.fourth = parts.slice(3, -1).join(' ')
        nameParts.surname = parts[parts.length - 1] || ''
      } else {
        nameParts.fourth = ''
        nameParts.surname = parts[3] || ''
      }
    }
    
    // Set department selection string
    if (form.central_department) selectedDepartment.value = `central_${form.central_department}`
    else if (form.branch) selectedDepartment.value = `branch_${form.branch}`
    else if (form.district_police) selectedDepartment.value = `district_${form.district_police}`
    
    // Initial category sync logic
    if (form.current_status) {
      const statusObj = coreStore.statuses.find((s: any) => s.id === form.current_status)
      if (statusObj && statusObj.classification) {
        selectedClassification.value = statusObj.classification
      }
    }
    
    // Initial job title search query sync
    if (form.job_title) {
      const jobObj = coreStore.jobTitles.find((j: any) => j.id === form.job_title)
      if (jobObj) {
        jobSearchQuery.value = jobObj.name
      }
    }
    // Set department search query
    if (selectedDepartment.value) {
      for (const g of groupedDepartments.value) {
        const match = g.options.find(o => o.value === selectedDepartment.value)
        if (match) {
          deptSearchQuery.value = match.label
          break
        }
      }
    }
  }
}, { immediate: true })

function selectDepartment(opt: {value: string, label: string}) {
  selectedDepartment.value = opt.value
  deptSearchQuery.value = opt.label
  showDeptDropdown.value = false
}

watch(selectedDepartment, (val) => {
  form.central_department = null
  form.branch = null
  form.district_police = null
  
  if (val) {
    const [type, idStr] = val.split('_')
    const id = parseInt(idStr)
    if (type === 'central') form.central_department = id
    else if (type === 'branch') form.branch = id
    else if (type === 'district') form.district_police = id
  }
})

const normalizeAr = (text: string) => {
  if (!text) return ''
  return text
    // Replace 'ال' only if it's at the beginning of the string or preceded by a space
    .replace(/(^|\s)ال/g, '$1')
    .replace(/[أإآا]/g, 'ا')
    .replace(/ة/g, 'ه')
    .replace(/[يى]/g, 'ي')
    .replace(/\s/g, '')
    .trim()
}

// Auto-lock Job Title based on Position (StrictDataConsistencyRule)
watch(() => form.position, (newPosId) => {
  if (newPosId) {
    const pos = coreStore.positions.find((p: any) => p.id === newPosId)
    if (pos) {
      const posNorm = normalizeAr(pos.name)
      const matchingJob = coreStore.jobTitles.find((j: any) => normalizeAr(j.name) === posNorm)
      
      if (matchingJob) {
        form.job_title = matchingJob.id
        jobSearchQuery.value = matchingJob.name
      }
    }
  }
})

// Auto-select Position based on Job Title
watch(() => form.job_title, (newJobId) => {
  if (newJobId) {
    const job = coreStore.jobTitles.find((j: any) => j.id === newJobId)
    if (job) {
      jobSearchQuery.value = job.name
      const jobNorm = normalizeAr(job.name)
      
      if (form.position) {
         const currentPos = coreStore.positions.find((p: any) => p.id === form.position)
         if (currentPos && normalizeAr(currentPos.name) !== jobNorm) {
            form.position = null
         }
      }
      
      if (!form.position) {
        const matchingPos = coreStore.positions.filter((p: any) => normalizeAr(p.name) === jobNorm)
        if (matchingPos.length > 0) {
          form.position = matchingPos[0].id
        }
      }
    }
  } else {
    jobSearchQuery.value = ''
    form.position = null
  }
})

// Reverse filter Position based on Job Title
const filteredPositions = computed(() => {
  if (form.job_title && !form.position) {
    const job = coreStore.jobTitles.find((j: any) => j.id === form.job_title)
    if (job) {
      const jobNorm = normalizeAr(job.name)
      const matchingPos = coreStore.positions.filter((p: any) => normalizeAr(p.name) === jobNorm)
      return matchingPos
    }
  }
  return coreStore.positions
})

// Job Titles Search Logic
const groupedJobTitles = computed(() => {
  const groups = new Map<string, any[]>()
  
  coreStore.jobTitles.forEach((j: any) => {
    const catName = j.category_name || 'غير مصنف'
    if (!groups.has(catName)) {
      groups.set(catName, [])
    }
    groups.get(catName)!.push({ value: j.id, label: j.name })
  })
  
  const arr = []
  for (const [label, options] of groups.entries()) {
    arr.push({ label, options })
  }
  return arr
})

const filteredGroupedJobTitles = computed(() => {
  const query = jobSearchQuery.value.trim().toLowerCase()
  if (!query) return groupedJobTitles.value
  
  return groupedJobTitles.value.map(group => ({
    label: group.label,
    options: group.options.filter(o => o.label.toLowerCase().includes(query))
  }))
})

const flatJobOptions = computed(() => {
  const flat: {value: number, label: string, isGroup?: boolean}[] = []
  filteredGroupedJobTitles.value.forEach(group => {
    if (group.options.length > 0) {
      flat.push({ value: -1, label: group.label, isGroup: true })
      group.options.forEach(opt => flat.push({ ...opt, isGroup: false }))
    }
  })
  return flat
})

const focusedJobIndex = ref(-1)

watch(jobSearchQuery, (newVal) => {
  focusedJobIndex.value = -1
  
  // If user modifies the search query and it no longer matches the selected job, clear the selection
  if (form.job_title) {
    const job = coreStore.jobTitles.find((j: any) => j.id === form.job_title)
    if (job && job.name !== newVal) {
      form.job_title = null
      showJobDropdown.value = true
    }
  }
})

function navigateJob(dir: number) {
  if (!showJobDropdown.value) {
    showJobDropdown.value = true
    return
  }
  const total = flatJobOptions.value.length
  if (total === 0) return
  
  let newIdx = focusedJobIndex.value + dir
  while(newIdx >= 0 && newIdx < total && flatJobOptions.value[newIdx].isGroup) {
     newIdx += dir
  }
  
  if (newIdx >= total) {
     newIdx = 0
     while(newIdx < total && flatJobOptions.value[newIdx].isGroup) newIdx++
  } else if (newIdx < 0) {
     newIdx = total - 1
     while(newIdx >= 0 && flatJobOptions.value[newIdx].isGroup) newIdx--
  }
  
  focusedJobIndex.value = newIdx
  
  if (jobDropdownRef.value) {
     const list = jobDropdownRef.value.querySelector('ul')
     if (list && list.children[newIdx]) {
        (list.children[newIdx] as HTMLElement).scrollIntoView({ block: 'nearest', behavior: 'smooth' })
     }
  }
}

function selectFocusedJob() {
  if (showJobDropdown.value && focusedJobIndex.value >= 0 && focusedJobIndex.value < flatJobOptions.value.length) {
    const item = flatJobOptions.value[focusedJobIndex.value]
    if (!item.isGroup) selectJobTitle(item as any)
  } else if (!showJobDropdown.value) {
    showJobDropdown.value = true
  }
}

function selectJobTitle(opt: {value: number, label: string}) {
  form.job_title = opt.value
  jobSearchQuery.value = opt.label
  showJobDropdown.value = false
}

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
      return cat ? cat.name : (t('personnel.unspecified') || 'غير محدد')
    }
  }
  return ''
})

const filteredForceTypes = computed(() => {
  if (!form.current_rank) return coreStore.forceTypes
  const rankObj = coreStore.ranks.find((r: any) => r.id === form.current_rank)
  const isOfficer = rankObj?.is_officer || false
  
  return coreStore.forceTypes.filter((f: any) => {
    // Exact match with backend rank_type fields ('officer', 'personnel', 'both')
    if (isOfficer && f.rank_type === 'personnel') return false
    if (!isOfficer && f.rank_type === 'officer') return false
    return true
  })
})

// Validation Engine
function validateRankLogic() {
  validationErrors.current_rank = ''
  validationErrors.force_classification = ''
  
  if (!form.current_rank) return
  
  const rankObj = coreStore.ranks.find((r: any) => r.id === form.current_rank)
  const isOfficerRank = rankObj?.is_officer || false
  
  // Military Number Prefix Rule
  if (form.military_number) {
    const prefix = form.military_number.substring(0, 2)
    const firstDigit = form.military_number[0]
    
    if (prefix === '60' && !isOfficerRank) {
      validationErrors.current_rank = 'الرقم العسكري يبدأ بـ 60 (ضابط) لكن الرتبة المختارة هي رتبة أفراد.'
    } else if ((firstDigit === '7' || firstDigit === '5') && prefix !== '60' && isOfficerRank) {
      validationErrors.current_rank = `الرقم العسكري يبدأ بـ ${prefix} (أفراد/لجان) لكن الرتبة المختارة هي رتبة ضباط.`
    }
  }
  
  // Force Classification Rule
  if (form.force_classification) {
    // Check if the selected force classification is still valid for this rank
    const validIds = filteredForceTypes.value.map((f: any) => f.id)
    if (!validIds.includes(form.force_classification)) {
      // Auto-clear invalid selection
      form.force_classification = null
    }
  }
  
  // Auto-select if there is only 1 valid force classification
  if (!form.force_classification && filteredForceTypes.value.length === 1) {
    form.force_classification = filteredForceTypes.value[0].id
  }
}

watch(() => form.military_number, () => {
  validateRankLogic()
})

function checkValidity() {
  Object.keys(validationErrors).forEach(k => delete validationErrors[k])
  let isValid = true
  
  if (!form.military_number || form.military_number.length !== 7) {
    validationErrors.military_number = 'الرقم العسكري يجب أن يكون 7 أرقام بالضبط'
    isValid = false
  }
  
  if (!form.national_id || !form.national_id_confirm || form.national_id !== form.national_id_confirm) {
    validationErrors.national_id = 'يرجى إكمال خطوات إدخال وتأكيد الرقم الوطني.'
    isValid = false
  }
  
  if (!nameParts.first) { validationErrors.name_first = 'مطلوب'; isValid = false }
  if (!nameParts.second) { validationErrors.name_second = 'مطلوب'; isValid = false }
  if (!nameParts.third) { validationErrors.name_third = 'مطلوب'; isValid = false }
  if (!nameParts.surname) { validationErrors.name_surname = 'مطلوب'; isValid = false }
  
  if (form.phone_number) {
    if (!/^7\d{8}$/.test(form.phone_number)) {
      validationErrors.phone_number = 'رقم الهاتف يجب أن يبدأ بـ 7 ويتكون من 9 أرقام'
      isValid = false
    }
  }

  if (!form.current_rank) {
    validationErrors.current_rank = 'الرتبة مطلوبة'
    isValid = false
  }
  if (!form.current_status) {
    validationErrors.current_status = 'الحالة الخدمية مطلوبة'
    isValid = false
  }
  
  validateRankLogic()
  if (validationErrors.current_rank || validationErrors.force_classification) {
    isValid = false
  }
  
  return isValid
}

async function handleSubmit() {
  if (!checkValidity()) {
    internalError.value = 'يرجى إصلاح الأخطاء المظللة باللون الأحمر قبل الحفظ.'
    window.scrollTo({ top: 0, behavior: 'smooth' })
    return
  }

  if (isNationalIdDuplicate.value && props.mode === 'create') {
    internalError.value = t('personnel.duplicate_national_id') || 'الرقم الوطني المدخل مسجل مسبقاً.'
    window.scrollTo({ top: 0, behavior: 'smooth' })
    return
  }

  // ✅ التحقق من تاريخ الميلاد مقابل تاريخ التجنيد (18 سنة على الأقل)
  if (form.birth_date && form.join_date) {
    const birth = new Date(form.birth_date as string)
    const join = new Date(form.join_date as string)
    if (!isNaN(birth.getTime()) && !isNaN(join.getTime())) {
      let ageAtJoin = join.getFullYear() - birth.getFullYear()
      const monthDiff = join.getMonth() - birth.getMonth()
      if (monthDiff < 0 || (monthDiff === 0 && join.getDate() < birth.getDate())) {
        ageAtJoin--
      }
      if (ageAtJoin < 18) {
        internalError.value = `❌ خطأ في التواريخ: تاريخ الميلاد (${(form.birth_date as string)}) يجعل عمر الفرد ${ageAtJoin} سنة عند تاريخ التجنيد (${(form.join_date as string)}). يجب أن يكون عمره 18 سنة على الأقل. يرجى تصحيح أحد التاريخين.`
        window.scrollTo({ top: 0, behavior: 'smooth' })
        return
      }
    }
  }

  internalError.value = ''

  // Combine names
  const parts = [nameParts.first, nameParts.second, nameParts.third]
  if (nameParts.fourth) parts.push(nameParts.fourth)
  parts.push(nameParts.surname)
  form.full_name = parts.join(' ')

  // Clean empty strings to null for API
  const payload = { ...form }
  console.log("PAYLOAD TO SEND:", payload)
  Object.keys(payload).forEach(key => {
    if (payload[key as keyof typeof payload] === '') {
      if (key !== 'notes') {
        (payload as any)[key] = null
      }
    }
  })
  
  // Ensure notes is an empty string instead of null, as Django TextField does not allow null
  if (payload.notes === null) {
    payload.notes = ''
  }

  emit('submit', payload)
}

onMounted(() => {
  if (coreStore.ranks.length === 0) {
    coreStore.fetchAllReferences()
  }
  document.addEventListener('mousedown', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside)
})
</script>

<style scoped>
/* Smooth transition for error states */
input, select, textarea {
  transition: all 0.2s ease-in-out;
}
</style>
