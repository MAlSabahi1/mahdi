<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="تفويض الصلاحيات والوصول الطارئ" />

    <div class="space-y-6 text-start animate-fade-in" dir="rtl">
      
      <!-- Premium Header Card -->
      <div class="relative overflow-hidden rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-sm">
        <div class="absolute -right-16 -top-16 w-48 h-48 bg-brand-500/5 rounded-full blur-3xl pointer-events-none"></div>
        
        <div class="relative flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-brand-500/10 text-brand-600 dark:text-brand-400 rounded-2xl shadow-theme-xs">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-black text-gray-900 dark:text-white">
                تفويض الصلاحيات والوصول الطارئ (Break-Glass)
              </h1>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                حوكمة وإدارة تكليف الصلاحيات المؤقتة بين الضباط وتفعيل بروتوكولات التجاوز الاستثنائي لقيود النطاق الجغرافي عند الطوارئ.
              </p>
            </div>
          </div>

          <!-- Tab Switcher -->
          <div class="inline-flex p-1 bg-gray-100 dark:bg-gray-800/80 rounded-xl border border-gray-200/40 dark:border-gray-700/30">
            <button 
              @click="activeTab = 'delegation'"
              class="px-4 py-2 text-xs font-black rounded-lg transition-all cursor-pointer inline-flex items-center gap-2"
              :class="[activeTab === 'delegation' ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-theme-xs' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400']"
            >
              تفويض الصلاحيات المؤقتة
            </button>
            <button 
              @click="activeTab = 'break_glass'"
              class="px-4 py-2 text-xs font-black rounded-lg transition-all cursor-pointer inline-flex items-center gap-2"
              :class="[activeTab === 'break_glass' ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-theme-xs' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400']"
            >
              الوصول الاستثنائي الطارئ
            </button>
          </div>
        </div>
      </div>

      <!-- Tab 1: Temporary Delegation -->
      <div v-show="activeTab === 'delegation'" class="space-y-4">
        <!-- Main Actions Bar -->
        <div class="flex justify-between items-center bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-4 shadow-sm">
          <div class="text-xs text-gray-500 dark:text-gray-400 font-bold">
            مجموع التراخيص المصدرة: {{ delegations.length }}
          </div>
          <button 
            @click="showCreateModal = true"
            class="inline-flex items-center gap-2 rounded-lg bg-brand-500 px-4 py-2 text-xs font-black text-white shadow-theme-xs hover:bg-brand-600 transition-colors cursor-pointer"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
            </svg>
            إصدار تفويض مؤقت جديد
          </button>
        </div>

        <!-- Full Width Grid Table for Active Delegations -->
        <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-gray-150 dark:border-gray-800 pb-3">
            <h3 class="text-sm font-black text-gray-900 dark:text-white">سجل التراخيص والتفويضات النشطة</h3>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-right border-collapse min-w-[1000px]">
              <thead>
                <tr class="border-b border-gray-100 dark:border-gray-800 text-xs font-bold text-gray-400 bg-gray-50/50 dark:bg-gray-900/50">
                  <th class="p-3 text-start">الضابط المفوض (المنشِئ)</th>
                  <th class="p-3">الضابط المفوض له (المستفيد)</th>
                  <th class="p-3">حزمة الصلاحيات والمستوى المعين</th>
                  <th class="p-3">رقم الأمر الإداري</th>
                  <th class="p-3">تاريخ الصلاحية</th>
                  <th class="p-3">المبرر وسياق التفويض</th>
                  <th class="p-3 text-left">الحالة والتحكم</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 dark:divide-gray-850">
                <tr v-if="delegations.length === 0">
                  <td colspan="7" class="p-8 text-center text-gray-400">
                    لا توجد سجلات تفويض نشطة حالياً.
                  </td>
                </tr>
                <tr 
                  v-for="del in delegations" 
                  :key="del.id" 
                  class="text-xs hover:bg-gray-50/40 dark:hover:bg-gray-850/20 transition-colors"
                >
                  <td class="p-3">
                    <span class="font-extrabold text-gray-900 dark:text-white block">{{ del.delegator_name }}</span>
                    <span class="text-[10px] text-gray-400 font-mono block">@{{ del.delegator }}</span>
                  </td>
                  <td class="p-3">
                    <span class="font-extrabold text-gray-900 dark:text-white block">{{ del.delegatee_name }}</span>
                    <span class="text-[10px] text-gray-400 font-mono block">@{{ del.delegatee }}</span>
                  </td>
                  <td class="p-3">
                    <span class="font-bold text-gray-800 dark:text-gray-250 block">{{ getPackageLabel(del.package_code) }}</span>
                    <span class="px-1.5 py-0.5 rounded text-[8px] font-mono bg-brand-50 text-brand-600 dark:bg-brand-950/20 dark:text-brand-400 border border-brand-200/30">
                      {{ del.package_code }}
                    </span>
                  </td>
                  <td class="p-3 font-mono font-bold text-gray-700 dark:text-gray-300">
                    {{ del.official_order }}
                  </td>
                  <td class="p-3 font-mono text-[10px]">
                    <span class="text-emerald-600 dark:text-emerald-450 block">البدء: {{ del.startDate }}</span>
                    <span class="text-red-500 block">الانتهاء: {{ del.endDate }}</span>
                  </td>
                  <td class="p-3 max-w-[200px] truncate" :title="del.reason">
                    <span class="text-gray-550 dark:text-gray-400">{{ del.reason }}</span>
                  </td>
                  <td class="p-3 text-left">
                    <div class="flex items-center justify-end gap-2">
                      <span 
                        class="px-2 py-0.5 rounded-full font-bold text-[9px] border"
                        :class="[
                          del.status === 'active' ? 'bg-success-50 text-success-700 border-success-200 dark:bg-success-950/20 dark:text-success-400' : 'bg-gray-100 text-gray-500 border-gray-200 dark:bg-gray-800 dark:text-gray-400'
                        ]"
                      >
                        {{ del.status === 'active' ? 'نشط' : 'ملغى' }}
                      </span>
                      <button
                        v-if="del.status === 'active'"
                        @click="revokeDelegation(del.id)"
                        class="text-[9px] font-black text-red-650 bg-red-50 hover:bg-red-100 dark:bg-red-950/20 dark:hover:bg-red-950/40 border border-red-200/30 px-2 py-1 rounded-lg transition-all cursor-pointer"
                      >
                        سحب
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Tab 2: Break Glass Override -->
      <div v-show="activeTab === 'break_glass'" class="space-y-6">
        
        <div class="grid gap-6 lg:grid-cols-12">
          <!-- Control Panel & Status -->
          <div class="lg:col-span-8 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-sm space-y-6">
            <div class="flex items-center justify-between border-b border-gray-100 dark:border-gray-800 pb-4">
              <div>
                <h3 class="text-base font-semibold text-gray-900 dark:text-white">لوحة التحكم ببروتوكول التجاوز (Break-Glass Control)</h3>
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">التعطيل الاستثنائي المؤقت لقواعد حظر النطاق الجغرافي (ABAC) في ظروف الكوارث أو انقطاع الربط.</p>
              </div>
            </div>

            <!-- Current State Banner -->
            <div 
              class="rounded-xl border p-5 transition-all duration-300 flex items-center justify-between gap-4"
              :class="[isEmergencyActive ? 'bg-red-500/10 border-red-500 text-red-900 dark:text-red-400' : 'bg-emerald-500/5 border-emerald-500/30 text-emerald-900 dark:text-emerald-450']"
            >
              <div class="flex items-center gap-4">
                <div 
                  class="p-3 rounded-xl"
                  :class="[isEmergencyActive ? 'bg-red-600 text-white animate-pulse' : 'bg-emerald-600 text-white']"
                >
                  <svg v-if="isEmergencyActive" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.75c0 5.592 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.57-.598-3.75h-.152c-3.196 0-6.1-1.249-8.25-3.286zm0 13.036h.008v.008H12v-.008z" />
                  </svg>
                </div>
                <div>
                  <h4 class="font-extrabold text-sm">
                    حالة النظام الحالية: 
                    <span v-if="isEmergencyActive" class="underline decoration-2 text-red-650">وضع الطوارئ وتجاوز ABAC نشط</span>
                    <span v-else>وضع الحماية والـ ABAC مفروض بالكامل</span>
                  </h4>
                  <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-1">
                    {{ isEmergencyActive ? 'تحذير أمني: يسمح النظام الآن بالوصول العابر للمحافظات. كافة الأنشطة تسجل للمساءلة.' : 'جميع عمليات الاستعلام مقيدة بالنطاق الجغرافي المسجل لكل ضابط.' }}
                  </p>
                </div>
              </div>

              <button 
                @click="toggleEmergencyMode"
                class="px-5 py-2.5 rounded-xl text-xs font-black shadow-theme-xs transition-all cursor-pointer"
                :class="[isEmergencyActive ? 'bg-gray-900 text-white hover:bg-black dark:bg-gray-800' : 'bg-red-600 text-white hover:bg-red-700']"
              >
                {{ isEmergencyActive ? 'إلغاء وضع الطوارئ فوراً' : 'بدء طلب تفعيل التجاوز' }}
              </button>
            </div>

            <!-- Activation form if initiating -->
            <div v-if="showBreakGlassForm" class="bg-gray-50/60 dark:bg-gray-950 p-5 rounded-xl border border-gray-200 dark:border-gray-800 space-y-4">
              <h4 class="text-xs font-black text-gray-900 dark:text-white">استمارة طلب المصادقة لتجاوز قيود الـ ABAC</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-[11px] font-bold text-gray-500 dark:text-gray-400 mb-1.5">الجهة/المنطقة العسكرية الطالبة</label>
                  <input 
                    type="text" 
                    v-model="bgAgency" 
                    placeholder="مثال: الإدارة العامة لشؤون المحافظات..."
                    class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2.5 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:outline-none"
                  />
                </div>
                <div>
                  <label class="block text-[11px] font-bold text-gray-500 dark:text-gray-400 mb-1.5">رقم البرقية أو الأمر العملياتي المعتمد</label>
                  <input 
                    type="text" 
                    v-model="bgOrder" 
                    placeholder="مثال: برقية عمليات رقم 482-م..."
                    class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2.5 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:outline-none"
                  />
                </div>
                <div>
                  <label class="block text-[11px] font-bold text-gray-500 dark:text-gray-400 mb-1.5">المدة الزمنية المطلوبة للتجاوز</label>
                  <select 
                    v-model="bgDuration" 
                    class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2.5 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:outline-none"
                  >
                    <option value="2">ساعتان (2h)</option>
                    <option value="4">4 ساعات (4h)</option>
                    <option value="8">8 ساعات (8h)</option>
                    <option value="12">12 ساعة (طوارئ قصوى)</option>
                  </select>
                </div>
                <div>
                  <label class="block text-[11px] font-bold text-gray-500 dark:text-gray-400 mb-1.5">المشرف الأمني المصدق الثاني (Four-Eyes Checker)</label>
                  <select 
                    v-model="bgChecker" 
                    class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2.5 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:outline-none"
                  >
                    <option value="">اختر المشرف المصدق...</option>
                    <option v-for="u in users" :key="u.id" :value="u.username">
                      {{ u.full_name || u.username }} (مسؤول أمن نظام)
                    </option>
                  </select>
                </div>
                <div class="md:col-span-2">
                  <label class="block text-[11px] font-bold text-gray-500 dark:text-gray-400 mb-1.5">مبرر وسياق التفعيل الطارئ بالتفصيل</label>
                  <textarea 
                    v-model="bgReason" 
                    placeholder="اكتب بالتفصيل سبب تجاوز القيود الجغرافية..."
                    rows="2"
                    class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2.5 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:outline-none"
                  ></textarea>
                </div>
              </div>
              
              <div class="flex justify-end gap-2">
                <button 
                  @click="showBreakGlassForm = false"
                  class="px-4 py-2 border border-gray-200 dark:border-gray-800 text-xs rounded-xl hover:bg-gray-50"
                >
                  إلغاء
                </button>
                <button 
                  @click="submitBreakGlassRequest"
                  class="px-4 py-2 bg-red-600 text-white text-xs font-bold rounded-xl hover:bg-red-700"
                >
                  إرسال للتحقق الثنائي وتفعيل التجاوز
                </button>
              </div>
            </div>
          </div>

          <!-- Strict Safeguards Checklist -->
          <div class="lg:col-span-4 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-sm space-y-4">
            <h3 class="text-xs font-bold text-gray-900 dark:text-white pb-3 border-b border-gray-150 dark:border-gray-800">
              الضوابط الأمنية لمنع التلاعب والتسريب
            </h3>
            
            <div class="space-y-3.5">
              <div class="flex items-start gap-2.5 text-[10px] text-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4.5 w-4.5 text-emerald-500 shrink-0 mt-0.5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
                <div>
                  <span class="font-bold text-gray-800 dark:text-white block">مصادقة المسؤول الأمني الثاني</span>
                  لا يمكن تفعيل التجاوز من طرف واحد أبداً؛ بل يجب توقيع مسؤول الأمن الثاني في النظام فوراً لمنع الخيانة.
                </div>
              </div>
              
              <div class="flex items-start gap-2.5 text-[10px] text-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4.5 w-4.5 text-emerald-500 shrink-0 mt-0.5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
                <div>
                  <span class="font-bold text-gray-800 dark:text-white block">الإيقاف التلقائي</span>
                  ينتهي وضع التجاوز تلقائياً فور انتهاء المدة المحددة لمنع الاستغلال الدائم أو النسيان.
                </div>
              </div>

              <div class="flex items-start gap-2.5 text-[10px] text-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4.5 w-4.5 text-amber-500 shrink-0 mt-0.5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zm-1 9a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
                </svg>
                <div>
                  <span class="font-bold text-gray-800 dark:text-white block">حظر تحميل وتصدير البيانات بالكامل</span>
                  أثناء تفعيل وضع الطوارئ، يمنع النظام تلقائياً أي عمليات تصدير (Excel/PDF) للقوة العسكرية لحين عودة وضع الحماية.
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Audit log of Emergency activates -->
        <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl shadow-sm overflow-hidden">
          <div class="p-5 border-b border-gray-150 dark:border-gray-800">
            <h3 class="text-sm font-black text-gray-900 dark:text-white">أرشيف تفعيل بروتوكول التجاوز (Break-Glass Audit Trail)</h3>
            <p class="text-[11px] text-gray-400 dark:text-gray-500 mt-0.5">توثيق العمليات الاستثنائية وتفاصيل الموافقين وتبريرات الإدارة المدخلة.</p>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-right border-collapse min-w-[1000px]">
              <thead>
                <tr class="border-b border-gray-100 dark:border-gray-800 text-xs font-bold text-gray-400 bg-gray-50/50 dark:bg-gray-900/50">
                  <th class="p-3 text-start">المستخدم الفاعل</th>
                  <th class="p-3">الجهة والمنطقة العسكرية</th>
                  <th class="p-3">رقم برقية العمليات</th>
                  <th class="p-3">المصادق المعتمد الثاني</th>
                  <th class="p-3">مدة وساعة التفعيل</th>
                  <th class="p-3">المبرر وسياق الطوارئ</th>
                  <th class="p-3 text-left">الحالة</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 dark:divide-gray-855">
                <tr v-if="breakGlassLogs.length === 0">
                  <td colspan="7" class="p-8 text-center text-gray-400">
                    لا توجد سجلات تفعيل لوضع التجاوز حالياً.
                  </td>
                </tr>
                <tr 
                  v-for="log in breakGlassLogs" 
                  :key="log.id" 
                  class="text-xs hover:bg-gray-50/40 dark:hover:bg-gray-850/20 transition-colors"
                >
                  <td class="p-3">
                    <span class="font-extrabold text-gray-900 dark:text-white block">{{ log.username }}</span>
                    <span class="text-[10px] text-gray-400 font-mono block">IP: {{ log.ip_address }}</span>
                  </td>
                  <td class="p-3 font-semibold text-gray-700 dark:text-gray-300">
                    {{ log.scope }}
                  </td>
                  <td class="p-3 font-mono font-bold text-gray-850 dark:text-gray-250">
                    {{ log.order_num }}
                  </td>
                  <td class="p-3 font-extrabold text-gray-800 dark:text-gray-300">
                    {{ log.approver || '—' }}
                  </td>
                  <td class="p-3 font-mono text-[10px]">
                    <span class="block text-gray-800 dark:text-gray-250">البدء: {{ log.timestamp }}</span>
                    <span class="block text-red-500 font-bold">المدة: {{ log.duration_hours }} ساعات</span>
                  </td>
                  <td class="p-3 max-w-xs truncate" :title="log.reason">
                    <span class="text-gray-600 dark:text-gray-400 italic">{{ log.reason }}</span>
                  </td>
                  <td class="p-3 text-left">
                    <span 
                      class="px-2 py-0.5 rounded-full font-bold text-[9px] border inline-flex items-center gap-1"
                      :class="[
                        log.status === 'active' ? 'bg-error-50 text-error-700 border-error-200 dark:bg-error-950/20 dark:text-error-400' : 'bg-gray-100 text-gray-500 border-gray-200 dark:bg-gray-800 dark:text-gray-400'
                      ]"
                    >
                      <span class="h-1 w-1 rounded-full" :class="log.status === 'active' ? 'bg-red-500 animate-pulse' : 'bg-gray-450'"></span>
                      {{ log.status === 'active' ? 'نشط (تجاوز)' : 'منتهي' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>

    </div>

    <!-- Issue Temporary Delegation Modal -->
    <div 
      v-if="showCreateModal"
      class="fixed inset-0 bg-gray-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-[9999] animate-fade-in"
      dir="rtl"
    >
      <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-850 rounded-2xl max-w-xl w-full flex flex-col overflow-hidden shadow-2xl">
        <!-- Modal Header -->
        <div class="p-4 bg-gray-50 dark:bg-gray-950 border-b border-gray-200 dark:border-gray-850 flex justify-between items-center">
          <div>
            <h3 class="text-sm font-black text-gray-900 dark:text-white">إصدار ترخيص تفويض مؤقت جديد</h3>
            <p class="text-[10px] text-gray-400 dark:text-gray-500 mt-0.5">تكليف ضابط آخر بمستوى صلاحيات محددة لفترة محددة.</p>
          </div>
          <button 
            @click="showCreateModal = false"
            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 p-1.5 rounded-lg hover:bg-gray-200/50 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Modal Body -->
        <div class="p-6 space-y-4 text-right">
          <div class="grid grid-cols-1 gap-4">
            <!-- Select user -->
            <div>
              <label class="block text-[11px] font-bold text-gray-500 dark:text-gray-400 mb-1.5">الضابط المفوض له (المستفيد)</label>
              <select 
                v-model="delegatedUser" 
                class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2.5 bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500"
              >
                <option value="">اختر الضابط...</option>
                <option v-for="u in users" :key="u.id" :value="u.username">
                  {{ u.full_name || u.username }} ({{ u.username }})
                </option>
              </select>
            </div>

            <!-- Logical Delegation Packages -->
            <div>
              <label class="block text-[11px] font-bold text-gray-500 dark:text-gray-400 mb-1.5">نوع حزمة الصلاحيات المفوضة</label>
              <select 
                v-model="permissionPackage" 
                class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2.5 bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500"
              >
                <option value="">اختر حزمة الصلاحيات...</option>
                <option v-for="pkg in delegationPackages" :key="pkg.code" :value="pkg.code">
                  {{ pkg.name }} ({{ pkg.description }})
                </option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-[11px] font-bold text-gray-500 dark:text-gray-400 mb-1.5">تاريخ بدء التفويض</label>
                <input 
                  type="date" 
                  v-model="startDate" 
                  class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2.5 bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none"
                />
              </div>
              <div>
                <label class="block text-[11px] font-bold text-gray-500 dark:text-gray-400 mb-1.5">تاريخ انتهاء التفويض</label>
                <input 
                  type="date" 
                  v-model="endDate" 
                  class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2.5 bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label class="block text-[11px] font-bold text-gray-500 dark:text-gray-400 mb-1.5">رقم الأمر الإداري / المذكرة الرسمية</label>
              <input 
                type="text" 
                v-model="officialOrder" 
                placeholder="مثال: أمر إداري رقم 244 لعام 2026..."
                class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2.5 bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none"
              />
            </div>

            <div>
              <label class="block text-[11px] font-bold text-gray-500 dark:text-gray-400 mb-1.5">المبرر وسياق التفويض</label>
              <textarea 
                v-model="reason" 
                placeholder="اكتب مبرر إصدار هذا التكليف أو التفويض المؤقت للعمل..." 
                rows="2" 
                class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2.5 bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 focus:outline-none"
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="p-4 bg-gray-50 dark:bg-gray-950 border-t border-gray-200 dark:border-gray-850 flex justify-end gap-2">
          <button 
            @click="showCreateModal = false"
            class="px-4 py-2 border border-gray-200 dark:border-gray-800 text-xs rounded-xl hover:bg-gray-50 cursor-pointer"
          >
            إلغاء
          </button>
          <button 
            @click="handleCreateDelegation"
            class="px-5 py-2 bg-brand-500 hover:bg-brand-600 text-white text-xs font-black rounded-xl cursor-pointer"
          >
            حفظ وإصدار الترخيص
          </button>
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
import Swal from 'sweetalert2'

interface UserRecord {
  id: number
  username: string
  full_name: string
}

interface Delegation {
  id: number
  delegator: string
  delegator_name: string
  delegatee: string
  delegatee_name: string
  package_code: string
  official_order: string
  startDate: string
  endDate: string
  reason: string
  status: 'active' | 'revoked'
}

interface BreakGlassLog {
  id: number
  username: string
  ip_address: string
  scope: string
  order_num: string
  approver: string
  duration_hours: number
  timestamp: string
  reason: string
  status: 'active' | 'expired'
}

const activeTab = ref('delegation')
const showCreateModal = ref(false)
const showBreakGlassForm = ref(false)
const users = ref<UserRecord[]>([])
const loadingUsers = ref(false)

// Active Override Status
const isEmergencyActive = ref(false)

// Form fields for Delegation
const delegatedUser = ref('')
const permissionPackage = ref('')
const officialOrder = ref('')
const startDate = ref('')
const endDate = ref('')
const reason = ref('')

// Form fields for Break-Glass Override
const bgAgency = ref('')
const bgOrder = ref('')
const bgDuration = ref('4')
const bgChecker = ref('')
const bgReason = ref('')

// Logical Delegation Packages Definition
const delegationPackages = [
  { code: 'READONLY_AUDIT', name: 'حزمة القراءة والاستعلام فقط', description: 'عرض الأفراد والتقارير العامة وسجلات الخدمة دون القدرة على التعديل أو الحذف.' },
  { code: 'LIMITED_ENTRY', name: 'حزمة الإدخال والتحرير المحدود', description: 'إضافة وتعديل بيانات الأفراد الاعتيادية مع حظر حذف السجلات أو اعتماد التعديلات الحساسة.' },
  { code: 'FINANCE_ADMIN', name: 'حزمة إدارة الموارد المالية والرواتب', description: 'تعديل حقول البدلات والرواتب وتفاصيل البطاقات البنكية للمستفيدين (خاضع للاعتماد المزدوج).' },
  { code: 'FULL_PROXY', name: 'تكليف كامل بالنيابة عن المفوض', description: 'تفويض كامل للصلاحيات النشطة للضابط المنشئ للمستفيد خلال فترة غيابه الرسمية.' }
]

function getPackageLabel(code: string): string {
  const pkg = delegationPackages.find(p => p.code === code)
  return pkg ? pkg.name : code
}

// Mock High Fidelity list for Delegations
const delegations = ref<Delegation[]>([
  {
    id: 1,
    delegator: 'admin',
    delegator_name: 'مدير عام النظام',
    delegatee: 'ali_ahmad',
    delegatee_name: 'الرائد علي أحمد',
    package_code: 'LIMITED_ENTRY',
    official_order: 'أمر إداري رقم 44/2026',
    startDate: '2026-07-04',
    endDate: '2026-07-10',
    reason: 'أمر تكليف رسمي لتغطية عجز الإدخال خلال فترة حصر دفعات التجنيد.',
    status: 'active'
  },
  {
    id: 2,
    delegator: 'admin',
    delegator_name: 'مدير عام النظام',
    delegatee: 'salah_ali',
    delegatee_name: 'العقيد صلاح علي',
    package_code: 'FULL_PROXY',
    official_order: 'قرار تكليف رقم 12/2026',
    startDate: '2026-06-25',
    endDate: '2026-06-30',
    reason: 'تفويض كامل الصلاحيات بالنيابة بسبب السفر في مهمة عمل خارجية لمحافظة حضرموت.',
    status: 'revoked'
  }
])

const breakGlassLogs = ref<BreakGlassLog[]>([
  {
    id: 101,
    username: 'salem_hassan',
    ip_address: '10.140.22.45',
    scope: 'شؤون الأفراد - أمن عدن',
    order_num: 'برقية طوارئ رقم 982-م',
    approver: 'admin_security',
    duration_hours: 4,
    timestamp: '2026-07-01 10:22:15 ص',
    reason: 'انقطاع ربط الألياف الضوئية الإقليمي وحاجة طارئة لمطابقة كشوفات الترقيات للضباط.',
    status: 'expired'
  }
])

async function fetchUsers() {
  loadingUsers.value = true
  try {
    const res = await api.get('/users/', { params: { page_size: 500 } })
    users.value = res.data.results || []
  } catch (err) {
    console.error('Failed to fetch users for delegation:', err)
  } finally {
    loadingUsers.value = false
  }
}

async function toggleEmergencyMode() {
  if (isEmergencyActive.value) {
    const result = await Swal.fire({
      title: 'إلغاء وضع الطوارئ والتجاوز',
      text: 'هل تريد إلغاء بروتوكول التجاوز الاستثنائي وإعادة فرض قيود النطاق الجغرافي والـ ABAC فوراً؟',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'نعم، إلغاء التفعيل',
      cancelButtonText: 'تراجع',
      confirmButtonColor: '#1f2937',
      cancelButtonColor: '#6b7280'
    })
    
    if (result.isConfirmed) {
      isEmergencyActive.value = false
      breakGlassLogs.value.forEach(log => {
        if (log.status === 'active') log.status = 'expired'
      })
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'info',
        title: 'تم إيقاف وضع التجاوز وإعادة فرض الحماية الجغرافية',
        showConfirmButton: false,
        timer: 3000
      })
    }
  } else {
    // Open the creation form
    showBreakGlassForm.value = true
  }
}

