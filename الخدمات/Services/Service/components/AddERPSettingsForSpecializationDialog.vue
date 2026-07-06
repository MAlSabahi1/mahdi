<template>

  <component
    :is="embedded ? 'div' : 'custom-dialog'"
    v-model="dialog"
    height="auto"
    persistent
    :title="$t('erp_services_settings') + '(' + title + ')'"
    width="auto"
    min-width="700"
  >
    <v-card rounded="lg" v-if="loading">
      <v-skeleton-loader type="table" height="300" />
    </v-card>
    <div v-else class="pa-4">
      <div >
        <v-sheet border rounded="xl" class="pa-1">
          <custom-data-table-with-save
            :="{
              headers: headers,
              getData: getData,
              items: items,
              top: false,
            }"
            :click="save"
            :canAdd="true"
          >
          </custom-data-table-with-save>
        </v-sheet>
      </div>
    </div>
  </component>
</template>

<script>
import Axios from "axios";

export default {
  props: {
    modelValue: Boolean,
    service: Object,
    embedded: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["update:modelValue", "switch-to-first"],
  data() {
    return {
      loading: false,
      items: [],
      service_settings_data: {},
      url: "d-services/service-erp-settings/",
      org_config_defaults:{},
      installment_period_items: [],
      specializations_items:[],
      study_systems_items:[],
      currency_items:[],
      selected_service:{},
      schoolarships:[],
      discounts:[],
      cost_centers:[],
      activities:[],
      products:[],
      projects:[],
      erp_url:this.setting?.erp_url
    };
  },
  async created() {
    const erp_specialization_data_autolist = this.service?.erp_specialization_data_autolist
    const erp_study_system_data_autolist = this.service?.erp_study_system_data_autolist
    if (this.$dataList() && this.$dataList()[erp_specialization_data_autolist]) {
      this.specializations_items =
        await this.$dataList()[erp_specialization_data_autolist].method();
    }
    if (this.$dataList() && this.$dataList()[erp_study_system_data_autolist]) {
      this.study_systems_items =
        await this.$dataList()[erp_study_system_data_autolist].method();
    }
    if (this.$dataList() && this.$dataList().Currency) {
      this.currency_items =
        await this.$dataList().Currency.method();
    }
    if (this.$dataList && this.$dataList().Schoolarships) {
      this.schoolarships =
        await this.$dataList().Schoolarships.method();
    }
    if (this.$dataList && this.$dataList().Discounts) {
      this.discounts =
        await this.$dataList().Discounts.method();
    }
    if (this.$dataList && this.$dataList().CostCenters) {
      this.cost_centers =
        await this.$dataList().CostCenters.method();
    }
    if (this.$dataList && this.$dataList().Activities) {
      this.activities =
        await this.$dataList().Activities.method();
    }
    if (this.$dataList && this.$dataList().Products) {
      this.products =
        await this.$dataList().Products.method();
    }
    if (this.$dataList && this.$dataList().Projects) {
      this.projects =
        await this.$dataList().Projects.method();
    }
  },
  computed: {
    dialog: {
      get() {
        return this.modelValue;
      },
      set(val) {
        this.$emit("update:modelValue", val);
      },
    },
    title() {
      return this.service?.name_ar || "";
    },
    headers() {
      return [
        {
          title:this.$t("specialization_id"),
          key:"specialization_id",
          field:{
            name:"specialization_id",
            type:"ForeignKey",
            name_list:"Specialization",
            null: false,
            width: "200",
            objects: this.specializations_items,
          }
        },
        {
          title:this.$t("study_system_id"),
          key:"study_system_id",
          field:{
            name:"study_system_id",
            type:"ForeignKey",
            name_list:"StudySystem",
            add:false,
            null: false,
            width: "200",
            objects: this.study_systems_items,
          }
        },
        {
          title:this.$t("fk_currency"),
          key:"fk_currency",
          field:(field_data)=>({
            name:"fk_currency",
            type:"ForeignKey",
            name_list:"Currency",
            objects: this.currency_items,
            null: false,
            width: "200",
          })
        },
        {
          title:this.$t("service_fee"),
          key:"service_fee",
          field:(field_data)=>({
            name:"service_fee",
            icon: "cash",
            null: false,
            type: "PositiveIntegerField",
            rules: [this.$numeric],
            width: "150",
          })
        },

        {
          title:this.$t("is_discount_allowed"),
          key:"is_discount_allowed",
          field:(field_data)=>({
            name:"is_discount_allowed",
            type:"BooleanField",
            hideDetails: "auto",
            update:()=>{
              if(!field_data.is_discount_allowed){
                field_data.erp_product_for_discount_id=null
                field_data.erp_product_for_discount_name=null
              }
            }
          })
        },
        {
          title:this.$t("erp_product_for_discount_id"),
          key:"erp_product_for_discount_id",
          field:(field_data)=>({
            name:"erp_product_for_discount_id",
            type:"ForeignKey",
            name_list:"Discounts",
            objects: this.discounts,
            null:!field_data?.is_discount_allowed,
            width: "200",
            icon:"identifier",
            disabled:!field_data?.is_discount_allowed,
            update:()=>{
              field_data.erp_product_for_discount_name = this.getNameByID(this.discounts,field_data.erp_product_for_discount_id)
            }
          })
        },

        {
          title:this.$t("is_donor_invoice_allowed"),
          key:"is_donor_invoice_allowed",
          field:(field_data)=>({
            name:"is_donor_invoice_allowed",
            type:"BooleanField",
            hideDetails: "auto",
            update: () => {
              if(! field_data.is_donor_invoice_allowed){
                field_data.erp_product_for_internal_donors_id=null
                field_data.erp_product_for_internal_donors_name=null
              }
            }
          })
        },
        {
          title:this.$t("erp_product_for_internal_donors_id"),
          key:"erp_product_for_internal_donors_id",
          field:(field_data)=>({
            name:"erp_product_for_internal_donors_id",
            type:"ForeignKey",
            name_list:"Schoolarships",
            objects: this.schoolarships,
            width: "200",
            null:!field_data?.is_donor_invoice_allowed,
            icon:"identifier",
            disabled:!field_data?.is_donor_invoice_allowed,
            update:()=>{
              field_data.erp_product_for_internal_donors_name = this.getNameByID(this.schoolarships,field_data.erp_product_for_internal_donors_id)

            }
          })
        },

        {
          title:this.$t("erp_product_id"),
          key:"erp_product_id",
          field:(field_data)=>({
            name:"erp_product_id",
            type:"ForeignKey",
            name_list:"Products",
            objects: this.products,
            width: "200",
            icon:"identifier",
            update:()=>{
              field_data.erp_product_name = this.getNameByID(this.products,field_data.erp_product_id)

            }
          })
        },


        {
          title:this.$t("erp_project_id"),
          key:"erp_project_id",
          field:(field_data)=>({
            name:"erp_project_id",
            type:"ForeignKey",
            name_list:"Projects",
            objects: this.projects,
            width: "200",
            icon:"identifier",
            update:()=>{
              field_data.erp_project_name = this.getNameByID(this.projects,field_data.erp_project_id)

            }
          })
        },

        {
          title:this.$t("erp_activity_id"),
          key:"erp_activity_id",
          field:(field_data)=>({
            name:"erp_activity_id",
            type:"ForeignKey",
            name_list:"Activities",
            objects: this.activities,
            width: "200",
            icon:"identifier",
            update:()=>{
              field_data.erp_activity_name = this.getNameByID(this.activities,field_data.erp_activity_id)

            }
          })
        },

        {
          title:this.$t("erp_cost_center_id"),
          key:"erp_cost_center_id",
          field:(field_data)=>({
            name:"erp_cost_center_id",
            type:"ForeignKey",
            name_list:"CostCenters",
            objects: this.cost_centers,
            width: "200",
            icon:"identifier",
            update:()=>{
              field_data.erp_cost_center_name = this.getNameByID(this.cost_centers,field_data.erp_cost_center_id)
            }
          })
        },

      ];
    },
  },
  methods: {
    getNameByID(data_list,selected_id){
      const record = data_list?.find(item=>item.id==selected_id);
      return record ? record?.name : null
    },
    initRecord(record){
      record.fk_currency = this.org_config_defaults?.fk_currency
      record.service_fee = this.org_config_defaults?.service_fee
      record.is_discount_allowed = this.org_config_defaults?.is_discount_allowed
      record.erp_product_for_discount_id = this.org_config_defaults?.erp_product_for_discount_id
      record.erp_product_for_discount_name = this.org_config_defaults?.erp_product_for_discount_name
      record.is_donor_invoice_allowed = this.org_config_defaults?.is_donor_invoice_allowed
      record.erp_product_for_internal_donors_id = this.org_config_defaults?.erp_product_for_internal_donors_id
      record.erp_product_for_internal_donors_name = this.org_config_defaults?.erp_product_for_internal_donors_name
      record.erp_product_id = this.org_config_defaults?.erp_product_id
      record.erp_product_name = this.org_config_defaults?.erp_product_name
      record.erp_project_id = this.org_config_defaults?.erp_project_id
      record.erp_project_name = this.org_config_defaults?.erp_project_name
      record.erp_activity_id = this.org_config_defaults?.erp_activity_id
      record.erp_activity_name = this.org_config_defaults?.erp_activity_name
      record.erp_cost_center_id = this.org_config_defaults?.erp_cost_center_id
      record.erp_cost_center_name = this.org_config_defaults?.erp_cost_center_name
    },
    async getData() {
      this.loading = true;
      await this.$axios(`${this.url}`, {
        params: {
          fk_service: this.service?.id,
        },
      })
        .then((response) => {
          this.items = response.data?.data ?? [];
          this.org_config_defaults = response.data?.org_config_defaults;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    async save() {
      if (this.service?.id) {
        return await this.$axios
          .post(this.url, {
            fk_service: this.service.id,
            settings: this.items,
          })
          .then((res) => {
            this.$snack("add", { message: res.data?.message });
          });
      }
    },
    requestSwitch() {
      this.$emit("switch-to-first");
    },

  },
  watch: {
    dialog(val) {
      if (val) {
        this.getData();
      }
    },
    "service.id": {
      handler(val) {
        if (val && this.embedded) {
          this.getData();
        }
      },
      immediate: true,
    },
    "items.length": {
      handler(newLength,oldLength) {
        if(newLength>oldLength ){
          const last_record = this.items[newLength-1];
          this.initRecord(last_record)
        }
      },
    },

  },
};
</script>
