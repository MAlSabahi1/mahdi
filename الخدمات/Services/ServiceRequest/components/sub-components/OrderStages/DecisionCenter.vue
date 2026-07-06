<template>
  <div class="executive-command-node rounded-2xl overflow-hidden mb-6">
    <!-- Header Section -->
    <div class="command-header pa-4 pa-md-6 border-bottom-matrix bg-white">
      <div class="d-flex align-center justify-space-between">
        <div class="d-flex align-center ga-3 ga-md-4">
          <div class="command-icon-box d-none d-sm-flex">
            <v-icon icon="mdi-shield-crown-outline" color="primary" size="22"></v-icon>
          </div>
          <div class="command-title-logic">
            <h3 class="portal-h3">{{ title }}</h3>
            <div class="portal-sub">نظام اتخاذ القرار السيادي</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Documentation Rail (Current Stage Status) -->
    <div
      class="status-context-rail pa-3 pa-md-4 bg-slate-50/50 border-bottom-matrix d-flex align-center justify-space-between">
      <div class="d-flex align-center ga-2">
        <span class="rail-label">الحالة:</span>
        <div class="status-chip active text-truncate" style="max-width: 150px">{{ selectedStage?.title }}</div>
      </div>
      <v-avatar size="24" color="white" class="elevation-1">
        <v-icon icon="mdi-account-tie" size="14" color="primary"></v-icon>
      </v-avatar>
    </div>

    <div class="command-body pa-4 pa-md-6 bg-white">
      <!-- Action Matrix -->
      <div class="actions-grid d-flex flex-column ga-2 ga-md-3">
        <template v-for="action in actions" :key="action.type">
          <v-btn v-if="checkStagesActionPermission(action?.type)" block flat :height="action.height || '46'"
            :class="['command-btn-elite', action.type, { 'is-primary-hero': action.type === 'complete' || action.type === 'approve' }]"
            @click="startAction(action?.type)">
            <v-icon :icon="action.icon" size="18" class="ml-2 ml-md-3"></v-icon>
            <span class="font-weight-black">{{ action.label }}</span>
          </v-btn>
        </template>
      </div>
    </div>
  </div>

  <!-- Dialogs -->
  <BaseDialog v-model="dialog.show" :title="dialog?.type == 'return' ? 'إرجاع الطلب للتعديل' : 'رفض الطلب نهائياً'"
    :loading="dialog?.loading" @confirm="doActionStage(dialog?.type, dialog)">
    <template #fields>
      <custom-text-field
          v-if="dialog?.type == 'return'"
          v-model="dialog.return_reason"
          icon="pen-outline"
          label="سبب الإرجاع"
          :hideDetails="auto"
          placeholder="أدخل عنواناً موجزاً لسبب الإرجاع..."
          :rules="[$required, $max_value(100)]"
          class="mb-4"
        />
        <custom-text-note
          hide-details="auto"

          v-model="dialog[dialog?.type == 'return' ? 'return_reason_details' : 'reject_reason']"
          icon="note"
          :label="dialog?.type == 'return' ? 'تفاصيل سبب الإرجاع' : 'سبب الرفض'"
          placeholder="يرجى كتابة التفاصيل الكاملة للإجراء..."
          rows="5"
          :rules="[$required, $max_value(500)]"
        />
    </template>
  </BaseDialog>

  <BaseConfirm v-model="con_dia.show" v-bind="con_dia" :loading="loading?.con_btn"
    @confirm="doActionStage(con_dia?.action)"></BaseConfirm>
</template>

