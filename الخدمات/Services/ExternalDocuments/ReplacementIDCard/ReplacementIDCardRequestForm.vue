<template>
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
                <span class="value dotted-line" style="min-width: 120px">{{input_data?.student_academic_no}}</span>
              </div>
            </v-col>
            <v-col cols="12">
              <div class="info-line">
                <span class="label">الكلية  :</span>
                <span class="value dotted-line flex-grow-1">{{input_data?.collage_name_ar}}</span>
                <span class="label">التخصص  :</span>
                <span class="value dotted-line flex-grow-1">{{input_data?.specialization_name_ar}}</span>

              </div>
            </v-col>
            <v-col cols="12">
              <div class="info-line">
                <span class="label">المستوى  :</span>
                <span class="value dotted-line flex-grow-1">{{input_data?.level}}</span>


                <span class="label">العام الجامعي  :</span>
                <span class="value dotted-line flex-grow-1">{{input_data?.academic_year_m}}</span>

              </div>
            </v-col>
          </v-row>
        </div>






        <!-- Declaration Box -->
        <div class="declaration-box mb-6 pa-4">أرجو التكرم بالموافقة على استخراج بطاقة جامعية (بدل فاقد) بدلاً عن بطاقتي المفقودة، وأقر أنا الطالب المذكور أعلاه بمسؤوليتي الكاملة في حال العثور عليها أو سوء استخدامها.
        </div>
      </div>
    </div>

  </div>

</template>
<script>
export default {
  name: "ReplacementIDCardRequestForm",
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
