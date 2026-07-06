<template>
  <AddERPSettings
    v-model="dialog"
    :type="embedded ? 'section' : 'dialog'"
    width="1200"
    :items="[]"
    :data="settingsData"
    :re_open="false"
  >

  </AddERPSettings>
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
      erp_org_settings: {},
      url_erp_org_settings: "d-services/service-erp-settings/",
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
      return Object.assign(this.erp_org_settings, {
        fk_service: this.service?.id,
        id: this.service?.id, // Use service id for PUT URL
      });
    },
  },
  methods: {
    async getERPOrgSettings() {
      if (!this.service?.id) return;
      return await this.$axios(
        `${this.url_service_settings}${this.service.id}/`
      ).then(
        (response) => (this.erp_org_settings = response.data?.data ?? {})
      );
    },
  },
  watch: {
    dialog(val) {
      if (val) {
        this.getERPOrgSettings();
      }
    },
    "service.id": {
      handler(val) {
        if (val && this.embedded) {
          this.getERPOrgSettings();
        }
      },
      immediate: true,
    },
  },
};
</script>
