<template>
  <v-dialog
    v-model="internalValue"
    :max-width="maxWidth"
    persistent
    transition="scale-transition"
    scrollable
  >
    <v-card class="premium-dialog-card" rounded="xl">
      <!-- Premium Header -->
      <div class="dialog-header-premium px-6 py-5 d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <div :class="['header-icon-wrapper ml-4', `bg-${type}-soft`]">
            <v-icon
              :icon="icon?.includes('mdi') ? icon : `mdi-${icon}`"
              :color="typeColor"
              size="22"
            ></v-icon>
          </div>
          <div>
            <h3 class="text-h6 font-weight-black text-slate-900 mb-0 leading-tight">
              {{ title }}
            </h3>
            <p v-if="subtitle" class="text-caption text-slate-500 mb-0 font-weight-medium">
              {{ subtitle }}
            </p>
          </div>
        </div>
        <v-btn
          icon="mdi-close"
          variant="tonal"
          color="slate-300"
          size="small"
          class="rounded-circle close-btn-premium"
          @click="close"
        ></v-btn>
      </div>

      <v-divider class="border-slate-100"></v-divider>

      <!-- Content Area -->
      <v-card-text class="pa-0 bg-white ">
        <div class="dialog-content-inner pa-6 pa-md-8">
          <slot>
            <v-form ref="fields_form">
              <v-row>
                <slot name="fields">
                  <fields :="{ data, fields }"></fields>
                </slot>
              </v-row>
            </v-form>
          </slot>
        </div>
      </v-card-text>

      <v-divider class="border-slate-100"></v-divider>

      <!-- Actions -->
      <div v-if="actions" class="dialog-actions-premium pa-6 bg-slate-50 d-flex align-center gap-3">
        <v-btn
          variant="tonal"
          color="slate-400"
          class="px-8 font-weight-bold rounded-lg action-btn-secondary"
          height="48"
          @click="close"
          :disabled="loading"
        >
          {{ cancelText }}
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          v-if="!hideConfirm"
          :color="confirmColor || typeColor"
          variant="flat"
          class="px-12 font-weight-black rounded-lg action-btn-primary elevation-0"
          height="48"
          :loading="loading"
          @click="handleConfirm"
        >
          {{ confirmText }}
        </v-btn>
      </div>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "BaseDialog",
  emits: ["update:modelValue", "confirm", "cancel"],
  props: {
    modelValue: Boolean,
    title: { type: String, required: true },
    subtitle: { type: String, default: "" },
    type: { type: String, default: "primary" }, // primary, success, warning, error, info
    maxWidth: { type: [String, Number], default: 640 },
    maxHeight: { type: [String, Number], default: 450 },
    confirmText: { type: String, default: "تأكيد" },
    icon: { type: String, default: "information-outline" },
    cancelText: { type: String, default: "إلغاء" },
    loading: { type: Boolean, default: false },
    hideConfirm: { type: Boolean, default: false },
    confirmColor: { type: String, default: "" },
    fields: { type: Array, default: [] },
    attr: { type: Array, default: {} },
    data: { type: Array, default: {} },
    actions: { type: Boolean, default: true },
  },
  computed: {
    internalValue: {
      get() {
        return this.modelValue;
      },
      set(val) {
        this.$emit("update:modelValue", val);
      },
    },
    typeColor() {
      const map = {
        primary: "#2563eb",
        success: "#10b981",
        warning: "#f59e0b",
        error: "#ef4444",
        info: "#06b6d4",
      };
      return map[this.type] || "#2563eb";
    },
    typeIcon() {
      const map = {
        primary: "shield-check-outline",
        success: "check-decagram-outline",
        warning: "alert-octagon-outline",
        error: "close-octagon-outline",
        info: "information-outline",
      };
      return map[this.type] || "mdi-information-outline";
    },
  },
  methods: {
    async handleConfirm() {
      if (await this.$validate(this.$refs["fields_form"])) {
        this.$emit("confirm");
      }
    },
    close() {
      this.$emit("update:modelValue", false);
      this.$emit("cancel");
    },
  },
};
</script>

<style scoped>

.premium-dialog-card {
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.8);
  font-family: 'Almarai', sans-serif !important;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15) !important;
  display: flex;
  flex-direction: column;
}

.dialog-header-premium {
  background: #ffffff;
  position: sticky;
  top: 0;
  z-index: 10;
}

.header-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.premium-dialog-card:hover .header-icon-wrapper {
  transform: scale(1.05);
}

.bg-primary-soft { background-color: #eff6ff; }
.bg-success-soft { background-color: #ecfdf5; }
.bg-warning-soft { background-color: #fffbeb; }
.bg-error-soft { background-color: #fef2f2; }
.bg-info-soft { background-color: #f0f9ff; }

.close-btn-premium {
  transition: all 0.2s ease;
}

.close-btn-premium:hover {
  background-color: #f1f5f9 !important;
  color: #ef4444 !important;
  transform: rotate(90deg);
}

.dialog-actions-premium {
  position: sticky;
  bottom: 0;
  z-index: 10;
}

.text-slate-900 { color: #0f172a !important; }
.text-slate-500 { color: #64748b !important; }
.bg-slate-50 { background-color: #f8fafc !important; }
.border-slate-100 { border-color: #f1f5f9 !important; }

.leading-tight { line-height: 1.25; }
.gap-3 { gap: 12px; }

.action-btn-primary {
  transition: all 0.3s ease;
}

.action-btn-primary:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.action-btn-secondary {
  background-color: #f1f5f9 !important;
  color: #64748b !important;
  transition: all 0.2s ease;
}

.action-btn-secondary:hover {
  background-color: #e2e8f0 !important;
}

@media (max-width: 600px) {
  .dialog-content-inner {
    padding: 20px !important;
  }
}
</style>
