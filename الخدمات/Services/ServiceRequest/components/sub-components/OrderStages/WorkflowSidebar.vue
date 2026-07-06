<template>
  <v-col cols="12" md="4" lg="3" class="workflow-sidebar-modern">
    <!-- Sidebar Header: Elite Command Block -->
    <div class="sidebar-header-sovereign pa-4 pa-lg-5 border-bottom-matrix">
      <div class="d-flex align-center mb-2 mb-sm-5 d-none d-sm-flex">
        <div class="brand-shell-prime ml-4">
          <v-icon :icon="icon" color="primary" size="20"></v-icon>
          <div class="shell-halo"></div>
        </div>
        <div class="brand-logic-stack">
          <h3 class="sovereign-title text-truncate" style="max-width: 200px">{{ title }}</h3>
          <div class="sovereign-meta">{{ subtitle }}</div>
        </div>
      </div>

      <!-- Ultra-Premium Progress Engine -->
      <div class="progress-engine-chamber pa-4 rounded-xl">
        <div class="d-flex justify-space-between align-center mb-3">
          <span class="engine-label">اكتمال المسار الإداري</span>
          <div class="engine-percent-pill px-3 py-0.5 rounded-pill">
            <span class="engine-percent">{{ Math.min(progress, 100) }}%</span>
          </div>
        </div>
        <div class="premium-track-blueprint">
          <div class="premium-fill-blueprint" :style="{ width: Math.min(progress, 100) + '%' }">
            <div class="luminous-sweep"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigational Architecture -->
    <div class="sidebar-nav-blueprint pa-4 pa-lg-5">
      <div v-for="(stage, index) in stages" :key="stage.id" class="workflow-node-elite" :class="{
        'is-active': selectedId === stage.id,
        'is-completed': stage.stage_status === 'completed',
        'is-current': stage.is_current,
        'is-returned': stage.stage_status === 'returned',
        'is-rejected': stage.stage_status === 'rejected',
      }" @click="$emit('select', stage)">

        <div class="node-architecture-elite">
          <div class="node-visual-elite">
            <v-icon v-if="stage.stage_status === 'completed'" icon="mdi-shield-check" size="16"></v-icon>
            <v-icon v-else-if="stage.stage_status === 'returned'" icon="mdi-alert-circle-outline" size="16"></v-icon>
            <v-icon v-else-if="stage.stage_status === 'rejected'" icon="mdi-close-octagon-outline" size="16"></v-icon>
            <span v-else>{{ (index + 1).toString().padStart(2, '0') }}</span>
          </div>
          <div v-if="index < stages.length - 1" class="tactical-connector"></div>
        </div>

        <div class="node-content-logic">
          <div class="node-title-main">{{ stage.fk_workflow_step__fk_stage__name_ar }}</div>
          <div class="node-status-badge">
            <span class="status-indicator-dot"></span>
            {{ stage.stage_status__display }}
          </div>
        </div>

        <div class="active-node-ribbon"></div>
      </div>
    </div>
  </v-col>
</template>

<script>
export default {
  name: "WorkflowSidebar",
  props: {
    stages: { type: Array, required: true },
    selectedId: { type: [Number, String], required: true },
    // progress: { type: Number, default: 0 },
    title: { type: String, default: "مركز التحكم" },
    subtitle: { type: String, default: "نظام تتبع المسار الذكي" },
    icon: { type: String, default: "mdi-shield-check" },
  },
  emits: ["select"],
  computed: {
    progress() {
      const completed = this.stages?.filter(
        (s) => s?.stage_status == "completed"
      )?.length;
      return this.stages?.length
        ? Math?.round((completed / this.stages?.length) * 100)
        : 0;
    },
  },
  methods: {
    // getStatusText(status) {
    //   const map = {
    //     completed: "مكتملة بنجاح",
    //     current: "قيد المعالجة",
    //     pending: "بانتظار الدور",
    //     rejected: "مرفوض",
    //     returned: "مرجع للتعديل",
    //   };
    //   return map[status] || "غير معروف";
    // },
    // getStatusIcon(status) {
    //   const map = {
    //     completed: "mdi-check-decagram",
    //     current: "mdi-lightning-bolt",
    //     pending: "mdi-clock-outline",
    //     rejected: "mdi-close-circle",
    //     returned: "mdi-keyboard-return",
    //   };
    //   return map[status] || "mdi-help-circle";
    // },
  },
};
</script>


