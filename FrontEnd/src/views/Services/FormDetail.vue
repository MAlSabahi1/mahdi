<template>
  <admin-layout>
    <!-- Header Section -->
    <div class="print:hidden mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <PageBreadcrumb :pageTitle="'تفاصيل المعاملة رقم ' + (form?.id || '')" />
      
      <!-- Action Buttons -->
      <div v-if="form && canApprove" class="flex flex-wrap gap-2">
        <button v-if="canApprove" @click="rejectForm" class="bg-white text-red-600 hover:bg-red-50 border border-red-200 dark:bg-gray-900 dark:border-red-900/50 dark:hover:bg-red-950/30 font-bold px-4 py-2 rounded-lg transition-all text-xs shadow-sm">
          رفض
        </button>
        <button v-if="canApprove" @click="returnFormModal" class="bg-white text-amber-600 hover:bg-amber-50 border border-amber-200 dark:bg-gray-900 dark:border-amber-900/50 dark:hover:bg-amber-950/30 font-bold px-4 py-2 rounded-lg transition-all text-xs shadow-sm flex items-center gap-2">
          إرجاع للتعديل
        </button>
        <button v-if="canApprove" @click="approveForm()" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2 rounded-lg transition-all shadow-md shadow-emerald-500/20 text-xs flex items-center gap-2">
          اعتماد الطلب
        </button>
        <button v-if="form && form.status === 'draft'" @click="submitDraft" class="bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-2 rounded-lg transition-all shadow-md shadow-blue-500/20 text-xs flex items-center gap-2">
          تقديم الطلب النهائي
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col justify-center items-center py-32 print:hidden">
      <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-brand-600 mb-4"></div>
      <p class="text-gray-500 text-sm font-medium">جاري تحميل تفاصيل المعاملة...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error || !form" class="bg-red-50 border border-red-100 text-red-600 p-8 rounded-2xl text-center font-bold print:hidden shadow-sm">
      <svg class="w-12 h-12 mx-auto text-red-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
      {{ error || 'لم يتم العثور على تفاصيل هذه المعاملة.' }}
      <div class="mt-6">
        <RouterLink to="/services/transactions" class="text-brand-600 hover:text-brand-700 underline text-sm transition-colors">العودة لمركز المعاملات</RouterLink>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else class="space-y-6 text-start" dir="rtl">
      
      <!-- Official Document Header -->
      <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl shadow-sm overflow-hidden print:border-none print:shadow-none print:bg-transparent">
        <div class="border-b border-gray-100 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-900/50 px-6 py-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div class="flex items-center gap-4">
            <div class="h-12 w-12 bg-brand-50 dark:bg-brand-900/30 rounded-lg flex items-center justify-center border border-brand-100 dark:border-brand-800">
              <svg class="w-6 h-6 text-brand-600 dark:text-brand-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            </div>
            <div>
              <h1 class="text-xl font-black text-gray-900 dark:text-white leading-tight">
                {{ (form.form_type_display || form.form_type || '').replace('returned_to_service', 'عائد للخدمة') }}
              </h1>
              <div class="flex items-center gap-3 mt-1.5 text-xs text-gray-500 font-medium">
                <span class="flex items-center gap-1 font-mono text-gray-700 dark:text-gray-300">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14"/></svg>
                  TX-{{ form.id.toString().padStart(6, '0') }}
                </span>
                <span class="w-1 h-1 rounded-full bg-gray-300 dark:bg-gray-700"></span>
                <span class="flex items-center gap-1 font-mono">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                  {{ new Date(form.submitted_at || form.created_at).toLocaleString('en-GB') }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="flex items-center bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-1.5 shadow-sm">
            <span :class="getStatusDot(form.status)" class="h-2 w-2 rounded-full ml-2"></span>
            <span :class="getStatusTextColor(form.status)" class="text-xs font-bold">{{ getStatusLabel(form.status, form.current_step_name) }}</span>
          </div>
        </div>

        <!-- Progress Steps (If available) -->
        <div v-if="form.all_steps && form.all_steps.length > 0" class="px-6 py-5 bg-white dark:bg-gray-900 print:hidden border-b border-gray-100 dark:border-gray-800">
          <div class="flex items-center w-full justify-between gap-1">
            <div v-for="(step, idx) in form.all_steps" :key="idx" class="flex-1 flex flex-col gap-2.5 relative">
              <div class="h-1.5 rounded-full w-full relative z-10 transition-colors"
                :class="[
                  idx < form.current_step_index ? 'bg-emerald-500' :
                  idx === form.current_step_index && form.status !== 'approved' && form.status !== 'rejected' ? 'bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.5)]' :
                  form.status === 'approved' ? 'bg-emerald-500' :
                  form.status === 'rejected' && idx === form.current_step_index ? 'bg-red-500' :
                  'bg-gray-100 dark:bg-gray-800'
                ]"></div>
              <div class="text-[10px] font-bold text-center transition-colors"
                :class="[
                  idx < form.current_step_index ? 'text-emerald-700 dark:text-emerald-500' :
                  idx === form.current_step_index && form.status !== 'approved' && form.status !== 'rejected' ? 'text-blue-700 dark:text-blue-500' :
                  form.status === 'approved' ? 'text-emerald-700 dark:text-emerald-500' :
                  form.status === 'rejected' && idx === form.current_step_index ? 'text-red-700 dark:text-red-500' :
                  'text-gray-400 dark:text-gray-500'
                ]">
                {{ step }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 print:block print:w-full">
        <!-- Main Content Column -->
        <div class="lg:col-span-2 space-y-6 print:w-full print:block">
          
          <!-- Personnel Details Box -->
          <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-6 shadow-sm">
            <div class="flex justify-between items-center mb-5 pb-3 border-b border-gray-100 dark:border-gray-800">
              <h2 class="text-sm font-black text-gray-900 dark:text-white flex items-center gap-2">
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                بيانات مقدم الطلب
              </h2>
              <RouterLink v-if="form.personnel?.military_number || form.personnel_military_number"
                :to="`/personnel/${form.personnel?.military_number || form.personnel_military_number}`"
                class="text-[11px] font-bold text-brand-600 bg-brand-50 hover:bg-brand-100 dark:bg-brand-900/20 dark:hover:bg-brand-900/40 px-3 py-1.5 rounded-md transition-colors flex items-center gap-1.5">
                عرض الملف الكامل
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
              </RouterLink>
            </div>
            
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-y-4 gap-x-8">
              <div class="flex flex-col sm:col-span-2 md:col-span-1">
                <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">الاسم الرباعي</span>
                <span class="text-sm font-bold text-gray-900 dark:text-gray-100">{{ form.personnel?.full_name || form.personnel_name || '—' }}</span>
              </div>
              <div class="flex flex-col">
                <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">الرقم العسكري</span>
                <span class="text-sm font-bold font-mono text-gray-900 dark:text-gray-100">{{ form.personnel?.military_number || form.personnel_military_number || '—' }}</span>
              </div>
              <div class="flex flex-col">
                <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">الرتبة الحالية</span>
                <span class="text-sm font-bold text-gray-900 dark:text-gray-100">{{ form.personnel?.rank || form.personnel_rank || form.personnel?.rank_name || form.personnel?.current_rank?.name || '—' }}</span>
              </div>
              <div class="flex flex-col">
                <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">المؤهل العلمي</span>
                <span class="text-sm font-bold text-gray-900 dark:text-gray-100">{{ form.personnel?.qualification_name || form.personnel?.qualification_detail?.name || '—' }}</span>
              </div>
              <div class="flex flex-col">
                <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">حالة النفقات</span>
                <span class="text-sm font-bold text-gray-900 dark:text-gray-100">{{ form.personnel?.expense_status_display || '—' }}</span>
              </div>
              <div class="flex flex-col">
                <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">تاريخ النفاذ</span>
                <span class="text-sm font-bold font-mono text-gray-900 dark:text-gray-100">{{ form.effective_date ? new Date(form.effective_date).toLocaleDateString('en-GB') : '—' }}</span>
              </div>
            </div>
          </div>

          <!-- Official Form Data -->
          <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-6 shadow-sm">
            <div class="mb-5 pb-3 border-b border-gray-100 dark:border-gray-800">
              <h2 class="text-sm font-black text-gray-900 dark:text-white flex items-center gap-2">
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
                تفاصيل الاستمارة
              </h2>
            </div>
            
            <div v-if="form.form_data && Object.keys(form.form_data).length > 0" class="overflow-hidden rounded-lg border border-gray-100 dark:border-gray-800">
              <table class="min-w-full text-right text-sm">
                <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
                  <tr v-for="(value, key, index) in filteredFormData" :key="key" 
                      :class="index % 2 === 0 ? 'bg-gray-50/50 dark:bg-gray-900/30' : 'bg-white dark:bg-gray-900'">
                    <td class="w-1/3 px-4 py-3 text-[11px] font-bold text-gray-500 align-top">
                      {{ translateField(key) }}
                    </td>
                    <td class="px-4 py-3 text-sm font-bold text-gray-900 dark:text-gray-100">
                      {{ value }}
                    </td>
                  </tr>
                </tbody>
              </table>
              <div v-if="Object.keys(filteredFormData).length === 0" class="p-6 text-center text-sm text-gray-500 bg-gray-50 dark:bg-gray-800/30">
                جميع الحقول فارغة في هذه الاستمارة.
              </div>
            </div>
            <div v-else class="text-sm text-gray-500 bg-gray-50 dark:bg-gray-800/30 p-6 rounded-lg text-center border border-gray-100 dark:border-gray-800">
              لا توجد حقول إضافية في هذه الاستمارة.
            </div>
            
            <!-- Notes & Rejection Alert -->
            <div v-if="form.notes || form.rejection_reason" class="mt-6 space-y-3">
              <div v-if="form.notes" class="p-4 bg-blue-50/50 dark:bg-blue-900/10 text-blue-900 dark:text-blue-100 rounded-lg text-sm border-l-4 border-blue-500">
                <p class="text-[10px] font-black uppercase tracking-wider mb-1 text-blue-600 dark:text-blue-400">ملاحظات الطلب الأساسية</p>
                <p class="font-medium">{{ form.notes }}</p>
              </div>
              <div v-if="form.rejection_reason" class="p-4 bg-red-50/50 dark:bg-red-900/10 text-red-900 dark:text-red-100 rounded-lg text-sm border-l-4 border-red-500">
                <p class="text-[10px] font-black uppercase tracking-wider mb-1 text-red-600 dark:text-red-400">سبب الرفض / الإرجاع</p>
                <p class="font-bold">{{ form.rejection_reason }}</p>
              </div>
            </div>
          </div>

          <!-- Attachments -->
          <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-6 shadow-sm">
            <div class="mb-5 pb-3 border-b border-gray-100 dark:border-gray-800">
              <h2 class="text-sm font-black text-gray-900 dark:text-white flex items-center gap-2">
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"/></svg>
                الوثائق المرفقة
              </h2>
            </div>
            
            <div v-if="form.attachments && form.attachments.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div v-for="att in form.attachments" :key="att.id" class="flex items-center justify-between p-3 border border-gray-100 dark:border-gray-700/50 rounded-lg bg-gray-50/50 dark:bg-gray-800/20 hover:bg-white dark:hover:bg-gray-800 hover:border-gray-300 dark:hover:border-gray-600 transition-colors group">
                <div class="flex items-center gap-3">
                  <div class="p-2 bg-gray-100 dark:bg-gray-700 text-gray-500 rounded-md group-hover:bg-brand-50 group-hover:text-brand-600 transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path v-if="att.file?.endsWith('.pdf')" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                      <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                    </svg>
                  </div>
                  <div>
                    <p class="text-xs font-bold text-gray-900 dark:text-white">{{ translateField(att.document_type || 'مستند مرفق') }}</p>
                    <p class="text-[9px] text-gray-400 font-mono mt-0.5">REF: {{ String(att.id).padStart(4, '0') }}</p>
                  </div>
                </div>
                <a :href="att.file" target="_blank" class="text-[10px] font-bold text-gray-600 hover:text-brand-600 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 px-3 py-1.5 rounded hover:border-brand-300 dark:hover:border-brand-700 transition-all shadow-sm">
                  عرض
                </a>
              </div>
            </div>
            <div v-else class="text-center py-8 text-sm text-gray-500 bg-gray-50 dark:bg-gray-800/30 rounded-lg border border-dashed border-gray-200 dark:border-gray-700">
              لا توجد مرفقات مرتبطة بهذه المعاملة.
            </div>
          </div>

          <ReportFooter />
        </div>

        <!-- Sidebar Column -->
        <div class="space-y-6 print:hidden">
          
          <!-- Event History Timeline -->
          <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-6 shadow-sm">
            <h2 class="text-sm font-black text-gray-900 dark:text-white mb-5 pb-3 border-b border-gray-100 dark:border-gray-800">
              سجل الحركات والأحداث
            </h2>
            
            <div class="relative pl-2 pr-4 space-y-6">
              <!-- Vertical Line -->
              <div class="absolute right-[11px] top-2 bottom-2 w-px bg-gray-200 dark:bg-gray-700"></div>

              <div v-for="event in timeline" :key="event.id" class="relative flex items-start gap-4 pr-5 text-right">
                <span :class="[
                  event.action === 'created' || event.action === 'submitted' ? 'bg-blue-500 ring-4 ring-blue-50 dark:ring-blue-900/20' :
                  event.action === 'approved' || event.action === 'checklist_checked' ? 'bg-emerald-500 ring-4 ring-emerald-50 dark:ring-emerald-900/20' :
                  event.action === 'rejected' ? 'bg-red-500 ring-4 ring-red-50 dark:ring-red-900/20' :
                  event.action === 'returned' ? 'bg-amber-500 ring-4 ring-amber-50 dark:ring-amber-900/20' : 'bg-gray-400 ring-4 ring-gray-50 dark:ring-gray-800'
                ]" class="absolute right-[-4px] top-1.5 h-3 w-3 rounded-full z-10"></span>
                
                <div class="w-full">
                  <div class="flex justify-between items-start mb-0.5">
                    <p class="text-xs font-bold text-gray-900 dark:text-gray-100">{{ event.action_display || event.action }}</p>
                    <span class="text-[9px] font-mono text-gray-400">{{ new Date(event.created_at).toLocaleDateString('en-GB') }}</span>
                  </div>
                  <p class="text-[10px] text-gray-500 mb-1.5">بواسطة: {{ event.performed_by_name || 'النظام التلقائي' }}</p>
                  
                  <div v-if="event.notes" class="text-[10px] text-gray-600 dark:text-gray-300 bg-gray-50 dark:bg-gray-800/50 p-2.5 rounded-lg border border-gray-100 dark:border-gray-700 leading-relaxed">
                    {{ event.notes }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Internal Chat / Notes -->
          <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-6 shadow-sm flex flex-col h-[400px]">
            <h2 class="text-sm font-black text-gray-900 dark:text-white mb-4 pb-3 border-b border-gray-100 dark:border-gray-800 flex items-center gap-2">
              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/></svg>
              المراسلات الداخلية
            </h2>
            
            <div class="flex-1 overflow-y-auto pr-2 custom-scrollbar space-y-3 mb-4">
              <div v-if="notes.length === 0" class="flex flex-col items-center justify-center h-full text-gray-400">
                <svg class="w-8 h-8 mb-2 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
                <span class="text-[10px]">لا توجد مراسلات أو ملاحظات حالياً</span>
              </div>
              <div v-for="note in notes" :key="note.id" class="bg-brand-50/50 dark:bg-brand-900/10 p-3 rounded-lg rounded-tr-none border border-brand-100/50 dark:border-brand-800/30">
                <div class="flex justify-between items-start mb-1.5">
                  <span class="text-[10px] font-black text-brand-700 dark:text-brand-400">{{ note.created_by_name }}</span>
                  <span class="text-[9px] text-gray-400 font-mono">{{ new Date(note.created_at).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }) }}</span>
                </div>
                <p class="text-xs text-gray-700 dark:text-gray-300 leading-relaxed">{{ note.content }}</p>
              </div>
            </div>
            
            <div class="relative">
              <input v-model="newNote" type="text" placeholder="اكتب رسالة للفريق هنا..." class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg pl-12 pr-4 py-2.5 text-xs focus:ring-1 focus:ring-brand-500 focus:border-brand-500 outline-none transition-shadow" @keyup.enter="submitNote" />
              <button @click="submitNote" :disabled="!newNote.trim()" class="absolute left-1.5 top-1.5 bottom-1.5 bg-brand-600 hover:bg-brand-700 disabled:opacity-50 disabled:hover:bg-brand-600 text-white px-3 rounded text-[10px] font-bold transition-colors cursor-pointer">
                إرسال
              </button>
            </div>
          </div>
          
          <!-- Checklist Section -->
          <div v-if="checklist.length > 0" class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-6 shadow-sm">
            <h2 class="text-sm font-black text-gray-900 dark:text-white mb-4 pb-3 border-b border-gray-100 dark:border-gray-800 flex items-center gap-2">
              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
              متطلبات المرحلة الحالية
            </h2>
            <div class="space-y-2">
              <label v-for="item in checklist" :key="item.id" class="flex items-start gap-3 p-2.5 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-colors border border-transparent hover:border-gray-100 dark:hover:border-gray-700 group">
                <div class="pt-0.5">
                  <input type="checkbox" :checked="item.is_checked" @change="toggleChecklist(item)" class="w-4 h-4 text-brand-600 rounded border-gray-300 focus:ring-brand-500 cursor-pointer" />
                </div>
                <span class="text-xs font-medium text-gray-700 dark:text-gray-300 select-none leading-tight" :class="{ 'line-through text-gray-400 dark:text-gray-500': item.is_checked }">
                  {{ item.title }}
                  <span v-if="item.is_required" class="text-red-500 mr-1 text-[10px]">*</span>
                </span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Print Only Attachments Section -->
    <div class="hidden print:block w-full" v-if="form?.attachments?.length">
      <div v-for="(att, idx) in form.attachments" :key="'print-att-'+att.id" style="page-break-before: always; padding-top: 2cm;">
        <h3 class="text-xl font-bold text-center mb-6 text-gray-900 border-b-2 border-gray-800 pb-2 inline-block">
          مرفق ({{ Number(idx) + 1 }}): {{ translateField(att.document_type || 'مستند') }}
        </h3>
        <div class="flex justify-center w-full">
          <img v-if="att.file && !att.file.endsWith('.pdf')" :src="att.file" class="max-w-full max-h-[25cm] border border-gray-400 p-2 shadow-sm" alt="Attachment">
          <div v-else class="text-center p-10 border-2 border-dashed border-gray-400">
            <p class="font-bold text-gray-800 text-lg">هذا المرفق بصيغة PDF</p>
            <p class="text-sm text-gray-600">يرجى طباعته بشكل مستقل من النظام.</p>
            <p class="text-xs mt-4 font-mono">{{ att.file }}</p>
          </div>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import ReportFooter from '@/components/reports/ReportFooter.vue'
