<template>
  <admin-layout>
    <div class="space-y-8 pb-20 relative min-h-screen">
      <!-- ─── Subtle Background Glows ─────────────────────────────────── -->
      <div class="absolute top-0 left-1/4 w-96 h-96 bg-brand-500/10 rounded-full blur-[100px] -z-10 pointer-events-none mix-blend-multiply dark:mix-blend-lighten"></div>
      <div class="absolute top-40 right-1/4 w-96 h-96 bg-red-500/10 rounded-full blur-[100px] -z-10 pointer-events-none mix-blend-multiply dark:mix-blend-lighten"></div>

      <!-- ─── Page Header ─────────────────────────────────────────────── -->
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 relative z-10 bg-white/40 dark:bg-gray-900/40 backdrop-blur-xl border border-white/60 dark:border-gray-800/60 p-6 rounded-3xl shadow-sm">
        <div class="flex items-start gap-4">
          <div class="relative flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 shadow-lg shadow-brand-500/30 overflow-hidden shrink-0">
            <!-- Radar sweep animation -->
            <div class="absolute inset-0 border-2 border-transparent rounded-2xl animate-[spin_4s_linear_infinite]" style="border-top-color: rgba(255,255,255,0.4); border-radius: 50%"></div>
            <svg class="w-7 h-7 text-white relative z-10" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
          </div>
          <div>
            <h2 class="text-3xl font-black bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-400 bg-clip-text text-transparent tracking-tight">لوحة الإنذارات المبكرة</h2>
            <p class="mt-1.5 text-sm font-medium text-gray-500 dark:text-gray-400 flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
              المحرك الاستباقي — يفحص السجلات ويحسب الاستحقاقات برمجياً
            </p>
          </div>
        </div>
        
        <div class="flex flex-wrap items-center gap-3">
          <!-- Filter by warning type -->
          <div class="relative">
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <svg class="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/></svg>
            </div>
            <select
              v-model="activeFilter"
              class="h-11 appearance-none rounded-xl border border-gray-200/80 bg-white/80 pr-10 pl-8 py-2 text-sm font-medium text-gray-700 shadow-sm backdrop-blur-md focus:border-brand-500 focus:outline-none focus:ring-4 focus:ring-brand-500/10 dark:border-gray-700/80 dark:bg-gray-800/80 dark:text-gray-200 transition-all hover:bg-white dark:hover:bg-gray-800 cursor-pointer"
            >
              <option value="">جميع الإنذارات النشطة</option>
              <option value="exceeded">تجاوزوا السن أو المدة</option>
              <option value="critical">حالة حرجة (أقل من شهر)</option>
              <option value="high">حالة عالية (أقل من 3 أشهر)</option>
              <option value="medium">حالة متوسطة (أقل من 6 أشهر)</option>
              <option value="info">بيانات ناقصة أو غير مكتملة</option>
              <option value="temp">حالات مؤقتة (انتهاء مدة)</option>
            </select>
          </div>

          <button
            @click="runEngine"
            :disabled="loading"
            class="group relative flex items-center gap-2 h-11 rounded-xl bg-gray-900 dark:bg-white hover:bg-gray-800 dark:hover:bg-gray-100 disabled:opacity-70 px-5 text-sm font-bold text-white dark:text-gray-900 shadow-lg shadow-gray-900/20 dark:shadow-white/10 transition-all hover:-translate-y-0.5 active:translate-y-0 overflow-hidden"
          >
            <div class="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]"></div>
            <svg :class="['w-4 h-4 relative z-10', loading && 'animate-[spin_1s_ease-in-out_infinite]']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span class="relative z-10">{{ loading ? 'جاري المسح العميق...' : 'تحديث البيانات' }}</span>
          </button>
        </div>
      </div>

      <!-- ─── Stats Cards ────────────────────────────────────────────── -->
      <div v-if="stats" class="grid grid-cols-2 md:grid-cols-5 gap-5">
        <!-- تجاوزوا السن -->
        <div
          @click="activeFilter = activeFilter === 'exceeded' ? '' : 'exceeded'"
          :class="['group cursor-pointer rounded-3xl p-5 transition-all duration-300 relative overflow-hidden', activeFilter === 'exceeded' ? 'bg-red-500 text-white shadow-xl shadow-red-500/30 scale-[1.02]' : 'bg-white dark:bg-gray-800 border border-red-100 dark:border-red-900/30 hover:border-red-300 hover:shadow-lg hover:-translate-y-1']"
        >
          <div v-if="activeFilter !== 'exceeded'" class="absolute inset-0 bg-gradient-to-br from-red-50/50 to-transparent dark:from-red-900/10 pointer-events-none"></div>
          <div class="flex items-center justify-between mb-4 relative z-10">
            <div :class="['w-10 h-10 rounded-xl flex items-center justify-center transition-colors', activeFilter === 'exceeded' ? 'bg-white/20' : 'bg-red-100 dark:bg-red-500/20 text-red-600 dark:text-red-400']">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
            </div>
            <span :class="['text-xs font-bold px-2 py-1 rounded-lg', activeFilter === 'exceeded' ? 'bg-white/20' : 'bg-red-50 text-red-600 dark:bg-red-500/10 dark:text-red-400']">حرج جداً</span>
          </div>
          <div class="relative z-10">
            <div :class="['text-sm font-semibold mb-1', activeFilter === 'exceeded' ? 'text-white/80' : 'text-gray-500 dark:text-gray-400']">تجاوزوا السن أو المدة</div>
            <div class="text-4xl font-black tracking-tight flex items-baseline gap-2">
              {{ stats.exceeded_age + stats.exceeded_service }}
              <span :class="['text-xs font-medium', activeFilter === 'exceeded' ? 'text-white/70' : 'text-gray-400']">فرد</span>
            </div>
            <div :class="['text-xs mt-3 flex items-center gap-1.5', activeFilter === 'exceeded' ? 'text-white/70' : 'text-red-600/70 dark:text-red-400/70']">
              <span>{{ stats.exceeded_age }} بالعمر</span>
              <span class="w-1 h-1 rounded-full bg-current opacity-50"></span>
              <span>{{ stats.exceeded_service }} بالمدة</span>
            </div>
          </div>
        </div>

        <!-- مقتربون -->
        <div
          @click="activeFilter = activeFilter === 'medium' ? '' : 'medium'"
          :class="['group cursor-pointer rounded-3xl p-5 transition-all duration-300 relative overflow-hidden', activeFilter === 'medium' ? 'bg-orange-500 text-white shadow-xl shadow-orange-500/30 scale-[1.02]' : 'bg-white dark:bg-gray-800 border border-orange-100 dark:border-orange-900/30 hover:border-orange-300 hover:shadow-lg hover:-translate-y-1']"
        >
          <div v-if="activeFilter !== 'medium'" class="absolute inset-0 bg-gradient-to-br from-orange-50/50 to-transparent dark:from-orange-900/10 pointer-events-none"></div>
          <div class="flex items-center justify-between mb-4 relative z-10">
            <div :class="['w-10 h-10 rounded-xl flex items-center justify-center transition-colors', activeFilter === 'medium' ? 'bg-white/20' : 'bg-orange-100 dark:bg-orange-500/20 text-orange-600 dark:text-orange-400']">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
            <span :class="['text-xs font-bold px-2 py-1 rounded-lg', activeFilter === 'medium' ? 'bg-white/20' : 'bg-orange-50 text-orange-600 dark:bg-orange-500/10 dark:text-orange-400']">تنبيه مستمر</span>
          </div>
          <div class="relative z-10">
            <div :class="['text-sm font-semibold mb-1', activeFilter === 'medium' ? 'text-white/80' : 'text-gray-500 dark:text-gray-400']">إنذار تقاعد مبكر</div>
            <div class="text-4xl font-black tracking-tight flex items-baseline gap-2">
              {{ stats.approaching }}
              <span :class="['text-xs font-medium', activeFilter === 'medium' ? 'text-white/70' : 'text-gray-400']">فرد</span>
            </div>
            <div :class="['text-xs mt-3 flex items-center gap-1.5', activeFilter === 'medium' ? 'text-white/70' : 'text-orange-600/70 dark:text-orange-400/70']">
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              أقل من {{ settings?.warning_months || 6 }} أشهر على التقاعد
            </div>
          </div>
        </div>

        <!-- حالات مؤقتة -->
        <div
          @click="activeFilter = activeFilter === 'temp' ? '' : 'temp'"
          :class="['group cursor-pointer rounded-3xl p-5 transition-all duration-300 relative overflow-hidden', activeFilter === 'temp' ? 'bg-purple-600 text-white shadow-xl shadow-purple-500/30 scale-[1.02]' : 'bg-white dark:bg-gray-800 border border-purple-100 dark:border-purple-900/30 hover:border-purple-300 hover:shadow-lg hover:-translate-y-1']"
        >
          <div v-if="activeFilter !== 'temp'" class="absolute inset-0 bg-gradient-to-br from-purple-50/50 to-transparent dark:from-purple-900/10 pointer-events-none"></div>
          <div class="flex items-center justify-between mb-4 relative z-10">
            <div :class="['w-10 h-10 rounded-xl flex items-center justify-center transition-colors', activeFilter === 'temp' ? 'bg-white/20' : 'bg-purple-100 dark:bg-purple-500/20 text-purple-600 dark:text-purple-400']">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
            </div>
            <span :class="['text-xs font-bold px-2 py-1 rounded-lg', activeFilter === 'temp' ? 'bg-white/20' : 'bg-purple-50 text-purple-600 dark:bg-purple-500/10 dark:text-purple-400']">متابعة إدارية</span>
          </div>
          <div class="relative z-10">
            <div :class="['text-sm font-semibold mb-1', activeFilter === 'temp' ? 'text-white/80' : 'text-gray-500 dark:text-gray-400']">حالات مؤقتة منتهية</div>
            <div class="text-4xl font-black tracking-tight flex items-baseline gap-2">
              {{ stats.temp_status_ending }}
              <span :class="['text-xs font-medium', activeFilter === 'temp' ? 'text-white/70' : 'text-gray-400']">ملف</span>
            </div>
            <div :class="['text-xs mt-3 flex items-center gap-1.5', activeFilter === 'temp' ? 'text-white/70' : 'text-purple-600/70 dark:text-purple-400/70']">
              دراسة / سجن / انتداب / مرافقة
            </div>
          </div>
        </div>

        <!-- بيانات ناقصة -->
        <div
          @click="activeFilter = activeFilter === 'info' ? '' : 'info'"
          :class="['group cursor-pointer rounded-3xl p-5 transition-all duration-300 relative overflow-hidden', activeFilter === 'info' ? 'bg-yellow-500 text-white shadow-xl shadow-yellow-500/30 scale-[1.02]' : 'bg-white dark:bg-gray-800 border border-yellow-100 dark:border-yellow-900/30 hover:border-yellow-300 hover:shadow-lg hover:-translate-y-1']"
        >
          <div v-if="activeFilter !== 'info'" class="absolute inset-0 bg-gradient-to-br from-yellow-50/50 to-transparent dark:from-yellow-900/10 pointer-events-none"></div>
          <div class="flex items-center justify-between mb-4 relative z-10">
            <div :class="['w-10 h-10 rounded-xl flex items-center justify-center transition-colors', activeFilter === 'info' ? 'bg-white/20' : 'bg-yellow-100 dark:bg-yellow-500/20 text-yellow-600 dark:text-yellow-400']">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
            <span :class="['text-xs font-bold px-2 py-1 rounded-lg', activeFilter === 'info' ? 'bg-white/20' : 'bg-yellow-50 text-yellow-700 dark:bg-yellow-500/10 dark:text-yellow-400']">تحديث مطلوب</span>
          </div>
          <div class="relative z-10">
            <div :class="['text-sm font-semibold mb-1', activeFilter === 'info' ? 'text-white/80' : 'text-gray-500 dark:text-gray-400']">بيانات ناقصة</div>
            <div class="text-4xl font-black tracking-tight flex items-baseline gap-2">
              {{ stats.missing_data }}
              <span :class="['text-xs font-medium', activeFilter === 'info' ? 'text-white/70' : 'text-gray-400']">سجل</span>
            </div>
            <div :class="['text-xs mt-3 flex items-center gap-1.5', activeFilter === 'info' ? 'text-white/70' : 'text-yellow-700/70 dark:text-yellow-400/70']">
              المحرك عاجز عن تقييم حالتهم
            </div>
          </div>
        </div>

        <!-- الإجمالي -->
        <div class="rounded-3xl p-5 border border-brand-100 dark:border-brand-900/40 bg-gradient-to-br from-brand-50 to-white dark:from-brand-900/20 dark:to-gray-800 relative overflow-hidden shadow-sm">
          <div class="absolute -right-4 -bottom-4 opacity-5 dark:opacity-10 text-brand-600">
            <svg class="w-32 h-32" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2zm0 4.5l6.5 13h-13L12 6.5z"/></svg>
          </div>
          <div class="flex items-center justify-between mb-4 relative z-10">
            <div class="w-10 h-10 rounded-xl bg-brand-100 dark:bg-brand-500/20 flex items-center justify-center text-brand-600 dark:text-brand-400">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
            </div>
            <span class="text-xs font-bold px-2 py-1 rounded-lg bg-brand-50 text-brand-700 dark:bg-brand-500/10 dark:text-brand-400">حصيلة النظام</span>
          </div>
          <div class="relative z-10">
            <div class="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-1">إجمالي الإنذارات</div>
            <div class="text-4xl font-black tracking-tight flex items-baseline gap-2 text-brand-700 dark:text-brand-400">
              {{ stats.total }}
              <span class="text-xs font-medium text-gray-400">إنذار نشط</span>
            </div>
            <div class="text-xs mt-3 text-brand-600/70 dark:text-brand-400/70">
              تم مسح جميع القوة النشطة
            </div>
          </div>
        </div>
      </div>

      <!-- ─── Active Settings Info ───────────────────────────────────── -->
      <div v-if="settings" class="flex flex-wrap items-center gap-2 p-4 bg-white/60 dark:bg-gray-900/60 backdrop-blur-xl border border-gray-200/60 dark:border-gray-700/60 rounded-2xl shadow-sm">
        <div class="flex items-center gap-2 pr-2 border-l border-gray-200 dark:border-gray-700">
          <div class="w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
            <svg class="w-4 h-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/></svg>
          </div>
          <div>
            <div class="text-[10px] uppercase font-bold text-gray-400 tracking-wider">سن التقاعد المعتمد</div>
            <div class="text-sm font-black text-gray-900 dark:text-white">{{ settings.retirement_age }} سنة</div>
          </div>
        </div>
        
        <div class="flex items-center gap-2 pr-2 border-l border-gray-200 dark:border-gray-700">
          <div class="w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
            <svg class="w-4 h-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
          </div>
          <div>
            <div class="text-[10px] uppercase font-bold text-gray-400 tracking-wider">الحد الأدنى للخدمة</div>
            <div class="text-sm font-black text-gray-900 dark:text-white">{{ settings.min_service_years }} سنة</div>
          </div>
        </div>
        
        <div class="flex items-center gap-2 pr-2 border-l border-gray-200 dark:border-gray-700">
          <div class="w-8 h-8 rounded-full bg-orange-50 dark:bg-orange-500/10 flex items-center justify-center">
            <svg class="w-4 h-4 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
          <div>
            <div class="text-[10px] uppercase font-bold text-orange-400 tracking-wider">نطاق الإنذار للتقاعد</div>
            <div class="text-sm font-black text-orange-600 dark:text-orange-400">{{ settings.warning_months }} أشهر</div>
          </div>
        </div>

        <div class="flex items-center gap-2 pr-2 border-l border-gray-200 dark:border-gray-700">
          <div class="w-8 h-8 rounded-full bg-purple-50 dark:bg-purple-500/10 flex items-center justify-center">
            <svg class="w-4 h-4 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
          </div>
          <div>
            <div class="text-[10px] uppercase font-bold text-purple-400 tracking-wider">تنبيه الحالات المؤقتة</div>
            <div class="text-sm font-black text-purple-600 dark:text-purple-400">{{ settings.temp_warning_days }} يوم</div>
          </div>
        </div>

        <div class="flex items-center gap-2 pr-4 mr-auto">
          <router-link to="/settings" class="flex items-center gap-2 h-9 rounded-lg bg-gray-900 dark:bg-white px-4 text-xs font-bold text-white dark:text-gray-900 shadow-md transition-all hover:scale-105 active:scale-95">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
            تخصيص الإعدادات
          </router-link>
        </div>
      </div>

      <!-- ─── DataTable ──────────────────────────────────────────────── -->
      <div class="rounded-3xl bg-white dark:bg-gray-800/80 shadow-2xl shadow-gray-200/50 dark:shadow-black/20 overflow-hidden border border-gray-100 dark:border-gray-700/50 backdrop-blur-md">
        <DataTable
          :columns="columns"
          :data="filteredWarnings"
          row-key="military_number"
          :loading="loading"
          :error="error"
          :has-actions="true"
          :has-filters="false"
          :total-count="filteredWarnings.length"
          :total-pages="1"
          :current-page="1"
          search-placeholder="بحث برقم عسكري أو اسم الفرد..."
          empty-title="لا توجد إنذارات حالية"
          empty-description="لم يُعثر على أي أفراد يتطلبون تدخلاً بناءً على معايير النظام الحالية."
          @refresh="runEngine"
          @search="onSearch"
        >
          <!-- urgency badge -->
          <template #cell-urgency="{ value }">
            <span :class="urgencyClass(value)" class="inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-black tracking-wide border border-current/10">
              <span class="w-1.5 h-1.5 rounded-full inline-block shadow-sm" :class="urgencyDotClass(value)"></span>
              {{ urgencyLabel(value) }}
            </span>
          </template>

          <!-- warning type -->
          <template #cell-warning_type="{ value }">
            <span class="inline-flex items-center gap-1.5 rounded-lg bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 px-2.5 py-1 text-xs font-semibold text-gray-700 dark:text-gray-300">
              {{ warningTypeLabel(value) }}
            </span>
          </template>

          <!-- age -->
          <template #cell-age_years="{ row }">
            <div v-if="row.age_years !== null" class="flex flex-col">
              <span class="text-sm font-black text-gray-900 dark:text-white">{{ row.age_years }} سنة</span>
              <span v-if="row.age_months > 0" class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">{{ row.age_months }} أشهر إضافية</span>
            </div>
            <span v-else class="inline-flex items-center gap-1 text-xs font-bold text-yellow-600 dark:text-yellow-400 bg-yellow-50 dark:bg-yellow-500/10 px-2 py-0.5 rounded-md">
              <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              مفقود
            </span>
          </template>

          <!-- service -->
          <template #cell-service_years="{ row }">
            <div v-if="row.service_years !== null" class="flex flex-col">
              <span class="text-sm font-black text-gray-900 dark:text-white">{{ row.service_years }} سنة</span>
              <span v-if="row.service_months > 0" class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">{{ row.service_months }} أشهر إضافية</span>
            </div>
            <span v-else class="inline-flex items-center gap-1 text-xs font-bold text-yellow-600 dark:text-yellow-400 bg-yellow-50 dark:bg-yellow-500/10 px-2 py-0.5 rounded-md">
              <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              مفقود
            </span>
          </template>

          <!-- message -->
          <template #cell-message="{ value }">
            <p class="text-[13px] font-medium text-gray-600 dark:text-gray-300 max-w-sm leading-relaxed">{{ value }}</p>
          </template>

          <!-- Actions -->
          <template #actions="{ row }">
            <router-link
              :to="`/personnel/${row.military_number}`"
              class="group flex items-center gap-2 rounded-xl bg-white dark:bg-gray-700 hover:bg-brand-50 dark:hover:bg-brand-500/20 border border-gray-200 dark:border-gray-600 hover:border-brand-300 dark:hover:border-brand-500/50 px-4 py-2 text-xs font-bold text-gray-700 dark:text-gray-200 hover:text-brand-700 dark:hover:text-brand-300 shadow-sm transition-all hover:shadow-md active:scale-95"
            >
              <svg class="w-4 h-4 text-gray-400 group-hover:text-brand-500 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
              فتح الملف
            </router-link>
          </template>
        </DataTable>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import DataTable from '@/components/tables/DataTable.vue'
