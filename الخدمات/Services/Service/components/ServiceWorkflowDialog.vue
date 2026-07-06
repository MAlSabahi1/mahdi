<template>
  <component
    :is="embedded ? 'div' : 'custom-dialog'"
    v-model="dialog"
    :title="$t('addServiceWorkflow') + '(' + title + ')'"
    width="auto"
  >
    <v-card rounded="lg" v-if="loading">
      <v-skeleton-loader type="table" height="300" />
    </v-card>
    <div v-else>
      <custom-data-table-with-save
        :="{
          headers: headers,
          getData: getData,
          items: items,
          top: false,
        }"
        :click="
          is_details
            ? null
            : $perm('add', 'workflow-stages') || $perm('edit', '')
            ? save
            : null
        "
        :canAdd="is_details ? false : true"
      ></custom-data-table-with-save>
    </div>
  </component>
</template>

<script>
export default {
  props: {
    modelValue: Boolean,
    service: Object,
    embedded: {
      type: Boolean,
      default: false,
    },
    is_details: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      loading: false,
      items: [],
      workflow_stage_items: [],
      url: "d-services/service-workflow-steps/",
    };
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
          title: this.$t("order"),
          key: "order",
          field: (field_data) => ({
            name: "order",
            type: "PositiveSmallIntegerField",
            null: false,
            width: "100",
            disabled: true,
          }),
        },
        {
          title: this.$t("stage_name"),
          key: "fk_stage",
          field: (field_data) => ({
            name: "fk_stage",
            type: "ForeignKey",
            null: false,
            name_list: "WorkflowStages",
            width: "200",
            objects: this.workflow_stage_items,
            update: () => {
              const fk_stage_object = this.workflow_stage_items.find(
                (e) => e.id === field_data?.fk_stage
              );
              field_data.is_final_step = fk_stage_object?.is_final_stage;
              field_data.is_execution_step = fk_stage_object?.is_execution_stage;
            },
            rules: [this.$duplicate(this.items.map((e) => e.fk_stage))],
          }),
        },
        {
          title: this.$t("has_approval"),
          key: "has_approval",
          field: (field_data) => ({
            name: "has_approval",
            type: "BooleanField",
            null: true,
          }),
        },
        {
          title: this.$t("is_final_step"),
          key: "is_final_step",
          field: (field_data) => ({
            name: "is_final_step",
            type: "BooleanField",
            null: true,
          }),
        },
        {
          title: this.$t("is_execution_step"),
          key: "is_execution_step",
          field: (field_data) => ({
            name: "is_execution_step",
            type: "BooleanField",
            null: true,
            update: () => {
              if (!field_data.is_execution_step && field_data.execution_procedure_name) {
                field_data.execution_procedure_name = null;
              }
            },
          }),
        },
        {
          title: this.$t("execution_procedure_name"),
          key: "execution_procedure_name",
          field: (field_data) => ({
            name: "execution_procedure_name",
            type: "CharField",
            name_list: "ExecutionFunctionsChoice",
            disabled: !field_data?.is_execution_step,
            null: field_data?.is_execution_step ? false : true,
            width: "200",
          }),
        },
        {
          title: this.$t("has_custom_input"),
          key: "has_custom_input",
          field: (field_data) => ({
            name: "has_custom_input",
            type: "BooleanField",
            update: () => {
              if (!field_data?.has_custom_input) {
                field_data.custom_input_template = null;
                field_data.custom_input_function = null;
              }
            },
          }),
        },
        {
          title: this.$t("custom_input_template"),
          key: "custom_input_template",
          field: (field_data) => ({
            name: "custom_input_template",
            type: "CharField",
            name_list: "InputTemplateTypeChoice",
            null: field_data?.has_custom_input ? false : true,
            disabled: !field_data?.has_custom_input,
            width: "200",
          }),
        },
        {
          title: this.$t("custom_input_function"),
          key: "custom_input_function",
          field: (field_data) => ({
            name: "custom_input_function",
            type: "CharField",
            name_list: "InputFunctionsChoice",
            null: field_data?.has_custom_input ? false : true,
            disabled: !field_data?.has_custom_input,
            width: "200",
          }),
        },
        {
          title: this.$t("has_custom_output"),
          key: "has_custom_output",
          field: (field_data) => ({
            name: "has_custom_output",
            type: "BooleanField",
            update: () => {
              if (!field_data?.has_custom_output) {
                field_data.custom_output_template = null;
                field_data.custom_output_function = null;
              }
            },
          }),
        },
        {
          title: this.$t("custom_output_template"),
          key: "custom_output_template",
          field: (field_data) => ({
            name: "custom_output_template",
            type: "CharField",
            name_list: "OutputTemplateTypeChoice",
            null: field_data?.has_custom_output ? false : true,
            disabled: !field_data?.has_custom_output,
            width: "200",
          }),
        },
        {
          title: this.$t("custom_output_function"),
          key: "custom_output_function",
          field: (field_data) => ({
            name: "custom_output_function",
            type: "CharField",
            name_list: "OutputFunctionsChoice",
            null: field_data?.has_custom_output ? false : true,
            disabled: !field_data?.has_custom_output,
            width: "200",
          }),
        },
        {
          title: this.$t("start_offset_days"),
          key: "start_offset_days",
          field: (field_data) => ({
            name: "start_offset_days",
            type: "PositiveSmallIntegerField",
            rules: [this.$min_value(0), this.$max_value(365)],
            null: false,
            width: "100",
          }),
        },
        {
          title: this.$t("delivery_offset_days"),
          key: "delivery_offset_days",
          field: (field_data) => ({
            name: "delivery_offset_days",
            type: "PositiveSmallIntegerField",
            null: false,
            rules: [this.$min_value(0), this.$max_value(365)],
            width: "100",
          }),
        },
        {
          title: this.$t("icon"),
          key: "icon",
          field: (field_data) => ({
            name: "icon",
            type: "CharField",
            null: true,
            width: "200",
          }),
        },
        {
          title: this.$t("description"),
          key: "description",
          field: (field_data) => ({
            name: "description",
            type: "TextField",
            null: true,
            width: "200",
          }),
        },
      ];
    },
  },
  async created() {
    if (this.$dataList && this.$dataList().WorkflowStages) {
      this.workflow_stage_items = await this.$dataList().WorkflowStages.method();
    }
  },
  methods: {
    async getData() {
      if (!this.service?.id) return;
      this.loading = true;
      return await this.$axios
        .post(`${this.url}filter/`, {
          filters: [{ field: "fk_service", value: this.service.id }],
        })
        .then((response) => {
          this.items = response.data.data;
          this.loading = false;
        });
    },
    async save() {
      return await this.$axios
        .post(this.url, { fk_service: this.service.id, steps: this.items })
        .then((res) => {
          this.$snack("add", { message: res.data.message });
        });
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
      handler(val) {
        this.items?.forEach((item, index) => {
          item.order = index + 1;
        });
      },
    },
  },
};
</script>
