<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.general_configs')" />
    
    <div class="flex flex-col lg:flex-row gap-6 text-start min-h-[calc(100vh-160px)]" dir="rtl">
      
      <!-- Sidebar Navigation for Configs -->
      <div class="w-full lg:w-72 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-4 shadow-sm h-fit shrink-0">
        <h3 class="font-black text-gray-900 dark:text-white px-2 mb-4 text-lg">تهيئة الهيكل</h3>
        
        <div class="space-y-1">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-bold transition-all duration-200 cursor-pointer"
            :class="[
              activeTab === tab.id 
                ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' 
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800'
            ]"
          >
            <component :is="tab.icon" class="w-5 h-5" />
            {{ tab.name }}
          </button>
        </div>
      </div>

      <!-- Main Content Area -->
      <div class="flex-1 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-6 shadow-sm overflow-hidden flex flex-col">
        
        <!-- Tab Header -->
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
          <div>
            <h2 class="text-xl font-black text-gray-900 dark:text-white flex items-center gap-2">
              <component :is="currentTab.icon" class="w-6 h-6 text-blue-500" />
              {{ currentTab.name }}
            </h2>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ currentTab.description }}</p>
          </div>
          
          <button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-xl text-sm font-bold flex items-center gap-2 transition-colors shrink-0 cursor-pointer">
            <Plus class="w-4 h-4" /> إضافة سجل جديد
          </button>
        </div>

        <!-- DataTable Component -->
        <div class="flex-1 overflow-hidden">
          <DataTable
            :columns="currentColumns"
            :data="currentData"
            :search-placeholder="'بحث في ' + currentTab.name + '...'"
          >
            <!-- Custom Cell for Military Ranks Icon/Badge -->
            <template #cell-badge="{ row }">
              <div v-if="activeTab === 'ranks'" class="flex items-center justify-center w-8 h-8 rounded bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                <ShieldCheck class="w-4 h-4 text-amber-500" />
              </div>
              <div v-else-if="activeTab === 'statuses'" class="flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-bold" :class="row.is_active ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400' : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'">
                <div class="w-2 h-2 rounded-full" :class="row.is_active ? 'bg-emerald-500' : 'bg-red-500'"></div>
                {{ row.is_active ? 'نشط' : 'غير نشط' }}
              </div>
              <span v-else class="text-gray-500">-</span>
            </template>
            
            <template #cell-actions="{ row }">
              <div class="flex items-center gap-2">
                <button class="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-colors cursor-pointer" title="تعديل">
                  <Edit class="w-4 h-4" />
                </button>
                <button class="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-lg transition-colors cursor-pointer" title="حذف">
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </template>
          </DataTable>
        </div>
      </div>
      
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import DataTable from '@/components/tables/DataTable.vue'
import { 
  Plus, Edit, Trash2, 
  ShieldCheck, UserCheck, Briefcase, Award, Settings2 
} from 'lucide-vue-next'

const { t } = useI18n()

// Tabs Configuration
const activeTab = ref('ranks')

const tabs = [
  { id: 'ranks', name: 'الرتب العسكرية', description: 'إدارة الرتب العسكرية واختصاراتها وترتيبها الهرمي', icon: ShieldCheck },
  { id: 'statuses', name: 'الحالات الوظيفية', description: 'إدارة حالات الخدمة (على رأس العمل، منتدب، الخ)', icon: UserCheck },
  { id: 'categories', name: 'الفئات الوظيفية', description: 'تصنيف الأفراد (فني، إداري، مقاتل)', icon: Briefcase },
  { id: 'titles', name: 'المسميات القيادية', description: 'إدارة المسميات الوظيفية والمناصب القيادية', icon: Award },
]

const currentTab = computed(() => tabs.find(t => t.id === activeTab.value) || tabs[0])

