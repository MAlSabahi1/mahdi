<template>
  <add-grant-source
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

      url: "d-services/grant-sources/",
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
      return this.$headers["grant-source"] || [];
    },
  },
};
</script>