<style scoped>
.workflow-sidebar-modern {
  background: #ffffff;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #f1f5f9;
  position: relative;
  z-index: 1;
  font-family: 'Almarai', 'Noto Sans Arabic', sans-serif;
}

/* 1. Elite Command Block Header */
.sidebar-header-sovereign {
  background:
    radial-gradient(at 0% 0%, rgba(var(--v-theme-primary), 0.05) 0, transparent 50%),
    linear-gradient(180deg, #ffffff 0%, #fcfdfe 100%);
}

.brand-shell-prime {
  width: 42px;
  height: 42px;
  background: white;
  border: 1px solid rgba(var(--v-theme-primary), 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.05),
    0 10px 15px -3px rgba(var(--v-theme-primary), 0.1);
}

.shell-halo {
  position: absolute;
  inset: -2px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.2), transparent);
  opacity: 0.5;
  z-index: -1;
}

.sovereign-title {
  font-size: 1rem;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -0.015em;
  margin-bottom: 0px;
}

.sovereign-meta {
  font-size: 9px;
  font-weight: 800;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

@media (max-width: 600px) {
  .sovereign-title {
    font-size: 0.9rem;
  }

  .progress-engine-chamber {
    padding: 8px !important;
  }

  .engine-label {
    font-size: 10px;
  }
}

/* 2. Progress Engine Chamber */
.progress-engine-chamber {
  background: white;
  border: 1px solid #f1f5f9;
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.02),
    0 10px 20px -5px rgba(0, 0, 0, 0.03);
}

.engine-label {
  font-size: 11px;
  font-weight: 850;
  color: #475569;
}

.engine-percent-pill {
  background: rgba(var(--v-theme-primary), 0.06);
  border: 1px solid rgba(var(--v-theme-primary), 0.1);
}

.engine-percent {
  font-size: 11px;
  font-weight: 900;
  color: rgb(var(--v-theme-primary));
}

.premium-track-blueprint {
  height: 6px;
  background: #f1f5f9;
  border-radius: 100px;
  overflow: hidden;
  position: relative;
}

.premium-fill-blueprint {
  height: 100%;
  background: linear-gradient(90deg, rgb(var(--v-theme-primary)), #3b82f6);
  border-radius: 100px;
  position: relative;
}

.luminous-sweep {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 60px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
}

@keyframes hyper-sweep {
  0% {
    transform: translateX(-100%);
  }

  100% {
    transform: translateX(400%);
  }
}

/* 3. Navigational Architecture */
.sidebar-nav-blueprint {
  flex-grow: 1;
  overflow-y: auto;
}

.sidebar-nav-blueprint::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav-blueprint::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 10px;
}

.workflow-node-elite {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  margin-bottom: 4px;
  border-radius: 14px;
  cursor: pointer;
  position: relative;
  border: 1px solid transparent;
}

.workflow-node-elite:hover {
  background: #f8fafc;
}

.workflow-master-frame {
  min-height: 85vh;
  background: #ffffff;
}

.workflow-main-row {
  height: 100%;
}

.workflow-node-elite.is-active {
  background: white;
  border-color: #f1f5f9;
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.02),
    0 10px 15px -3px rgba(0, 0, 0, 0.04);
}

.active-node-ribbon {
  position: absolute;
  right: 0;
  top: 14px;
  bottom: 14px;
  width: 4px;
  background: rgb(var(--v-theme-primary));
  border-radius: 100px 0 0 100px;
  transform: scaleY(0);
}

.workflow-node-elite.is-active .active-node-ribbon {
  transform: scaleY(1);
}

.node-architecture-elite {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: 20px;
  flex-shrink: 0;
  z-index: 2;
}

.node-visual-elite {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: white;
  border: 2px solid #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 900;
  color: #94a3b8;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.tactical-connector {
  width: 1.5px;
  height: 32px;
  background: #f1f5f9;
  margin-top: 4px;
  position: absolute;
  top: 34px;
  z-index: 1;
}

