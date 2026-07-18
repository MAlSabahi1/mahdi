<template>
  <AdminLayout>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900" dir="rtl">
    <!-- Top Toolbar -->
    <header class="bg-white border-b border-gray-200 dark:bg-gray-800 dark:border-gray-700 sticky top-0 z-30">
      <div class="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center gap-4">
            <button @click="router.push('/admin/documents/list')" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            </button>
            <h1 class="text-xl font-bold text-gray-900 dark:text-white">
              {{ isEditing ? 'تعديل الاستمارة' : 'تصميم استمارة جديدة' }}
            </h1>
          </div>
          <div class="flex items-center gap-3">
            <button @click="loadPreset" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-700">
              استخدام قالب جاهز
            </button>
            <button @click="preview" class="px-4 py-2 text-sm font-medium text-blue-700 bg-blue-100 border border-transparent rounded-md shadow-sm hover:bg-blue-200 dark:bg-blue-900 dark:text-blue-200 dark:hover:bg-blue-800">
              معاينة
            </button>
            <button @click="save" :disabled="isSaving" class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-brand-600 border border-transparent rounded-md shadow-sm hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 disabled:opacity-50">
              <svg v-if="isSaving" class="w-4 h-4 mr-2 -ml-1 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              حفظ
            </button>
          </div>
        </div>
      </div>
    </header>

    <div class="px-4 py-8 mx-auto max-w-7xl sm:px-6 lg:px-8 flex gap-6 items-start relative">
      
      <!-- Right Sidebar: Settings & Tools -->
      <aside class="w-80 flex-shrink-0 space-y-6 sticky top-24">
        
        <!-- General Settings -->
        <div class="bg-white rounded-lg shadow dark:bg-gray-800 p-5">
          <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">إعدادات عامة</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">اسم الاستمارة</label>
              <input v-model="form.name" type="text" class="block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:border-brand-500 focus:ring-brand-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white sm:text-sm">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">الرمز (Slug)</label>
              <input v-model="form.slug" type="text" dir="ltr" class="block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:border-brand-500 focus:ring-brand-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white sm:text-sm">
              <p class="mt-1 text-xs text-gray-500">حروف إنجليزية بدون مسافات</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">التصنيف</label>
              <select v-model="form.category" class="block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:border-brand-500 focus:ring-brand-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white sm:text-sm">
                <option value="رسمية">رسمية</option>
                <option value="إدارية">إدارية</option>
                <option value="شؤون أفراد">شؤون أفراد</option>
                <option value="أخرى">أخرى</option>
              </select>
            </div>
            <div class="flex items-center">
              <input v-model="form.is_active" id="is_active" type="checkbox" class="w-4 h-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500 dark:border-gray-600 dark:bg-gray-700">
              <label for="is_active" class="block ml-2 mr-2 text-sm text-gray-900 dark:text-gray-300">مفعّلة ومتاحة للاستخدام</label>
            </div>
          </div>
        </div>

        <!-- Layout Settings -->
        <div class="bg-white rounded-lg shadow dark:bg-gray-800 p-5">
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

        <!-- Dynamic Fields Helper -->
        <div class="bg-white rounded-lg shadow border border-gray-100 dark:border-gray-700 dark:bg-gray-800 p-5 mt-4">
          <h2 class="text-sm font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
            <svg class="w-4 h-4 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            الحقول الديناميكية المتوفرة
          </h2>
          <p class="text-xs text-gray-500 dark:text-gray-400 mb-4 leading-relaxed">
            اضغط على أي متغير أدناه لنسخه، ثم ألصقه في المكان المناسب داخل المحرر. سيتم استبداله تلقائياً بالبيانات الحقيقية عند الطباعة.
          </p>
          <ul class="space-y-4">
            <li class="flex flex-col gap-1.5">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-gray-700 dark:text-gray-300">الاسم الرباعي</span>
                <span @click="copyField('الاسم_الرباعي')" class="cursor-pointer px-2 py-0.5 text-[11px] font-mono bg-blue-50 text-blue-700 rounded border border-blue-200 hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800 transition-colors" title="اضغط للنسخ" v-text="'{{الاسم_الرباعي}}'"></span>
              </div>
              <span class="text-[10px] text-gray-400 dark:text-gray-500">مثال: أحمد محمد علي صالح</span>
            </li>
            <li class="flex flex-col gap-1.5">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-gray-700 dark:text-gray-300">الرقم العسكري</span>
                <span @click="copyField('الرقم_العسكري')" class="cursor-pointer px-2 py-0.5 text-[11px] font-mono bg-blue-50 text-blue-700 rounded border border-blue-200 hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800 transition-colors" title="اضغط للنسخ" v-text="'{{الرقم_العسكري}}'"></span>
              </div>
              <span class="text-[10px] text-gray-400 dark:text-gray-500">مثال: 987654321</span>
            </li>
            <li class="flex flex-col gap-1.5">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-gray-700 dark:text-gray-300">الرتبة العسكرية</span>
                <span @click="copyField('الرتبة')" class="cursor-pointer px-2 py-0.5 text-[11px] font-mono bg-blue-50 text-blue-700 rounded border border-blue-200 hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800 transition-colors" title="اضغط للنسخ" v-text="'{{الرتبة}}'"></span>
              </div>
              <span class="text-[10px] text-gray-400 dark:text-gray-500">مثال: ملازم أول، جندي، إلخ</span>
            </li>
            <li class="flex flex-col gap-1.5">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-gray-700 dark:text-gray-300">جهة العمل / الوحدة</span>
                <span @click="copyField('الوحدة')" class="cursor-pointer px-2 py-0.5 text-[11px] font-mono bg-blue-50 text-blue-700 rounded border border-blue-200 hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800 transition-colors" title="اضغط للنسخ" v-text="'{{الوحدة}}'"></span>
              </div>
              <span class="text-[10px] text-gray-400 dark:text-gray-500">مثال: الإدارة العامة للشؤون الإدارية</span>
            </li>
            <li class="flex flex-col gap-1.5">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-gray-700 dark:text-gray-300">تاريخ اليوم</span>
                <span @click="copyField('تاريخ_اليوم')" class="cursor-pointer px-2 py-0.5 text-[11px] font-mono bg-blue-50 text-blue-700 rounded border border-blue-200 hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800 transition-colors" title="اضغط للنسخ" v-text="'{{تاريخ_اليوم}}'"></span>
              </div>
              <span class="text-[10px] text-gray-400 dark:text-gray-500">تاريخ طباعة الاستمارة الفعلي</span>
            </li>
          </ul>
        </div>
      </aside>

      <!-- Main Canvas -->
      <main class="flex-1 min-w-0">
        <div class="bg-white shadow-lg rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700 dark:bg-gray-800">
          
          <div class="p-8 pb-16 min-h-[800px] flex flex-col">
            
            <!-- Header Section -->
            <div class="mb-8 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-4 relative group">
              <span class="absolute -top-3 right-4 bg-white dark:bg-gray-800 px-2 text-xs font-semibold text-gray-500">الترويسة (Header)</span>
              
              <div class="grid gap-4" :style="`grid-template-columns: repeat(${form.header_columns}, minmax(0, 1fr));`">
                <div v-for="(block, index) in form.header_columns" :key="'h'+index">
                  <CKEditorComponent v-model="form.header_blocks[index]" height="120px" />
                </div>
              </div>
            </div>

            <!-- Body Section -->
            <div class="flex-1 mb-8 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-4 relative group">
              <span class="absolute -top-3 right-4 bg-white dark:bg-gray-800 px-2 text-xs font-semibold text-gray-500">محتوى الاستمارة (Body)</span>
              <CKEditorComponent v-model="form.body_content" height="400px" />
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
  category: 'رسمية',
  is_active: true,
  header_columns: 3,
  header_blocks: ['','',''],
  body_content: '',
  footer_columns: 3,
  footer_blocks: ['','',''],
  page_size: 'A4',
  orientation: 'portrait'
})

