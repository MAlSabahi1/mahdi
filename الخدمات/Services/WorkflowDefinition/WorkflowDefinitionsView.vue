<template>
  <add-workflow-definition
    v-model="drawer"
    :items="items"
    :data="data"
    :getData="getData"
  />
  <custom-data-table
    :="{
      headers,
      items,
      getData,
      editItem,
      delItem: url,
      create: () => (drawer = true),
    }"
  >
  <template v-slot:item-slot="{ item, key }">
    <span v-if="key=='order'" >
      <v-chip class="rounded" size="small" color="primary">
        <span class="text-h6">{{item[key]}}</span>
      </v-chip>
    </span>
  </template>
  </custom-data-table>
</template>
<script>
export default {
  data() {
    return {
      data: {},
      items: {},
      drawer: false,
      url: "d-services/workflow/workflow-definitions/",
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
        { title: this.$t("service"), key: "service_name" },
        {
          title: this.$t("from_stage"),
          key: "fk_from_stage_name",
        },
        {
          title: this.$t("to_stage"),
          key: "fk_to_stage_name",
        },
        {
          title: 'مرحلة نهائية',
          key: "is_final",
        },
        { title: this.$t("condition_expression"), key: "condition_expression",show:false },
        { title: this.$t("order"), key: "order" },
      ];
    },
  },
};
</script>
