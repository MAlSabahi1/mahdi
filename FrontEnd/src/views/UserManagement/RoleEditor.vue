<template>
  <admin-layout>
    <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div class="flex items-center gap-3">
        <button @click="$router.push({ name: 'roles-management' })"
          class="flex h-10 w-10 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-500 shadow-theme-xs hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 transition-colors">
          <svg class="h-5 w-5 rtl:rotate-180" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
        </button>
        <div>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">
            {{ isEdit ? $t('roles.edit_role') : $t('roles.add_role') }}
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {{ isEdit ? $t('roles.edit_subtitle') : $t('roles.create_subtitle') }}
          </p>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <button @click="$router.push({ name: 'roles-management' })"
          class="rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 transition-colors dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700">
          {{ $t('common.cancel') }}
        </button>
        <button @click="saveRole" :disabled="submitLoading"
          class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors disabled:opacity-50">
          <svg v-if="submitLoading" class="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          <svg v-else class="h-4.5 w-4.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          {{ isEdit ? $t('roles.save_role') : $t('roles.create_role') }}
        </button>
      </div>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="flex items-start gap-3 rounded-lg border border-error-200 bg-error-50 p-4 dark:border-error-500/30 dark:bg-error-500/10">
      <div class="mt-0.5 text-error-600 dark:text-error-400">
        <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>
      <div class="flex-1">
        <h3 class="text-sm font-medium text-error-800 dark:text-error-400">{{ $t('roles.save_error') || 'خطأ في الحفظ' }}</h3>
        <p class="mt-1 text-sm text-error-700 dark:text-error-300">{{ error }}</p>
      </div>
    </div>

    <!-- Loading Skeleton -->
    <div v-if="pageLoading" class="animate-pulse space-y-6">
      <div class="rounded-xl border border-gray-200 bg-white p-6 shadow-theme-sm dark:border-gray-800 dark:bg-gray-900/50 h-32"></div>
      <div class="rounded-xl border border-gray-200 bg-white p-6 shadow-theme-sm dark:border-gray-800 dark:bg-gray-900/50 h-96"></div>
    </div>

    <template v-else>
      <!-- Basic Info Card -->
      <div class="rounded-xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900/50">
        <div class="border-b border-gray-100 p-5 dark:border-gray-800">
          <h3 class="text-base font-semibold text-gray-900 dark:text-white">{{ $t('users.personal_info') || 'البيانات الأساسية' }}</h3>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">
                {{ $t('roles.role_name') }} <span class="text-error-500">*</span>
              </label>
              <input v-model="form.name" v-field-error="'name'" type="text" placeholder="..." required
                class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white" />
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">
                {{ $t('roles.role_code') }} <span class="text-error-500">*</span>
              </label>
              <input v-model="form.code" v-field-error="'code'" type="text" placeholder="..." dir="ltr" required
                class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white" />
            </div>

            <div v-if="isEdit" class="flex items-center pt-8">
              <label class="relative inline-flex cursor-pointer items-center">
                <input v-model="form.is_active" v-field-error="'is_active'" type="checkbox" class="peer sr-only" />
                <div class="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:start-[2px] after:top-[2px] after:h-5 after:w-5 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-success-500 peer-checked:after:translate-x-full peer-checked:after:border-white dark:border-gray-700 dark:bg-gray-700 rtl:peer-checked:after:-translate-x-full"></div>
                <span class="ms-3 text-sm font-medium text-gray-700 dark:text-gray-300">{{ $t('users.active') }}</span>
              </label>
            </div>

            <div class="md:col-span-2 lg:col-span-3">
              <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">{{ $t('roles.description') }}</label>
              <textarea v-model="form.description" v-field-error="'description'" rows="2" placeholder="..."
                class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"></textarea>
            </div>
          </div>
        </div>
      </div>

      <!-- Permissions Matrix Card -->
      <div class="rounded-xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900/50 overflow-hidden">
        <div class="flex flex-col gap-4 border-b border-gray-100 p-5 sm:flex-row sm:items-center sm:justify-between dark:border-gray-800">
          <div>
            <h3 class="text-base font-semibold text-gray-900 dark:text-white">{{ $t('roles.advanced_permissions') || 'مصفوفة الصلاحيات المتقدمة' }}</h3>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">{{ $t('roles.advanced_permissions_subtitle') || 'حدد الصلاحيات المطلوبة لكل شاشة بدقة' }}</p>
          </div>
          
          <div class="flex items-center gap-3 bg-gray-50 p-1.5 rounded-lg border border-gray-200 dark:bg-gray-800/50 dark:border-gray-700">
            <span class="text-sm font-medium text-gray-700 dark:text-gray-300 px-2">{{ $t('roles.select_all') || 'تحديد جميع الصلاحيات في النظام:' }}</span>
            <label class="relative inline-flex cursor-pointer items-center">
              <input type="checkbox" :checked="allSelected" @change="toggleAllPermissions($event.target.checked)" class="peer sr-only" />
              <div class="peer h-6 w-11 rounded-full bg-gray-300 after:absolute after:start-[2px] after:top-[2px] after:h-5 after:w-5 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-brand-500 peer-checked:after:translate-x-full peer-checked:after:border-white dark:border-gray-600 dark:bg-gray-700 rtl:peer-checked:after:-translate-x-full"></div>
            </label>
          </div>
        </div>

        <div class="overflow-x-auto w-full">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
            <thead class="bg-gray-50/50 dark:bg-gray-800/30">
              <tr>
                <th class="px-5 py-4 text-start text-sm font-semibold text-gray-700 dark:text-gray-300 min-w-[180px] sticky right-0 bg-gray-50/95 dark:bg-gray-900/95 backdrop-blur-sm z-10 border-l border-gray-200 dark:border-gray-800">{{ $t('roles.screen_module') || 'الشاشة / الوحدة' }}</th>
                
                <th class="px-4 py-4 text-center w-20 group/th">
                  <div class="flex flex-col items-center gap-1.5">
                    <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">{{ $t('roles.view') || 'عرض' }}</span>
                    <input type="checkbox" :checked="isColumnAllSelected('view')" @change="toggleColumnPermissions('view', $event.target.checked)" class="h-4.5 w-4.5 rounded border-gray-300 text-blue-500 focus:ring-blue-500 bg-white dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" :title="$t('roles.select_all_view') || 'تحديد كل العرض'" />
                  </div>
                </th>
                
                <th class="px-4 py-4 text-center w-20 group/th">
                  <div class="flex flex-col items-center gap-1.5">
                    <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">{{ $t('common.add') || 'إضافة' }}</span>
                    <input type="checkbox" :checked="isColumnAllSelected('create')" @change="toggleColumnPermissions('create', $event.target.checked)" class="h-4.5 w-4.5 rounded border-gray-300 text-green-500 focus:ring-green-500 bg-white dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" :title="$t('roles.select_all_create') || 'تحديد كل الإضافة'" />
                  </div>
                </th>

                <th class="px-4 py-4 text-center w-20 group/th">
                  <div class="flex flex-col items-center gap-1.5">
                    <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">{{ $t('common.edit') || 'تعديل' }}</span>
                    <input type="checkbox" :checked="isColumnAllSelected('edit')" @change="toggleColumnPermissions('edit', $event.target.checked)" class="h-4.5 w-4.5 rounded border-gray-300 text-amber-500 focus:ring-amber-500 bg-white dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" :title="$t('roles.select_all_edit') || 'تحديد كل التعديل'" />
                  </div>
                </th>

                <th class="px-4 py-4 text-center w-20 group/th">
                  <div class="flex flex-col items-center gap-1.5">
                    <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">{{ $t('common.delete') || 'حذف' }}</span>
                    <input type="checkbox" :checked="isColumnAllSelected('delete')" @change="toggleColumnPermissions('delete', $event.target.checked)" class="h-4.5 w-4.5 rounded border-gray-300 text-error-500 focus:ring-error-500 bg-white dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" :title="$t('roles.select_all_delete') || 'تحديد كل الحذف'" />
                  </div>
                </th>

                <th class="px-4 py-4 text-center w-20 group/th">
                  <div class="flex flex-col items-center gap-1.5">
                    <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">{{ $t('roles.approve') || 'اعتماد' }}</span>
                    <input type="checkbox" :checked="isColumnAllSelected('approve')" @change="toggleColumnPermissions('approve', $event.target.checked)" class="h-4.5 w-4.5 rounded border-gray-300 text-success-500 focus:ring-success-500 bg-white dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" :title="$t('roles.select_all_approve') || 'تحديد كل الاعتماد'" />
                  </div>
                </th>

                <th class="px-4 py-4 text-center w-20 group/th">
                  <div class="flex flex-col items-center gap-1.5">
                    <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">{{ $t('common.export') || 'تصدير' }}</span>
                    <input type="checkbox" :checked="isColumnAllSelected('export')" @change="toggleColumnPermissions('export', $event.target.checked)" class="h-4.5 w-4.5 rounded border-gray-300 text-purple-500 focus:ring-purple-500 bg-white dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" :title="$t('roles.select_all_export') || 'تحديد كل التصدير'" />
                  </div>
                </th>

                <th class="px-4 py-4 text-center w-20 group/th">
                  <div class="flex flex-col items-center gap-1.5">
                    <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">{{ $t('roles.manage') || 'إدارة' }}</span>
                    <input type="checkbox" :checked="isColumnAllSelected('manage')" @change="toggleColumnPermissions('manage', $event.target.checked)" class="h-4.5 w-4.5 rounded border-gray-300 text-brand-500 focus:ring-brand-500 bg-white dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" :title="$t('roles.select_all_manage') || 'تحديد كل الإدارة'" />
                  </div>
                </th>

                <th class="px-4 py-4 text-center w-20 group/th">
                  <div class="flex flex-col items-center gap-1.5">
                    <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">{{ $t('roles.execute') || 'تنفيذ' }}</span>
                    <input type="checkbox" :checked="isColumnAllSelected('execute')" @change="toggleColumnPermissions('execute', $event.target.checked)" class="h-4.5 w-4.5 rounded border-gray-300 text-orange-500 focus:ring-orange-500 bg-white dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" :title="$t('roles.select_all_execute') || 'تحديد كل التنفيذ'" />
                  </div>
                </th>

                <th class="px-4 py-4 text-center w-20 group/th">
                  <div class="flex flex-col items-center gap-1.5">
                    <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">{{ $t('roles.import') || 'استيراد' }}</span>
                    <input type="checkbox" :checked="isColumnAllSelected('import')" @change="toggleColumnPermissions('import', $event.target.checked)" class="h-4.5 w-4.5 rounded border-gray-300 text-teal-500 focus:ring-teal-500 bg-white dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" :title="$t('roles.select_all_import') || 'تحديد كل الاستيراد'" />
                  </div>
                </th>

                <th class="px-4 py-4 text-start min-w-[200px]">
                  <div class="flex flex-col items-start gap-1.5">
                    <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">{{ $t('roles.custom_permissions') || 'صلاحيات مخصصة' }}</span>
                    <input type="checkbox" :checked="isColumnAllSelected('custom')" @change="toggleColumnPermissions('custom', $event.target.checked)" class="h-4.5 w-4.5 rounded border-gray-300 text-gray-500 focus:ring-gray-500 bg-white dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" :title="$t('roles.select_all_custom') || 'تحديد كل الصلاحيات المخصصة'" />
                  </div>
                </th>

                <th class="px-4 py-4 text-center text-sm font-semibold text-gray-700 dark:text-gray-300 w-20 border-r border-gray-200 dark:border-gray-800">{{ $t('common.all') || 'الكل' }}</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 bg-white dark:divide-gray-800 dark:bg-transparent">
              <tr v-for="screen in rolesStore.screens" :key="screen.name" 
                class="hover:bg-gray-50/50 dark:hover:bg-gray-800/20 transition-colors group">
                <!-- Screen Name -->
                <td class="px-5 py-4 text-start text-sm font-medium text-gray-900 dark:text-white sticky right-0 bg-white group-hover:bg-gray-50/50 dark:bg-gray-900 dark:group-hover:bg-gray-800/50 z-10 border-l border-gray-100 dark:border-gray-800 transition-colors">
                  {{ screen.label }}
                  <div class="text-xs text-gray-400 font-normal mt-0.5">{{ screen.name }}</div>
                </td>

                <!-- View -->
                <td class="px-4 py-4 text-center">
                  <div v-if="screen.permissions.view.length" class="flex flex-col items-center gap-1.5">
                    <label v-for="perm in screen.permissions.view" :key="perm.id" class="cursor-pointer" :title="perm.label">
                      <input type="checkbox" :value="perm.code" v-model="form.permissions" v-field-error="'permissions'"
                        class="h-5 w-5 rounded border-gray-300 text-blue-500 focus:ring-blue-500 bg-transparent dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" />
                    </label>
                  </div>
                  <span v-else class="text-gray-300 dark:text-gray-700">—</span>
                </td>

                <!-- Create -->
                <td class="px-4 py-4 text-center">
                  <div v-if="screen.permissions.create.length" class="flex flex-col items-center gap-1.5">
                    <label v-for="perm in screen.permissions.create" :key="perm.id" class="cursor-pointer" :title="perm.label">
                      <input type="checkbox" :value="perm.code" v-model="form.permissions" v-field-error="'permissions'"
                        class="h-5 w-5 rounded border-gray-300 text-green-500 focus:ring-green-500 bg-transparent dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" />
                    </label>
                  </div>
                  <span v-else class="text-gray-300 dark:text-gray-700">—</span>
                </td>

                <!-- Edit -->
                <td class="px-4 py-4 text-center">
                  <div v-if="screen.permissions.edit.length" class="flex flex-col items-center gap-1.5">
                    <label v-for="perm in screen.permissions.edit" :key="perm.id" class="cursor-pointer" :title="perm.label">
                      <input type="checkbox" :value="perm.code" v-model="form.permissions" v-field-error="'permissions'"
                        class="h-5 w-5 rounded border-gray-300 text-amber-500 focus:ring-amber-500 bg-transparent dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" />
                    </label>
                  </div>
                  <span v-else class="text-gray-300 dark:text-gray-700">—</span>
                </td>

                <!-- Delete -->
                <td class="px-4 py-4 text-center">
                  <div v-if="screen.permissions.delete.length" class="flex flex-col items-center gap-1.5">
                    <label v-for="perm in screen.permissions.delete" :key="perm.id" class="cursor-pointer" :title="perm.label">
                      <input type="checkbox" :value="perm.code" v-model="form.permissions" v-field-error="'permissions'"
                        class="h-5 w-5 rounded border-gray-300 text-error-500 focus:ring-error-500 bg-transparent dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" />
                    </label>
                  </div>
                  <span v-else class="text-gray-300 dark:text-gray-700">—</span>
                </td>

                <!-- Approve -->
                <td class="px-4 py-4 text-center">
                  <div v-if="screen.permissions.approve && screen.permissions.approve.length" class="flex flex-col items-center gap-1.5">
                    <label v-for="perm in screen.permissions.approve" :key="perm.id" class="cursor-pointer" :title="perm.label">
                      <input type="checkbox" :value="perm.code" v-model="form.permissions" v-field-error="'permissions'"
                        class="h-5 w-5 rounded border-gray-300 text-success-500 focus:ring-success-500 bg-transparent dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" />
                    </label>
                  </div>
                  <span v-else class="text-gray-300 dark:text-gray-700">—</span>
                </td>

                <!-- Export -->
                <td class="px-4 py-4 text-center">
                  <div v-if="screen.permissions.export && screen.permissions.export.length" class="flex flex-col items-center gap-1.5">
                    <label v-for="perm in screen.permissions.export" :key="perm.id" class="cursor-pointer" :title="perm.label">
                      <input type="checkbox" :value="perm.code" v-model="form.permissions" v-field-error="'permissions'"
                        class="h-5 w-5 rounded border-gray-300 text-purple-500 focus:ring-purple-500 bg-transparent dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" />
                    </label>
                  </div>
                  <span v-else class="text-gray-300 dark:text-gray-700">—</span>
                </td>

                <!-- Manage -->
                <td class="px-4 py-4 text-center">
                  <div v-if="screen.permissions.manage && screen.permissions.manage.length" class="flex flex-col items-center gap-1.5">
                    <label v-for="perm in screen.permissions.manage" :key="perm.id" class="cursor-pointer" :title="perm.label">
                      <input type="checkbox" :value="perm.code" v-model="form.permissions" v-field-error="'permissions'"
                        class="h-5 w-5 rounded border-gray-300 text-brand-500 focus:ring-brand-500 bg-transparent dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" />
                    </label>
                  </div>
                  <span v-else class="text-gray-300 dark:text-gray-700">—</span>
                </td>

                <!-- Execute -->
                <td class="px-4 py-4 text-center">
                  <div v-if="screen.permissions.execute && screen.permissions.execute.length" class="flex flex-col items-center gap-1.5">
                    <label v-for="perm in screen.permissions.execute" :key="perm.id" class="cursor-pointer" :title="perm.label">
                      <input type="checkbox" :value="perm.code" v-model="form.permissions" v-field-error="'permissions'"
                        class="h-5 w-5 rounded border-gray-300 text-orange-500 focus:ring-orange-500 bg-transparent dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" />
                    </label>
                  </div>
                  <span v-else class="text-gray-300 dark:text-gray-700">—</span>
                </td>

                <!-- Import -->
                <td class="px-4 py-4 text-center">
                  <div v-if="screen.permissions.import && screen.permissions.import.length" class="flex flex-col items-center gap-1.5">
                    <label v-for="perm in screen.permissions.import" :key="perm.id" class="cursor-pointer" :title="perm.label">
                      <input type="checkbox" :value="perm.code" v-model="form.permissions" v-field-error="'permissions'"
                        class="h-5 w-5 rounded border-gray-300 text-teal-500 focus:ring-teal-500 bg-transparent dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors" />
                    </label>
                  </div>
                  <span v-else class="text-gray-300 dark:text-gray-700">—</span>
                </td>

                <!-- Custom -->
                <td class="px-4 py-4">
                  <div v-if="screen.permissions.custom && screen.permissions.custom.length" class="flex flex-wrap gap-2">
                    <label v-for="perm in screen.permissions.custom" :key="perm.id"
                      class="inline-flex items-center gap-2 cursor-pointer rounded border px-3 py-1.5 transition-all select-none text-xs font-medium"
                      :class="form.permissions.includes(perm.code)
                        ? 'bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-500/10 dark:border-brand-500/30 dark:text-brand-400'
                        : 'bg-white border-gray-200 text-gray-500 hover:bg-gray-50 dark:bg-gray-900 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-800'"
                      :title="perm.label">
                      <input type="checkbox" :value="perm.code" v-model="form.permissions" v-field-error="'permissions'"
                        class="h-4 w-4 rounded border-gray-300 text-brand-500 focus:ring-brand-500 bg-transparent dark:border-gray-600 dark:bg-gray-800" />
                      {{ perm.label }}
                    </label>
                  </div>
                  <span v-else class="text-gray-300 dark:text-gray-700">—</span>
                </td>

                <!-- Select All for this screen -->
                <td class="px-4 py-4 text-center bg-gray-50/30 dark:bg-gray-800/10 border-r border-gray-100 dark:border-gray-800">
                  <label class="relative inline-flex cursor-pointer items-center justify-center">
                    <input type="checkbox"
                      :checked="isScreenAllSelected(screen)"
                      @change="toggleScreenPermissions(screen, $event.target.checked)"
                      class="h-5 w-5 rounded border-gray-300 text-brand-500 focus:ring-brand-500 bg-white dark:border-gray-600 dark:bg-gray-800 cursor-pointer transition-colors"
                      title="تحديد الكل لهذه الشاشة" />
                  </label>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
    </div>
  </admin-layout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useRolesStore } from '@/stores/roles'