async function submitBreakGlassRequest() {
  if (!bgAgency.value || !bgOrder.value || !bgReason.value || !bgChecker.value) {
    Swal.fire('تنبيه أمني', 'يجب تعبئة كافة حقول استمارة الطوارئ وتحديد المسؤول الأمني الثاني للمصادقة.', 'warning')
    return
  }

  const result = await Swal.fire({
    title: 'تأكيد تفعيل بروتوكول التجاوز (Break-Glass)',
    text: `⚠️ سيتم تفعيل وضع الطوارئ والسماح للمستخدم بالوصول خارج النطاق الجغرافي لمدى ${bgDuration.value} ساعات. هل أنت متأكد؟`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'تأكيد التفعيل الثنائي',
    cancelButtonText: 'إلغاء الطلب',
    confirmButtonColor: '#dc2626',
    cancelButtonColor: '#6b7280'
  })

  if (result.isConfirmed) {
    isEmergencyActive.value = true
    showBreakGlassForm.value = false
    
    const newLog: BreakGlassLog = {
      id: Date.now(),
      username: 'admin',
      ip_address: '10.140.10.2',
      scope: bgAgency.value,
      order_num: bgOrder.value,
      approver: bgChecker.value,
      duration_hours: parseInt(bgDuration.value),
      timestamp: new Date().toLocaleString('ar-YE', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      }),
      reason: bgReason.value,
      status: 'active'
    }

    breakGlassLogs.value.unshift(newLog)

    // Clear form inputs
    bgAgency.value = ''
    bgOrder.value = ''
    bgReason.value = ''
    bgChecker.value = ''

    Swal.fire({
      icon: 'warning',
      title: 'وضع التجاوز الاستثنائي نشط',
      text: 'تم تفعيل وضع الطوارئ وتجاوز قيود الـ ABAC. كافة الصلاحيات مفعلة ويحظر تصدير أي بيانات عسكرية.',
      confirmButtonColor: '#dc2626'
    })
  }
}

