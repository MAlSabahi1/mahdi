<template>
  <admin-layout>
    <div class="space-y-6 pb-20 max-w-7xl mx-auto px-4 mt-6">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-3xl font-bold text-gray-800 dark:text-white/90">استوديو ذكاء الأعمال (Enterprise BI)</h2>
          <p class="text-sm text-gray-500 mt-1">قم بتصميم تقارير مؤسسية معقدة عبر مصادر بيانات متعددة، تجميعات، وفلاتر متداخلة</p>
        </div>
        <button @click="saveReport" :disabled="isSaving" class="px-6 py-2.5 bg-brand-600 text-white rounded-lg shadow-sm hover:bg-brand-700 font-medium transition-colors flex items-center gap-2">
          <svg v-if="!isSaving" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
          </svg>
          {{ isSaving ? 'جاري الحفظ...' : 'حفظ ونشر التقرير' }}
        </button>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Sidebar: Configuration Tabs -->
        <div class="lg:col-span-1 space-y-2">
          <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
            :class="[
              'w-full text-right px-4 py-3 rounded-xl text-sm font-medium transition-all flex items-center gap-3',
              activeTab === tab.id 
                ? 'bg-brand-50 text-brand-700 border border-brand-200 dark:bg-brand-900/20 dark:text-brand-300 dark:border-brand-800' 
                : 'bg-white text-gray-600 border border-transparent hover:bg-gray-50 dark:bg-gray-900 dark:text-gray-400 dark:hover:bg-gray-800'
            ]">
            <div v-html="tab.icon" class="w-5 h-5"></div>
            {{ tab.name }}
          </button>
        </div>

        <!-- Main Content Area -->
        <div class="lg:col-span-3">
          <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 min-h-[500px]">
            
            <!-- Tab 1: General Settings -->
            <div v-if="activeTab === 'general'" class="space-y-5">
              <h3 class="text-lg font-bold border-b pb-2 mb-4 dark:border-gray-800">المعلومات الأساسية</h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium mb-1">عنوان التقرير *</label>
                  <input v-model="form.title" type="text" class="w-full rounded-lg border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:ring-brand-500">
                </div>
                <div>
                  <label class="block text-sm font-medium mb-1">الرمز المرجعي (Slug) *</label>
                  <input v-model="form.slug" type="text" class="w-full text-left font-mono rounded-lg border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:ring-brand-500" placeholder="e.g. officers_summary">
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium mb-1">مصدر البيانات (Data Source) *</label>
                <select v-model="form.data_source" class="w-full rounded-lg border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:ring-brand-500">
                  <option value="" disabled>اختر مصدر البيانات...</option>
                  <option v-for="src in dataSources" :key="src.id" :value="src.id">
                    {{ src.name }} ({{ src.source_type_display }})
                  </option>
                </select>
                <p class="text-xs text-gray-500 mt-1">يحدد مصدر البيانات الجداول أو الـ Views التي سيتم الاستعلام منها.</p>
              </div>

              <div>
                <label class="block text-sm font-medium mb-1">نوع التخطيط (Layout Type)</label>
                <div class="flex gap-4">
                  <label class="flex items-center gap-2 p-3 border rounded-xl cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition"
                    :class="{'border-brand-500 bg-brand-50/30 dark:bg-brand-900/10': schema.layout_type === 'table'}">
                    <input type="radio" v-model="schema.layout_type" value="table" class="text-brand-600 focus:ring-brand-500">
                    <span class="text-sm font-medium">جدول قياسي</span>
                  </label>
                  <label class="flex items-center gap-2 p-3 border rounded-xl cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition"
                    :class="{'border-brand-500 bg-brand-50/30 dark:bg-brand-900/10': schema.layout_type === 'pivot'}">
                    <input type="radio" v-model="schema.layout_type" value="pivot" class="text-brand-600 focus:ring-brand-500">
                    <span class="text-sm font-medium">جدول محوري (Pivot)</span>
                  </label>
                  <label class="flex items-center gap-2 p-3 border rounded-xl cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition"
                    :class="{'border-brand-500 bg-brand-50/30 dark:bg-brand-900/10': schema.layout_type === 'summary'}">
                    <input type="radio" v-model="schema.layout_type" value="summary" class="text-brand-600 focus:ring-brand-500">
                    <span class="text-sm font-medium">بطاقات خلاصة</span>
                  </label>
                </div>
              </div>
            </div>

            <!-- Tab 2: Columns -->
            <div v-if="activeTab === 'columns'" class="space-y-5">
              <div class="flex items-center justify-between border-b pb-2 mb-4 dark:border-gray-800">
                <h3 class="text-lg font-bold">هيكلة الأعمدة</h3>
                <button @click="addColumn" class="text-sm bg-gray-100 dark:bg-gray-800 px-3 py-1.5 rounded-lg font-medium hover:bg-gray-200 transition">إضافة عمود +</button>
              </div>

              <div class="space-y-4">
                <div v-for="(col, idx) in schema.columns" :key="idx" class="p-4 border border-gray-100 dark:border-gray-800 rounded-xl bg-gray-50/50 dark:bg-gray-800/20 flex flex-col gap-3">
                  <div class="flex items-start gap-4">
                    <div class="flex-1 grid grid-cols-2 gap-3">
                      <div>
                        <label class="block text-xs text-gray-500 mb-1">الحقل (Field)</label>
                        <input v-model="col.field" type="text" class="w-full text-sm py-1.5 rounded border-gray-300 dark:bg-gray-800 dark:border-gray-700" placeholder="e.g. current_rank__name">
                      </div>
                      <div>
                        <label class="block text-xs text-gray-500 mb-1">الاسم المعروض (Label)</label>
                        <input v-model="col.label" type="text" class="w-full text-sm py-1.5 rounded border-gray-300 dark:bg-gray-800 dark:border-gray-700" placeholder="الرتبة">
                      </div>
                    </div>
                    <button @click="removeColumn(idx)" class="mt-6 text-red-500 p-1.5 hover:bg-red-50 rounded-md bg-white dark:bg-gray-900 border" title="حذف">
                      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                    </button>
                  </div>
                  <div class="flex items-center gap-4 text-sm bg-white dark:bg-gray-900 p-2 rounded-lg border border-gray-200 dark:border-gray-800">
                    <label class="flex items-center gap-1.5 cursor-pointer">
                      <input v-model="col.visible" type="checkbox" class="rounded border-gray-300 text-brand-600 focus:ring-brand-600">
                      <span>مرئي</span>
                    </label>
                    <label class="flex items-center gap-1.5 cursor-pointer">
                      <input v-model="col.sortable" type="checkbox" class="rounded border-gray-300 text-brand-600 focus:ring-brand-600">
                      <span>قابل للفرز</span>
                    </label>
                    <div class="flex-1 flex items-center justify-end gap-2">
                      <span class="text-xs text-gray-500">المحاذاة:</span>
                      <select v-model="col.alignment" class="text-xs py-1 rounded border-gray-300 dark:bg-gray-800 dark:border-gray-700">
                        <option value="right">يمين</option>
                        <option value="center">وسط</option>
                        <option value="left">يسار</option>
                      </select>
                    </div>
                  </div>
                </div>
                <div v-if="!schema.columns.length" class="text-center py-8 text-gray-500 text-sm">
                  لا توجد أعمدة مضافة.
                </div>
              </div>
            </div>

            <!-- Tab 3: Aggregations & Grouping -->
            <div v-if="activeTab === 'aggregations'" class="space-y-6">
              <div>
                <div class="flex items-center justify-between border-b pb-2 mb-4 dark:border-gray-800">
                  <h3 class="text-lg font-bold text-blue-700 dark:text-blue-400">التجميع (Group By)</h3>
                  <button @click="addGroupBy" class="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded border border-blue-200">إضافة تجميع +</button>
                </div>
                <div class="space-y-2">
                  <div v-for="(gb, idx) in schema.group_by" :key="'gb'+idx" class="flex gap-2">
                    <input v-model="schema.group_by[idx]" type="text" class="w-full text-sm py-1.5 rounded border-gray-300 dark:bg-gray-800 dark:border-gray-700" placeholder="الحقل للتجميع (مثال: current_rank__name)">
                    <button @click="removeGroupBy(idx)" class="text-red-500 px-2 hover:bg-red-50 rounded border">×</button>
                  </div>
                  <p v-if="!schema.group_by.length" class="text-xs text-gray-500">لا يوجد تجميع للبيانات.</p>
                </div>
              </div>

              <div>
                <div class="flex items-center justify-between border-b pb-2 mb-4 dark:border-gray-800">
                  <h3 class="text-lg font-bold text-green-700 dark:text-green-400">العمليات الحسابية (Aggregations)</h3>
                  <button @click="addAggregation" class="text-xs bg-green-50 text-green-700 px-2 py-1 rounded border border-green-200">إضافة عملية +</button>
                </div>
                <div class="space-y-2">
                  <div v-for="(agg, idx) in schema.aggregations" :key="'agg'+idx" class="flex items-center gap-2 bg-gray-50 dark:bg-gray-800/30 p-2 rounded-lg border">
                    <select v-model="agg.function" class="w-1/4 text-sm py-1.5 rounded border-gray-300 dark:bg-gray-800 dark:border-gray-700 font-bold text-green-700">
                      <option value="COUNT">COUNT</option>
                      <option value="SUM">SUM</option>
                      <option value="AVG">AVG</option>
                      <option value="MAX">MAX</option>
                      <option value="MIN">MIN</option>
                    </select>
                    <span class="text-gray-400 font-mono">(</span>
                    <input v-model="agg.field" type="text" class="flex-1 text-sm py-1.5 rounded border-gray-300 dark:bg-gray-800 dark:border-gray-700" placeholder="الحقل (مثال: military_number)">
                    <span class="text-gray-400 font-mono">) AS</span>
                    <input v-model="agg.alias" type="text" class="w-1/4 text-sm py-1.5 rounded border-gray-300 dark:bg-gray-800 dark:border-gray-700 font-mono text-purple-600" placeholder="الاسم المستعار">
                    <button @click="removeAggregation(idx)" class="text-red-500 px-2 hover:bg-red-50 rounded border">×</button>
                  </div>
                  <p v-if="!schema.aggregations.length" class="text-xs text-gray-500">لا توجد عمليات حسابية.</p>
                </div>
              </div>
            </div>

            <!-- Tab 4: Advanced Filters -->
            <div v-if="activeTab === 'filters'" class="space-y-5">
              <div class="flex items-center justify-between border-b pb-2 mb-4 dark:border-gray-800">
                <div>
                  <h3 class="text-lg font-bold">بناء الفلاتر (AST Builder)</h3>
                  <p class="text-xs text-gray-500">الفلتر الأساسي يستخدم لتقييد البيانات للمستوى المطلوب</p>
                </div>
              </div>

              <!-- Visual Representation of AST would go here. For MVP, we provide JSON Editor for advanced users, or basic list -->
              <div class="bg-gray-900 rounded-xl p-4 overflow-hidden relative">
                <div class="absolute top-2 left-2 flex gap-2">
                   <button @click="resetFilters" class="text-xs bg-gray-800 text-gray-300 px-2 py-1 rounded hover:text-white">إعادة تعيين</button>
                </div>
                <textarea v-model="schemaFiltersJson" rows="12" class="w-full bg-transparent text-green-400 font-mono text-sm border-none focus:ring-0 resize-y" dir="ltr" placeholder='{ "operator": "AND", "conditions": [] }'></textarea>
              </div>
              <p class="text-xs text-gray-500 mt-2">يمكنك إدخال شجرة ফلاتر معقدة بصيغة JSON لدعم (AND / OR) المعقدة والمتداخلة.</p>

            </div>

          </div>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'

