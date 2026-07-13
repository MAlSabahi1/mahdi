<template>
  <div class="print-form" dir="rtl" lang="ar">

    <!-- ═══════════════════════════════════════════════
         رأسية الاستمارة الرسمية
    ═══════════════════════════════════════════════ -->
    <div class="form-header">
      <div class="header-logo">
        <img src="/images/republic_logo.png" alt="شعار الجمهورية" class="logo-img" onerror="this.style.display='none'" />
      </div>
      <div class="header-text">
        <p class="ministry-name">الجمهورية اليمنية</p>
        <p class="ministry-sub">وزارة الداخلية</p>
        <p class="form-title">{{ formTitle }}</p>
        <div class="form-meta-row">
          <span>رقم المعاملة: <strong>{{ formId }}</strong></span>
          <span>التاريخ: <strong>{{ formatDate(form?.created_at) }}</strong></span>
        </div>
      </div>
      <div class="header-logo header-logo-right">
        <div class="qr-placeholder">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" width="48" height="48">
            <rect x="2" y="2" width="8" height="8" rx="1" stroke-width="2"/>
            <rect x="14" y="2" width="8" height="8" rx="1" stroke-width="2"/>
            <rect x="2" y="14" width="8" height="8" rx="1" stroke-width="2"/>
            <path d="M14 14h2v2h-2zM18 14h2v2h-2zM14 18h2v2h-2zM18 18h2v2h-2z" stroke-width="1.5"/>
          </svg>
          <p class="text-[8px] text-gray-500 mt-0.5">TX-{{ String(form?.id).padStart(6, '0') }}</p>
        </div>
      </div>
    </div>

    <!-- ═══ بيانات الفرد ═══ -->
    <section class="form-section">
      <h3 class="section-title">بيانات الفرد المعني</h3>
      <div class="fields-grid-4">
        <div class="field-box">
          <label>الاسم الرباعي</label>
          <span>{{ form?.personnel?.full_name || '—' }}</span>
        </div>
        <div class="field-box">
          <label>الرقم العسكري</label>
          <span class="font-mono">{{ form?.personnel?.military_number || '—' }}</span>
        </div>
        <div class="field-box">
          <label>الرتبة الحالية</label>
          <span>{{ form?.personnel?.rank || '—' }}</span>
        </div>
        <div class="field-box">
          <label>الوحدة / الإدارة</label>
          <span>{{ form?.personnel?.central_department || '—' }}</span>
        </div>
        <div class="field-box">
          <label>الحالة الخدمية السابقة</label>
          <span>{{ form?.from_status || '—' }}</span>
        </div>
        <div class="field-box">
          <label>الحالة الخدمية الجديدة</label>
          <span class="text-bold">{{ form?.to_status || '—' }}</span>
        </div>
        <div class="field-box">
          <label>تاريخ النفاذ</label>
          <span>{{ form?.effective_date ? formatDate(form.effective_date) : '—' }}</span>
        </div>
        <div class="field-box">
          <label>نوع الخدمة</label>
          <span>{{ form?.form_type_display || '—' }}</span>
        </div>
      </div>
    </section>

    <!-- ═══ الحقول الخاصة بنوع الاستمارة ═══ -->
    <section class="form-section" v-if="specificFields.length > 0">
      <h3 class="section-title">تفاصيل الاستمارة</h3>
      <div class="fields-grid-3">
        <div v-for="field in specificFields" :key="field.key" class="field-box" :class="field.wide ? 'col-span-2' : ''">
          <label>{{ field.label }}</label>
          <span>{{ getFieldValue(field.key) || '—' }}</span>
        </div>
      </div>
    </section>

    <!-- ═══ ملاحظات ═══ -->
    <section class="form-section" v-if="form?.notes">
      <h3 class="section-title">ملاحظات</h3>
      <div class="notes-box">{{ form.notes }}</div>
    </section>

    <!-- ═══ المرفقات المطلوبة ═══ -->
    <section class="form-section" v-if="form?.required_attachments?.length">
      <h3 class="section-title">المستندات والوثائق المرفقة</h3>
      <div class="attachments-table">
        <table>
          <thead>
            <tr>
              <th style="width:30px">م</th>
              <th>نوع المستند</th>
              <th style="width:80px">الحالة</th>
              <th style="width:80px">ملاحظة</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(att, idx) in form.required_attachments" :key="idx">
              <td class="text-center">{{ Number(idx) + 1 }}</td>
              <td>{{ translateAttachment(att) }}</td>
              <td class="text-center">
                <span v-if="isAttachmentPresent(att)" class="att-present">✓ مرفق</span>
                <span v-else class="att-missing">✗ ناقص</span>
              </td>
              <td></td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- ═══ خانات التواقيع ═══ -->
    <section class="signatures-section">
      <div class="signature-block" v-for="sig in signatures" :key="sig.role">
        <div class="sig-role">{{ sig.role }}</div>
        <div class="sig-name-line">الاسم: _______________</div>
        <div class="sig-line">التوقيع: _______________</div>
        <div class="sig-date">التاريخ: _______________</div>
        <div class="sig-stamp">الختم الرسمي</div>
      </div>
    </section>

    <!-- ═══ قرار الوزارة (للخدمات الخارجية) ═══ -->
    <section class="form-section ministry-section" v-if="form?.is_external">
      <h3 class="section-title ministry-title">🏛 قرار الوزارة</h3>
      <div class="fields-grid-3">
        <div class="field-box col-span-2">
          <label>رقم القرار / المذكرة الوزارية</label>
          <span>{{ form?.ministry_approval_doc_id ? `مستند #${form.ministry_approval_doc_id}` : 'لم يرفق بعد' }}</span>
        </div>
        <div class="field-box">
          <label>تاريخ القرار</label>
          <span>____________________</span>
        </div>
      </div>
    </section>

    <!-- ═══ تذييل الصفحة ═══ -->
    <div class="form-footer">
      <div class="footer-left">
        <p>نظام إدارة الموارد البشرية — HRMS</p>
        <p>طُبع بواسطة: {{ form?.submitted_by || 'النظام' }}</p>
      </div>
      <div class="footer-center">
        <p>سري — للاستخدام الرسمي فقط</p>
      </div>
      <div class="footer-right">
        <p>{{ new Date().toLocaleDateString('ar-SA') }}</p>
        <p class="font-mono text-xs">TX-{{ String(form?.id).padStart(6, '0') }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  form: any
}>()

