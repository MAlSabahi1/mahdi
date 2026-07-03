<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="حوكمة الحسابات وأمن النظام" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Header Section (Flat & Premium) -->
      <div class="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-4 border-b border-gray-200 dark:border-gray-800 pb-5">
        <div>
          <h1 class="text-2xl font-black text-gray-900 dark:text-white">
            مركز حوكمة الهوية وأمن النظام
          </h1>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            البوابة الأمنية والرقابية للتحكم الفوري في قفل الحسابات ومتابعة سجل الاختراق وضبط ضوابط الحماية.
          </p>
        </div>

        <!-- Global Actions -->
        <div class="flex items-center gap-3">
          <button 
            @click="refreshAll" 
            :disabled="loading || loadingLogs"
            class="flex items-center gap-1.5 border border-brand-200 bg-brand-50 hover:bg-brand-100 dark:border-brand-900/30 dark:bg-brand-950/20 text-brand-700 dark:text-brand-450 rounded-xl px-4 py-2.5 text-xs font-black transition-all cursor-pointer shadow-sm disabled:opacity-50"
          >
            <svg class="h-4 w-4" :class="{'animate-spin': loading || loadingLogs}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 8H17" />
            </svg>
            تحديث البيانات
          </button>
        </div>
      </div>

      <!-- Metrics Grid (Clean outline style cards with professional corporate accent colors) -->
      <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        
        <!-- Total Users Card -->
        <div class="relative overflow-hidden rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03] transition-all duration-300 hover:-translate-y-0.5 hover:shadow-sm shadow-theme-xs">
          <div class="flex justify-between items-center mb-4">
            <span class="text-[10px] font-black px-2.5 py-1 rounded-full tracking-wide bg-blue-50 text-blue-700 dark:bg-blue-950/20 dark:text-blue-400">
              قاعدة البيانات
            </span>
            <div class="h-9 w-9 rounded-xl flex items-center justify-center bg-blue-50 dark:bg-blue-950/30 border border-blue-100 dark:border-blue-900/20">
              <svg class="h-5 w-5 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.109A11.386 11.386 0 0110.089 21c-2.243 0-4.352-.648-6.124-1.763v-.109A11.386 11.386 0 018.91 18.06M8.91 18.06a9.38 9.38 0 00-2.625.372 9.337 9.337 0 00-4.121-.952 4.125 4.125 0 007.533-2.493M8.91 18.06c.498-.907.78-1.954.78-3.067V13.8M9.69 13.8a4.5 4.5 0 11-1.38-7.9M9.69 13.8a4.5 4.5 0 004.31-3.3M12.69 6.2a4.5 4.5 0 115.65 6.64" />
              </svg>
            </div>
          </div>
          <p class="text-[11px] text-gray-500 dark:text-gray-400 font-bold tracking-wider">إجمالي المستخدمين</p>
          <h3 class="text-2xl font-black text-gray-900 dark:text-white mt-1.5 flex items-baseline gap-1.5">
            {{ totalUsers }}
            <span class="text-xs font-semibold text-gray-400 dark:text-gray-500">حساب</span>
          </h3>
          <p class="text-xs text-gray-400 dark:text-gray-500 mt-3 flex items-center gap-1.5 font-medium">
            <span class="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
            مسجلين في المنظومة
          </p>
        </div>

        <!-- Locked Users Card -->
        <div class="relative overflow-hidden rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03] transition-all duration-300 hover:-translate-y-0.5 hover:shadow-sm shadow-theme-xs">
          <div class="flex justify-between items-center mb-4">
            <span class="text-[10px] font-black px-2.5 py-1 rounded-full tracking-wide bg-error-50 text-error-700 dark:bg-error-950/20 dark:text-error-400">
              الحظر النشط
            </span>
            <div class="h-9 w-9 rounded-xl flex items-center justify-center bg-error-50 dark:bg-error-950/30 border border-error-100 dark:border-error-900/20">
              <svg class="h-5 w-5 text-error-600 dark:text-error-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
              </svg>
            </div>
          </div>
          <p class="text-[11px] text-gray-500 dark:text-gray-400 font-bold tracking-wider">الحسابات المقفلة</p>
          <h3 class="text-2xl font-black mt-1.5 flex items-baseline gap-1.5 text-error-650 dark:text-error-400">
            {{ lockedUsersCount }}
            <span class="text-xs font-semibold text-gray-400 dark:text-gray-500">حساب</span>
          </h3>
          <p class="text-xs text-gray-400 dark:text-gray-500 mt-3 flex items-center gap-1.5 font-medium">
            <span class="h-1.5 w-1.5 rounded-full bg-red-500"></span>
            بسبب محاولات خاطئة
          </p>
        </div>

        <!-- Failed Attempts Card -->
        <div class="relative overflow-hidden rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03] transition-all duration-300 hover:-translate-y-0.5 hover:shadow-sm shadow-theme-xs">
          <div class="flex justify-between items-center mb-4">
            <span class="text-[10px] font-black px-2.5 py-1 rounded-full tracking-wide bg-warning-50 text-warning-700 dark:bg-warning-950/20 dark:text-warning-400">
              محاولات فاشلة
            </span>
            <div class="h-9 w-9 rounded-xl flex items-center justify-center bg-warning-50 dark:bg-warning-950/30 border border-warning-100 dark:border-warning-900/20">
              <svg class="h-5 w-5 text-warning-600 dark:text-warning-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m0-10.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.75c0 5.592 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.57-.598-3.75h-.152c-3.196 0-6.1-1.249-8.25-3.286zm0 13.036h.008v.008H12v-.008z" />
              </svg>
            </div>
          </div>
          <p class="text-[11px] text-gray-500 dark:text-gray-400 font-bold tracking-wider">سجل المحاولات الخاطئة</p>
          <h3 class="text-2xl font-black text-gray-900 dark:text-white mt-1.5 flex items-baseline gap-1.5">
            {{ failedAttemptsCount }}
            <span class="text-xs font-semibold text-gray-400 dark:text-gray-500">محاولة</span>
          </h3>
          <p class="text-xs text-gray-400 dark:text-gray-500 mt-3 flex items-center gap-1.5 font-medium">
            <span class="h-1.5 w-1.5 rounded-full bg-amber-500"></span>
            خلال آخر 24 ساعة
          </p>
        </div>

        <!-- Active Sessions Card -->
        <div class="relative overflow-hidden rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03] transition-all duration-300 hover:-translate-y-0.5 hover:shadow-sm shadow-theme-xs">
          <div class="flex justify-between items-center mb-4">
            <span class="text-[10px] font-black px-2.5 py-1 rounded-full tracking-wide bg-success-50 text-success-700 dark:bg-success-950/20 dark:text-success-400">
              الاتصال اللحظي
            </span>
            <div class="h-9 w-9 rounded-xl flex items-center justify-center bg-success-50 dark:bg-success-950/30 border border-success-100 dark:border-success-900/20">
              <svg class="h-5 w-5 text-success-600 dark:text-success-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 17.25v1.007a3 3 0 01-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0115 18.257V17.25m6-12V15a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 15V5.25m18 0A2.25 2.25 0 0018.75 3H5.25A2.25 2.25 0 003 5.25m18 0V12a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 12V5.25" />
              </svg>
            </div>
          </div>
          <p class="text-[11px] text-gray-500 dark:text-gray-400 font-bold tracking-wider">الجلسات والأجهزة النشطة</p>
          <h3 class="text-2xl font-black text-gray-900 dark:text-white mt-1.5 flex items-baseline gap-1.5">
            {{ activeSessionsCount }}
            <span class="text-xs font-semibold text-gray-400 dark:text-gray-500">جلسة نشطة</span>
          </h3>
          <p class="text-xs text-gray-400 dark:text-gray-500 mt-3 flex items-center gap-1.5 font-medium">
            <span class="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
            متصلة بالمنظومة
          </p>
        </div>
      </div>

      <!-- Main Layout Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Right Column: User Management Table & Timeline Logs (8 Columns) -->
        <div class="lg:col-span-8 space-y-6">
          
          <!-- Users Control Table -->
          <div class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03] shadow-theme-xs overflow-hidden">
            
            <!-- Table Header Toolbar -->
            <div class="p-5 border-b border-gray-250 dark:border-gray-800 space-y-4">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h3 class="text-sm font-black text-gray-900 dark:text-white">إدارة الحسابات والتحكم الأمني</h3>
                  <p class="text-[11px] text-gray-400 dark:text-gray-500 mt-0.5">صلاحيات التحكم المباشر بإلغاء الحظر وتجميد وتفعيل حسابات المستخدمين.</p>
                </div>

                <!-- Tabs segment -->
                <div class="inline-flex p-1 bg-gray-100 dark:bg-gray-900 rounded-xl">
                  <button 
                    v-for="status in ['all', 'active', 'locked', 'inactive']" 
                    :key="status"
                    @click="activeFilter = status"
                    class="px-3 py-1.5 text-[10px] font-black rounded-lg transition-all cursor-pointer"
                    :class="[activeFilter === status ? 'bg-white dark:bg-gray-800 text-gray-900 dark:text-white shadow-theme-xs' : 'text-gray-500 hover:text-gray-700']"
                  >
                    {{ getStatusFilterName(status) }}
                  </button>
                </div>
              </div>

              <!-- Search Bar -->
              <div class="relative">
                <span class="absolute inset-y-0 start-0 flex items-center ps-3 text-gray-400">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </span>
                <input 
                  type="text" 
                  v-model="searchQuery"
                  placeholder="ابحث عن حساب مستخدم بالاسم، اسم المستخدم، أو البريد الإلكتروني..." 
                  class="w-full ps-9 pe-4 py-2 text-xs border border-gray-200 dark:border-gray-800 rounded-xl bg-white dark:bg-gray-950 focus:outline-none focus:ring-2 focus:ring-brand-500 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            <!-- Table content -->
            <div v-if="loading" class="flex justify-center py-12">
              <svg class="h-6 w-6 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
            </div>

            <div v-else-if="filteredUsers.length === 0" class="text-center py-12">
              <span class="text-xs text-gray-400 dark:text-gray-500">لا توجد حسابات مستخدمين مطابقة للخيارات.</span>
            </div>

            <div v-else class="overflow-x-auto">
              <table class="w-full text-right border-collapse text-xs">
                <thead>
                  <tr class="border-b border-gray-200 dark:border-gray-800 text-[10px] font-bold text-gray-400 bg-gray-50/50 dark:bg-gray-950/20">
                    <th class="px-5 py-3 text-start">الحساب / الموظف</th>
                    <th class="px-5 py-3">الحالة الأمنية</th>
                    <th class="px-5 py-3 text-center">محاولات خاطئة</th>
                    <th class="px-5 py-3">البريد الإلكتروني</th>
                    <th class="px-5 py-3 text-center">إجراءات الحوكمة</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-150 dark:divide-gray-850">
                  <tr v-for="user in filteredUsers" :key="user.id" class="hover:bg-gray-50/40 dark:hover:bg-gray-800/10">
                    
                    <!-- User Account / Avatar (Restored dynamic pastel initial colors) -->
                    <td class="px-5 py-3.5">
                      <div class="flex items-center gap-3">
                        <div class="w-8.5 h-8.5 rounded-xl flex items-center justify-center font-black text-xs shadow-theme-xs shrink-0 border" :class="getAvatarBgColor(user.username)">
                          {{ getUserInitials(user.username) }}
                        </div>
                        <div>
                          <div class="font-extrabold text-gray-900 dark:text-white flex items-center gap-1.5">
                            <span>{{ user.username }}</span>
                            <span 
                              v-if="user.security_status?.must_change_password"
                              class="px-1.5 py-0.5 rounded text-[8px] bg-amber-50 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400 font-bold border border-amber-200/50"
                            >
                              إلزام التغيير
                            </span>
                          </div>
                          <div class="text-[10px] text-gray-400 mt-0.5">{{ user.full_name || 'بدون اسم كامل' }}</div>
                        </div>
                      </div>
                    </td>

                    <!-- Status Badge (Restored clean colored badges) -->
                    <td class="px-5 py-3.5">
                      <span 
                        class="px-2.5 py-0.5 rounded-full font-bold text-[9px] inline-flex items-center gap-1.5 border"
                        :class="getUserStatusClasses(user)"
                      >
                        <span class="h-1.5 w-1.5 rounded-full" :class="getUserStatusDotClass(user)"></span>
                        {{ getUserStatusLabel(user) }}
                      </span>
                    </td>

                    <!-- Failed Attempts -->
                    <td class="px-5 py-3.5 text-center font-extrabold text-gray-950 dark:text-white font-mono">
                      <span :class="[user.security_status?.failed_attempts && user.security_status.failed_attempts >= 3 ? 'text-error-600 bg-error-50 px-2 py-0.5 rounded-lg' : 'text-gray-500']">
                        {{ user.security_status?.failed_attempts || 0 }} / 5
                      </span>
                    </td>

                    <!-- Email -->
                    <td class="px-5 py-3.5 text-gray-650 dark:text-gray-400 font-mono text-[10px]">{{ user.email || '—' }}</td>

                    <!-- Action buttons (Clean outline style with soft icon colors) -->
                    <td class="px-5 py-3.5 text-center">
                      <div class="flex items-center justify-center gap-2">
                        
                        <!-- Unlock -->
                        <button
                          v-if="user.security_status?.is_locked"
                          @click="handleUnlockUser(user)"
                          class="px-2.5 py-1.5 text-[10px] font-black text-gray-700 dark:text-gray-300 bg-white hover:bg-gray-50 dark:bg-gray-900 dark:hover:bg-gray-800 border border-gray-200 dark:border-gray-750 rounded-lg transition-colors cursor-pointer inline-flex items-center gap-1 shadow-sm"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 10.5V6.75a4.5 4.5 0 119 0v3.75M3.75 21.75h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H3.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
                          </svg>
                          <span>فك القفل</span>
                        </button>

                        <!-- Reset password -->
                        <button
                          @click="handleResetPassword(user)"
                          class="px-2.5 py-1.5 text-[10px] font-black text-gray-700 dark:text-gray-300 bg-white hover:bg-gray-50 dark:bg-gray-900 dark:hover:bg-gray-800 border border-gray-200 dark:border-gray-750 rounded-lg transition-colors cursor-pointer inline-flex items-center gap-1 shadow-sm"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 5.25a3 3 0 013 3m3 0a6 6 0 01-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H3.75v-2.25A2.25 2.25 0 014.22 17.5l4.83-4.83a1.875 1.875 0 00.43-1.563 6 6 0 1110.27-5.857z" />
                          </svg>
                          <span>إعادة تعيين</span>
                        </button>

                        <!-- Deactivate / Activate -->
                        <button
                          v-if="user.is_active"
                          @click="handleDeactivateUser(user)"
                          class="px-2.5 py-1.5 text-[10px] font-black text-gray-700 dark:text-gray-300 bg-white hover:bg-gray-50 dark:bg-gray-900 dark:hover:bg-gray-800 border border-gray-200 dark:border-gray-750 rounded-lg transition-colors cursor-pointer inline-flex items-center gap-1 shadow-sm"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                          </svg>
                          <span>تعطيل الحساب</span>
                        </button>
                        <button
                          @click="handleActivateUser(user)"
                          v-else
                          class="px-2.5 py-1.5 text-[10px] font-black text-gray-700 dark:text-gray-300 bg-white hover:bg-gray-50 dark:bg-gray-900 dark:hover:bg-gray-800 border border-gray-200 dark:border-gray-750 rounded-lg transition-colors cursor-pointer inline-flex items-center gap-1 shadow-sm"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          <span>تفعيل</span>
                        </button>

                      </div>
                    </td>

                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Real-Time Activity Feed Logs (Clean Light Theme Timeline with Warning Orange Indicators) -->
          <div class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03] p-6 shadow-theme-xs space-y-4">
            
            <div class="flex items-center justify-between border-b border-gray-100 dark:border-gray-800 pb-3">
              <h3 class="text-sm font-black text-gray-900 dark:text-white flex items-center gap-2">
                <span class="p-1 rounded-lg bg-orange-500/10 text-orange-600">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-4.5 h-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </span>
                <span>سجل محاولات الدخول المشبوهة والفاشلة</span>
              </h3>
              
              <button 
                @click="loadLogs"
                class="text-[11px] font-black text-gray-700 dark:text-gray-300 bg-gray-50 hover:bg-gray-100 dark:bg-gray-800 dark:hover:bg-gray-750 px-3 py-1.5 rounded-xl border border-gray-200 dark:border-gray-700 transition-all cursor-pointer"
              >
                تحديث السجل
              </button>
            </div>

            <!-- Logs list -->
            <div v-if="loadingLogs" class="flex justify-center py-6">
              <svg class="h-6 w-6 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
            </div>

            <div v-else-if="failedLoginLogs.length === 0" class="text-center py-6 text-xs text-gray-400">
              لا توجد محاولات دخول فاشلة مسجلة.
            </div>

            <!-- Beautiful Muted Timeline Logs (Warning Red/Orange Indicator Dots) -->
            <div v-else class="space-y-4 relative before:absolute before:inset-y-0 before:end-3.5 before:w-0.5 before:bg-gray-100 dark:before:bg-gray-800">
              <div 
                v-for="log in failedLoginLogs" 
                :key="log.id" 
                class="relative pe-8 flex flex-col md:flex-row md:items-start justify-between gap-2 text-right"
              >
                <!-- Timeline Dot Indicator -->
                <span class="absolute top-1.5 end-2.5 w-2 h-2 rounded-full bg-red-500 ring-4 ring-red-50 dark:ring-red-950/20"></span>
                
                <div class="space-y-1">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="font-extrabold text-gray-700 dark:text-gray-300">فشل دخول لـ:</span>
                    <span class="font-mono font-black text-amber-700 bg-amber-50 dark:bg-amber-950/20 dark:text-amber-400 px-2 py-0.5 rounded border border-amber-200/30">{{ log.username_attempted }}</span>
                    <span class="px-2 py-0.5 rounded text-[9px] font-bold bg-error-50 text-error-700 dark:bg-error-950/20 dark:text-error-400 border border-error-200/30">
                      {{ formatFailureReason(log.failure_reason) }}
                    </span>
                  </div>
                  
                  <div class="text-[10px] text-gray-400 dark:text-gray-500 font-mono flex flex-wrap items-center gap-x-2 gap-y-1">
                    <span>IP: <span class="text-gray-600 dark:text-gray-400">{{ log.ip_address }}</span></span>
                    <span>|</span>
                    <span>الموقع: <span class="text-gray-600 dark:text-gray-400">{{ log.geo_location || 'غير محدد' }}</span></span>
                    <span>|</span>
                    <span class="max-w-xs truncate" :title="log.user_agent">المتصفح: {{ log.user_agent }}</span>
                  </div>
                </div>

                <div class="text-gray-400 dark:text-gray-500 text-[10px] font-mono shrink-0 md:text-left self-start mt-0.5">
                  {{ formatDate(log.timestamp) }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Left Column: Security Posture Circular Progress & Checklist (4 Columns) -->
        <div class="lg:col-span-4 space-y-6">
          
          <!-- Circular score panel -->
          <div class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03] p-6 shadow-theme-xs space-y-6">
            
            <div class="flex items-center gap-3 pb-4 border-b border-gray-150 dark:border-gray-800">
              <span class="p-1.5 rounded-lg bg-blue-50 dark:bg-blue-950/30 text-blue-600 dark:text-blue-400">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </span>
              <div>
                <h3 class="text-sm font-black text-gray-900 dark:text-white">مؤشر أمان السياسات</h3>
                <p class="text-[10px] text-gray-400 mt-0.5">تقييم الالتزام بضوابط ومعايير حماية الحسابات.</p>
              </div>
            </div>

            <!-- Gauge UI -->
            <div class="flex flex-col items-center py-5 bg-gray-50/50 dark:bg-gray-950/40 rounded-2xl border border-gray-100 dark:border-gray-850">
              <div class="relative w-32 h-32">
                <svg class="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                  <path
                    class="text-gray-100 dark:text-gray-800"
                    stroke-width="3"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <path
                    class="text-brand-500"
                    stroke-width="3"
                    stroke-dasharray="95, 100"
                    stroke-linecap="round"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                </svg>
                <div class="absolute inset-0 flex flex-col items-center justify-center text-center">
                  <span class="text-3xl font-black text-gray-900 dark:text-white tracking-tighter">95%</span>
                  <span class="text-[9px] font-bold text-gray-400 uppercase tracking-wide mt-0.5">درجة الأمان</span>
                </div>
              </div>
              <div class="text-center mt-4 px-4">
                <span class="text-[10px] font-black text-emerald-700 bg-emerald-50 dark:bg-emerald-500/10 dark:text-emerald-400 px-3 py-1 rounded-full border border-emerald-200/30">
                  ضوابط حماية مكتملة
                </span>
                <p class="text-[10px] text-gray-500 dark:text-gray-400 mt-2.5 leading-relaxed">
                  السياسة تلبي ضوابط الأمن وحماية الهوية ضد الهجمات العشوائية.
                </p>
              </div>
            </div>

            <!-- Rules list -->
            <div class="space-y-4">
              
              <!-- Lockout item -->
              <div class="p-3.5 bg-gray-50/50 dark:bg-gray-950/40 border border-gray-150 dark:border-gray-850 rounded-xl">
                <div class="flex items-center justify-between mb-1.5">
                  <span class="text-xs font-bold text-gray-900 dark:text-white">الحظر التلقائي المتكرر</span>
                  <span class="px-2 py-0.5 rounded text-[8px] bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400 font-bold border border-emerald-250/30">نشط</span>
                </div>
                <p class="text-[10px] text-gray-500 leading-relaxed">
                  قفل حساب المستخدم مؤقتاً لمدة 30 دقيقة بعد 5 محاولات خاطئة لمنع هجمات التخمين.
                </p>
              </div>

              <!-- Idle Timeout -->
              <div class="p-3.5 bg-gray-50/50 dark:bg-gray-950/40 border border-gray-150 dark:border-gray-850 rounded-xl">
                <div class="flex items-center justify-between mb-1.5">
                  <span class="text-xs font-bold text-gray-900 dark:text-white">مهلة انتهاء الجلسة</span>
                  <span class="px-2 py-0.5 rounded text-[8px] bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400 font-bold border border-emerald-250/30">نشط</span>
                </div>
                <p class="text-[10px] text-gray-500 leading-relaxed">
                  إنهاء اتصال الجلسة تلقائياً وتسجيل خروج المستخدم عند خموله لمدة 30 دقيقة.
                </p>
              </div>

              <!-- Devices policy -->
              <div class="p-3.5 bg-gray-50/50 dark:bg-gray-950/40 border border-gray-150 dark:border-gray-850 rounded-xl">
                <div class="flex items-center justify-between mb-1.5">
                  <span class="text-xs font-bold text-gray-900 dark:text-white">تعدد الجلسات والأجهزة</span>
                  <span class="px-2 py-0.5 rounded text-[8px] bg-amber-50 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400 font-bold border border-amber-250/30">مراقب</span>
                </div>
                <p class="text-[10px] text-gray-500 leading-relaxed mb-2">
                  مراقبة الاتصالات المتزامنة من عدة متصفحات أو أجهزة وإنهاؤها الفوري.
                </p>
                <button
                  @click="$router.push({ name: 'ActiveSessions' })"
                  class="text-[9px] font-black text-brand-700 bg-brand-50 hover:bg-brand-100 dark:bg-brand-500/10 dark:text-brand-450 px-3 py-1.5 rounded-lg border border-brand-200/30 transition-all cursor-pointer"
                >
                  إدارة الأجهزة النشطة &larr;
                </button>
              </div>

              <!-- Integrity checklist -->
              <div class="pt-4 border-t border-gray-150 dark:border-gray-800">
                <span class="text-xs font-bold text-gray-900 dark:text-white block mb-2">امتثال الضوابط الأمنية</span>
                <div class="space-y-2">
                  <div class="flex items-center gap-2.5 text-[10px] text-gray-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-500 shrink-0" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                    </svg>
                    <span>تأمين هجمات تخمين كلمات السر (Brute-Force)</span>
                  </div>
                  <div class="flex items-center gap-2.5 text-[10px] text-gray-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-500 shrink-0" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                    </svg>
                    <span>فرض قواعد التعقيد وسياسات كلمات المرور</span>
                  </div>
                  <div class="flex items-center gap-2.5 text-[10px] text-gray-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-500 shrink-0" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                    </svg>
                    <span>تأمين ملفات الجلسات (CSRF & Session Lockout)</span>
                  </div>
                </div>
              </div>

            </div>

          </div>

        </div>

      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import api from '@/lib/api'
