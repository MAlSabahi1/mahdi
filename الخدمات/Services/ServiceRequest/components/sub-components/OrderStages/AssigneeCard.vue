<template>
  <div class="executive-execution-node rounded-2xl overflow-hidden">
    <!-- Ledger Header -->
    <div class="portal-header pa-4 pa-md-6 border-bottom-matrix bg-white">
      <div class="d-flex align-center justify-space-between">
        <div class="d-flex align-center ga-3 ga-md-4">
          <div class="portal-icon-box d-none d-sm-flex">
            <v-icon icon="mdi-history" color="primary" size="24"></v-icon>
          </div>
          <div class="portal-title-logic">
            <h3 class="portal-h3">سجل تنفيذ المرحلة</h3>
            <div class="portal-sub">تتبع الأنشطة والمخرجات الزمنية</div>
          </div>
        </div>
        <div class="entry-count-badge">
          {{ selectedStage?.action_logs?.length || 0 }} <span class="d-none d-sm-inline">عمليات</span>
        </div>
      </div>
    </div>

    <!-- Active Assignee Rail -->
    <div v-if="selectedStage?.stage_assignee_name"
      class="status-context-rail pa-3 pa-md-4 bg-slate-50/50 border-bottom-matrix d-flex align-center">
      <div class="avatar-halo ml-2 ml-md-3">
        <v-avatar color="white" size="28" size-md="32" class="elevation-1">
          <v-icon color="primary" size="16">mdi-account-check-outline</v-icon>
        </v-avatar>
      </div>
      <div class="flex-grow-1">
        <div class="rail-label">المسؤول عن التنفيذ:</div>
        <div class="text-caption text-sm-subtitle-2 font-weight-black text-slate-800">{{
          selectedStage?.stage_assignee_name }}</div>
      </div>
      <v-chip size="x-small" color="success" variant="tonal"
        class="rounded-lg px-2 px-sm-3 font-weight-black d-none d-sm-inline-flex">على رأس العمل</v-chip>
    </div>

    <!-- Timeline Body -->
    <div class="portal-body pa-4 pa-md-6 bg-white overflow-auto scroll-premium" style="max-height: 400px">
      <div v-if="actionResponsibilities?.length" class="execution-deployment-stack pr-1 pr-sm-2">
        <div v-for="(log, idx) in actionResponsibilities" :key="idx" class="history-step">
          <div class="step-line-container">
            <!-- <div :class="['step-dot', log.action_type]"></div>
            <div v-if="idx < selectedStage.action_logs.length - 1" class="step-connector"></div> -->
            <div class="step-dot" :class="[log.action]" :style="{ backgroundColor: log.colof, borderColor: log.color }">
              <v-icon :icon="log.icon" size="10" color="white" style="position: absolute;top:50%;left:50%;transform: transform: translate(-50%, -50%);" />
              <div v-if="idx < actionResponsibilities.length - 1" class="step-connector"></div>
            </div>
          </div>

          <div class="step-content pb-4 pb-md-6">
            <div class="d-flex align-center justify-space-between mb-1">
              <span class="step-action-name font-weight-black">{{ log.display_name }}</span>
              <span class="step-timestamp" dir="ltr">{{ $moment(log.time).format("hh:mm A") }}</span>
            </div>
            <div class="step-meta">
              <span class="d-none d-sm-inline">بواسطة: </span><span class="text-primary">{{ log.user
              }}</span>
              <v-icon icon="mdi-circle-small" size="14"></v-icon>
              {{ $moment(log.time).format("YYYY/MM/DD") }}
            </div>
          </div>
        </div>
      </div>

      <!-- Empty Architecture -->
      <div v-else class="empty-trace py-16 text-center">
        <v-icon icon="mdi-tray-full" size="48" color="slate-100" class="mb-4"></v-icon>
        <h4 class="portal-h3 text-slate-300">لا توجد سجلات تنفيذ</h4>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AssigneeCard",
  emits: ["chat"],
  props: {
    selectedStage: { type: Object, default: null },
  },
  data() {
    return {};
  },

  computed: {
    actionResponsibilities() {
      return [
        {
          user: `${this.selectedStage["fk_started_by__first_name"]} ${this.selectedStage["fk_started_by__last_name"]}`,
          role: this.selectedStage["fk_started_username"],
          img: this.selectedStage["fk_started__image_user"],
          time: this.selectedStage["start_time"],
          action: "started",
          display_name: "بدء المرحلة",
          icon: "mdi-play",
          color: "#10b981",
        },
        {
          user: `${this.selectedStage["fk_completed_by__first_name"]} ${this.selectedStage["fk_completed_by__last_name"]}`,
          role: this.selectedStage["fk_completed_by__username"],
          img: this.selectedStage["fk_completed__image_user"],
          time: this.selectedStage["completed_at"],
          action: "completed",
          display_name: "إتمام المرحلة",
          icon: "mdi-check-all",
          color: "#2563eb",
        },
        {
          user: `${this.selectedStage["fk_approved_by__first_name"]} ${this.selectedStage["fk_approved_by__last_name"]}`,
          role: this.selectedStage["fk_approved_by__username"],
          img: this.selectedStage["fk_approved_by__image_user"],
          time: this.selectedStage["approved_at"],
          action: "approve",
          display_name: "اعتماد المرحلة",
          icon: "mdi-check-decagram",
          color: "#3b82f6",
        },
        {
          user: `${this.selectedStage["fk_executed_by__first_name"]} ${this.selectedStage["fk_executed_by__last_name"]}`,
          role: this.selectedStage["fk_executed_by__username"],
          img: this.selectedStage["fk_executed__image_user"],
          time: this.selectedStage["executed_at"],
          action: "executed",
          display_name: "تنفيذ المهام",
          icon: "mdi-cog-play-outline",
          color: "#f97316",
        },
        {
          user: `${this.selectedStage["fk_moved_to_next_by__first_name"]} ${this.selectedStage["fk_moved_to_next_by__last_name"]}`,
          role: this.selectedStage["fk_moved_to_next_by__username"],
          img: this.selectedStage["fk_moved_to_next_by__image_user"],
          time: this.selectedStage["moved_to_next_at"],
          action: "moved_to_next",
          display_name: "تحويل للمرحلة التالية",
          icon: "mdi-arrow-right-circle",
          color: "#9333ea",
        },
        {
          user: `${this.selectedStage["fk_returned_by__first_name"]} ${this.selectedStage["fk_returned_by__last_name"]}`,
          role: this.selectedStage["fk_returned_by__username"],
          img: this.selectedStage["fk_returned_by__image_user"],
          time: this.selectedStage["returned_at"],
          action: "returned",
          display_name: "إعادة المرحلة",
          icon: "mdi-keyboard-return",
          color: "#f59e0b",
        },
        {
          user: `${this.selectedStage["fk_rejected_by__first_name"]} ${this.selectedStage["fk_rejected_by__last_name"]}`,
          role: this.selectedStage["fk_rejected_by__username"],
          img: this.selectedStage["fk_rejected_by__image_user"],
          time: this.selectedStage["rejected_at"],
          action: "rejected",
          display_name: "رفض المرحلة",
          icon: "mdi-close-circle-outline",
          color: "#ef4444",
        },
      ]?.filter((r) => r?.role && r?.time).sort((a,b) => new Date(a.time) - new Date(b.time))
    },
  },
  methods: {},
};
</script>