// ━━ عنوان الاستمارة ━━
const formTitle = computed(() => {
  const titles: Record<string, string> = {
    martyr: 'استمارة إثبات حالة شهيد',
    death: 'استمارة إثبات حالة وفاة',
    retirement_age: 'استمارة إحالة للتقاعد — بلوغ السن القانوني',
    medical_unfit: 'استمارة إثبات عدم اللياقة الصحية',
    missing: 'استمارة إثبات حالة مفقود',
    imprisoned: 'استمارة إثبات حالة مسجون',
    seconded: 'استمارة انتداب خارجي',
    escort: 'استمارة مرافق / معيات',
    study_leave: 'استمارة تفريغ للدراسة',
    end_of_service: 'استمارة إنهاء مدة الخدمة',
    retired: 'استمارة إحالة للتقاعد',
    correction: 'استمارة تصحيح بيانات',
  }
  return titles[props.form?.form_type] || props.form?.form_type_display || 'استمارة إثبات حالة'
})

// ━━ رقم الاستمارة ━━
const formId = computed(() => `TX-${String(props.form?.id || 0).padStart(6, '0')}`)

// ━━ الحقول الخاصة بكل نوع ━━
interface FormField { key: string; label: string; wide?: boolean }

const specificFields = computed<FormField[]>(() => {
  const type = props.form?.form_type
  const fieldMap: Record<string, FormField[]> = {
    martyr: [
      { key: 'martyrdom_date', label: 'تاريخ الاستشهاد' },
      { key: 'martyrdom_location', label: 'مكان الاستشهاد / الجبهة' },
      { key: 'martyrdom_cause', label: 'سبب الاستشهاد', wide: true },
      { key: 'operations_report', label: 'رقم بلاغ العمليات' },
      { key: 'assignment_order', label: 'رقم أمر التكليف' },
    ],
    death: [
      { key: 'death_date', label: 'تاريخ الوفاة' },
      { key: 'death_cause', label: 'سبب الوفاة', wide: true },
      { key: 'death_location', label: 'مكان الوفاة' },
      { key: 'death_certificate', label: 'رقم شهادة الوفاة' },
    ],
    retirement_age: [
      { key: 'retirement_date', label: 'تاريخ الإحالة للتقاعد' },
      { key: 'service_years', label: 'سنوات الخدمة الفعلية' },
      { key: 'decision_number', label: 'رقم قرار الإحالة' },
    ],
    medical_unfit: [
      { key: 'medical_committee_date', label: 'تاريخ قرار اللجنة الطبية' },
      { key: 'medical_committee_number', label: 'رقم قرار اللجنة' },
      { key: 'diagnosis', label: 'التشخيص / سبب عدم اللياقة', wide: true },
    ],
    missing: [
      { key: 'missing_date', label: 'تاريخ الاختفاء' },
      { key: 'missing_location', label: 'آخر موقع معروف' },
      { key: 'missing_circumstances', label: 'ظروف الاختفاء / الفقدان', wide: true },
    ],
    imprisoned: [
      { key: 'imprisonment_date', label: 'تاريخ السجن' },
      { key: 'court_name', label: 'اسم المحكمة' },
      { key: 'verdict', label: 'الحكم الصادر', wide: true },
    ],
    seconded: [
      { key: 'secondment_entity', label: 'جهة الانتداب' },
      { key: 'secondment_start', label: 'تاريخ بداية الانتداب' },
      { key: 'secondment_end', label: 'تاريخ نهاية الانتداب' },
      { key: 'secondment_purpose', label: 'الغرض من الانتداب', wide: true },
    ],
    escort: [
      { key: 'escorted_person', label: 'اسم الشخصية المرافَقة' },
      { key: 'escort_start', label: 'تاريخ بداية المرافقة' },
      { key: 'escort_end', label: 'تاريخ نهاية المرافقة' },
    ],
    study_leave: [
      { key: 'university_name', label: 'اسم الجامعة / المؤسسة' },
      { key: 'specialty', label: 'التخصص / المجال' },
      { key: 'study_start', label: 'تاريخ بداية الدراسة' },
      { key: 'study_end', label: 'التاريخ المتوقع للانتهاء' },
    ],
    end_of_service: [
      { key: 'termination_reason', label: 'سبب إنهاء الخدمة', wide: true },
      { key: 'decision_number', label: 'رقم قرار الإنهاء' },
      { key: 'termination_date', label: 'تاريخ الإنهاء' },
    ],
    correction: [
      { key: 'field_to_correct', label: 'الحقل المراد تصحيحه' },
      { key: 'old_value', label: 'القيمة القديمة الخاطئة' },
      { key: 'new_value', label: 'القيمة الصحيحة الجديدة' },
      { key: 'correction_reason', label: 'سبب التصحيح', wide: true },
    ],
  }
  return fieldMap[type] || []
})