<script>
export default {
  name: "DecisionCenter",
  emits: ["action"],
  inject: [
    "checkStagesActionPermission",
    "getRequestDetails",
    "getStagesStatus",
  ],
  props: {
    title: { type: String, default: "مركز اتخاذ القرار" },
    selectedStage: { type: Object, default: {} },
    actions: {
      type: Array,
      default: () => [
        {
          type: "start",
          label: "بدء المرحلة",
          icon: "mdi-play-circle-outline",
          color: "success",
          class: "text-white mb-3 rounded-lg action-btn-modern",
          height: "60",
        },
        {
          type: "complete",
          label: "اكمال المرحلة",
          icon: "mdi-check-all",
          color: "primary",
          class: "text-white mb-3 rounded-lg action-btn-modern",
          height: "60",
        },
        {
          type: "execute",
          label: "تنفيذ",
          icon: "mdi-cog-play-outline",
          color: "warning",
          class: "text-white mb-3 rounded-lg action-btn-modern",
        },
        {
          type: "approve",
          label: "الموافقة",
          icon: "mdi-check-decagram",
          color: "white",
          class: "text-primary mb-3 rounded-lg action-btn-modern",
        },
        {
          type: "return",
          label: "إرجاع للتعديل",
          icon: "mdi-keyboard-return",
          color: "rgba(255,255,255,0.15)",
          variant: "flat",
          class: "text-white mb-3",
          height: 50,
        },
        {
          type: "reject",
          label: "رفض الطلب نهائياً",
          icon: "mdi-close-circle-outline",
          variant: "text",
          color: "rgba(255,255,255,0.6)",
          class: "",
          height: 40,
        },
        {
          type: "advance",
          label: "الانتقال للمرحلة التالية",
          icon: "mdi-arrow-right-circle",
          color: "purple",
          class: "text-white",
          height: 50,
        },
      ],
    },
  },
  data() {
    return {
      url_start: "d-services/request-actions/id/",
      loading: {},
      dialog: {},
      con_dia: {},
    };
  },

  methods: {
    openDialog(action) {
      this.dialog.show = true;
      this.dialog.type = action;
    },
    openConfirmDia(action) {
      switch (action) {
        case "start":
          this.con_dia = {
            title: "بدء المرحلة",
            message: "المتابعة في بدء المرحلة",
            type: "success",
            icon: this.actions?.find((a) => a?.type == action)?.icon,
          };
          break;
        case "complete":
          this.con_dia = {
            title: "إكمال المرحلة",
            message: "المتابعة في إكمال المرحلة",
            type: "primary",
            icon: this.actions?.find((a) => a?.type == action)?.icon,
          };
          break;
        case "execute":
          this.con_dia = {
            title: "تنفيذ المراحل",
            message: "المتابعة في تنفيذ المراحل",
            type: "warning",
            icon: this.actions?.find((a) => a?.type == action)?.icon,
          };
          break;
        case "approve":
          this.con_dia = {
            title: "الموافقة على المرحلة",
            message: "المتابعة في الموافقة على المرحلة",
            type: "info",
            icon: this.actions?.find((a) => a?.type == action)?.icon,
          };
          break;
        case "advance":
          this.con_dia = {
            title: "انتقال للمرحلة التالية",
            message: "المتابعة في الانتقال الى المرحلة",
            type: "info",
            icon: this.actions?.find((a) => a?.type == action)?.icon,
          };
          break;
      }

      this.con_dia.action = action;
      this.con_dia.show = true;
    },
    async startAction(action) {
      if (action) {
        switch (action) {
          case "return":
            this.openDialog(action);
            break;
          case "reject":
            this.openDialog(action);
            break;
          default:
            this.openConfirmDia(action);
            break;
        }
      }
    },
    async doActionStage(action, data) {
      try {
        this.loading.con_btn = true;
        this.dialog.loading = true;
        await this.$axios
          ?.post(
            this.url_start?.replace("id", this.selectedStage?.id) +
            `${action}/`,
            data ? { ...data } : undefined
          )
          .then((response) => {
            this.getRequestDetails();
            this.getStagesStatus();

            this.$snack("add", { message: response?.data?.message });
          });
      } catch (e) {
        console.log(e);
      } finally {
        this.loading.con_btn = false;
        this.dialog = {};
        this.con_dia = {};
      }
    },
  },
};
</script>


<style scoped>
.executive-command-node {
  font-family: 'Almarai', 'Noto Sans Arabic', sans-serif;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  position: relative;
}

