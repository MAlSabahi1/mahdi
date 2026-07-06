<template>
  <!-- بيان درجات لغير الخريجين -->
  <v-sheet
    v-if="output_data && Object.keys(output_data).length > 0"
    class="mx-auto position-relative overflow-hidden"
  >
    <div class="px-10 py-5 content-wrapper d-flex flex-column">
      <div>
        <v-row>
          <v-col cols="12">
            تشهد جامعة
            {{ output_data.organization_ar ? output_data.organization_ar : "----" }}
            - كلية
            {{
              output_data.specialization_name_ar
                ? output_data.specialization_name_ar
                : "----"
            }}
            بأن الطالب:
            <span class="mx-1 text-indigo-darken-4">{{
              output_data.student_name_ar ? output_data.student_name_ar : "----"
            }}</span>
            المولود في:
            <span class="mx-1 text-indigo-darken-4"
              >{{
                output_data.place_of_brith?.governorate
                  ? output_data.place_of_brith?.governorate
                  : "----"
              }}/{{
                output_data.place_of_brith?.directorate
                  ? output_data.place_of_brith?.directorate
                  : "----"
              }}/{{
                output_data.place_of_brith?.region
                  ? output_data.place_of_brith?.region
                  : "----"
              }}/{{
                output_data.place_of_brith?.street
                  ? output_data.place_of_brith?.street
                  : "----"
              }}</span
            >
            بتاريخ:
            <span class="mx-1 text-indigo-darken-4">{{
              output_data.date_of_birth ? output_data.date_of_birth : "---"
            }}</span>
            <span class="mx-1 text-indigo-darken-4">{{
              output_data.nationality_name_ar ? output_data.nationality_name_ar : "----"
            }}</span>
            الجنسية التحق بالكلية في العام الجامعي
            <span class="mx-1 text-indigo-darken-4">{{
              output_data.enrollment_year_year_h
                ? output_data.enrollment_year_year_h
                : "----"
            }}</span>
            برقم قيد:
            <span class="mx-1 text-indigo-darken-4">{{
              output_data.student_academice_no ? output_data.student_academice_no : "----"
            }}</span>
            بتخصص :
            <span class="mx-1 text-indigo-darken-4">{{
              output_data.specialization_name_ar
                ? output_data.specialization_name_ar
                : "----"
            }}</span>
          </v-col>
          <v-col cols="12" class="my-0 py-0 mb-1"> وقد درس المقررات التالية. </v-col>
        </v-row>
      </div>
      <div v-if="output_data.levels && output_data.levels.length > 0">
        <div v-for="(level, index) in output_data.levels" :key="index">
          <div
            class="bg-grey-lighten-4 d-flex justify-space-between align-center px-4 py-1 mb-1 mt-2 rounded"
          >
            <span class="font-weight-black">المستوى {{ level.level_name }}</span>
            <span class="font-weight-black"
              >العام الجامعي: {{ level.academic_year_year_h }}</span
            >
          </div>

          <div class="grades-container rounded">
            <div
              class="flex-grow-1 border-left-double"
              v-for="(semester, index) in level.semesters"
              :key="index"
            >
              <table class="transcript-table w-100">
                <thead>
                  <tr class="bg-grey-lighten-4">
                    <th colspan="6">{{ semester.name_ar }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(course, i) in semester.subjects" :key="i">
                    <td class="text-center">{{ i + 1 }}</td>
                    <td class="text-right px-2">{{ course.name_ar }}</td>
                    <td class="text-center font-weight-bold">
                      {{ course.number_of_hours }}
                    </td>
                    <td class="text-center font-weight-bold">
                      {{ course.grades }}
                    </td>
                    <td class="text-center">{{ course.estimate }}</td>
                  </tr>
                </tbody>
                <tfoot>
                  <tr class="bg-grey-lighten-4 font-weight-bold">
                    <td colspan="2" class="text-left px-2">معدل الفصل:</td>
                    <td colspan="3" class="text-center">{{ semester.avg }}%</td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <div
          class="bg-grey-lighten-4 d-flex justify-space-between align-center px-4 py-1 mb-1"
        >
          <span class="font-weight-black">المستوى ####</span>
          <span class="font-weight-black">العام الجامعي: ####</span>
        </div>

        <div class="d-flex flex-row grades-container">
          <div class="flex-grow-1 border-left-double">
            <table class="transcript-table w-100">
              <thead>
                <tr class="bg-grey-lighten-4">
                  <th colspan="6">####</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="text-center">{{ i + 1 }}</td>
                  <td class="text-right px-2">####</td>
                  <td class="text-center font-weight-bold">####</td>
                  <td class="text-center font-weight-bold">####</td>
                  <td class="text-center">####</td>
                </tr>
              </tbody>
              <tfoot>
                <tr class="bg-grey-lighten-4 font-weight-bold">
                  <td colspan="2" class="text-left px-2">معدل الفصل:</td>
                  <td colspan="3" class="text-center">####%</td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>
      </div>

      <div class="cumulative-box d-flex justify-center">
        <div class="pa-2 text-center">
          <span class="text-subtitle-1 font-weight-black"
            >المعدل التراكمي العام (GPA):
          </span>
          <span class="text-h6 font-weight-black text-indigo-darken-4 mx-2">####%</span>
        </div>
      </div>
      <v-spacer></v-spacer>
    </div>
  </v-sheet>
  <v-sheet v-else class="d-flex flex-column align-center justify-center">
    <div class="px-10 py-5 font-weight-bold text-grey-darken-2 mb-2">
      <div class="text-center">
        <v-icon size="120">mdi-database-off-outline</v-icon>
        <div class="text-h5 font-weight-black py-1 px-6 d-inline-block">
          لاتوجد بيانات!!
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
      output_data: this.context.output_data,
    };
  },
};
</script>

<style scoped>
/* Text Styles */
.label {
  color: #616161;
  font-size: 0.85rem;
}

/* Transcript Tables */
.grades-container {
  border: 1px solid #000;
  display: grid;
  grid-template-columns: 1fr 1fr;
}
.transcript-table {
  border-collapse: collapse;
}
.transcript-table th,
.transcript-table td {
  border: 1px solid #000;
  font-size: 0.72rem;
  padding: 2px;
  /* height: 1px; */
}
.border-left-double {
  border-left: 3px double #000 !important;
}
.border-right-white {
  border-right-color: #fff !important;
}
</style>
