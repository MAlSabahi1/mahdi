<template>
  <v-container class="d-flex justify-center my-5">
    <v-card class="pa-12 document-paper" width="850" variant="outlined">
      <v-row class="text-center mb-8 align-center">
        <v-col cols="12" class="text-left">
          <div>التاريخ: .... / .... / 2026م</div>
          <div>الرقم: ....................</div>
        </v-col>
      </v-row>

      <div class="text-center mb-10">
        <h2 class="doc-title">إفادة غياب بعذر مقبول</h2>
      </div>

      <div class="doc-body text-right">
        <p>
          تفيد عمادة كلية
          <span class="dotted-line" style="width: 150px"></span> بأن الطالب /
          <span class="dotted-line" style="width: 320px"></span>
        </p>
        <p>
          المقيد بقسم
          <span class="dotted-line" style="width: 180px"></span> بالمستوى الدراسي
          <span class="dotted-line" style="width: 100px"></span>.
        </p>
        <p class="mt-4">
          قد تقدم بعذر مقبول لتبرير غيابه للفترة من تاريخ
          <span class="dotted-line" style="width: 120px"></span> إلى تاريخ
          <span class="dotted-line" style="width: 120px"></span>.
        </p>
        <p class="mt-6">
          وعليه، يرجى من السادة مدرسي المواد التعاون مع الطالب المذكور وتمكينه من تعويض ما
          فاته من تكاليف أو اختبارات شهرية وفقاً للوائح.
        </p>
      </div>

      <v-row class="mt-15 text-center">
        <v-col cols="6">
          <p class="font-weight-bold">مسجل الكلية</p>
          <div class="sign-space">.........................</div>
        </v-col>
        <v-col cols="6">
          <p class="font-weight-bold">عميد شؤون الطلاب بالكلية</p>
          <div class="sign-space">.........................</div>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>
<style scoped>
.document-paper {
  background-color: #fff;
  font-family: "Amiri", serif !important;
  color: #000;
  line-height: 2.8;
  border: 1.5px solid #000 !important;
  border-radius: 0;
}

.doc-title {
  text-decoration: underline;
  text-underline-offset: 10px;
  font-weight: 900;
  font-size: 1.8rem;
}

.doc-body {
  font-size: 1.35rem;
  direction: rtl;
}

.text-indent {
  padding-right: 40px;
}

/* نمط الإدخال السطري الموحد */
.inline-write {
  border: none;
  border-bottom: 1.5px dotted #000;
  outline: none;
  background: transparent;
  font-weight: bold;
  color: #4e342e; /* لون بني داكن للتمييز */
  padding: 0 8px;
  text-align: center;
}

.dotted-line {
  border-bottom: 2.5px dotted #000;
  display: inline-block;
  vertical-align: middle;
}

.sign-space {
  height: 50px;
}

@media print {
  .no-print {
    display: none !important;
  }
  .document-paper {
    border: none !important;
    box-shadow: none !important;
    margin: 0;
    padding: 0;
  }
  .inline-write::placeholder {
    color: transparent;
  }
}
</style>