import Swal from 'sweetalert2'

interface UserRecord {
  id: number
  username: string
  full_name: string
  email: string
  is_active: boolean
  security_status?: {
    is_locked: boolean
    failed_attempts: number
    must_change_password: boolean
  }
}

interface LoginAudit {
  id: number
  action: string
  username_attempted: string
  ip_address: string
  user_agent: string
  geo_location: string
  failure_reason: string
  timestamp: string
}

const loading = ref(false)
const loadingLogs = ref(false)
const users = ref<UserRecord[]>([])
const failedLoginLogs = ref<LoginAudit[]>([])
const failedAttemptsCount = ref(0)
const activeSessionsCount = ref(0)
const activeFilter = ref('all')
const searchQuery = ref('')

// Compute filtered users based on active filter tab and search query
const filteredUsers = computed(() => {
  let list = users.value

  // Apply status filter tab
  if (activeFilter.value === 'active') {
    list = list.filter(u => u.is_active && !u.security_status?.is_locked)
  } else if (activeFilter.value === 'locked') {
    list = list.filter(u => u.security_status?.is_locked)
  } else if (activeFilter.value === 'inactive') {
    list = list.filter(u => !u.is_active)
  }

  // Apply search query
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(u => 
      u.username.toLowerCase().includes(q) || 
      (u.full_name && u.full_name.toLowerCase().includes(q)) ||
      (u.email && u.email.toLowerCase().includes(q))
    )
  }

  return list
})

