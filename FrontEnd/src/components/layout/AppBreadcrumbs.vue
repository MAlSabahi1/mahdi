<template>
  <nav class="flex px-4 py-3 md:px-6 print:hidden sticky top-[73px] lg:top-[73px] z-40 bg-white/70 dark:bg-gray-900/70 backdrop-blur-xl border-b border-gray-200/50 dark:border-gray-800/50 shadow-[0_4px_30px_rgba(0,0,0,0.02)] transition-all duration-300" aria-label="Breadcrumb">
    <div class="mx-auto w-full max-w-(--breakpoint-2xl)">
      <ol class="inline-flex items-center gap-1 md:gap-2 overflow-x-auto whitespace-nowrap hide-scrollbar w-full py-0.5">
        <li v-for="(crumb, index) in breadcrumbs" :key="index" class="inline-flex items-center">
          
          <!-- Chevron separator for all but the first item -->
          <div v-if="index > 0" class="flex items-center justify-center mx-1 md:mx-1.5 text-gray-400 dark:text-gray-600">
            <svg class="w-3.5 h-3.5 rtl:-scale-x-100" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
            </svg>
          </div>

          <!-- Home Icon for the first item -->
          <router-link v-if="index === 0" :to="crumb.path" class="inline-flex items-center gap-1.5 px-3 py-1.5 text-[13px] font-bold text-gray-600 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 hover:text-brand-600 hover:border-brand-200 hover:shadow-sm hover:-translate-y-0.5 transition-all duration-300 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-brand-400 dark:hover:border-brand-700">
            <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            {{ crumb.title }}
          </router-link>

          <!-- Interactive link for intermediate items -->
          <router-link v-else-if="index < breadcrumbs.length - 1 && crumb.clickable !== false" :to="crumb.path" class="inline-flex items-center px-3 py-1.5 text-[13px] font-semibold text-gray-600 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 hover:text-brand-600 hover:border-brand-200 hover:shadow-sm hover:-translate-y-0.5 transition-all duration-300 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-brand-400 dark:hover:border-brand-700">
            {{ crumb.title }}
          </router-link>

          <!-- Current page (last item or non-clickable intermediate item) -->
          <span v-else class="inline-flex items-center gap-1.5 px-3 py-1.5 text-[13px] font-extrabold text-blue-700 bg-blue-50/80 border border-blue-200 rounded-xl shadow-[0_2px_10px_rgba(37,99,235,0.1)] dark:bg-blue-900/30 dark:border-blue-800/80 dark:text-blue-300 pointer-events-none transition-all duration-300">
            <svg v-if="index === breadcrumbs.length - 1" class="w-2.5 h-2.5 text-blue-500 animate-pulse" fill="currentColor" viewBox="0 0 8 8">
              <circle cx="4" cy="4" r="3" />
            </svg>
            {{ crumb.title }}
          </span>
        </li>
      </ol>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const routeDictionary: Record<string, string> = {
  'admin': 'الإدارة والتنظيم',
  'personnel': 'شؤون الأفراد',
  'services': 'نظام الخدمات',
  'secretariat': 'السكرتارية والأرشفة',
  'reports': 'نظام التقارير',
  'users': 'إدارة المستخدمين',
  'dashboard': 'لوحة التحكم',
  'builder': 'منشئ المذكرات',
  'view': 'عرض التفاصيل',
  'settings': 'الإعدادات',
  'official-reports': 'تقارير نظام الخدمات',
  'graphical': 'التقارير البيانية',
  'hierarchical': 'الهيكل التنظيمي',
  'monthly-services': 'التقارير الشهرية',
  'export-requests': 'طلبات التصدير',
  'stats': 'إحصائيات النظام',
  'users-activity': 'نشاط المستخدمين',
  'audit': 'التدقيق المركزي',
  'tasks': 'سجل المهام',
  'meetings': 'الاجتماعات',
  'correspondences': 'المراسلات الواردة والصادرة',
  'edit': 'تعديل البيانات',
  'create': 'إضافة جديد',
  'new': 'عنصر جديد'
}

const breadcrumbs = computed(() => {
  const crumbs: { title: string, path: string, clickable?: boolean }[] = [{ title: 'الرئيسية', path: '/', clickable: true }]
  if (route.path === '/') return crumbs

  const pathSegments = route.path.split('/').filter(p => p)
  let currentPath = ''
  
  const allRoutes = router.getRoutes()

  pathSegments.forEach((segment, index) => {
    currentPath += `/${segment}`
    
    // Check if there is an exact route match
    const matchedRoute = allRoutes.find(r => r.path === currentPath)
    let title = matchedRoute?.meta?.title as string
    let clickable = !!matchedRoute // If there's an actual route, it's clickable
    
    // Special exception for /reports redirect
    if (currentPath === '/reports') clickable = true;
    if (currentPath === '/services') clickable = true;
    
    // If no route or no title, use dictionary fallback
    if (!title && routeDictionary[segment.toLowerCase()]) {
      title = routeDictionary[segment.toLowerCase()]
      if (!matchedRoute) clickable = false // Disable clicking if it's purely a logical grouping without a page
    }
    
    // If we are at the last segment and still no title, use the current route's meta.title
    if (!title && index === pathSegments.length - 1 && route.meta?.title) {
      title = route.meta.title as string
      clickable = true
    }

    // Special logic for generic parameter IDs (e.g., /reports/view/1)
    if (!title && /^\d+$/.test(segment)) {
      title = `عنصر #${segment}`
    }

    if (title && title !== 'Dashboard') {
      // Avoid duplicate titles sequentially (e.g. if the meta.title is exactly the same as the dictionary)
      if (crumbs.length > 0 && crumbs[crumbs.length - 1].title === title) {
        // Skip duplicate
      } else {
        crumbs.push({ title, path: currentPath, clickable })
      }
    }
  })
  
  return crumbs
})
</script>

<style scoped>
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
