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
              <tr v-else-if="services.length === 0" class="border-b border-gray-100 dark:border-gray-800">
                <td colspan="4" class="px-6 py-10 text-center text-gray-400">
                  لا توجد خدمات مضافة حتى الآن.
                </td>
              </tr>
              <tr v-else v-for="svc in services" :key="svc.id" class="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50/50 dark:hover:bg-gray-800/20 transition-colors">
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
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">الإجراء التنفيذي</label>
              <select v-model="activeService.execution_action" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm outline-none">
                <option value="UPDATE_STATUS">تغيير الحالة (استمارات إثبات الحالة)</option>
                <option value="UPDATE_RANK">تحديث الرتبة (ترقيات)</option>
                <option value="SECURITY_RESTRICT">قيد أمني</option>
                <option value="NONE">للتوثيق فقط (لا يوجد تأثير)</option>
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
              <select v-model="activeService.service_type" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm outline-none">
                <option value="form">استمارة</option>
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
              <input type="text" v-model="activeService.target_audience" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none" placeholder="مثال: الكل، الضباط، الأفراد" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">المدة المتوقعة (بالساعات)</label>
              <input type="number" v-model="activeService.expected_duration_hours" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none" placeholder="مثال: 24" />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4 pt-2">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" v-model="activeService.requires_approval" class="w-4 h-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500" />
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">تتطلب موافقات</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" v-model="activeService.is_repeatable" class="w-4 h-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500" />
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">قابلة للتكرار (أكثر من مرة للفرد)</span>
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
          <div v-if="sections.length === 0" class="text-center py-10 border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-xl">
            <p class="text-gray-500">لم يتم إضافة أي أقسام لهذه الاستمارة.</p>
          </div>
          
          <div v-for="(section, sIdx) in sections" :key="sIdx" class="border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-800 overflow-hidden shadow-sm">
            <div class="bg-gray-100 dark:bg-gray-700/50 px-4 py-3 flex justify-between items-center border-b border-gray-300 dark:border-gray-600">
              <div class="flex items-center gap-3 w-2/3">
                <input type="text" v-model="section.title" placeholder="عنوان القسم (مثال: البيانات الشخصية)" class="w-1/2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg px-2 py-1 text-sm font-bold outline-none" />
                <select v-model="section.source" class="w-1/3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg px-2 py-1 text-sm outline-none">
                  <option value="personnel_master">قاعدة بيانات الأفراد (DB)</option>
                  <option value="user_input">إدخال مستخدم (User Input)</option>
                </select>
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
              <div v-if="section.fields.length === 0" class="text-center py-4 text-xs text-gray-400">لا توجد حقول في هذا القسم</div>
              
              <div v-for="(field, fIdx) in section.fields" :key="fIdx" class="p-3 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-900/50 relative group">
                <button @click="removeFieldFromSection(Number(sIdx), Number(fIdx))" class="absolute top-2 left-2 p-1 text-red-500 hover:bg-red-50 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity">
                  <Trash2 class="w-3 h-3" />
                </button>
                
                <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
                  <div class="col-span-1 md:col-span-2">
                    <label class="block text-[10px] font-bold text-gray-500 mb-1">اسم الحقل (يظهر للمستخدم)</label>
                    <input type="text" v-model="field.label" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-2 py-1 text-xs outline-none" />
                  </div>
                  
                  <div class="col-span-1">
                    <label class="block text-[10px] font-bold text-gray-500 mb-1">المفتاح (Key)</label>
                    <select v-if="section.source === 'personnel_master'" v-model="field.key" @change="onDbFieldSelected(field)" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-2 py-1 text-xs outline-none">
                      <option value="" disabled>اختر الحقل...</option>
                      <option v-for="pf in personnelFields" :key="pf.key" :value="pf.key">{{ pf.label }}</option>
                    </select>
                    <input v-else type="text" v-model="field.key" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-2 py-1 text-xs outline-none" />
                  </div>
                  
                  <div class="col-span-1">
                    <label class="block text-[10px] font-bold text-gray-500 mb-1">نوع الحقل</label>
                    <select v-model="field.type" :disabled="section.source === 'personnel_master'" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-2 py-1 text-xs outline-none disabled:opacity-50 disabled:cursor-not-allowed">
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
                    <label class="block text-[10px] font-bold text-gray-500 mb-1">الخيارات (مفصولة بفاصلة)</label>
                    <input type="text" v-model="field.optionsStr" placeholder="ذكر, أنثى" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-2 py-1 text-xs outline-none" />
                  </div>
                  <div :class="field.type === 'select' ? '' : 'col-span-2'">
                    <label class="block text-[10px] font-bold text-gray-500 mb-1">قيمة افتراضية (Default)</label>
                    <input type="text" v-model="field.default" placeholder="مثال: منتدب" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md px-2 py-1 text-xs outline-none" />
                  </div>
                </div>
              </div>
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
          <h3 class="font-bold text-gray-900 dark:text-white flex items-center gap-2">
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
          <div v-if="prerequisites.length === 0" class="text-center py-10 border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-xl">
            <ShieldAlert class="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <p class="text-gray-500 text-sm">لم يتم إضافة أي شروط لهذه الخدمة بعد.</p>
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
              <div class="col-span-1 md:col-span-2">
                <label class="block text-xs font-medium text-gray-500 mb-1">اسم المرفق (مثال: صورة البطاقة)</label>
                <input type="text" v-model="att.label" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-1.5 text-sm outline-none" />
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
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { Settings, Save, Loader2, Plus, LayoutTemplate, Trash2, FileText, GitMerge, ShieldCheck, X, PlusCircle, ShieldAlert, Paperclip } from 'lucide-vue-next'
import Swal from 'sweetalert2'
import api from '@/lib/api'

