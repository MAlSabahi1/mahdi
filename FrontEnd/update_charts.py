import re

with open('src/views/Reports/GraphicalReports.vue', 'r') as f:
    content = f.read()

# 1. Add new Refs
refs = """
const geoLabels = ref<string[]>([])
const geoSeries = ref<any[]>([])

const qualLabels = ref<string[]>([])
const qualSeries = ref<any[]>([])

const expLabels = ref<string[]>([])
const expSeries = ref<any[]>([])

const dqSeries = ref<any[]>([])
"""
content = content.replace("const statusSeries = ref<any[]>([])", "const statusSeries = ref<any[]>([])\n" + refs)

# 2. Add Chart Options
options = """
// 9. Geographic Distribution (Bar)
const geoChartOptions = computed(() => ({
  chart: { type: 'bar', ...commonChartConfig, toolbar: { show: false } },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  colors: ['#0f766e'],
  plotOptions: { bar: { horizontal: false, borderRadius: 4, columnWidth: '50%' } },
  dataLabels: { enabled: true, style: { fontSize: '12px', colors: ['#fff'] }, formatter: (val: any) => formatNumber(val) },
  xaxis: { categories: geoLabels.value, labels: { style: { colors: getLabelColor(), fontFamily, fontWeight: 'bold' } } },
  yaxis: { labels: { style: { colors: getLabelColor(), fontFamily } } },
  tooltip: { theme: isDarkMode.value ? 'dark' : 'light' }
}))

// 10. Qualification (Donut)
const qualChartOptions = computed(() => ({
  chart: { type: 'donut', ...commonChartConfig, toolbar: { show: false } },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  labels: qualLabels.value,
  colors: ['#1e3a8a', '#1d4ed8', '#0369a1', '#14532d', '#b45309'],
  stroke: { show: isDarkMode.value, colors: ['#1f2937'], width: 2 },
  dataLabels: { enabled: true, style: { fontFamily, fontSize: '12px', fontWeight: 'bold' }, dropShadow: { enabled: true } },
  legend: { position: 'bottom', fontFamily, labels: { colors: getLabelColor() } },
  tooltip: { theme: isDarkMode.value ? 'dark' : 'light' }
}))

// 11. Expenses (Pie)
const expChartOptions = computed(() => ({
  chart: { type: 'pie', ...commonChartConfig, toolbar: { show: false } },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  labels: expLabels.value,
  colors: ['#15803d', '#b91c1c', '#d97706'],
  stroke: { show: isDarkMode.value, colors: ['#1f2937'], width: 2 },
  dataLabels: { enabled: true, style: { fontFamily, fontSize: '12px', fontWeight: 'bold' } },
  legend: { position: 'bottom', fontFamily, labels: { colors: getLabelColor() } },
  tooltip: { theme: isDarkMode.value ? 'dark' : 'light' }
}))

// 12. Data Quality (RadialBar)
const dqChartOptions = computed(() => ({
  chart: { type: 'radialBar', ...commonChartConfig, toolbar: { show: false } },
  theme: { mode: isDarkMode.value ? 'dark' : 'light' },
  colors: ['#10b981', '#3b82f6', '#8b5cf6'],
  plotOptions: {
    radialBar: {
      dataLabels: {
        name: { fontSize: '14px', fontFamily, color: getLabelColor() },
        value: { fontSize: '20px', fontWeight: 'bold', fontFamily, color: getLabelColor(), formatter: (val: any) => val + '%' },
        total: { show: true, label: 'متوسط الجودة', color: getLabelColor(), formatter: (w: any) => Math.round(w.globals.seriesTotals[2]) + '%' }
      }
    }
  },
  labels: ['اكتمال الملفات', 'نظافة البيانات', 'مؤشر الجودة'],
  legend: { show: true, position: 'bottom', fontFamily, labels: { colors: getLabelColor() } }
}))
"""
content = content.replace("</script>", options + "\n</script>")