const totalUsers = computed(() => users.value.length)
const lockedUsersCount = computed(() => {
  return users.value.filter(u => u.security_status?.is_locked).length
})

async function loadData() {
  loading.value = true
  try {
    const usersRes = await api.get('/users/', { params: { page_size: 500 } })
    users.value = usersRes.data.results || []
    
    // Calculate active sessions count from active sessions endpoint in telemetry
    const telRes = await api.get('/telemetry/dashboard/')
    activeSessionsCount.value = telRes.data?.data?.active_sessions?.active_count || 1
  } catch (err) {
    console.error('Failed to load users for governance:', err)
  } finally {
    loading.value = false
  }
}

async function loadLogs() {
  loadingLogs.value = true
  try {
    const attemptsRes = await api.get('/audit/logins/failed_attempts/')
    failedLoginLogs.value = attemptsRes.data.results || []
    failedAttemptsCount.value = attemptsRes.data.count || failedLoginLogs.value.length
  } catch (err) {
    console.error('Failed to load failed attempts:', err)
  } finally {
    loadingLogs.value = false
  }
}

function refreshAll() {
  loadData()
  loadLogs()
}

// Avatar Initials Helpers
function getUserInitials(name: string): string {
  if (!name) return 'U'
  return name.slice(0, 2).toUpperCase()
}

