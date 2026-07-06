<template>
  <!-- <v-row v-if="templateType == 'form' && fields_schema?.fields?.length > 0">
    <ServiceFields :data="data" :fields="fields_schema?.fields ?? []" :attrs="fields_schema?.attrs ?? {}">
    </ServiceFields>
  </v-row> -->

  <VStepper complete-icon="mdi-check" v-model="step_index" class="border-t mx-2 elevation-1" flat
    v-if="templateType == 'wizard'" @click.prevent>
    <VStepperItem v-for="(step, index) in fields_schema" :key="step" :title="step.title" :value="index" editable
      :icon="step.icon" class="elevation-1" color="primary" :error="form_valid[index] === false">
    </VStepperItem>
    <VStepperWindow>
      <template v-for="(step, index) in fields_schema" :key="index">
        <v-form ref="form" v-model="form_valid[index]">
          <VStepperWindowItem :value="index">
            <ServiceFields :fields="step.fields" :data="data" :attrs="step.attrs" />
          </VStepperWindowItem>
        </v-form>
      </template>
    </VStepperWindow>
  </VStepper>

</template>

<script>

export default {
  name: "FormPreview",
  props: {
    fields_schema: {
      type: [Array, Object],
      required: true,
    },
    data: {
      type: Object,
      required: true
    },
    templateType: {
      type: String,
      default: 'form'
    }
  },
  data() {
    return {
      step_index: 0,
      form_valid: [],
    };
  },

  computed: {

  },
};
</script>
