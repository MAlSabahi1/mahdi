import re

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

def replace_select_with_multiselect(var_name, options_var, placeholder, label_override=None):
    global content
    pattern = r'(<label class="mb-1\.5 block text-sm font-medium text-gray-700 dark:text-gray-400">)(.*?)(</label>\s*<div class="relative z-20 bg-transparent">\s*<select v-model="' + var_name + r'".*?</div>\s*</div>)'
    
    def replacer(match):
        label_text = label_override if label_override else match.group(2)
        return f'{match.group(1)}{label_text}</label>\n                  <MultiSelect v-model="{var_name}" :options="{options_var}" valueKey="id" labelKey="name" placeholder="{placeholder}" />\n                </div>'
    
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)

replace_select_with_multiselect("filterQualification", "coreStore.qualifications", "كل المؤهلات")
replace_select_with_multiselect("filterPosition", "coreStore.positions", "كل المناصب")
replace_select_with_multiselect("filterForceClass", "coreStore.forceTypes", "كل التصنيفات", "تصنيف القوة")

# Fix Workplaces & Status
workplace_pattern = r'<div>\s*<label class="mb-1\.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الإدارة المركزية \(للقطاعات\)</label>.*?<!-- Dropdown Menu -->.*?</div>\s*</div>\s*</div>'
workplace_replacement = """<div class="lg:col-span-2">
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">جهة العمل (إدارة / فرع / مديرية)</label>
              <MultiSelect v-model="filterWorkplaces" :options="groupedWorkplaces" valueKey="value" labelKey="label" placeholder="كل الجهات" />
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">التصنيف العام للحالة</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="filterStatusClassification" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option value="">جميع الحالات</option>
                  <option value="active_full">قوة عاملة فعلية</option>
                  <option value="active_part">قوة عاملة غير فعلية</option>
                  <option value="inactive_temp">قوة غير عاملة مؤقتاً</option>
                  <option value="inactive_perm">قوة غير عاملة نهائياً</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                </span>
              </div>
            </div>
            
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">نوع الحالة المخصص</label>
              <MultiSelect v-model="filterStatusIds" :options="filteredStatuses" valueKey="id" labelKey="name" placeholder="جميع الأنواع" :disabled="!filterStatusClassification" disabledPlaceholder="اختر التصنيف أولاً..." />
            </div>"""
content = re.sub(workplace_pattern, workplace_replacement, content, flags=re.DOTALL)

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(content)

print("Done phase 2")
