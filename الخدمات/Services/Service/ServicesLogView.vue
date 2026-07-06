<template>
 
  <VCard>
    <VChip color="primary" class="ma-5" size="small" prepend-icon="mdi-sync">
      
      {{ `مزامنة ناجحة  : ${statusSync.success}` }}</VChip
    >
    <VChip color="secondary" class="ma-5" size="small" prepend-icon="mdi-sync-off">
      {{ `غير مزامنة   : ${statusSync.not_synced}` }}</VChip
    >
    <VChip color="red" class="ma-5"   size="small" prepend-icon="mdi-sync-alert">
      {{ `مزامنة فاشلة  : ${statusSync.failed}` }}</VChip
    >
    <VChip color="orange" class="ma-5" size="small" prepend-icon="mdi-numeric">
      {{ `الاجمالي  : ${statusSync.total}` }}</VChip
    >
  </VCard>

  <custom-data-table
    :="{
      headers,
      items,
      getData,
    }"
  >
    <template v-slot:action>
      <custom-btn
        label="مزامنة"
        icon="sync"
        color="primary"
        :click="saveData"
      />
    </template>
  </custom-data-table>
</template>
<script>
export default {
  data() {
    return {
      headers: [],
      items: [],
      statusSync: {},
    };
  },
  methods: {
    async getData() {
      const response = await await this.$axios("d-services/service-sync-log/");
      this.items.results = response.data?.items;
      this.statusSync = response.data?.stats;
    },
    async saveData() {
      const res = await await this.$axios.post(
        "d-services/trigger-service-sync/"
      );

      this.$alert("add", {
        message: {
          الحالة: res?.data?.message,
          "عدد الخدمات التي تمت مزامنتها": String(res?.data?.total),
        },

      });
      this.getData()
    },
  },
  computed: {
    headers(){
      return [
        {title:this.$t('service_name'),key:'service_name'},
        {title:this.$t('service_code'),key:'service_code'},
        {title:this.$t('service_status'),key:'status_display'},
        {title:this.$t('last_synced_at'),key:'last_synced_at'},
        {title:this.$t('error_message'),key:'error_message'},
      ]
    }
  },
};
</script>