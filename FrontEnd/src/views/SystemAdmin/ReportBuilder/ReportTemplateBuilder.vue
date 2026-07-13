<template>
  <AdminLayout>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900" dir="rtl">
    <!-- Top Toolbar -->
    <header class="bg-white border-b border-gray-200 dark:bg-gray-800 dark:border-gray-700 sticky top-0 z-30">
      <div class="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center gap-4">
            <button @click="router.push('/admin/reports/templates/list')" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            </button>
            <h1 class="text-xl font-bold text-gray-900 dark:text-white">
              {{ isEditing ? 'تعديل قالب التقرير' : 'تصميم قالب تقرير جديد' }}
            </h1>
          </div>
          <div class="flex items-center gap-3">
            <button @click="preview" class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-700">
              <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
              معاينة القالب
            </button>
            <button @click="save" :disabled="isSaving" class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-brand-600 border border-transparent rounded-md shadow-sm hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 disabled:opacity-50">
              <svg v-if="isSaving" class="w-4 h-4 ml-2 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              {{ isSaving ? 'جاري الحفظ...' : 'حفظ القالب' }}
            </button>
          </div>
        </div>
      </div>
    </header>

    <div class="flex max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 gap-8 items-start">
      
      <!-- Sidebar Settings -->
      <aside class="w-80 shrink-0">
        <div class="bg-white rounded-lg shadow border border-gray-200 dark:border-gray-700 dark:bg-gray-800 p-5 mb-4">
          <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">إعدادات القالب</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">اسم القالب <span class="text-red-500">*</span></label>
              <input type="text" v-model="form.name" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="مثال: القالب الرئيسي">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">الرمز (Slug) <span class="text-red-500">*</span></label>
              <input type="text" v-model="form.slug" dir="ltr" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="main_template">
              <p class="text-[11px] text-gray-500 mt-1">يجب أن يحتوي على حروف إنجليزية وأرقام وشرطة سفلية فقط بدون مسافات.</p>
            </div>
            <div class="flex items-center mt-4">
              <input id="is_active" type="checkbox" v-model="form.is_active" class="w-4 h-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500 dark:bg-gray-700 dark:border-gray-600">
              <label for="is_active" class="mr-2 block text-sm text-gray-900 dark:text-white">مفعّل وجاهز للاستخدام</label>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow border border-gray-200 dark:border-gray-700 dark:bg-gray-800 p-5">
          <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">التخطيط (Layout)</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">أعمدة الترويسة (Header)</label>
              <div class="flex items-center gap-3">
                <button @click="changeColumns('header', -1)" type="button" class="w-8 h-8 flex items-center justify-center rounded-md bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 font-bold transition-colors shadow-sm border border-gray-200 dark:border-gray-700">-</button>
                <span class="w-8 text-center font-bold text-gray-900 dark:text-white">{{ form.header_columns }}</span>
                <button @click="changeColumns('header', 1)" type="button" class="w-8 h-8 flex items-center justify-center rounded-md bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 font-bold transition-colors shadow-sm border border-gray-200 dark:border-gray-700">+</button>
              </div>
            </div>
            <hr class="border-gray-200 dark:border-gray-700">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">أعمدة التذييل (Footer)</label>
              <div class="flex items-center gap-3">
                <button @click="changeColumns('footer', -1)" type="button" class="w-8 h-8 flex items-center justify-center rounded-md bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 font-bold transition-colors shadow-sm border border-gray-200 dark:border-gray-700">-</button>
                <span class="w-8 text-center font-bold text-gray-900 dark:text-white">{{ form.footer_columns }}</span>
                <button @click="changeColumns('footer', 1)" type="button" class="w-8 h-8 flex items-center justify-center rounded-md bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 font-bold transition-colors shadow-sm border border-gray-200 dark:border-gray-700">+</button>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow border border-gray-100 dark:border-gray-700 dark:bg-gray-800 p-5 mt-4">
          <h2 class="text-sm font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
            <svg class="w-4 h-4 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            الحقول الديناميكية المتوفرة
          </h2>
          <p class="text-xs text-gray-500 dark:text-gray-400 mb-4 leading-relaxed">
            اضغط على أي متغير أدناه لنسخه، ثم ألصقه في المحرر لكي يظهر في التقرير.
          </p>
          <ul class="space-y-4">
            <li class="flex flex-col gap-1.5">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-gray-700 dark:text-gray-300">تاريخ التقرير</span>
                <span @click="copyField('{{تاريخ_التقرير}}')" class="cursor-pointer px-2 py-0.5 text-[11px] font-mono bg-blue-50 text-blue-700 rounded border border-blue-200 hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800 transition-colors" title="اضغط للنسخ">{{تاريخ_التقرير}}</span>
              </div>
              <span class="text-[10px] text-gray-400 dark:text-gray-500">التاريخ الفعلي لاستخراج التقرير</span>
            </li>
            <li class="flex flex-col gap-1.5">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-gray-700 dark:text-gray-300">مُصدّر التقرير</span>
                <span @click="copyField('{{اسم_المستخدم}}')" class="cursor-pointer px-2 py-0.5 text-[11px] font-mono bg-blue-50 text-blue-700 rounded border border-blue-200 hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800 transition-colors" title="اضغط للنسخ">{{اسم_المستخدم}}</span>
              </div>
              <span class="text-[10px] text-gray-400 dark:text-gray-500">اسم المستخدم الذي قام بطباعة التقرير</span>
            </li>
          </ul>
        </div>
      </aside>

      <!-- Main Canvas -->
      <main class="flex-1 min-w-0">
        <div class="bg-white shadow-lg rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700 dark:bg-gray-800">
          
          <div class="p-8 min-h-[600px] flex flex-col">
            
            <!-- Header Section -->
            <div class="mb-8 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-4 relative group">
              <span class="absolute -top-3 right-4 bg-white dark:bg-gray-800 px-2 text-xs font-semibold text-gray-500">الترويسة (Header)</span>
              
              <div class="grid gap-4" :style="`grid-template-columns: repeat(${form.header_columns}, minmax(0, 1fr));`">
                <div v-for="(block, index) in form.header_columns" :key="'h'+index">
                  <CKEditorComponent v-model="form.header_blocks[index]" height="120px" />
                </div>
              </div>
            </div>

            <!-- Body Placeholder -->
            <div class="flex-1 mb-8 border-2 border-dashed border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 rounded-xl p-8 flex items-center justify-center">
              <div class="text-center">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                <p class="mt-2 text-sm text-gray-500">محتوى التقرير (الجداول والبيانات) سيتم إدراجه هنا تلقائياً</p>
              </div>
            </div>

            <!-- Footer Section -->
            <div class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-4 relative group">
              <span class="absolute -top-3 right-4 bg-white dark:bg-gray-800 px-2 text-xs font-semibold text-gray-500">التذييل (التوقيعات - Footer)</span>
              
              <div class="grid gap-4" :style="`grid-template-columns: repeat(${form.footer_columns}, minmax(0, 1fr));`">
                <div v-for="(block, index) in form.footer_columns" :key="'f'+index">
                  <CKEditorComponent v-model="form.footer_blocks[index]" height="150px" />
                </div>
              </div>
            </div>

          </div>
        </div>
      </main>

    </div>
  </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/lib/api'