function getAvatarBgColor(username: string): string {
  const hash = username.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
  const colors = [
    'bg-blue-50 text-blue-700 border-blue-200/40 dark:bg-blue-900/30 dark:text-blue-400',
    'bg-indigo-50 text-indigo-700 border-indigo-200/40 dark:bg-indigo-900/30 dark:text-indigo-400',
    'bg-purple-50 text-purple-700 border-purple-200/40 dark:bg-purple-900/30 dark:text-purple-400',
    'bg-pink-50 text-pink-700 border-pink-200/40 dark:bg-pink-900/30 dark:text-pink-400',
    'bg-emerald-50 text-emerald-700 border-emerald-200/40 dark:bg-emerald-900/30 dark:text-emerald-400'
  ]
  return colors[hash % colors.length]
}

async function handleUnlockUser(user: UserRecord) {
  const result = await Swal.fire({
    title: 'تأكيد إلغاء قفل الحساب',
    text: `هل أنت متأكد من إلغاء قفل حساب "${user.username}" وتصفير عدد محاولات الدخول الخاطئة؟`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'تأكيد إلغاء القفل',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#10b981',
    cancelButtonColor: '#6b7280',
  })

  if (result.isConfirmed) {
    try {
      await api.post(`/users/${user.id}/unlock/`)
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: `تم إلغاء قفل الحساب ${user.username} وتصفير محاولاته`,
        showConfirmButton: false,
        timer: 3000
      })
      await loadData()
    } catch (err: any) {
      Swal.fire('خطأ', err.response?.data?.error || 'فشل إلغاء قفل الحساب', 'error')
    }
  }
}