const copyField = (fieldName: string) => {
  const text = `{{${fieldName}}}`
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
    const res = await api.get(`/service-cycle/admin/document-templates/${templateId}/`)
    if (res.data.success) {
      form.value = { ...res.data.data }
      updateHeaderBlocks()
      updateFooterBlocks()
    }
  } catch (error) {
    Swal.fire('خطأ', 'تعذر تحميل بيانات الاستمارة', 'error')
  }
}

const loadPreset = async () => {
  const result = await Swal.fire({
    title: 'اختيار قالب جاهز',
    input: 'select',
    inputOptions: {
      'official': 'استمارة رسمية (3 أعمدة هيدر / 3 فوتر)',
      'letter': 'خطاب إداري (عمودين هيدر / 1 فوتر)',
      'meeting': 'محضر اجتماع (3 أعمدة هيدر / 2 فوتر)'
    },
    inputPlaceholder: 'اختر القالب...',
    showCancelButton: true,
    confirmButtonText: 'تطبيق',
    cancelButtonText: 'إلغاء'
  })

  if (result.isConfirmed) {
    if (result.value === 'official') {
      form.value.header_columns = 3
      form.value.footer_columns = 3
      form.value.header_blocks = [
        '<p style="text-align:right;">الجمهورية اليمنية<br>وزارة الداخلية<br>شؤون الأفراد</p>',
        '<p style="text-align:center;"><strong>[شعار الجمهورية]</strong></p>',
        '<p style="text-align:left;">التاريخ: {{تاريخ_اليوم}}<br>الرقم: .........</p>'
      ]
      form.value.body_content = '<h2 style="text-align:center;">استمارة تحديث بيانات</h2><p>...</p>'
      form.value.footer_blocks = [
        '<p style="text-align:center;">المختص<br>...........</p>',
        '<p style="text-align:center;">المدير المباشر<br>...........</p>',
        '<p style="text-align:center;">المدير العام<br>...........</p>'
      ]
    } else if (result.value === 'letter') {
      form.value.header_columns = 2
      form.value.footer_columns = 1
      form.value.header_blocks = [
        '<p style="text-align:right;">الجمهورية اليمنية<br>وزارة الداخلية</p>',
        '<p style="text-align:left;">التاريخ: {{تاريخ_اليوم}}</p>'
      ]
      form.value.body_content = '<p>الأخ / .................................... المحترم</p><p>تحية طيبة وبعد،</p><p>الموضوع: ..........................</p><p>...</p>'
      form.value.footer_blocks = [
        '<p style="text-align:left;">توقيع المدير<br>...........</p>'
      ]
    } else if (result.value === 'meeting') {
      form.value.header_columns = 3
      form.value.footer_columns = 2
      form.value.header_blocks = ['','<h2 style="text-align:center;">محضر اجتماع</h2>','']
      form.value.body_content = '<p>إنه في يوم (........) الموافق (........) تم عقد اجتماع برئاسة...</p>'
      form.value.footer_blocks = [
        '<p style="text-align:right;">مقرر الاجتماع<br>...........</p>',
        '<p style="text-align:left;">رئيس الاجتماع<br>...........</p>'
      ]
    }
  }
}

