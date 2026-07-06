<template>
  استمارة غياب بعذ

  <div class="pa-4">
    <div class="pb-3 text-left">
      <div><strong>رقم الاستمارة:</strong> ....................</div>
      <div class="mt-2"><strong>التاريخ:</strong>
      <span class="value dotted-line"> {{input_data?.issue_date}} </span>
      </div>
    </div>
    <div class="content-box rounded-lg pa-3 mb-2">
      <v-row no-gutters>
        <v-col cols="12" class="mb-2">
          <strong>الأخ الدكتور/ عميد كلية </strong>
          <span class="value dotted-line"> {{input_data?.collage_name_ar}} </span>
          <span class="float-left"><strong>المحترم</strong></span>
        </v-col>

        <v-col cols="12" class="text-center mb-2">
          <strong>تحية طيبة وبعد ،</strong>
        </v-col>

        <v-col cols="12" class="text-justify line-height-normal mb-2">
          أنا الطالب : <span class="dotted-line">
            <span > {{input_data?.student_name}} </span>
            </span> مقيد في :
          <span class="dotted-line">
            {{input_data?.collage_name_ar}}
          </span>
          برقم :
          <span class="dotted-line">
            {{input_data?.academic_no}}
          </span>
           تخصص :
          <span class="dotted-line">
            {{input_data?.specialization_name_ar}}
          </span>
          المستوى :
          <span class="dotted-line">
            {{input_data?.level}}
          </span>

           الفصل:
           <span class="dotted-line">
            {{input_data?.semester}}
           </span>
           للعام الجامعي :
          <span class="dotted-line">{{input_data?.academic_year_m}}</span>
          أتقدم إليكم بطلب غياب بعذر عن المقرر الدراسي :
        </v-col>

        <v-col cols="12" class="d-flex justify-space-between px-2 mb-3 font-weight-bold">
          <span class="value dotted-line">
            {{input_data?.subject}}
          </span>

        </v-col>

        <v-col cols="12" class="mb-2">
          نتيجة : <span class="value dotted-line">

            {{input_data?.reason}}
          </span>
        </v-col>

        <v-col cols="12">
          <v-row>
            <v-col cols="6" class="text-right"> تاريخ :
              <span class="value dotted-line">
                {{input_data?.issue_date}}
              </span>
            </v-col>
            <v-col cols="6" class="text-left pl-8">
              <strong>التوقيع :</strong> ....................
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </div>

    <v-divider class="border-opacity-100 mb-1"></v-divider>

    <!-- <div class="mb-2 px-2">
      <v-row no-gutters>
        <v-col cols="12" class="d-flex justify-space-between">
          <strong>الأخ / ت : شؤون الطلبة</strong>
          <strong>المحترم / ة</strong>
        </v-col>
        <v-col cols="12" class="text-center">
          <strong>بعد التحية</strong>
        </v-col>
        <v-col cols="12" class="text-center">
          لاتخاذ الإجراءات بحسب النظام واللوائح المنظمة
        </v-col>
        <v-col cols="12" class="text-left pl-8">
          <strong>عميد الكلية</strong>
        </v-col>
      </v-row>
    </div>

    <div class="mb-1 bg-grey-lighten-4 py-1 px-2 section-header border-top-bottom">
      <strong>- بيانات تملأ من قبل شؤون الطلبة :-</strong>
    </div>

    <div class="table-container mb-2">
      <table class="custom-table">
        <thead>
          <tr>
            <th width="5%">م</th>
            <th width="65%">البيان</th>
            <th width="15%">مطابق</th>
            <th width="15%">غير مطابق</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>1</td>
            <td>الطلب تم خلال الفترة الزمنية القانونية</td>
            <td></td>
            <td></td>
          </tr>
          <tr>
            <td>2</td>
            <td>
              الطلب مرفق بمبرر للغياب بعذر : تقرير طبي من المستشفى الجامعي / تذكرة السفر /
              ....................
            </td>
            <td></td>
            <td></td>
          </tr>
          <tr>
            <td>3</td>
            <td>
              سبق للطالب وقف قيده لمدة (....................) في العام الجامعي
              (....................)
            </td>
            <td></td>
            <td></td>
          </tr>
          <tr>
            <td>4</td>
            <td>
              سبق للطالب أن غاب بعذر في (....................) في العام
              (....................) من .................... الجامعي
            </td>
            <td></td>
            <td></td>
          </tr>
          <tr>
            <td>5</td>
            <td>لا يوجد نواقص في ملف الطالب</td>
            <td></td>
            <td></td>
          </tr>
        </tbody>
      </table>

      <div class="table-footer-grid mt-1">
        <div><strong>المختص</strong></div>
        <div><strong>شؤون الطلبة</strong></div>
        <div><strong>رأي العمادة</strong></div>
      </div>
    </div>

    <v-divider class="border-opacity-100 mb-2"></v-divider>

    <div
      class="decision-box rounded-lg pa-2 bg-grey-lighten-4 flex-grow-1 d-flex flex-column"
    >
      <div class="text-center mb-1 text-h6 font-weight-bold">القرار</div>
      <p class="text-justify line-height-normal mb-2">
        بعد الإطلاع على ما تقدم به الطالب ونظراً للمبررات التي ذكرت للغياب بعذر وبناءً على
        وضع الطالب الدراسي
        <strong
          >فأننا نوافق على غياب بعذر للطالب المذكور أعلاه في المقررات الدراسية التالية
          :</strong
        >
      </p>

      <v-col cols="12" class="d-flex justify-space-between px-2 mb-3 font-weight-bold">
        <span>1- ....................</span>
        <span>2- ....................</span>
        <span>3- ....................</span>
        <span>4- ....................</span>
        <span>5- ....................</span>
      </v-col>

      <div class="mb-4 font-weight-bold">
        على أن يتم إختبار هذه المقررات في
        ........................................................................
      </div>

      <div class="mt-auto">
        <v-row align="end">
          <v-col cols="7">
            <div class="text-caption font-weight-bold">
              * يتأكد الطالب من استكمال الموافقة على قبول الغياب بعذر من عدمه ، وأنه تم
              حفظ صورة في ملفه
            </div>
          </v-col>
          <v-col cols="5" class="text-left pl-8">
            <strong>عميد الكلية</strong>
          </v-col>
        </v-row>
      </div>
    </div> -->
  </div>
