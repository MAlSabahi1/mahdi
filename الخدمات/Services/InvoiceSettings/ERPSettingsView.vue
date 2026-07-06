<template>
  <AddERPSettings
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

      url: "d-services/organization-service-config/",
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
        {
          title:this.$t("specialization_id"),
          key:"specialization_id",
        },
        {
          title:this.$t("study_system_id"),
          key:"study_system_id",
        },
        {
          title:this.$t("fk_currency"),
          key:"fk_currency",
        },
        {
          title:this.$t("service_fee"),
          key:"service_fee",
        },
        {
          title:this.$t("is_donor_invoice_allowed"),
          key:"is_donor_invoice_allowed",
        },
        {
          title:this.$t("is_discount_allowed"),
          key:"is_discount_allowed",
        },
        {
          title:this.$t("erp_product_id"),
          key:"erp_product_id",
        },
        {
          title:this.$t("erp_product_name"),
          key:"erp_product_name",
        },
        {
          title:this.$t("erp_product_for_discount_id"),
          key:"erp_product_for_discount_id",
        },
        {
          title:this.$t("erp_product_for_discount_name"),
          key:"erp_product_for_discount_name",
        },
        {
          title:this.$t("erp_product_for_internal_donors_id"),
          key:"erp_product_for_internal_donors_id",
        },
        {
          title:this.$t("erp_product_for_internal_donors_name"),
          key:"erp_product_for_internal_donors_name",
        },
        {
          title:this.$t("erp_project_id"),
          key:"erp_project_id",
        },
        {
          title:this.$t("erp_project_name"),
          key:"erp_project_name",
        },
        {
          title:this.$t("erp_activity_id"),
          key:"erp_activity_id",
        },
        {
          title:this.$t("erp_activity_name"),
          key:"erp_activity_name",
        },
        {
          title:this.$t("erp_cost_center_id"),
          key:"erp_cost_center_id",

        },
        {
          title:this.$t("erp_cost_center_name"),
          key:"erp_cost_center_name",
        },
      ];
    },
  },
};
</script>
