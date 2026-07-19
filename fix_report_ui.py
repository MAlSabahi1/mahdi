import re

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

# 1. Add import
if "import MultiSelect" not in content:
    content = content.replace("import ReportHeader from '@/components/reports/ReportHeader.vue'", 
                              "import MultiSelect from '@/components/common/MultiSelect.vue'\nimport ReportHeader from '@/components/reports/ReportHeader.vue'")

# 2. Fix Store variables
content = content.replace("coreStore.categories", "coreStore.jobCategories")
content = content.replace("coreStore.forceClassifications", "coreStore.forceTypes")

# 3. Replace Rank Dropdown
rank_html = """<div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الرتبة</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterRank" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                      <option value="">جميع الرتب</option>
                      <option v-for="r in coreStore.ranks" :key="r.id" :value="r.id">{{ r.name }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>"""
rank_new = """<div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الرتبة</label>
                  <MultiSelect v-model="filterRank" :options="coreStore.ranks" valueKey="id" labelKey="name" placeholder="جميع الرتب" />
                </div>"""
content = content.replace(rank_html, rank_new)

# 4. Replace Category Dropdown
cat_html = """<div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الفئة</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterCategory" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                      <option value="">جميع الفئات</option>
                      <option v-for="c in coreStore.jobCategories" :key="c.id" :value="c.id">{{ c.name }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>"""
cat_new = """<div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الفئة</label>
                  <MultiSelect v-model="filterCategory" :options="coreStore.jobCategories" valueKey="id" labelKey="name" placeholder="جميع الفئات" />
                </div>"""
content = content.replace(cat_html, cat_new)

# 5. Replace Workplaces & Status blocks
workplace_status_html = """<div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الإدارة المركزية (للقطاعات)</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="filterCentralDept" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option value="">كل الإدارات المركزية</option>
                  <option v-for="d in coreStore.centralDepartments" :key="d.id" :value="d.id">{{ d.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                </span>
              </div>
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الإدارة الأمنية</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="filterSecurityAdmin" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                  <option value="">كل الإدارات الأمنية</option>
                  <option v-for="d in availableSecurityAdmins" :key="d.id" :value="d.id">{{ d.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                </span>
              </div>
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الفرع الرئيسي</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="filterBranch" :disabled="!filterSecurityAdmin" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800 disabled:opacity-50 disabled:cursor-not-allowed">
                  <option value="">كل الفروع</option>
                  <option v-for="b in availableBranches" :key="b.id" :value="b.id">{{ b.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                </span>
              </div>
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">المديرية</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="filterDistrict" :disabled="!filterSecurityAdmin" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800 disabled:opacity-50 disabled:cursor-not-allowed">
                  <option value="">كل المديريات</option>
                  <option v-for="d in availableDistricts" :key="d.id" :value="d.id">{{ d.name_ar || d.name }}</option>
                </select>
                <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                </span>
              </div>
            </div>

            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">الحالة</label>
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

            <!-- Custom Multi-Select Dropdown for Status Types -->
            <div class="relative">
              <!-- Backdrop to close dropdown -->
              <div v-if="showStatusDropdown" @click="showStatusDropdown = false" class="fixed inset-0 z-40"></div>
              
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">نوع الحالة</label>
              <button 
                type="button"
                @click="showStatusDropdown = !showStatusDropdown"
                :disabled="!filterStatusClassification"
                class="relative z-50 flex h-11 w-full items-center justify-between rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span class="truncate">
                  {{ !filterStatusClassification ? 'اختر الحالة أولاً...' : (filterStatusIds.length === 0 ? 'جميع الأنواع' : `محدد (${filterStatusIds.length})`) }}
                </span>
                <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 20 20" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" />
                </svg>
              </button>
              
              <!-- Dropdown Menu -->
              <div v-if="showStatusDropdown" class="absolute z-50 mt-1 max-h-60 w-full overflow-y-auto rounded-xl border border-gray-200 bg-white p-2 shadow-lg dark:border-gray-700 dark:bg-gray-800">
                <div class="space-y-1">
                  <!-- Select All -->
                  <label class="flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2 hover:bg-gray-50 dark:hover:bg-gray-700">
                    <input type="checkbox" :checked="filterStatusIds.length === filteredStatuses.length && filteredStatuses.length > 0" @change="toggleAllStatuses" class="h-4 w-4 rounded border-gray-300 text-brand-600 focus:ring-brand-500" />
                    <span class="text-sm font-bold text-gray-900 dark:text-gray-100">تحديد الكل</span>
                  </label>
                  <div class="h-px bg-gray-100 dark:bg-gray-700 my-1"></div>
                  <!-- Individual Items -->
                  <label v-for="s in filteredStatuses" :key="s.id" class="flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2 hover:bg-gray-50 dark:hover:bg-gray-700">
                    <input type="checkbox" :value="s.id" v-model="filterStatusIds" class="h-4 w-4 rounded border-gray-300 text-brand-600 focus:ring-brand-500" />
                    <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ s.name }}</span>
                  </label>
                </div>
              </div>
            </div>"""

workplace_status_new = """<div class="lg:col-span-2">
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

if workplace_status_html in content:
    content = content.replace(workplace_status_html, workplace_status_new)
else:
    print("Warning: workplace_status_html not found")


# 6. Replace Residence Governorate
res_html = """<div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">المحافظة</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="filterResidenceGov" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                      <option value="">اختر...</option>
                      <option v-for="g in coreStore.governorates" :key="g.id" :value="g.id">{{ g.name }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>"""
res_new = """<div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">المحافظة</label>
                  <MultiSelect v-model="filterResidenceGov" :options="coreStore.governorates" valueKey="id" labelKey="name" placeholder="كل المحافظات" />
                </div>"""
content = content.replace(res_html, res_new)

# 7. Additional replacements
add_replacements = [
    ("filterQualification", "coreStore.qualifications", "كل المؤهلات"),
    ("filterPosition", "coreStore.positions", "كل المناصب"),
    ("filterForceClass", "coreStore.forceTypes", "كل التصنيفات")
]

for var_name, options, placeholder in add_replacements:
    html = f"""<div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{"تصنيف القوة" if var_name == "filterForceClass" else ("المنصب" if var_name == "filterPosition" else "المؤهل")}</label>
                  <div class="relative z-20 bg-transparent">
                    <select v-model="{var_name}" class="dark:bg-dark-900 h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 ltr:pr-11 rtl:pl-11 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800">
                      <option value="">{placeholder}</option>
                      <option v-for="{'c' if var_name == 'filterForceClass' else 'p'} in {options}" :key="{'c' if var_name == 'filterForceClass' else 'p'}.id" :value="{'c' if var_name == 'filterForceClass' else 'p'}.id">{{{"c" if var_name == "filterForceClass" else "p"}.name }}</option>
                    </select>
                    <span class="absolute z-30 text-gray-700 -translate-y-1/2 pointer-events-none ltr:right-4 rtl:left-4 top-1/2 dark:text-gray-400">
                      <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79175 7.396L10.0001 12.6043L15.2084 7.396" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
                    </span>
                  </div>
                </div>"""
    
    new_h = f"""<div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">{"تصنيف القوة" if var_name == "filterForceClass" else ("المنصب" if var_name == "filterPosition" else "المؤهل")}</label>
                  <MultiSelect v-model="{var_name}" :options="{options}" valueKey="id" labelKey="name" placeholder="{placeholder}" />
                </div>"""
    if html in content:
        content = content.replace(html, new_h)
    else:
        print(f"Warning: {var_name} html not found")


with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(content)

print("Done phase 1")
