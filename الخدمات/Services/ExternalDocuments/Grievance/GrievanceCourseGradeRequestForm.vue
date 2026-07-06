<template>
  <div class="pa-4">
    <div class="d-flex">
      <div>
        <div class="pb-3">
          <div><strong>رقم الاستمارة:</strong> ....................</div>
          <div class="mt-2">
            <strong>التاريخ:</strong> {{ input_data?.issue_date }}
          </div>
        </div>
      </div>
    </div>
    <div
      class="
        student-info-box
        rounded-lg
        pa-3
        mb-4
        bg-grey-lighten-3
        border-thin
      "
    >
      <v-row no-gutters class="text-body-2 font-weight-bold">
        <v-col cols="12" class="mb-2">
          اسم الطالب :

          <span class="dotted-line">
            {{ input_data?.student_name }}
          </span>
          كلية :
          <span class="dotted-line">
            {{ input_data?.college }}
          </span>
          التخصص :
          <span class="dotted-line">
            {{ input_data?.specialization }}
          </span>
          رقم القيد :
          <span class="dotted-line">
            {{ input_data?.academic_no }}
          </span>
        </v-col>
        <v-col cols="12">
          العام الجامعي :
          <span class="dotted-line">
            {{ input_data?.current_academic_year }}
          </span>
        </v-col>
      </v-row>
    </div>

    <div class="mb-2">
      <div class="mb-2 pr-2">
        <strong
          >الأخ الدكتور/ عميد كلية :
          <span class="dotted-line">
            {{ input_data?.college }}
          </span>
        </strong>
        <span class="float-left ml-4"><strong>المحترم</strong></span>
      </div>
      <div class="text-center mb-2">
        أرجو قبول تظلمي في المواد المبينة أدناه
      </div>

      <table class="custom-table mb-2">
        <thead>
          <tr>
            <th>اسم المقرر</th>
            <th class="bg-white">
              {{ input_data?.subject_data?.name_ar }}
            </th>
            <th>المستوى</th>
            <th class="bg-white">
              {{ input_data?.level }}
            </th>
            <th>الفصل الدراسي</th>
            <th class="bg-white">
              {{ input_data?.semester }}
            </th>
          </tr>
          <v-divider></v-divider>
          <tr>
            <th>رقم</th>
            <th>اسم التوزيع</th>
            <th>اقصى درجة في التوزيع</th>
            <th>الدرجة الحاصل عليها الطالب</th>
            <th colspan="2" rowspan="3">سبب التظلم</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(grade_record, index) in input_data?.subject_data
              .grades_records"
            :key="index"
          >
            <td>
              {{ index + 1 }}
            </td>
            <td>
              {{ grade_record.name }}
            </td>
            <td>
              {{ grade_record.max_grade }}
            </td>
            <td>
              {{ grade_record.grade }}
            </td>
            <td colspan="2">----</td>
          </tr>
        </tbody>
      </table>

      <v-row no-gutters class="mb-4">
        <v-col cols="6" class="text-right">
          تاريخ :
          {{ input_data?.issue_date }}
        </v-col>
        <v-col cols="6" class="text-left pl-10">
          <strong>التوقيع :</strong> ....................
        </v-col>
      </v-row>
    </div>

    <v-divider class="border-opacity-100 mb-2"></v-divider>
  </div>
</template>

<script>
export default {
  name: "GrievanceCourseGradeRequestForm",
  inject: ["context"],
  data() {
    return {
      input_data: this.context?.input_data ?? {},
    };
  },
};
</script>

<style scoped>
/* صندوق بيانات الطالب */
.student-info-box {
  border: 1px solid #aaa;
}

/* تنسيق الجداول */
.custom-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8rem;
}

.custom-table th,
.custom-table td {
  border: 1px solid #000;
  padding: 4px;
  text-align: center;
}

.custom-table th {
  background-color: #e0e0e0; /* رمادي فاتح للعناوين */
  font-weight: bold;
}

/* ارتفاع ثابت لصفوف الجدول لتبدو مثل الصورة */
.custom-table td {
  height: 25px;
}

/* فواصل الأقسام */
.section-header {
  border-radius: 4px;
  font-size: 0.9rem;
}

.dashed-separator {
  border-top: 2px dashed #000;
  width: 100%;
}

.border-all {
  border: 1px solid #000;
}
</style>