async function handleResetPassword(user: UserRecord) {
  const { value: newPassword } = await Swal.fire({
    title: 'إعادة تعيين كلمة المرور',
    text: `سيتم فرض تغيير كلمة المرور للمستخدم "${user.username}" عند تسجيل الدخول القادم.`,
    input: 'text',
    inputLabel: 'أدخل كلمة مرور مؤقتة جديدة للمستخدم',
    inputValue: 'TempPass@2026',
    showCancelButton: true,
    confirmButtonText: 'تأكيد وحفظ',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#2563eb',
    cancelButtonColor: '#6b7280',
    inputValidator: (value) => {
      if (!value || value.length < 8) {
        return 'يجب أن لا تقل كلمة المرور المؤقتة عن 8 خانات'
      }
    }
  })

  if (newPassword) {
    try {
      await api.post(`/users/${user.id}/reset-password/`, { new_password: newPassword })
      Swal.fire({
        icon: 'success',
        title: 'نجحت العملية',
        text: `تم تعيين كلمة المرور المؤقتة لـ "${user.username}" وفرض تغييرها بنجاح.`,
        confirmButtonColor: '#2563eb',
      })
      await loadData()
    } catch (err: any) {
      Swal.fire('خطأ', err.response?.data?.error || 'فشل فرض إعادة تعيين كلمة المرور', 'error')
    }
  }
}

