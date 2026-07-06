<template>
  <div>
    <v-row class="text-center mb-8 align-center">
      <v-col cols="12" class="text-left">
        <div class="d-flex justify-end align-center">
          <span>كلية:</span>
          <span class="dotted-line" style="width: 100px"></span>
        </div>
        <div class="d-flex justify-end align-center mt-2">
          <span>قسم:</span>
          <span class="dotted-line" style="width: 100px"></span>
        </div>
      </v-col>
    </v-row>

    <div class="text-center mb-12">
      <h1 class="doc-title">مستند إعفاء من الحضور المحاضرات</h1>
    </div>

    <v-card-text class="doc-body" style="line-height: 2">
      <p>
        تشهد عمادة شؤون الطلاب بأن الطالب/ة:
        <span class="dotted-line" style="width: 400px">{{
          output_data.student_name
        }}</span>
      </p>
      <p>
        المقيد في المستوى:
        <span class="dotted-line" style="width: 100px">{{ output_data.level }}</span>
        رقم قيد (<span class="dotted-line" style="width: 100px">{{
          output_data.student_id
        }}</span
        >)
      </p>
      <p>
        قد تم منحه إعفاءً من حضور المحاضرات للفترة من:{{ output_data.from_date }}
        إلى:
        {{ output_data.to_date }}
      </p>
      <p>
        وذلك للأسباب التالية:
        <span class="dotted-line" style="width: 300px"></span>
      </p>
    </v-card-text>

    <div style="margin-top: 200px">
      <v-row class="text-center">
        <v-col cols="6">
          <p class="font-weight-bold">ختم الكلية</p>
          <div style="height: 80px"></div>
        </v-col>
        <v-col cols="6">
          <p class="font-weight-bold">توقيع العميد</p>
          <div style="height: 80px">
            <span class="dotted-line" style="width: 100px"></span>
          </div>
        </v-col>
      </v-row>
    </div>
  </div>
</template>
<script>
export default {
  name: "AttendanceExemptionDocument",
  inject: ["context"],
  data() {
    return {
      output_data: this.context?.output_data ?? {},
    };
  },
};
</script>
