<template>

  <div class="pa-4" >
    <div class="pb-3 text-left">
      <div><strong>رقم الاستمارة:</strong> ....................</div>
      <div class="mt-2"><strong>التاريخ:</strong> {{ output_data?.issue_date }}</div>
    </div>
    <div class="student-info-box rounded-lg pa-3 mb-4 bg-grey-lighten-3 border-thin">
      <v-row no-gutters class="text-body-2 font-weight-bold">
        <v-col cols="12" class="mb-2">
          اسم الطالب :
          <span class="dotted-line">
            {{ output_data?.student_name }}
          </span>
          كلية :
          <span class="dotted-line">
            {{ output_data?.college }}
          </span>
          التخصص :
          <span class="dotted-line">
            {{ output_data?.specialization }}
          </span>
          رقم القيد :
          <span class="dotted-line">
            {{ output_data?.academic_no }}
          </span>
        </v-col>
        <v-col cols="12">
          العام الجامعي :
          {{ output_data?.current_academic_year }}
        </v-col>
      </v-row>
    </div>



    <table class="custom-table mb-2">
        <thead>
          <tr>
            <th>اسم المقرر</th>
            <th class="bg-white">
              {{output_data?.subject_data?.name_ar}}
            </th>
            <th>المستوى</th>
            <th class="bg-white">
              {{output_data?.level}}
            </th>
            <th> الفصل الدراسي</th>
            <th class="bg-white">
              {{output_data?.semester}}
            </th>
          </tr>
          <v-divider></v-divider>
          <tr>
            <th>
              رقم
            </th>
            <th>
              اسم التوزيع
            </th>

            <th colspan="2">
              الدرجة قبل التظلم
            </th>
            <th colspan="2">
              الدرجة بعد التظلم
            </th>

          </tr>

        </thead>
        <tbody>
          <tr v-for="(grade_record,index) in output_data?.subject_data?.grade_records" :key="index">
            <td>
              {{index+1}}
            </td>
            <td>
              {{grade_record.name}}
            </td>

            <td colspan="2">
              {{grade_record.old_grade}}
            </td>
            <td colspan="2">
              {{grade_record.new_grade}}
            </td>

          </tr>
        </tbody>
      </table>

    <div class="footer-signatures d-flex justify-space-between px-8 mt-4">
      <div class="text-center">
        <strong>عضو اللجنة</strong>
      </div>
      <div class="text-center">
        <strong>عضو اللجنة</strong>
      </div>
      <div class="text-center">
        <strong>رئيس الكنترول</strong>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "GrievanceCourseGradeDocument",
  inject: ["context"],
  data() {
    return {
      output_data: this.context?.output_data ?? {},
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
