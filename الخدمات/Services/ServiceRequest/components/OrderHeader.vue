<template>
  <div class="header-root">
    <v-card class="header-card-premium elevation-0 rounded-0 border-b">
      <div class="header-content px-6 py-4">
        <div class="d-flex align-center justify-space-between gap-4 flex-wrap">
          <!-- Right Side: Navigation & Identity -->
          <div
            class="d-flex align-center flex-grow-1 header-main-section min-w-0"
          >
            <v-btn
              icon
              variant="text"
              color="slate-500"
              class="back-btn-premium ml-4"
              @click="$router?.back()"
            >
              <v-icon icon="mdi-arrow-right" size="24"></v-icon>
            </v-btn>

            <div class="d-flex flex-column min-w-0">
              <div class="d-flex align-center gap-3 mb-1">
                <h1 class="page-title mb-0 text-truncate">
                  {{ title }}
                </h1>
                <!-- Request ID Badge -->
                <div class="id-badge-premium">
                  <span class="hash">#</span>{{ requestId }}
                </div>
              </div>

              <div
                class="
                  d-flex
                  align-center
                  gap-3
                  text-caption text-slate-500
                  header-meta
                  flex-wrap
                "
              >
                <span class="d-flex align-center">
                  <v-icon
                    icon="mdi-calendar-blank-outline"
                    size="14"
                    class="ml-1"
                  ></v-icon>
                  {{ date }}
                </span>
                <span class="meta-dot d-none d-sm-block">•</span>
                <span
                  :style="{ color: priorityColor }"
                  class="font-weight-bold d-flex align-center"
                >
                  {{ priorityText }}
                </span>
                <span class="meta-dot">•</span>
                <span
                  class="status-text-premium"
                  :style="{ color: statusColor }"
                >
                  <v-progress-circular
                    v-if="statusLoading"
                    indeterminate
                    size="10"
                    width="2"
                    class="ml-1"
                  ></v-progress-circular>
                  {{ statusText }}
                </span>
              </div>
            </div>
          </div>

          <!-- Left Side: Actions -->
          <div class="d-flex align-center gap-2 header-actions">
            <!-- Quick Status Indicator (Visual) -->
            <div
              class="status-pill-premium mr-4 hidden-sm-and-down"
              :style="{ '--c': statusColor }"
            >
              <v-icon :icon="statusIcon" size="16" class="ml-1"></v-icon>
              <span>{{ statusText }}</span>
            </div>

            <div class="divider-vertical mx-2 hidden-sm-and-down"></div>

            <div class="action-buttons d-flex align-center gap-2">
              <v-tooltip
                text="قفل الطلب"
                location="top"
                v-if="checkActionPermission('LOCK')"
              >
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    variant="flat"
                    color="error-soft"
                    class="action-btn-premium text-error"
                    height="40"
                    @click="openDialog('lock')"
                  >
                    <v-icon icon="mdi-lock-outline" class="mr-md-2"></v-icon>
                    <span class="d-none d-md-block">قفل</span>
                  </v-btn>
                </template>
              </v-tooltip>

              <v-tooltip
                text="فتح الطلب"
                location="top"
                v-if="checkActionPermission('UNLOCK')"
              >
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    variant="flat"
                    color="success-soft"
                    class="action-btn-premium text-success"
                    height="40"
                    @click="openDialog('unlock')"
                  >
                    <v-icon
                      icon="mdi-lock-open-variant-outline"
                      class="mr-md-2"
                    ></v-icon>
                    <span class="d-none d-md-block">فتح</span>
                  </v-btn>
                </template>
              </v-tooltip>
            </div>
          </div>
        </div>
      </div>
    </v-card>
  </div>
  <BaseDialog
    v-model="dialog.show"
    :data="data"
    v-bind="dialog"
    @confirm="toggleLockUnlockRequest(dialog?.action)"
  >
  </BaseDialog>
  <BaseNotification v-model="notification.show" v-bind="notification" />
</template>