const save = async () => {
  if (!form.value.name || !form.value.slug) {
    Swal.fire('تنبيه', 'الرجاء إدخال اسم الاستمارة والرمز', 'warning')
    return
  }

  isSaving.value = true
  try {
    if (isEditing.value) {
      await api.put(`/service-cycle/admin/document-templates/${templateId}/`, form.value)
      Swal.fire('تم', 'تم تحديث الاستمارة بنجاح', 'success')
    } else {
      const res = await api.post('/service-cycle/admin/document-templates/', form.value)
      Swal.fire('تم', 'تم إنشاء الاستمارة بنجاح', 'success')
      router.push(`/admin/documents/builder/${res.data.data.id}`)
    }
  } catch (error: any) {
    Swal.fire('خطأ', error.response?.data?.error || 'حدث خطأ أثناء الحفظ', 'error')
  } finally {
    isSaving.value = false
  }
}

const preview = () => {
  localStorage.setItem('document_builder_draft', JSON.stringify(form.value))
  window.open(router.resolve(`/admin/documents/preview/draft`).href, '_blank')
}

onMounted(() => {
  if (isEditing.value) {
    loadTemplate()
  }
})
</script>

<style scoped>
/* Ensure grid cols classes are generated by tailwind */
.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
.grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
</style>
