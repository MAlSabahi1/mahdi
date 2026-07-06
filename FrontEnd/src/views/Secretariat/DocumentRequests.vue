<template>
  <admin-layout>
    <div class="no-print">
      <PageBreadcrumb :pageTitle="$t('secretariat.office_work.title')" />
    </div>

    <div class="space-y-6">
      <!-- Tabs (Hidden on print) -->
      <div class="flex gap-2 p-1 bg-gray-100 dark:bg-gray-800 rounded-2xl w-fit no-print">
        <button
          v-for="t in ['writer', 'requests']"
          :key="t"
          @click="activeTab = t"
          :class="[
            'px-5 py-2 rounded-xl text-sm font-semibold transition cursor-pointer',
            activeTab === t
              ? 'bg-white dark:bg-gray-900 text-gray-900 dark:text-white shadow-theme-xs'
              : 'text-gray-500 hover:text-gray-900 dark:hover:text-white'
          ]"
        >
          {{ t === 'writer' ? 'صياغة وطباعة المذكرات الرسمية' : 'طلبات الطباعة والخدمات المكتبية' }}
        </button>
      </div>

      <!-- TAB 1: Memo Writer & Printer -->
      <div v-if="activeTab === 'writer'" class="grid grid-cols-1 xl:grid-cols-12 gap-6 items-start animate-fade-in">
        <!-- Form Editor (Hidden on print) -->
        <div class="xl:col-span-5 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-3xl p-6 shadow-theme-sm space-y-4 no-print">
          <div class="border-b border-gray-150 dark:border-gray-800 pb-3">
            <h3 class="text-base font-bold text-gray-900 dark:text-white">محرر الخطابات الرسمية</h3>
            <p class="text-xs text-gray-400 mt-1">اختر القالب واملأ البيانات للحصول على ترويسة رسمية مطابقة للمواصفات الحكومية</p>
          </div>

          <div class="space-y-4">
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1.5">نوع الوثيقة/النموذج *</label>
              <select v-model="memo.templateType" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm text-gray-900 dark:border-gray-750 dark:bg-gray-800 dark:text-white">
                <option value="memo">مذكرة رسمية (Memo)</option>
                <option value="circular">تعميم إداري (Circular)</option>
                <option value="decision">قرار إداري (Decision)</option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1.5">رقم المذكرة/المرجع *</label>
                <input v-model="memo.refNo" type="text" placeholder="مثال: أ ش/25/2026" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm text-gray-900 dark:bg-gray-800 dark:border-gray-700" />
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1.5">التاريخ *</label>
                <input v-model="memo.date" type="text" placeholder="مثال: 18 محرم 1448هـ" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm text-gray-900 dark:bg-gray-800 dark:border-gray-700" />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1.5">الموافق *</label>
                <input v-model="memo.gregorianDate" type="text" placeholder="مثال: 05 يوليو 2026م" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm text-gray-900 dark:bg-gray-800 dark:border-gray-700" />
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1.5">المرفقات</label>
                <input v-model="memo.attachments" type="text" placeholder="مثال: لا يوجد" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm text-gray-900 dark:bg-gray-800 dark:border-gray-700" />
              </div>
            </div>

            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1.5">الموجه إليه (المرسل إليه) *</label>
              <input v-model="memo.recipient" type="text" placeholder="الأخ/ مدير عام الشؤون المالية..." class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm text-gray-900 dark:bg-gray-800 dark:border-gray-700" />
            </div>

            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1.5">الموضوع *</label>
              <input v-model="memo.subject" type="text" placeholder="بشأن صرف عهدة مكتبية..." class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm text-gray-900 dark:bg-gray-800 dark:border-gray-700" />
            </div>

            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1.5">مضمون ونص الخطاب *</label>
              <textarea v-model="memo.body" rows="6" placeholder="اكتب هنا نص ومضمون الخطاب بالتفصيل..." class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm leading-relaxed text-gray-900 dark:bg-gray-800 dark:border-gray-700"></textarea>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1.5">اسم وتوقيع الموقع *</label>
                <input v-model="memo.signatoryName" type="text" placeholder="العميد/ أحمد علي سالم" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm text-gray-900 dark:bg-gray-800 dark:border-gray-700" />
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1.5">صفة الموقع *</label>
                <input v-model="memo.signatoryTitle" type="text" placeholder="مدير إدارة القوى البشرية" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm text-gray-900 dark:bg-gray-800 dark:border-gray-700" />
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-2 pt-4 border-t border-gray-150 dark:border-gray-800">
            <button
              @click="printMemo"
              class="w-full py-2.5 px-4 bg-brand-500 hover:bg-brand-600 text-white rounded-xl font-bold flex justify-center items-center gap-2 cursor-pointer transition shadow-theme-xs"
            >
              🖨️ طباعة الخطاب الرسمي
            </button>
            <button
              @click="saveAsCorrespondence"
              :disabled="savingCorrespondence"
              class="w-full py-2.5 px-4 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300 rounded-xl font-bold flex justify-center items-center gap-2 cursor-pointer transition disabled:opacity-50"
            >
              📥 حفظ كخطاب صادر في أرشيف المراسلات
            </button>
          </div>
        </div>

        <!-- Official Live Preview Sheet -->
        <div class="xl:col-span-7 bg-white dark:bg-gray-950 border border-gray-200 dark:border-gray-800 rounded-3xl p-6 shadow-theme-sm overflow-x-auto">
          <div class="no-print mb-4 flex justify-between items-center text-xs text-gray-500 border-b border-gray-100 dark:border-gray-800 pb-2">
            <span>المعاينة الرسمية (مطابق لأبعاد الورقة الرسمية A4)</span>
            <span class="text-brand-500 font-bold">جاهز للطباعة</span>
          </div>

          <!-- A4 Sheet Container -->
          <div class="print-preview-container mx-auto bg-white text-black p-6 border border-gray-300 shadow-lg rounded-md font-serif text-sm max-w-[800px] min-h-[1050px] flex flex-col justify-between" style="font-family: 'Amiri', 'Times New Roman', serif;">
            <!-- Inner Letterhead Border Wrapper -->
            <div class="border-2 border-double border-black pt-9 pb-7 px-8 flex flex-col justify-between flex-grow h-full">
              <!-- Header Section -->
              <div>
                <div class="flex justify-between items-end pb-2" dir="rtl" style="width: 100%; display: flex;">
                  <!-- Right Header: Calligraphy image followed by official titles (Aligned to the Right Edge) -->
                  <div class="flex flex-col items-start justify-end text-right" style="width: 30%; min-width: 30%; align-items: flex-start; font-family: 'Amiri', serif;">
                    <img :src="yemenCalligraphy" class="w-[145px] h-9 object-contain mb-1.5" alt="الجمهورية اليمنية" />
                    <p class="text-[13px] font-bold text-gray-900 leading-tight">وزارة الداخلية</p>
                    <p class="text-[13px] font-bold text-gray-900 leading-tight mt-1">شرطة م/ {{ userSecurityAdminName }}</p>
                    <p class="text-[11.5px] font-semibold text-gray-800 leading-tight mt-1">إدارة القوى البشرية</p>
                  </div>

                  <!-- Center: Basmala (Classical Naskh) & Colored Republican Eagle -->
                  <div class="flex flex-col items-center justify-center space-y-2 mt-1" style="width: 40%; min-width: 40%; text-align: center; align-self: center; align-items: center;">
                    <p class="basmala-text leading-none text-center w-full">بسم الله الرحمن الرحيم</p>
                    <img :src="yemenLogo" class="w-[110px] h-auto object-contain mx-auto mt-1" alt="شعار الجمهورية اليمنية" />
                  </div>

                  <!-- Left Header: Symmetrically aligned metadata container (Aligned to the Left Edge) -->
                  <div class="text-xs pb-1 flex flex-col items-end justify-end" style="width: 30%; min-width: 30%; align-items: flex-end; font-family: 'Amiri', serif;">
                    <div style="width: 145px; display: flex; flex-direction: column; gap: 5px;">
                      <div class="flex justify-between items-center w-full text-[12.5px] font-bold text-gray-900" style="display: flex; justify-content: space-between; align-items: center;">
                        <span>الرقــم:</span>
                        <span class="font-sans font-semibold text-[11.5px] text-left">{{ memo.refNo || '............' }}</span>
                      </div>
                      <div class="flex justify-between items-center w-full text-[12.5px] font-bold text-gray-900" style="display: flex; justify-content: space-between; align-items: center;">
                        <span>التاريخ:</span>
                        <span class="font-sans font-semibold text-[11.5px] text-left">{{ memo.date || '............' }}</span>
                      </div>
                      <div class="flex justify-between items-center w-full text-[12.5px] font-bold text-gray-900" style="display: flex; justify-content: space-between; align-items: center;">
                        <span>الموافق:</span>
                        <span class="font-sans font-semibold text-[11.5px] text-left">{{ memo.gregorianDate || '............' }}</span>
                      </div>
                      <div class="flex justify-between items-center w-full text-[12.5px] font-bold text-gray-900" style="display: flex; justify-content: space-between; align-items: center;">
                        <span>المرفقات:</span>
                        <span class="font-sans font-semibold text-[11.5px] text-left">{{ memo.attachments || 'لا يوجد' }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Thin solid divider -->
                <div class="border-b border-black mt-6 mb-7 opacity-85"></div>

                <!-- Document Title inside elegant centered layout -->
                <div class="text-center my-6">
                  <h2 class="text-[22px] font-bold tracking-wider text-gray-950 pb-1.5 px-6 inline-block" style="font-family: 'Amiri', serif; border-bottom: 2px solid black;">
                    {{ memo.templateType === 'memo' ? 'مـذكـــــرة رسميـــــة' : memo.templateType === 'circular' ? 'تـعـمـيـم إداري' : 'قــرار إداري' }}
                  </h2>
                </div>

                <!-- Recipient Line -->
                <div class="text-right text-[15.5px] font-bold my-5 space-y-2 pr-1" style="font-family: 'Amiri', serif;">
                  <p class="text-gray-950">
                    الأخ / 
                    <span class="px-2 pb-0.5 inline-block text-center" :style="memo.recipient ? 'border-bottom: 1.5px dotted black; min-width: 280px;' : 'min-width: 280px;'">
                      {{ memo.recipient || '..................................................' }}
                    </span> 
                    المحترم
                  </p>
                  <p class="pr-8 text-gray-900">تحية طيبة وبعد،،،</p>
                </div>

                <!-- Subject Line (Simple & Elegant Print-Compliant Style) -->
                <div class="text-right text-[15.5px] font-bold my-5 pr-1" style="font-family: 'Amiri', serif;">
                  <span class="text-gray-900 pr-1">الموضوع:</span>
                  <span class="font-bold text-gray-950 px-2 pb-0.5 inline-block text-center" :style="memo.subject ? 'border-bottom: 1.5px solid black; min-width: 350px;' : 'min-width: 350px;'">
                    {{ memo.subject || '.......................................................................' }}
                  </span>
                </div>

                <!-- Body Line -->
                <div class="text-right text-[16px] leading-[2.2] text-gray-950 whitespace-pre-wrap px-4 min-h-[380px] text-justify font-normal indent-8" style="font-family: 'Amiri', serif;">
                  {{ memo.body || 'يرجى كتابة نص المذكرة هنا ليتم عرضه كترويسة رسمية...' }}
                </div>
              </div>

              <!-- Bottom Section (Signatures & Copy lists) -->
              <div>
                <div class="grid grid-cols-2 mt-8 pb-4" dir="rtl">
                  <div></div>
                  <!-- Signature Area (Title first, signature space, then name) -->
                  <div class="text-center space-y-1 flex flex-col items-center" style="font-family: 'Amiri', serif;">
                    <p class="font-bold text-[15.5px] text-gray-950 leading-tight">
                      {{ memo.signatoryTitle || 'مدير إدارة القوى البشرية' }}
                    </p>
                    <div class="h-14"></div> <!-- Space for signing & stamping -->
                    <p class="font-bold text-[15px] text-gray-900 border-t border-dotted border-black/40 pt-1.5 px-4 inline-block min-w-[200px]">
                      {{ memo.signatoryName || '.....................................' }}
                    </p>
                    <p class="text-[11px] text-gray-400 italic mt-1 font-sans">(التوقيع والختم الرسمي)</p>
                  </div>
                </div>

                <!-- Circular template CC list (نسخة مع التحية) -->
                <div class="text-right text-[11.5px] text-gray-700 border-t border-gray-300 pt-3 mt-6 space-y-0.5" style="font-family: 'Amiri', serif;">
                  <p class="font-bold text-gray-900">نسخة مع التحية لـ:</p>
                  <p class="pr-2">- أرشيف السكرتارية العام</p>
                  <p class="pr-2">- ملف المتابعة والرقابة</p>
                </div>
              </div>
          </div>
          </div>
        </div>
      </div>

      <!-- TAB 2: Office work requests (printing/copying) -->
      <div v-if="activeTab === 'requests'" class="space-y-6 animate-fade-in no-print">
        <div class="flex justify-between items-center bg-white dark:bg-gray-900 p-5 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-theme-sm">
          <h3 class="text-base font-bold text-gray-900 dark:text-white">طلبات الطباعة والنسخ والمسح الضوئي</h3>
          <button
            @click="showAddModal = true"
            class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white hover:bg-brand-600 transition shadow-theme-xs cursor-pointer"
          >
            + تسجيل طلب مكتبي جديد
          </button>
        </div>

        <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
            <thead class="bg-gray-50 dark:bg-gray-800/50">
              <tr>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">الموضوع/العنوان</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">نوع الخدمة</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">عدد النسخ</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">عدد الصفحات</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">طالب الخدمة</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">الحالة</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">الإجراءات</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-800 bg-white dark:bg-gray-900">
              <tr v-if="loading" class="text-center py-6"><td colspan="7" class="py-6 text-sm text-gray-500">جاري التحميل...</td></tr>
              <tr v-else-if="requests.length === 0" class="text-center py-6"><td colspan="7" class="py-6 text-sm text-gray-500">لا توجد طلبات أعمال مكتبية معلقة.</td></tr>
              <tr v-else v-for="req in requests" :key="req.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/30 transition">
                <td class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white">{{ req.title }}</td>
                <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{{ req.type_display }}</td>
                <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 font-medium">{{ req.copies_count }}</td>
                <td class="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 font-medium">{{ req.pages_count }}</td>
                <td class="px-6 py-4 text-sm text-gray-900 dark:text-white font-medium">{{ req.requested_by_name }}</td>
                <td class="px-6 py-4 text-sm">
                  <span
                    :class="[
                      'px-2 py-0.5 rounded-full text-xxs font-semibold',
                      req.status === 'completed' ? 'bg-green-50 text-green-700 dark:bg-green-900/30' :
                      req.status === 'in_progress' ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/30' :
                      req.status === 'cancelled' ? 'bg-gray-100 text-gray-700' :
                      'bg-amber-50 text-amber-700 dark:bg-amber-900/30'
                    ]"
                  >
                    {{ req.status_display }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm flex gap-2">
                  <template v-if="req.status === 'pending'">
                    <button
                      @click="updateStatus(req.id, 'in_progress')"
                      class="px-2 py-0.5 text-xxs font-bold text-white bg-blue-500 hover:bg-blue-600 rounded cursor-pointer"
                    >
                      بدء التنفيذ
                    </button>
                  </template>
                  <template v-if="req.status === 'in_progress'">
                    <button
                      @click="updateStatus(req.id, 'completed')"
                      class="px-2 py-0.5 text-xxs font-bold text-white bg-green-500 hover:bg-green-600 rounded cursor-pointer"
                    >
                      اكتمل
                    </button>
                  </template>
                  <span v-else-if="req.status === 'completed'" class="text-xs text-green-500">تم الإنجاز</span>
                  <span v-else class="text-gray-400">-</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Create Request Modal (Hidden on print) -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm no-print">
      <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-2xl shadow-xl overflow-hidden border border-gray-200 dark:border-gray-800 animate-fade-in">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center bg-gray-50 dark:bg-gray-800/50">
          <h3 class="text-sm font-bold text-gray-900 dark:text-white">تقديم طلب أعمال مكتبية</h3>
          <button @click="showAddModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl font-bold cursor-pointer">&times;</button>
        </div>
        <form @submit.prevent="submitRequest" class="p-6 space-y-4">
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">الموظف طالب الخدمة *</label>
            <select v-model="form.requested_by" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm">
              <option value="" disabled>اختر الموظف...</option>
              <option v-for="emp in employees" :key="emp.military_number" :value="emp.military_number">
                {{ emp.full_name }} ({{ emp.military_number }})
              </option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">نوع الخدمة *</label>
            <select v-model="form.type" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm">
              <option value="print">طباعة (Print)</option>
              <option value="photocopy">تصوير أوراق (Photocopy)</option>
              <option value="scan">مسح ضوئي (Scan)</option>
              <option value="other">أخرى (Other)</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">العنوان/الموضوع *</label>
            <input v-model="form.title" type="text" required placeholder="مثال: تصوير تعميم وزاري، طباعة تقرير مالي" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
          </div>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">عدد النسخ المطلوبة *</label>
              <input v-model.number="form.copies_count" type="number" required min="1" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">عدد الصفحات للنسخة *</label>
              <input v-model.number="form.pages_count" type="number" required min="1" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
            </div>
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">تعليمات إضافية/وصف</label>
            <textarea v-model="form.description" rows="2" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm"></textarea>
          </div>
          <div class="flex justify-end gap-2 pt-4 border-t border-gray-200 dark:border-gray-800">
            <button type="button" @click="showAddModal = false" class="px-4 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">إلغاء</button>
            <button type="submit" class="px-4 py-2 text-xs font-medium text-white bg-brand-500 rounded-lg hover:bg-brand-600">إرسال الطلب</button>
          </div>
        </form>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useSecretariatStore } from '@/stores/secretariat'
