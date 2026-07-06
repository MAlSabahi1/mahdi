<template>
  <div class="stage-banner-premium">
    <div class="banner-glass pa-3 pa-md-6">
      <div class="d-flex align-center justify-space-between flex-nowrap ga-3 ga-md-4">
        <div class="flex-grow-1 overflow-hidden">
          <!-- Status & Meta Row -->
          <div class="d-flex align-center flex-wrap ga-1 ga-md-2 mb-2 mb-md-3">
            <div :class="['executive-badge', selectedStage?.stage_status]">
              <div class="badge-dot"></div>
              <span class="text-tiny">{{ selectedStage?.stage_status__display }}</span>
            </div>

            <div class="meta-capsule-glass d-none d-sm-inline-flex">
              <v-icon icon="mdi-fingerprint" size="10" class="ml-1 opacity-50"></v-icon>
              <span>ID: {{ selectedStage?.fk_request__request_number }}</span>
            </div>
          </div>

          <!-- Main Identity -->
          <h1 class="executive-title text-truncate mb-1">
            {{ selectedStage?.fk_workflow_step__fk_stage__name_ar }}
          </h1>

          <p class="executive-subtitle text-truncate d-none d-md-block mb-0">
            {{ selectedStage?.fk_workflow_step__fk_stage__description_ar || `نظام ذكي لمتابعة وإدارة سير العمل التنفيذي
            في هذه المرحلة.` }}
          </p>
        </div>

        <!-- Kinetic Indicator -->
        <div class="kinetic-wrapper d-flex justify-center align-center flex-shrink-0 ml-1">
          <div class="kinetic-status" :class="selectedStage?.stage_status">
            <div class="kinetic-core">
              <v-icon :icon="getStatusIcon(selectedStage?.stage_status)" size="18" size-md="24"></v-icon>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "StageHeader",
  props: {
    selectedStage: { type: Object, default: {} },
  },
  methods: {
    getStatusColor(status) {
      const map = {
        completed: "success",
        pending: "primary",
        rejected: "slate-400",
        cancelled: "error",
        returned: "info",
      };
      return map[status] || "grey";
    },
    getStatusText(status) {
      const map = {
        completed: "مكتملة بنجاح",
        current: "قيد المعالجة",
        pending: "بانتظار الدور",
      };
      return map[status] || "غير معروف";
    },
    getStatusIcon(status) {
      const map = {
        completed: "mdi-check-decagram",
        pending: "mdi-lightning-bolt",
        rejected: "mdi-cancel",
        cancelled: "mdi-close-circle",
        returned: "mdi-information",
      };
      return map[status] || "mdi-help-circle";
    },
  },
};
</script>


<style scoped>
.stage-banner-premium {
  font-family: 'Almarai', sans-serif;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 24px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
}

.banner-glass {
  background:
    radial-gradient(circle at top right, rgba(var(--v-theme-primary), 0.08), transparent 40%),
    radial-gradient(circle at bottom left, rgba(var(--v-theme-primary), 0.03), transparent 40%);
  position: relative;
  z-index: 2;
}

/* Executive Badges */
.executive-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 100px;
  font-size: 10.5px;
  font-weight: 800;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  margin-left: 8px;
  background: white;
  box-shadow: 0 0 10px white;
}

.executive-badge.completed {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.executive-badge.completed .badge-dot {
  background: #34d399;
  box-shadow: 0 0 10px #34d399;
}

.executive-badge.in_progress,
.executive-badge.pending {
  background: rgba(37, 99, 235, 0.15);
  color: #60a5fa;
}

.executive-badge.in_progress .badge-dot {
  background: #60a5fa;
  box-shadow: 0 0 10px #60a5fa;
}

.meta-capsule-glass {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  background: #f1f5f9;
  border-radius: 10px;
  font-size: 10px;
  font-weight: 700;
  color: #64748b;
}

/* Typography */
.executive-title {
  color: #1e293b;
  font-size: 22px;
  font-weight: 900;
  line-height: 1.2;
}

.executive-subtitle {
  color: #64748b;
  font-size: 13px;
  font-weight: 700;
  line-height: 1.5;
  max-width: 600px;
}

/* Kinetic Indicator */
.kinetic-status {
  width: 60px;
  height: 60px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (min-width: 960px) {
  .kinetic-status {
    width: 80px;
    height: 80px;
  }
}


.kinetic-core {
  width: 36px;
  height: 36px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgb(var(--v-theme-primary));
  z-index: 5;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

@media (min-width: 960px) {
  .kinetic-core {
    width: 48px;
    height: 48px;
    border-radius: 14px;
  }
}

.kinetic-status.completed .kinetic-core {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.kinetic-status.rejected .kinetic-core {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

@media (max-width: 960px) {
  .executive-title {
    font-size: 24px;
  }

  .executive-subtitle {
    font-size: 13px;
  }
}

@media (max-width: 600px) {
  .banner-glass {
    padding: 16px 12px !important;
  }

  .executive-title {
    font-size: 16px;
  }

  .kinetic-status {
    width: 50px;
    height: 50px;
  }

  .kinetic-core {
    width: 32px;
    height: 32px;
  }
}

.text-tiny {
  font-size: 9px !important;
}
</style>