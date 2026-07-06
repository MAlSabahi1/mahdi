<template>
  <fieldset class="pa-2 border rounded ma-2 mt-3">
    <legend class="px-4">اختر الطلب</legend>
    <v-row>
      <auto-list
        v-model="filter.fk_service_category"
        name="ServiceCategory"
        :rules="[$required]"
        cols="3"
      />
      <auto-list
        v-model="filter.fk_service"
        name="DynamicServicesByCategory"
        :rules="[$required]"
        :param="filter.fk_service_category"
        cols="3"
      />
      <auto-list
        v-model="selected_request_id"
        name="ServicesRequestsByService"
        :param="filter.fk_service"
        :rules="[$required]"
        @update:modelValue="getServiceRequestHistory()"
        cols="3"
      />
    </v-row>
  </fieldset>
  <custom-data-table
    :="{
      headers: headers,
      items: service_request_history,
      getData: getServiceRequestHistory,
      pagination: false,
    }"
  />
</template>
<script>
export default {
  data() {
    return {
      data: {},
      filter: {},
      service_request_history: [],
      selected_request_id: this.$route?.query?.request_id
        ? Number(this.$route?.query?.request_id)
        : null,
      url_request_service: "d-services/services/instances/",
    };
  },
  async created() {
    if (this.selected_request_id) {
      await this.getServiceRequestHistory();
    }
  },
  methods: {
    async getServiceRequestHistory(params = this.$params) {
      if (this.selected_request_id) {
        return await this.$axios(
          `${this.url_request_service}${this.selected_request_id}/history/`,
          params
        ).then((response) => (this.service_request_history = response.data));
      }
    },
  },
  computed: {
    headers() {
      return [
        { title: this.$t("request_id"), key: "request_id" },
        { title: this.$t("service"), key: "service_name" },
        { title: this.$t("action_by_name"), key: "fk_action_by_name" },
        { title: this.$t("action_type_name"), key: "action_type_name" },
        {
          title: this.$t("current_stage"),
          key: "fk_from_stage_name",
        },
        { title: this.$t("next_stage"), key: "fk_to_stage_name" },
        {
          title: this.$t("instance_current_stage_name"),
          key: "instance_current_stage_name",
        },
        { title: this.$t("comments"), key: "comments" },
        { title: this.$t("created_at"), key: "created_at" },
      ];
    },
  },
};
</script>
