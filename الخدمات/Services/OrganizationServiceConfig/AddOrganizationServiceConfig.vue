<template>
  <drawer
    :data="data"
    :getData="getData"
    click="d-services/organization-service-config/"
  >
    <template v-slot>
      <div class="w-100">
        <filter-fields
          class="ma-3 border-dashed"
          label_class="text-primary"
          :label="$t('service_init')"
        >
          <template #fields>
            <fields
              :data="data"
              url="service-settings"
              group="service_init"
              :attr="{
                request_prefix: {
                  rules: [$required, $en, $max_length(20)],
                },
                is_paid: {
                  // Always visible
                  update: updateFields,
                },
                is_installment_allowed: {
                  depend: data.is_paid == true,
                },
              }"
            />
          </template>
        </filter-fields>
        <v-expand-transition class="v-col-12 pa-0">
          <div v-show="data?.is_paid">
            <filter-fields
              class="ma-3 border-dashed"
              label_class="text-primary"
              :label="$t('payment_set')"
            >
              <template #fields>
                <fields
                  :data="data"
                  url="service-settings"
                  group="payment_set"
                  :attr="{
                    is_installment_allowed: {
                      update: emptyInstallment,
                    },
                    free_limit_per_year: {
                      type: 'number',
                      rules: [$numeric],
                    },
                    fk_currency: {
                      rules: [$numeric],
                    },
                    fee_amount: {
                      type: 'number',
                      rules: data?.is_paid ? [$numeric, $min_value(1)] : [],
                    },
                    installments_count: {
                      depend: data.is_installment_allowed == true,
                      type: 'number',
                      rules: [$numeric, $min_value(1)],
                    },
                    installment_period: {
                      depend: data.is_installment_allowed == true,
                    },
                  }"
                />
              </template>
            </filter-fields>
          </div>
        </v-expand-transition>
        <filter-fields
          class="ma-3 border-dashed"
          label_class="text-primary"
          :label="$t('print_set')"
        >
          <template #fields>
            <fields
              :data="data"
              url="service-settings"
              group="print_set"
              :attr="{}"
            />
          </template>
        </filter-fields>
      </div>
    </template>
  </drawer>
</template>
<script>
export default {
  props: {
    data: Object,
  },

  methods: {
    updateFields(val) {
      if (!val) {
        this.data.fk_currency = null;
        this.data.fee_amount = 0;
        this.data.free_limit_per_year = 0;
        this.data.is_installment_allowed = false;

        this.emptyInstallment(false);
      }
    },

    emptyInstallment(val) {
      if (!val) {
        this.data.installments_count = 1;
        this.data.installment_period = null;
      }
    },
  },
};
</script>
