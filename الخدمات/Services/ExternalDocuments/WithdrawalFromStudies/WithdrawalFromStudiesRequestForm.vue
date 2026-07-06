<template>
  استمارة انسحاب من الدراسة

  <div class="pa-2">
    <div class="pb-3 text-left">
      <div><strong>رقم الاستمارة:</strong> ....................</div>
      <div class="mt-2"><strong>التاريخ:</strong> ................................</div>
    </div>
    <div class="inner-frame rounded-xl pa-4 mb-4">
      <v-row no-gutters>
        <v-col cols="12" class="mb-4">
          <strong>الأخ الدكتور/ عميد</strong>
          ........................................................................
          <span class="float-left"><strong>المحترم</strong></span>
          <div class="text-center mt-1"><strong>بعد التحية</strong></div>
        </v-col>

        <v-col cols="12" class="text-justify data-lines mb-3">
          أنا الطالب : <span class="data-field">مرسل أمين مطهر</span> الجنسية :
          <span class="data-field">يمني</span> تاريخ الإلتحاق بالكلية :
          <span class="data-field">2024</span> برقم قيد :
          <span class="data-field">24112005</span>
        </v-col>

        <v-col cols="12" class="mb-3">
          القسم :
          <span class="data-field">الأنظمة الذكية والروبوتيكس</span>
          المستوى :
          <span class="data-field">1</span>
        </v-col>

        <v-col cols="12" class="mb-2 font-weight-bold">
          أطلب سحب ملفي من كلية الحاسوب والهندسة التكنولوجية وذلك للأسباب التالية :
        </v-col>

        <v-col cols="12" class="lined-area-container mb-4">
          <div class="lined-row"></div>
          <div class="lined-row"></div>
          <div class="lined-row"></div>
          <div class="lined-row"></div>
          <div class="lined-row"></div>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script setup>
// لا يوجد منطق برمجي
</script>

<style scoped>
/* الإطارات الداخلية (المربعات التي تحتوي النص) */
.inner-frame {
  border: 2px solid #ddd; /* أخضر باهت قليلاً أو رمادي مخضر حسب الصورة */
  background-color: transparent;
}
/* تنسيق الحقول المعبأة */
.data-field {
  font-weight: bold;
  padding: 0 5px;
  display: inline-block;
}

/* تباعد الأسطر للنصوص */
.data-lines {
  line-height: 2;
}

/* محاكاة الأسطر للكتابة */
.lined-area-container {
  border: 1px solid transparent;
}

.lined-row {
  border-bottom: 1px dotted #999;
  height: 35px; /* ارتفاع السطر */
  width: 100%;
  margin-bottom: 5px;
}
</style>
