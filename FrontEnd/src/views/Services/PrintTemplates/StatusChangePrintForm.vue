<template>
  <div class="print-form" dir="rtl" lang="ar">
    <!-- Header Section -->
    <div class="header-section">
      <div class="header-right">
        <p class="font-bold text-lg">الجمهورية اليمنية</p>
        <p class="font-bold text-lg">وزارة الداخلية</p>
        <p class="font-bold text-sm">الوكيل لقطاع الموارد البشرية</p>
        <p class="font-bold text-sm">الادارة العامة للقوى البشرية</p>
        <p class="font-bold text-sm">لجنة بناء الاستمارات</p>
      </div>
      
      <div class="header-center">
        <div class="text-center mb-1">
          <span class="font-mushaf text-xl">بسم الله الرحمن الرحيم</span>
        </div>
        <img src="/images/logo/yemen_logo_clean.png" alt="الشعار" class="logo-img" onerror="this.style.display='none'" />
      </div>

      <div class="header-left">
        <div class="header-box">
          <div class="flex justify-between mb-2">
            <span>الرقم:</span>
            <span>( {{ String(form?.id || '').padStart(6, '0') }} )</span>
          </div>
          <div class="flex justify-between mb-2">
            <span>التاريخ:</span>
            <span>{{ new Date().toLocaleDateString('en-GB') }} م</span>
          </div>
          <div class="flex justify-between">
            <span>المرفقات:</span>
            <span>.....................</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Title Section -->
    <div class="title-container">
      <div class="title-badge">
        <div class="title-badge-inner">
          {{ formTitle }}
        </div>
      </div>
    </div>

    <!-- Table 1: Personal Data -->
    <div class="section-container mt-6">
      <h3 class="section-title">أولاً البيانات الشخصية</h3>
      <table class="official-table">
        <thead>
          <tr>
            <th>الرتبة</th>
            <th>الرقم العسكري</th>
            <th class="w-2/5">الاسم</th>
            <th>الوحدة</th>
            <th>السرية</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="font-bold">{{ form?.personnel?.rank || '—' }}</td>
            <td class="font-bold">{{ form?.personnel?.military_number || '—' }}</td>
            <td class="font-bold">{{ form?.personnel?.full_name || '—' }}</td>
            <td class="font-bold">{{ form?.personnel?.central_department || form?.personnel?.workplace || '—' }}</td>
            <td class="font-bold">{{ form?.personnel?.company || '—' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Table 2: Birth & Residence Data -->
    <div class="section-container">
      <h3 class="section-title">ثانياً بيانات الميلاد والاقامة الحالية</h3>
      <table class="official-table">
        <thead>
          <tr>
            <th>الرقم الوطني</th>
            <th>محل الميلاد</th>
            <th>محل الاقامة الحالية</th>
            <th>جهة الاصدار</th>
            <th>تاريخ الاصدار</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="font-bold">{{ form?.personnel?.national_id || '—' }}</td>
            <td class="font-bold text-sm">{{ formatLocation('birth') }}</td>
            <td class="font-bold text-sm">{{ formatLocation('residence') }}</td>
            <td class="font-bold">{{ form?.personnel?.id_issue_place || '—' }}</td>
            <td class="font-bold">{{ form?.personnel?.id_issue_date || '—' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Table 3: Status Data (Dynamic) -->
    <div class="section-container">
      <h3 class="section-title">ثالثاً بيــانات الحـــــالة</h3>
      <table class="official-table">
        <thead>
          <tr>
            <th v-for="field in specificFields" :key="'h-'+field.key">{{ field.label }}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td v-for="field in specificFields" :key="'d-'+field.key" class="font-bold">
              {{ field.value !== undefined ? field.value : (getFieldValue(field.key) || '—') }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Letter Body Section -->
    <div class="letter-body mt-8 px-4 text-justify leading-loose">
      <p class="font-bold text-lg mb-4">الأخ/ مدير عام القوى البشرية <span class="float-left ml-16">المحترم</span></p>
      <p class="font-bold text-center mb-4">بعد التحية:-</p>
      
      <p class="font-bold mb-4">
        موضحاً لكم اعلاه بيانات حالة المذكور والتي بموجبها تم ضمه على فئة ({{ form?.form_data?.category || form?.form_type_display || '—' }}) ومرفق لكم الاوليات
      </p>
      
      <div class="attachments-list font-bold pr-8 mb-6">
        <span class="ml-4">1- الطلب الشخصي المقدم من المذكور.</span>
        <span>2 - نسخة من البطاقة العسكرية والشخصية معمدة.</span>
        <div v-for="(att, idx) in additionalAttachments" :key="idx" class="mt-1">
          {{ idx + 3 }}- {{ translateAttachment(att) }}.
        </div>
      </div>

      <p class="font-bold mb-6">نأمل التوجيه الى المختصين باستكمال الاجراءات بحسب النظام.</p>
      <p class="font-bold text-center text-lg mb-16">وتقبلوا خالص تحياتنا،،،،</p>
    </div>

    <!-- Signatures -->
    <div class="signatures-grid px-8 mt-12">
      <div class="text-center font-bold">
        <p class="mb-4">قسم الخدمات</p>
        <p class="mb-4 text-right">رتبة/ ........................</p>
        <p class="mb-4 text-right">الاسم/ ........................</p>
      </div>
      <div class="text-center font-bold">
        <p class="mb-4">مدير إدارة القوى البشرية</p>
        <p class="mb-4 text-right">رتبة/ ........................</p>
        <p class="mb-4 text-right">الاسم/ ........................</p>
      </div>
      <div class="text-center font-bold">
        <p class="mb-4">مدير عام شرطة ....................</p>
        <p class="mb-4 text-right">رتبة/ ........................</p>
        <p class="mb-4 text-right">الاسم/ ........................</p>
        <p class="text-center text-sm text-gray-500 mt-2">الختم</p>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  form: any
}>()

const formTitle = computed(() => {
  const titles: Record<string, string> = {
    martyr: 'استمارة إثبات حالة (شهيد)',
    death: 'استمارة إثبات حالة (وفاة)',
    retirement_age: 'استمارة إثبات حالة (بلوغ السن القانوني)',
    medical_unfit: 'استمارة إثبات حالة (عدم اللياقة الصحية)',
    missing: 'استمارة إثبات حالة (مفقود)',
    imprisoned: 'استمارة إثبات حالة (مسجون)',
    seconded: 'استمارة إثبات حالة (انتداب خارجي)',
    escort: 'استمارة إثبات حالة (مرافق / معيات)',
    study_leave: 'استمارة إثبات حالة (تفريغ للدراسة)',
    end_of_service: 'استمارة إثبات حالة (إنهاء خدمة)',
    retired: 'استمارة إثبات حالة (محال للتقاعد)',
    correction: 'استمارة إثبات حالة (تصحيح بيانات)',
  }
  return titles[props.form?.form_type] || \`استمارة إثبات حالة (\${props.form?.form_type_display || ''})\`
})

interface FormField { key: string; label: string; value?: any }

const specificFields = computed<FormField[]>(() => {
  const type = props.form?.form_type
  
  if (type === 'retired') {
    return [
      { key: 'category', label: 'الفئة', value: props.form?.form_data?.category || 'محال للتقاعد' },
      { key: 'birth_date', label: 'تاريخ الميلاد', value: props.form?.personnel?.birth_date || '—' },
      { key: 'join_date', label: 'تاريخ الالتحاق', value: props.form?.personnel?.join_date || '—' },
      { key: 'decision_number', label: 'رقم قرار الاحالة', value: props.form?.form_data?.decision_number || '—' },
      { key: 'referral_date', label: 'تاريخ الاحالة', value: props.form?.form_data?.referral_date || props.form?.form_data?.retirement_date || '—' },
      { key: 'notes', label: 'ملاحظات', value: props.form?.form_data?.notes || '—' }
    ]
  }

  // Fallback for other types
  const fieldMap: Record<string, FormField[]> = {
    martyr: [
      { key: 'category', label: 'الفئة', value: 'شهيد' },
      { key: 'martyrdom_date', label: 'تاريخ الاستشهاد' },
      { key: 'martyrdom_location', label: 'مكان الاستشهاد' },
      { key: 'operations_report', label: 'رقم بلاغ العمليات' },
      { key: 'assignment_order', label: 'رقم أمر التكليف' },
      { key: 'notes', label: 'ملاحظات' }
    ],
    death: [
      { key: 'category', label: 'الفئة', value: 'وفاة' },
      { key: 'death_date', label: 'تاريخ الوفاة' },
      { key: 'death_location', label: 'مكان الوفاة' },
      { key: 'death_certificate', label: 'رقم شهادة الوفاة' },
      { key: 'notes', label: 'ملاحظات' }
    ],
    imprisoned: [
      { key: 'category', label: 'الفئة', value: 'مسجون' },
      { key: 'imprisonment_date', label: 'تاريخ السجن' },
      { key: 'court_name', label: 'اسم المحكمة' },
      { key: 'verdict', label: 'الحكم الصادر' },
      { key: 'notes', label: 'ملاحظات' }
    ],
    study_leave: [
      { key: 'category', label: 'الفئة', value: 'تفريغ للدراسة' },
      { key: 'university_name', label: 'اسم الجامعة' },
      { key: 'specialty', label: 'التخصص' },
      { key: 'study_start', label: 'بداية الدراسة' },
      { key: 'study_end', label: 'نهاية الدراسة' },
      { key: 'notes', label: 'ملاحظات' }
    ]
  }
  return fieldMap[type] || [
      { key: 'category', label: 'الفئة', value: props.form?.form_type_display },
      { key: 'effective_date', label: 'التاريخ الفعلي', value: props.form?.effective_date },
      { key: 'notes', label: 'ملاحظات' }
  ]
})

const additionalAttachments = computed(() => {
  // Return attachments from the payload minus the first two default ones.
  const atts = props.form?.required_attachments || []
  return atts.filter((a: any) => {
    const t = translateAttachment(a)
    return !t.includes('الطلب الشخصي') && !t.includes('البطاقة العسكرية')
  })
})

function getFieldValue(key: string) {
  return props.form?.form_data?.[key] ?? ''
}

function formatLocation(prefix: 'birth' | 'residence') {
  const p = props.form?.personnel
  if (!p) return '—'
  const gov = p[`${prefix}_governorate_name`]
  const dist = p[`${prefix}_district_name`]
  if (gov && dist) return `${gov} - ${dist}`
  if (gov) return gov
  return '—'
}

function translateAttachment(att: any) {
  if (typeof att === 'string') return att
  return att?.label || att?.name || att?.doc_type || att?.key || String(att)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Aref+Ruqaa:wght@400;700&display=swap');

.print-form {
  font-family: 'Cairo', Arial, sans-serif;
  background: white;
  color: black;
  width: 210mm;
  min-height: 297mm;
  padding: 15mm;
  margin: 0 auto;
  box-sizing: border-box;
}

.font-mushaf {
  font-family: 'Aref Ruqaa', serif;
  font-weight: 700;
}

/* Header Grid */
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 4px double #1e3a8a;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.header-right {
  flex: 1;
  text-align: right;
  line-height: 1.4;
  color: #1e3a8a;
}

.header-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.logo-img {
  width: 90px;
  height: 90px;
  object-fit: contain;
}

.header-left {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}
.header-box {
  border: 2px solid #1e3a8a;
  padding: 10px 15px;
  width: 220px;
  font-size: 14px;
  font-weight: bold;
}

/* Title Badge */
.title-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}
.title-badge {
  background-color: #dbeafe; /* light blue */
  border: 3px solid #60a5fa; /* border blue */
  border-radius: 8px;
  padding: 4px 6px;
  box-shadow: inset 0 0 0 2px white, 0 4px 6px rgba(0,0,0,0.1);
}
.title-badge-inner {
  font-size: 22px;
  font-weight: 900;
  color: #1e3a8a;
  padding: 6px 20px;
}

/* Tables */
.section-container {
  margin-bottom: 20px;
}
.section-title {
  color: #991b1b;
  font-size: 18px;
  font-weight: 900;
  margin-bottom: 8px;
  text-decoration: underline;
  text-decoration-color: #991b1b;
  text-underline-offset: 4px;
}

.official-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  border: 2px solid #374151;
}
.official-table th {
  background-color: #e5e7eb;
  color: #1f2937;
  font-weight: 800;
  font-size: 15px;
  border: 2px solid #374151;
  padding: 8px;
}
.official-table td {
  border: 2px solid #374151;
  padding: 8px;
  font-size: 14px;
  color: #000;
}

/* Signatures */
.signatures-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

@media print {
  @page {
    size: A4;
    margin: 0;
  }
  body {
    margin: 0;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  .print-form {
    padding: 10mm 15mm;
    width: 100%;
    height: 100vh;
    box-shadow: none;
  }
}
</style>