import { useServicesStore } from '@/stores/services'
import { useAuthStore } from '@/stores/auth'
import api from '@/lib/api'

const route = useRoute()
const router = useRouter()
const servicesStore = useServicesStore()
const authStore = useAuthStore()

const id = route.params.id as string
const form = ref<any>(null)
const loading = ref(true)
const error = ref('')

const timeline = ref<any[]>([])
const notes = ref<any[]>([])
const checklist = ref<any[]>([])
const newNote = ref('')

// Dictionary to translate raw database keys to official Arabic terms
const fieldTranslations: Record<string, string> = {
  rank: 'الرتبة',
  unit: 'الوحدة / اللواء',
  company: 'السرية / الكتيبة',
  category: 'التصنيف',
  full_name: 'الاسم الكامل',
  'full name': 'الاسم الكامل',
  id_issuer: 'جهة إصدار الهوية',
  'id issuer': 'جهة إصدار الهوية',
  birth_place: 'محل الميلاد',
  'birth place': 'محل الميلاد',
  national_id: 'الرقم الوطني / الهوية',
  'national id': 'الرقم الوطني / الهوية',
  id_issue_date: 'تاريخ إصدار الهوية',
  'id issue date': 'تاريخ إصدار الهوية',
  martyrdom_date: 'تاريخ الاستشهاد',
  'martyrdom date': 'تاريخ الاستشهاد',
  martyrdom_cause: 'سبب الاستشهاد',
  'martyrdom cause': 'سبب الاستشهاد',
  military_number: 'الرقم العسكري',
  'military number': 'الرقم العسكري',
  current_residence: 'مقر السكن الحالي',
  'current residence': 'مقر السكن الحالي',
  martyrdom_location: 'مكان الاستشهاد / الجبهة',
  'martyrdom location': 'مكان الاستشهاد / الجبهة',
  occurrence_context: 'سياق الواقعة',
  'occurrence context': 'سياق الواقعة',
  assignment_order: 'أمر التكليف',
  operations_report: 'بلاغ العمليات',
  appointment_ruling: 'حكم تنصيب',
  attorney_id: 'هوية الوكيل',
  national_id_front: 'صورة الهوية الوطنية (وجه)',
  power_of_attorney: 'وكالة شرعية',
  heir_ruling: 'انحصار ورثة',
  death_certificate: 'شهادة وفاة'
}