async function handleDeactivateUser(user: UserRecord) {
  const result = await Swal.fire({
    title: 'تعطيل الحساب',
    text: `هل أنت متأكد من تعطيل حساب "${user.username}"؟ لن يتمكن من تسجيل الدخول إلى النظام.`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'تأكيد التعطيل',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#6b7280',
  })

  if (result.isConfirmed) {
    try {
      await api.delete(`/users/${user.id}/`)
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: `تم تعطيل حساب ${user.username} بنجاح`,
        showConfirmButton: false,
        timer: 3000
      })
      await loadData()
    } catch (err: any) {
      Swal.fire('خطأ', err.response?.data?.error || 'فشل تعطيل الحساب', 'error')
    }
  }
}

async function handleActivateUser(user: UserRecord) {
  const result = await Swal.fire({
    title: 'تفعيل الحساب',
    text: `هل تريد إعادة تفعيل حساب المستخدم "${user.username}" والسماح له بالولوج للمنظومة؟`,
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'تأكيد التفعيل',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#10b981',
    cancelButtonColor: '#6b7280',
  })

  if (result.isConfirmed) {
    try {
      await api.post(`/users/${user.id}/activate/`)
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: `تم تفعيل حساب ${user.username} بنجاح`,
        showConfirmButton: false,
        timer: 3000
      })
      await loadData()
    } catch (err: any) {
      Swal.fire('خطأ', err.response?.data?.error || 'فشل تفعيل الحساب', 'error')
    }
  }
}