.is-completed .node-visual-elite {
  background: #f0fdf4;
  border-color: #dcfce7;
  color: #10b981;
}

.is-completed .tactical-connector {
  background: linear-gradient(180deg, #10b981 0%, #f1f5f9 100%);
  opacity: 0.3;
}

.is-returned .node-visual-elite {
  border-color: #fde68a;
  color: #d97706;
  background: #fffbeb;
}

.is-rejected .node-visual-elite {
  border-color: #fecaca;
  color: #dc2626;
  background: #fef2f2;
}

.workflow-node-elite.is-active .node-visual-elite {
  background: rgb(var(--v-theme-primary));
  color: white;
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 8px 20px rgba(var(--v-theme-primary), 0.25);
  transform: scale(1.05);
}

.is-current .node-visual-elite::before {
  content: '';
  position: absolute;
  inset: -5px;
  border-radius: 14px;
  border: 1px solid rgb(var(--v-theme-primary));
  opacity: 0.5;
}

@keyframes sovereign-ping {
  0% {
    transform: scale(1);
    opacity: 0.6;
  }

  100% {
    transform: scale(1.3);
    opacity: 0;
  }
}

.node-content-logic {
  flex-grow: 1;
}

.node-title-main {
  font-size: 13.5px;
  font-weight: 900;
  color: #334155;
  line-height: 1.4;
  letter-spacing: -0.01em;
  transition: color 0.3s ease;
}

.workflow-node-elite.is-active .node-title-main {
  color: #0f172a;
}

.node-status-badge {
  font-size: 10.5px;
  font-weight: 850;
  color: #94a3b8;
  margin-top: 2px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-indicator-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #cbd5e1;
}

.is-active .status-indicator-dot {
  background: rgb(var(--v-theme-primary));
}

.is-completed .status-indicator-dot {
  background: #10b981;
}

.is-returned .status-indicator-dot {
  background: #f59e0b;
}

.is-rejected .status-indicator-dot {
  background: #ef4444;
}

.border-bottom-matrix {
  border-bottom: 1px solid #f1f5f9;
}

/* 4. Responsive Architecture */
@media (max-width: 960px) {
  .workflow-sidebar-modern {
    border-left: none;
    border-bottom: 2px solid #f1f5f9;
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: hidden;
  }

  .sidebar-header-sovereign {
    padding: 10px !important;
  }

  .progress-engine-chamber {
    padding: 6px !important;
    border-radius: 8px !important;
    box-shadow: none !important;
    border: 1px dashed rgba(var(--v-theme-primary), 0.1) !important;
  }

  .engine-label,
  .engine-percent-pill {
    display: none !important;
  }

  .premium-track-blueprint {
    height: 4px;
    margin-bottom: 0px !important;
  }

  .sidebar-nav-blueprint {
    display: flex;
    padding: 16px 20px !important;
    gap: 16px;
    overflow-x: auto;
    scrollbar-width: none;
    scroll-snap-type: x mandatory;
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
  }

  /* Hide scrollbar for Chrome/Safari */
  .sidebar-nav-blueprint::-webkit-scrollbar {
    display: none;
  }

  .workflow-node-elite {
    flex-shrink: 0;
    margin-bottom: 0;
    padding: 16px 20px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    min-width: calc(100vw - 60px);
    /* calculated for "Single Option" focus */
    scroll-snap-align: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    display: flex;
    align-items: center;
    justify-content: flex-start;
  }

  .workflow-node-elite.is-active {
    border-color: rgb(var(--v-theme-primary));
    background: #f0f9ff;
    box-shadow: 0 8px 20px rgba(var(--v-theme-primary), 0.1);
  }

  .node-title-main {
    font-size: 14px;
    font-weight: 800;
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
    max-width: 100%;
    margin-top: 2px;
  }

  .node-architecture-elite {
    margin-left: 16px;
  }

  .node-visual-elite {
    width: 40px;
    height: 40px;
    font-size: 12px;
    border-width: 2px;
  }

  .node-status-badge {
    font-size: 11px;
    margin-top: 4px;
  }

  /* Visual Connector for Carousel context */
  .tactical-connector {
    display: none;
  }

  .active-node-ribbon {
    display: none;
  }
}
</style>
