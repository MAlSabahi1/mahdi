<template>
  <!-- سند تسديد رسوم الحافظة -->
  <v-sheet class="mx-auto document-sheet position-relative overflow-hidden">
    <div class="pa-5 content-wrapper position-relative d-flex flex-column flex-grow-1">
      <div class="meta-grid mb-4">
        <div class="meta-item">
          <span class="label">رقم الفاتورة</span>
          <span class="value">{{
            stage_output_data?.request_number ? stage_output_data?.request_number : "----"
          }}</span>
        </div>
        <div class="meta-item">
          <span class="label">التاريخ</span>
          <span class="value">{{
            stage_output_data?.requested_at ? stage_output_data?.requested_at : "----"
          }}</span>
        </div>
        <div class="meta-item">
          <span class="label">العام</span>
          <span class="value">24-25</span>
        </div>
        <div class="meta-item bg-green-lighten-5 border-green">
          <span class="label text-green-darken-2">الحالة</span>
          <span class="value text-green-darken-3 font-weight-black">
            {{
              stage_output_data?.payment_status
                ? stage_output_data?.payment_status
                : "----"
            }}
          </span>
        </div>
      </div>

      <div class="section-box mb-4">
        <div class="section-header py-1 px-3">
          <v-icon size="x-small" start>mdi-account-school</v-icon>
          بيانات الطالب
        </div>
        <v-row no-gutters class="pa-2">
          <v-col cols="6" class="mb-1">
            <div class="text-[9px] text-grey-darken-1">
              الاسم:
              <span class="text-caption font-weight-bold text-indigo-darken-4">
                {{
                  stage_output_data?.requester_name
                    ? stage_output_data?.requester_name
                    : "----"
                }}
              </span>
            </div>
          </v-col>
          <v-col cols="6" class="mb-1">
            <div class="text-[9px] text-grey-darken-1">
              الرقم الأكاديمي:
              <span class="text-caption font-weight-bold"> 203009 </span>
            </div>
          </v-col>
          <v-col cols="6">
            <div class="text-[9px] text-grey-darken-1">
              الكلية:
              <span class="text-[10px] font-weight-bold"> الكلية الحربية </span>
            </div>
          </v-col>
          <v-col cols="6">
            <div class="text-[9px] text-grey-darken-1">
              التخصص:
              <span class="text-[10px] font-weight-bold">الرماية وركوب الخيل</span>
            </div>
          </v-col>
        </v-row>
      </div>

      <div class="mb-2 flex-grow-1">
        <v-table density="compact" class="invoice-table">
          <thead>
            <tr>
              <th class="text-center w-10 py-1">#</th>
              <th class="text-right w-50 py-1">البيان</th>
              <th class="text-center w-10 py-1">عدد</th>
              <th class="text-center w-15 py-1">السعر</th>
              <th class="text-center w-15 py-1">الإجمالي</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="text-center text-grey">1</td>
              <td class="font-weight-medium text-[10px]">رسوم بيان درجات</td>
              <td class="text-center">1</td>
              <td class="text-center text-[10px]">750</td>
              <td class="text-center font-weight-bold text-[10px]">750</td>
            </tr>
            <tr>
              <td class="text-center text-grey">2</td>
              <td class="font-weight-medium text-[10px]">رسوم مصادقة</td>
              <td class="text-center">1</td>
              <td class="text-center text-[10px]">750</td>
              <td class="text-center font-weight-bold text-[10px]">750</td>
            </tr>
          </tbody>
        </v-table>
        <v-card elevation="0" class="bg-grey-lighten-5 pa-4 mt-3">
          <div class="d-flex justify-space-between align-center">
            <div>
              <div class="d-flex justify-space-between text-[9px] mb-1">
                <span class="text-grey-darken-2">المرجع:</span>
                <span class="font-weight-bold">TXN-4492</span>
              </div>
              <div class="d-flex justify-space-between text-[9px]">
                <span class="text-grey-darken-2">التاريخ:</span>
                <span class="">2026-01-06</span>
              </div>
            </div>
            <div>
              <div class="text-[8px] opacity-70 mb-0">الإجمالي المستحق</div>
              <div class="text-h4 font-weight-black mb-0">
                {{ stage_output_data?.total_fee ? stage_output_data?.total_fee : "----" }}
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
      stage_output_data: this.files_data?.stage_output_data,
    };
  },
};
</script>
<style scoped>
.color-navy {
  color: #1a237e;
}
.color-gold {
  color: #c5a059;
}

/* Small Text Utilities */
.text-\[8px\] {
  font-size: 8px !important;
}
.text-\[9px\] {
  font-size: 9px !important;
}
.text-\[10px\] {
  font-size: 10px !important;
}

/* Grid for Invoice Meta */
.meta-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px; /* Smaller gap */
}
.meta-item {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 4px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: #fff;
}
.meta-item .label {
  font-size: 0.6rem;
  color: #757575;
}
.meta-item .value {
  font-size: 0.75rem;
  font-weight: 700;
  color: #1a237e;
}

/* Section Box Styling */
.section-box {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
}
.section-header {
  background-color: #f5f5f5;
  font-weight: bold;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
}

/* Table Styling */
.invoice-table {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
}
.invoice-table thead th {
  background-color: #f5f5f5 !important;
  color: #424242 !important;
  font-weight: 800 !important;
  font-size: 0.7rem !important;
  border-bottom: 2px solid #e0e0e0 !important;
  height: 30px !important;
}
.invoice-table td {
  padding-top: 4px !important;
  padding-bottom: 4px !important;
  height: 30px !important;
}
</style>
