<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      <span>معssالج متعدد الخطوات</span>
      <v-spacer></v-spacer>
      <v-btn
        color="primary"
        prepend-icon="mdi-plus"
        variant="outlined"
        @click="addNewStep"
        >اضافة خطوة</v-btn
      >
    </v-card-title>
    <v-card-text>
      <VStepper v-if="steppers?.length > 0" v-model="step_index">
        <VStepperItem
          v-for="(step, index) in steppers"
          :key="step"
          :title="step.title"
          :value="index"
          editable
          :icon="step.icon"
          color="primary"
          @click.prevent
        >
          <template v-slot:title>
            <span class="mx-2 text-h6">{{ step.title }}</span>
            <v-icon
              v-if="step_index == index"
              @click="selectStep(index)"
              color="warning"
              class="me-2"
              >mdi-pencil</v-icon
            >
            <v-icon
              v-if="step_index == index"
              @click="deleteStep(index)"
              color="red"
              >mdi-delete</v-icon
            >
          </template>
        </VStepperItem>
        <VStepperWindow>
          <VStepperWindowItem
            v-for="(step, index) in steppers"
            :key="index"
            :value="index"
          >
            <json-editor
              :fields="step.fields"
              :attrs="step?.attrs ?? {}"
              @update:fields="step.fields = $event"
              @update:attrs="step.attrs = $event"
            ></json-editor>
          </VStepperWindowItem>
        </VStepperWindow>
      </VStepper>
      <div v-else class="text-center py-12">
        <v-avatar size="80" color="grey-lighten-2" class="mb-4">
          <v-icon size="40" color="grey">mdi-form-select</v-icon>
        </v-avatar>
        <h3 class="text-h6 mb-2 text-grey-darken-1">لا توجد خطوات مضافة</h3>
        <p class="text-body-2 text-grey mb-4">
          ابدأ بإضافة خطوة جديدة لبناء النموذج الخاص بك
        </p>
        <v-btn
          @click="addNewStep"
          color="primary"
          prepend-icon="mdi-plus"
          class="text-none"
        >
          إضافة خطوة جديدة
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
  <v-dialog v-model="add_step_dialog" width="400">
    <v-card>
      <v-card-title class="my-2"> بيانات الخطوة </v-card-title>
      <v-card-text>
        <v-form @submit.prevent ref="form">
          <v-text-field
            v-model="step_temp.title"
            label="ادخل عنوان الخطوة"
            :rules="[$required]"
            density="compact"
            variant="outlined"
            color="primary"
            ref="title"
            autofocus
          >
          </v-text-field>
          <v-text-field
            v-model="step_temp.subtitle"
            label="ادخل العنوان الفرعي للخطوة"
            density="compact"
            variant="outlined"
            color="primary"
          >
          </v-text-field>
          <v-text-field
            v-model="step_temp.icon"
            label="ادخل ايقونة الخطوة"
            density="compact"
            variant="outlined"
            color="primary"
          >
          </v-text-field>
          <v-btn
            v-if="!is_update"
            color="primary"
            type="submit"
            @click="addStep"
            >اضافة</v-btn
          >
          <v-btn v-else color="success" @click="updateStep">تعديل</v-btn>
          <v-btn class="ms-2" variant="tonal" @click="cancel">الغاء</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  props: {
    modelValue: {
      type: Object,
      default: () => [],
    },
  },
  data() {
    return {
      step_index: 0,
      // steppers: [],
      add_step_dialog: false,
      step_temp: {},
      is_update: false,
      selected_step_id: null,
    };
  },

  methods: {
    addNewStep() {
      this.step_temp = {};
      this.add_step_dialog = true;
    },
    deleteStep(step_id) {
      this.steppers.splice(step_id, 1);
    },
    selectStep(step_id) {
      this.is_update = true;
      this.add_step_dialog = true;
      this.selected_step_id = step_id;
      this.step_temp = {
        ...(this.steppers?.find((stepper, index) => index == step_id) ?? {}),
      };
    },
    cancel() {
      this.add_step_dialog = false;
      this.step_temp = {};
    },
    async addStep() {
      const { valid } = await this.$refs.form.validate();
      if (valid) {
        this.steppers.push({ fields: [], attrs: {}, ...this.step_temp });
        this.step_temp = {};
        this.$refs.title.focus();
      }
    },

    async updateStep() {
      const { valid } = await this.$refs.form.validate();
      if (valid) {
        this.steppers[this.selected_step_id] = this.step_temp;
        this.step_temp = {};
        this.is_update = false;
      }
    },
  },
  computed: {
    steppers:{
      get(){
        return this.modelValue
      },
      set(val){
        this.$emit('update:modelValue',val)
      }
    }
  },
};

</script>