.executive-command-node::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, rgb(var(--v-theme-primary)), rgba(var(--v-theme-primary), 0.6));
  z-index: 10;
}

.command-icon-box {
  width: 48px;
  height: 48px;
  background: #f1f5f9;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e2e8f0;
  position: relative;
}


.portal-h3 {
  font-size: 1.1rem;
  font-weight: 900;
  color: #0f172a;
}

.portal-sub {
  font-size: 9px;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
}

@media (max-width: 600px) {
  .portal-h3 {
    font-size: 0.95rem;
  }

  .command-icon-box {
    width: 36px;
    height: 36px;
    border-radius: 10px;
  }

  .status-chip.active {
    padding: 2px 8px;
    font-size: 10px;
  }
}

.status-context-rail {
  background: #f8fafc;
}

.rail-label {
  font-size: 11px;
  font-weight: 800;
  color: #64748b;
}

.status-chip.active {
  padding: 4px 12px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  color: #2563eb;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 800;
}

.command-btn-elite {
  text-transform: none !important;
  border-radius: 12px !important;
  border: 1px solid #e2e8f0 !important;
  background: #ffffff !important;
  color: #334155 !important;
  font-size: 13.5px !important;
  font-weight: 850 !important;
  letter-spacing: 0 !important;
  position: relative;
  overflow: hidden;
}

@media (max-width: 600px) {
  .command-btn-elite {
    font-size: 12.5px !important;
    height: auto !important;
    padding-top: 10px !important;
    padding-bottom: 10px !important;
  }
}

.command-btn-elite:hover {
  transform: translateX(-6px);
  border-color: #cbd5e1 !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
}

/* Operational States Logic */

/* 1. START Action */
.command-btn-elite.start {
  color: #059669 !important;
  background: #f0fdf4 !important;
  border-color: #bcf0da !important;
}

.command-btn-elite.start:hover {
  background: #dcfce7 !important;
  border-color: #86efac !important;
}

/* 2. COMPLETE / APPROVE (The Heroes) */
.command-btn-elite.complete,
.command-btn-elite.approve {
  background: rgb(var(--v-theme-primary)) !important;
  color: white !important;
  border: none !important;
  box-shadow: 0 8px 16px -4px rgba(var(--v-theme-primary), 0.3) !important;
}

.command-btn-elite.complete:hover,
.command-btn-elite.approve:hover {
  background: rgba(var(--v-theme-primary), 0.9) !important;
  box-shadow: 0 12px 24px -6px rgba(var(--v-theme-primary), 0.45) !important;
  transform: translateX(-6px) scale(1.01);
}

/* 3. EXECUTE (The Technical) */
.command-btn-elite.execute {
  color: #d97706 !important;
  background: #fffbeb !important;
  border-color: #fde68a !important;
}

.command-btn-elite.execute:hover {
  background: #fef3c7 !important;
  border-color: #fbbf24 !important;
}

/* 4. RETURN (The Revision) */
.command-btn-elite.return {
  color: #4f46e5 !important;
  background: #f5f3ff !important;
  border-color: #ddd6fe !important;
}

.command-btn-elite.return:hover {
  background: #ede9fe !important;
  border-color: #c4b5fd !important;
}

/* 5. REJECT (The Critical) */
.command-btn-elite.reject {
  color: #dc2626 !important;
  background: #fef2f2 !important;
  border: 1px dashed #fecaca !important;
}

.command-btn-elite.reject:hover {
  background: #fee2e2 !important;
  border-style: solid !important;
  border-color: #f87171 !important;
}

/* 6. ADVANCE (The Transition) */
.command-btn-elite.advance {
  border: 2px solid rgba(var(--v-theme-primary), 0.2) !important;
  color: rgb(var(--v-theme-primary)) !important;
}

.command-btn-elite.advance:hover {
  background: rgba(var(--v-theme-primary), 0.05) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
}

.border-bottom-matrix {
  border-bottom: 1px solid #f1f5f9;
}
</style>
