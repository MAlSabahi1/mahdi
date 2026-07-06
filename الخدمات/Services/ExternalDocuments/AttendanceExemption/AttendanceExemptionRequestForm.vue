<template>
  <div>
    <v-row class="text-center mb-8 align-center">
      <v-col cols="12" class="text-left">
        <div class="d-flex justify-end align-center">
          <span>التاريخ:</span>
          <span class="dotted-line" style="width: 100px">{{
            input_data?.issue_date
          }}</span>
        </div>
        <div class="d-flex justify-end align-center mt-2">
          <span>الرقم:</span>
          <span class="dotted-line" style="width: 100px"></span>
        </div>
      </v-col>
    </v-row>
    <div class="text-center mb-12">
      <h1 class="doc-title">طلب إعفاء من حضور المحاضرات</h1>
    </div>

    <div class="doc-body">
      <p>
        أنا الطالب /
        <span class="dotted-line" style="width: 230px">{{
          input_data?.student_name
        }}</span>
        المقيد في كلية
        <span class="dotted-line" style="width: 150px">{{ input_data?.college }}</span>
      </p>

      <p class="mt-3">
        قسم
        <span class="dotted-line" style="width: 175px">{{
          input_data?.specialization
        }}</span>
        المستوى الدراسي
        <span class="dotted-line" style="width: 130px">{{ input_data?.level }}</span>
        بـالرقم الجامعي (
        <span class="dotted-line" style="width: 100px">{{ input_data?.student_id }}</span>
        ).
      </p>

      <p class="mt-6">
        أتقدم بطلبي هذا إلى عمادة الكلية للإعفاء من الحضور للفترة من تاريخ
        <span class="dotted-line" style="width: 100px">{{ input_data?.from_date }}</span>
        إلى تاريخ
        <span class="dotted-line" style="width: 100px">{{ input_data?.to_date }}</span
        >.
      </p>

      <p class="mt-4">
        وذلك بسبب:
        <span class="dotted-line" style="width: 340px"></span>
      </p>

      <p class="mt-10 text-center font-weight-bold">وتقبلوا خالص التحية والتقدير،،</p>
    </div>
    <div style="margin-top: 200px">
      <v-row class="text-center">
        <v-col cols="6" class="text-center">
          <div class="font-weight-bold mb-10">توقيع الطالب</div>
          <div><span class="dotted-line" style="width: 150px"></span></div>
        </v-col>
        <v-col cols="6" class="text-center">
          <div class="font-weight-bold mb-10">اعتماد الكلية/القسم</div>
          <div><span class="dotted-line" style="width: 150px"></span></div>
        </v-col>
      </v-row>
    </div>
  </div>
</template>
<script>
export default {
  name: "AttendanceExemptionRequestForm",
  inject: ["context"],
  data() {
    return {
      input_data: this.context?.input_data ?? {},
    };
  },
};
</script>
