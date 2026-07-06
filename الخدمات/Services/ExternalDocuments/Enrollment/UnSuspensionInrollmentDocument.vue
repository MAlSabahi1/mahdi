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
        <h2 class="doc-title">قـرار إلغاء قيد دراسي (نهائي)</h2>
      </div>

      <div class="doc-body text-right">
        <p>
          بناءً على رغبة الطالب وتوقيعه على نموذج إخلاء الطرف، تقرر إلغاء قيد الطالب /
          <span class="dotted-line" style="width: 350px"></span>
        </p>
        <p>
          المقيد بالرقم الجامعي (
          <span class="dotted-line" style="width: 150px"></span> ) بكلية
          <span class="dotted-line" style="width: 150px"></span>
          قسم <span class="dotted-line" style="width: 180px"></span>
        </p>
        <p>
          دفعة
          <span class="dotted-line" style="width: 150px"></span>.
        </p>
        <p class="mt-4">
          ويعتبر هذا القرار نافذاً من تاريخ صدوره، وقد تم تسليم الطالب كافة وثائقه الأصلية
          المودعة في ملفه لدى الجامعة.
        </p>
      </div>

      <v-row class="mt-15 text-center">
        <v-col cols="4">
          <p class="font-weight-bold">مدير القبول والتسجيل</p>
          <div class="sign-space">
            <span class="dotted-line" style="width: 150px"></span>
          </div>
        </v-col>
        <v-col cols="4">
          <p class="font-weight-bold">ختم الجامعة</p>
          <div class="stamp-space"></div>
        </v-col>
        <v-col cols="4">
          <p class="font-weight-bold">المسجل العام</p>
          <div class="sign-space">
            <span class="dotted-line" style="width: 150px"></span>
          </div>
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

.dotted-line {
  border-bottom: 2px dotted #000;
  display: inline-block;
  vertical-align: middle;
}

.sign-space {
  height: 50px;
}
</style>