function translateField(key: string) {
  const normalizedKey = String(key).toLowerCase()
  return fieldTranslations[normalizedKey] || String(key).replace(/_/g, ' ')
}

onMounted(async () => {
  if (!id) {
    error.value = 'رقم المعاملة مفقود.'
    loading.value = false
    return
  }
  await fetchFormDetails()
})

const canApprove = computed(() => {
  if (!form.value) return false
  const status = form.value.status
  if (status === 'approved' || status === 'rejected') return false
  const role = authStore.user?.authz_profile?.role_name || ''
  if (status === 'pending_services' && (role.includes('رئيس الخدمات') || authStore.isAdmin)) return true
  if (status === 'pending_hr' && (role.includes('مدير الموارد') || authStore.isAdmin)) return true
  if (status === 'pending_director' && (role.includes('المدير العام') || authStore.isAdmin)) return true
  if (status === 'in_progress' && authStore.isAdmin) return true
  return false
})

// Filter out empty form fields (null, undefined, "-", empty string)
const filteredFormData = computed(() => {
  if (!form.value?.form_data) return {}
  const filtered: Record<string, any> = {}
  for (const [key, value] of Object.entries(form.value.form_data)) {
    if (value !== null && value !== undefined && value !== '' && value !== '-') {
      filtered[key] = value
    }
  }
  return filtered
})

