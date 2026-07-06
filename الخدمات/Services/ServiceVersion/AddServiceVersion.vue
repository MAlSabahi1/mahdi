<template>
  <drawer
    type="dialog"
    width="900"
    :data="data"
    :click="saveData"
    :re_open="false"
  >
    <template v-slot>
      <VRow>
        <auto-list
          v-model="selected_version"
          name="ServiceVersions"
          returnObject
          @update:modelValue="updateServiceVersions"
          :param="serviceId"
          cols="10"
          :refresh="refresh_selected_version"
        />

        <VCheckbox
          v-model="data.is_current"
          label="الاصدار الحالي"
          :disabled="!data.id || data.is_current"
          @click="updateCurrentVersion"
        />
      </VRow>
      <fields :data="data" url="service-versions" :group="true">
        <template v-slot="{ field }">
          <span v-if="field.name === 'fields_schema'">
            <json-editor
              v-if="data?.component_type == 'form'"
              :fields="data?.fields_schema?.fields ?? []"
              :attrs="data?.fields_schema?.attrs ?? ''"
              @update:fields="data.fields_schema['fields'] = $event"
              @update:attrs="data.fields_schema['attrs'] = $event"
            />
            <stepper-editor
              v-if="data?.component_type == 'wizard' ?? false"
              v-model="data.fields_schema"
            ></stepper-editor>
          </span>
        </template>
      </fields>
    </template>
  </drawer>
</template>
<script>
export default {
  props: {
    serviceId: Number,
  },
  data() {
    return {
      selected_version: null,
      refresh_selected_version: false,

      data: {
        component_type: null,
        is_current: false,
        fields_schema: {
          fields: [],
          attrs: {},
        },
      },
    };
  },

  methods: {
    async updateCurrentVersion() {
      try {
        await this.$axios
          .patch(`d-services/service-versions/${this.data.id}/set-current/`)
          .then((res) => {
            this.$snack("update", {
              message: "تم اعادة تحديث الاصدار الحالي للخدمة",
            });
          });

        this.refresh_selected_version = true;
        setTimeout(() => {
          this.refresh_selected_version = false;
        }, 100);
      } catch {
        this.data.is_current = !this.data.is_current;
      }
    },

    updateServiceVersions() {
      this.data = { ...this.selected_version };
    },
    resetData(type_ver) {
      const type = type_ver || "form";
      if (type == "form" && !this.data?.fields_schema?.fields) {
        this.data.fields_schema = {
          fields: [],
          attrs: "{}",
        };
      } else if (type == "wizard" && !Array.isArray(this.data?.fields_schema)) {
        this.data.fields_schema = [];
      }
    },

    async saveData() {     
      const data = {
        ...this.data,
        fk_service: this.serviceId,
      };
      if (this.data?.id) {
        await this.$axios.put(
          `d-services/service-versions/${this.data.id}/`,
          data
        );
       
        this.$alert("update");
      } else {
        await this.$axios.post("d-services/service-versions/", data);
        this.$alert("add");
      }
    },
  },
  watch: {
    "data.component_type": {
      handler(type) {
        this.resetData(type);
      },
    },
  },
};
</script>
