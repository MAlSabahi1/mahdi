<template>
  <add-service-version v-model="drawer" :items="items" :data="data" :getData="getData" />
  <custom-data-table :="{
    headers,
    items,
    getData,
    create: () => (drawer = true),
    delItem: url,
    editItem,
    actionList
  }">
    <template v-slot:top>
      <VLabel class="ms-5">
        * ملاحظة : يمكنك النقر على الايقونة في عمود الاصدار الحالي لتحديد الاصدار للخدمة
      </VLabel>
    </template>

    <template v-slot:item-slot="{ item, key }">
      <span v-if="key === 'is_current'">
        <v-icon :color="item.is_current ? 'success' : 'error'"
          :icon="item.is_current ? 'mdi-check-circle' : 'mdi-close-circle'" @click="setCurrentVersion(item.id)" />
      </span>
      <span v-if="key === 'preview'">
        <v-icon color="primary" icon="mdi-eye" @click="preview(item)" />
      </span>
    </template>
  </custom-data-table>
  <custom-dialog v-model="preview_dialog" title="معاينة النموذج" height='auto'>
    <v-container>
      <form-preview :data="preview_data" :fields_schema="fields_schema" :templateType="component_type" />
    </v-container>
  </custom-dialog>
</template>
<script>
export default {
  data() {
    return {
      data: {},
      preview_data: {},
      items: {},
      fields_schema: [],
      component_type: null,
      service_id: this.$route.params?.service_id,
      drawer: false,
      preview_dialog: false,
      url: "d-services/service-versions/",
      url_paginate: "d-services/service-versions/filter-paginate/",
    };
  },
  methods: {

    // دالة جلب الاصدارات الخاصة بالخدمة
    async getData(params = this.$params) {
      return await this.$axios
        .post(this.url_paginate, { filters: [{ field: 'fk_service', value: this.service_id }] }, params)
        .then((response) => (this.items = response.data));
    },
    async setCurrentVersion(version_id) {
      return await this.$axios.patch(`${this.url}${version_id}/set-current/`).then(res => {
        this.$snack('update', { message: 'تم اعادة تحديث الاصدار الحالي للخدمة' })
        this.getData()
      })
    },

    editItem(data) {
      this.data = { ...data };
      this.drawer = true;
    },
    preview(item) {
      this.preview_dialog = true;
      this.fields_schema = item.fields_schema;
      this.component_type = item.component_type
    },
  },
  computed: {
    headers() {
      return [
        { title: this.$t("fk_service"), key: "fk_service__name_ar" },
        { title: this.$t("version_name"), key: "version_name" },
        {
          title: this.$t("component_type"),
          key: "component_type__display",
        },
        { title: this.$t("is_current_version"), key: "is_current" },
        { title: this.$t("preview"), key: "preview" },
      ];
    },
  },
};
</script>
