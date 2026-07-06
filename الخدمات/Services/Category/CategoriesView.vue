<template>
  <add-category v-model="drawer" :getData="getData"/>
  <custom-data-table
    :="{
      headers,
      items,
      getData,
      create: () => (drawer = true),
      delItem: url,
      editItem,
    }"
  />
</template>
<script>
export default {
  data() {
    return {
      data: {},
      items: {},
      drawer: false,
      url: "d-services/workflow/categories/",
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
        { title: this.$t("category_name"), key: "name" },
        {
          title: this.$t("category_parent"),
          key: "parent",
        },
        { title: this.$t("service_count"), key: "service_count" },
        { title: this.$t("description"), key: "description" },

      ];
    },
  },
};
</script>
