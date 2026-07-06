<template>
  <v-dialog v-model="show" max-width="420" persistent transition="scale-transition" origin="center center">
    <v-card class="premium-confirm-card" rounded="xl">
      <div class="confirm-content pa-8 text-center">
        <!-- Animated Icon Box -->
        <div class="icon-container mb-6">
          <div :class="['icon-ring', `ring-${type}`]"></div>
          <div :class="['icon-box-inner', `bg-${type}-soft`]">
            <v-icon :color="typeColor" size="36">
              {{ icon || typeIcon }}
            </v-icon>
          </div>
        </div>

        <h3 class="text-h6 font-weight-black text-slate-900 mb-1">
          {{ title }}
        </h3>
        <p v-if="subtitle" class="text-caption text-slate-500 mb-3 font-weight-medium">
          {{ subtitle }}
        </p>

        <p class="text-body-2 text-slate-600 mb-0 leading-relaxed px-2">
          {{ message }}
        </p>

        <div v-if="subMessage" class="sub-message-box mt-4 pa-3 rounded-lg bg-slate-50">
          <p class="text-caption text-slate-500 mb-0 font-weight-medium">
            {{ subMessage }}
          </p>
        </div>
      </div>

      <!-- Actions -->
      <div class="confirm-actions pa-6 d-flex align-center gap-3">
        <v-btn variant="tonal" color="slate-400" class="flex-grow-1 font-weight-bold rounded-lg action-btn-secondary"
          height="48" @click="show = false">
          {{ cancelText }}
        </v-btn>
        <v-btn :color="typeColor" variant="flat"
          class="flex-grow-1 font-weight-bold rounded-lg action-btn-primary elevation-0" height="48" :loading="loading"
          @click="confirmMessage">
          {{ confirmText }}
        </v-btn>
      </div>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "BaseConfirm",
  props: {
    modelValue: { type: Boolean, required: true },
    title: { type: String, required: true },
    subtitle: { type: String, default: "" },
    icon: { type: String, default: "" },
    message: { type: String, required: true },
    subMessage: { type: String },
    description: { type: String, default: "" },
    confirmText: { type: String, default: "تأكيد" },
    cancelText: { type: String, default: "إلغاء" },
    type: { type: String, default: "success" }, // success, error, warning, info
    loading: { type: Boolean, default: false },
  },
  emits: ["update:modelValue", "confirm"],
  data() {
    return {
      progress: 100,
      interval: null,
    };
  },
  computed: {
    show: {
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
        primary: "mdi-shield-check-outline",
        success: "mdi-check-decagram-outline",
        warning: "mdi-alert-octagon-outline",
        error: "mdi-close-octagon-outline",
        info: "mdi-information-outline",
      };
      return map[this.type] || "mdi-information-outline";
    },
  },
  methods: {
    confirmMessage() {
      this.$emit("confirm");
    },
  },
};
</script>

<style scoped>

.premium-confirm-card {
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.8);
  font-family: 'Almarai', sans-serif !important;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1) !important;
}

.icon-container {
  position: relative;
  width: 88px;
  height: 88px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-ring {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 32px;
  opacity: 0.15;
}

.ring-success {
  background-color: #10b981;
}

.ring-error {
  background-color: #ef4444;
}

.ring-warning {
  background-color: #f59e0b;
}

.ring-info {
  background-color: #06b6d4;
}

.ring-primary {
  background-color: #2563eb;
}

.icon-box-inner {
  width: 64px;
  height: 64px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
}

.bg-success-soft {
  background-color: #ecfdf5;
}

.bg-error-soft {
  background-color: #fef2f2;
}

.bg-warning-soft {
  background-color: #fffbeb;
}

.bg-info-soft {
  background-color: #f0f9ff;
}

.bg-primary-soft {
  background-color: #eff6ff;
}

@keyframes pulse-ring {
  0% {
    transform: scale(0.8);
    opacity: 0.2;
  }

  50% {
    transform: scale(1);
    opacity: 0.1;
  }

  100% {
    transform: scale(0.8);
    opacity: 0.2;
  }
}

.text-slate-900 {
  color: #0f172a !important;
}

.text-slate-600 {
  color: #475569 !important;
}

.text-slate-500 {
  color: #64748b !important;
}

.bg-slate-50 {
  background-color: #f8fafc !important;
}

.leading-relaxed {
  line-height: 1.8;
}

.gap-3 {
  gap: 12px;
}

.action-btn-primary {
  transition: all 0.3s ease;
}

.action-btn-primary:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}

.action-btn-secondary {
  background-color: #f1f5f9 !important;
  color: #64748b !important;
}

.action-btn-secondary:hover {
  background-color: #e2e8f0 !important;
}
</style>
