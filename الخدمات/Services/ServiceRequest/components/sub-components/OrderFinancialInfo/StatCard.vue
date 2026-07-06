<template>
  <v-card class="premium-stat-card" :style="{ '--accent': hexColor }">
    <!-- Decorative Background Pattern -->
    <div class="card-pattern"></div>
    
    <div class="pa-6 pa-md-7 h-100 d-flex flex-column relative-content">
      <!-- Top Section: Icon & Status -->
      <div class="d-flex align-center justify-space-between mb-6">
        <div class="premium-icon-box">
          <v-icon :icon="icon" size="30" :color="color" class="icon-anim"></v-icon>
        </div>
        <div class="d-flex flex-column align-end ga-1">
          <div v-if="statusLabel" class="premium-status-badge" :style="{backgroundColor: statusColor + '15', color: statusColor}">
            <span class="status-dot" :style="{backgroundColor: statusColor}"></span>
            {{ statusLabel }}
          </div>
          <div v-if="trend" class="premium-trend-text">
            {{ trend }}
          </div>
        </div>
      </div>

      <!-- Middle Section: Value & Label -->
      <div class="premium-stat-body">
        <div class="premium-stat-label mb-1">{{ title }}</div>
        <div class="d-flex align-baseline flex-wrap">
          <span class="premium-stat-value">{{ formatValue(value) }}</span>
          <span class="premium-stat-currency mr-2">{{ currency }}</span>
        </div>
      </div>

      <!-- Bottom Section: Progress -->
      <div v-if="showProgress" class="mt-auto pt-6">
        <div class="d-flex justify-space-between align-center mb-2">
          <span class="premium-progress-label">{{ progressLabel }}</span>
          <span class="premium-progress-percent font-weight-black">{{ progressValue }}%</span>
        </div>
        <div class="premium-progress-track">
          <div 
            class="premium-progress-fill" 
            :style="{ width: progressValue + '%', backgroundColor: hexColor }"
          >
            <div class="progress-shine"></div>
          </div>
        </div>
      </div>
      
      <!-- Subtle Hover Line -->
      <div class="hover-indicator" :style="{ backgroundColor: hexColor }"></div>
    </div>
  </v-card>
</template>

<script>
export default {
  name: "StatCard",
  props: {
    title: { type: String, required: true },
    value: { type: [Number, String], required: true },
    currency: { type: String, default: "ر.س" },
    icon: { type: String, required: true },
    color: { type: String, default: "primary" },
    hexColor: { type: String, default: "#2563eb" },
    trend: { type: String, default: "" },
    showProgress: { type: Boolean, default: false },
    progressValue: { type: Number, default: 0 },
    progressLabel: { type: String, default: "النسبة" },
    statusLabel: { type: String, default: "" },
    statusColor: { type: String, default: "" },
  },
  methods: {
    formatValue(val) {
      if (typeof val === "number") {
        return new Intl.NumberFormat("ar-SA").format(val);
      }
      return val;
    },
  },
};
</script>

<style scoped>
.premium-stat-card {
  background: #ffffff !important;
  border-radius: 24px !important;
  border: 1px solid #e2e8f0 !important;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.premium-stat-card:hover {
  border-color: var(--accent) !important;
}

.relative-content {
  position: relative;
  z-index: 1;
}

.premium-icon-box {
  width: 56px;
  height: 56px;
  background-color: #f8fafc;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #f1f5f9;
  transition: all 0.3s ease;
}

.premium-stat-card:hover .premium-icon-box {
  background-color: #ffffff;
  border-color: var(--accent);
  transform: scale(1.05) rotate(5deg);
}

.icon-anim {
  transition: transform 0.4s ease;
}

.premium-status-badge {
  padding: 4px 12px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 800;
  display: flex;
  align-items: center;
  white-space: nowrap;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-left: 8px;
}

.premium-trend-text {
  font-size: 11px;
  font-weight: 700;
  color: #94a3b8;
}

.premium-stat-label {
  font-size: 14px;
  font-weight: 800;
  color: #64748b;
}

.premium-stat-value {
  font-size: 2.25rem;
  font-weight: 900;
  color: #0f172a;
  line-height: 1;
  letter-spacing: -0.02em;
}

.premium-stat-currency {
  font-size: 1rem;
  font-weight: 700;
  color: #94a3b8;
}

.premium-progress-label {
  font-size: 12px;
  font-weight: 700;
  color: #64748b;
}

.premium-progress-track {
  height: 8px;
  background-color: #f1f5f9;
  border-radius: 10px;
  overflow: hidden;
  position: relative;
}

.premium-progress-fill {
  height: 100%;
  border-radius: 10px;
  position: relative;
}



.hover-indicator {
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 3px;
  border-radius: 3px 3px 0 0;
  transition: all 0.2s ease;
  transform: translateX(-50%);
}

.premium-stat-card:hover .hover-indicator {
  width: 40%;
}

.ga-1 { gap: 4px; }

@media (max-width: 600px) {
  .premium-stat-value { font-size: 1.75rem; }
  .premium-stat-label { font-size: 13px; }
  .premium-icon-box { width: 44px; height: 44px; border-radius: 12px; }
  .premium-icon-box :deep(.v-icon) { font-size: 24px !important; }
  .pa-6 { padding: 20px !important; }
}
</style>
