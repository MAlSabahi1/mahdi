<template>
  استمارة طلب اعادة قيد
  {{ input_data }}
  <v-container fluid class="pa-0 align-start justify-center no-print-bg">
    <v-card flat class="pa-8">
      <!-- Main Content Wrapper with Border -->
      <div class="content-border-wrapper">
        <div class="inner-content">
          <!-- Form Meta Box -->
          <div class="form-meta-box mb-6 pa-3">
            <div class="info-line mb-0">
              <span class="label">الأخ الدكتور/عميد</span>
              <span class="label dotted-line">{{ input_data.college }}</span>
              <v-spacer></v-spacer>
              <span class="label">المحترم</span>
            </div>
            <div
              class="mt-2 mb-4"
              style="justify-content: center !important, display:flex"
            >
              <span class="label">تحية طيبة وبعد:</span>
            </div>
            <div class="info-line mb-0">
              <span class="label mr-4">أنا الطالب:</span>
              <span class="value mr-2 dotted-line">{{ input_data.student_name }}</span>
              <span class="label mr-4">مقيد في:</span>
              <span class="value mr-2">كلية </span>
              <span class="value mr-2 dotted-line">{{ input_data.college }} </span>
              <span class="label mr-4">برقم قيد:</span>
              <span class="value mr-2 dotted-line">{{ input_data.student_id }}</span>
            </div>
            <div class="info-line mb-0 mt-2">
              <span class="label mr-4">المستوى:</span>
              <span class="value mr-2 dotted-line">{{ input_data.level }}</span>
              <span class="label mr-4"
                >اتقدم اليكم بطلب إعادة قيدي ابتداء من الفصل الدراسي:</span
              >
              <span class="value mr-2 dotted-line">{{ input_data.semester }}</span>
              <span class="label mr-4">من العام الجامعي:</span>
              <span class="mr-2 dotted-line">{{ input_data.new_batch }}</span>
            </div>
            <div class="info-line mb-0 mt-2">
              <span class="label mr-4">تاريخ:</span>
              <span class="value mr-2 dotted-line">{{ input_data.date_today }}</span>
            </div>
            <div class="info-line mb-0 mt-2">
              <span class="label" style="margin-right: 250px">التوقيع:</span>
              <span class="value dotted-line flex-grow-1"></span>
            </div>
          </div>

          <!-- Basic Student Info Section -->
          <div class="section-header mb-4">
            <span class="section-title">شؤون الطلبة</span>
          </div>
          <div class="mb-6">
            <div class="info-line mb-0">
              <span class="label">الأخ / ت :شؤون الطلبة </span>
              <v-spacer></v-spacer>
              <span class="label">المحترم / ة</span>
            </div>
            <div class="mt-2 mb-4 justify-center d-flex">
              <span class="label">بعد التحية</span><br />
              <span class="label">لإتخاذ الاجراءات بحسب النظام واللوئح المنظمة</span>
            </div>
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
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "UnSuspensionInrollmentRequestForm",
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
  /* border: 1.5px solid #1b2f5e; */
  border-radius: 15px;
  position: relative;
}
.form-meta-box {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
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
</style>
