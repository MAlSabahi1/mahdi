import re

with open('src/views/Reports/ActiveForceReport.vue', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Page Header
page_header = """      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 print:hidden">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-slate-100 dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700">
            <svg class="h-8 w-8 text-slate-700 dark:text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <div>
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white">تفاصيل القوة العاملة</h2>
            <p class="text-sm font-medium text-slate-500 dark:text-slate-400 mt-1">استعراض كشوفات تفصيلية بأسماء الأفراد وتوزيعهم الميداني على الإدارات</p>
          </div>
        </div>
        <div class="flex items-center gap-2">"""

content = re.sub(r'<div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 print:hidden">.*?<div class="flex items-center gap-3">', page_header, content, flags=re.DOTALL)

# Find where <!-- Filters Panel --> starts, we want to inject "Expand All / Collapse All" right above or below it.
# Actually let's put it right before the Grouped Display loops
expand_controls = """
      <!-- Accordion Controls -->
      <div v-if="!loading && filteredGroupedData.length > 0" class="flex justify-between items-center bg-white dark:bg-slate-900 p-3 rounded-xl border border-slate-200 dark:border-slate-800 print:hidden">
        <span class="text-sm font-bold text-slate-700 dark:text-slate-300">إجمالي الإدارات: {{ filteredGroupedData.length }}</span>
        <div class="flex gap-2">
          <button @click="expandAll" class="px-4 py-1.5 text-sm bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg transition-colors font-medium">فتح الكل</button>
          <button @click="collapseAll" class="px-4 py-1.5 text-sm bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg transition-colors font-medium">طي الكل</button>
        </div>
      </div>

      <!-- Grouped Display -->
"""
content = re.sub(r'<!-- Grouped Display -->\s*<!-- Grouped Display -->', expand_controls, content)

# Now rewrite the group header and the table wrapper
group_block_regex = r'<!-- Title block matching the paper.*?<!-- Official Print Footer'

new_group_block = """<!-- Title block as Accordion Header -->
          <div 
            @click="toggleGroup(group.unit)"
            class="flex items-center justify-between bg-slate-50 hover:bg-slate-100 dark:bg-slate-800/50 dark:hover:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 px-6 py-4 rounded-xl cursor-pointer transition-colors print:hidden mb-2 group/header"
          >
            <div class="flex items-center gap-4">
              <div class="bg-white dark:bg-slate-700 p-2 rounded-lg shadow-sm border border-slate-200 dark:border-slate-600">
                <svg class="h-6 w-6 text-slate-600 dark:text-slate-300 transform transition-transform duration-300" :class="{'rotate-180': expandedGroups[group.unit]}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
              <h3 class="text-lg font-bold text-slate-900 dark:text-white">
                {{ group.unit }}
              </h3>
              <span class="inline-flex items-center justify-center rounded-md bg-slate-200 dark:bg-slate-700 px-2.5 py-1 text-xs font-bold text-slate-700 dark:text-slate-300">
                {{ group.items.length }} فرد
              </span>
            </div>
            
            <button 
              @click.stop="printSingleUnit(group.unit)" 
              class="opacity-0 group-hover/header:opacity-100 transition-opacity print:hidden bg-white dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:text-brand-600 dark:hover:text-brand-400 p-2 rounded-lg shadow-sm border border-slate-200 dark:border-slate-600 focus:outline-none"
              title="طباعة كشف هذه الجهة فقط"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
            </button>
          </div>
          
          <!-- Native Table matching official reports -->
          <div v-show="expandedGroups[group.unit]" class="overflow-x-auto bg-white dark:bg-slate-900 rounded-xl shadow-sm border-2 border-slate-200 dark:border-slate-800 print:border-none print:shadow-none print:rounded-none print-expand mb-12">
            <table class="w-full text-right text-sm border-collapse">
              <thead class="bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 border-b-2 border-slate-200 dark:border-slate-700">
                <tr>
                  <th v-for="col in columns" :key="col.key" class="px-4 py-3.5 font-bold text-sm text-center align-middle whitespace-nowrap border-l border-slate-200 dark:border-slate-700">
                    {{ col.label }}
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
                <tr v-for="row in group.items" :key="row.index" class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                  <td class="px-3 py-3 border-l border-slate-100 dark:border-slate-800 text-center font-bold text-slate-500 dark:text-slate-400">{{ row.index }}</td>
                  <td class="px-3 py-3 border-l border-slate-100 dark:border-slate-800 text-center font-semibold text-slate-900 dark:text-white whitespace-nowrap">{{ row.rank || '-' }}</td>
                  <td class="px-3 py-3 border-l border-slate-100 dark:border-slate-800 text-center font-mono font-medium text-slate-600 dark:text-slate-400">{{ row.military_number || '-' }}</td>
                  <td class="px-4 py-3 border-l border-slate-100 dark:border-slate-800 font-bold text-slate-900 dark:text-white text-base">{{ row.full_name || '-' }}</td>
                  <td class="px-3 py-3 border-l border-slate-100 dark:border-slate-800 text-center font-medium text-slate-700 dark:text-slate-300">{{ row.unit !== 'غير محدد (لا توجد بيانات)' ? row.unit : '-' }}</td>
                  <td class="px-3 py-3 border-l border-slate-100 dark:border-slate-800 text-center font-medium text-slate-700 dark:text-slate-300">{{ row.service_type || '-' }}</td>
                  <td class="px-3 py-3 border-l border-slate-100 dark:border-slate-800 text-center font-mono font-medium text-slate-600 dark:text-slate-400">{{ row.national_id || '-' }}</td>
                  <td class="px-3 py-3 border-l border-slate-100 dark:border-slate-800 text-center font-medium text-slate-700 dark:text-slate-300">{{ row.qualification || '-' }}</td>
                  <td class="px-3 py-3 text-center text-slate-500 dark:text-slate-400 max-w-[150px] truncate" :title="row.notes">{{ row.notes || '-' }}</td>
                </tr>
                <!-- Empty state for dummy group -->
                <tr v-if="group.items.length === 0">
                  <td :colspan="columns.length" class="px-6 py-12 text-center text-slate-500 bg-slate-50 dark:bg-slate-800/30">
                    <div class="flex flex-col items-center justify-center">
                      <svg class="h-10 w-10 text-slate-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                      </svg>
                      <span class="font-bold text-slate-600 dark:text-slate-300 text-base">لا توجد بيانات مطابقة لمعايير البحث</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <!-- Official Print Footer"""

content = re.sub(group_block_regex, new_group_block, content, flags=re.DOTALL)


# Now add the expandedGroups state in script setup
script_injection = """const printingUnit = ref<string | null>(null)

const expandedGroups = ref<Record<string, boolean>>({})

const toggleGroup = (unit: string) => {
  expandedGroups.value[unit] = !expandedGroups.value[unit]
}
const expandAll = () => {
  filteredGroupedData.value.forEach((g: any) => expandedGroups.value[g.unit] = true)
}
const collapseAll = () => {
  const newState: Record<string, boolean> = {}
  filteredGroupedData.value.forEach((g: any) => newState[g.unit] = false)
  expandedGroups.value = newState
}"""

content = content.replace("const printingUnit = ref<string | null>(null)", script_injection)

# Add .print-expand class to styles
style_injection = """
  /* Force table expansion in print mode */
  .print-expand {
    display: block !important;
  }
"""

content = content.replace(".print\:hidden {", style_injection + "\n  .print\:hidden {")

with open('src/views/Reports/ActiveForceReport.vue', 'w', encoding='utf-8') as f:
    f.write(content)
