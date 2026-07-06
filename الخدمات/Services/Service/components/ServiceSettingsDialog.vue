<template>
  <add-organization-service-config
    v-model="dialog"
    :type="embedded ? 'section' : 'dialog'"
    width="1200"
    :items="[]"
    :data="settingsData"
    :re_open="false"
  />
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
      service_settings_data: {},
      url_service_settings: "d-services/organization-service-config/",
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
    settingsData() {
      // Use fk_service as id for PUT request URL
      return Object.assign(this.service_settings_data, {
        fk_service: this.service?.id,
        id: this.service?.id, // Use service id for PUT URL
      });
    },
  },
  methods: {
    async getServiceSettings() {
      if (!this.service?.id) return;
      return await this.$axios(
        `${this.url_service_settings}${this.service.id}/`
      ).then(
        (response) => (this.service_settings_data = response.data?.data ?? {})
      );
    },
  },
  watch: {
    dialog(val) {
      if (val) {
        this.getServiceSettings();
      }
    },
    "service.id": {
      handler(val) {
        if (val && this.embedded) {
          this.getServiceSettings();
        }
      },
      immediate: true,
    },
  },
};
</script>