import { validateFormFields } from '@/stores/validation'
import Swal from 'sweetalert2'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const rolesStore = useRolesStore()

const isEdit = computed(() => route.name === 'role-edit')
const roleId = computed(() => Number(route.params.id))

const pageLoading = ref(true)
const submitLoading = ref(false)
const error = ref('')

const form = reactive({
  name: '',
  code: '',
  description: '',
  is_active: true,
  permissions: []
})

// ── Computed helpers ──

const ALL_CATEGORIES = ['view', 'create', 'edit', 'delete', 'approve', 'export', 'manage', 'execute', 'import', 'custom']

const allPermissionCodes = computed(() => {
  const codes = []
  for (const screen of rolesStore.screens) {
    const p = screen.permissions
    for (const cat of ALL_CATEGORIES) {
      if (p[cat]) {
        for (const perm of p[cat]) {
          codes.push(perm.code)
        }
      }
    }
  }
  return codes
})

const allSelected = computed(() => {
  return allPermissionCodes.value.length > 0 && form.permissions.length === allPermissionCodes.value.length
})

// ── Methods ──

function getScreenPermCodes(screen) {
  const codes = []
  const p = screen.permissions
  for (const cat of ALL_CATEGORIES) {
    if (p[cat]) {
      for (const perm of p[cat]) {
        codes.push(perm.code)
      }
    }
  }
  return codes
}