<style scoped>
.executive-execution-node {
  font-family: 'Almarai', 'Noto Sans Arabic', sans-serif;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  position: relative;
}

.executive-execution-node::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, #94a3b8, #cbd5e1);
  z-index: 10;
}

.portal-header {
  background: #ffffff;
}

.portal-icon-box {
  width: 48px;
  height: 48px;
  background: #f1f5f9;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e2e8f0;
}

.portal-h3 {
  font-size: 1.1rem;
  font-weight: 900;
  color: #0f172a;
  margin-bottom: 2px;
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

  .portal-icon-box {
    width: 36px;
    height: 36px;
    border-radius: 10px;
  }
}

.entry-count-badge {
  padding: 4px 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 800;
  color: #64748b;
}

.status-context-rail {
  background: #f8fafc;
}

.rail-label {
  font-size: 10px;
  font-weight: 800;
  color: #94a3b8;
  margin-bottom: 2px;
}

.history-step {
  display: flex;
  gap: 10px;
}

@media (min-width: 600px) {
  .history-step {
    gap: 16px;
  }
}

.step-line-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 10px;
}

.step-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #cbd5e1;
  border: 1.5px solid white;
  box-shadow: 0 0 0 3px #f8fafc;
  flex-shrink: 0;
  margin-top: 6px;
}

@media (min-width: 600px) {
  .step-dot {
    width: 10px;
    height: 10px;
    border: 2px solid white;
    box-shadow: 0 0 0 4px #f8fafc;
  }
}

.step-dot.complete,
.step-dot.approve {
  background: #10b981;
}

.step-dot.reject {
  background: #ef4444;
}

.step-dot.return {
  background: #f59e0b;
}

.step-connector {
  width: 2px;
  flex-grow: 1;
  background: #f1f5f9;
  margin: 4px 0;
}

.step-content {
  flex-grow: 1;
}

.step-action-name {
  font-size: 12.5px;
  color: #1e293b;
}

.step-timestamp {
  font-size: 10px;
  font-weight: 700;
  color: #94a3b8;
}

.step-meta {
  font-size: 10px;
  font-weight: 700;
  color: #94a3b8;
}

@media (min-width: 600px) {
  .step-action-name {
    font-size: 13px;
  }

  .step-timestamp {
    font-size: 11px;
  }

  .step-meta {
    font-size: 11px;
  }
}

.border-bottom-matrix {
  border-bottom: 1px solid #f1f5f9;
}

.scroll-premium::-webkit-scrollbar {
  width: 4px;
}

.scroll-premium::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 10px;
}
</style>
