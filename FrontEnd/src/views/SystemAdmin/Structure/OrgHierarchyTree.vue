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
          <button @click="handleAddSector" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-sm font-bold flex items-center gap-2 transition-colors shrink-0 cursor-pointer">
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
                  <Briefcase class="w-3.5 h-3.5" /> الإدارات والفروع: {{ sector.children ? sector.children.length : 0 }}
                </p>
              </div>

              <div class="flex items-center gap-2 shrink-0">
                <button @click.stop="handleEditNode(sector)" class="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-colors cursor-pointer" title="تعديل"><Edit class="w-4 h-4" /></button>
                <button @click.stop="handleAddDept(sector)" class="p-2 text-gray-400 hover:text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-900/30 rounded-lg transition-colors cursor-pointer" title="إضافة إدارة / فرع / مديرية"><Plus class="w-4 h-4" /></button>
              </div>
            </div>

            <!-- Level 2: General Departments -->
            <div v-if="sector.expanded" class="pr-12 pt-4 pb-2 space-y-4 border-r-2 border-dashed border-gray-200 dark:border-gray-800 mr-6">
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
                      <div class="flex items-center gap-1">
                        <button @click.stop="handleEditNode(dept)" class="p-1 text-gray-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded cursor-pointer transition-colors" title="تعديل"><Edit class="w-4 h-4" /></button>
                        <button @click.stop="handleAddDivision(dept)" class="p-1 text-gray-400 hover:text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-900/30 rounded cursor-pointer transition-colors" title="إضافة إدارة فرعية/قسم"><Plus class="w-4 h-4" /></button>
                      </div>
                    </div>
                    
                    <p class="text-xs text-gray-500 dark:text-gray-400 mt-1.5 flex items-center gap-3">
                      <span>المدير: {{ dept.manager }}</span>
                      <span class="bg-gray-200 dark:bg-gray-700 px-1.5 py-0.5 rounded">{{ dept.code }}</span>
                    </p>

                    <!-- Level 3: Sub Departments -->
                    <div v-if="dept.expanded" class="mt-4 space-y-2 border-t border-gray-200 dark:border-gray-700 pt-3">
                      <div v-for="subDept in dept.children" :key="subDept.id" class="flex flex-col p-2 rounded-lg hover:bg-white dark:hover:bg-gray-800 transition-colors group">
                        <div class="flex items-center justify-between">
                          <div class="flex items-center gap-2 cursor-pointer" @click="subDept.expanded = !subDept.expanded">
                            <button v-if="subDept.children && subDept.children.length > 0" class="p-0.5 border border-gray-200 dark:border-gray-700 rounded shadow-sm hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                              <ChevronDown v-if="subDept.expanded" class="w-3.5 h-3.5 text-gray-500" />
                              <ChevronLeft v-else class="w-3.5 h-3.5 text-gray-500" />
                            </button>
                            <div v-else class="w-5 h-5"></div>
                            <Layers class="w-4 h-4 text-gray-400" />
                            <span class="text-sm font-bold text-gray-700 dark:text-gray-300">{{ subDept.name }}</span>
                          </div>
                          <div class="flex items-center gap-3 text-xs text-gray-500">
                            <span>الوحدات: {{ subDept.children ? subDept.children.length : 0 }}</span>
                            <div class="flex items-center gap-1">
                              <button @click.stop="handleEditNode(subDept)" class="p-1 text-gray-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded cursor-pointer transition-colors" title="تعديل"><Edit class="w-4 h-4" /></button>
                              <button @click.stop="handleAddUnit(subDept)" class="p-1 text-gray-400 hover:text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-900/30 rounded cursor-pointer transition-colors" title="إضافة وحدة"><Plus class="w-4 h-4" /></button>
                            </div>
                          </div>
                        </div>
                        
                        <!-- Level 4: Units -->
                        <div v-if="subDept.expanded" class="mt-2 space-y-1 border-r border-dashed border-gray-200 dark:border-gray-700 mr-6 pr-4">
                          <div v-for="unit in subDept.children" :key="unit.id" class="flex items-center justify-between p-1.5 rounded hover:bg-gray-50 dark:hover:bg-gray-700/50 group/unit">
                            <div class="flex items-center gap-2">
                              <Box class="w-3.5 h-3.5 text-gray-400" />
                              <span class="text-xs font-medium text-gray-600 dark:text-gray-400">{{ unit.name }}</span>
                            </div>
                            <div class="flex items-center gap-2 text-xs text-gray-400">
                              <span>{{ unit.code }}</span>
                              <div class="flex items-center gap-1">
                                <button @click.stop="handleEditNode(unit)" class="p-1 text-gray-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded cursor-pointer transition-colors"><Edit class="w-3.5 h-3.5" /></button>
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
      </div>
    </div>
    
    <!-- Modal -->
    <OrgNodeModal
      ref="orgModalRef"
      :is-open="isModalOpen"
      :mode="modalMode"
      :node-type="modalNodeType"
      :initial-data="modalInitialData"
      :geo-gov-options="geoGovOptions"
      @close="isModalOpen = false"
      @submit="handleModalSubmit"
    />
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { ShieldAlert, Search, Plus, ChevronDown, ChevronLeft, Shield, UserCheck, Users, Edit, Briefcase, Layers, Box } from 'lucide-vue-next'
import Swal from 'sweetalert2'
import api from '@/lib/api'
import OrgNodeModal from './components/OrgNodeModal.vue'

