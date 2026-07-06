<template>
  <v-container class="d-flex justify-center my-5">
    <v-card class="pa-12 document-paper interactive" width="850" elevation="6">
      <div class="text-center mb-8">
        <h2 class="doc-title">طلب تسكين في السكن الجامعي</h2>
      </div>

      <div class="doc-body text-right">
        <p>الأخ / مدير عام الإسكان الجامعي المحترم</p>
        <p class="mt-2">تحية طيبة وبعد،،،</p>

        <p>
          أنا الطالب /
          <span class="dotted-line" style="width: 350px"></span>
          من محافظة
          <span class="dotted-line" style="width: 150px"></span>
        </p>

        <p>
          مديرية
          <span class="dotted-line" style="width: 150px"></span>. أحمل الرقم الجامعي (
          <span class="dotted-line" style="width: 150px"></span>
          ) بكلية
          <span class="dotted-line" style="width: 150px"></span>.
        </p>

        <p class="mt-6">
          أرجو التكرم بالموافقة على منحي مقعداً في السكن الجامعي، نظراً لكوني من خارج
          محافظة صنعاء وأعاني من صعوبة في المواصلات.
        </p>

        <p class="mt-8 pa-3 border-dashed">
          <span>خاص بالإدارة: تم التحقق من وثائق الطالب وتبين أنه: </span>
          <span class="dotted-line" style="width: 250px"></span>
        </p>

        <v-row class="mt-10 align-end">
          <v-col cols="6" class="text-center">
            <p>توقيع الطالب: <span class="dotted-line" style="width: 150px"></span></p>
          </v-col>
          <v-col cols="6" class="text-left">
            <p>
              رقم التلفون:
              <span class="dotted-line" style="width: 150px"></span>
            </p>
          </v-col>
        </v-row>
      </div>
    </v-card>
  </v-container>
</template>

<style scoped>
.document-paper {
  background-color: #fff;
  font-family: "Amiri", serif;
  color: #000;
  line-height: 2.6;
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
  font-size: 1.3rem;
  direction: rtl;
}

.dotted-line {
  border-bottom: 2px dotted #000;
  display: inline-block;
  vertical-align: middle;
}

.border-dashed {
  border: 1px dashed #555;
  font-size: 1.1rem;
}

.sign-space {
  height: 50px;
}
</style>
