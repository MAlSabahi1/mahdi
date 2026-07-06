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
        <h2 class="doc-title">إفادة تسكين جامعي</h2>
      </div>

      <div class="doc-body text-right">
        <p>
          تشهد إدارة الإسكان الجامعي بجامعة صنعاء بأن الطالب /
          <span class="dotted-line" style="width: 350px"></span>
        </p>
        <p>
          المقيد بكلية
          <span class="dotted-line" style="width: 150px"></span> قسم
          <span class="dotted-line" style="width: 180px"></span> بالمستوى الدراسي
          <span class="dotted-line" style="width: 80px"></span>.
        </p>
        <p class="mt-4">
          أنه مسكن ومقيم حالياً في السكن الجامعي (مبنى:
          <span class="dotted-line" style="width: 100px"></span>) غرفة رقم (
          <span class="dotted-line" style="width: 80px"></span> ) للعام الجامعي 2025 /
          2026م.
        </p>
        <p class="mt-6">
          وقد أعطيت له هذه الإفادة بناءً على طلبه لتقديمها إلى من يهمه الأمر.
        </p>
      </div>

      <v-row class="mt-15 text-center">
        <v-col cols="6">
          <p class="font-weight-bold">مشرف مبنى السكن</p>
          <div class="sign-space">.........................</div>
        </v-col>
        <v-col cols="6">
          <p class="font-weight-bold">مدير عام الإسكان الجامعي</p>
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
