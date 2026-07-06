<template>
  مقاصة داخلية

  <div>
    <!-- Main Content Wrapper with Border -->
    <div class="inner-content">
      <!-- Form Meta Box -->
      <div class="form-meta-box mb-6 pa-3">
        <div class="info-line mb-0">
          <span class="label">رقم الإستمارة :</span>
          <span class="value dotted-line" style="min-width: 150px"
            >....................</span
          >
          <v-spacer></v-spacer>
          <span class="label mr-4">التاريخ :</span>
          <span class="value dotted-line" style="min-width: 150px">
            {{ output_data?.issue_date }}
          </span>
        </div>
      </div>

      <!-- Student Info Section -->
      <div class="student-info-section mb-2">
        <v-row dense>
          <v-col cols="12">
            <div class="info-line">
              <span class="value dotted-line flex-grow-1">
                {{ output_data?.student_info?.name }}
              </span>
              <span class="label mr-4">للعام الجامعي :</span>
              <span class="value dotted-line" style="min-width: 150px">
                {{ output_data?.student_info?.academic_year }}
              </span>
              <span class="label mr-4">المستوى :</span>
              <span class="value dotted-line" style="min-width: 50px">
                {{ output_data?.student_info?.level }}
              </span>
            </div>
          </v-col>
          <v-col cols="12">
            <div class="info-line">
              <span class="label">رقم القيد :</span>
              <span class="value dotted-line" style="min-width: 150px">
                {{ output_data?.student_info?.academic_no }}
              </span>
              <span class="label mr-4">المحول من تخصص :</span>
              <span class="value dotted-line flex-grow-1">
                {{ output_data?.student_info?.old_specialization }}
              </span>
            </div>
          </v-col>
          <v-col cols="12">
            <div class="info-line">
              <span class="label">إلى تخصص :</span>
              <span class="value dotted-line flex-grow-1">
                {{ output_data?.student_info?.new_specialization }}
              </span>
              <span class="label mr-4">بالكلية وفقاً للإجراءات التالية :</span>
            </div>
          </v-col>
        </v-row>
      </div>

      <!-- Separator Line -->
      <div class="section-divider mb-2"></div>

      <!-- Main Equivalence Table -->
      <div class="main-table-container mb-4">
        <template v-for="level in output_data?.levels_list" :key="level">
          <div
            class="bg-grey-lighten-4 d-flex justify-space-between align-center px-4 py-1 mb-1 mt-2 rounded"
          >
            <span class="font-weight-black">المستوى:
              <span class="dotted-line">{{ level.name }}</span>
            </span>
            <span class="font-weight-black"
              >العام الجامعي:
              <span class="dotted-line">{{ level.academic_year }}</span>
              </span
            >
          </div>
          <table class="equivalence-table my-2">

            <thead>
              <tr>
                <th rowspan="2" class="course-col">الفصل الدراسي</th>
                <th rowspan="2" class="course-col">مقررات التخصص</th>
                <th rowspan="2" class="hours-col">ساعات</th>
                <th colspan="4" class="equivalent-header">
                  المقررات المعادلة التي درسها الطالب بمكانها
                </th>
                <th rowspan="2" class="notes-col">ملاحظات</th>
              </tr>
              <tr>
                <th class="course-sub-col">المقررات</th>
                <th class="hours-sub-col">ساعات</th>
                <th class="grade-col">الدرجة</th>
                <th class="appreciation-col">التقدير</th>
              </tr>
            </thead>
            <tbody>
              <template
                v-for="(semester, semester_index) in level?.semesters"
                :key="semester_index"
              >
                <tr
                  v-for="(subject, subject_index) in semester?.subjects"
                  :key="subject_index"
                >
                  <th>{{ semester?.name }}</th>
                  <th>{{ subject?.old_subject_name }}</th>
                  <th>{{ subject?.old_hours }}</th>
                  <th>{{ subject?.new_subject_name }}</th>
                  <th>{{ subject?.new_hours }}</th>
                  <th>{{ subject?.new_grade }}</th>
                  <th>{{ subject?.new_estimate }}</th>
                  <th>---</th>
                </tr>
              </template>
            </tbody>
          </table>

          <!-- Bottom Tables Section -->
          <v-row class="mb-4" no-gutters>
            <v-col cols="6" class="pl-1" v-if="level?.remaining_subjects?.length>0">
              <table class="sub-table">
                <thead>
                  <tr>
                    <th class="serial-col">م</th>
                    <th>المقررات المتبقية على الطالب</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(subject, subject_index) in level?.remaining_subjects" :key="subject_index">
                    <td class="text-center">{{ subject_index+1 }}</td>
                    <td>
                      {{subject?.subject_name}}
                    </td>
                  </tr>
                </tbody>
              </table>
            </v-col>
            <v-col cols="6" class="pr-1">
              <table class="sub-table">
                <thead>
                  <tr>
                    <th class="serial-col">م</th>
                    <th>المقررات التي يعفى منها الطالب</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="i in 5" :key="'exc-' + i">
                    <td class="text-center">{{ i }}</td>
                    <td></td>
                  </tr>
                </tbody>
              </table>
            </v-col>
          </v-row>
          <VDivider opacity="1" thickness="3px" class="my-2"/>
        </template>
      </div>

      <!-- Level Determination Box -->
      <div class="determination-box mt-4 mb-2 pa-4">
        تحدد أن يكون الطالب في المستوى :
        <span class="dotted-line px-4" style="min-width: 100px">
          {{output_data?.student_info?.new_level}}
        </span>
        ، وفقاً للمقاصة بعدد المقررات :
        <span class="dotted-line px-4" style="min-width: 100px"></span>
      </div>
    </div>

    <!-- Footer Signatures -->
    <div class="footer-signatures">
      <v-row no-gutters>
        <v-col cols="3" class="pa-2">
          <div class="signature-item">
            <span class="label">مسؤول القسم :</span>
            <div class="sig-line"></div>
          </div>
        </v-col>
        <v-col cols="3" class="pa-2">
          <div class="signature-item">
            <span class="label">رئيس قسم القبول :</span>
            <div class="sig-line"></div>
          </div>
        </v-col>
        <v-col cols="3" class="pa-2">
          <div class="signature-item">
            <span class="label">مدير شؤون الطلاب :</span>
            <div class="sig-line"></div>
          </div>
        </v-col>
        <v-col cols="3" class="pa-2">
          <div class="signature-item">
            <span class="label">مسجل الكلية :</span>
            <div class="sig-line"></div>
          </div>
        </v-col>
      </v-row>
      <v-row no-gutters class="mt-4">
        <v-col cols="6" class="pa-2">
          <div class="signature-item">
            <span class="label">رئيس القسم العلمي المحول إليه الطالب :</span>
            <div class="sig-line"></div>
          </div>
        </v-col>
        <v-col cols="6" class="pa-2">
          <div class="signature-item">
            <span class="label">يعتمد / عميد الكلية :</span>
            <div class="sig-line"></div>
          </div>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
