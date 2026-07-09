<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="t('admin.org_tree')" />
    
    <div class="space-y-6 text-start" dir="rtl">
      <!-- Header & Actions -->
      <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-6 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h2 class="text-xl font-black text-gray-900 dark:text-white flex items-center gap-2">
            <ShieldAlert class="w-6 h-6 text-blue-500" />
            الهيكل التنظيمي للقوة
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">تصفح وإدارة القطاعات والإدارات والأقسام العسكرية والإدارية</p>
        </div>
        <div class="flex items-center gap-3 w-full md:w-auto">
          <div class="relative flex-1 md:w-64">
            <input 
              type="text" 
              v-model="searchQuery"
              placeholder="بحث في الهيكل التنظيمي..." 
              class="w-full pl-10 pr-10 py-2 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            >
            <Search class="w-4 h-4 text-gray-400 absolute top-3 right-3" />
          </div>
          <button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-sm font-bold flex items-center gap-2 transition-colors shrink-0 cursor-pointer">
            <Plus class="w-4 h-4" /> إضافة قطاع
          </button>
        </div>
      </div>

      <!-- Org Tree View -->
      <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-6 shadow-sm overflow-x-auto min-h-[500px]">
        <div class="min-w-[700px]">
          
          <div v-for="sector in filteredTree" :key="sector.id" class="mb-6 relative">
            <!-- Level 1: Sector Card -->
            <div class="flex items-center gap-4 p-4 rounded-xl bg-gradient-to-l from-blue-50 to-white dark:from-blue-900/20 dark:to-gray-900 border border-blue-100 dark:border-blue-900/50 shadow-sm relative z-10">
              <button @click="sector.expanded = !sector.expanded" class="p-1.5 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors cursor-pointer">
                <ChevronDown v-if="sector.expanded" class="w-5 h-5 text-gray-600 dark:text-gray-300" />
                <ChevronLeft v-else class="w-5 h-5 text-gray-600 dark:text-gray-300" />
              </button>
              
              <div class="w-12 h-12 rounded-xl bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center text-blue-600 dark:text-blue-400 shrink-0">
                <Shield class="w-6 h-6" />
              </div>
              
              <div class="flex-1">
                <h3 class="font-black text-lg text-gray-900 dark:text-white">{{ sector.name }}</h3>
                <p class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-2 mt-1">
                  <UserCheck class="w-3.5 h-3.5" /> القائد: {{ sector.manager }}
                  <span class="mx-1">•</span>
                  <Users class="w-3.5 h-3.5" /> الأفراد: {{ sector.personnelCount }}
                </p>
              </div>

              <div class="flex items-center gap-2 shrink-0">
                <button class="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-colors cursor-pointer" title="تعديل"><Edit class="w-4 h-4" /></button>
                <button class="p-2 text-gray-400 hover:text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-900/30 rounded-lg transition-colors cursor-pointer" title="إضافة إدارة عامة"><Plus class="w-4 h-4" /></button>
              </div>
            </div>

            <!-- Level 2: General Departments -->
            <div v-show="sector.expanded" class="pr-12 pt-4 pb-2 space-y-4 border-r-2 border-dashed border-gray-200 dark:border-gray-800 mr-6">
              <div v-for="dept in sector.children" :key="dept.id" class="relative">
                <!-- Connector Line -->
                <div class="absolute right-[-48px] top-7 w-12 h-0.5 bg-gray-200 dark:bg-gray-800 border-t-2 border-dashed border-gray-200 dark:border-gray-800"></div>
                
                <div class="flex items-start gap-4 p-4 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-700 hover:border-gray-200 dark:hover:border-gray-600 transition-colors">
                  <button v-if="dept.children && dept.children.length > 0" @click="dept.expanded = !dept.expanded" class="p-1 mt-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded shadow-sm hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors cursor-pointer">
                    <ChevronDown v-if="dept.expanded" class="w-4 h-4 text-gray-500" />
                    <ChevronLeft v-else class="w-4 h-4 text-gray-500" />
                  </button>
                  <div v-else class="w-6 h-6 mt-1"></div>

                  <div class="flex-1">
                    <div class="flex items-center justify-between">
                      <h4 class="font-bold text-gray-800 dark:text-gray-200 flex items-center gap-2">
                        <Briefcase class="w-4 h-4 text-amber-500" />
                        {{ dept.name }}
                      </h4>
                      <div class="flex items-center gap-1 opacity-0 hover:opacity-100 transition-opacity" :class="{'opacity-100': dept.expanded}">
                        <button class="p-1 text-gray-400 hover:text-blue-600 rounded cursor-pointer" title="تعديل"><Edit class="w-3.5 h-3.5" /></button>
                        <button class="p-1 text-gray-400 hover:text-emerald-600 rounded cursor-pointer" title="إضافة إدارة فرعية"><Plus class="w-3.5 h-3.5" /></button>
                      </div>
                    </div>
                    
                    <p class="text-xs text-gray-500 dark:text-gray-400 mt-1.5 flex items-center gap-3">
                      <span>المدير: {{ dept.manager }}</span>
                      <span class="bg-gray-200 dark:bg-gray-700 px-1.5 py-0.5 rounded">{{ dept.code }}</span>
                    </p>

                    <!-- Level 3: Sub Departments -->
                    <div v-show="dept.expanded" class="mt-4 space-y-2 border-t border-gray-200 dark:border-gray-700 pt-3">
                      <div v-for="subDept in dept.children" :key="subDept.id" class="flex items-center justify-between p-2 rounded-lg hover:bg-white dark:hover:bg-gray-800 transition-colors group">
                        <div class="flex items-center gap-2">
                          <Layers class="w-4 h-4 text-gray-400" />
                          <span class="text-sm font-bold text-gray-700 dark:text-gray-300">{{ subDept.name }}</span>
                        </div>
                        <div class="flex items-center gap-3 text-xs text-gray-500">
                          <span>قوة: {{ subDept.personnelCount }}</span>
                          <div class="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1">
                            <button class="p-1 text-gray-400 hover:text-blue-600 rounded cursor-pointer"><Edit class="w-3.5 h-3.5" /></button>
                            <button class="p-1 text-gray-400 hover:text-emerald-600 rounded cursor-pointer"><Plus class="w-3.5 h-3.5" /></button>
                          </div>
                        </div>
                      </div>
                    </div>

                  </div>
                </div>
              </div>
            </div>

          </div>
          
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
import { ShieldAlert, Search, Plus, ChevronDown, ChevronLeft, Shield, UserCheck, Users, Edit, Briefcase, Layers } from 'lucide-vue-next'

