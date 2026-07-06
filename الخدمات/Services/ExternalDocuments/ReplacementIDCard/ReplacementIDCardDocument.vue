<template>

  <div id="student_cards">
    <student-card
      :="{ card_data: students_data, print_side: print_set?.side }"
    ></student-card>
  </div>
</template>
<script>
export default {
  name: "ReplacementIDCardDocument",
  inject: ["context"],
  data() {
    return {
      output_data: this.context?.output_data ?? {},
      print_set: { side: "1" },
    };
  },
  computed:{
    students_data(){
      return[
        {...this.output_data}
      ]
    }
  }
};
</script>
<style scoped>
.document-paper {
  background-color: #fff;
  font-family: "Amiri", serif;
  color: #000;
  line-height: 2.8;
  border: 1.5px solid #000 !important;
  border-radius: 0;
  position: relative;
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

.dotted-line {
  border-bottom: 2.5px dotted #000;
  display: inline-block;
  vertical-align: middle;
}

.finance-box {
  border: 1px dashed #444;
  font-size: 1.1rem;
}

.photo-placeholder {
  width: 100px;
  height: 120px;
  border: 1px solid #000;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 140px;
  left: 50px;
  font-size: 0.8rem;
  color: #666;
}

.sign-space {
  height: 40px;
}
:deep(.print-cards-table tbody td) {
  max-width: 256px !important;
}
</style>
