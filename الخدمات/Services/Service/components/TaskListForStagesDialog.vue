<template>
  <component
    :is="embedded ? 'div' : 'custom-dialog'"
    v-model="dialog"
    :title="$t('task_list_for_stages') + '(' + title + ')'"
    width="auto"
    min-width="1200"
  >
    <v-card rounded="lg" v-if="loading">
      <v-skeleton-loader type="table" height="300" />
    </v-card>
    <div v-else>
      <v-sheet
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
      </v-sheet>
      <auto-list
        v-model="filter.service_workflow_steps"
        name="ServiceWorkflowSteps"
        cols="3"
        :param="service.id"
        :add="false"
        :rules="[$required]"
        @update:modelValue="getData"
      />
      <div
        :class="{
          'disabled-row': !filter.service_workflow_steps,
        }"
      >
        <custom-data-table-with-save
          :="{
            headers: headers,
            getData: getData,
            items: items,
            top: false,
          }"
          :click="save"
          :canAdd="true"
        ></custom-data-table-with-save>
      </div>
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
  },
  emits: ["update:modelValue"],
  data() {
    return {
      loading: false,
      items: [],
      user_perms: {},
      url: "d-services/workflow-step-checklist-templates/",
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
          title: this.$t("order_task"),
          key: "order",
          field: {
            name: "order",
            null: false,
            type: "IntegerField",
            width: "120",
          },
        },
        {
          title: this.$t("title"),
          key: "title",
          field: {
            name: "title",
            null: false,
            type: "CharField",
            width: "300",
          },
        },
        {
          title: this.$t("description"),
          key: "description",
          field: {
            name: "description",
            null: false,
            type: "TextField",
            width: "300",
          },
        },
        {
          title: this.$t("is_required"),
          key: "is_required",
          field: {
            name: "is_required",
            null: false,
            type: "BooleanField",
          },
        },
      ];
    },
  },
  methods: {
    async getData() {
      if (this.filter.service_workflow_steps) {
        if (!this.service?.id) return;
        this.loading = true;
        await this.$axios(`${this.url}`, {
          params: {
            fk_workflow_step: this.filter?.service_workflow_steps,
          },
        })
          .then((response) => {
            this.items = response.data.data;
          })
          .finally(() => {
            this.loading = false;
          });
      }
    },
    async save() {
      console.log(this.items, "2222222222222222");
      const payload = {
        fk_workflow_step: this.filter?.service_workflow_steps,
        templates: this.items,
      };
      return await this.$axios.post(this.url, payload).then((res) => {
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
  },
};
</script>
