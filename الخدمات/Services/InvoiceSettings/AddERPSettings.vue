<template>
  <drawer
    :data="data"
    :getData="getData"
    :click="saveData"
  >
    <template v-slot>
      <div class="w-100">
        <filter-fields
          class="ma-3 border-dashed"
          label_class="text-primary"
          :label="$t('donor_init')"
        >
          <template #fields>
            <fields
              :data="data"
              url="service-erp-settings"
              group="DONOR"
              :attr="{
                is_donor_invoice_allowed:{
                  update:()=>{
                    if(!data.is_donor_invoice_allowed){
                      data.erp_product_for_internal_donors_id = null
                      data.erp_product_for_internal_donors_name = null
                    }
                  }
                },
                erp_product_for_internal_donors_id:{
                  depend:data?.is_donor_invoice_allowed,
                  objects:schoolarships,
                  update:()=>{
                    if(!data.erp_product_for_internal_donors_id){
                      data.erp_product_for_internal_donors_name=null
                    }else{
                      data.erp_product_for_internal_donors_name = getNameByID(schoolarships,data.erp_product_for_internal_donors_id)
                    }
                  }
                },

              }"
            />
          </template>
        </filter-fields>
        <filter-fields
          class="ma-3 border-dashed"
          label_class="text-primary"
          :label="$t('discount_init')"
        >
          <template #fields>
            <fields
              :data="data"
              url="service-erp-settings"
              group="DISCOUNT"
              :attr="{
                is_discount_allowed:{
                  update:()=>{
                    if(!data.is_discount_allowed){
                      data.erp_product_for_discount_id = null
                      data.erp_product_for_discount_name = null
                    }
                  }
                },
                erp_product_for_discount_id:{
                  depend:data?.is_discount_allowed,
                  objects:discounts,
                  update:()=>{
                    if(!data.erp_product_for_discount_id){
                      data.erp_product_for_discount_name=null
                    }else{
                      data.erp_product_for_discount_name = getNameByID(discounts,data.erp_product_for_discount_id)
                    }
                  }
                },

              }"
            />
          </template>
        </filter-fields>
        <filter-fields
          class="ma-3 border-dashed"
          label_class="text-primary"
          :label="$t('basic_init')"
        >
          <template #fields>
            <fields
              :data="data"
              url="service-erp-settings"
              group="BASIC"
              :attr="{
                erp_product_id:{
                  disabled:false,
                  objects:products,
                  update:()=>{
                    if(!data.erp_product_id){
                      data.erp_product_name=null
                    }else{
                      data.erp_product_name = getNameByID(products,data.erp_product_id)
                    }
                  }
                },
                erp_project_id:{
                  disabled:false,
                  objects:projects,
                  update:()=>{
                    if(!data.erp_project_id){
                      data.erp_project_name=null
                    }else{
                      data.erp_project_name = getNameByID(projects,data.erp_project_id)
                    }
                  }
                },
                erp_activity_id:{
                  disabled:false,
                  objects:activities,
                  update:()=>{
                    if(!data.erp_activity_id){
                      data.erp_activity_name=null
                    }else{
                      data.erp_activity_name = getNameByID(activities,data.erp_activity_id)
                    }
                  }
                },
                erp_cost_center_id:{
                  disabled:false,
                  objects:cost_centers,
                  update:()=>{
                    if(!data.erp_cost_center_id){
                      data.erp_cost_center_name=null
                    }else{
                      data.erp_cost_center_name = getNameByID(cost_centers,data.erp_cost_center_id)
                    }
                  }
                },

              }"
            />
          </template>
        </filter-fields>
      </div>
    </template>

  </drawer>
</template>
<script>
// import erp_url from './erp_url.json'


import Axios from "axios";
export default {
  props: {
    data: Object,
  },
  data(){
    return{
      url:"d-services/organization-service-config/",
      schoolarships:[],
      discounts:[],
      cost_centers:[],
      activities:[],
      products:[],
      projects:[],
      erp_url:this.setting?.erp_url
    }
  },
  async created(){

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

  methods: {
    getNameByID(data_list,selected_id){
      const record = data_list?.find(item=>item.id==selected_id);
      return record ? record?.name : null
    },
    async saveData(){
      await this.$axios.patch(`${this.url}${this.data?.id}/update-erp-invoice-settings/`,this.data).then(res=>{
        this.$snack('update')
      })
    },

  },
};
</script>
