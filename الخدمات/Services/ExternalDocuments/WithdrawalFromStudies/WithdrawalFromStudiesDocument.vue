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
        <h2 class="doc-title">قـرار انسحاب من الدراسة</h2>
      </div>

      <div class="doc-body text-right">
        <p>
          بعد الاطلاع على الطلب المقدم من الطالب /
          <span class="dotted-line" style="width: 350px"></span>
        </p>
        <p>
          المقيد بكلية
          <span class="dotted-line" style="width: 180px"></span> قسم
          <span class="dotted-line" style="width: 200px"></span> رقم جامعي (
          <span class="dotted-line" style="width: 120px"></span> ).
        </p>
        <p class="mt-4">
          تقرر الموافقة على **انسحابه نهائياً** من الدراسة بطلب منه، وقد تم إخلاء طرفه من
          كافة مرافق الجامعة وتسليمه أصول وثائقه المودعة لدى نيابة شؤون الطلاب.
        </p>
        <p class="mt-6 text-subtitle-1 font-weight-bold">
          يعتبر هذا القرار نافذاً من تاريخ صدوره،،،
        </p>
      </div>

      <v-row class="mt-15 text-center">
        <v-col cols="4">
          <p class="font-weight-bold">مدير القبول والتسجيل</p>
          <div class="sign-space">.........................</div>
        </v-col>
        <v-col cols="4">
          <p class="font-weight-bold">ختم الكلية</p>
          <div class="stamp-space"></div>
        </v-col>
        <v-col cols="4">
          <p class="font-weight-bold">المسجل العام</p>
          <div class="sign-space">.........................</div>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>
<style scoped>
.document-paper {
  background-color: #fff;
  font-family: "Amiri", serif;
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
  font-family: "Cairo", sans-serif;
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
</style>
