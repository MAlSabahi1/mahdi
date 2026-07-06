<template>
  <drawer
    type="dialog"
    width="900"
    :data="data"
    :getData="getData"
    :click="saveData"
    :re_open="false"
  >
  </drawer>
</template>
<script>
export default {
  props: {
    data: {
      type: Object,
      default: () => ({ fields_schema: { fields: [], attrs: "" } }),
    },

    getData: {
      type: Function,
    },
  },
  data() {
    return {
      step_index: 0,
      form_valid: [],
      add_step_dialog: false,
      service_id: this.$route.params?.service_id,
      step_temp: {},
      fields_schema: [],
      steppers: [],
      url: "d-services/service-versions/",
    };
  },
  methods: {
    async saveData() {
      const data = {
        ...this.data,
        fk_service: this.service_id,
      };
      console.log(data, "======");

      // data.fields_schema?.forEach((field, index) => {
      //   field.index = index + 1;
      // });
      if (this.data?.id) {
        await this.$axios
          .put(`d-services/service-versions/${this.data.id}/`, data)
          .then((e) => {
            this.$alert("update");
          });
      } else {
        await this.$axios
          .post("d-services/service-versions/", data)
          .then((e) => {
            this.$alert("add");
          });
      }
    },
  },
  watch: {
    // "data.id": {
    //   handler(id) {
    //     if (id) {
    //       console.log();
    //       if (this.data.component_type == "form") {
    //         this.fields_schema = this.data.fields_schema;
    //       }
    //       if (this.data.component_type == "wizard") {
    //         this.fields_schema = this.data.fields_schema;
    //       }
    //     }
    //   },
    // },
    // fields_schema: {
    //   handler(newVal) {
    //     this.data["fields_schema"] = newVal;
    //   },
    //   deep: true,
    // },
  },
};
</script>