function getStatusFilterName(status: string): string {
  const names: Record<string, string> = {
    all: 'كل الحسابات',
    active: 'النشطة',
    locked: 'المقيدة أمنياً',
    inactive: 'المعطلة إدارياً'
  }
  return names[status] || status
}

function getUserStatusLabel(user: UserRecord): string {
  if (user.security_status?.is_locked) return 'مغلق أمنياً'
  return user.is_active ? 'نشط' : 'معطل إدارياً'
}

// Restored standard high-fidelity color theme classes
function getUserStatusClasses(user: UserRecord): string {
  if (user.security_status?.is_locked) {
    return 'bg-error-50 text-error-700 border-error-200 dark:bg-error-950/20 dark:text-error-400 dark:border-error-500/20'
  }
  return user.is_active 
    ? 'bg-success-50 text-success-700 border-success-200 dark:bg-success-950/20 dark:text-success-400 dark:border-success-500/20' 
    : 'bg-gray-100 text-gray-600 border-gray-250/20 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-700/20'
}

function getUserStatusDotClass(user: UserRecord): string {
  if (user.security_status?.is_locked) return 'bg-error-500'
  return user.is_active ? 'bg-success-500' : 'bg-gray-400'
}

function formatFailureReason(reason: string): string {
  const reasons: Record<string, string> = {
    invalid_password: 'كلمة مرور خاطئة',
    account_locked: 'حساب مغلق مؤقتاً',
    account_disabled: 'حساب معطل',
    user_not_found: 'مستخدم غير مسجل',
    two_factor_failed: 'فشل التحقق الثنائي',
    session_expired: 'جلسة منتهية الصلاحية',
  }
  return reasons[reason] || reason || 'فشل مجهول'
}

function formatDate(dateStr: string): string {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  return date.toLocaleString('ar-YE', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

onMounted(() => {
  loadData()
  loadLogs()
})
</script>