<script>
export default {
  name: "OrderHeader",
  props: {
    requestId: { type: String, required: true },
    title: { type: String, required: true },
    subtitle: { type: String, default: "" },
    date: { type: String, required: true },
    priority: { type: String, default: "normal" },
    status: { type: String, default: "in_progress" },
    statusLoading: { type: Boolean, default: false },
  },
  emits: ["lock"],
  inject: ["context", "getRequestDetails", "checkActionPermission"],
  data() {
    return {
      data: {},
      dialog: {
        show: false,
      },
      notification: {},
      request_details: this.context?.request_details ?? {},
      url: this.context?.url,
      request_id: this.context?.request_id,
    };
  },
  methods: {
    async toggleLockUnlockRequest(action) {
      try {
        this.dialog.loading = true;
        await this.$axios
          .post(`${this.url}${this.request_id}/${action}/`, this.data)
          .then(async (res) => {
            await this.getRequestDetails();
            this.showNotification(
              this.$t(`${action}_msg_title`),
              this.$t(`${action}_msg_success`),
              "success"
            );
          });
      } catch (error) {
      } finally {
        this.dialog.loading = false;
        this.dialog = {};
        this.data = {};
      }
    },
    showNotification(msg, desc, type = "success") {
      this.notification.message = msg;
      this.notification.description = desc;
      this.notification.type = type;
      this.notification.show = true;
    },

    openDialog(type) {
      switch (type) {
        case "lock":
          this.dialog = {
            title: "قفل الطلب",
            type: "error",
            action: type,
            icon: "mdi-lock-outline",
            fields: [
              {
                name: "locked_reason",
                type: "TextField",
                null: false,
                label_ar: "ملاحظة سبب اقفال الطلب",
                max_length: 100,
                default: null,
                min_length: null,
                icon: "text-long",
                group: null,
                name_list: null,
                width: null,
                model: null,
              },
            ],
          };
          break;
        case "unlock":
          this.dialog = {
            title: "فتح الطلب",
            type: "success",
            action: type,
            icon: "lock-open-variant-outline",
            fields: [
              {
                name: "unlock_reason",
                type: "TextField",
                null: false,
                label_ar: "ملاحظة سبب فتح الطلب",
                max_length: 100,
                default: null,
                min_length: null,
                icon: "text-long",
                group: null,
                name_list: null,
                width: null,
                model: null,
              },
            ],
          };
          break;

        default:
          break;
      }
      this.dialog.show = true;
    },
  },

  computed: {
    priorityText() {
      const map = { high: "عالي جداً", normal: "متوسط", low: "منخفض" };
      return map[this.priority] || "عادي";
    },
    priorityColor() {
      const map = { high: "#f43f5e", normal: "#f59e0b", low: "#10b981" };
      return map[this.priority] || "#3b82f6";
    },
    priorityIcon() {
      const map = {
        high: "mdi-fire",
        normal: "mdi-lightning-bolt",
        low: "mdi-leaf",
      };
      return map[this.priority] || "mdi-information";
    },
    statusText() {
      const map = {
        pending: "قيد الانتظار",
        in_progress: "جاري المعالجة",
        completed: "مكتمل",
        rejected: "مرفوض",
      };
      return map[this.status] || "غير معروف";
    },
    statusColor() {
      const map = {
        pending: "#64748b",
        in_progress: "#2563eb",
        completed: "#10b981",
        rejected: "#ef4444",
      };
      return map[this.status] || "#94a3b8";
    },
    statusIcon() {
      const map = {
        pending: "mdi-clock-fast",
        in_progress: "mdi-progress-check",
        completed: "mdi-check-decagram",
        rejected: "mdi-alert-octagon",
      };
      return map[this.status] || "mdi-help-circle";
    },
  },
};
</script>

<style scoped>
.header-root {
  width: 100%;
  font-family: "Almarai", sans-serif !important;
}

.header-card-premium {
  background: rgba(255, 255, 255, 0.85);
  /* backdrop-filter: blur(12px); */
  /* -webkit-backdrop-filter: blur(12px); */
  border-bottom: 1px solid rgba(226, 232, 240, 0.8) !important;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02),
    0 2px 4px -1px rgba(0, 0, 0, 0.02) !important;
  z-index: 10;
  transition: all 0.3s ease;
}

.page-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

/* Back Button */
.back-btn-premium {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background-color: #f8fafc;
  border: 1px solid #f1f5f9;
}

.back-btn-premium:hover {
  background-color: #ffffff;
  border-color: #e2e8f0;
  color: #0f172a !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transform: translateX(2px);
}

/* ID Badge */
.id-badge-premium {
  background: #f1f5f9;
  padding: 3px 10px;
  border-radius: 8px;
  font-family: monospace;
  font-size: 13px;
  font-weight: 700;
  color: #475569;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.id-badge-premium:hover {
  border-color: #cbd5e1;
  background: #e2e8f0;
}

.id-badge-premium .hash {
  color: #94a3b8;
  margin-left: 2px;
}

/* Meta Info */
.header-meta {
  font-size: 13px;
  font-weight: 500;
}

.meta-dot {
  color: #cbd5e1;
  font-size: 8px;
  /* Slightly smaller dot */
}

/* Top Status & Date items */
.meta-item-badge {
  padding: 2px 8px;
  border-radius: 6px;
  background-color: transparent;
  transition: background-color 0.2s ease;
}

.meta-item-badge:hover {
  background-color: #f8fafc;
}

/* Status Pill (Big One) */
.status-pill-premium {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  border-radius: 99px;
  font-size: 13px;
  font-weight: 700;
  background: color-mix(in srgb, var(--c), white 92%);
  color: var(--c);
  border: 1px solid color-mix(in srgb, var(--c), white 85%);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
}

.status-text-premium {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Action Buttons */
.action-btn-premium {
  border-radius: 10px;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: none;
  box-shadow: none;
}

.action-btn-premium:hover {
  filter: brightness(0.96);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.bg-error-soft {
  background-color: #fff1f2 !important;
}

.text-error {
  color: #e11d48 !important;
}

.bg-success-soft {
  background-color: #ecfdf5 !important;
}

.text-success {
  color: #059669 !important;
}

.divider-vertical {
  width: 1px;
  height: 24px;
  background: #cbd5e1;
  opacity: 0.5;
}

.text-slate-500 {
  color: #64748b !important;
}

/* Utilities */
.gap-1 {
  gap: 4px;
}

.gap-2 {
  gap: 8px;
}

.gap-3 {
  gap: 12px;
}

.gap-4 {
  gap: 16px;
}

.min-w-0 {
  min-width: 0;
}

@media (max-width: 600px) {
  .header-actions {
    width: 100%;
    margin-top: 16px;
    /* Slightly more space */
    padding-top: 16px;
    border-top: 1px dashed #e2e8f0;
    /* Dashed line for mobile separation */
  }

  /* Expand buttons container */
  .action-buttons {
    width: 100%;
    display: flex;
    gap: 12px;
  }

  /* Make buttons full width */
  .action-buttons .v-btn {
    flex: 1;
    min-width: 0;
    height: 44px !important;
    /* Taller touch targets */
  }

  .back-btn-premium {
    width: 38px;
    height: 38px;
    margin-left: 12px !important;
  }

  .page-title {
    font-size: 1.15rem;
  }
}
</style>