async function fetchFormDetails() {
  loading.value = true
  try {
    form.value = await servicesStore.fetchFormById(id)
    const [t, n, c] = await Promise.all([
      servicesStore.fetchFormTimeline(id),
      servicesStore.fetchFormNotes(id),
      servicesStore.fetchFormChecklist(id, form.value.status)
    ])
    timeline.value = t
    notes.value = n
    checklist.value = c
    
    if (route.query.print === 'true') {
      setTimeout(() => { window.print() }, 500)
    }
  } catch (err: any) {
    error.value = 'فشل جلب تفاصيل المعاملة. قد تكون محذوفة أو غير متوفرة.'
  } finally {
    loading.value = false
  }
}

async function submitNote() {
  if (!newNote.value.trim()) return
  try {
    const note = await servicesStore.addFormNote(id, newNote.value)
    notes.value.unshift(note) // Add to top for chat style
    newNote.value = ''
    timeline.value = await servicesStore.fetchFormTimeline(id)
  } catch (err: any) {
    Swal.fire({ toast: true, position: 'top-end', icon: 'error', title: 'فشل إرسال الرسالة', showConfirmButton: false, timer: 2000 })
  }
}

async function toggleChecklist(item: any) {
  try {
    item.is_checked = !item.is_checked
    await servicesStore.toggleChecklistItem(item.id, item.is_checked)
    timeline.value = await servicesStore.fetchFormTimeline(id)
  } catch (err: any) {
    item.is_checked = !item.is_checked
    Swal.fire({ toast: true, position: 'top-end', icon: 'error', title: 'فشل التحديث', showConfirmButton: false, timer: 2000 })
  }
}

