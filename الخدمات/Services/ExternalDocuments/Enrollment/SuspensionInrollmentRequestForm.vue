<template>
  <div elevation="4" class="pa-4 position-relative">
    <div class="text-left mb-2">
      <strong>التاريخ:</strong>
      {{ input_data?.date_today }}
    </div>

    <div class="content-box rounded-lg pa-3 mb-2">
      <v-row no-gutters>
        <v-col cols="12" class="mb-2">
          <strong>الأخ الدكتور/ عميد كلية</strong>
          <strong class="mx-1">{{ input_data?.college }}</strong>
          <span class="float-left"><strong>المحترم</strong></span>
        </v-col>

        <v-col cols="12" class="text-center mb-2">
          <strong>تحية طيبة وبعد ،</strong>
        </v-col>

        <v-col cols="12" class="text-justify line-height-normal mb-2">
          أنا الطالب :
          <span class="dotted-line label">{{ input_data?.student_name }}</span> مقيد في :
          <span class="dotted-line label">كلية : {{ input_data?.college }}</span>
          برقم :
          <span class="dotted-line label">{{ input_data?.student_id }}</span> المستوى
          <span class="dotted-line label"> {{ input_data?.level }} </span> للعام الجامعي :
          <span class="dotted-line label">{{ input_data?.current_academic_year }}</span>
          أتقدم إليكم بطلب وقف قيدي عن الدراسة لمدة :
          <span class="dotted-line label">{{
            input_data.period == "academic_year"
              ? "سنة دراسية"
              : input_data.period == "semester"
              ? "فصل دراسي"
              : ""
          }}</span>
          <span class="dotted-line label" v-if="input_data?.semester">
            {{ input_data?.semester?.name }}</span
          >
        </v-col>
        <v-col cols="12" class="text-justify line-height-normal mb-2">
          بسبب :
          <span class="dotted-line label" style="width: 90%">{{
            input_data?.reason
          }}</span>
        </v-col>

        <v-col cols="12" class="text-justify font-weight-bold mb-3">
          وأتعهد والتزم بتقديم طلب للجامعة لفتح القيد بعد انتهاء فترة وقف القيد وفي حالة
          تخلفي عن الموعد المحدد سأكون غائباً بدون عذر.
        </v-col>

        <v-col cols="12">
          <v-row>
            <v-col cols="6" class="text-right">
              تاريخ : {{ input_data?.return_date }}
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
export default {
  name: "SuspensionInrollmentRequestForm",
  inject: ["context"],
  data() {
    return {
      input_data: this.context?.input_data ?? {},
    };
  },
};
</script>

<style scoped>
.label {
  font-weight: bold;
  color: #1b2f5e;
  white-space: nowrap;
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
  margin-top: 10px;
  padding: 0 10px;
}

/* القوائم */
.custom-list {
  list-style-type: decimal;
  margin-right: 20px;
}

.line-height-normal {
  line-height: 1.8;
}

.border-top-bottom {
  border-top: 1px solid #999;
  border-bottom: 1px solid #999;
}
</style>