function isScreenAllSelected(screen) {
  const codes = getScreenPermCodes(screen)
  if (codes.length === 0) return false
  return codes.every(c => form.permissions.includes(c))
}

function toggleScreenPermissions(screen, check) {
  const codes = getScreenPermCodes(screen)
  if (check) {
    const toAdd = codes.filter(c => !form.permissions.includes(c))
    form.permissions.push(...toAdd)
  } else {
    form.permissions = form.permissions.filter(c => !codes.includes(c))
  }
}

function getColumnPermCodes(category) {
  const codes = []
  for (const screen of rolesStore.screens) {
    if (screen.permissions[category]) {
      for (const perm of screen.permissions[category]) {
        codes.push(perm.code)
      }
    }
  }
  return codes
}

function isColumnAllSelected(category) {
  const codes = getColumnPermCodes(category)
  if (codes.length === 0) return false
  return codes.every(c => form.permissions.includes(c))
}

function toggleColumnPermissions(category, check) {
  const codes = getColumnPermCodes(category)
  if (check) {
    const toAdd = codes.filter(c => !form.permissions.includes(c))
    form.permissions.push(...toAdd)
  } else {
    form.permissions = form.permissions.filter(c => !codes.includes(c))
  }
}

function toggleAllPermissions(check) {
  if (check) {
    form.permissions = [...allPermissionCodes.value]
  } else {
    form.permissions = []
  }
}