async function approveForm(ministryDocId?: number) {
  if (!form.value) return

  if (ministryDocId) {
    try {
      await servicesStore.approveForm(form.value.id, { ministry_document_id: ministryDocId })
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم اعتماد المعاملة بنجاح', showConfirmButton: false, timer: 2000 })
      fetchFormDetails()
    } catch (err: any) {
      let errorMsg = err.response?.data?.error || 'حدث خطأ أثناء اعتماد المعاملة'
      Swal.fire({ icon: 'error', title: 'خطأ', text: errorMsg })
    }
    return
  }

  Swal.fire({
    title: 'تأكيد الاعتماد؟',
    text: `سيتم الاعتماد وتمرير المعاملة للمرحلة التالية. هل أنت متأكد؟`,
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'نعم، اعتمد المعاملة',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#059669', // emerald-600
    reverseButtons: true
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await servicesStore.approveForm(form.value.id)
        Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم اعتماد المعاملة بنجاح', showConfirmButton: false, timer: 2000 })
        fetchFormDetails()
      } catch (err: any) {
        let errorMsg = err.response?.data?.error || 'حدث خطأ أثناء اعتماد المعاملة'
        
        if (errorMsg.includes('يجب إرفاق مستند موافقة الوزارة') || errorMsg.includes('مستند موافقة')) {
          return promptMinistryDoc()
        }

        if (err.response?.data && typeof err.response.data === 'object' && !err.response.data.error) {
          errorMsg = Object.values(err.response.data).flat().join('\n')
        }
        Swal.fire({ icon: 'error', title: 'خطأ', text: errorMsg })
      }
    }
  })
}

