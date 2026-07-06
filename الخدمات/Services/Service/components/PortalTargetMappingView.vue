<template>
 
  <custom-data-table-with-save
    :="{
      headers,
      getData,
      items,
      click: saveData,
      canAdd:true
    }"
  />
</template>

<script>
export default {
  props: {
    fk_service: Number,
    
  },
  data() {
    return {
      items: [],
      schemaFields: [],
    };
  },
  created() {
    this.getData();
    this.getSchemaFields();
  },
  methods: {
    async getSchemaFields() {
      const response = await this.$axios(
        `d-services/portal-target-mapping/schema-fields/?service_id=${this.fk_service}`,
        {
          params: {
            fk_service: this.fk_service,
          },
        }
      );
      this.schemaFields = response?.data?.data?.fields ||[];
    },
    async getData() {
      const response = await this.$axios("d-services/portal-target-mapping/", {
        params: {
          fk_service: this.fk_service,
        },
      });
      this.items = response.data.data;
    },
    async saveData() {
      const data = {
        fk_service: this.fk_service,
        mappings: this.items,
      };
      console.log(data);

      await this.$axios.post(
        "d-services/portal-target-mapping/bulk-sync/",
        data
      );
      this.$snack("update");
    },
  },
  computed: {
    headers() {
      return [
        {
          title: "اسم الحقل في QAS",
          key: "qas_field_name",
          field: {
            name: "fields",
            type: "ForeignKey",
            null: false,
            width: 200,
            add: false,
            name_list: "SchemaFields",
            objects: this.schemaFields,
            param: this.fk_service,
            rules: [
                this.$duplicate(
                  this.items.map(
                    (e) => e.qas_field_name
                  )
                ),
              ],
            update: (e,i,v) => {
              const item = this.schemaFields.find(e=>e.name===v)
              console.log(item);

              if(item){
                e.qas_model_name = item.model
                e.is_main_target = item.is_main
                e.field_order = item.order
              }
            },
          },
        },
        {
          title: "اسم الموديل في QAS",
          key: "qas_model_name",
          field: {
            name: "qas_model_name",
            type: "CharField",
            null: false,
            width: 200,
            max_length: 100,
          },
        },
        {
          title: "اسم الحقل في البوابة",
          key: "portal_field_name",
          field: {
            name: "portal_field_name",
            type: "CharField",
            null: false,
            width: 200,
            max_length: 100,
          },
        },
        {
          title: "طريقة التحويل",
          key: "resolve_by",
          field: {
            name: "resolve_by",
            type: "ForeignKey",
            null: false,
            width: 200,
            add: false,
            name_list: "ResolveByChoice",
          },
        },
        {
          title: "حقل البحث في QAS",
          key: "resolve_field",
          field: {
            name: "resolve_field",
            type: "CharField",
            null: false,
            width: 200,
            max_length: 100,
          },
        },
        {
          title: "دالة تحويل مخصصة",
          key: "custom_resolver",
          field: {
            name: "custom_resolver",
            type: "CharField",
            null: true,
            width: 200,
            max_length: 255,
          },
        },
        {
          title: "الحقل الرئيسي للهدف",
          key: "is_main_target",
          field: {
            name: "is_main_target",
            type: "BooleanField",
            null: false,
            width: 100,
            default: false,
          },
        },
        {
          title: "ترتيب الحقل",
          key: "field_order",
          field: {
            name: "field_order",
            type: "IntegerField",
            null: false,
            width: 200,
            default: 0,
          },
        },
      ];
    },
  },
};
</script>