<template>
  <component
    :is="embedded ? 'div' : 'custom-dialog'"
    v-model="dialog"
    :title="$t('addServicePrerequisite') + '(' + title + ')'"
    width="auto"
    min-width="1700"
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
            : $perm('add', 'service-prerequisites') ||
              $perm('edit', 'service-prerequisites')
            ? save
            : null
        "
        :canAdd="is_details ? null : true"
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
      url: "d-services/service-prerequisites/",
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
          field: {
            name: "order",
            icon: "order-numeric-ascending",
            type: "PositiveIntegerField",
            null: false,
            disabled: true,
            width: "100",
          },
        },
        {
          title: this.$t("name_ar"),
          key: "name_ar",
          field: {
            name: "name_ar",
            type: "CharField",
            rules: [this.$ar],
            icon: "text",
            null: false,
            max_length: 255,
            width: "200",
          },
        },
        {
          title: this.$t("name_en"),
          key: "name_en",
          field: {
            name: "name_en",
            type: "CharField",
            rules: [this.$en],
            icon: "translate",
            max_length: 255,
            null: true,
            width: "200",
          },
        },

        {
          title: this.$t("status"),
          key: "status",
          field: {
            name: "status",
            type: "CharField",
            name_list: "PrerequisiteStatusChoice",
            null: false,
            width: "200",
          },
        },
        {
          title: this.$t("validation_procedure_name"),
          key: "validation_procedure_name",
          field: {
            name: "validation_procedure_name",
            type: "CharField",
            icon: "cog-outline",
            max_length: 255,
            placeholder: "Class.Function",
            name_list: "ValidatorFunctionsChoice",
            null: true,
            width: "250",
          },
        },
        {
          title: this.$t("description"),
          key: "description",
          field: {
            name: "description",
            type: "TextField",
            null: true,
            width: "260",
          },
        },
      ];
    },
  },
  methods: {
    async getData() {
      if (!this.service?.id) return;
      this.loading = true;
      await this.$axios
        .post(`${this.url}` + "filter/", {
          filters: [
            {
              field: "fk_service",
              value: this.service?.id,
            },
          ],
        })
        .then((response) => {
          this.items = response.data.data ?? [];
        })
        .finally(() => {
          this.loading = false;
        });
    },
    async save() {
      return await this.$axios
        .post(this.url, {
          fk_service: this.service.id,
          prerequisites: this.items,
        })
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
    "items.length"(val) {
      this.items?.forEach((prerequisite, index) => {
        prerequisite.order = index + 1;
      });
    },
  },
};
</script>
