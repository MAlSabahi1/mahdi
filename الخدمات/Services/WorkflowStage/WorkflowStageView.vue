<template>
  <add-workflow-stage v-model="drawer" :items="items" :data="data" :getData="getData" />
  <custom-data-table :="{
    headers,
    items,
    getData,
    create: () => (drawer = true),
    delItem: url,
    editItem,
  }" />
</template>
<script>
export default {
  data() {
    return {
      data: {},
      items: {},

      drawer: false,

      url: "d-services/workflow-stages/",
    };
  },
  methods: {
    async getData(params = this.$params) {
      return await this.$axios(this.url, params).then(
        (response) => (this.items = response.data)
      );
    },
    editItem(data) {
      this.data = { ...data };
      this.drawer = true;
    },
  },
  computed: {
    headers() {
      return [
        { title: this.$t("stage_name"), key: "name_ar" },
        {
          title: this.$t("stage_name_en"),
          key: "name_en",
        },
        { title: this.$t("stage_type"), key: "stage_type__display" },
        { title: this.$t("is_final"), key: "is_final_stage" },
        { title: this.$t("is_execution_stage"), key: "is_execution_stage" },
        { title: this.$t("expected_duration_days"), key: "expected_duration_days" },

      ];
    },
  },
};
</script>
