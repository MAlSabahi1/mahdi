<template>
  <add-service-template :data="data" :items="items" v-model="drawer" :getData="getData"  />
  <custom-data-table
    :="{
      headers,
      items,
      getData,
      create: () => (drawer = true),
      delItem: url,
      actionList,
      editItem,
    }"
  />

  <custom-dialog v-model="preview_dialog" title="معاينة النموذج" width='auto' height='auto'>
    <v-container>
      <form-preview :fields="json_schema" :attrs="attrs " :templateType="template_type" />
    </v-container>
  </custom-dialog>
</template>
<script>
export default {
  data() {
    return {
      data: {},
      items: {},
      template_type:null,

      json_schema: [],
      attrs: {},
      preview_dialog: false,

      drawer: false,

      url: "d-services/workflow/data-templates/",
    };
  },
  methods: {
    actionList(item) {
      return [
        {
          title_ar: "معاينة",
          title_en: "Preview",
          click: () => {
            this.preview_dialog = true;
            this.json_schema = item.json_schema;
            this.attrs = item?.attrs;
            this.template_type = item.template_type
          },
        },
      ];
    },

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
        { title: this.$t("template_name"), key: "name" },
        {
          title: this.$t("service"),
          key: "service_name",
        },
        { title: this.$t("template_type"), key: "template_type_name" },
        { title: this.$t("version"), key: "version" },
        { title: this.$t("is_active"), key: "is_active" },
        {
          title: this.$t("created_at"),
          key: "created_at",
          sortable: false,
        },
      ];
    },
  },
};
</script>
