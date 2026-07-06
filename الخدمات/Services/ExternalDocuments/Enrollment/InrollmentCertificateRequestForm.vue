<template>
  <div>
    <div class="text-center mb-8">
      <h2 class="doc-title">طلب استخراج شهادة قيد</h2>
    </div>

    <div class="doc-body">
      <p>الأخ / مدير عام النظم والمعلومات - جامعة صنعاء المحترم</p>
      <p class="mt-4">تحية طيبة وبعد،،،</p>

      <p>
        أنا الطالب /
        <span class="dotted-line" style="width: 320px">{{
          input_data.student_name
        }}</span>
        والذي أحمل الرقم الجامعي (
        <span class="dotted-line" style="width: 120px">{{ input_data.student_id }}</span>
        )
      </p>

      <p class="pt-2">
        أرجو التكرم بالموافقة على منحي شهادة قيد دراسي للعام الجامعي 2025-2026م،
      </p>
      <p class="pt-2">
        السبب:
        <span class="dotted-line" style="width: 400px"></span>
      </p>

      <p class="mt-10 text-center font-weight-bold">مقدم الطلب</p>
      <v-row class="justify-center">
        <v-col cols="4" class="text-center">
          <div>التوقيع: <span class="dotted-line" style="width: 150px"></span></div>
          <div class="mt-2 d-flex align-center justify-center">
            <span>تلفون:</span>
            <span class="dotted-line" style="width: 150px"></span>
          </div>
        </v-col>
      </v-row>
    </div>
  </div>
</template>
<script>
export default {
  name: "InrollmentCertificateRequestForm",
  inject: ["context"],
  data() {
    return {
      input_data: this.context?.input_data ?? {},
    };
  },
};
</script>
