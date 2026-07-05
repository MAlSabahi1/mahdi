<template>
  <admin-layout>
    <div class="space-y-4">
      <!-- Header Area -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white dark:bg-gray-900 p-5 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-theme-xs relative overflow-hidden">
        <div class="absolute -left-6 -top-6 w-24 h-24 rounded-full bg-brand-50 dark:bg-brand-500/5 blur-2xl pointer-events-none"></div>
        <div class="flex items-center gap-4 relative z-10">
          <div class="h-12 w-12 rounded-xl bg-brand-50 dark:bg-brand-500/10 text-brand-600 dark:text-brand-400 flex items-center justify-center shrink-0 border border-brand-100 dark:border-brand-500/20">
            <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div>
            <h1 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('excel_editor.title') }}</h1>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ $t('excel_editor.subtitle') }}</p>
          </div>
        </div>
        <div class="flex gap-3 relative z-10">
          <button @click="addRow" class="flex items-center gap-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 px-5 py-2.5 rounded-lg text-sm font-medium shadow-theme-xs transition-colors cursor-pointer">
            <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
            {{ $t('excel_editor.add_row') }}
          </button>
          <button @click="saveChanges" class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 transition-colors cursor-pointer">
            <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" /></svg>
            {{ $t('excel_editor.save_changes') }}
          </button>
        </div>
      </div>

      <!-- Excel Grid Container -->
      <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-theme-xs overflow-hidden h-[calc(100vh-230px)] flex flex-col">
        <!-- Formula Bar / Toolbar -->
        <div class="flex items-center gap-3 p-3 border-b border-gray-200 dark:border-gray-800 bg-gray-50/80 dark:bg-gray-800/50">
           <div class="font-mono text-xs font-bold px-3 py-1.5 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 shadow-sm rounded-md text-gray-700 dark:text-gray-300 min-w-[60px] text-center select-none">
             {{ activeCellLabel }}
           </div>
           <div class="flex-1 relative">
             <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
               <span class="font-serif italic text-gray-400 dark:text-gray-500 font-bold">fx</span>
             </div>
             <input type="text" :value="activeCellValue" @input="updateActiveCellValue" 
                    :placeholder="$t('excel_editor.formula_bar')"
                    class="w-full text-sm border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-1.5 ps-10 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all shadow-sm" />
           </div>
        </div>

        <!-- Scrollable Grid Area -->
        <div class="flex-1 overflow-auto relative excel-grid custom-scrollbar" ref="gridContainer" @keydown="handleKeyDown" tabindex="0">
          <table class="w-full border-collapse text-[13px]">
            <thead class="sticky top-0 z-20 bg-gray-100 dark:bg-gray-800 border-b-2 border-gray-300 dark:border-gray-700 select-none shadow-sm">
              <tr>
                <!-- Row Number Column Header -->
                <th class="w-12 border-e border-gray-300 dark:border-gray-700 bg-gray-200 dark:bg-gray-700 sticky start-0 z-30 shadow-[1px_0_0_0_rgba(209,213,219,1)] dark:shadow-[1px_0_0_0_rgba(55,65,81,1)]"></th>
                
                <!-- Data Column Headers -->
                <th v-for="(col, index) in columns" :key="col.field" 
                    class="border-e border-gray-300 dark:border-gray-700 px-3 py-2.5 font-bold text-gray-700 dark:text-gray-300 text-start min-w-[150px] relative hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
                  <div class="flex items-center justify-between">
                    <span>{{ col.headerName }}</span>
                  </div>
                  <div class="absolute end-0 top-0 bottom-0 w-1 cursor-col-resize hover:bg-brand-500"></div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, rIndex) in data" :key="row.id" 
                  class="border-b border-gray-200 dark:border-gray-800 hover:bg-brand-50/30 dark:hover:bg-brand-900/10 transition-colors group">
                
                <!-- Row Number Cell -->
                <td class="w-12 border-e border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/80 sticky start-0 z-10 text-center font-medium text-gray-500 dark:text-gray-400 select-none shadow-[1px_0_0_0_rgba(229,231,235,1)] dark:shadow-[1px_0_0_0_rgba(31,41,55,1)]"
                    :class="{'bg-brand-100 text-brand-700 dark:bg-brand-900/40 dark:text-brand-400': activeRow === rIndex}">
                  {{ rIndex + 1 }}
                </td>
                
                <!-- Data Cells -->
                <td v-for="(col, cIndex) in columns" :key="col.field" 
                    class="border-e border-gray-200 dark:border-gray-800 p-0 relative bg-white dark:bg-gray-900"
                    :class="{'ring-2 ring-inset ring-brand-500 z-10': isActiveCell(rIndex, cIndex)}"
                    @mousedown="setActiveCell(rIndex, cIndex)"
                    @dblclick="startEditing(rIndex, cIndex)">
                  
                  <!-- View Mode -->
                  <div v-if="!isEditing(rIndex, cIndex)" 
                       class="px-3 py-2.5 h-full w-full truncate cursor-cell select-none whitespace-pre" 
                       :class="[row[col.field] ? 'text-gray-900 dark:text-gray-100' : 'text-gray-400 dark:text-gray-500']">
                    {{ row[col.field] || '' }}
                  </div>
                  
                  <!-- Edit Mode -->
                  <input v-else 
                         :ref="el => setEditInputRef(el, rIndex, cIndex)"
                         v-model="row[col.field]"
                         @blur="stopEditing"
                         @keydown.enter.stop.prevent="stopEditingAndMoveDown"
                         @keydown.esc.stop.prevent="stopEditing"
                         @keydown.tab.stop.prevent="handleTabInEdit"
                         class="absolute inset-0 w-full h-full px-3 py-2.5 bg-white dark:bg-gray-900 text-gray-900 dark:text-white border-0 outline-none ring-2 ring-inset ring-brand-500 z-20 shadow-lg"
                         type="text" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import Swal from 'sweetalert2'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Data Configuration