</template>

<script >
export default {
  name: "ExcusedAbsenceRequestForm",
  inject: ["context"],
  data() {
    return {
      input_data: this.context?.input_data ?? {},
    };
  },
};
</script>

<style scoped>
/* إعداد الخطوط والاتجاه */
.v-application {
  font-family: "Cairo", sans-serif !important;
  direction: rtl;
}

/* ضبط العنوان العائم */
.section-title-container {
  margin-top: -25px;
}

/* المربع الرمادي الشفاف */
.content-box {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
}

.decision-box {
  border: 1px solid #bbb;
}

/* الخطوط المنقطة */
.dotted-line {
  border-bottom: 1px dotted #000;
  display: inline-block;
  min-width: 40px;
  text-align: center;
  font-weight: bold;
  margin: 0 4px;
}

/* تنسيق الجدول المخصص */
.custom-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.custom-table th,
.custom-table td {
  border: 1px solid #000; /* حدود سوداء واضحة */
  padding: 4px 8px;
  text-align: right;
}

.custom-table th {
  background-color: #e0e0e0;
  text-align: center;
  font-weight: bold;
}

.custom-table td:nth-child(3),
.custom-table td:nth-child(4) {
  text-align: center; /* توسيط أعمدة المطابقة */
}

/* شبكة التوقيعات أسفل الجدول */
.table-footer-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  text-align: center;
  margin-top: 5px;
  padding: 0 10px;
}

.line-height-normal {
  line-height: 1.8;
}

.border-top-bottom {
  border-top: 1px solid #999;
  border-bottom: 1px solid #999;
}

/* تحسينات الطباعة */
@media print {
  .v-main {
    padding: 0 !important;
    background: white !important;
  }
  .form-paper {
    box-shadow: none !important;
    margin: 0 !important;
    width: 100% !important;
    height: 100% !important;
  }
}
</style>