# 3. Fill the Data in fetchStatsAndAnalytics
fill_logic = """
      if (a.geographic_distribution && a.geographic_distribution.length) {
        geoLabels.value = a.geographic_distribution.map((i: any) => i.name || 'غير محدد')
        geoSeries.value = [{ name: 'الأفراد', data: a.geographic_distribution.map((i: any) => i.value) }]
      }
      
      if (a.qualification_distribution && a.qualification_distribution.length) {
        qualLabels.value = a.qualification_distribution.map((i: any) => i.name || 'بدون')
        qualSeries.value = a.qualification_distribution.map((i: any) => i.value)
      }
      
      if (a.expense_distribution && a.expense_distribution.length) {
        const translateExp = (val: string) => {
          if (val === 'has_expenses' || val === 'expenses') return 'يستلم نفقات'
          if (val === 'no_expenses') return 'بدون نفقات'
          return 'غير محدد'
        }
        expLabels.value = a.expense_distribution.map((i: any) => translateExp(i.name))
        expSeries.value = a.expense_distribution.map((i: any) => i.value)
      }
      
      if (a.data_quality_stats) {
        const dq = a.data_quality_stats
        const total = dq.complete_profiles + dq.incomplete_profiles || 1
        const completePct = Math.round((dq.complete_profiles / total) * 100)
        const cleanPct = Math.round((dq.clean_data / total) * 100)
        dqSeries.value = [completePct, cleanPct, Math.round(dq.average_score)]
      }
"""
content = content.replace("loadingAnalytics.value = false", fill_logic + "\n      loadingAnalytics.value = false")


# 4. Add HTML to the grid
html = """
          <!-- Geographic Distribution -->
          <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 relative flex flex-col xl:col-span-2 lg:col-span-2 sm:col-span-1 hover:shadow-theme-md transition-all">
            <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-800/30">
              <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-100 text-teal-600 dark:bg-teal-900/40 dark:text-teal-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </span>
                التوزيع الجغرافي (حسب المحافظة)
              </h3>
            </div>
            <div class="p-4 flex-1 flex flex-col justify-center min-h-[380px]">
              <div v-if="loadingAnalytics" class="flex justify-center"><svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg></div>
              <apexchart v-else-if="geoSeries[0]?.data?.length" type="bar" width="100%" height="320" :options="geoChartOptions" :series="geoSeries"></apexchart>
              <div v-else class="text-gray-400 font-bold flex flex-col items-center">
                <svg class="w-10 h-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                لا توجد بيانات متاحة
              </div>
            </div>
          </div>

          <!-- Data Quality -->
          <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 relative flex flex-col hover:shadow-theme-md transition-all">
            <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-800/30">
              <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-100 text-emerald-600 dark:bg-emerald-900/40 dark:text-emerald-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </span>
                مؤشرات جودة البيانات
              </h3>
            </div>
            <div class="p-4 flex-1 flex flex-col justify-center min-h-[380px]">
              <div v-if="loadingAnalytics" class="flex justify-center"><svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg></div>
              <apexchart v-else-if="dqSeries.length" type="radialBar" width="100%" height="320" :options="dqChartOptions" :series="dqSeries"></apexchart>
              <div v-else class="text-gray-400 font-bold flex flex-col items-center">
                <svg class="w-10 h-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                لا توجد بيانات متاحة
              </div>
            </div>
          </div>

          <!-- Qualifications -->
          <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 relative flex flex-col hover:shadow-theme-md transition-all">
            <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-800/30">
              <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-orange-100 text-orange-600 dark:bg-orange-900/40 dark:text-orange-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path></svg>
                </span>
                التوزيع حسب المؤهل العلمي
              </h3>
            </div>
            <div class="p-4 flex-1 flex flex-col justify-center min-h-[380px]">
              <div v-if="loadingAnalytics" class="flex justify-center"><svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg></div>
              <apexchart v-else-if="qualSeries.length" type="donut" width="100%" height="320" :options="qualChartOptions" :series="qualSeries"></apexchart>
              <div v-else class="text-gray-400 font-bold flex flex-col items-center">
                <svg class="w-10 h-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                لا توجد بيانات متاحة
              </div>
            </div>
          </div>

          <!-- Expenses -->
          <div class="bg-white rounded-2xl border border-gray-200 shadow-theme-sm dark:bg-gray-800 dark:border-gray-700 relative flex flex-col hover:shadow-theme-md transition-all">
            <div class="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-800/30">
              <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-yellow-100 text-yellow-600 dark:bg-yellow-900/40 dark:text-yellow-400">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </span>
                الموقف المالي والنفقات
              </h3>
            </div>
            <div class="p-4 flex-1 flex flex-col justify-center min-h-[380px]">
              <div v-if="loadingAnalytics" class="flex justify-center"><svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg></div>
              <apexchart v-else-if="expSeries.length" type="pie" width="100%" height="320" :options="expChartOptions" :series="expSeries"></apexchart>
              <div v-else class="text-gray-400 font-bold flex flex-col items-center">
                <svg class="w-10 h-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                لا توجد بيانات متاحة
              </div>
            </div>
          </div>
"""
content = content.replace("<!-- Overall Ranks (Bar) -->", html + "\n          <!-- Overall Ranks (Bar) -->")

with open('src/views/Reports/GraphicalReports.vue', 'w') as f:
    f.write(content)

print("Done")