async function promptMinistryDoc() {
  const result = await Swal.fire({
    title: 'تسجيل موافقة الوزارة',
    html: `<div class="text-right" dir="rtl"><p class="text-xs text-gray-600 mb-3">يجب إرفاق ملف القرار/المذكرة الوزارية.</p><input type="file" id="ministry-doc" class="block w-full text-xs" accept=".pdf,.png,.jpg,.jpeg"></div>`,
    icon: 'info', showCancelButton: true, confirmButtonText: 'رفع واعتماد', cancelButtonText: 'إلغاء', confirmButtonColor: '#10b981', showLoaderOnConfirm: true,
    preConfirm: async () => {
      const fileInput = document.getElementById('ministry-doc') as HTMLInputElement
      if (!fileInput?.files?.length) { Swal.showValidationMessage('يجب اختيار ملف'); return false }
      const fd = new FormData()
      fd.append('file', fileInput.files[0])
      fd.append('document_type', 'ministry_approval')
      try {
        const uploadRes = await api.post('/storage/upload/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
        const docId = uploadRes.data?.data?.id || uploadRes.data?.id
        if (!docId) throw new Error('فشل الحصول على معرّف المستند')
        return docId
      } catch (e: any) {
        Swal.showValidationMessage(e.response?.data?.error || 'حدث خطأ أثناء رفع الملف')
        return false
      }
    }
  })
  
  if (result.isConfirmed && result.value) {
     approveForm(result.value)
  }
}

async function submitDraft() {
  if (!form.value) return
  Swal.fire({
    title: 'تقديم الطلب',
    text: `هل أنت متأكد من تقديم هذا الطلب نهائياً وبدء دورة الاعتماد؟`,
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'نعم، قدم الطلب',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#2563eb', // blue-600
    reverseButtons: true
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await api.post(`/service-cycle/forms/${form.value.id}/submit/`)
        Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم تقديم الطلب بنجاح', showConfirmButton: false, timer: 2000 })
        fetchFormDetails()
      } catch (err: any) {
        Swal.fire({ icon: 'error', title: 'فشل التقديم', text: err.response?.data?.error || 'حدث خطأ أثناء التقديم' })
      }
    }
  })
}