const columns = computed(() => [
  { field: 'military_number', headerName: t('excel_editor.columns.military_number') },
  { field: 'full_name', headerName: t('excel_editor.columns.full_name') },
  { field: 'rank', headerName: t('excel_editor.columns.rank') },
  { field: 'unit', headerName: t('excel_editor.columns.unit') },
  { field: 'service_type', headerName: t('excel_editor.columns.service_type') },
  { field: 'amount', headerName: t('excel_editor.columns.amount') },
  { field: 'status', headerName: t('excel_editor.columns.status') },
  { field: 'notes', headerName: t('excel_editor.columns.notes') }
])

// Data
const STORAGE_KEY = 'mahdi_services_excel_data'
const savedData = localStorage.getItem(STORAGE_KEY)
const data = ref<any[]>(savedData ? JSON.parse(savedData) : [])

// Grid State
const activeRow = ref(0)
const activeCol = ref(0)
const editingCell = ref<{r: number, c: number} | null>(null)
const gridContainer = ref<HTMLElement | null>(null)

// Refs array for dynamic inputs
const editInputs = ref<Map<string, HTMLInputElement>>(new Map())

function setEditInputRef(el: any, r: number, c: number) {
  if (el) {
    editInputs.value.set(`${r}-${c}`, el as HTMLInputElement)
  }
}

// Computed
const activeCellLabel = computed(() => {
  if (columns.value.length === 0) return ''
  const colLetter = String.fromCharCode(65 + activeCol.value)
  return `${colLetter}${activeRow.value + 1}`
})

const activeCellValue = computed(() => {
  if (data.value[activeRow.value] && columns.value[activeCol.value]) {
    const field = columns.value[activeCol.value].field
    return data.value[activeRow.value][field] || ''
  }
  return ''
})

// Methods
function addRow() {
  data.value.unshift({
    id: Date.now(),
    military_number: '',
    full_name: '',
    rank: '',
    unit: '',
    service_type: '',
    amount: '',
    status: '',
    notes: ''
  })
  activeRow.value = 0
  activeCol.value = 0
  startEditing(0, 0)
}

function updateActiveCellValue(event: Event) {
  const val = (event.target as HTMLInputElement).value
  if (data.value[activeRow.value] && columns.value[activeCol.value]) {
    const field = columns.value[activeCol.value].field
    data.value[activeRow.value][field] = val
  }
}

function isActiveCell(r: number, c: number) {
  return activeRow.value === r && activeCol.value === c
}

function isEditing(r: number, c: number) {
  return editingCell.value?.r === r && editingCell.value?.c === c
}

