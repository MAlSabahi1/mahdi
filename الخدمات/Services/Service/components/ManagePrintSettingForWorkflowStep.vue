<template>
  <custom-dialog
    v-model="dialog"
    :title="'ادارة اعدادات الطباعة لخطوات سير العمل' + '(' + title + ')'"
    width="auto"
    min-width="1200"
  >
    <!-- <v-card rounded="lg" v-if="loading">
        <v-skeleton-loader type="table" height="300" />
      </v-card> -->
    <div>
      <!-- <v-sheet
          border
          rounded="lg"
          class="mb-4 pa-3 d-flex align-center justify-space-between bg-grey-lighten-5"
        >
          <div class="d-flex align-center">
            <v-avatar color="primary" variant="tonal" size="40" class="me-3">
              <v-icon>mdi-shield-account-outline</v-icon>
            </v-avatar>
            <div>
              <div class="text-subtitle-1 font-weight-bold">
                {{ $t("task_list_for_stages") }}
              </div>
              <div class="text-caption text-medium-emphasis">
                تحكم في وصول الصلاحيات المختلفة لهذه المرحلة
              </div>
            </div>
          </div>
        </v-sheet> -->
      <!-- <auto-list
          v-model="filter.service_workflow_steps"
          name="ServiceWorkflowSteps"
          cols="3"
          :param="service.id"
          :add="false"
          :rules="[$required]"
          @update:modelValue="getData"
        /> -->

      <custom-data-table-with-save
        :="{
          headers: headers,
          getData: getData,
          items: items,
          top: false,
          canAdd: false,
        }"
        :click="$perm('edit', 'services-catalog') ? saveData : null"
      ></custom-data-table-with-save>
    </div>
  </custom-dialog>
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
  },
  emits: ["update:modelValue"],
  data() {
    return {
      loading: false,
      items: [],
      //   requester_img_fun_list: [],
      //   requester_info_fun_list: [],
      user_perms: {},
      url: "d-services/workflow-step-print-report-settings/",
      filter: {},
    };
  },
  async created() {},
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
          title: this.$t("workflow_step__fk_stage__name_ar"),
          key: "fk_workflow_step__fk_stage__name_ar",
        },
        {
          title: this.$t("print_report_setting_for_input"),
          key: "fk_print_report_setting_for_input",
          width: "250px",
          field: {
            name: "fk_print_report_setting_for_input",
            type: "ForeignKey",
            null: true,
            label_ar: "إعدادات الطباعة لاستمارة المرحلة",
            label_en: "Print Report Setting For Input",
            max_length: null,
            default: null,
            icon: null,
            group: "print_set",
            name_list: "PrintReportSetting",
            model: "",

            hideDetails: true,
          },
        },
        {
          title: this.$t("print_report_setting_for_output"),
          key: "fk_print_report_setting_for_output",
          field: {
            name: "fk_print_report_setting_for_output",
            type: "ForeignKey",
            null: true,
            label_ar: "إعدادات الطباعة لمخرج المرحلة",
            label_en: "Print Report Setting For Output",
            max_length: null,
            default: null,
            icon: null,
            group: "print_set",
            name_list: "PrintReportSetting",
            model: null,

            hideDetails: true,
          },
        },
      ];
    },
  },
  methods: {
    // async runFunctions() {
    //   this.requester_img_fun_list =
    //     await this.$dataList()?.RequesterFunctionsChoice?.methods();
    //   this.requester_img_fun_list =
    //     await this.$dataList()?.RequesterFunctionsChoice?.methods();
    // },
    async getData() {
      if (!this.service?.id) return;
      this.loading = true;
      await this.$axios(`${this.url}`, {
        params: {
          fk_service: this.service?.id,
        },
      })
        .then((response) => {
          console.log(response?.data);
          this.items = response.data.data;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    async saveData() {
      //   const payload = {
      //     fk_workflow_step: this.filter?.service_workflow_steps,
      //     templates: this.items,
      //   };
      return await this.$axios
        .put(this.url + "666/", {
          fk_service: this.service?.id,
          settings: this.items,
        })
        .then((res) => {
          this.$snack("add", { message: res.data.message });
        });
    },
  },
  watch: {
    dialog(val) {
      if (val) {
        // this.runFunctions();
        this.getData();
      }
    },
  },
};
</script>
