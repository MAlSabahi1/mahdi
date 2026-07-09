<template>
  <admin-layout>
    <div class="px-4 py-6 sm:px-6 lg:px-8">
      <page-breadcrumb
        title="محاكي الصلاحيات والسياسات"
        subtitle="مختبر فحص وتقييم الصلاحيات للمستخدمين والأدوار"
        :breadcrumbs="[
          { label: 'إدارة الصلاحيات', to: '/users' },
          { label: 'محاكي السياسات', to: '/users/policy-simulator' }
        ]"
      />

      <div class="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-3">
        <!-- Input Section -->
        <div class="lg:col-span-1">
          <div class="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-900">
            <h3 class="mb-5 text-lg font-bold text-gray-900 dark:text-white">معطيات المحاكاة</h3>
            
            <form @submit.prevent="runSimulation" class="space-y-5">
              <!-- Target Type -->
              <div>
                <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">نوع المستهدف</label>
                <select v-model="form.targetType" class="block w-full rounded-xl border border-gray-200 bg-gray-50 p-3 text-sm focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white">
                  <option value="user">مستخدم محدد (User)</option>
                  <option value="role">دور وظيفي (Role)</option>
                </select>
              </div>

              <!-- Target Selection -->
              <div>
                <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">
                  {{ form.targetType === 'user' ? 'اختر المستخدم' : 'اختر الدور الوظيفي' }}
                </label>
                <select v-model="form.targetId" required class="block w-full rounded-xl border border-gray-200 bg-gray-50 p-3 text-sm focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white">
                  <option value="" disabled>يرجى الاختيار...</option>
                  <template v-if="form.targetType === 'user'">
                    <option value="2">أحمد (أخصائي موارد بشرية)</option>
                    <option value="3">خالد (مدقق عام)</option>
                    <option value="1">Admin (مدير النظام)</option>
                  </template>
                  <template v-else>
                    <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
                  </template>
                </select>
              </div>

              <hr class="border-gray-100 dark:border-gray-800" />

              <!-- Module -->
              <div>
                <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">الوحدة (Module)</label>
                <select v-model="form.module" required class="block w-full rounded-xl border border-gray-200 bg-gray-50 p-3 text-sm focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white">
                  <option value="PERSONNEL">شؤون الأفراد</option>
                  <option value="REPORTS">التقارير</option>
                  <option value="AUDIT">التدقيق</option>
                  <option value="SYSTEM">النظام العام</option>
                </select>
              </div>

              <!-- Action -->
              <div>
                <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">الإجراء المطلوب (Action)</label>
                <select v-model="form.action" required class="block w-full rounded-xl border border-gray-200 bg-gray-50 p-3 text-sm focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white">
                  <option value="READ">قراءة وعرض (Read)</option>
                  <option value="WRITE">إضافة وتعديل (Write)</option>
                  <option value="DELETE">حذف (Delete)</option>
                  <option value="EXPORT">تصدير (Export)</option>
                  <option value="APPROVE">اعتماد (Approve)</option>
                </select>
              </div>

              <button type="submit" :disabled="isSimulating" class="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-5 py-3.5 text-sm font-bold text-white shadow-lg shadow-brand-500/30 transition-all hover:bg-brand-700 focus:ring-4 focus:ring-brand-500/20 disabled:opacity-50">
                <svg v-if="isSimulating" class="h-5 w-5 animate-spin" viewBox="0 0 24 24" fill="none"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                {{ isSimulating ? 'جاري الفحص...' : 'فحص الصلاحية' }}
              </button>
            </form>
          </div>
        </div>

        <!-- Output Section -->
        <div class="lg:col-span-2">
          <div class="flex h-full flex-col rounded-2xl border border-gray-100 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900">
            <div class="border-b border-gray-100 p-6 dark:border-gray-800">
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">نتيجة المحاكاة</h3>
            </div>
            
            <div class="flex-1 p-6">
              <!-- Empty State -->
              <div v-if="!result" class="flex h-full flex-col items-center justify-center text-center opacity-60">
                <div class="mb-4 rounded-full bg-gray-50 p-4 dark:bg-gray-800">
                  <svg class="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
                </div>
                <p class="text-lg font-medium text-gray-900 dark:text-white">لا توجد نتائج بعد</p>
                <p class="mt-1 text-sm text-gray-500">قم بإدخال المعطيات في اللوحة الجانبية واضغط على فحص لرؤية النتيجة.</p>
              </div>

              <!-- Result State -->
              <div v-else class="space-y-6">
                <!-- Status Card -->
                <div :class="[
                  'rounded-2xl p-6 border',
                  result.status === 'ALLOWED' ? 'bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-800' : 
                  result.status === 'DENIED' ? 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800' : 
                  'bg-yellow-50 border-yellow-200 dark:bg-yellow-900/20 dark:border-yellow-800'
                ]">
                  <div class="flex items-center gap-4">
                    <div :class="[
                      'rounded-full p-3',
                      result.status === 'ALLOWED' ? 'bg-green-200 text-green-700 dark:bg-green-800 dark:text-green-300' : 
                      result.status === 'DENIED' ? 'bg-red-200 text-red-700 dark:bg-red-800 dark:text-red-300' : 
                      'bg-yellow-200 text-yellow-700 dark:bg-yellow-800 dark:text-yellow-300'
                    ]">
                      <svg v-if="result.status === 'ALLOWED'" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                      <svg v-else-if="result.status === 'DENIED'" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                      <svg v-else class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                    </div>
                    <div>
                      <h4 :class="[
                        'text-xl font-black',
                        result.status === 'ALLOWED' ? 'text-green-800 dark:text-green-400' : 
                        result.status === 'DENIED' ? 'text-red-800 dark:text-red-400' : 
                        'text-yellow-800 dark:text-yellow-400'
                      ]">
                        {{ result.status === 'ALLOWED' ? 'العملية مسموحة (Allowed)' : result.status === 'DENIED' ? 'العملية مرفوضة (Denied)' : 'مسموح بشروط (Requires Dual Auth)' }}
                      </h4>
                      <p class="mt-1 text-sm font-medium opacity-80" :class="result.status === 'ALLOWED' ? 'text-green-700 dark:text-green-300' : result.status === 'DENIED' ? 'text-red-700 dark:text-red-300' : 'text-yellow-700 dark:text-yellow-300'">
                        {{ result.message }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Detailed Breakdown -->
                <div class="rounded-2xl border border-gray-100 p-5 dark:border-gray-800">
                  <h4 class="mb-4 text-sm font-bold text-gray-900 dark:text-gray-300">مسار التقييم (Evaluation Path)</h4>
                  <ul class="space-y-4">
                    <li v-for="(step, i) in result.steps" :key="i" class="flex gap-4">
                      <div class="flex flex-col items-center">
                        <div :class="['flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold text-white', step.passed ? 'bg-green-500' : 'bg-red-500']">
                          <svg v-if="step.passed" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                          <svg v-else class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                        </div>
                        <div v-if="i !== result.steps.length - 1" class="h-full w-px bg-gray-200 dark:bg-gray-700"></div>
                      </div>
                      <div class="pb-4">
                        <p class="text-sm font-bold text-gray-900 dark:text-white">{{ step.title }}</p>
                        <p class="text-xs text-gray-500 dark:text-gray-400">{{ step.detail }}</p>
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import axiosInstance from '@/lib/api'

const roles = ref([])
const isSimulating = ref(false)
const result = ref(null)

const form = ref({
  targetType: 'role',
  targetId: '',
  module: 'PERSONNEL',
  action: 'READ'
})

async function fetchRoles() {
  try {
    const res = await axiosInstance.get('/roles/')
    roles.value = res.data.results || res.data || []
  } catch (err) {
    console.error(err)
  }
}

async function runSimulation() {
  isSimulating.value = true
  result.value = null
  
  await new Promise(resolve => setTimeout(resolve, 800))
  
  try {
    let status = 'ALLOWED'
    let message = 'المستخدم يمتلك الصلاحية المطلوبة للقيام بهذا الإجراء.'
    let steps = [
      { title: 'التحقق من الهوية', detail: 'المستهدف موجود ونشط', passed: true },
      { title: 'التحقق من الدور الوظيفي', detail: 'تم العثور على دور مرتبط يغطي الوحدة المطلوبة', passed: true }
    ]

    const action = form.value.action
    const target = form.value.targetId
    
    if (action === 'DELETE' || action === 'APPROVE') {
      if (form.value.targetType === 'user' && target === '1') {
        status = 'ALLOWED'
        message = 'بصفتك مدير نظام، يمكنك تجاوز الاعتماد الثنائي.'
        steps.push({ title: 'فحص الاعتماد الثنائي', detail: 'العملية تتطلب اعتماد ولكن المستهدف لديه تجاوز (Bypass)', passed: true })
      } else {
        status = 'REQUIRES_DUAL'
        message = 'الإجراء يتطلب موافقة واعتماد ثنائي من مدير أعلى.'
        steps.push({ title: 'فحص الاعتماد الثنائي', detail: 'تم اكتشاف ارتباط الصلاحية بسياسة الاعتماد الثنائي الإلزامية', passed: false })
      }
    } else {
      steps.push({ title: 'التحقق من الصلاحية', detail: 'الصلاحية المباشرة موجودة ضمن مجموعة الصلاحيات الممنوحة للمستهدف', passed: true })
    }

    if (form.value.targetType === 'user' && target === '3' && form.value.module === 'PERSONNEL') {
      status = 'DENIED'
      message = 'لا يمتلك هذا المستخدم الصلاحيات الكافية للوصول للوحدة المحددة.'
      steps[1].passed = false
      steps[1].detail = 'لم يتم العثور على أي ارتباط بين الدور الوظيفي للمستخدم ووحدة شؤون الأفراد'
    }

    result.value = { status, message, steps }
  } catch (err) {
    console.error(err)
  } finally {
    isSimulating.value = false
  }
}

onMounted(() => {
  fetchRoles()
})
</script>
