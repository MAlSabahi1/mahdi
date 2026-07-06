<template>
  <div>
    <v-row class="text-center mb-8 align-center">
      <v-col cols="12" class="text-left">
        <div>التاريخ: {{ output_data.date_today }}</div>
        <div>الرقم: ....................</div>
      </v-col>
    </v-row>

    <div class="text-center mb-10">
      <h2 class="doc-title">قـرار إيقاف قيد دراسي</h2>
    </div>

    <div class="doc-body text-right">
      <p>
        استناداً إلى اللائحة التنظيمية لشؤون الطلاب، وبناءً على الطلب المقدم من الطالب /
        <span class="dotted-line" style="width: 350px">{{
          output_data.student_name
        }}</span>
      </p>
      <p>
        المقيد بكلية
        <span class="dotted-line" style="width: 150px">{{ output_data.college }}</span>
        قسم
        <span class="dotted-line" style="width: 180px">{{
          output_data.specialization
        }}</span>
        بالمستوى
        <span class="dotted-line" style="width: 120px">{{ output_data.level }}</span
        >.
      </p>
      <p class="mt-4">
        تقرر **إيقاف قيد** الطالب المذكور أعلاه للعام الجامعي (
        <span class="dotted-line" style="width: 120px">{{
          output_data.current_academic_year
        }}</span>
        ) نظراً للظروف الموضحة في طلبه، على أن يعاود الدراسة في العام الجامعي القادم.
      </p>
      <p class="mt-6 text-subtitle-2 text-red-darken-4">
        * ملاحظة: لا يحق للطالب دخول الامتحانات خلال فترة إيقاف القيد.
      </p>
    </div>

    <v-row class="mt-15 text-center">
      <v-col cols="4">
        <p class="font-weight-bold">المسجل العام</p>
        <div class="sign-space">
          <span class="dotted-line" style="width: 80px"></span>
        </div>
      </v-col>
      <v-col cols="4">
        <p class="font-weight-bold">ختم الكلية</p>
        <div class="stamp-space"></div>
      </v-col>
      <v-col cols="4">
        <p class="font-weight-bold">نائب العميد لشؤون الطلاب</p>
        <div class="sign-space">
          <span class="dotted-line" style="width: 80px"></span>
        </div>
      </v-col>
    </v-row>
  </div>
</template>
<script>
export default {
  name: "SuspensionInrollmentDocument",
  inject: ["context"],
  data() {
    return {
      output_data: this.context?.output_data ?? {},
    };
  },
};
</script>
