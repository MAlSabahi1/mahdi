<template>
  <admin-layout>
    <!-- Breadcrumb (Unified) -->
    <PageBreadcrumb :pageTitle="$t('nav.dashboard') || 'لوحة التحكم'" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Top Dynamic Filter Header (Designed exactly like the university system reference) -->
      <div class="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-4 border-b border-gray-200 dark:border-gray-800 pb-5">
        <div>
          <h1 class="text-2xl font-black text-gray-900 dark:text-white">
            {{ dashboardData.title }}
          </h1>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            بوابة الإحصائيات والمؤشرات التفاعلية العامة للنظام النشط.
          </p>
        </div>

        <!-- Filters & Control Actions (Feels exactly like the screenshot: filters, date-ranges, action button) -->
        <div class="flex flex-wrap items-center gap-3" dir="ltr">
          
          <!-- Normal Login Mock Button (تسجيل دخول عادي) -->
          <button class="flex items-center gap-1.5 border border-brand-200 bg-brand-50/50 hover:bg-brand-50 dark:border-brand-900/30 dark:bg-brand-950/20 text-brand-700 dark:text-brand-400 rounded-xl px-4 py-2 text-xs font-bold transition-all cursor-pointer">
            <span class="h-2 w-2 rounded-full bg-brand-500 animate-ping"></span>
            تسجيل دخول عادي
          </button>

          <!-- Date Dropdown (شهري / Monthly) -->
          <select class="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs font-bold text-gray-700 dark:border-gray-800 dark:bg-gray-950 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-brand-500 cursor-pointer">
            <option>شهري / Monthly</option>
            <option>يومي / Daily</option>
            <option>سنوي / Yearly</option>
          </select>
          
          <!-- Date Range Inputs -->
          <div class="flex items-center gap-2 rounded-xl border border-gray-200 bg-white px-2.5 py-1.5 dark:border-gray-800 dark:bg-gray-950">
            <input type="date" class="bg-transparent text-xs font-semibold text-gray-700 dark:text-gray-300 focus:outline-none" value="2026-07-01" />
            <span class="text-gray-400 text-xs font-bold">←</span>
            <input type="date" class="bg-transparent text-xs font-semibold text-gray-700 dark:text-gray-300 focus:outline-none" value="2026-07-31" />
          </div>

          <!-- Refresh Button (تحديث) -->
          <button class="flex items-center gap-1 bg-brand-600 hover:bg-brand-700 text-white rounded-xl px-4 py-2.5 text-xs font-black transition-all cursor-pointer shadow-sm shadow-brand-500/20">
            <svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 8H17" />
            </svg>
            تحديث
          </button>
        </div>
      </div>

      <!-- Educational Portal Banner (Dynamically explains the current active dashboard context based on active system) -->
      <div class="rounded-2xl border border-blue-150 bg-blue-50/40 p-5 dark:border-blue-900/30 dark:bg-blue-950/20">
        <div class="flex gap-3 items-center">
          <div class="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-600 text-white shrink-0">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h4 class="text-sm font-bold text-blue-950 dark:text-blue-200">
              البوابة المركزية الموحدة للأنظمة (عرض هيكلي وتجريبي محاكي)
            </h4>
            <p class="text-xs text-blue-700/80 dark:text-blue-300/80 mt-1 leading-relaxed">
              <strong>تنبيه توضيحي للمطورين والإدارة:</strong> هذه اللوحة تفاعلية ومرنة؛ حيث تتبدل تلقائياً وفق رتب وصلاحيات المستخدمين ونطاقهم الجغرافي (على سبيل المثال: عند دخول <strong>مدير النظام العام</strong> يُعرض له إجمالي إحصائيات كافة المحافظات، بينما عند دخول <strong>مدير محافظة أو فرع معين</strong> يتم تقييد وعرض البيانات الخاصة بنطاقه الجغرافي فقط). إن التصميم الحالي هو نموذج تجريبي محاكي، وسيتم تصميم وتطوير لوحة التحكم الإنتاجية النهائية بما يتوافق مع أفضل المعايير العالمية وأحدث ممارسات تجربة المستخدم (UI/UX) وهندسة البيانات.
            </p>
          </div>
        </div>
      </div>

      <!-- Dynamic Cards Grid (Feels exactly like the 4 cards in the screenshot) -->
      <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div 
          v-for="(card, index) in dashboardData.cards" 
          :key="index" 
          class="relative overflow-hidden rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03] transition-all duration-300 hover:-translate-y-1 hover:shadow-lg"
        >
          <!-- Top Row: Badge status + Icon (Matches the screenshot layout) -->
          <div class="flex justify-between items-center mb-4">
            <span :class="['text-[10px] font-black px-2.5 py-1 rounded-full tracking-wide uppercase', card.badgeClass]">
              {{ card.badgeText }}
            </span>
            <div :class="['h-9 w-9 rounded-xl flex items-center justify-center text-white shadow-sm', card.iconBg]">
              <!-- Custom rendered micro-icons inside dashboard card -->
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" :d="card.iconPath" />
              </svg>
            </div>
          </div>
          
          <!-- Middle Row: Label + Large Value (Exactly like the photo structure) -->
          <p class="text-[11px] text-gray-500 dark:text-gray-400 font-bold tracking-wider">{{ card.label }}</p>
          <h3 class="text-2xl font-black text-gray-900 dark:text-white mt-1.5 flex items-baseline gap-1.5">
            {{ card.value }}
            <span class="text-xs font-semibold text-gray-400 dark:text-gray-500">{{ card.unit }}</span>
          </h3>
          
          <!-- Bottom Row: Subtext Status -->
          <p class="text-xs text-gray-400 dark:text-gray-500 mt-3.5 flex items-center gap-1.5 font-medium">
            <span class="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            {{ card.subtext }}
          </p>

          <!-- Bottom colored indicator line (Like the colorful bottom border in university system screenshot) -->
          <div class="absolute bottom-0 left-0 right-0 h-1.5 transition-all" :style="{ backgroundColor: card.lineColor }"></div>
        </div>
      </div>

      <!-- Charts & Visual Trends (Layout mirrors the bottom section of the university system screenshot) -->
      <div class="grid gap-6 lg:grid-cols-12">
        
        <!-- Right Section: Trend chart (e.g. Force growth or document flow) -->
        <div class="lg:col-span-8 rounded-2xl border border-gray-200 bg-white p-6 dark:border-gray-800 dark:bg-white/[0.03]">
          <div class="flex justify-between items-center mb-6">
            <div>
              <h3 class="text-lg font-black text-gray-900 dark:text-white">{{ dashboardData.chartTitle }}</h3>
              <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">{{ dashboardData.chartSubtitle }}</p>
            </div>
            
            <div class="flex items-center gap-1.5 text-xs text-gray-400 dark:text-gray-500 font-bold">
              <span class="h-2.5 w-2.5 rounded-full bg-brand-500"></span>
              معدل النمو والنشاط العام
            </div>
          </div>

          <!-- Simulated High-Quality SVG Graph (Perfect visual layout matching) -->
          <div class="h-64 w-full flex items-end">
            <svg class="w-full h-full overflow-visible" viewBox="0 0 500 200" preserveAspectRatio="none">
              <!-- Y-Axis Grid Lines -->
              <line x1="0" y1="50" x2="500" y2="50" stroke="rgba(156, 163, 175, 0.08)" stroke-dasharray="4" />
              <line x1="0" y1="100" x2="500" y2="100" stroke="rgba(156, 163, 175, 0.08)" stroke-dasharray="4" />
              <line x1="0" y1="150" x2="500" y2="150" stroke="rgba(156, 163, 175, 0.08)" stroke-dasharray="4" />
              <line x1="0" y1="200" x2="500" y2="200" stroke="rgba(156, 163, 175, 0.08)" stroke-dasharray="4" />
              
              <!-- Graph Line Path -->
              <path :d="dashboardData.svgPath" fill="none" stroke="#2563eb" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
              
              <!-- Gradient under the curve -->
              <path :d="dashboardData.svgPathArea" fill="url(#brand-gradient)" opacity="0.15" />
              
              <defs>
                <linearGradient id="brand-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#2563eb" />
                  <stop offset="100%" stop-color="#2563eb" stop-opacity="0" />
                </linearGradient>
              </defs>
            </svg>
          </div>
        </div>

        <!-- Left Section: Sub-analytics / Progress bars -->
        <div class="lg:col-span-4 rounded-2xl border border-gray-200 bg-white p-6 dark:border-gray-800 dark:bg-white/[0.03]">
          <h3 class="text-lg font-black text-gray-900 dark:text-white mb-2">{{ dashboardData.secondaryTitle }}</h3>
          <p class="text-xs text-gray-400 dark:text-gray-500 mb-6">{{ dashboardData.secondarySubtitle }}</p>

          <!-- Dynamic Progress Bars (Exactly like the progress indicators in screenshot) -->
          <div class="space-y-5">
            <div v-for="(bar, index) in dashboardData.bars" :key="index" class="space-y-2">
              <div class="flex justify-between items-center text-xs font-bold">
                <span class="text-gray-700 dark:text-gray-300">{{ bar.label }}</span>
                <span class="text-gray-900 dark:text-white">{{ bar.valueText }}</span>
              </div>
              <div class="h-2.5 w-full bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                <div class="h-full rounded-full transition-all duration-700" :class="bar.bgClass" :style="{ width: bar.width }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Footer Note to seal the proposal context -->
      <p class="text-[11px] text-gray-400 dark:text-gray-500 text-center leading-relaxed">
        * كافة المؤشرات، الأرقام والبيانات الرسومية المعروضة أعلاه هي محاكاة تفاعلية ذكية للبروتوكول الهيكلي، ويتم ربطها بقاعدة البيانات بناءً على صلاحيات المستخدم والنظام المحدد.
      </p>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useSystemStore } from '@/stores/system'
