<template>
  <drawer
    :data="data"
    :getData="getData"
    :click="handleSubmit"
    type="dialog"
    width="70vw"
    :re_open="false"
  >
    <template v-slot>
      <div>
        <filter-fields
          class="ma-3 border-dashed"
          label_class="text-primary"
          :label="$t('basic_service_information')"
        >
          <template #fields>
            <fields
              :data="data"
              url="d-services"
              group="BSI"
              :attr="{
                name_ar: {
                  rules: [$required, $ar, $max_length(100)],
                },
                name_en: {
                  rules: [$en, $max_length(100)],
                },
              }"
            />
          </template>
        </filter-fields>
        <filter-fields
          class="ma-3 border-dashed"
          label_class="text-primary"
          :label="$t('operational_and_control_settings')"
        >
          <template #fields>
            <fields :data="data" url="d-services" group="OCS" :attr="{}" />
          </template>
        </filter-fields>
        <filter-fields
          class="ma-3 border-dashed"
          label_class="text-primary"
          :label="$t('forms_and_data_settings')"
        >
          <template #fields>
            <fields
              :data="data"
              url="d-services"
              group="FDS"
              :attr="{
                output_data_function: {
                  depend: data.output_template_type,
                  cols: 4,
                },
                input_data_function: {
                  depend: data.input_template_type,
                  cols: 4,
                },
              }"
            />
          </template>
        </filter-fields>
        <filter-fields
          class="ma-3 border-dashed"
          label_class="text-primary"
          :label="$t('application_data_settings')"
        >
          <template #fields>
            <fields :data="data" url="d-services" group="ADS" :attr="{}" />
          </template>
        </filter-fields>
        <filter-fields
          class="ma-3 border-dashed"
          label_class="text-primary"
          :label="$t('erp_services_settings')"
        >
          <template #fields>
            <fields :data="data" url="d-services" group="ERP" :attr="{}" />
          </template>
        </filter-fields>
        <!-- <fields
          :data="data"
          url="d-services"
          :group="true"
          :attr="{
            name_ar: {
              rules: [$required, $ar, $max_length(100)],
            },
            name_en: {
              rules: [$en, $max_length(100)],
            },
            installments_count: {
              depend: data.is_installment_allowed == true,
            },
            output_data_function: {
              depend: data.output_template_type,
              cols: 4,
            },
            input_data_function: {
              depend: data.input_template_type,
              cols: 4,
            },
          }"
        /> -->
      </div>
    </template>
  </drawer>
</template>
<script>
export default {
  props: {
    data: Object,
    getData: Function,
  },
  data() {
    return {
      url: "d-services/services/",
    };
  },
  methods: {
    async handleSubmit() {
      if (this.data.id) {
        // Update - use PATCH
        return await this.$axios.patch(
          `${this.url}${this.data.id}/`,
          this.data
        );
      } else {
        // Create - use POST
        return await this.$axios.post(this.url, this.data);
      }
    },
  },
};
</script>