const router = useRouter()
const isSaving = ref(false)
const dataSources = ref<any[]>([])

// Inline SVG components as strings for simplicity or rely on existing ones.
const icons = {
  general: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>`,
  columns: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>`,
  aggregations: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>`,
  filters: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path></svg>`
}

const tabs = [
  { id: 'general', name: 'البيانات الأساسية', icon: icons.general },
  { id: 'columns', name: 'هيكلة الأعمدة', icon: icons.columns },
  { id: 'aggregations', name: 'التجميع والعمليات', icon: icons.aggregations },
  { id: 'filters', name: 'شروط الفلترة', icon: icons.filters },
]
const activeTab = ref('general')

const form = ref({
  title: '',
  slug: '',
  description: '',
  data_source: '',
})

const schema = ref({
  layout_type: 'table',
  columns: [
    { field: 'military_number', label: 'الرقم العسكري', width: '150px', alignment: 'right', format: 'string', visible: true, sortable: true },
    { field: 'full_name', label: 'الاسم الرباعي', width: '250px', alignment: 'right', format: 'string', visible: true, sortable: true }
  ] as any[],
  group_by: [] as string[],
  aggregations: [] as any[],
  filters: {
    operator: 'AND',
    conditions: [] as any[]
  }
})

// Schema Filters computed (JSON formatting)
const schemaFiltersJson = computed({
  get: () => JSON.stringify(schema.value.filters, null, 2),
  set: (val) => {
    try {
      schema.value.filters = JSON.parse(val)
    } catch (e) {
      // ignore parse errors while typing
    }
  }
})