export default {
  name: "InternalEquivalence",
  inject: ["context"],
  data() {
    return {
      output_data: this.context?.output_data ?? {},
    };
  },
};
</script>

<style scoped>
.inner-content {
  padding: 40px 30px;
}

.form-meta-box {
  background-color: #f5f5f5;
  border: 1px solid #bcbcbc;
  border-radius: 10px;
}

.info-line {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  font-size: 1.1rem;
}

.label {
  font-weight: bold;
  color: #1b2f5e;
  white-space: nowrap;
}

.dotted-line {
  border-bottom: 1px dotted #000;
  padding: 0 10px;
  text-align: center;
  margin: 0 5px;
}

.section-divider {
  border-top: 1.5px solid #1b2f5e;
  width: 100%;
}

.equivalence-table,
.sub-table {
  width: 100%;
  border-collapse: collapse;
  border: 1.5px solid #1b2f5e;
}

.equivalence-table th,
.equivalence-table td,
.sub-table th,
.sub-table td {
  border: 1px solid #1b2f5e;
  padding: 6px 4px;
  height: 32px;
  font-size: 0.9rem;
}
.sub-table th {
  background-color: #f5f5f5;
}

.equivalence-table thead th {
  background-color: #f5f5f5;
  color: #1b2f5e;
  font-weight: bold;
}

.serial-col {
  width: 35px;
}
.hours-col,
.hours-sub-col {
  width: 55px;
}
.grade-col,
.appreciation-col {
  width: 65px;
}
.semester-header {
  width: 40px;
  border: none !important;
  background: transparent !important;
}

.semester-label {
  background-color: #f5f5f5;
  width: 40px;
  text-align: center;
  vertical-align: middle;
  border-right: 1.5px solid #1b2f5e !important;
}

.vertical-text {
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  font-weight: bold;
  color: #1b2f5e;
  white-space: nowrap;
  font-size: 1rem;
}

.determination-box {
  border: 2px solid #1b2f5e;
  border-radius: 20px;
  background-color: #f9fbf9;
  font-size: 1.1rem;
  font-weight: bold;
  text-align: center;
  color: #1b2f5e;
}

.sig-line {
  border-bottom: 1px solid #1b2f5e;
  width: 100%;
  height: 25px;
  margin-top: 5px;
}
</style>