import api from '@/lib/api'

// ─── State ─────────────────────────────────────────────────────────────────
const loading = ref(false)
const error = ref<string | null>(null)
const warnings = ref<any[]>([])
const stats = ref<any>(null)
const settings = ref<any>(null)
const activeFilter = ref('')
const searchQuery = ref('')

// ─── Columns ────────────────────────────────────────────────────────────────
const columns = [
  { key: 'urgency',        label: 'الخطورة',        minWidth: '120px' },
  { key: 'warning_type',   label: 'نوع الإنذار',    minWidth: '130px' },
  { key: 'military_number',label: 'الرقم العسكري',  minWidth: '100px' },
  { key: 'full_name',      label: 'الاسم الكامل',   minWidth: '160px' },
  { key: 'rank',           label: 'الرتبة',         minWidth: '90px'  },
  { key: 'security_admin', label: 'جهة الأمن',      minWidth: '120px' },
  { key: 'unit',           label: 'الوحدة',         minWidth: '110px' },
  { key: 'age_years',      label: 'العمر الحقيقي',  minWidth: '110px' },
  { key: 'service_years',  label: 'مدة الخدمة',     minWidth: '110px' },
  { key: 'message',        label: 'تفاصيل الإنذار', minWidth: '220px' },
]

// ─── Computed ───────────────────────────────────────────────────────────────
const filteredWarnings = computed(() => {
  let data = warnings.value
  if (activeFilter.value) {
    if (activeFilter.value === 'temp') {
      data = data.filter(w => w.warning_type === 'temp_status_ended' || w.warning_type === 'temp_status_ending_soon')
    } else {
      data = data.filter(w => w.urgency === activeFilter.value)
    }
  }
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    data = data.filter(w =>
      w.military_number?.toLowerCase().includes(q) ||
      w.full_name?.toLowerCase().includes(q) ||
      w.rank?.toLowerCase().includes(q) ||
      w.unit?.toLowerCase().includes(q)
    )
  }
  return data
})

