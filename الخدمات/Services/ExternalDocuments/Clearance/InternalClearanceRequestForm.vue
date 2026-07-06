<template>
  استمارة طلب مقاصة داخلية
  <div>
    <div class="content-border-wrapper">
      <div class="inner-content">
        <!-- Form Meta Box -->
        <div class="form-meta-box mb-6 pa-3">
          <div class="info-line mb-0">
            <span class="label">رقم الإستمارة :</span>
            <span class="value dotted-line" style="min-width: 150px"></span>
            <v-spacer></v-spacer>
            <span class="label mr-4">التاريخ :</span>
            <span class="value dotted-line" style="min-width: 150px"
              >{{input_data?.issue_date}}</span
            >
          </div>
        </div>

        <!-- Basic Student Info Section -->
        <div class="section-header mb-4">
          <span class="section-title">البيانات الأساسية للطالب</span>
        </div>
        <div class="student-info-section mb-6">
          <v-row dense>
            <v-col cols="12">
              <div class="info-line">
                <span class="label">اسم الطالب :</span>
                <span class="value dotted-line flex-grow-1">{{input_data?.student_name}}</span>
                <span class="label mr-4">رقم القيد :</span>
                <span class="value dotted-line" style="min-width: 120px">{{input_data?.academic_no}}</span>
              </div>
            </v-col>
            <v-col cols="12">
              <div class="info-line">
                <span class="label">التخصص الحالي :</span>
                <span class="value dotted-line flex-grow-1">{{input_data?.old_specialization}}</span>
                <span class="label mr-4">المعدل التراكمي :</span>
                <span class="value dotted-line" style="min-width: 120px"
                  >{{input_data?.avg}}</span
                >
              </div>
            </v-col>
          </v-row>
        </div>

        <!-- Transfer Details Section -->
        <div class="section-header mb-4">
          <span class="section-title">تفاصيل التحويل المطلوب</span>
        </div>
        <div class="transfer-details-section mb-6">
          <v-row dense>
            <v-col cols="12" class="mb-4">
              <div class="info-line">
                <span class="label">القسم المطلوب التحويل إليه :</span>
                <span class="value dotted-line flex-grow-1">{{input_data?.new_specialization}}</span>
              </div>
            </v-col>
            <!-- <v-col cols="12">
              <div class="info-line align-start">
                <span class="label">سبب طلب التحويل :</span>
                <div class="flex-grow-1">
                  <div class="value dotted-line w-100 text-right mb-2">
                    الرغبة في التخصص الدقيق في مجال بناء وتطوير الأنظمة البرمجية الواسعة.
                  </div>
                  <div class="dotted-line w-100" style="height: 20px"></div>
                </div>
              </div>
            </v-col> -->
          </v-row>
        </div>

        <!-- Courses Table Section -->
        <div class="section-header mb-4">
          <span class="section-title">المقررات المطلوب معادلتها</span>
        </div>
        <div class="main-table-container mb-6">
          <table class="equivalence-table">
            <thead>
              <tr>
                <th class="serial-col">م</th>
                <th class="course-col">المقرر المنجز (السابق)</th>
                <th class="course-col">المقرر المعادل (الجديد)</th>
                <th class="grade-col">الدرجة</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(i, index) in input_data.table_data" :key="index">
                <td class="text-center">{{ index + 1 }}</td>
                <td class="text-center">{{ i.completed_subject }}</td>
                <td>{{ i.equivalent_subject }}</td>
                <td class="text-center">{{ i.grade }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Declaration Box -->
        <div class="declaration-box mb-6 pa-4">
          أقر أنا الطالب المذكور أعلاه بصحة البيانات الواردة في هذه الاستمارة، وبأني اطلعت
          على لائحة المقاصة بالجامعة وأتحمل كامل المسؤولية عن أي نقص في الأوراق أو
          البيانات المقدمة.
        </div>
      </div>
    </div>

    <!-- Footer Signatures -->
    <!-- <div class="footer-signatures mt-8">
        <v-row no-gutters>
          <v-col cols="4" class="pa-4">
            <div class="signature-item text-center">
              <span class="label mb-4 d-block">توقيع الطالب</span>
              <div class="sig-line-with-label">
                <span>التاريخ:</span>
                <span class="dotted-line flex-grow-1">.... / .... / 2024م</span>
              </div>
              <div class="sig-line-with-label mt-2">
                <span>الاسم:</span>
                <span class="dotted-line flex-grow-1">................................</span>
              </div>
            </div>
          </v-col>
          <v-col cols="4" class="pa-4">
            <div class="signature-item text-center">
              <span class="label mb-4 d-block">الموظف المختص</span>
              <div class="sig-line-with-label mt-8">
                <span>الاسم:</span>
                <span class="dotted-line flex-grow-1">................................</span>
              </div>
            </div>
          </v-col>
          <v-col cols="4" class="pa-4">
            <div class="signature-item text-center">
              <span class="label mb-4 d-block">اعتماد شؤون الطلاب</span>
              <div class="sig-line mt-10"></div>
            </div>
          </v-col>
        </v-row>
      </div> -->
  </div>
</template>

<script>
export default {
  name: "InternalStudentTransferRequestForm",
  inject: ["context"],
  data() {
    return {
      input_data: this.context?.input_data ?? {},
    };
  },
};
</script>

<style scoped>
.content-border-wrapper {
  border-radius: 15px;
  position: relative;
}

.form-meta-box {
  background-color: #f5f5f5;
  border: 1px solid #cccccc;
  border-radius: 10px;
}

.section-header {
  border-right: 5px solid #1b2f5e;
  padding-right: 10px;
}

.section-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #1b2f5e;
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

.equivalence-table {
  width: 100%;
  border-collapse: collapse;
  border: 1.5px solid #1b2f5e;
}

.equivalence-table th,
.equivalence-table td {
  border: 1px solid #1b2f5e;
  padding: 8px 6px;
  height: 35px;
  font-size: 0.95rem;
}

.equivalence-table thead th {
  background-color: #f5f5f5;
  color: #1b2f5e;
  font-weight: bold;
}

.serial-col {
  width: 40px;
}
.grade-col {
  width: 80px;
}

.declaration-box {
  border: 2px dashed #000;
  background-color: #fcfcfc;
  font-size: 1rem;
  font-weight: bold;
  text-align: center;
  line-height: 1.6;
}

.sig-line {
  border-bottom: 1px solid #1b2f5e;
  width: 100%;
  height: 25px;
}
</style>
