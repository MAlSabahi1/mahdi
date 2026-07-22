<template>
  <admin-layout>
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <Settings class="w-8 h-8 text-brand-600" />
            إدارة وتكوين الخدمات (Services Setup)
          </h1>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            مركز التحكم الشامل لبناء الخدمات، الحقول، مسارات العمل، والشروط.
          </p>
        </div>
        <div class="flex gap-3">
          <button @click="openCreateModal" class="px-4 py-2.5 text-sm font-bold text-white bg-brand-600 rounded-xl hover:bg-brand-700 flex items-center gap-2 shadow-sm shadow-brand-500/20 transition-all">
            <Plus class="w-4 h-4" />
            إنشاء خدمة جديدة
          </button>
        </div>
      </div>

      <!-- Tabs Control Panel -->
      <div class="flex gap-2 p-1.5 bg-gray-100/80 dark:bg-gray-800/80 rounded-xl overflow-x-auto mb-2 border border-gray-200 dark:border-gray-800">
        <button v-for="tab in tabs" :key="tab.id" @click="selectedTab = tab.id" :class="[
          selectedTab === tab.id
            ? 'bg-white dark:bg-gray-700 text-brand-600 dark:text-brand-400 shadow-sm ring-1 ring-gray-900/5 dark:ring-white/10'
            : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-200/50 dark:hover:bg-gray-700/50',
          'px-4 py-2 rounded-lg text-xs font-bold transition-all whitespace-nowrap flex items-center gap-2'
        ]">
          {{ tab.label }}
          <span class="px-2 py-0.5 rounded-md bg-gray-200/50 dark:bg-gray-800 text-[10px]">{{ tab.count }}</span>
        </button>
      </div>

      <!-- Services Table -->
      <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl overflow-hidden shadow-sm">
        <div class="overflow-x-auto">
          <table class="w-full text-sm text-right">
            <thead class="text-xs text-gray-500 bg-gray-50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-800">
              <tr>
                <th class="px-6 py-4 font-bold">الخدمة الأساسية</th>
                <th class="px-6 py-4 font-bold">الفئة</th>
                <th class="px-6 py-4 font-bold">الحالة</th>
                <th class="px-6 py-4 font-bold text-center">الإعدادات والتكوين (Builders)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading" class="border-b border-gray-100 dark:border-gray-800">
                <td colspan="4" class="px-6 py-10 text-center text-gray-400">
                  <Loader2 class="w-6 h-6 animate-spin mx-auto mb-2" />
                  جاري تحميل البيانات...
                </td>
              </tr>
              <tr v-else-if="filteredServices.length === 0" class="border-b border-gray-100 dark:border-gray-800">
                <td colspan="4" class="px-6 py-10 text-center text-gray-400">
                  لا توجد خدمات مضافة حتى الآن في هذا التبويب.
                </td>
              </tr>
              <tr v-else v-for="svc in filteredServices" :key="svc.id" class="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50/50 dark:hover:bg-gray-800/20 transition-colors">
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-gray-50 dark:bg-gray-800 flex items-center justify-center text-gray-500 border border-gray-100 dark:border-gray-700">
                      <FileText class="w-5 h-5" />
                    </div>
                    <div>
                      <div class="font-bold text-gray-900 dark:text-white">{{ svc.name_ar }}</div>
                      <div class="text-[10px] text-gray-500 mt-0.5">{{ svc.code }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <span class="px-2.5 py-1 text-[10px] font-bold rounded-lg bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400">
                    {{ svc.category === 'military' ? 'عسكرية' : svc.category === 'financial' ? 'مالية' : svc.category === 'disciplinary' ? 'انضباط' : 'أخرى' }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span v-if="svc.is_active" class="px-2.5 py-1 text-[10px] font-bold rounded-lg bg-emerald-50 text-emerald-600 dark:bg-emerald-900/20 dark:text-emerald-400">مفعلة</span>
                  <span v-else class="px-2.5 py-1 text-[10px] font-bold rounded-lg bg-gray-50 text-gray-500 dark:bg-gray-800 dark:text-gray-400">غير مفعلة</span>
                </td>
                <td class="px-6 py-4">
                  <div class="flex items-center justify-center gap-2">
                    <button @click="openEditModal(svc)" class="px-3 py-1.5 text-[10px] font-bold text-gray-700 bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 rounded-lg transition-colors border border-gray-200 dark:border-gray-700 flex items-center gap-1" title="تعديل الإعدادات الأساسية">
                      <Settings class="w-3.5 h-3.5" />
                      تعديل الأساسية
                    </button>
                    <button @click="openFieldsModal(svc)" class="px-3 py-1.5 text-[10px] font-bold text-brand-700 bg-brand-50 hover:bg-brand-100 dark:bg-brand-900/20 dark:text-brand-400 dark:hover:bg-brand-900/40 rounded-lg transition-colors border border-brand-200 dark:border-brand-800/50 flex items-center gap-1" title="بناء حقول الاستمارة">
                      <LayoutTemplate class="w-3.5 h-3.5" />
                      إصدارات الحقول
                    </button>
                    <button @click="openWorkflowModal(svc)" class="px-3 py-1.5 text-[10px] font-bold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 dark:bg-indigo-900/20 dark:text-indigo-400 dark:hover:bg-indigo-900/40 rounded-lg transition-colors border border-indigo-200 dark:border-indigo-800/50 flex items-center gap-1" title="تصميم مراحل الاعتماد">
                      <GitMerge class="w-3.5 h-3.5" />
                      مراحل سير العمل
                    </button>
                    <button @click="openPrereqsModal(svc)" class="px-3 py-1.5 text-[10px] font-bold text-rose-700 bg-rose-50 hover:bg-rose-100 dark:bg-rose-900/20 dark:text-rose-400 dark:hover:bg-rose-900/40 rounded-lg transition-colors border border-rose-200 dark:border-rose-800/50 flex items-center gap-1" title="تكوين شروط التقديم">
                      <ShieldCheck class="w-3.5 h-3.5" />
                      شروط الخدمة
                    </button>
                    <button @click="openAttachmentsModal(svc)" class="px-3 py-1.5 text-[10px] font-bold text-amber-700 bg-amber-50 hover:bg-amber-100 dark:bg-amber-900/20 dark:text-amber-400 dark:hover:bg-amber-900/40 rounded-lg transition-colors border border-amber-200 dark:border-amber-800/50 flex items-center gap-1" title="المرفقات الإلزامية">
                      <Paperclip class="w-3.5 h-3.5" />
                      المرفقات
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- 1. Create Basic Service Modal -->
    <div v-if="modals.create" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/50 backdrop-blur-sm">
      <div class="bg-white dark:bg-gray-800 w-full max-w-lg rounded-2xl shadow-xl overflow-hidden animate-fade-in-up">
        <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center bg-gray-50 dark:bg-gray-900/50">
          <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Settings class="w-5 h-5 text-brand-600" />
            بيانات الخدمة الأساسية
          </h3>
          <button @click="modals.create = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <X class="w-5 h-5" />
          </button>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">اسم الخدمة</label>
            <input type="text" v-model="activeService.name_ar" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none" placeholder="مثال: إثبات حالة زواج" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">كود الخدمة (إنجليزي - فريد)</label>
              <input type="text" v-model="activeService.code" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none" placeholder="مثال: SV_MARRIAGE" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">الأيقونة (Lucide)</label>
              <input type="text" v-model="activeService.icon" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none" placeholder="مثال: FileText" />
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">الفئة</label>
              <select v-model="activeService.category" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm outline-none">
                <option value="military">عسكرية (حركات وتعيينات)</option>
                <option value="financial">مالية (رواتب واستقطاعات)</option>
                <option value="disciplinary">انضباطية</option>
                <option value="other">أخرى</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">الإجراء التنفيذي (الأوتوماتيكي)</label>
              <select v-model="activeService.execution_action" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm outline-none">
                <!-- استمارات إثبات الحالة -->
                <option v-if="activeService.service_type === 'form'" value="UPDATE_STATUS">تغيير الحالة (استمارات إثبات الحالة)</option>
                
                <!-- تصحيحات -->
                <option v-if="activeService.service_type === 'correction'" value="CORRECTION_NAME">تصحيح الاسم</option>
                <option v-if="activeService.service_type === 'correction'" value="CORRECTION_MILITARY_NUM">تصحيح الرقم العسكري</option>
                <option v-if="activeService.service_type === 'correction'" value="CORRECTION_NATIONAL_ID">تصحيح الرقم الوطني</option>
                <option v-if="activeService.service_type === 'correction'" value="CORRECTION_LINKED_SWAP">التبديل المترابط للأرقام</option>
                
                <!-- ترقيات وتسويات -->
                <option v-if="activeService.service_type === 'rank_settlement'" value="UPDATE_RANK">تحديث الرتبة (ترقيات وتسويات)</option>
                
                <!-- أمان ومزامنة -->
                <option v-if="activeService.service_type === 'security'" value="SECURITY_RESTRICT">قيد أمني (إيقاف / تجميد)</option>
                <option v-if="activeService.service_type === 'security'" value="SECURITY_SYNC">مزامنة أمنية</option>

                <!-- جزاءات -->
                <option v-if="activeService.service_type === 'disciplinary'" value="DISCIPLINARY_DEDUCTION">خصم مالي / أيام</option>
                <option v-if="activeService.service_type === 'disciplinary'" value="DISCIPLINARY_DEMOTION">تنزيل رتبة</option>
                <option v-if="activeService.service_type === 'disciplinary'" value="DISCIPLINARY_PRISON">سجن عسكري</option>

                <option value="NONE">للتوثيق فقط (لا يُنفذ تغيير آلي)</option>
              </select>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">نوع الموافقة</label>
              <select v-model="activeService.approval_type" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm outline-none">
                <option value="internal">موافقة داخلية</option>
                <option value="external">موافقة خارجية</option>
                <option value="none">لا تتطلب موافقة</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">تصنيف الخدمة</label>
              <select v-model="activeService.service_type" @change="activeService.execution_action = 'NONE'" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm outline-none">
                <option value="form">استمارة (تغيير حالة)</option>
                <option value="correction">تصحيح بيانات</option>
                <option value="rank_settlement">ترقية / تسوية رتبة</option>
                <option value="disciplinary">جزاء تأديبي</option>
                <option value="security">أمان ومزامنة</option>
                <option value="other">أخرى</option>
              </select>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">الفئة المستهدفة</label>
              <select v-model="activeService.target_audience" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm outline-none">
                <option value="الكل">الكل</option>
                <option value="الضباط">الضباط فقط</option>
                <option value="الأفراد">الأفراد فقط</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">المدة المتوقعة (بالساعات)</label>
              <input type="number" v-model="activeService.expected_duration_hours" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none" placeholder="مثال: 24" />
            </div>
          </div>
          <!-- Dynamic Execution Config based on Action -->
          <div v-if="activeService.execution_action !== 'NONE'" class="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-xl border border-gray-100 dark:border-gray-700 space-y-4 mb-4">
            <h4 class="text-sm font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <Settings class="w-4 h-4 text-brand-500" />
              إعدادات التنفيذ (Execution Config)
            </h4>
            
            <div v-if="activeService.execution_action === 'UPDATE_STATUS'">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">الحالة المستهدفة (Target Status) <span class="text-rose-500">*</span></label>
              <select v-model="activeService.execution_config.to_status_id" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm outline-none">
                <option value="">-- اختر الحالة --</option>
                <option v-for="st in statuses" :key="st.id" :value="st.id">{{ st.name }}</option>
              </select>
              <p class="text-[10px] text-gray-500 mt-1">الحالة التي سيتحول إليها الفرد بعد الموافقة النهائية.</p>
            </div>

            <div v-if="activeService.execution_action === 'UPDATE_RANK'">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">نوع الترقية / التسوية</label>
              <select v-model="activeService.execution_config.promotion_type" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm outline-none">
                <option value="normal_promotion">ترقية أفراد عادية</option>
                <option value="officer_settlement">تسوية رتبة لضابط</option>
              </select>
            </div>

            <div v-if="activeService.execution_action === 'SECURITY_RESTRICT' || activeService.execution_action === 'SECURITY_SYNC'">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">نوع القيد / المزامنة</label>
              <input type="text" v-model="activeService.execution_config.restriction_type" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm outline-none" placeholder="مثال: حرمان من الترقية، إيقاف راتب" />
            </div>

            <!-- Correction Info -->
            <div v-if="activeService.execution_action.startsWith('CORRECTION_')" class="p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
              <p class="text-xs text-blue-700 dark:text-blue-300 font-bold flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                تحديث تلقائي لقاعدة البيانات
              </p>
              <p class="text-[10px] text-blue-600 dark:text-blue-400 mt-1">
                هذا الإجراء سيقوم بتحديث بيانات السجل المدني والعسكري للفرد مباشرة فور الاعتماد النهائي، ولا يتطلب إعدادات إضافية هنا.
              </p>
            </div>

            <!-- Disciplinary Config -->
            <div v-if="activeService.execution_action === 'DISCIPLINARY_DEDUCTION'">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">الحد الأقصى للخصم (بالأيام)</label>
              <input type="number" v-model="activeService.execution_config.max_deduction_days" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm outline-none" placeholder="مثال: 15" />
            </div>
            
            <div v-if="activeService.execution_action === 'DISCIPLINARY_DEMOTION'">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">مستوى التنزيل</label>
              <select v-model="activeService.execution_config.demotion_levels" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm outline-none">
                <option value="1">رتبة واحدة (الرتبة الأدنى مباشرة)</option>
                <option value="2">رتبتين</option>
                <option value="custom">تحديد يدوي من قبل اللجنة</option>
              </select>
            </div>

            <div v-if="activeService.execution_action === 'DISCIPLINARY_PRISON'">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">الحد الأقصى للسجن (بالأيام)</label>
              <input type="number" v-model="activeService.execution_config.max_prison_days" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm outline-none" placeholder="مثال: 30" />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" v-model="activeService.is_active" class="w-4 h-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500" />
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">الخدمة مفعلة</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" v-model="activeService.requires_approval" class="w-4 h-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500" />
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">تتطلب موافقات</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" v-model="activeService.is_repeatable" class="w-4 h-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500" />
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">قابلة للتكرار</span>
            </label>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">وصف الخدمة</label>
            <textarea v-model="activeService.description" rows="2" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none" placeholder="اكتب وصفاً مختصراً لهذه الخدمة..."></textarea>
          </div>
        </div>
        <div class="px-6 py-4 border-t border-gray-100 dark:border-gray-700 flex justify-end gap-3 bg-gray-50 dark:bg-gray-900/50">
          <button @click="modals.create = false" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-xl hover:bg-gray-50">إلغاء</button>
          <button @click="saveBasicService" :disabled="saving" class="px-4 py-2 text-sm font-medium text-white bg-brand-600 rounded-xl hover:bg-brand-700 disabled:opacity-50 flex items-center gap-2">
            <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
            <span v-else>حفظ الخدمة</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 2. Fields Builder Modal (Dynamic Sections) -->
    <div v-if="modals.fields" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/50 backdrop-blur-sm p-4">
      <div class="bg-white dark:bg-gray-800 w-full max-w-5xl rounded-2xl shadow-xl overflow-hidden animate-fade-in-up flex flex-col max-h-[90vh]">
          <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center bg-gray-50 dark:bg-gray-900/50">
          <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <LayoutTemplate class="w-5 h-5 text-brand-600" />
            إصدارات الحقول للخدمة: {{ activeService.name_ar }}
          </h3>
          <div class="flex gap-2">
            <button @click="addSection" class="px-3 py-1.5 text-xs font-bold text-brand-700 bg-brand-50 rounded-lg hover:bg-brand-100 flex items-center gap-1 border border-brand-200">
              <Plus class="w-3.5 h-3.5" /> إضافة قسم جديد
            </button>
            <button @click="modals.fields = false" class="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
              <X class="w-5 h-5" />
            </button>
          </div>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6 space-y-6 bg-gray-50/30 dark:bg-gray-900/30">

          <!-- ══ Field Guide Reference Panel ══ -->
          <details class="border border-blue-200 dark:border-blue-800 rounded-xl overflow-hidden bg-blue-50/60 dark:bg-blue-900/10">
            <summary class="flex items-center gap-2 px-4 py-3 cursor-pointer select-none font-bold text-sm text-blue-800 dark:text-blue-300 list-none hover:bg-blue-100/50 dark:hover:bg-blue-900/20">
              <span class="text-lg">📖</span>
              دليل الحقول — أنواع المصادر وكيفية استخدامها
              <span class="mr-auto text-xs font-normal opacity-60">انقر للعرض / الإخفاء</span>
            </summary>
            <div class="px-4 pb-4 space-y-4 text-xs">

              <!-- Source Types Legend -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mt-3">
                <div class="p-3 bg-white dark:bg-gray-800 border border-green-200 dark:border-green-800 rounded-lg">
                  <div class="font-bold text-green-700 dark:text-green-400 mb-1 flex items-center gap-1">
                    <span>✏️</span> إدخال مستخدم
                  </div>
                  <p class="text-gray-600 dark:text-gray-400">حقل يُعبئه المستخدم يدوياً عند تقديم الطلب. مثل: رقم القرار، تاريخ القرار، سبب التنزيل، الملاحظات.</p>
                </div>
                <div class="p-3 bg-white dark:bg-gray-800 border border-blue-200 dark:border-blue-800 rounded-lg">
                  <div class="font-bold text-blue-700 dark:text-blue-400 mb-1 flex items-center gap-1">
                    <span>🗄️</span> قاعدة البيانات (سجل الفرد)
                  </div>
                  <p class="text-gray-600 dark:text-gray-400">يُسحب تلقائياً من ملف الفرد. لا يُعبئه المستخدم. مثل: الاسم، الرقم العسكري، الرتبة، الوحدة، تاريخ الميلاد.</p>
                </div>
                <div class="p-3 bg-white dark:bg-gray-800 border border-orange-200 dark:border-orange-800 rounded-lg">
                  <div class="font-bold text-orange-700 dark:text-orange-400 mb-1 flex items-center gap-1">
                    <span>⚙️</span> من النظام (ثابت - مخفي)
                  </div>
                  <p class="text-gray-600 dark:text-gray-400">قيمة ثابتة يضعها النظام تلقائياً. مثل: الفئة (ثابتة كـ "الترقيات")، نوع التسوية. تكون معطلة ومخفية عن المستخدم.</p>
                </div>
              </div>

              <!-- DB Fields Quick Reference -->
              <div class="mt-2">
                <p class="font-bold text-gray-700 dark:text-gray-300 mb-2">⚡ حقول سجل الفرد — يمكن إضافتها بنقرة واحدة:</p>
                <div class="flex flex-wrap gap-1.5">
                  <button v-for="pf in personnelFields" :key="pf.key"
                    @click="quickAddDbField(pf)"
                    class="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-700 rounded-lg hover:bg-blue-200 dark:hover:bg-blue-800/50 text-[10px] font-bold flex items-center gap-1 transition-colors">
                    <span>+</span> {{ pf.label }}
                    <code class="opacity-60 font-mono">{{ pf.key }}</code>
                  </button>
                </div>
              </div>

              <!-- Common System Fields -->
              <div class="mt-2">
                <p class="font-bold text-gray-700 dark:text-gray-300 mb-2">⚙️ حقول النظام الثابتة الشائعة:</p>
                <div class="flex flex-wrap gap-1.5">
                  <button v-for="sf in systemFields" :key="sf.key"
                    @click="quickAddSystemField(sf)"
                    class="px-2 py-1 bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300 border border-orange-200 dark:border-orange-700 rounded-lg hover:bg-orange-200 dark:hover:bg-orange-800/50 text-[10px] font-bold flex items-center gap-1 transition-colors">
                    <span>+</span> {{ sf.label }}
                    <code class="opacity-60 font-mono">{{ sf.key }}</code>
                  </button>
                </div>
              </div>
            </div>
          </details>

          <!-- Auto Sections from FormRegistry (Read-Only Reference) -->
          <div v-for="(autoSec, aIdx) in registryAutoSections" :key="'auto-' + aIdx" class="border border-gray-300 dark:border-gray-600 rounded-xl bg-gray-100 dark:bg-gray-800 opacity-75 overflow-hidden shadow-sm">
            <div class="bg-gray-200 dark:bg-gray-700/50 px-4 py-3 flex justify-between items-center border-b border-gray-300 dark:border-gray-600">
              <div class="flex items-center gap-2 text-gray-700 dark:text-gray-300 font-bold text-sm">
                <ShieldCheck class="w-4 h-4 text-emerald-600" />
                {{ autoSec.title }} (تلقائي — للاستمارات فقط)
              </div>
              <span class="text-[10px] bg-gray-300 dark:bg-gray-600 text-gray-600 dark:text-gray-300 px-2 py-0.5 rounded-full">🔒 للقراءة فقط</span>
            </div>
            <div class="p-3 flex flex-wrap gap-1.5 bg-gray-50 dark:bg-gray-900/20">
              <span v-for="f in autoSec.fields" :key="f.key" class="text-[10px] bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 px-2 py-1 rounded-md border border-blue-200 dark:border-blue-800 font-bold">
                🗄️ {{ f.label }}
              </span>
            </div>
          </div>

          <!-- Divider -->
          <div v-if="registryAutoSections.length > 0 || activeService.service_type === 'form'" class="flex items-center gap-4 py-2">
            <div class="h-px bg-brand-200 dark:bg-brand-800/30 flex-1"></div>
            <span class="text-xs font-bold text-brand-600 dark:text-brand-400 bg-brand-50 dark:bg-brand-900/20 px-3 py-1 rounded-full border border-brand-100 dark:border-brand-800/50">الأقسام والحقول الديناميكية (قابلة للتحرير)</span>
            <div class="h-px bg-brand-200 dark:bg-brand-800/30 flex-1"></div>
          </div>

          <!-- ══ Live Table Preview ══ -->
          <details v-if="sections.some(s => s.fields.length > 0)" class="border border-brand-200 dark:border-brand-800/60 rounded-xl overflow-hidden bg-white dark:bg-gray-900 shadow-sm mt-4">
            <summary class="flex items-center gap-2 px-5 py-4 cursor-pointer select-none font-bold text-sm text-brand-800 dark:text-brand-300 list-none hover:bg-brand-50/50 dark:hover:bg-brand-900/20 transition-colors border-b border-transparent dark:border-transparent data-[open]:border-brand-100">
              <svg class="w-5 h-5 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
              معاينة — كيف ستظهر الحقول في دليل الخدمات
              <span class="mr-auto text-xs font-normal text-gray-400 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded-md">انقر للعرض</span>
            </summary>
            <div class="p-5 overflow-x-auto bg-gray-50/30 dark:bg-gray-900/30">
              <div class="border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden shadow-sm bg-white dark:bg-gray-900">
                <table class="w-full border-collapse text-right text-sm">
                  <thead>
                    <tr class="bg-gray-50 dark:bg-gray-800/80 text-gray-700 dark:text-gray-300 font-bold text-xs uppercase tracking-wider">
                      <th class="p-3 border-b border-l border-gray-200 dark:border-gray-700 text-center w-10">م</th>
                      
                      <!-- Hardcoded columns for Specialized Transactions to match directory UI -->
                      <template v-if="['rank_demotion', 'rank_promotion', 'personnel_to_officer'].includes(activeService.form_type)">
                        <th class="p-3 border-b border-l border-gray-200 dark:border-gray-700 text-center text-blue-700 dark:text-blue-400 bg-blue-50/50 dark:bg-blue-900/10">الرتبة</th>
                        <th class="p-3 border-b border-l border-gray-200 dark:border-gray-700 text-center text-blue-700 dark:text-blue-400 bg-blue-50/50 dark:bg-blue-900/10">الرقم العسكري</th>
                        <th class="p-3 border-b border-l border-gray-200 dark:border-gray-700 text-center text-blue-700 dark:text-blue-400 bg-blue-50/50 dark:bg-blue-900/10">الاسم الرباعي</th>
                      </template>

                      <template v-for="(autoSec) in registryAutoSections" :key="'prev-auto-' + autoSec.title">
                        <th v-for="f in autoSec.fields" :key="'prev-' + f.key" class="p-3 border-b border-l border-gray-200 dark:border-gray-700 text-center text-blue-700 dark:text-blue-400 bg-blue-50/50 dark:bg-blue-900/10">
                          {{ f.label }}
                        </th>
                      </template>
                      <template v-for="sec in sections" :key="'prev-sec-' + sec.title">
                        <template v-for="f in sec.fields.filter((ff:any) => ff.source !== 'system')" :key="'prev-f-' + f.key">
                          <th class="p-3 border-b border-l border-gray-200 dark:border-gray-700 text-center text-brand-700 dark:text-brand-400 bg-brand-50/30 dark:bg-brand-900/10">
                            {{ f.label }}
                            <span v-if="f.required" class="text-red-500 mr-1">*</span>
                          </th>
                        </template>
                      </template>
                      <th class="p-3 border-b border-gray-200 dark:border-gray-700 text-center w-16">الإجراء</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                      <td class="p-3 border-b border-l border-gray-200 dark:border-gray-700 text-center font-bold">1</td>
                      
                      <template v-if="['rank_demotion', 'rank_promotion', 'personnel_to_officer'].includes(activeService.form_type)">
                        <td class="p-3 border-b border-l border-gray-200 dark:border-gray-700 text-center text-xs opacity-60">(تلقائي)</td>
                        <td class="p-3 border-b border-l border-gray-200 dark:border-gray-700 text-center text-xs opacity-60 font-mono">(تلقائي)</td>
                        <td class="p-3 border-b border-l border-gray-200 dark:border-gray-700 text-center text-xs opacity-60">(تلقائي)</td>
                      </template>

                      <template v-for="(autoSec) in registryAutoSections" :key="'sample-auto-' + autoSec.title">
                        <td v-for="f in autoSec.fields" :key="'sample-' + f.key" class="p-3 border-b border-l border-gray-200 dark:border-gray-700 text-center text-xs opacity-60">
                          (تلقائي)
                        </td>
                      </template>
                      <template v-for="sec in sections" :key="'sample-sec-' + sec.title">
                        <template v-for="f in sec.fields.filter((ff:any) => ff.source !== 'system')" :key="'sample-f-' + f.key">
                          <td class="p-3 border-b border-l border-gray-200 dark:border-gray-700 text-center text-xs text-gray-400">
                            <div v-if="f.options_source" class="flex items-center justify-center gap-1.5 text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-900/20 py-1 px-2 rounded">
                              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/></svg>
                              {{ linkedDataSources[f.options_source] || 'قائمة' }}
                            </div>
                            <div v-else-if="f.type === 'select'" class="flex items-center justify-center gap-1.5 bg-gray-100 dark:bg-gray-800 py-1 px-2 rounded">
                              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg> قائمة
                            </div>
                            <div v-else-if="f.type === 'date'" class="flex items-center justify-center gap-1.5">
                              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                            </div>
                            <div v-else-if="f.type === 'textarea'" class="flex items-center justify-center gap-1.5">
                              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"/></svg>
                            </div>
                            <div v-else class="text-gray-300 dark:text-gray-600 border-b-2 border-dashed border-gray-300 dark:border-gray-600 w-8 mx-auto"></div>
                          </td>
                        </template>
                      </template>
                      <td class="p-3 border-b border-gray-200 dark:border-gray-700 text-center">
                        <button class="text-red-400 hover:text-red-600 bg-red-50 hover:bg-red-100 dark:bg-red-900/20 p-1.5 rounded-lg transition-colors cursor-not-allowed">
                          <Trash2 class="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </details>

          <div v-if="sections.length === 0" class="text-center py-10 border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-xl">
            <p class="text-gray-500">لم يتم إضافة أي أقسام إضافية لهذه الاستمارة.</p>
          </div>
          
          <div v-for="(section, sIdx) in sections" :key="sIdx" class="border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-800 overflow-hidden shadow-sm">
            <div class="bg-gray-100 dark:bg-gray-700/50 px-4 py-3 flex justify-between items-center border-b border-gray-300 dark:border-gray-600">
              <div class="flex items-center gap-3 w-2/3">
                <input type="text" v-model="section.title" placeholder="عنوان القسم (مثال: البيانات الشخصية)" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg px-2 py-1 text-sm font-bold outline-none" />
              </div>
              <div class="flex items-center gap-2">
                <button @click="addFieldToSection(Number(sIdx))" class="px-2 py-1 text-xs font-bold text-brand-700 bg-brand-50 rounded-lg hover:bg-brand-100 border border-brand-200 flex items-center gap-1">
                  <Plus class="w-3.5 h-3.5" /> إضافة حقل
                </button>
                <button @click="removeSection(Number(sIdx))" class="p-1 text-red-500 hover:bg-red-50 rounded-lg" title="حذف القسم">
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </div>
            
            <div class="p-4 space-y-3">
              <div v-if="section.fields.filter((f:any) => f.source !== 'system' || !['rank_demotion', 'rank_promotion', 'personnel_to_officer'].includes(activeService.form_type)).length === 0" class="text-center py-4 text-xs text-gray-400">لا توجد حقول في هذا القسم</div>
              
              <template v-for="(field, fIdx) in section.fields" :key="'f-' + fIdx">
                <div v-if="field.source !== 'system' || !['rank_demotion', 'rank_promotion', 'personnel_to_officer'].includes(activeService.form_type)" class="p-3 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-900/50 relative group">
                <button @click="removeFieldFromSection(Number(sIdx), Number(fIdx))" class="absolute top-2 left-2 p-1 text-red-500 hover:bg-red-50 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity">
                  <Trash2 class="w-3 h-3" />
                </button>
                
                <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
                  <div class="col-span-1 md:col-span-1">
                    <label class="block text-[10px] font-bold text-gray-500 mb-1">اسم الحقل (يظهر للمستخدم)</label>
                    <input type="text" v-model="field.label" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-2 py-1 text-xs outline-none" />
                  </div>
                  
                  <div class="col-span-1 md:col-span-1">
                    <label class="block text-[10px] font-bold text-gray-500 mb-1">مصدر الحقل</label>
                    <select v-model="field.source" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-2 py-1 text-xs outline-none">
                      <option value="user_input">إدخال مستخدم</option>
                      <option value="personnel_master">قاعدة البيانات (سجل الفرد)</option>
                      <option value="system">من النظام (ثابت - مخفي)</option>
                    </select>
                  </div>
                  
                  <div class="col-span-1">
                    <label class="block text-[10px] font-bold text-gray-500 mb-1">المفتاح (Key)</label>
                    <select v-if="field.source === 'personnel_master'" v-model="field.key" @change="onDbFieldSelected(field)" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-2 py-1 text-xs outline-none">
                      <option value="" disabled>اختر الحقل...</option>
                      <option v-for="pf in personnelFields" :key="pf.key" :value="pf.key">{{ pf.label }}</option>
                    </select>
                    <input v-else type="text" v-model="field.key" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-2 py-1 text-xs outline-none" />
                  </div>
                  
                  <div class="col-span-1">
                    <label class="block text-[10px] font-bold text-gray-500 mb-1">نوع الحقل</label>
                    <select v-model="field.type" :disabled="field.source === 'personnel_master'" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-2 py-1 text-xs outline-none disabled:opacity-50 disabled:cursor-not-allowed">
                      <option value="text">نص</option>
                      <option value="number">رقم</option>
                      <option value="date">تاريخ</option>
                      <option value="select">قائمة</option>
                      <option value="location_cascade">تحديد موقع (محافظة، الخ)</option>
                      <option value="auto">تلقائي (قراءة فقط)</option>
                    </select>
                  </div>
                  
                  <div class="col-span-1 flex items-center justify-around pt-4" :class="{'opacity-50 pointer-events-none': section.source === 'personnel_master'}">
                     <label class="flex items-center gap-1 text-[10px] text-gray-600">
                        <input type="checkbox" v-model="field.required" class="rounded text-brand-600" :disabled="section.source === 'personnel_master'" />
                        إلزامي
                     </label>
                     <label class="flex items-center gap-1 text-[10px] text-gray-600">
                        <input type="checkbox" v-model="field.disabled" class="rounded text-brand-600" :disabled="section.source === 'personnel_master'" />
                        معطل (مخفي)
                     </label>
                  </div>
                </div>
                
                <div v-if="field.type === 'select' || field.default !== undefined || true" class="mt-2 grid grid-cols-2 gap-3 pt-2 border-t border-gray-100 dark:border-gray-700">
                  <div v-if="field.type === 'select'">
                    <label class="block text-[10px] font-bold text-gray-500 mb-1">مصدر الخيارات</label>
                    <select v-model="field.options_source" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-2 py-1 text-xs outline-none">
                      <option v-for="(lbl, key) in linkedDataSources" :key="key" :value="key">{{ lbl }}</option>
                    </select>
                    <div v-if="!field.options_source" class="mt-1">
                      <label class="block text-[10px] font-bold text-gray-500 mb-1">الخيارات (مفصولة بفاصلة)</label>
                      <input type="text" v-model="field.optionsStr" placeholder="خيار 1, خيار 2, خيار 3" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-2 py-1 text-xs outline-none" />
                    </div>
                    <div v-else class="mt-1 text-[10px] text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-900/20 px-2 py-1 rounded border border-emerald-200 dark:border-emerald-800">
                      ✅ سيتم تحميل الخيارات تلقائياً من النظام ({{ linkedDataSources[field.options_source] || field.options_source }})
                    </div>
                  </div>
                  <div :class="field.type === 'select' ? '' : 'col-span-2'">
                    <label class="block text-[10px] font-bold text-gray-500 mb-1">قيمة افتراضية (Default)</label>
                    <input type="text" v-model="field.default" placeholder="" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-2 py-1 text-xs outline-none" />
                  </div>
                </div>
              </div>
              </template>
            </div>
          </div>
        </div>
        
        <div class="px-6 py-4 border-t border-gray-100 dark:border-gray-700 flex justify-end gap-3 bg-gray-50 dark:bg-gray-900/50">
          <button @click="modals.fields = false" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-xl hover:bg-gray-50">إغلاق</button>
          <button @click="saveFieldsSchema" :disabled="saving" class="px-4 py-2 text-sm font-medium text-white bg-brand-600 rounded-xl hover:bg-brand-700 disabled:opacity-50 flex items-center gap-2">
            <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
            <span v-else>حفظ الاستمارة</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 3. Workflow Builder Modal -->
    <div v-if="modals.workflow" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/50 backdrop-blur-sm p-4">
      <div class="bg-white dark:bg-gray-800 w-full max-w-4xl rounded-2xl shadow-xl overflow-hidden animate-fade-in-up flex flex-col max-h-[90vh]">
        <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center bg-indigo-50 dark:bg-indigo-900/20">
          <h3 class="font-bold text-gray-900 dark:white flex items-center gap-2">
            <GitMerge class="w-5 h-5 text-indigo-600" />
            مراحل سير العمل للخدمة: {{ activeService.name_ar }}
          </h3>
          <div class="flex gap-2">
            <button @click="modals.workflow = false" class="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
              <X class="w-5 h-5" />
            </button>
          </div>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6 bg-gray-50/30 dark:bg-gray-900/30 flex gap-6">
          <!-- Available Stages -->
          <div class="w-1/3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-4 h-fit">
            <h4 class="text-xs font-bold text-gray-500 mb-3 uppercase tracking-wider">المراحل المتاحة</h4>
            <div class="space-y-2">
              <div v-for="st in availableStages" :key="st.id" @click="addWorkflowStep(st)" class="p-2.5 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-900 hover:border-indigo-500 cursor-pointer flex justify-between items-center group">
                <span class="text-sm font-medium">{{ st.name_ar }}</span>
                <PlusCircle class="w-4 h-4 text-gray-400 group-hover:text-indigo-500" />
              </div>
            </div>
            
            <button @click="createNewStage" class="mt-4 w-full py-2 border-2 border-dashed border-gray-300 dark:border-gray-700 text-gray-500 rounded-lg hover:border-indigo-500 hover:text-indigo-500 text-sm font-medium flex justify-center items-center gap-2 transition-colors">
              <Plus class="w-4 h-4" /> مرحلة جديدة
            </button>
          </div>
          
          <!-- Selected Steps -->
          <div class="w-2/3 space-y-3">
            <h4 class="text-xs font-bold text-gray-500 mb-3 uppercase tracking-wider">التسلسل المعتمد للخدمة</h4>
            <div v-if="workflowSteps.length === 0" class="text-center py-10 border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-xl">
              <p class="text-gray-500 text-sm">انقر على مرحلة من القائمة لإضافتها إلى التسلسل.</p>
            </div>
            
            <div v-for="(step, index) in workflowSteps" :key="index" class="p-3 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-800 flex gap-4 shadow-sm relative group">
              <div class="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-400 font-black text-sm shrink-0">
                {{ index + 1 }}
              </div>
              <div class="flex-1">
                <div class="flex justify-between items-start">
                  <h5 class="font-bold text-sm">{{ step.stage_details?.name_ar || getStageName(step.stage) }}</h5>
                  <button @click="removeWorkflowStep(index)" class="text-red-400 hover:text-red-600 opacity-0 group-hover:opacity-100 transition-opacity">
                    <Trash2 class="w-4 h-4" />
                  </button>
                </div>
                
                <input type="text" v-model="step.description" placeholder="تعليمات وإرشادات لهذه المرحلة..." class="mt-2 w-full text-xs p-2 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded outline-none" />
                
                <div class="flex gap-4 mt-3">
                  <label class="flex items-center gap-1.5 text-xs text-gray-600 dark:text-gray-400 cursor-pointer">
                    <input type="checkbox" v-model="step.requires_approval" class="rounded text-indigo-600 focus:ring-indigo-500">
                    تتطلب اعتماد
                  </label>
                  <label class="flex items-center gap-1.5 text-xs text-gray-600 dark:text-gray-400 cursor-pointer">
                    <input type="checkbox" v-model="step.is_final_step" @change="ensureOnlyOneFinal(index)" class="rounded text-indigo-600 focus:ring-indigo-500">
                    مرحلة نهائية
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="px-6 py-4 border-t border-gray-100 dark:border-gray-700 flex justify-end gap-3 bg-gray-50 dark:bg-gray-900/50">
          <button @click="modals.workflow = false" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-xl hover:bg-gray-50">إغلاق</button>
          <button @click="saveWorkflowSteps" :disabled="saving" class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-xl hover:bg-indigo-700 disabled:opacity-50 flex items-center gap-2">
            <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
            <span v-else>حفظ المسار</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 4. Prerequisites Modal -->
    <div v-if="modals.prereqs" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/50 backdrop-blur-sm p-4">
      <div class="bg-white dark:bg-gray-800 w-full max-w-4xl rounded-2xl shadow-xl overflow-hidden animate-fade-in-up flex flex-col max-h-[90vh]">
        <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center bg-rose-50 dark:bg-rose-900/20">
          <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <ShieldCheck class="w-5 h-5 text-rose-600" />
            شروط التقديم للخدمة: {{ activeService.name_ar }}
          </h3>
          <div class="flex gap-2">
            <button @click="addPrerequisite" class="px-3 py-1.5 text-xs font-bold text-rose-700 bg-rose-100 rounded-lg hover:bg-rose-200 flex items-center gap-1 border border-rose-200">
              <Plus class="w-3.5 h-3.5" /> إضافة شرط
            </button>
            <button @click="modals.prereqs = false" class="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
              <X class="w-5 h-5" />
            </button>
          </div>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6 bg-gray-50/30 dark:bg-gray-900/30 space-y-4">
          
          <!-- Engine Rules Banner -->
          <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-4 mb-2">
            <h4 class="text-sm font-bold text-blue-900 dark:text-blue-300 flex items-center gap-2 mb-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
              محرك القواعد المتقدم (Service Rules Engine)
            </h4>
            <p class="text-xs text-blue-700 dark:text-blue-400 leading-relaxed mb-3">
              تعمل هذه الخدمة تحت مظلة <b>محرك القواعد المركزي</b> في الخادم (Backend). الشروط المضافة أدناه هي شروط واجهة مساعدة (UI) للمستخدم فقط. 
              أما القواعد المركزية التالية فهي قواعد صارمة (Hardcoded)، ولكن <b>تم منحك صلاحية تفعيلها أو إيقافها استثنائياً</b> لهذه الخدمة:
            </p>
            
            <div v-if="engineRules.length > 0" class="space-y-2 mt-3">
              <div v-for="rule in engineRules" :key="rule.id" class="flex items-start justify-between gap-2 bg-white/60 dark:bg-gray-900/50 p-2 rounded-lg border border-blue-100 dark:border-blue-800/50">
                <div class="flex gap-2">
                  <ShieldCheck class="w-4 h-4 shrink-0 mt-0.5" :class="rule.is_active ? 'text-blue-500' : 'text-gray-400'" />
                  <div>
                    <p class="text-xs font-bold flex gap-2" :class="rule.is_active ? 'text-blue-900 dark:text-blue-300' : 'text-gray-500 dark:text-gray-400 line-through'">
                      {{ rule.name }}
                      <span class="font-mono text-[9px] px-1 rounded" :class="rule.is_active ? 'text-blue-400 bg-blue-100 dark:bg-blue-800/50' : 'text-gray-400 bg-gray-100 dark:bg-gray-800/50'">{{ rule.id }}</span>
                    </p>
                    <p class="text-[10px] mt-0.5" :class="rule.is_active ? 'text-blue-700 dark:text-blue-400' : 'text-gray-400'">{{ rule.description || 'قاعدة نظام أساسية.' }}</p>
                  </div>
                </div>
                <label class="relative inline-flex items-center cursor-pointer ml-2 mt-1">
                  <input type="checkbox" :checked="rule.is_active" @change="toggleEngineRule(rule)" class="sr-only peer">
                  <div class="w-9 h-5 bg-gray-200 peer-focus:outline-none rounded-full peer dark:bg-gray-700 peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:right-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all dark:border-gray-600 peer-checked:bg-blue-500"></div>
                </label>
              </div>
            </div>
            <div v-else class="text-xs text-blue-600 dark:text-blue-500 bg-white/60 dark:bg-gray-900/50 p-2 rounded-lg italic">
              هذه الخدمة لا تستخدم محرك القواعد المركزي حالياً وتعتمد فقط على الشروط المعرفة في الواجهة أدناه.
            </div>
          </div>

          <div v-if="prerequisites.length === 0" class="text-center py-10 border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-xl">
            <ShieldAlert class="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <p class="text-gray-500 text-sm">لم يتم إضافة أي شروط واجهة مساعدة لهذه الخدمة.</p>
          </div>
          
          <div v-for="(prereq, index) in prerequisites" :key="index" class="p-4 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-800 relative group shadow-sm">
            <button @click="removePrerequisite(index)" class="absolute top-3 left-3 p-1.5 text-red-500 hover:bg-red-50 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity">
              <Trash2 class="w-4 h-4" />
            </button>
            
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div class="col-span-1 md:col-span-2">
                <label class="block text-xs font-medium text-gray-500 mb-1">اسم الشرط (للعرض)</label>
                <input type="text" v-model="prereq.name_ar" placeholder="مثال: ألا يقل العمر عن 30" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-1.5 text-sm outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-200" />
              </div>
              
              <div class="col-span-1">
                <label class="block text-xs font-medium text-gray-500 mb-1">نوع التحقق</label>
                <select v-model="prereq.validation_type" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-1.5 text-sm outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-200">
                  <option value="age_min">الحد الأدنى للعمر</option>
                  <option value="age_max">الحد الأقصى للعمر</option>
                  <option value="service_years_min">الحد الأدنى لسنوات الخدمة</option>
                  <option value="status_check">التحقق من الحالة</option>
                  <option value="custom">مخصص</option>
                </select>
              </div>
              
              <div class="col-span-1">
                <label class="block text-xs font-medium text-gray-500 mb-1">القيمة المطلوبة</label>
                <input type="text" v-model="prereq.validation_value" placeholder="مثال: 30" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-1.5 text-sm outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-200" />
              </div>
            </div>
            
            <div class="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700 flex gap-4 items-center">
              <input type="text" v-model="prereq.description" placeholder="رسالة الخطأ التوضيحية عند عدم تحقق الشرط..." class="flex-1 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-1.5 text-xs outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-200" />
              
              <label class="flex items-center gap-1.5 text-xs text-gray-600 dark:text-gray-400 cursor-pointer">
                <input type="checkbox" v-model="prereq.is_mandatory" class="rounded text-rose-600 focus:ring-rose-500">
                إلزامي (يمنع التقديم)
              </label>
            </div>
          </div>
        </div>

        <div class="px-6 py-4 border-t border-gray-100 dark:border-gray-700 flex justify-end gap-3 bg-gray-50 dark:bg-gray-900/50">
          <button @click="modals.prereqs = false" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-xl hover:bg-gray-50">إغلاق</button>
          <button @click="savePrerequisites" :disabled="saving" class="px-4 py-2 text-sm font-medium text-white bg-rose-600 rounded-xl hover:bg-rose-700 disabled:opacity-50 flex items-center gap-2">
            <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
            <span v-else>حفظ الشروط</span>
          </button>
        </div>
      </div>
    </div>
    <!-- 5. Attachments Modal -->
    <div v-if="modals.attachments" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/50 backdrop-blur-sm p-4">
      <div class="bg-white dark:bg-gray-800 w-full max-w-3xl rounded-2xl shadow-xl overflow-hidden animate-fade-in-up flex flex-col max-h-[90vh]">
        <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center bg-amber-50 dark:bg-amber-900/20">
          <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Paperclip class="w-5 h-5 text-amber-600" />
            المرفقات الإلزامية للخدمة: {{ activeService.name_ar }}
          </h3>
          <div class="flex gap-2">
            <button @click="addAttachment" class="px-3 py-1.5 text-xs font-bold text-amber-700 bg-amber-100 rounded-lg hover:bg-amber-200 flex items-center gap-1">
              <Plus class="w-3.5 h-3.5" /> إضافة مرفق
            </button>
            <button @click="modals.attachments = false" class="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
              <X class="w-5 h-5" />
            </button>
          </div>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50/30 dark:bg-gray-900/30">
          <div v-if="attachments.length === 0" class="text-center py-10 border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-xl">
            <p class="text-gray-500 text-sm">لا توجد مرفقات مطلوبة لهذه الخدمة.</p>
          </div>
          
          <div v-for="(att, idx) in attachments" :key="idx" class="p-4 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-800 relative group shadow-sm">
            <button @click="removeAttachment(idx)" class="absolute top-3 left-3 p-1.5 text-red-500 hover:bg-red-50 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity">
              <Trash2 class="w-4 h-4" />
            </button>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="col-span-1 md:col-span-2 relative">
                <label class="block text-xs font-medium text-gray-500 mb-1">اسم المرفق (مثال: صورة البطاقة)</label>
                <input type="text" v-model="att.label" @focus="att.showDropdown = true" @blur="hideDropdown(att)" placeholder="اختر من القائمة أو اكتب اسماً جديداً..." class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-1.5 text-sm outline-none focus:ring-2 focus:ring-amber-500" />
                
                <div v-if="att.showDropdown" class="absolute z-50 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-xl max-h-48 overflow-y-auto">
                  <div v-for="(item, i) in commonAttachmentsList.filter(x => !att.label || x.includes(att.label))" :key="i" @mousedown="selectAttachment(att, item)" class="px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-amber-50 dark:hover:bg-amber-900/30 cursor-pointer border-b border-gray-100 dark:border-gray-700 last:border-0">
                    {{ item }}
                  </div>
                  <div v-if="commonAttachmentsList.filter(x => !att.label || x.includes(att.label)).length === 0" class="px-3 py-2 text-xs text-gray-500">
                    اضغط Enter لإضافة "{{ att.label }}"
                  </div>
                </div>
              </div>
              
              <div class="col-span-1">
                <label class="block text-xs font-medium text-gray-500 mb-1">المفتاح (Key)</label>
                <input type="text" v-model="att.key" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-1.5 text-sm outline-none" />
              </div>
            </div>
            
            <div class="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700 flex gap-4 items-center">
              <input type="text" v-model="att.description" placeholder="وصف المرفق (اختياري)..." class="flex-1 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-1.5 text-xs outline-none" />
              
              <label class="flex items-center gap-1.5 text-xs text-gray-600 dark:text-gray-400 cursor-pointer">
                <input type="checkbox" v-model="att.required" class="rounded text-amber-600 focus:ring-amber-500">
                مرفق إلزامي
              </label>
            </div>
          </div>
        </div>

        <div class="px-6 py-4 border-t border-gray-100 dark:border-gray-700 flex justify-end gap-3 bg-gray-50 dark:bg-gray-900/50">
          <button @click="modals.attachments = false" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-xl hover:bg-gray-50">إغلاق</button>
          <button @click="saveAttachmentsSchema" :disabled="saving" class="px-4 py-2 text-sm font-medium text-white bg-amber-600 rounded-xl hover:bg-amber-700 disabled:opacity-50 flex items-center gap-2">
            <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
            <span v-else>حفظ المرفقات</span>
          </button>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { Settings, Save, Loader2, Plus, LayoutTemplate, Trash2, FileText, GitMerge, ShieldCheck, X, PlusCircle, ShieldAlert, Paperclip, Lock } from 'lucide-vue-next'
import Swal from 'sweetalert2'
import api from '@/lib/api'

const loading = ref(true)
const saving = ref(false)
const services = ref<any[]>([])
const engineRules = ref<any[]>([])
const availableStages = ref<any[]>([])
const statuses = ref<any[]>([])

const selectedTab = ref('all')

const tabs = computed(() => [
  { id: 'all', label: 'الكل', count: services.value.length },
  { id: 'form', label: 'استمارات إثبات حالة', count: services.value.filter(s => s.service_type === 'form').length },
  { id: 'correction', label: 'طلبات تصحيح', count: services.value.filter(s => s.service_type === 'correction').length },
  { id: 'rank_settlement', label: 'ترقيات وتسويات', count: services.value.filter(s => s.service_type === 'rank_settlement').length },
  { id: 'disciplinary', label: 'إجراءات وجزاءات', count: services.value.filter(s => s.service_type === 'disciplinary').length },
  { id: 'security', label: 'أمان ومزامنة', count: services.value.filter(s => s.service_type === 'security').length }
])

const filteredServices = computed(() => {
  if (selectedTab.value === 'all') return services.value
  return services.value.filter(s => s.service_type === selectedTab.value)
})

const commonAttachmentsList = [
  'بطاقة وطنية - الوجهين معاً (ملف واحد)', 'بطاقة وطنية - أمامي', 'بطاقة وطنية - خلفي', 'بطاقة وطنية - ماسح ضوئي',
  'بطاقة عسكرية - الوجهين معاً (ملف واحد)', 'بطاقة عسكرية - أمامي', 'بطاقة عسكرية - خلفي', 'قرار ترقية',
  'قرار تسوية فرد→ضابط', 'أمر نقل', 'قرار تصحيح اسم', 'قرار تغيير حالة خدمية',
  'طلب إجازة', 'القرار الطبي الأصل', 'إجازة مرضية', 'شهادة الوفاة',
  'حكم انحصار الورثة', 'وكالة شرعية', 'حكم التنصيب', 'حكم شرعي بالفقدان',
  'إعلان الجريدة (لإثبات النشر عن فقدان الفرد)', 'بلاغ الفقدان', 
  'بلاغ العمليات (لإثبات واقعة الاستشهاد ميدانياً)', 'استمارة إثبات حالة (شهيد)',
  'الطلب الشخصي المقدم من المذكور', 'صورة البطاقة الشخصية للوكيل', 'صورة حديثة للمريض',
  'نسخة من الحكم (في حال صدوره)', 'مذكرة توضح بأن الفرد لا زال في السجن من النيابة',
  'نسخة من الأمر الصادر بالتكليف / المهمة', 'نسخة من الأمر الصادر بالتفرغ الدراسي',
  'نسخة من الأمر الصادر بالانتداب', 'مذكرة توضيحية / إرسال', 'خطاب رسمي',
  'شهادة', 'صورة شخصية', 'مذكرة رسمية بطلب تصحيح الرقم العسكري', 'مذكرة رسمية بطلب التبديل', 'أخرى'
]

const modals = ref({
  create: false,
  fields: false,
  workflow: false,
  prereqs: false,
  attachments: false
})

const activeService = ref<any>({})
const sections = ref<any[]>([])
const registryAutoSections = ref<any[]>([])
const workflowSteps = ref<any[]>([])
const prerequisites = ref<any[]>([])
const attachments = ref<any[]>([])
const hasCoreSections = computed(() => sections.value.some(s => s.title.includes('البيانات الشخصية') || s.title.includes('بيانات الميلاد')))

// Available linked data sources for select fields
const linkedDataSources: Record<string, string> = {
  '': 'خيارات يدوية (مفصولة بفاصلة)',
  'ranks': 'الرتب العسكرية (من النظام)',
  'statuses': 'الحالات الخدمية (من النظام)',
  'units': 'الوحدات / التشكيلات',
  'governorates': 'المحافظات',
  'settlement_types': 'أنواع التسويات',
}

const personnelFields = ref<any[]>([
  { key: 'full_name', label: 'الاسم الرباعي (من السجل)', type: 'text' },
  { key: 'military_number', label: 'الرقم العسكري', type: 'text' },
  { key: 'national_id', label: 'الرقم الوطني', type: 'text' },
  { key: 'current_rank', label: 'الرتبة الحالية', type: 'text' },
  { key: 'current_status', label: 'الحالة الحالية', type: 'text' },
  { key: 'birth_date', label: 'تاريخ الميلاد', type: 'date' },
  { key: 'blood_type', label: 'فصيلة الدم', type: 'text' },
  { key: 'governorate', label: 'المحافظة', type: 'text' },
  { key: 'district', label: 'المديرية', type: 'text' },
  { key: 'unit', label: 'الوحدة / التشكيل', type: 'text' },
  { key: 'join_date', label: 'تاريخ التجنيد', type: 'date' },
])

// Common system/fixed fields reference
const systemFields = ref([
  { key: 'category', label: 'الفئة', type: 'text', default: '' },
  { key: 'settlement_type', label: 'نوع التسوية', type: 'text', default: '' },
  { key: 'service_type', label: 'نوع الخدمة', type: 'text', default: '' },
  { key: 'status_type', label: 'نوع الحالة', type: 'text', default: '' },
  { key: 'form_type', label: 'نوع الاستمارة', type: 'text', default: '' },
])

// Quick-add a personnel_master (DB) field to the first user_input section
function quickAddDbField(pf: any) {
  let targetSection = sections.value.find((s: any) => s.source !== 'personnel_master')
  if (!targetSection) {
    sections.value.push({ title: 'بيانات الحالة', source: 'user_input', fields: [] })
    targetSection = sections.value[sections.value.length - 1]
  }
  targetSection.fields.push({
    key: pf.key,
    label: pf.label,
    type: pf.type || 'text',
    source: 'personnel_master',
    required: false,
    disabled: true,
    default: '',
    optionsStr: ''
  })
}

// Quick-add a system-fixed field to the first user_input section
function quickAddSystemField(sf: any) {
  let targetSection = sections.value.find((s: any) => s.source !== 'personnel_master')
  if (!targetSection) {
    sections.value.push({ title: 'بيانات الحالة', source: 'user_input', fields: [] })
    targetSection = sections.value[sections.value.length - 1]
  }
  targetSection.fields.push({
    key: sf.key,
    label: sf.label,
    type: sf.type || 'text',
    source: 'system',
    required: true,
    disabled: true,
    default: sf.default || '',
    optionsStr: ''
  })
}

// --- Initialization ---
onMounted(async () => {
  await fetchData()
  await fetchStatuses()
})

async function fetchStatuses() {
  try {
    const res = await api.get('/dictionaries/statuses/')
    statuses.value = res.data.results || res.data
  } catch (err) {
    console.error('Failed to fetch statuses', err)
  }
}

async function fetchData() {
  loading.value = true
  try {
    const sRes = await api.get('/service-cycle/catalog/')
    services.value = sRes.data.results || sRes.data

    const wRes = await api.get('/service-cycle/workflow-stages/')
    availableStages.value = wRes.data.results || wRes.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

// --- 1. Basic Service ---
function openCreateModal() {
  activeService.value = { 
    name_ar: '', 
    code: '', 
    category: 'military', 
    is_active: true,
    description: '',
    icon: 'FileText',
    execution_action: 'UPDATE_STATUS',
    approval_type: 'internal',
    service_type: 'form',
    target_audience: 'الكل',
    expected_duration_hours: 48,
    requires_approval: true,
    is_repeatable: true,
    execution_config: {}
  }
  modals.value.create = true
}

function openEditModal(svc: any) {
  activeService.value = { 
    ...svc,
    execution_config: svc.execution_config || {}
  }
  modals.value.create = true
}

async function saveBasicService() {
  if (!activeService.value.name_ar || !activeService.value.code) {
    return Swal.fire({ icon: 'error', text: 'يرجى إدخال اسم وكود الخدمة' })
  }
  
  saving.value = true
  try {
    const payload = {
      ...activeService.value,
      form_type: activeService.value.code // Map to form_type internally
    }
    
    if (activeService.value.id) {
      await api.put(`/service-cycle/catalog/${activeService.value.id}/`, payload)
    } else {
      await api.post('/service-cycle/catalog/', payload)
    }
    
    modals.value.create = false
    await fetchData()
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم الحفظ بنجاح', showConfirmButton: false, timer: 1500 })
  } catch (err) {
    console.error(err)
  } finally {
    saving.value = false
  }
}

// --- 2. Fields Builder ---
async function openFieldsModal(svc: any) {
  activeService.value = { ...svc, _is_registry_managed: false }
  sections.value = []
  registryAutoSections.value = []
  loading.value = true

  try {
    if (svc.form_type) {
      const res = await api.get(`/service-cycle/forms/schema/?type=${svc.form_type}`)
      const schema = res.data?.data
      if (schema && schema.sections && schema.sections.length > 0) {
        // Store auto sections for reference display ONLY for standard forms
        const isStandardForm = !['rank_demotion', 'rank_promotion', 'personnel_to_officer'].includes(svc.form_type)
        
        if (isStandardForm) {
          registryAutoSections.value = schema.sections
            .filter((s: any) => s.source === 'auto')
            .map((s: any) => ({
              title: s.title,
              fields: (s.fields || []).map((f: any) => ({ key: f.key, label: f.label, type: f.type }))
            }))
        } else {
          registryAutoSections.value = []
        }

        // Load ALL user_input section fields with correct source
        const userSections = schema.sections.filter((s: any) => s.source === 'user_input' || !s.source)
        if (userSections.length > 0) {
          sections.value = userSections.map((s: any) => {
            let sectionTitle = s.title || 'بيانات الحالة'
            // Clean up the "ثالثاً:" prefix for non-form services
            if (!isStandardForm) {
              if (sectionTitle.includes('ثالثاً:')) {
                sectionTitle = sectionTitle.replace('ثالثاً:', '').trim()
              }
              if (sectionTitle === 'بيانات الحالة') {
                sectionTitle = 'بيانات الطلب / القرار'
              }
            }

            return {
              title: sectionTitle,
              source: 'user_input',
              fields: (s.fields || []).map((f: any) => {
              let src = f.source || 'user_input'
              const defaultVal = f.default || f.value || ''
              if (f.type === 'auto') src = 'personnel_master'
              else if (f.disabled && defaultVal) src = 'system'

              // Detect linked data source for select fields
              let optionsSrc = f.options_source || ''
              if (f.key === 'to_rank' && f.type === 'select') optionsSrc = 'ranks'
              if (f.key === 'settlement_type' && f.type === 'select') optionsSrc = 'settlement_types'

              return {
                key: f.key,
                label: f.label,
                type: f.type === 'auto' ? 'text' : f.type,
                source: src,
                required: f.required ?? true,
                disabled: f.disabled ?? false,
                default: defaultVal,
                options_source: optionsSrc,
                optionsStr: (!optionsSrc && f.options) ? (f.options.map((o: any) => typeof o === 'object' ? o.label || o.value : o).join(', ')) : ''
              }
            })
            }
          })
          modals.value.fields = true
          loading.value = false
          return
        }
      }
    }

    // Fallback
    sections.value = [{ title: 'ثالثاً: بيانات الحالة', source: 'user_input', fields: [] }]
  } catch (err) {
    console.error('Failed to load schema from API, using empty default', err)
    sections.value = [{ title: 'ثالثاً: بيانات الحالة', source: 'user_input', fields: [] }]
  } finally {
    loading.value = false
  }

  modals.value.fields = true
}

function unlockCoreSections() {
  sections.value.unshift(
    {
      title: 'أولاً: البيانات الشخصية',
      fields: [
        { key: 'military_number', label: 'الرقم العسكري', type: 'text', source: 'personnel_master', required: true, disabled: true },
        { key: 'full_name', label: 'الاسم الرباعي', type: 'text', source: 'personnel_master', required: true, disabled: true },
        { key: 'current_rank', label: 'الرتبة', type: 'text', source: 'personnel_master', required: false, disabled: true },
        { key: 'unit', label: 'الوحدة', type: 'text', source: 'personnel_master', required: false, disabled: true },
      ]
    },
    {
      title: 'ثانياً: بيانات الميلاد والإقامة',
      fields: [
        { key: 'national_id', label: 'الرقم الوطني', type: 'text', source: 'personnel_master', required: true, disabled: true },
        { key: 'birth_date', label: 'تاريخ الميلاد', type: 'date', source: 'personnel_master', required: true, disabled: true },
        { key: 'governorate', label: 'محافظة الإقامة', type: 'text', source: 'personnel_master', required: false, disabled: true },
      ]
    }
  )
}

function onDbFieldSelected(field: any) {
  const pf = personnelFields.value.find(p => p.key === field.key)
  if (pf) {
    field.label = pf.label
    field.type = 'auto' // Force DB fields to auto (read-only)
    field.required = false
    field.disabled = true
  }
}

function addSection() {
  sections.value.push({ title: 'قسم جديد', fields: [] })
}

function removeSection(idx: number) { sections.value.splice(idx, 1) }

function addFieldToSection(sIdx: number) {
  sections.value[sIdx].fields.push({
    label: 'حقل جديد',
    key: `field_${Date.now()}`,
    type: 'text',
    source: 'user_input',
    required: false,
    disabled: false,
    optionsStr: '',
    default: ''
  })
}

function removeFieldFromSection(sIdx: number, fIdx: number) {
  sections.value[sIdx].fields.splice(fIdx, 1)
}

async function saveFieldsSchema() {
  saving.value = true
  try {
    // Build auto sections from registry reference
    const autoSections = registryAutoSections.value.map((s: any) => ({
      title: s.title,
      source: 'auto',
      fields: s.fields.map((f: any) => ({
        key: f.key, label: f.label, type: f.type || 'auto',
        required: false, disabled: true
      }))
    }))

    // Build user sections with full metadata
    const userSections = sections.value.map(s => ({
      title: s.title,
      source: s.source || 'user_input',
      fields: s.fields.map((f: any) => {
        const fieldData: any = {
          key: f.key, label: f.label, type: f.type,
          source: f.source || 'user_input',
          required: !!f.required, disabled: !!f.disabled
        }
        if (f.default) fieldData.default = f.default
        if (f.options_source) fieldData.options_source = f.options_source
        if (f.type === 'select' && f.optionsStr && !f.options_source) {
          fieldData.options = f.optionsStr.split(',').map((opt: string) => opt.trim()).filter(Boolean)
        }
        return fieldData
      })
    }))

    const finalSchema = {
      label: `استمارة ${activeService.value.name_ar}`,
      form_type: activeService.value.form_type || activeService.value.code,
      sections: [...autoSections, ...userSections]
    }

    await api.patch(`/service-cycle/catalog/${activeService.value.id}/`, { fields_schema: finalSchema })
    modals.value.fields = false
    await fetchData()
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم حفظ الحقول', showConfirmButton: false, timer: 1500 })
  } catch (err) {
    console.error(err)
  } finally {
    saving.value = false
  }
}

// --- 3. Workflow Builder ---
async function openWorkflowModal(svc: any) {
  activeService.value = { ...svc }
  loading.value = true
  try {
    const wRes = await api.get(`/service-cycle/workflow-steps/?service_id=${svc.id}`)
    workflowSteps.value = (wRes.data.results || wRes.data).sort((a: any, b: any) => a.order - b.order)
    modals.value.workflow = true
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

function getStageName(stageId: number) {
  const st = availableStages.value.find(s => s.id === stageId)
  return st ? st.name_ar : 'مرحلة'
}

function addWorkflowStep(stage: any) {
  workflowSteps.value.push({
    service: activeService.value.id,
    stage: stage.id,
    stage_details: stage,
    order: workflowSteps.value.length + 1,
    description: `مراجعة واعتماد ${stage.name_ar}`,
    is_final_step: false,
    requires_approval: true
  })
}

async function createNewStage() {
  const { value: formValues } = await Swal.fire({
    title: 'إضافة مرحلة عمل جديدة',
    html:
      '<div class="space-y-4 mt-2 text-start">' +
      '<div><label class="block text-xs font-bold text-gray-500 mb-1">اسم المرحلة (عربي)</label>' +
      '<input id="swal-input1" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all" placeholder="مثال: مكتب الأمن"></div>' +
      '<div><label class="block text-xs font-bold text-gray-500 mb-1">الكود البرمجي (إنجليزي)</label>' +
      '<input id="swal-input2" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all" placeholder="مثال: SECURITY"></div>' +
      '</div>',
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: 'إضافة',
    cancelButtonText: 'إلغاء',
    customClass: {
      confirmButton: 'bg-indigo-600 text-white px-4 py-2 rounded-lg ml-2',
      cancelButton: 'bg-gray-200 text-gray-800 px-4 py-2 rounded-lg'
    },
    buttonsStyling: false,
    preConfirm: () => {
      const name = (document.getElementById('swal-input1') as HTMLInputElement).value
      const code = (document.getElementById('swal-input2') as HTMLInputElement).value
      if (!name || !code) {
        Swal.showValidationMessage('الرجاء إدخال اسم وكود المرحلة')
      }
      return { name_ar: name, code: code, name_en: name }
    }
  })

  if (formValues) {
    try {
      saving.value = true
      const res = await api.post('/service-cycle/workflow-stages/', formValues)
      availableStages.value.push(res.data)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم إضافة المرحلة للقائمة', showConfirmButton: false, timer: 1500 })
    } catch (err: any) {
      console.error(err)
      Swal.fire('خطأ', 'حدث خطأ، قد يكون الكود موجود مسبقاً', 'error')
    } finally {
      saving.value = false
    }
  }
}

function removeWorkflowStep(idx: number) {
  workflowSteps.value.splice(idx, 1)
  workflowSteps.value.forEach((step, i) => step.order = i + 1)
}

function ensureOnlyOneFinal(index: number) {
  if (workflowSteps.value[index].is_final_step) {
    workflowSteps.value.forEach((step, idx) => {
      if (idx !== index) step.is_final_step = false
    })
  }
}

async function saveWorkflowSteps() {
  saving.value = true
  try {
    for (let i = 0; i < workflowSteps.value.length; i++) {
      const step = workflowSteps.value[i]
      const payload = {
        service: activeService.value.id,
        stage: step.stage,
        order: i + 1,
        description: step.description,
        is_final_step: step.is_final_step,
        requires_approval: step.requires_approval
      }
      
      if (step.id) {
        await api.put(`/service-cycle/workflow-steps/${step.id}/`, payload)
      } else {
        await api.post('/service-cycle/workflow-steps/', payload)
      }
    }
    
    modals.value.workflow = false
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم حفظ المسار', showConfirmButton: false, timer: 1500 })
  } catch (err) {
    console.error(err)
  } finally {
    saving.value = false
  }
}

// --- 4. Prerequisites ---
async function openPrereqsModal(svc: any) {
  activeService.value = { ...svc }
  loading.value = true
  try {
    const pRes = await api.get(`/service-cycle/prerequisites/?service_id=${svc.id}`)
    prerequisites.value = (pRes.data.results || pRes.data).sort((a: any, b: any) => a.order - b.order)
    
    // Fetch Engine Rules for this specific service
    engineRules.value = []
    try {
      const eRes = await api.get(`/service-cycle/catalog/${svc.id}/engine_rules/`)
      engineRules.value = eRes.data || []
    } catch (e) {
      console.warn("Could not fetch engine rules", e)
    }

    modals.value.prereqs = true
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

// تبديل حالة قاعدة محرك
async function toggleEngineRule(rule: any) {
  const previousState = rule.is_active;
  rule.is_active = !previousState; // Optimistic UI update

  try {
    const res = await api.post(`/service-cycle/catalog/${activeService.value.id}/toggle_engine_rule/`, {
      rule_id: rule.id,
      is_active: rule.is_active
    });
    
    if (res.data.success) {
      // Show small toast for feedback
      Swal.fire({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        icon: rule.is_active ? 'success' : 'warning',
        title: rule.is_active ? 'تم تفعيل القاعدة' : 'تم إيقاف القاعدة',
        text: `تم ${rule.is_active ? 'تفعيل' : 'إيقاف'} "${rule.name}" بنجاح.`
      });
    }
  } catch (error) {
    console.error("Failed to toggle rule:", error);
    rule.is_active = previousState; // Revert on failure
    Swal.fire('خطأ', 'تعذر تغيير حالة القاعدة، تأكد من اتصالك بالخادم.', 'error');
  }
}

function addPrerequisite() {
  prerequisites.value.push({
    service: activeService.value.id,
    name_ar: '',
    description: '',
    validation_type: 'age_min',
    validation_value: '',
    is_mandatory: true,
    order: prerequisites.value.length + 1
  })
}

function removePrerequisite(idx: number) {
  prerequisites.value.splice(idx, 1)
  prerequisites.value.forEach((p, i) => p.order = i + 1)
}

async function savePrerequisites() {
  const invalid = prerequisites.value.find(p => !p.name_ar || !p.validation_value)
  if (invalid) {
    return Swal.fire({ icon: 'error', text: 'يرجى إدخال اسم الشرط والقيمة لجميع الشروط المضافة' })
  }
  
  saving.value = true
  try {
    // Basic bulk creation logic (real logic should delete removed items, but for now we create/update)
    for (let i = 0; i < prerequisites.value.length; i++) {
      const p = prerequisites.value[i]
      const payload = {
        service: activeService.value.id,
        name_ar: p.name_ar,
        description: p.description,
        validation_type: p.validation_type,
        validation_value: p.validation_value,
        is_mandatory: p.is_mandatory,
        order: i + 1
      }
      
      if (p.id) {
        await api.put(`/service-cycle/prerequisites/${p.id}/`, payload)
      } else {
        await api.post('/service-cycle/prerequisites/', payload)
      }
    }
    
    modals.value.prereqs = false
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم حفظ الشروط المسبقة بنجاح', showConfirmButton: false, timer: 1500 })
  } catch (err) {
    console.error(err)
    Swal.fire('خطأ', 'يرجى تعبئة جميع الحقول وإدخال قيم صحيحة', 'error')
  } finally {
    saving.value = false
  }
}

// --- 5. Attachments Builder ---
async function openAttachmentsModal(svc: any) {
  activeService.value = { ...svc }
  attachments.value = Array.isArray(svc.attachments_schema) && svc.attachments_schema.length > 0 
    ? [...svc.attachments_schema] 
    : []
  
  if (attachments.value.length === 0 && svc.form_type) {
    loading.value = true
    try {
      const res = await api.get(`/service-cycle/forms/schema/?type=${svc.form_type}`)
      const schema = res.data?.data
      if (schema && schema.attachments) {
        attachments.value = schema.attachments.map((a:any) => ({
          key: a.doc_type || a.key,
          label: a.label,
          required: a.required !== false, // default true
          description: a.description || ''
        }))
      }
    } catch (err) {
      console.error('Failed to load attachments schema', err)
    } finally {
      loading.value = false
    }
  }
  
  modals.value.attachments = true
}

function addAttachment() {
  attachments.value.push({
    key: `attach_${attachments.value.length + 1}`,
    label: '',
    required: true,
    description: '',
    showDropdown: false
  })
}

function hideDropdown(att: any) {
  setTimeout(() => {
    att.showDropdown = false
  }, 200)
}

function selectAttachment(att: any, item: string) {
  att.label = item
  att.showDropdown = false
}

function removeAttachment(index: number) { attachments.value.splice(index, 1) }

async function saveAttachmentsSchema() {
  saving.value = true
  try {
    const finalAttachments = attachments.value.map(a => ({
      key: a.key,
      label: a.label,
      required: !!a.required,
      description: a.description || ''
    }))

    await api.patch(`/service-cycle/catalog/${activeService.value.id}/`, { attachments_schema: finalAttachments, attachments_count: finalAttachments.length })
    modals.value.attachments = false
    await fetchData()
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم حفظ المرفقات', showConfirmButton: false, timer: 1500 })
  } catch (err) {
    console.error(err)
  } finally {
    saving.value = false
  }
}
</script>