function handleCreateDelegation() {
  if (!delegatedUser.value || !permissionPackage.value || !startDate.value || !endDate.value || !reason.value || !officialOrder.value) {
    Swal.fire('تنبيه', 'يرجى إكمال كافة حقول استمارة التفويض وتحديد رقم التكليف الإداري.', 'warning')
    return
  }

  const targetUser = users.value.find(u => u.username === delegatedUser.value)
  const delegateeLabel = targetUser ? targetUser.full_name : delegatedUser.value

  const newDelegation: Delegation = {
    id: Date.now(),
    delegator: 'admin',
    delegator_name: 'مدير عام النظام',
    delegatee: delegatedUser.value,
    delegatee_name: delegateeLabel,
    package_code: permissionPackage.value,
    official_order: officialOrder.value,
    startDate: startDate.value,
    endDate: endDate.value,
    reason: reason.value,
    status: 'active'
  }

  delegations.value.unshift(newDelegation)

  // Reset fields
  delegatedUser.value = ''
  permissionPackage.value = ''
  officialOrder.value = ''
  startDate.value = ''
  endDate.value = ''
  reason.value = ''
  showCreateModal.value = false

  Swal.fire({
    toast: true,
    position: 'top-end',
    icon: 'success',
    title: 'تم إصدار وتفعيل قرار التفويض المؤقت بنجاح',
    showConfirmButton: false,
    timer: 3000
  })
}

async function revokeDelegation(id: number) {
  const result = await Swal.fire({
    title: 'إلغاء وسحب التفويض',
    text: 'هل أنت متأكد من إلغاء قرار التفويض وسحب الصلاحيات فوراً؟',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'نعم، إلغاء الآن',
    cancelButtonText: 'تراجع',
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#6b7280'
  })

  if (result.isConfirmed) {
    const del = delegations.value.find(d => d.id === id)
    if (del) {
      del.status = 'revoked'
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'تم إلغاء التفويض وسحب الصلاحية بنجاح',
        showConfirmButton: false,
        timer: 3000
      })
    }
  }
}

onMounted(() => {
  fetchUsers()
})
</script>