async function rejectForm() {
  if (!form.value) return
  Swal.fire({
    title: 'رفض المعاملة نهائياً',
    text: `الرجاء كتابة سبب الرفض بوضوح:`,
    input: 'text',
    icon: 'error',
    showCancelButton: true,
    confirmButtonText: 'تأكيد الرفض',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#dc2626', // red-600
    reverseButtons: true,
    inputValidator: (val) => !val ? 'يجب إدخال سبب الرفض!' : undefined
  }).then(async (result) => {
    if (result.isConfirmed && result.value) {
      try {
        await servicesStore.rejectForm(form.value.id, result.value)
        Swal.fire({ toast: true, position: 'top-end', icon: 'warning', title: 'تم رفض المعاملة', showConfirmButton: false, timer: 2000 })
        fetchFormDetails()
      } catch (err: any) {
        let errorMsg = err.response?.data?.error || 'حدث خطأ أثناء الرفض'
        if (err.response?.data && typeof err.response.data === 'object' && !err.response.data.error) {
          errorMsg = Object.values(err.response.data).flat().join('\n')
        }
        Swal.fire({ icon: 'error', title: 'خطأ', text: errorMsg })
      }
    }
  })
}

async function returnFormModal() {
  if (!form.value) return
  const { value: formValues } = await Swal.fire({
    title: 'إرجاع المعاملة للتعديل',
    html:
      '<div class="text-right space-y-4">' +
      '<div><label class="block text-sm font-bold mb-1">سبب الإرجاع الرئيسي:</label>' +
      '<select id="swal-reason" class="w-full border border-gray-300 rounded-lg p-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none">' +
      '<option value="missing_attachments">نقص وثائق أو مرفقات داعمة</option>' +
      '<option value="incorrect_data">بيانات الاستمارة غير صحيحة أو متضاربة</option>' +
      '<option value="incomplete_form">متطلبات المعاملة غير مكتملة</option>' +
      '<option value="other">أسباب أخرى</option>' +
      '</select></div>' +
      '<div><label class="block text-sm font-bold mb-1">تفاصيل وملاحظات للمنشئ:</label>' +
      '<textarea id="swal-details" class="w-full border border-gray-300 rounded-lg p-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none h-24" placeholder="اكتب الملاحظات بدقة ليقوم المنشئ بتعديلها..."></textarea></div>' +
      '</div>',
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: 'إرجاع المعاملة',
    cancelButtonText: 'إلغاء',
    confirmButtonColor: '#d97706', // amber-600
    reverseButtons: true,
    preConfirm: () => {
      const details = (document.getElementById('swal-details') as HTMLTextAreaElement).value
      if (!details) {
        Swal.showValidationMessage('الرجاء كتابة تفاصيل الملاحظات')
      }
      return {
        reason: (document.getElementById('swal-reason') as HTMLSelectElement).value,
        details: details
      }
    }
  })

  if (formValues) {
    try {
      await servicesStore.returnForm(form.value.id, {
        reason: formValues.reason,
        details: formValues.details,
        to_status: 'returned'
      })
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'تم إرجاع المعاملة للتعديل', showConfirmButton: false, timer: 2000 })
      fetchFormDetails()
    } catch (err: any) {
      let errorMsg = err.response?.data?.error || 'حدث خطأ أثناء الإرجاع'
      if (err.response?.data && typeof err.response.data === 'object' && !err.response.data.error) {
        errorMsg = Object.values(err.response.data).flat().join('\n')
      }
      Swal.fire({ icon: 'error', title: 'خطأ', text: errorMsg })
    }
  }
}

