<template>
  <div>
    <div class="text-center mb-8">
      <h2 class="doc-title">شهادة القيد الدراسي</h2>
    </div>

    <div class="doc-body">
      <p>
        تشهد كلية:
        <span class="dotted-line" style="width: 120px">{{ output_data.college }}</span>
        بأن الطالب:
        <span class="dotted-line" style="width: 350px">{{
          output_data.student_name
        }}</span>
      </p>
      <p>
        المولو في:
        <span class="dotted-line" style="width: 120px">{{
          output_data.place_of_birth
        }}</span>
        بتاريخ:
        <span class="dotted-line" style="width: 120px">{{
          output_data.date_of_birth
        }}</span>
        الجنسية:
        <span class="dotted-line" style="width: 120px">{{
          output_data.nationality
        }}</span>
      </p>
      <p>
        التحق بالكلية في العام الجامعي:
        <span class="dotted-line" style="width: 120px">{{
          output_data.enrollment_year
        }}</span>
        برقم قيد:
        <span class="dotted-line" style="width: 120px">{{ output_data.student_id }}</span>
        تخصص:
        <span class="dotted-line" style="width: 120px">{{
          output_data.specialization
        }}</span>
      </p>
      <p>
        مقيد بالمستوى:
        <span class="dotted-line" style="width: 120px">{{ output_data.level }}</span>
        للعام الجامعي:
        <span class="dotted-line" style="width: 120px">{{
          output_data.current_academic_year
        }}</span>
        بتاريخ:
        <span class="dotted-line" style="width: 120px">{{ output_data.issue_date }}</span>
      </p>

      <div style="margin-top: 200px">
        <v-row class="justify-center">
          <v-col cols="3" class="text-center">
            <p class="mb-10 text-center font-weight-bold">مسجل الكلية</p>
            <div><span class="dotted-line" style="width: 150px"></span></div>
            <div class="mt-2 d-flex align-center justify-center"></div>
          </v-col>
          <v-col cols="3" class="text-center">
            <p class="mb-10 text-center font-weight-bold">عميد الكلية</p>
            <div><span class="dotted-line" style="width: 150px"></span></div>
            <div class="mt-2 d-flex align-center justify-center"></div>
          </v-col>
          <v-col cols="3" class="text-center">
            <p class="mb-10 text-center font-weight-bold">المسجل العام</p>
            <div><span class="dotted-line" style="width: 150px"></span></div>
            <div class="mt-2 d-flex align-center justify-center"></div>
          </v-col>
          <v-col cols="3" class="text-center">
            <p class="mb-10 text-center font-weight-bold">
              نائب رئيس الجامعة لشؤن الطلاب
            </p>
            <div><span class="dotted-line" style="width: 150px"></span></div>
            <div class="mt-2 d-flex align-center justify-center"></div>
          </v-col>
        </v-row>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "InrollmentCertificateDocument",
  inject: ["context"],
  data() {
    return {
      output_data: this.context?.output_data ?? {},
    };
  },
};
</script>