// Mock Data & Columns for Each Tab
const tablesConfig = {
  ranks: {
    columns: [
      { key: 'badge', label: 'الشارة', sortable: false },
      { key: 'name', label: 'اسم الرتبة', sortable: true },
      { key: 'code', label: 'الاختصار', sortable: true },
      { key: 'level', label: 'المستوى (الترتيب)', sortable: true },
      { key: 'type', label: 'التصنيف', sortable: true },
    ],
    data: [
      { id: 1, name: 'لواء', code: 'MG', level: 1, type: 'ضباط' },
      { id: 2, name: 'عميد', code: 'BG', level: 2, type: 'ضباط' },
      { id: 3, name: 'عقيد', code: 'COL', level: 3, type: 'ضباط' },
      { id: 4, name: 'مقدم', code: 'LTC', level: 4, type: 'ضباط' },
      { id: 5, name: 'رائد', code: 'MAJ', level: 5, type: 'ضباط' },
      { id: 6, name: 'نقيب', code: 'CPT', level: 6, type: 'ضباط' },
      { id: 7, name: 'ملازم أول', code: '1LT', level: 7, type: 'ضباط' },
      { id: 8, name: 'ملازم', code: '2LT', level: 8, type: 'ضباط' },
      { id: 9, name: 'مساعد أول', code: 'WO1', level: 9, type: 'ضباط صف' },
      { id: 10, name: 'رقيب أول', code: 'SFC', level: 10, type: 'ضباط صف' },
    ]
  },
  statuses: {
    columns: [
      { key: 'name', label: 'اسم الحالة', sortable: true },
      { key: 'code', label: 'الرمز', sortable: true },
      { key: 'badge', label: 'الحالة النظامية', sortable: false },
      { key: 'description', label: 'الوصف', sortable: false },
    ],
    data: [
      { id: 1, name: 'على رأس العمل', code: 'ACTIVE', is_active: true, description: 'متواجد بالخدمة الفعلية' },
      { id: 2, name: 'إجازة سنوية', code: 'LEAVE_ANNUAL', is_active: true, description: 'في إجازة رسمية' },
      { id: 3, name: 'منتدب', code: 'DEPUTED', is_active: true, description: 'منتدب لجهة أخرى' },
      { id: 4, name: 'متقاعد', code: 'RETIRED', is_active: false, description: 'منهى خدمته بالتقاعد' },
      { id: 5, name: 'شهيد', code: 'MARTYR', is_active: false, description: 'استشهد أثناء الواجب' },
      { id: 6, name: 'هارب', code: 'AWOL', is_active: false, description: 'منقطع عن العمل بغير عذر' },
    ]
  },
  categories: {
    columns: [
      { key: 'name', label: 'اسم الفئة', sortable: true },
      { key: 'code', label: 'الرمز', sortable: true },
      { key: 'members_count', label: 'عدد المنتسبين', sortable: true },
    ],
    data: [
      { id: 1, name: 'قوة قتالية', code: 'COMBAT', members_count: '15,200' },
      { id: 2, name: 'قوة إدارية', code: 'ADMIN', members_count: '2,450' },
      { id: 3, name: 'قوة فنية', code: 'TECH', members_count: '1,800' },
      { id: 4, name: 'طاقم طبي', code: 'MEDICAL', members_count: '420' },
    ]
  },
  titles: {
    columns: [
      { key: 'name', label: 'المسمى القيادي', sortable: true },
      { key: 'level', label: 'المستوى الإداري', sortable: true },
      { key: 'min_rank', label: 'الرتبة كحد أدنى', sortable: true },
    ],
    data: [
      { id: 1, name: 'قائد قطاع', level: 'القيادة العليا', min_rank: 'عميد' },
      { id: 2, name: 'مدير عام', level: 'الإدارة العامة', min_rank: 'عقيد' },
      { id: 3, name: 'رئيس شعبة', level: 'الإدارة الفرعية', min_rank: 'مقدم' },
      { id: 4, name: 'مدير إدارة', level: 'الإدارة التنفيذية', min_rank: 'رائد' },
      { id: 5, name: 'رئيس قسم', level: 'الأقسام', min_rank: 'نقيب' },
    ]
  }
}

const currentColumns = computed(() => {
  const baseColumns = tablesConfig[activeTab.value as keyof typeof tablesConfig].columns
  // Add actions column at the end
  return [...baseColumns, { key: 'actions', label: 'الإجراءات', sortable: false }]
})

const currentData = computed(() => tablesConfig[activeTab.value as keyof typeof tablesConfig].data)

</script>