import AdminLayout from '../components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'

const systemStore = useSystemStore()

// SVG icon paths for standard dashboard cards
const icons = {
  users: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z',
  security: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z',
  docs: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
  chart: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
}

const dashboardData = computed(() => {
  const system = systemStore.currentSystem

  if (system === 'secretariat') {
    return {
      title: 'لوحة نظام السكرتارية والوثائق',
      chartTitle: 'معدل تدفق المراسلات اليومي',
      chartSubtitle: 'إحصائيات الوارد والصادر خلال الـ 24 ساعة الماضية',
      secondaryTitle: 'إنجاز المراسلات حسب التصنيف',
      secondarySubtitle: 'نسبة أرشفة وتصدير الوثائق والمراسلات الكلية',
      svgPath: 'M 0 150 Q 100 120 200 130 T 400 80 T 500 100',
      svgPathArea: 'M 0 150 Q 100 120 200 130 T 400 80 T 500 100 L 500 200 L 0 200 Z',
      cards: [
        {
          label: 'المراسلات الواردة اليوم',
          value: '48',
          unit: 'معاملة',
          badgeText: '+15% زيادة',
          badgeClass: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400',
          iconPath: icons.docs,
          iconBg: 'bg-blue-600',
          lineColor: '#2563eb',
          subtext: 'الوارد الخارجي: 20'
        },
        {
          label: 'المراسلات الصادرة اليوم',
          value: '32',
          unit: 'معاملة',
          badgeText: 'مستقر',
          badgeClass: 'bg-blue-50 text-blue-700 dark:bg-blue-500/10 dark:text-brand-400',
          iconPath: icons.docs,
          iconBg: 'bg-emerald-600',
          lineColor: '#10b981',
          subtext: 'الصادر للوزارات: 18'
        },
        {
          label: 'معاملات تنتظر التوقيع',
          value: '15',
          unit: 'وثيقة',
          badgeText: 'عاجل',
          badgeClass: 'bg-rose-50 text-rose-700 dark:bg-rose-500/10 dark:text-rose-400',
          iconPath: icons.docs,
          iconBg: 'bg-amber-600',
          lineColor: '#f59e0b',
          subtext: 'تنتظر اعتماد المدير'
        },
        {
          label: 'إجمالي الأرشيف السحابي',
          value: '24.5',
          unit: 'ألف وثيقة',
          badgeText: 'مؤرشف',
          badgeClass: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400',
          iconPath: icons.chart,
          iconBg: 'bg-indigo-600',
          lineColor: '#ef4444',
          subtext: 'المساحة: 120 جيجابايت'
        }
      ],
      bars: [
        { label: 'مراسلات المحافظات والمحاور', width: '82%', valueText: '82% منجز', bgClass: 'bg-blue-500' },
        { label: 'الخطابات الدبلوماسية والوزارية', width: '65%', valueText: '65% منجز', bgClass: 'bg-amber-500' },
        { label: 'التعاميم والتكليفات الإدارية', width: '95%', valueText: '95% منجز', bgClass: 'bg-emerald-500' }
      ]
    }
  } else if (system === 'services_personnel') {
    // Exactly matches the metrics shown in the university system screenshot!
    return {
      title: 'لوحة نظام الخدمات والأفراد',
      chartTitle: 'اتجاه تسجيل القوة والطلاب',
      chartSubtitle: 'متابعة نمو أعداد القيد الجديد شهرياً للفروع',
      secondaryTitle: 'التحصيل ومطابقة كشوفات الرواتب',
      secondarySubtitle: 'معدل مطابقة السجلات في نظام الخدمات المالية والرواتب',
      svgPath: 'M 0 160 Q 120 140 250 80 T 500 50',
      svgPathArea: 'M 0 160 Q 120 140 250 80 T 500 50 L 500 200 L 0 200 Z',
      cards: [
        {
          label: 'إجمالي الأفراد والطلاب',
          value: '234',
          unit: 'طالب/فرد',
          badgeText: 'نشط 100%',
          badgeClass: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400',
          iconPath: icons.users,
          iconBg: 'bg-blue-600',
          lineColor: '#3b82f6',
          subtext: 'نشط: 233 طالب'
        },
        {
          label: 'إجمالي الضباط والموظفين',
          value: '19',
          unit: 'موظف/ضابط',
          badgeText: 'نشط 68%',
          badgeClass: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400',
          iconPath: icons.users,
          iconBg: 'bg-emerald-600',
          lineColor: '#10b981',
          subtext: 'نشط: 13 موظف'
        },
        {
          label: 'المسرحين والخريجين',
          value: '11',
          unit: 'مسرح',
          badgeText: 'مستقر',
          badgeClass: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300',
          iconPath: icons.users,
          iconBg: 'bg-amber-600',
          lineColor: '#eab308',
          subtext: 'لهذا العام: 0'
        },
        {
          label: 'إجمالي الدفعات والكشوفات',
          value: '44',
          unit: 'دفعة',
          badgeText: 'نشط 100%',
          badgeClass: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400',
          iconPath: icons.chart,
          iconBg: 'bg-red-600',
          lineColor: '#ef4444',
          subtext: 'نشط: 44 دفعة'
        }
      ],
      bars: [
        { label: 'التحصيل ومطابقة رواتب الأفراد', width: '88%', valueText: '88% مطابقة', bgClass: 'bg-emerald-500' },
        { label: 'مستندات الصرف والاعتماد المالي', width: '92%', valueText: '92% معتمدة', bgClass: 'bg-blue-500' },
        { label: 'التدقيق الجغرافي لفروع المحافظات', width: '75%', valueText: '75% تدقيق', bgClass: 'bg-purple-500' }
      ]
    }
  } else if (system === 'users_permissions') {
    return {
      title: 'لوحة إدارة المستخدمين والصلاحيات',
      chartTitle: 'معدل نشاط المستخدمين وتكرار الدخول',
      chartSubtitle: 'متابعة النشاط الأسبوعي على مستوى الأنظمة الأربعة',
      secondaryTitle: 'نسب معالجة طلبات الأمان',
      secondarySubtitle: 'قياس الاستجابة والتحقق من حسابات مدراء النظام',
      svgPath: 'M 0 140 Q 100 170 200 110 T 500 70',
      svgPathArea: 'M 0 140 Q 100 170 200 110 T 500 70 L 500 200 L 0 200 Z',
      cards: [
        {
          label: 'إجمالي حسابات المستخدمين',
          value: '145',
          unit: 'مستخدم',
          badgeText: 'نشط 95%',
          badgeClass: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400',
          iconPath: icons.users,
          iconBg: 'bg-blue-600',
          lineColor: '#2563eb',
          subtext: 'الحسابات المعطلة: 5'
        },
        {
          label: 'مجموعات الصلاحيات (Roles)',
          value: '8',
          unit: 'مجموعات',
          badgeText: 'محدد',
          badgeClass: 'bg-blue-50 text-blue-700 dark:bg-blue-500/10 dark:text-brand-400',
          iconPath: icons.security,
          iconBg: 'bg-indigo-600',
          lineColor: '#10b981',
          subtext: 'صلاحيات مخصصة: 12'
        },
        {
          label: 'طلبات إعادة تعيين كلمة المرور',
          value: '3',
          unit: 'طلبات',
          badgeText: 'معلق',
          badgeClass: 'bg-amber-50 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400',
          iconPath: icons.security,
          iconBg: 'bg-amber-600',
          lineColor: '#f59e0b',
          subtext: 'تحت التحقق الثنائي'
        },
        {
          label: 'مستخدمين نشطين حالياً',
          value: '18',
          unit: 'مستخدم',
          badgeText: 'نشط الآن',
          badgeClass: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400',
          iconPath: icons.chart,
          iconBg: 'bg-emerald-600',
          lineColor: '#ef4444',
          subtext: 'جلسات متزامنة: 20'
        }
      ],
      bars: [
        { label: 'نشاط مدراء الأنظمة الفرعية', width: '78%', valueText: '78% تفاعل', bgClass: 'bg-blue-500' },
        { label: 'استجابة معالجة طلبات الأمان', width: '90%', valueText: '90% سرعة', bgClass: 'bg-emerald-500' },
        { label: 'مراجعة تقارير تدقيق الصلاحيات', width: '60%', valueText: '60% مراجعة', bgClass: 'bg-amber-500' }
      ]
    }
  } else {
    // Default to 'administration' system
    return {
      title: 'لوحة الإدارة المركزية والتدقيق',
      chartTitle: 'استخدام الموارد وتدفق المعالجات الآلية',
      chartSubtitle: 'معدل معالجة الطلبات بالثانية وحالة الخوادم',
      secondaryTitle: 'استقرار المزامنة البينية',
      secondarySubtitle: 'مؤشر تكامل الفروع والنسخ الاحتياطي لقواعد البيانات',
      svgPath: 'M 0 170 Q 100 130 200 140 T 400 70 T 500 40',
      svgPathArea: 'M 0 170 Q 100 130 200 140 T 400 70 T 500 40 L 500 200 L 0 200 Z',
      cards: [
        {
          label: 'الأنظمة والوحدات الفعالة',
          value: '4',
          unit: 'أنظمة',
          badgeText: 'مستقر 100%',
          badgeClass: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400',
          iconPath: icons.docs,
          iconBg: 'bg-blue-600',
          lineColor: '#2563eb',
          subtext: 'الربط البيني: نشط'
        },
        {
          label: 'تنبيهات النظام والتحذيرات',
          value: '12',
          unit: 'تنبيه',
          badgeText: 'متوسط',
          badgeClass: 'bg-amber-50 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400',
          iconPath: icons.security,
          iconBg: 'bg-amber-600',
          lineColor: '#10b981',
          subtext: 'المهام المعلقة: 3'
        },
        {
          label: 'استقرار خوادم الاتصال',
          value: '99.9',
          unit: '% Uptime',
          badgeText: 'ممتاز',
          badgeClass: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400',
          iconPath: icons.security,
          iconBg: 'bg-emerald-600',
          lineColor: '#f59e0b',
          subtext: 'الاستجابة: 120ms'
        },
        {
          label: 'العمليات المنفذة اليوم',
          value: '1,240',
          unit: 'عملية',
          badgeText: 'آمن',
          badgeClass: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400',
          iconPath: icons.chart,
          iconBg: 'bg-purple-600',
          lineColor: '#ef4444',
          subtext: 'عمليات التدقيق: 85'
        }
      ],
      bars: [
        { label: 'مزامنة قاعدة البيانات الإقليمية', width: '98%', valueText: '98% مزامنة', bgClass: 'bg-emerald-500' },
        { label: 'عمليات التحقق والهوية KYC', width: '85%', valueText: '85% دقة', bgClass: 'bg-blue-500' },
        { label: 'نسخ احتياطي تلقائي', width: '100%', valueText: '100% ناجح', bgClass: 'bg-purple-500' }
      ]
    }
  }
})
</script>