import Swal from 'sweetalert2'
import CKEditorComponent from '@/components/common/CKEditorComponent.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'

const router = useRouter()
const route = useRoute()
const templateId = route.params.id

const isEditing = ref(!!templateId)
const isSaving = ref(false)

const form = ref({
  name: '',
  slug: '',
  is_active: true,
  header_columns: 3,
  header_blocks: ['','',''],
  footer_columns: 1,
  footer_blocks: ['']
})

const copyField = (text: string) => {
  navigator.clipboard.writeText(text)
  Swal.fire({
    title: 'تم النسخ',
    text: 'تم نسخ المتغير، الصقه في المحرر',
    icon: 'success',
    toast: true,
    position: 'bottom-end',
    showConfirmButton: false,
    timer: 2000
  })
}

const changeColumns = (section: 'header' | 'footer', amount: number) => {
  if (section === 'header') {
    const newVal = form.value.header_columns + amount
    if (newVal >= 1 && newVal <= 6) {
      form.value.header_columns = newVal
      updateHeaderBlocks()
    }
  } else {
    const newVal = form.value.footer_columns + amount
    if (newVal >= 1 && newVal <= 6) {
      form.value.footer_columns = newVal
      updateFooterBlocks()
    }
  }
}

const updateHeaderBlocks = () => {
  const currentLength = form.value.header_blocks.length
  const newLength = form.value.header_columns
  if (newLength > currentLength) {
    for (let i = currentLength; i < newLength; i++) form.value.header_blocks.push('')
  } else if (newLength < currentLength) {
    form.value.header_blocks = form.value.header_blocks.slice(0, newLength)
  }
}

