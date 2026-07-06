<template>
  <drawer
    type="dialog"
    width="900"
    :data="data"
    :click="saveData"
    :getData="getData"
  >
    <template v-slot>
      <fields :data="data" url="data-templates" :group="true">
        <template v-slot="{ field }">
          <span v-if="field.name === 'fields_schema'">
            <json-editor
              v-if="data.component_type == 'form'"
              :fields="json_filds"
              :attrs="data?.attrs ?? {}"
              @update:fields="fields = $event"
              @update:attrs="data.attrs = $event"
            />
            <stepper-editor
              v-if="data.component_type == 2"
              v-model="steppers"
            ></stepper-editor>
          </span>

          <span v-if="['model_path', 'pk_field'].includes(field.name)">
            <template v-if="field.name === 'model_path'">
              <v-text-field
                density="compact"
                variant="outlined"
                label="اسم المودل"
                v-model="data.model_path"
                clearable
              ></v-text-field>
            </template>
            <template v-if="field.name == 'pk_field' && data.model_path">

              <VAutocomplete
                v-model="data.pk_field"
                density="compact"
                variant="outlined"
                label="اسم الحقل"
                :items="field_names"
                item-title="title"
                item-value="value"
                :rules="[$required]"
                clearable
              ></VAutocomplete>
            </template>
          </span>
        </template>
      </fields>
    </template>
  </drawer>
</template>
<script>

export default {
  props: {
    data: {
      type: Object,
      default: () => ({}),
    },

    getData: {
      type: Function,
    },
  },

  data() {
    return {
      step_index: 0,
      form_valid: [],
      add_step_dialog: false,
      step_temp: {},
      json_filds: [],
      steppers: [],
      url: "d-services/workflow/data-templates/",
    };
  },

  methods: {
    async saveData() {
      const data = {
        ...this.data,
        fields_schema:
          this.data.component_type == 'wizerd' ? this.steppers : this.json_filds,
        attrs: this.data.attrs ? this.data.attrs : "{}",
      };
      data.json_schema?.forEach((field, index) => {
        field.index = index + 1;
      });
      if (this.data?.id) {
        await this.$axios
          .put(`d-services/workflow/data-templates/${this.data.id}/`, data)
          .then((e) => {
            this.$alert("update");
            this.json_filds = [];
          });
      } else {
        await this.$axios
          .post("d-services/workflow/data-templates/", data)
          .then((e) => {
            this.$alert("add");
            this.json_filds = [];
          });
      }
    },
  },
  computed: {
    field_names(){
      if(this.data.component_type==1){
        return this.json_filds?.map(field=>{return {title:field.label_ar,value:field.name}})
      }
      else if (this.data.component_type==2){
        return this.steppers?.flatMap((step) => step?.fields).map(field=>{return {title:field.label_ar,value:field.name}}) ?? [];
      }
      return []
    }
  },

  watch: {
    "data.id": {
      handler(id) {
        if (id) {
          if (this.data.component_type == 1) {
            this.json_filds = this.data.json_schema;
          }
          if (this.data.component_type == 2) {
            this.steppers = this.data.json_schema;
          }
        }
      },
    },
    json_filds: {
      handler(newVal) {
        this.data["json_schema"] = newVal;
      },
      deep: true,
    },
  },
};
</script>