const addColumn = () => {
  schema.value.columns.push({
    field: '', label: '', width: '', alignment: 'right', format: 'string', visible: true, sortable: true
  })
}
const removeColumn = (idx: number) => schema.value.columns.splice(idx, 1)

const addGroupBy = () => schema.value.group_by.push('')
const removeGroupBy = (idx: number) => schema.value.group_by.splice(idx, 1)

const addAggregation = () => schema.value.aggregations.push({ field: '', function: 'COUNT', alias: 'count_val' })
const removeAggregation = (idx: number) => schema.value.aggregations.splice(idx, 1)

const resetFilters = () => {
  schema.value.filters = { operator: 'AND', conditions: [] }
}

const fetchDataSources = async () => {
  try {
    const res = await api.get('/services/api/admin/bi-sources/')
    dataSources.value = res.data.results || res.data
  } catch (e) {
    console.error('Failed to fetch data sources', e)
  }
}

const saveReport = async () => {
  if (!form.value.title || !form.value.slug || !form.value.data_source) {
    alert('يرجى تعبئة الحقول الإجبارية (العنوان، الرمز المرجعي، ومصدر البيانات)')
    return
  }

  isSaving.value = true
  try {
    const payload = {
      ...form.value,
      config_schema: schema.value
    }
    
    await api.post('/services/api/admin/bi-templates/', payload)
    
    alert('تم إنشاء تقرير ذكاء الأعمال بنجاح!')
    // Redirect to the new viewer
    router.push(`/reports/builder/view/${form.value.slug}`)
  } catch (e: any) {
    console.error(e)
    alert(e.response?.data?.slug ? 'الرمز المرجعي موجود مسبقاً.' : 'فشل الحفظ. تأكد من صحة البيانات.')
  } finally {
    isSaving.value = false
  }
}

onMounted(() => {
  fetchDataSources()
})
</script>