const updateFooterBlocks = () => {
  const currentLength = form.value.footer_blocks.length
  const newLength = form.value.footer_columns
  if (newLength > currentLength) {
    for (let i = currentLength; i < newLength; i++) form.value.footer_blocks.push('')
  } else if (newLength < currentLength) {
    form.value.footer_blocks = form.value.footer_blocks.slice(0, newLength)
  }
}

const loadTemplate = async () => {
  try {
    const res = await api.get(`/reports/templates/${templateId}/`)
    form.value = { ...res.data }
    updateHeaderBlocks()
    updateFooterBlocks()
  } catch (error) {
    Swal.fire('خطأ', 'تعذر تحميل بيانات القالب', 'error')
  }
}

const save = async () => {
  if (!form.value.name?.trim()) {
    Swal.fire('تنبيه', 'الرجاء إدخال اسم القالب', 'warning')
    return
  }

  if (!form.value.slug?.trim()) {
    Swal.fire('تنبيه', 'الرجاء إدخال الرمز (Slug)', 'warning')
    return
  }

  const slugRegex = /^[a-zA-Z0-9_-]+$/
  if (!slugRegex.test(form.value.slug.trim())) {
    Swal.fire('تنبيه', 'الرمز يجب أن يحتوي فقط على حروف إنجليزية، أرقام، وشرطة سفلية (بدون مسافات)', 'warning')
    return
  }

  isSaving.value = true
  try {
    if (isEditing.value) {
      await api.put(`/reports/templates/${templateId}/`, form.value)
      Swal.fire('تم', 'تم تحديث القالب بنجاح', 'success')
    } else {
      const res = await api.post('/reports/templates/', form.value)
      Swal.fire('تم', 'تم إنشاء القالب بنجاح', 'success')
      router.push(`/admin/reports/templates/builder/${res.data.id}`)
    }
  } catch (error: any) {
    let errMsg = 'حدث خطأ أثناء الحفظ'
    if (error.response?.data?.error) {
      if (typeof error.response.data.error === 'string') {
        errMsg = error.response.data.error
      } else if (error.response.data.error.message) {
        errMsg = error.response.data.error.message
      }
    }
    // We only show Swal if the global interceptor didn't already handle it (or just use it to be safe)
    Swal.fire('خطأ', errMsg, 'error')
  } finally {
    isSaving.value = false
  }
}

const preview = () => {
  localStorage.setItem('report_template_draft', JSON.stringify(form.value))
  window.open(router.resolve(`/admin/reports/templates/preview/draft`).href, '_blank')
}

onMounted(() => {
  if (isEditing.value) {
    loadTemplate()
  }
})
</script>
