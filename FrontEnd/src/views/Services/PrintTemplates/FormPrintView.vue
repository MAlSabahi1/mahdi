<template>
  <div class="min-h-screen bg-gray-100 print:bg-white" dir="rtl">

    <!-- شريط الأدوات (لا يُطبع) -->
    <div class="print:hidden sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm px-6 py-3 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <button @click="$router.back()" class="flex items-center gap-2 text-sm font-bold text-gray-600 hover:text-gray-900 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
          العودة للمعاملة
        </button>
        <span class="text-gray-300">|</span>
        <h1 class="text-sm font-black text-gray-900">معاينة الطباعة الرسمية</h1>
        <span v-if="form" class="text-xs font-mono text-gray-500 bg-gray-100 px-2 py-0.5 rounded">
          TX-{{ String(form.id).padStart(6, '0') }}
        </span>
      </div>
      <div class="flex items-center gap-2">
        <span v-if="form?.is_printed" class="flex items-center gap-1.5 text-xs font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-lg">
          <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
          تمت الطباعة مسبقاً
        </span>
        <button @click="handlePrint"
          class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold px-5 py-2 rounded-lg transition-all shadow-md shadow-blue-500/20">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/>
          </svg>
          طباعة الاستمارة
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-32 print:hidden">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
      <p class="text-gray-500 text-sm font-medium">جاري تحميل الاستمارة...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error || !form" class="max-w-lg mx-auto mt-20 p-8 bg-red-50 border border-red-200 rounded-2xl text-center print:hidden">
      <svg class="w-12 h-12 mx-auto text-red-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
      </svg>
      <p class="font-bold text-red-700">{{ error || 'لم يتم العثور على بيانات المعاملة' }}</p>
      <button @click="$router.back()" class="mt-4 text-sm text-red-600 underline">العودة</button>
    </div>

    <!-- نموذج الطباعة -->
    <div v-else class="max-w-[21cm] mx-auto my-6 print:my-0 shadow-xl print:shadow-none">
      <StatusChangePrintForm :form="form" />
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import StatusChangePrintForm from './StatusChangePrintForm.vue'
import { useServicesStore } from '@/stores/services'

const route = useRoute()
const router = useRouter()
const servicesStore = useServicesStore()

const id = route.params.id as string
const form = ref<any>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  if (!id) {
    error.value = 'رقم المعاملة مفقود'
    loading.value = false
    return
  }
  try {
    form.value = await servicesStore.fetchFormById(id)
  } catch (e: any) {
    error.value = 'فشل تحميل بيانات المعاملة'
  } finally {
    loading.value = false
  }
})

async function handlePrint() {
  if (!form.value) return
  try {
    await servicesStore.markFormPrinted(form.value.id)
    form.value.is_printed = true
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم تسجيل الطباعة', showConfirmButton: false, timer: 1500 })
  } catch (_) {
    // continue even if API fails
  }
  setTimeout(() => window.print(), 300)
}
</script>