import { usePersonnelStore } from '@/stores/personnel'
import { useAuthStore } from '@/stores/auth'
import { useCoreStore } from '@/stores/core'
import Swal from 'sweetalert2'

// Import the official Republican Eagle Logo and State Emblem
import yemenLogo from '@/assets/yemen_logo.jpg'
import yemenCalligraphy from '@/assets/yemen_calligraphy.svg'

const route = useRoute()
const store = useSecretariatStore()
const personnelStore = usePersonnelStore()
const authStore = useAuthStore()
const coreStore = useCoreStore()

const activeTab = ref<any>('writer')
const loading = ref(false)
const savingCorrespondence = ref(false)
const showAddModal = ref(false)

const requests = ref<any[]>([])
const employees = ref<any[]>([])

// Dynamic user Governorate detection based on ABAC security admin profiles
const userSecurityAdminName = computed(() => {
  const adminId = authStore.user?.authz_profile?.security_admin_id
  if (!adminId) return 'عــام'
  const matched = coreStore.securityAdmins.find(a => a.id === adminId)
  if (matched) {
    let name = matched.name
    name = name.replace('إدارة أمن محافظة ', '')
    name = name.replace('إدارة أمن ', '')
    name = name.replace('شرطة محافظة ', '')
    return name
  }
  return 'تعز'
})