// ─── Urgency Helpers ────────────────────────────────────────────────────────
const urgencyLabel = (v: string) => ({
  exceeded: 'حالة متجاوزة',
  critical: 'أولوية قصوى',
  high:     'عالي الأهمية',
  medium:   'متوسط الأهمية',
  low:      'منخفض الأهمية',
  info:     'تنبيه / معلومات',
}[v] || v)

const urgencyClass = (v: string) => ({
  exceeded: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300',
  critical: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300',
  high:     'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300',
  medium:   'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300',
  low:      'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300',
  info:     'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300',
}[v] || 'bg-gray-100 text-gray-700')

const urgencyDotClass = (v: string) => ({
  exceeded: 'bg-red-500',
  critical: 'bg-red-500 animate-pulse',
  high:     'bg-orange-500',
  medium:   'bg-amber-500',
  low:      'bg-yellow-500',
  info:     'bg-blue-400',
}[v] || 'bg-gray-400')

const warningTypeLabel = (v: string) => ({
  age_exceeded:              'تجاوز السن',
  age_approaching:           'اقتراب من التقاعد',
  service_exceeded:          'أكمل مدة الخدمة',
  missing_data:              'بيانات ناقصة',
  temp_status_ended:         'حالة مؤقتة منتهية',
  temp_status_ending_soon:   'حالة مؤقتة تنتهي قريباً',
}[v] || v)

// ─── Engine ─────────────────────────────────────────────────────────────────
const runEngine = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await api.get('/personnel/early-warnings/')
    warnings.value = res.data.results || []
    stats.value = res.data.stats || null
    settings.value = res.data.settings || null
  } catch (e: any) {
    error.value = e?.response?.data?.detail || 'فشل في تشغيل محرك الفحص'
  } finally {
    loading.value = false
  }
}

const onSearch = (q: string) => {
  searchQuery.value = q
}

onMounted(() => {
  runEngine()
})
</script>