async function loadData() {
  pageLoading.value = true
  try {
    // Ensure matrix is loaded
    if (rolesStore.screens.length === 0) {
      await rolesStore.fetchPermissionsMatrix()
    }
    
    // If editing, load the role data
    if (isEdit.value) {
      if (rolesStore.roles.length === 0) {
        await rolesStore.fetchRoles()
      }
      const role = rolesStore.roles.find(r => r.id === roleId.value)
      if (role) {
        form.name = role.name
        form.code = role.code
        form.description = role.description || ''
        form.is_active = role.is_active ?? true
        form.permissions = [...role.permissions]
      } else {
        Swal.fire({ toast: true, position: 'top-end', icon: 'error', title: t('roles.role_not_found') || 'لم يتم العثور على المجموعة المطلوبة', showConfirmButton: false, timer: 3000 })
        router.push({ name: 'roles-management' })
      }
    }
  } catch (err) {
    error.value = t('roles.load_error') || 'حدث خطأ أثناء جلب البيانات.'
  } finally {
    pageLoading.value = false
  }
}

async function saveRole() {
  if (!validateFormFields()) {
    error.value = t('roles.name_code_required') || 'يرجى إدخال اسم وكود المجموعة'
    return
  }
  if (form.permissions.length === 0) {
    error.value = t('roles.one_permission_required') || 'يجب اختيار صلاحية واحدة على الأقل'
    return
  }

  error.value = ''
  submitLoading.value = true
  
  try {
    if (isEdit.value) {
      await rolesStore.updateRole(roleId.value, form)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: t('roles.update_success') || 'تم تحديث المجموعة والصلاحيات بنجاح', showConfirmButton: false, timer: 3000 })
    } else {
      await rolesStore.createRole(form)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: t('roles.create_success') || 'تم إنشاء المجموعة بنجاح', showConfirmButton: false, timer: 3000 })
    }
    router.push({ name: 'roles-management' })
  } catch (err) {
    // Global interceptor handles standard Swal. We just keep local error for the UI hint if needed.
    error.value = err.response?.data?.detail || err.response?.data?.message || t('common.error') || 'حدث خطأ غير معروف'
  } finally {
    submitLoading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>
