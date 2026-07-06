<template>
  <v-snackbar v-model="show" :timeout="timeout" location="top center" class="premium-notification" variant="flat"
    color="transparent">
    <div :class="['notification-card-premium', `border-${type}`]">
      <div class="d-flex align-center pa-4">
        <!-- Icon Box with subtle animation -->
        <div :class="['icon-box-premium ml-4', `bg-${type}-soft`]">
          <v-icon :icon="iconComputed" color="white" size="20"></v-icon>
        </div>

        <div class="d-flex flex-column flex-grow-1">
          <span class="text-subtitle-2 font-weight-black text-slate-900 mb-0 leading-tight">
            {{ message }}
          </span>
          <span v-if="description" class="text-caption text-slate-500 font-weight-bold mt-1">
            {{ description }}
          </span>
        </div>

        <v-btn icon="mdi-close" variant="text" color="slate-300" size="x-small" class="ml-2 rounded-lg close-btn-toast"
          @click="show = false"></v-btn>
      </div>

      <!-- Smooth Progress Bar -->
      <div class="progress-container">
        <div :class="['progress-bar-premium', `bg-${type}`]" :style="{ width: progress + '%' }"></div>
      </div>
    </div>
  </v-snackbar>
</template>

<script>
export default {
  name: "BaseNotification",
  props: {
    modelValue: Boolean,
    message: { type: String, required: true },
    description: { type: String, default: "" },
    type: { type: String, default: "success" }, // success, error, warning, info
    timeout: { type: Number, default: 5000 },
  },
  emits: ["update:modelValue"],
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
    iconComputed() {
      const map = {
        success: "mdi-check-decagram",
        error: "mdi-close-octagon",
        warning: "mdi-alert-octagon",
        info: "mdi-information",
      };
      return map[this.type] || "mdi-check-decagram";
    },
  },
  watch: {
    show(val) {
      if (val) {
        this.startTimer();
      } else {
        clearInterval(this.interval);
      }
    },
  },
  methods: {
    startTimer() {
      this.progress = 100;
      const step = 100 / (this.timeout / 100);

      this.interval = setInterval(() => {
        this.progress -= step;
        if (this.progress <= 0) {
          clearInterval(this.interval);
        }
      }, 100);
    },
  },
  beforeUnmount() {
    clearInterval(this.interval);
  },
};
</script>

<style scoped>

.premium-notification :deep(.v-snackbar__wrapper) {
  background: transparent !important;
  box-shadow: none !important;
  min-width: 420px !important;
}

.notification-card-premium {
  position: relative;
  background: #ffffff !important;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
  border: 1px solid rgba(226, 232, 240, 0.8);
  font-family: 'Almarai', sans-serif !important;
  transition: all 0.3s ease;
}

.notification-card-premium:hover {
  transform: translateY(-2px);
  box-shadow: 0 25px 30px -5px rgba(0, 0, 0, 0.12) !important;
}

.icon-box-premium {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-card-premium:hover .icon-box-premium {
  transform: scale(1.1) rotate(5deg);
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

.bg-success {
  background-color: #10b981 !important;
}

.bg-error {
  background-color: #ef4444 !important;
}

.bg-warning {
  background-color: #f59e0b !important;
}

.bg-info {
  background-color: #06b6d4 !important;
}

.text-slate-900 {
  color: #0f172a !important;
}

.text-slate-500 {
  color: #64748b !important;
}

.close-btn-toast:hover {
  background-color: #f1f5f9 !important;
  color: #ef4444 !important;
}

.progress-container {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  background-color: rgba(241, 245, 249, 0.5);
}

.progress-bar-premium {
  height: 100%;
  transition: width 0.1s linear;
  border-radius: 0 2px 2px 0;
}

.leading-tight {
  line-height: 1.25;
}

@media (max-width: 600px) {
  .premium-notification :deep(.v-snackbar__wrapper) {
    min-width: 92vw !important;
  }
}
</style>
