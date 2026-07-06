<template>
  <component
    :is="embedded ? 'div' : 'custom-dialog'"
    v-model="dialog"
    height="auto"
    persistent
    :title="$t('serviceInstallmentsPlan') + '(' + title + ')'"
    width="1000px"
  >
    <v-card rounded="lg" v-if="loading">
      <v-skeleton-loader type="table" height="300" />
    </v-card>
    <div v-else class="pa-4">
      <div v-if="service_settings_data?.is_installment_allowed">
        <!-- خطة الاقساط -->
        <v-row class="mb-4">
          <v-col cols="12" md="6">
            <v-card elevation="0" border rounded="xl" class="overflow-hidden">
              <div class="d-flex align-center pa-4 bg-gradient-success-light">
                <v-avatar
                  color="success"
                  variant="elevated"
                  size="48"
                  class="me-4 elevation-2"
                >
                  <v-icon size="28">mdi-cash-multiple</v-icon>
                </v-avatar>
                <div>
                  <div
                    class="text-caption text-success font-weight-bold text-uppercase"
                  >
                    إجمالي الرسوم
                  </div>
                  <div class="text-h5 font-weight-black">
                    {{ service_settings_data?.fee_amount }}
                    <span class="text-caption font-weight-medium">ر.ي</span>
                  </div>
                </div>
              </div>
            </v-card>
          </v-col>
          <v-col cols="12" md="6">
            <v-card elevation="0" border rounded="xl" class="overflow-hidden">
              <div class="d-flex align-center pa-4 bg-gradient-info-light">
                <v-avatar
                  color="info"
                  variant="elevated"
                  size="48"
                  class="me-4 elevation-2"
                >
                  <v-icon size="28">mdi-calendar-clock</v-icon>
                </v-avatar>
                <div>
                  <div
                    class="text-caption text-info font-weight-bold text-uppercase"
                  >
                    خطة الأقساط
                  </div>
                  <div class="text-h5 font-weight-black">
                    {{ service_settings_data?.installments_count }}
                    <span class="text-caption font-weight-medium"
                      >أقساط مجدولة</span
                    >
                  </div>
                </div>
              </div>
            </v-card>
          </v-col>
        </v-row>

        <v-sheet border rounded="xl" class="pa-1">
          <custom-data-table-with-save
            :="{
              headers: headers,
              getData: getData,
              items: items,
              top: false,
            }"
            :click="save"
            :canAdd="true"
          >
          </custom-data-table-with-save>
        </v-sheet>
      </div>

      <!-- رسالة عدم القدرة على تحديد اقساط الخدمة - تصميم Empty State احترافي -->
      <div v-else class="d-flex flex-column align-center justify-center py-12">
        <v-sheet
          elevation="0"
          rounded="circle"
          color="warning-lighten-5"
          class="pa-6 mb-6 d-flex align-center justify-center"
          style="width: 120px; height: 120px; border: 2px dashed #fb8c00"
        >
          <v-icon size="64" color="warning">mdi-credit-card-off-outline</v-icon>
        </v-sheet>

        <h3 class="text-h5 font-weight-bold mb-2">التقسيط غير متاح حالياً</h3>
        <p
          class="text-body-1 text-medium-emphasis text-center mb-8"
          style="max-width: 400px"
        >
          لا يمكن إعداد خطة أقساط لهذه الخدمة لأنها إما خدمة مجانية أو لم يتم
          تفعيل خيار التقسيط في إعداداتها الأساسية.
        </p>

        <v-row justify="center" class="w-100 mb-8">
          <v-col cols="12" sm="5" md="4">
            <v-card
              border
              elevation="0"
              rounded="lg"
              class="pa-4 text-center h-100"
            >
              <v-icon color="error" class="mb-2">mdi-currency-usd-off</v-icon>
              <div class="text-subtitle-2 font-weight-bold">
                الخدمة غير مدفوعة
              </div>
            </v-card>
          </v-col>
          <v-col cols="12" sm="5" md="4">
            <v-card
              border
              elevation="0"
              rounded="lg"
              class="pa-4 text-center h-100"
            >
              <v-icon color="info" class="mb-2"
                >mdi-calendar-remove-outline</v-icon
              >
              <div class="text-subtitle-2 font-weight-bold">
                التقسيط غير مفعل
              </div>
            </v-card>
          </v-col>
        </v-row>

        <v-btn
          color="primary"
          size="large"
          variant="elevated"
          prepend-icon="mdi-cog-outline"
          @click="requestSwitch"
          class="rounded-pill px-8"
        >
          تعديل إعدادات الخدمة
        </v-btn>
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
  emits: ["update:modelValue", "switch-to-first"],
  data() {
    return {
      loading: false,
      items: [],
      service_settings_data: {},
      url: "d-services/service-installment-plans/",
      installment_period_items: [],
    };
  },
  async created() {
    if (this.$dataList && this.$dataList().InstallmentPeriodChoice) {
      this.installment_period_items =
        await this.$dataList().InstallmentPeriodChoice.method();
    }
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
        // {
        //   title: this.$t("installment_period"),
        //   key: "installment_period",
        //   field: {
        //     name: "installment_period",
        //     type: "ForeignKey",
        //     null: false,
        //     name_list: "InstallmentPeriodChoice",
        //     width: "150",
        //     objects: this.installment_period_items,
        //   },
        // },
        {
          title: this.$t("order"),
          key: "order",
          field: {
            name: "order",
            icon: "order-numeric-ascending",
            type: "PositiveIntegerField",
            null: false,
            disabled: true,
            // width: "100",
          },
        },
        {
          title: this.$t("amount"),
          key: "amount",
          field: (field_data) => ({
            name: "amount",
            type: "PositiveIntegerField",
            rules: [this.$numeric],
            icon: "cash",
            null: false,
            width: "150",
          }),
        },

        {
          title: this.$t("due_days_from_request"),
          key: "due_days_from_request",
          field: {
            name: "due_days_from_request",
            icon: "calendar",
            rules: [this.$numeric],
            type: "PositiveIntegerField",
            null: false,
            width: "150",
          },
        },
      ];
    },
  },
  methods: {
    async getData() {
      this.loading = true;
      await this.$axios(`${this.url}`, {
        params: {
          fk_service: this.service?.id,
        },
      })
        .then((response) => {
          this.items = response.data?.data ?? [];
          if (!this.service_settings_data) this.service_settings_data = {};
          this.service_settings_data["installments_count"] =
            response.data?.installments_count;
          this.service_settings_data["is_installment_allowed"] =
            response.data?.is_installment_allowed;
          this.service_settings_data["fee_amount"] = response.data?.fee_amount;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    async save() {
      if (this.service?.id) {
        return await this.$axios
          .post(this.url, {
            fk_service: this.service.id,
            plans: this.items,
          })
          .then((res) => {
            this.$snack("add", { message: res.data?.message });
          });
      }
    },
    requestSwitch() {
      this.$emit("switch-to-first");
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
      this.items?.forEach((plan, index) => {
        plan.order = index + 1;
      });
    },
  },
};
</script>
