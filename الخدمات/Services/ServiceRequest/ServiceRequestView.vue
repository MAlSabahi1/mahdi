<template>

  <v-form ref="date_ref">
    <filter-fields :label="$t('filter_fields')">
      <template #fields>
        <fields :data="filter_fields" url="service-requests" :attr="{
          status: {
            null: true,
            hideDetails: true,
          },
          priority: {
            null: true,
            hideDetails: true,
          },
          payment_status: {
            null: true,
            hideDetails: true,
          },
          grant_status: {
            null: true,
            hideDetails: true,
          },
          discount_status: {
            null: true,
            hideDetails: true,
          },
          fk_requester: {
            null: true,
            hideDetails: true,
          },
          request_number: {
            null: true,
            hideDetails: true,
          },
          is_locked: {
            null: true,
            hideDetails: true,
          },
        }">
          <template v-slot="{ field }">

            <custom-date v-if="field?.name_list == 'date_from'" v-model="filter_fields.date_from" type="date" cols="3"
              :hideDetails="true" :label="$t('from')"></custom-date>
            <custom-date v-if="field?.name_list == 'date_to'" v-model="filter_fields.date_to" type="date" cols="3"
              :rules="[
                $time_min_max(filter_fields.date_from, filter_fields.date_to),
              ]" hideDetails="auto" :label="$t('to')"></custom-date>
          </template>
        </fields>
        <v-col cols="auto" class="px-0">
          <custom-btn type="filter" :loading="loading['filter_btn']" :click="beforeGetData"></custom-btn>
        </v-col>
      </template>
    </filter-fields>
  </v-form>
  <custom-data-table :="{
    headers,
    items,
    getData,
    actionList,
    customLoading: loading['filter_btn'],
  }">
    <template v-slot:item-slot="{ item, key }">
      <template v-if="
        [
          'priority__display',
          'status__display',
          'payment_status__display',
        ].includes(key)
      ">
        <v-chip size="small" :color="getChipColor(key, item)" variant="tonal">
          {{ item[key] }}
        </v-chip>
      </template>
      <div v-if="key == 'actions'" class="text-center">
        <custom-btn type="update" isIcon icon="mdi-eye" elevation="0" color="transparent" icon-color="primary"
          :label="'تفاصيل الطلب'" @click="moveToNex('request-details', { request_id: item?.id }, {})" />
        <custom-btn v-if="item?.status=='pending'" type="update" isIcon elevation="0" color="transparent" icon-color="green" :click="() => moveToNex('request-service', {}, { request_id: item?.id })
          " />
      </div>
    </template>
  </custom-data-table>
</template>
<script>
export default {
  data() {
    return {
      data: {},
      items: {},
      filter_fields: {},
      do_filter_fields: {},
      loading: {},
      drawer: false,

      url: "d-services/service-requests/",
    };
  },

  computed: {
    headers() {
      return [
        { title: this.$t("request_no"), key: "request_number" },
        { title: this.$t("requester_name"), key: "requester_name" },
        { title: this.$t("service"), key: "fk_service__name_ar" },
        { title: this.$t("requested_by"), key: "fk_requester__username" },
        { title: this.$t("requested_at"), key: "requested_at" },
        { title: this.$t("priority"), key: "priority__display" },
        { title: this.$t("status"), key: "status__display" },
        { title: this.$t("payment_status"), key: "payment_status__display" },
      ];
    },
  },
  methods: {
    beforeGetData() {
      this.do_filter_fields = this.filter_fields;
      this.getData();
    },
    async getData(params = this.$params) {
      try {
        if (await this.$validate(this.$refs["date_ref"])) {
          this.loading["filter_btn"] = true;
          await this.$axios(this.url, {
            params: {
              ...params?.params,
              ...this.do_filter_fields,
              fk_service: this.$route.params.fk_service,
            },
          }).then((response) => {
            this.items = response.data;
            this.do_filter_fields = {};
          });
        }
      } finally {
        this.loading["filter_btn"] = false;
      }
    },

    actionList(item) {
      return [
        {
          title_ar: "معالجة الطلب",
          title_en: "Processing Request",
          click: () => {
            this.moveToNex("processing-request", { request_id: item.id }, {});
          },
        },
        {
          title_ar: "تفاصيل الطلب",
          title_en: "Request Details",
          click: () => {
            this.moveToNex("request-details", { request_id: item?.id }, {});
          },
        },
        {
          title_ar: "تعديل الطلب",
          title_en: "Request Edit",
          click: () => {
            this.moveToNex("request-service", {}, { request_id: item?.id });
          },
        },
      ];
    },
    getChipColor(key, item) {
      if (key == "status__display") {
        const status = item.status;
        if (status === "pending") return "warning";
        if (status == "approved" || status == "completed") return "success";
        if (status == "rejected" || status == "cancelled") return "error";
        return "primary";
      }
      if (key == "priority__display") {
        const priority = item.priority;
        if (priority == "high" || priority == "urgent") return "error";
        if (priority == "normal") return "info";
        return "grey";
      }
      if (key == "payment_status__display") {
        const payment = item.payment_status;
        if (payment === "paid") return "success";
        if (payment == "unpaid") return "error";
        if (payment == "partial") return "warning";
        return "grey";
      }
      return "grey";
    },

    moveToNex(screen, param, query) {
      this.$navigateTo({
        name: screen,
        params: param,
        query: query,
        blank: false,
      });
    },
  },

  watch: {
    filter_fields: {
      async handler(val) {
        if (Object?.values(val)?.every((v) => !v)) {
          this.getData();
        } else if (val?.date_from) {
          await this.$validate(this.$refs["date_ref"]);
        }
      },
      deep: true,
    },
  },
};
</script>