function setActiveCell(r: number, c: number) {
  if (isEditing(r, c)) return
  stopEditing()
  activeRow.value = r
  activeCol.value = c
  gridContainer.value?.focus()
}

function startEditing(r: number, c: number) {
  activeRow.value = r
  activeCol.value = c
  editingCell.value = { r, c }
  nextTick(() => {
    const input = editInputs.value.get(`${r}-${c}`)
    if (input) {
      input.focus()
    }
  })
}

function stopEditing() {
  editingCell.value = null
  editInputs.value.clear()
  gridContainer.value?.focus()
}

function stopEditingAndMoveDown() {
  stopEditing()
  if (activeRow.value < data.value.length - 1) {
    activeRow.value++
  }
  scrollToActiveCell()
}

function handleTabInEdit(e: KeyboardEvent) {
  stopEditing()
  if (e.shiftKey) {
    moveLeft()
  } else {
    moveRight()
  }
}

function moveRight() {
  if (activeCol.value > 0) {
    activeCol.value-- // RTL: Right arrow/tab goes left visually, decreasing col index
  } else if (activeRow.value < data.value.length - 1) {
    activeRow.value++
    activeCol.value = columns.value.length - 1
  }
  scrollToActiveCell()
}

function moveLeft() {
  if (activeCol.value < columns.value.length - 1) {
    activeCol.value++ // RTL: Left arrow/shift-tab goes right visually, increasing col index
  } else if (activeRow.value > 0) {
    activeRow.value--
    activeCol.value = 0
  }
  scrollToActiveCell()
}

function handleKeyDown(e: KeyboardEvent) {
  if (editingCell.value) return // Input handles its own events

  let moved = false

  switch (e.key) {
    case 'ArrowDown':
      if (activeRow.value < data.value.length - 1) {
        activeRow.value++
        moved = true
      }
      break
    case 'ArrowUp':
      if (activeRow.value > 0) {
        activeRow.value--
        moved = true
      }
      break
    case 'ArrowRight':
      if (activeCol.value > 0) {
        activeCol.value-- // RTL
        moved = true
      }
      break
    case 'ArrowLeft':
      if (activeCol.value < columns.value.length - 1) {
        activeCol.value++ // RTL
        moved = true
      }
      break
    case 'Tab':
      e.preventDefault()
      if (e.shiftKey) moveLeft()
      else moveRight()
      break
    case 'Enter':
      e.preventDefault()
      startEditing(activeRow.value, activeCol.value)
      break
    case 'Delete':
    case 'Backspace':
      const field = columns.value[activeCol.value].field
      data.value[activeRow.value][field] = ''
      break
    default:
      if (e.key.length === 1 && !e.ctrlKey && !e.altKey && !e.metaKey) {
        const f = columns.value[activeCol.value].field
        data.value[activeRow.value][f] = e.key
        startEditing(activeRow.value, activeCol.value)
        e.preventDefault()
      }
      break
  }

  if (moved) {
    e.preventDefault()
    scrollToActiveCell()
  }
}

function scrollToActiveCell() {
  nextTick(() => {
    if (!gridContainer.value) return
    const activeElem = gridContainer.value.querySelector('.ring-brand-500') as HTMLElement
    if (activeElem) {
      activeElem.scrollIntoView({ block: 'nearest', inline: 'nearest' })
    }
  })
}

function saveChanges() {
  Swal.fire({
    title: t('excel_editor.saving'),
    text: t('excel_editor.saving_desc'),
    icon: 'info',
    showConfirmButton: false,
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading()
      // محاكاة عملية رفع البيانات للخادم (API Call)
      setTimeout(() => {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data.value))
        Swal.fire({
          title: t('excel_editor.save_success'),
          text: t('excel_editor.save_success_desc'),
          icon: 'success',
          confirmButtonText: t('excel_editor.ok'),
          confirmButtonColor: '#10B981'
        })
      }, 1500)
    }
  })
}

onMounted(() => {
  gridContainer.value?.focus()
})
</script>

<style scoped>
.excel-grid {
  outline: none;
}
.custom-scrollbar::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 10px;
  border: 2px solid transparent;
  background-clip: padding-box;
}
:deep(.dark) .custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(75, 85, 99, 0.5);
}
</style>