// --- State ---
const loading = ref(true)
const saving = ref(false)
const services = ref<any[]>([])
const availableStages = ref<any[]>([])

const modals = ref({
  create: false,
  fields: false,
  workflow: false,
  prereqs: false,
  attachments: false
})

const activeService = ref<any>({})
const sections = ref<any[]>([])
const workflowSteps = ref<any[]>([])
const prerequisites = ref<any[]>([])
const attachments = ref<any[]>([])
const personnelFields = ref<any[]>([])

// --- Initialization ---
onMounted(async () => {
  await fetchData()
})

async function fetchData() {
  loading.value = true
  try {
    const sRes = await api.get('/service-cycle/catalog/')
    services.value = sRes.data.results || sRes.data

    const wRes = await api.get('/service-cycle/workflow-stages/')
    availableStages.value = wRes.data.results || wRes.data

    if (personnelFields.value.length === 0) {
      const pfRes = await api.get('/personnel/schema/')
      if (pfRes.data?.success) {
        personnelFields.value = pfRes.data.data
      }
    }
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
    icon: 'FileText'
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
function openFieldsModal(svc: any) {
  activeService.value = { ...svc }
  sections.value = []
  
  if (svc.fields_schema && svc.fields_schema.sections && svc.fields_schema.sections.length > 0) {
    sections.value = svc.fields_schema.sections.map((s: any) => ({
      title: s.title || '',
      source: s.source || 'user_input',
      fields: (s.fields || []).map((f: any) => ({
        ...f,
        optionsStr: f.options ? f.options.join(', ') : ''
      }))
    }))
  } else {
    // Default sections for a new form
    sections.value = [
      {
        title: 'أولاً: البيانات الشخصية',
        source: 'personnel_master',
        fields: [
          { key: 'military_number', label: 'الرقم العسكري', type: 'auto', required: true, disabled: false },
          { key: 'full_name', label: 'الاسم الرباعي واللقب', type: 'auto', required: true, disabled: false },
          { key: 'rank', label: 'الرتبة', type: 'auto', required: false, disabled: false },
        ]
      },
      {
        title: 'ثانياً: بيانات الطلب',
        source: 'user_input',
        fields: []
      }
    ]
  }
  
  modals.value.fields = true
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
  sections.value.push({ title: 'قسم جديد', source: 'user_input', fields: [] })
}

function removeSection(idx: number) { sections.value.splice(idx, 1) }

function addFieldToSection(sIdx: number) {
  sections.value[sIdx].fields.push({ key: `field_${sections.value[sIdx].fields.length + 1}`, label: 'حقل جديد', type: 'text', required: false, disabled: false, optionsStr: '', default: '' })
}

function removeFieldFromSection(sIdx: number, fIdx: number) {
  sections.value[sIdx].fields.splice(fIdx, 1)
}

async function saveFieldsSchema() {
  saving.value = true
  try {
    const finalSections = sections.value.map(s => {
      return {
        title: s.title,
        source: s.source,
        fields: s.fields.map((f: any) => {
          const fieldData: any = { key: f.key, label: f.label, type: f.type, required: !!f.required, disabled: !!f.disabled }
          if (f.default) fieldData.default = f.default
          if (f.type === 'select' && f.optionsStr) {
            fieldData.options = f.optionsStr.split(',').map((opt: string) => opt.trim()).filter(Boolean)
          }
          return fieldData
        })
      }
    })

    const finalSchema = {
      label: `استمارة ${activeService.value.name_ar}`,
      sections: finalSections
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
    modals.value.prereqs = true
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
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
function openAttachmentsModal(svc: any) {
  activeService.value = { ...svc }
  attachments.value = Array.isArray(svc.attachments_schema) ? [...svc.attachments_schema] : []
  modals.value.attachments = true
}

function addAttachment() {
  attachments.value.push({ key: `attach_${attachments.value.length + 1}`, label: 'مرفق جديد', required: true, description: '' })
}

function removeAttachment(idx: number) { attachments.value.splice(idx, 1) }

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