// Memo template state
const memo = ref({
  templateType: 'memo',
  refNo: '',
  date: '',
  gregorianDate: '',
  attachments: 'لا يوجد',
  recipient: '',
  subject: '',
  body: '',
  signatoryName: '',
  signatoryTitle: 'مدير إدارة القوى البشرية'
})

// Document request form state
const form = ref({
  requested_by: '',
  type: 'print',
  title: '',
  copies_count: 1,
  pages_count: 1,
  description: ''
})

async function fetchRequests() {
  loading.value = true
  try {
    const res = await store.fetchDocumentRequests()
    requests.value = res.results || []
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function submitRequest() {
  try {
    await store.createDocumentRequest(form.value)
    showAddModal.value = false
    form.value = { requested_by: '', type: 'print', title: '', copies_count: 1, pages_count: 1, description: '' }
    fetchRequests()
    Swal.fire({ icon: 'success', title: 'تم تقديم طلب الخدمة بنجاح', timer: 1500, showConfirmButton: false })
  } catch (err) {
    console.error(err)
  }
}

async function updateStatus(id: number, status: string) {
  try {
    await store.updateDocumentRequest(id, { status })
    fetchRequests()
  } catch (err) {
    console.error(err)
  }
}

function printMemo() {
  window.print()
}

async function saveAsCorrespondence() {
  if (!memo.value.subject || !memo.value.body) {
    Swal.fire({ icon: 'warning', title: 'الرجاء ملء موضوع المذكرة ونص الخطاب أولاً' })
    return
  }
  savingCorrespondence.value = true
  try {
    // Save as outgoing correspondence (صادر)
    await store.createCorrespondence({
      type: 'outgoing',
      reference_number: memo.value.refNo,
      subject: memo.value.subject,
      sender: `شرطة م/ ${userSecurityAdminName.value} - إدارة القوى البشرية`,
      receiver: memo.value.recipient,
      date: new Date().toISOString().split('T')[0], // Standard system ISO date
      status: 'sent',
      notes: `نص المذكرة:\n${memo.value.body}\n\nالتاريخ المدون: ${memo.value.date}\nالموافق: ${memo.value.gregorianDate}\nالموقع: ${memo.value.signatoryName} (${memo.value.signatoryTitle})`
    })
    Swal.fire({ icon: 'success', title: 'تم تسجيل وحفظ المذكرة في المراسلات الصادرة بنجاح', timer: 2000, showConfirmButton: false })
  } catch (err) {
    console.error(err)
    Swal.fire({ icon: 'error', title: 'حدث خطأ أثناء حفظ المراسلة' })
  } finally {
    savingCorrespondence.value = false
  }
}

watch(activeTab, (tab) => {
  if (tab === 'requests') fetchRequests()
})

onMounted(async () => {
  // Fetch employees list
  await personnelStore.fetchPersonnel()
  employees.value = personnelStore.records || []

  // Ensure security admin references are loaded to determine user's governorate
  if (coreStore.securityAdmins.length === 0) {
    await coreStore.fetchAllReferences()
  }

  // Pre-fill dates
  const today = new Date()
  memo.value.gregorianDate = today.toLocaleDateString('ar-YE', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
  memo.value.date = today.toLocaleDateString('ar-SA', { year: 'numeric', month: 'long', day: 'numeric' }) + 'هـ'

  // Pre-fill from query parameters (for generating covering letter replies)
  if (route.query.subject || route.query.recipient || route.query.refNo) {
    activeTab.value = 'writer'
    if (route.query.subject) memo.value.subject = route.query.subject as string
    if (route.query.recipient) memo.value.recipient = route.query.recipient as string
    if (route.query.refNo) memo.value.refNo = route.query.refNo as string
    if (route.query.body) memo.value.body = route.query.body as string
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400;1,700&family=Aref+Ruqaa:wght@400;700&display=swap');

.basmala-text {
  font-family: 'Aref Ruqaa', serif;
  font-size: 1.45rem;
  font-weight: 400;
  color: #111827;
  text-align: center;
}

@media print {
  /* Hide system elements */
  .no-print,
  nav,
  header,
  aside,
  button,
  .sidebar,
  .topbar,
  .page-breadcrumb {
    display: none !important;
  }
  
  /* Reset document flow and containers */
  body, html {
    background-color: white !important;
    color: black !important;
    font-size: 12pt !important;
    margin: 0 !important;
    padding: 0 !important;
  }
  
  /* Show only the sheet container */
  .print-preview-container {
    visibility: visible !important;
    position: absolute !important;
    left: 0 !important;
    top: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
    border: none !important;
    box-shadow: none !important;
    padding: 20mm 15mm 20mm 15mm !important;
    margin: 0 !important;
    background: white !important;
    color: black !important;
  }
}
</style>

<style>
@media print {
  @page {
    size: A4;
    margin: 0 !important;
  }
}
</style>
