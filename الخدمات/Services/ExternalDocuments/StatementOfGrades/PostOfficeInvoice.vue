<template>
  <!-- حافظة توريد بريدية -->
  <v-sheet class="mx-auto document-sheet position-relative overflow-hidden">
    <div class="pa-5 d-flex flex-column flex-grow-1">
      <v-card
        variant="outlined"
        color="grey-lighten-2"
        class="mb-4 text-center py-2 bg-grey-lighten-5 dashed-border"
      >
        <div class="text-[10px] text-grey-darken-2 font-weight-bold mb-0">
          رقم الحافظة الموحد
        </div>
        <div class="text-h5 font-weight-black text-black letter-spacing-2">
          {{
            stage_input_data?.random_number
              ? stage_input_data?.random_number
              : "----"
          }}
        </div>
      </v-card>

      <div class="mb-4">
        <div class="d-flex align-center mb-2">
          <v-icon color="indigo-darken-2" size="x-small" class="ms-1"
            >mdi-account-details</v-icon
          >
          <span class="text-caption font-weight-bold text-indigo-darken-2"
            >بيانات الطالب</span
          >
        </div>

        <v-table
          density="compact"
          class="info-table rounded-lg border text-caption"
        >
          <tbody>
            <tr>
              <td class="text-grey-darken-2 text-body-2 bg-grey-lighten-5 w-25">
                اسم الطالب
              </td>
              <td class="font-weight-bold text-body-2">
                {{
                  stage_input_data?.requester_name
                    ? stage_input_data?.requester_name
                    : "----"
                }}
              </td>
              <td class="text-grey-darken-2 text-body-2 bg-grey-lighten-5">
                رقم القيد
              </td>
              <td class="font-weight-bold text-body-2">{{stage_input_data?.academic_number}}</td>
            </tr>
            <tr>
              <td class="text-grey-darken-2 text-body-2 bg-grey-lighten-5">
                الكلية
              </td>
              <td class="font-weight-bold text-body-2">{{stage_input_data?.college_name}}</td>
              <td class="text-grey-darken-2 text-body-2 bg-grey-lighten-5">
                القسم/التخصص
              </td>
              <td class="font-weight-bold text-body-2">{{stage_input_data?.specialization_name}}</td>
            </tr>
            <tr>
              <td class="text-grey-darken-2 text-body-2 bg-grey-lighten-5">
                نوع الخدمة
              </td>
              <td class="font-weight-bold text-body-2">
                {{stage_input_data?.service_name}}
              </td>
            </tr>
          </tbody>
        </v-table>
        <v-card class="bg-grey-lighten-5 pa-4 mt-3" elevation="0" rounded="lg">
          <div class="d-flex justify-space-between align-center">
            <div>
              <div class="text-[10px] opacity-80 mb-0">
                المبلغ الإجمالي المستحق
              </div>
            </div>
            <div class="text-right">
              <div class="text-h4 font-weight-black">
                {{
                  stage_input_data?.discounted_fee??stage_input_data?.total_fee?? "----"
                }}
                <span class="text-caption">ريال</span>
              </div>
            </div>
          </div>
        </v-card>
      </div>
    </div>
  </v-sheet>
</template>
<script>
export default {
  inject: ["files_data"],
  data() {
    return {
      stage_input_data: this.files_data?.stage_input_data,
    };
  },
};
</script>
<style scoped>
.letter-spacing-2 {
  letter-spacing: 2px;
}

.dashed-border {
  border: 1.5px dashed #bdbdbd !important;
}

/* Compact line heights for A5 text */
.line-height-tight {
  line-height: 1.2 !important;
}

.text-\[10px\] {
  font-size: 10px !important;
}
.text-\[9px\] {
  font-size: 9px !important;
}

.info-table td {
  height: 27px !important; /* Force smaller height */
  border-bottom: 1px solid #eee !important;
}
</style>