function getStatusLabel(status: string, stepName?: string) {
  const map: Record<string, string> = {
    'draft': 'مسودة',
    'approved': 'معتمد نهائياً',
    'rejected': 'مرفوض',
    'returned': 'مُرجع للتعديل',
    'pending_services': 'قيد المراجعة: رئيس الخدمات',
    'pending_hr': 'قيد المراجعة: مدير الموارد',
    'pending_director': 'قيد المراجعة: المدير العام',
    'in_progress': `قيد المعالجة (${stepName || 'مرحلة حالية'})`,
  }
  return map[status] || status
}

function getStatusTextColor(status: string) {
  const colors: Record<string, string> = {
    'draft': 'text-gray-600 dark:text-gray-400',
    'pending_services': 'text-amber-600 dark:text-amber-400',
    'pending_hr': 'text-blue-600 dark:text-blue-400',
    'pending_director': 'text-purple-600 dark:text-purple-400',
    'in_progress': 'text-indigo-600 dark:text-indigo-400',
    'approved': 'text-emerald-600 dark:text-emerald-400',
    'rejected': 'text-red-600 dark:text-red-400',
    'returned': 'text-orange-600 dark:text-orange-400',
  }
  return colors[status] || 'text-gray-600'
}

function getStatusDot(status: string) {
  const dots: Record<string, string> = {
    'draft': 'bg-gray-400',
    'pending_services': 'bg-amber-500',
    'pending_hr': 'bg-blue-500',
    'pending_director': 'bg-purple-500',
    'in_progress': 'bg-indigo-500 shadow-[0_0_8px_rgba(99,102,241,0.6)]',
    'approved': 'bg-emerald-500',
    'rejected': 'bg-red-500',
    'returned': 'bg-orange-500',
  }
  return dots[status] || 'bg-gray-400'
}
</script>
