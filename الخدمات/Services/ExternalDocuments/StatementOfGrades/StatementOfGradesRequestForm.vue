<template>
  <!-- طلب بيانات لغير الخريجين -->
  <v-sheet class="mx-auto position-relative overflow-hidden">
    <div class="px-10 py-5 content-wrapper fill-height d-flex flex-column">
      <div class="section-title mb-4">
        <span>بيانات مقدم الطلب</span>
      </div>

      <v-table density="compact" class="info-table rounded-lg border text-caption">
        <tbody>
          <tr>
            <td class="text-grey-darken-2 text-body-2 bg-grey-lighten-5 w-25">
              اسم الطالب
            </td>
            <td class="font-weight-bold text-body-2">
              {{ input_data?.student_name_ar ? input_data?.student_name_ar : "----" }}
            </td>
            <td class="text-grey-darken-2 text-body-2 bg-grey-lighten-5">رقم القيد</td>
            <td class="font-weight-bold text-body-2">
              {{
                input_data?.student_academice_no
                  ? input_data?.student_academice_no
                  : "----"
              }}
            </td>
          </tr>
          <tr>
            <td class="text-grey-darken-2 text-body-2 bg-grey-lighten-5">الكلية</td>
            <td class="font-weight-bold text-body-2">
              {{ input_data?.college_name_ar }}
            </td>
            <td class="text-grey-darken-2 text-body-2 bg-grey-lighten-5">القسم/التخصص</td>
            <td class="font-weight-bold text-body-2">
              {{
                input_data?.specialization_name_ar
                  ? input_data?.specialization_name_ar
                  : "----"
              }}
            </td>
          </tr>
          <tr>
            <td class="text-grey-darken-2 text-body-2 bg-grey-lighten-5">
              الحالة الدراسية
            </td>
            <td class="font-weight-bold text-body-2">
              {{ input_data?.student_status ? input_data?.student_status : "----" }}
            </td>
            <td class="text-grey-darken-2 text-body-2 bg-grey-lighten-5">
              العام الدراسي
            </td>
            <td class="font-weight-bold text-body-2">
              {{ input_data?.academic_year_m ? input_data?.academic_year_m : "----" }}
              /
              {{ input_data?.academic_year_h ? input_data?.academic_year_h : "----" }}
            </td>
          </tr>
        </tbody>
      </v-table>

      <div class="section-title mt-4 mb-4">
        <span>تفاصيل المستند المطلوب</span>
      </div>

      <div class="border rounded-lg mb-8 bg-grey-lighten-5 shadow-sm">
        <v-row>
          <v-col cols="6" class="border-bottom-dotted">
            <span class="label d-block mb-1"
              >الغرض من الطلب:
              <span class="val font-weight-bold text-indigo-darken-4">{{
                input_data?.service_version?.purpose_name
                  ? input_data?.service_version?.purpose_name
                  : input_data?.service_version?.purpose
              }}</span></span
            >
          </v-col>
          <v-col cols="6" class="border-bottom-dotted">
            <span class="label d-block mb-1"
              >الجهة الموجه إليها:
              <span class="val font-weight-bold">{{
                input_data?.service_version?.destination_entity
                  ? input_data?.service_version?.destination_entity
                  : "----"
              }}</span></span
            >
          </v-col>
          <v-col cols="4" class="pt-4">
            <span class="label">لغة الوثيقة:</span>
            <span class="val font-weight-bold ms-2">{{
              input_data?.service_version?.language_name
                ? input_data?.service_version?.language_name
                : input_data?.service_version?.language
            }}</span>
          </v-col>
          <v-col cols="4" class="pt-4">
            <span class="label">عدد النسخ:</span>
            <span class="val font-weight-bold ms-2">{{
              input_data?.service_version?.copies_count
                ? input_data?.service_version?.copies_count
                : "----"
            }}</span>
          </v-col>
          <v-col cols="4" class="pt-4 text-left">
            <span class="label">رسوم الاستخراج:</span>
            <span class="val font-weight-bold ms-2">{{
              input_data?.payment_status ? input_data?.payment_status : "----"
            }}</span>
          </v-col>
        </v-row>
      </div>

      <div class="declaration-box pa-6 border rounded-lg mb-12">
        <div class="d-flex align-start">
          <v-icon color="indigo-darken-4" class="mt-1 me-3"
            >mdi-checkbox-marked-outline</v-icon
          >
          <p
            class="text-body-1 font-weight-bold mb-0 text-justify"
            style="line-height: 1.8"
          >
            أنا الطالب الموضح اسمي أعلاه، أقر بصحة البيانات الواردة في هذا الطلب، وأتحمل
            المسؤولية القانونية في حال ثبت خلاف ذلك، كما أفوض الجامعة بخصم الرسوم المقررة
            من رصيدي المالي.
          </p>
        </div>
      </div>
    </div>
  </v-sheet>
</template>

<script>
export default {
  inject: ["context"],
  data() {
    return {
      input_data: this.context.input_data,
    };
  },
};
</script>

<style scoped>
.section-title {
  font-weight: 900;
  color: #1a237e;
  border-right: 6px solid #1a237e;
  padding-right: 15px;
  font-size: 1.1rem;
}

.info-card {
  border: 2px solid #5c5c5c !important;
  border-radius: 8px !important;
}

.label {
  color: #5c5c5c;
  font-size: 0.85rem;
  font-weight: 600;
}

.val {
  color: #000;
  font-size: 0.95rem;
}

.border-b {
  border-bottom: 1px solid #e0e0e0 !important;
}
.border-e {
  border-right: 1px solid #e0e0e0 !important;
}

.border-bottom-dotted {
  border-bottom: 1px dotted #ccc;
}

.declaration-box {
  background-color: #fcfcfc;
  border: 1px dashed #1a237e !important;
}

.signature-label {
  font-weight: 800;
  color: #1a237e;
  font-size: 0.9rem;
}

.stamp-placeholder {
  width: 100px;
  height: 100px;
  border: 2px dashed #ccc;
  border-radius: 50%;
}
</style>
