<template>
  <drawer
    :data="Object.assign(data, { fk_organization: null })"
    click="d-services/workflow/workflow-definitions/"
  >
    <template v-slot>
      <fields
        :data="data"
        url="workflow-definitions"
        :attr="{
          fk_service:{
            update:(val)=> val? getAvailableServiceStages(data.fk_service):null
          },
          fk_from_stage: {
            items:extendListStages(available_stages?.filter(item=>item.id != data.fk_from_stage),from_stage)
          },
          fk_to_stage:{
            items:extendListStages(available_stages?.filter(item=>item.id != data.fk_from_stage),to_stage)
          }
        }"
      />
    </template>
  </drawer>
</template>
<script>
export default {
  props: {
    data: Object,
  },
  data(){
    return{
      available_stages:[],
      all_stages:[]
    }
  },
  computed:{

    from_stage(){
      return this.all_stages?.find(item=>item.id==this.data?.fk_from_stage)
    },
    to_stage(){
      return this.all_stages?.find(item=>item.id==this.data?.fk_to_stage)
    },

  },
  async created(){
    this.all_stages = await this.$dataList().WorkflowStages.method()
  },
  methods:{
    async getAvailableServiceStages(fk_service){
      this.available_stages = await this.$dataList(fk_service).AvailableServiceWorkflowStages.method()
    },
    extendListStages(stages_list,newStage,key="id"){
      if(!newStage) return stages_list
      const map = new Map(stages_list?.map(item=>[item[key],item]));
      map.set(newStage[key],newStage);
      return Array.from(map.values());
    }
  }
};
</script>