// ━━ التواقيع حسب نوع الخدمة ━━
const signatures = computed(() => {
  if (props.form?.is_external) {
    return [
      { role: 'رئيس قسم الخدمات' },
      { role: 'مدير الموارد البشرية' },
      { role: 'المدير العام' },
      { role: 'ممثل الوزارة (موافقة خارجية)' },
    ]
  }
  return [
    { role: 'رئيس قسم الخدمات' },
    { role: 'مدير الموارد البشرية' },
    { role: 'المدير العام' },
  ]
})

function getFieldValue(key: string) {
  return props.form?.form_data?.[key] ?? ''
}

function isAttachmentPresent(attType: string | Record<string, any>) {
  const key = typeof attType === 'string' ? attType : attType?.doc_type || attType?.key || ''
  return props.form?.attachments?.some((a: any) => a.document_type === key)
}

function translateAttachment(att: any) {
  if (typeof att === 'string') return att
  return att?.label || att?.name || att?.doc_type || att?.key || String(att)
}

function formatDate(dateStr?: string) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('ar-SA', {
    year: 'numeric', month: 'long', day: 'numeric'
  })
}
</script>

<style scoped>
.print-form {
  font-family: 'Cairo', 'Noto Kufi Arabic', Arial, sans-serif;
  direction: rtl;
  text-align: right;
  background: #fff;
  color: #1a1a1a;
  padding: 1cm 1.5cm;
  max-width: 21cm;
  margin: 0 auto;
  font-size: 11pt;
  line-height: 1.6;
}

