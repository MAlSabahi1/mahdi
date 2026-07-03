<template>
  <admin-layout>
    <PageBreadcrumb pageTitle="أداة محاكاة واختبار الصلاحيات" />

    <div class="space-y-6" dir="rtl">
      <!-- Info Header -->
      <div class="p-4 rounded-2xl bg-indigo-500/10 border border-indigo-200 dark:border-indigo-850 text-indigo-800 dark:text-indigo-200 text-xs leading-relaxed">
        <strong>🔍 محاكي السياسات وصلاحيات الوصول (Policy Simulator):</strong>
        تساعدك هذه الأداة على استكشاف وتدقيق قرارات نظام الأمان. يمكنك اختيار أي مستخدم وتحديد الصلاحية والظروف الجغرافية أو الإدارية المطلوبة، وسيقوم المحاكي بتتبع شروط الوصول خطوة بخطوة (RBAC & ABAC) لتوضيح سبب السماح بالوصول أو الرفض الأمني.
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Configuration Form (1/3 width) -->
        <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5 shadow-sm space-y-4 h-fit">
          <h3 class="text-sm font-black text-gray-900 dark:text-white border-b border-gray-100 dark:border-gray-800 pb-3 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2050/svg" class="w-5 h-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
            </svg>
            إعدادات سيناريو المحاكاة
          </h3>

          <!-- Select User -->
          <div>
            <label class="text-[11px] font-bold text-gray-400 block mb-1.5">المستخدم المستهدف بالدراسة</label>
            <select
              v-model="selectedUserId"
              class="w-full text-xs px-3 py-2.5 rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 text-right cursor-pointer"
              @change="handleUserChange"
            >
              <option value="" disabled>اختر مستخدماً من القائمة...</option>
              <option v-for="user in users" :key="user.id" :value="user.id">
                {{ user.username }} ({{ user.full_name || 'بدون اسم' }})
              </option>
            </select>
          </div>

          <!-- Select Permission / Action -->
          <div>
            <label class="text-[11px] font-bold text-gray-400 block mb-1.5">الصلاحية المراد اختبارها</label>
            <select
              v-model="targetPermission"
              class="w-full text-xs px-3 py-2.5 rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 text-right cursor-pointer"
            >
              <option value="" disabled>اختر الصلاحية...</option>
              <optgroup label="إدارة المستخدمين والصلاحيات">
                <option value="users.view">عرض المستخدمين (users.view)</option>
                <option value="users.manage">إدارة الحسابات (users.manage)</option>
                <option value="roles.manage">إدارة الأدوار والصلاحيات (roles.manage)</option>
              </optgroup>
              <optgroup label="شؤون الأفراد والبيانات الشخصية">
                <option value="personnel.view.all">عرض جميع الأفراد (personnel.view.all)</option>
                <option value="personnel.view.security_admin">عرض أفراد إدارة الأمن الخاصة (personnel.view.security_admin)</option>
                <option value="personnel.create">إضافة فرد جديد (personnel.create)</option>
                <option value="personnel.edit">تعديل ملف فرد (personnel.edit)</option>
              </optgroup>
              <optgroup label="إدارة الكشوفات والخدمات">
                <option value="services.approve">اعتماد كشوفات الترقيات (services.approve)</option>
                <option value="services.reconciliation">إجراء المطابقات الفنية (services.reconciliation)</option>
              </optgroup>
            </select>
          </div>

          <!-- Select Target Data Scope (ABAC parameter) -->
          <div>
            <label class="text-[11px] font-bold text-gray-400 block mb-1.5">النطاق الجغرافي / الإداري المطلوب للفحص</label>
            <select
              v-model="targetScopeUnit"
              class="w-full text-xs px-3 py-2.5 rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 text-right cursor-pointer"
            >
              <option value="1">إدارة أمن محافظة عدن (رئيسي)</option>
              <option value="2">إدارة أمن محافظة لحج</option>
              <option value="3">إدارة أمن محافظة تعز</option>
              <option value="4">إدارة أمن محافظة حضرموت</option>
              <option value="5">ديوان الوزارة العام (مركزي)</option>
            </select>
          </div>

          <!-- Extra Context Toggles -->
          <div class="space-y-2 pt-2 border-t border-gray-100 dark:border-gray-800">
            <label class="text-[11px] font-bold text-gray-400 block">سياق الطلب الإضافي</label>
            
            <label class="flex items-center gap-2 text-xs text-gray-600 dark:text-gray-300 cursor-pointer">
              <input type="checkbox" v-model="context.outsideWorkingHours" class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" />
              <span>الطلب خارج أوقات العمل الرسمية</span>
            </label>

            <label class="flex items-center gap-2 text-xs text-gray-600 dark:text-gray-300 cursor-pointer">
              <input type="checkbox" v-model="context.isTrustedIP" class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" />
              <span>الاتصال من شبكة داخلية موثوقة</span>
            </label>
          </div>

          <button
            @click="runSimulation"
            :disabled="!selectedUserId || !targetPermission"
            class="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-extrabold text-xs shadow-md shadow-indigo-500/10 transition-all cursor-pointer mt-2"
          >
            تشغيل محاكاة السياسة الأمنية
          </button>
        </div>

        <!-- Simulation Result Dashboard (2/3 width) -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Simulation Status Alert -->
          <div 
            v-if="simulationRan"
            class="rounded-2xl p-5 border shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4"
            :class="[
              result.allowed ? 'bg-emerald-500/5 border-emerald-200 dark:border-emerald-850' : 'bg-red-500/5 border-red-200 dark:border-red-850'
            ]"
          >
            <div>
              <h4 class="text-sm font-black flex items-center gap-2" :class="[result.allowed ? 'text-emerald-800 dark:text-emerald-400' : 'text-red-800 dark:text-red-400']">
                <svg v-if="result.allowed" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
                <span>{{ result.allowed ? 'مسموح بالوصول (ACCESS GRANTED)' : 'مرفوض أمنياً (ACCESS DENIED)' }}</span>
              </h4>
              <p class="text-xs text-gray-500 mt-1.5 leading-relaxed">
                {{ result.summary }}
              </p>
            </div>

            <div 
              class="px-4 py-2.5 rounded-2xl text-center font-black text-sm uppercase select-none shrink-0"
              :class="[result.allowed ? 'bg-emerald-500/10 text-emerald-600' : 'bg-red-500/10 text-red-600']"
            >
              {{ result.allowed ? 'مصرح به' : 'حظر وصول' }}
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="text-center py-20 border border-dashed border-gray-200 dark:border-gray-800 rounded-2xl bg-white dark:bg-gray-900">
            <span class="p-3 rounded-2xl bg-gray-50 dark:bg-gray-950 text-gray-400 inline-block mb-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </span>
            <h4 class="text-xs font-bold text-gray-500 dark:text-gray-400 mb-1">في انتظار تهيئة الطلب</h4>
            <p class="text-[10px] text-gray-400 max-w-sm mx-auto">
              قم باختيار أحد حسابات المستخدمين وتحديد الإجراء أو الصلاحية واضغط على تشغيل المحاكاة لعرض خريطة الفحص الأمني.
            </p>
          </div>

          <!-- Simulation Flow Steps -->
          <div v-if="simulationRan" class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5 shadow-sm">
            <h3 class="text-sm font-black text-gray-900 dark:text-white mb-6 border-b border-gray-100 dark:border-gray-800 pb-3">
              تتبع خطوات محرك السياسات والصلاحيات (Evaluation Trace)
            </h3>

            <div class="space-y-6 relative border-r-2 border-gray-100 dark:border-gray-800 pr-5 mr-3">
              <!-- Step 1: Authentication status -->
              <div class="relative">
                <!-- Dot marker -->
                <span class="absolute -right-[27px] top-0.5 w-3.5 h-3.5 rounded-full border-2 border-white dark:border-gray-900"
                  :class="result.trace.accountCheck.passed ? 'bg-emerald-500' : 'bg-red-500'"
                ></span>
                <div>
                  <h4 class="text-xs font-black text-gray-900 dark:text-white flex items-center gap-1.5">
                    <span>الخطوة 1: فحص حالة وصلاحية الحساب</span>
                    <span class="text-[9px] font-bold px-1.5 py-0.2 rounded" :class="result.trace.accountCheck.passed ? 'bg-emerald-50 bg-emerald-500/10 text-emerald-600' : 'bg-red-50 bg-red-500/10 text-red-600'">
                      {{ result.trace.accountCheck.passed ? 'مكتمل' : 'فشل' }}
                    </span>
                  </h4>
                  <p class="text-[10px] text-gray-500 mt-1 leading-relaxed">
                    {{ result.trace.accountCheck.message }}
                  </p>
                </div>
              </div>

              <!-- Step 2: RBAC permissions list -->
              <div class="relative">
                <span class="absolute -right-[27px] top-0.5 w-3.5 h-3.5 rounded-full border-2 border-white dark:border-gray-900"
                  :class="result.trace.rbacCheck.passed ? 'bg-emerald-500' : 'bg-red-500'"
                ></span>
                <div>
                  <h4 class="text-xs font-black text-gray-900 dark:text-white flex items-center gap-1.5">
                    <span>الخطوة 2: فحص الصلاحيات المكتسبة (RBAC)</span>
                    <span class="text-[9px] font-bold px-1.5 py-0.2 rounded" :class="result.trace.rbacCheck.passed ? 'bg-emerald-50 bg-emerald-500/10 text-emerald-600' : 'bg-red-50 bg-red-500/10 text-red-600'">
                      {{ result.trace.rbacCheck.passed ? 'مكتمل' : 'فشل' }}
                    </span>
                  </h4>
                  <p class="text-[10px] text-gray-500 mt-1 leading-relaxed">
                    {{ result.trace.rbacCheck.message }}
                  </p>
                  <!-- Roles badges -->
                  <div class="flex flex-wrap gap-1.5 mt-2">
                    <span v-for="role in result.trace.rbacCheck.roles" :key="role" class="px-2 py-0.5 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded text-[9px] font-bold">
                      الدور: {{ role }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Step 3: ABAC Data Scope matching -->
              <div class="relative">
                <span class="absolute -right-[27px] top-0.5 w-3.5 h-3.5 rounded-full border-2 border-white dark:border-gray-900"
                  :class="result.trace.abacCheck.passed ? 'bg-emerald-500' : 'bg-red-500'"
                ></span>
                <div>
                  <h4 class="text-xs font-black text-gray-900 dark:text-white flex items-center gap-1.5">
                    <span>الخطوة 3: مطابقة نطاق البيانات الجغرافي والوحدة الإدارية (ABAC)</span>
                    <span class="text-[9px] font-bold px-1.5 py-0.2 rounded" :class="result.trace.abacCheck.passed ? 'bg-emerald-50 bg-emerald-500/10 text-emerald-600' : 'bg-red-50 bg-red-500/10 text-red-600'">
                      {{ result.trace.abacCheck.passed ? 'مكتمل' : 'فشل' }}
                    </span>
                  </h4>
                  <p class="text-[10px] text-gray-500 mt-1 leading-relaxed">
                    {{ result.trace.abacCheck.message }}
                  </p>
                </div>
              </div>

              <!-- Step 4: Context conditions (time, IP, device) -->
              <div class="relative">
                <span class="absolute -right-[27px] top-0.5 w-3.5 h-3.5 rounded-full border-2 border-white dark:border-gray-900"
                  :class="result.trace.contextCheck.passed ? 'bg-emerald-500' : 'bg-red-500'"
                ></span>
                <div>
                  <h4 class="text-xs font-black text-gray-900 dark:text-white flex items-center gap-1.5">
                    <span>الخطوة 4: التحقق من شروط البيئة المحيطة (Context Rules)</span>
                    <span class="text-[9px] font-bold px-1.5 py-0.2 rounded" :class="result.trace.contextCheck.passed ? 'bg-emerald-50 bg-emerald-500/10 text-emerald-600' : 'bg-red-50 bg-red-500/10 text-red-600'">
                      {{ result.trace.contextCheck.passed ? 'مقبول' : 'فشل' }}
                    </span>
                  </h4>
                  <p class="text-[10px] text-gray-500 mt-1 leading-relaxed">
                    {{ result.trace.contextCheck.message }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import api from '@/lib/api'

interface UserRecord {
  id: number
  username: string
  full_name: string
  is_active: boolean
  role: { id: number; name: string; code: string } | null
}

const selectedUserId = ref<number | string>('')
const targetPermission = ref('')
const targetScopeUnit = ref('1')
const context = ref({
  outsideWorkingHours: false,
  isTrustedIP: true,
})

const users = ref<UserRecord[]>([])
const selectedUserDetail = ref<any>(null)
const simulationRan = ref(false)

// Result state
const result = ref({
  allowed: false,
  summary: '',
  trace: {
    accountCheck: { passed: false, message: '' },
    rbacCheck: { passed: false, message: '', roles: [] as string[] },
    abacCheck: { passed: false, message: '' },
    contextCheck: { passed: false, message: '' }
  }
})

async function loadUsers() {
  try {
    const res = await api.get('/users/', { params: { page_size: 100 } })
    users.value = res.data.results || []
  } catch (err) {
    console.error('Failed to load users for simulation:', err)
  }
}

async function handleUserChange() {
  if (!selectedUserId.value) return
  try {
    const res = await api.get(`/users/${selectedUserId.value}/`)
    selectedUserDetail.value = res.data.data || null
  } catch (err) {
    console.error('Failed to fetch target user detail:', err)
  }
}

function runSimulation() {
  if (!selectedUserId.value || !targetPermission.value) return

  const user = users.value.find(u => u.id === selectedUserId.value)
  if (!user) return

  // Mock-simulate permissions check matching Django's core policy rules
  const userRoleCode = user.role?.code || 'regular'
  const userRoleName = user.role?.name || 'مستخدم عادي'

  const isSuperuser = user.username === 'admin' || user.username === 'root'
  const isSuspended = !user.is_active

  // 1. Account Check
  const accountPassed = !isSuspended
  const accountMessage = isSuspended 
    ? '⚠️ الحساب معطل (Disabled) من قبل مدير النظام. يتم حظر كافة الطلبات فوراً.'
    : '✅ الحساب نشط وجلسة العمل موثقة عبر النظام.'

  // 2. RBAC check
  let rbacPassed = false
  let rbacMessage = ''
  
  if (isSuperuser) {
    rbacPassed = true
    rbacMessage = '👑 المستخدم يمتلك صلاحيات مدير عام النظام المطلق (Superuser). تخطي فحص RBAC والموافقة فوراً.'
  } else {
    // Check permission rules matching role codes
    if (targetPermission.value.startsWith('users.')) {
      // requires admin
      rbacPassed = userRoleCode === 'admin'
    } else if (targetPermission.value.startsWith('roles.')) {
      // requires admin
      rbacPassed = userRoleCode === 'admin'
    } else if (targetPermission.value.startsWith('personnel.view')) {
      rbacPassed = ['admin', 'personnel_manager', 'data_entry'].includes(userRoleCode)
    } else if (targetPermission.value.startsWith('personnel.create') || targetPermission.value.startsWith('personnel.edit')) {
      rbacPassed = ['admin', 'personnel_manager', 'data_entry'].includes(userRoleCode)
    } else if (targetPermission.value.startsWith('services.')) {
      rbacPassed = ['admin', 'services_officer', 'reconciliation_manager'].includes(userRoleCode)
    }

    rbacMessage = rbacPassed
      ? `✅ الإجراء [${targetPermission.value}] مسموح للمجموعة الوظيفية للمستخدم.`
      : `❌ المجموعة الوظيفية للمستخدم [${userRoleName}] لا تحتوي على الصلاحية المطلوب فحصها.`
  }

  // 3. ABAC Data Scope Check
  let abacPassed = false
  let abacMessage = ''

  if (isSuperuser) {
    abacPassed = true
    abacMessage = '✅ لا توجد قيود نطاق بيانات للـ Superuser (عرض كافة المحافظات والقطاعات).'
  } else {
    // Simulate geographic scopes: admin/data_entry has scope
    if (userRoleCode === 'admin') {
      abacPassed = true
      abacMessage = '✅ الحساب يمتلك صلاحيات إدارية عامة تغطي كافة القطاعات الإدارية.'
    } else {
      // Mock scope check (data_entry only allowed in unit "1" - Aden security admin)
      if (targetScopeUnit.value === '1') {
        abacPassed = true
        abacMessage = `✅ النطاق المطلوب [إدارة أمن عدن] متوافق مع الحدود الجغرافية الممنوحة للمستخدم في الهيكل التنظيمي.`
      } else {
        abacPassed = false
        abacMessage = `❌ تم رفض الطلب: نطاق عمل الحساب مقتصر على [إدارة أمن عدن] فقط، ولا يملك الصلاحية للوصول لبيانات الوحدة رقم ${targetScopeUnit.value}.`
      }
    }
  }

  // 4. Context conditions check
  let contextPassed = true
  let contextMessage = '✅ الظروف البيئية للطلب مطابقة للمعايير القياسية.'

  if (context.value.outsideWorkingHours && userRoleCode !== 'admin') {
    // If outside working hours and not admin, trigger a warning or rejection based on trusted IP
    if (!context.value.isTrustedIP) {
      contextPassed = false
      contextMessage = '❌ تم الرفض: محاولة الوصول خارج أوقات العمل ومن عنوان IP غير موثوق.'
    } else {
      contextMessage = '⚠️ تحذير: الوصول خارج أوقات العمل الرسمية ولكن تم السماح به نظراً للاتصال من IP داخلي موثوق.'
    }
  } else if (!context.value.isTrustedIP) {
    contextMessage = '⚠️ تنبيه: الطلب تم من شبكة خارجية (مراقب أمنياً).'
  }

  // Overall allowance calculation
  const overallAllowed = accountPassed && rbacPassed && abacPassed && contextPassed

  result.value = {
    allowed: overallAllowed,
    summary: overallAllowed
      ? `تم السماح بالوصول بنجاح. حساب المستخدم يطابق السياسات الأمنية المطلوبة للقيام بالعملية [${targetPermission.value}] تحت النطاق التنظيمي المحدد.`
      : `تم حظر الوصول لعدم استيفاء شروط الأمان. يرجى مراجعة تفاصيل التتبع أدناه لمعرفة موطن الخلل.`,
    trace: {
      accountCheck: { passed: accountPassed, message: accountMessage },
      rbacCheck: { 
        passed: rbacPassed, 
        message: rbacMessage, 
        roles: [userRoleName] 
      },
      abacCheck: { passed: abacPassed, message: abacMessage },
      contextCheck: { passed: contextPassed, message: contextMessage }
    }
  }

  simulationRan.value = true
}

onMounted(() => {
  loadUsers()
})
</script>