const { t } = useI18n()
const searchQuery = ref('')

const treeData = ref([
  {
    id: 'sec-1',
    name: 'قطاع الموارد البشرية والمالية',
    manager: 'اللواء/ أحمد عبدالله',
    personnelCount: 450,
    expanded: true,
    children: [
      {
        id: 'dept-101',
        name: 'الإدارة العامة لشؤون الأفراد',
        manager: 'العميد/ صالح محمد',
        code: 'HR-PR',
        expanded: true,
        children: [
          { id: 'sub-1011', name: 'إدارة السجلات والتوثيق', personnelCount: 15 },
          { id: 'sub-1012', name: 'إدارة الترقيات والعلاوات', personnelCount: 12 },
          { id: 'sub-1013', name: 'إدارة الإجازات والتنقلات', personnelCount: 18 }
        ]
      },
      {
        id: 'dept-102',
        name: 'الإدارة العامة للشؤون المالية',
        manager: 'العقيد/ خالد سعيد',
        code: 'FI-MN',
        expanded: false,
        children: [
          { id: 'sub-1021', name: 'إدارة الرواتب والأجور', personnelCount: 22 },
          { id: 'sub-1022', name: 'إدارة الموازنة والمشتريات', personnelCount: 14 }
        ]
      }
    ]
  },
  {
    id: 'sec-2',
    name: 'قطاع العمليات والتدريب',
    manager: 'اللواء/ قاسم يحيى',
    personnelCount: 820,
    expanded: false,
    children: [
      {
        id: 'dept-201',
        name: 'الإدارة العامة للتدريب والتأهيل',
        manager: 'العميد/ سعد مبارك',
        code: 'OP-TR',
        expanded: false,
        children: [
          { id: 'sub-2011', name: 'إدارة التخطيط التدريبي', personnelCount: 8 }
        ]
      }
    ]
  }
])

const filteredTree = computed(() => {
  if (!searchQuery.value) return treeData.value

  const q = searchQuery.value.toLowerCase()
  
  return treeData.value.map(sector => {
    if (sector.name.toLowerCase().includes(q) || sector.manager.toLowerCase().includes(q)) return { ...sector, expanded: true }
    
    const filteredDepts = sector.children.filter(dept => {
      if (dept.name.toLowerCase().includes(q) || dept.manager.toLowerCase().includes(q) || dept.code.toLowerCase().includes(q)) return true
      return dept.children?.some(sub => sub.name.toLowerCase().includes(q))
    }).map(dept => {
      return {
        ...dept,
        expanded: true,
        children: dept.children?.filter(sub => 
          dept.name.toLowerCase().includes(q) || sub.name.toLowerCase().includes(q)
        )
      }
    })

    if (filteredDepts.length > 0) {
      return { ...sector, expanded: true, children: filteredDepts }
    }
    return null
  }).filter(Boolean) as any[]
})

</script>