/* ━━ رأسية الاستمارة ━━ */
.form-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 3px double #1a3c6e;
  padding-bottom: 12px;
  margin-bottom: 16px;
}

.header-logo { width: 80px; text-align: center; }
.logo-img { width: 70px; height: 70px; object-fit: contain; }
.qr-placeholder { display: flex; flex-direction: column; align-items: center; color: #666; }

.header-text { text-align: center; flex: 1; }
.ministry-name { font-size: 14pt; font-weight: 900; color: #1a3c6e; margin: 0; }
.ministry-sub { font-size: 11pt; font-weight: 700; color: #2d5a9e; margin: 2px 0; }
.form-title {
  font-size: 13pt;
  font-weight: 900;
  color: #c0392b;
  margin: 6px 0 4px;
  border: 2px solid #c0392b;
  padding: 4px 16px;
  display: inline-block;
  border-radius: 4px;
}
.form-meta-row {
  font-size: 9pt;
  color: #555;
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 4px;
}

/* ━━ الأقسام ━━ */
.form-section { margin-bottom: 16px; }

.section-title {
  font-size: 10pt;
  font-weight: 900;
  color: #1a3c6e;
  background: #e8eff8;
  border-right: 4px solid #1a3c6e;
  padding: 4px 10px;
  margin-bottom: 10px;
  border-radius: 2px;
}

/* ━━ شبكة الحقول ━━ */
.fields-grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
.fields-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.col-span-2 { grid-column: span 2; }

.field-box {
  border: 1px solid #c5d5e8;
  border-radius: 4px;
  padding: 5px 8px;
  background: #f8fbff;
}
.field-box label {
  display: block;
  font-size: 7.5pt;
  font-weight: 700;
  color: #1a3c6e;
  margin-bottom: 2px;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}
.field-box span {
  font-size: 10pt;
  font-weight: 600;
  color: #1a1a1a;
  display: block;
  min-height: 18px;
  border-bottom: 1px dotted #aac;
}

/* ━━ جدول المرفقات ━━ */
.attachments-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 9pt;
}
.attachments-table th {
  background: #1a3c6e;
  color: #fff;
  padding: 5px 8px;
  font-weight: 700;
  border: 1px solid #1a3c6e;
}
.attachments-table td {
  padding: 5px 8px;
  border: 1px solid #ccd;
}
.attachments-table tr:nth-child(even) td { background: #f5f8fc; }
.att-present { color: #16a34a; font-weight: 700; }
.att-missing  { color: #dc2626; font-weight: 700; }

/* ━━ ملاحظات ━━ */
.notes-box {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px 12px;
  min-height: 48px;
  background: #fffdf0;
  font-size: 10pt;
  line-height: 1.7;
}

/* ━━ التواقيع ━━ */
.signatures-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin: 20px 0 16px;
  border-top: 2px solid #1a3c6e;
  padding-top: 16px;
}
.signature-block {
  border: 1px solid #aac;
  border-radius: 6px;
  padding: 10px;
  text-align: center;
  background: #f8fbff;
}
.sig-role {
  font-size: 9pt;
  font-weight: 900;
  color: #1a3c6e;
  margin-bottom: 12px;
  border-bottom: 1px solid #ccd;
  padding-bottom: 6px;
}
.sig-name-line, .sig-line, .sig-date {
  font-size: 8pt;
  color: #444;
  margin: 10px 0;
  text-align: right;
}
.sig-stamp {
  font-size: 7pt;
  color: #888;
  border: 1px dashed #aaa;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  line-height: 60px;
  margin: 8px auto 0;
}

/* ━━ قسم الوزارة ━━ */
.ministry-section { border: 2px solid #c0392b; border-radius: 6px; padding: 10px; }
.ministry-title { color: #c0392b; background: #fff5f5; border-color: #c0392b; }

/* ━━ التذييل ━━ */
.form-footer {
  border-top: 2px double #1a3c6e;
  padding-top: 8px;
  margin-top: 16px;
  display: flex;
  justify-content: space-between;
  font-size: 7.5pt;
  color: #666;
}

/* ━━ طباعة ━━ */
@media print {
  .print-form {
    padding: 0;
    max-width: 100%;
  }
  @page {
    size: A4;
    margin: 1.5cm;
  }
}
</style>