const { t } = useI18n()
const searchQuery = ref('')
const isLoading = ref(true)

const treeData = ref<any[]>([])

// Modal State
const isModalOpen = ref(false)
const modalMode = ref<'add' | 'edit'>('add')
const modalNodeType = ref<'sector' | 'dept' | 'division' | 'unit'>('sector')
const modalInitialData = ref<any>(null)
const currentParentNode = ref<any>(null)
const orgModalRef = ref<any>(null)
const geoGovOptions = ref<any[]>([])

const fetchOrgTree = async () => {
  isLoading.value = true
  try {
    const res = await api.get('/dictionaries/security-admins/tree/')
    const admins = res.data.data || res.data.results || res.data || []
    
    treeData.value = admins.map((admin: any) => {
      // Merge central_departments, branches, and district_police_units as children
      const children: any[] = []
      
      if (admin.central_departments) {
        admin.central_departments.forEach((dept: any) => {
          children.push({
            id: `dept-${dept.id}`,
            db_id: dept.id,
            type: 'central-departments',
            name: dept.name,
            manager: dept.head || '-',
            code: dept.code || '-',
            expanded: false,
            children: (dept.divisions || []).map((div: any) => ({
              id: `div-${div.id}`,
              db_id: div.id,
              type: 'divisions',
              name: div.name,
              personnelCount: (div.units || []).length,
              expanded: false,
              children: (div.units || []).map((u: any) => ({ id: `unit-${u.id}`, db_id: u.id, type: 'units', name: u.name, code: u.code }))
            }))
          })
        })
      }
      
      if (admin.branches) {
        admin.branches.forEach((branch: any) => {
          children.push({
            id: `branch-${branch.id}`,
            db_id: branch.id,
            type: 'branches',
            name: branch.name,
            manager: branch.head || '-',
            code: branch.code || '-',
            expanded: false,
            children: (branch.divisions || []).map((div: any) => ({
              id: `div-${div.id}`,
              db_id: div.id,
              type: 'divisions',
              name: div.name,
              personnelCount: (div.units || []).length,
              expanded: false,
              children: (div.units || []).map((u: any) => ({ id: `unit-${u.id}`, db_id: u.id, type: 'units', name: u.name, code: u.code }))
            }))
          })
        })
      }
      
      if (admin.district_police_units) {
        admin.district_police_units.forEach((dp: any) => {
          children.push({
            id: `dp-${dp.id}`,
            db_id: dp.id,
            type: 'district-police',
            name: dp.name,
            manager: dp.head || '-',
            code: dp.code || '-',
            expanded: false,
            children: (dp.divisions || []).map((div: any) => ({
              id: `div-${div.id}`,
              db_id: div.id,
              type: 'divisions',
              name: div.name,
              personnelCount: (div.units || []).length,
              expanded: false,
              children: (div.units || []).map((u: any) => ({ id: `unit-${u.id}`, db_id: u.id, type: 'units', name: u.name, code: u.code }))
            }))
          })
        })
      }

      return {
        id: `sec-${admin.id}`,
        db_id: admin.id,
        type: 'security-admins',
        name: admin.name,
        manager: admin.head || '-',
        personnelCount: children.length,
        expanded: false,
        children
      }
    })
    
    // Auto-expand first item
    if (treeData.value.length > 0) {
      treeData.value[0].expanded = true
    }
  } catch (error) {
    console.error('Error fetching org tree', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchOrgTree()
})

const filteredTree = computed(() => {
  if (!searchQuery.value) return treeData.value

  const q = searchQuery.value.toLowerCase()
  
  return treeData.value.map(sector => {
    if (sector.name.toLowerCase().includes(q) || sector.manager.toLowerCase().includes(q)) return { ...sector, expanded: true }
    
    const filteredDepts = sector.children.filter((dept: any) => {
      if (dept.name.toLowerCase().includes(q) || dept.manager.toLowerCase().includes(q) || dept.code.toLowerCase().includes(q)) return true
      return dept.children?.some((sub: any) => sub.name.toLowerCase().includes(q))
    }).map((dept: any) => {
      return {
        ...dept,
        expanded: true,
        children: dept.children?.filter((sub: any) => 
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

const handleAddSector = async () => {
  // Fetch governorates if empty
  if (geoGovOptions.value.length === 0) {
    try {
      const govRes = await api.get('/dictionaries/geo/governorates/')
      geoGovOptions.value = govRes.data.results || govRes.data || []
    } catch (e) {
      console.error(e)
    }
  }
  
  modalMode.value = 'add'
  modalNodeType.value = 'sector'
  currentParentNode.value = null
  modalInitialData.value = null
  isModalOpen.value = true
}

const handleEditNode = (node: any) => {
  modalMode.value = 'edit'
  
  if (node.type === 'security-admins') modalNodeType.value = 'sector'
  else if (node.type === 'central-departments' || node.type === 'branches' || node.type === 'district-police') modalNodeType.value = 'dept'
  else if (node.type === 'divisions') modalNodeType.value = 'division'
  else if (node.type === 'units') modalNodeType.value = 'unit'
  
  currentParentNode.value = node
  // Fetch full details if needed, but for now we have basic info in the tree node
  modalInitialData.value = {
    name: node.name,
    code: node.code !== '-' ? node.code : '',
    order: node.order || 0,
    head: node.manager !== '-' ? node.manager : '',
    head_position: node.head_position || '',
    is_active: node.is_active !== undefined ? node.is_active : true,
    geo_governorate: node.geo_governorate || '',
    type: node.type
  }
  isModalOpen.value = true
}

const handleAddDept = (sector: any) => {
  modalMode.value = 'add'
  modalNodeType.value = 'dept'
  currentParentNode.value = sector
  modalInitialData.value = null
  isModalOpen.value = true
}

const handleAddDivision = (dept: any) => {
  modalMode.value = 'add'
  modalNodeType.value = 'division'
  currentParentNode.value = dept
  modalInitialData.value = null
  isModalOpen.value = true
}

const handleAddUnit = (subDept: any) => {
  modalMode.value = 'add'
  modalNodeType.value = 'unit'
  currentParentNode.value = subDept
  modalInitialData.value = null
  isModalOpen.value = true
}

const handleModalSubmit = async ({ payload, deptType }: { payload: any, deptType: string }) => {
  try {
    if (modalMode.value === 'add') {
      if (modalNodeType.value === 'sector') {
        await api.post('/dictionaries/security-admins/', payload)
      } else if (modalNodeType.value === 'dept') {
        payload.security_admin = currentParentNode.value.db_id
        await api.post(`/dictionaries/${deptType}/`, payload)
      } else if (modalNodeType.value === 'division') {
        const parent = currentParentNode.value
        if (parent.type === 'central-departments') payload.central_department = parent.db_id
        if (parent.type === 'branches') payload.branch = parent.db_id
        if (parent.type === 'district-police') payload.district_police = parent.db_id
        await api.post('/dictionaries/divisions/', payload)
      } else if (modalNodeType.value === 'unit') {
        payload.division = currentParentNode.value.db_id
        await api.post('/dictionaries/units/', payload)
      }
      
      Swal.fire('تمت الإضافة', 'تم إضافة الجهة بنجاح', 'success')
      
    } else {
      // Edit mode
      const node = currentParentNode.value
      await api.patch(`/dictionaries/${node.type}/${node.db_id}/`, payload)
      Swal.fire('تم التحديث', 'تم تحديث البيانات بنجاح', 'success')
    }
    
    isModalOpen.value = false
    fetchOrgTree()
    
  } catch (e: any) {
    const errData = e.response?.data
    let msg = 'حدث خطأ غير معروف'
    if (errData?.error?.detail) {
      const detail = errData.error.detail
      const firstKey = Object.keys(detail)[0]
      if (firstKey && Array.isArray(detail[firstKey])) msg = detail[firstKey][0]
    } else if (errData?.name?.[0]) {
      msg = errData.name[0]
    } else if (errData?.code?.[0]) {
      msg = errData.code[0]
    }
    
    if (orgModalRef.value) {
      orgModalRef.value.setError(msg)
    } else {
      Swal.fire('خطأ', msg, 'error')
    }
  }
}

</script>
