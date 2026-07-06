<template>
  <div class="official-info-grid">
    <div class="info-grid-row">
      <div v-for="(value, key) in items" :key="key" class="info-card-elite">
        <div class="info-card-inner">
          <div class="info-card-icon-wrapper">
            <div class="icon-blob"></div>
            <v-icon
              :icon="getIconForKey(key)"
              size="18"
              class="icon-elite"
            ></v-icon>
          </div>
          <div class="info-card-body">
            <span class="info-label">{{ translate ? $t(key) : key }}</span>
            <div class="info-value" :title="value">
              <template v-if="Array.isArray(value)">
                <v-chip class="me-2" v-for="item in value" :key="item" density="compact">
                  {{item}}
                </v-chip>
              </template>
              <template v-else>
                {{ value || "---" }}
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "InfoGrid",
  props: {
    items: {
      type: Object,
      required: true,
    },
    translate: { type: Boolean, default: false },
  },
  methods: {
    getIconForKey(key) {
      const iconMap = {
        // Order Info
        "رقم الطلب": "mdi-identifier",
        "تاريخ التقديم": "mdi-calendar-clock",
        "نوع الخدمة": "mdi-cog-outline",
        الأولوية: "mdi-alert-decagram-outline",
        الإصدار: "mdi-source-branch",
        المصدر: "mdi-web",
        "تاريخ البدء": "mdi-play-outline",
        "حالة الدفع": "mdi-cash-check",

        // Student/Audience Info
        "حالة الطالب": "mdi-account-card-outline",
        "المعدل التراكمي": "mdi-trending-up",
        "السنة الدراسية": "mdi-calendar-range",
        "التخصص الدقيق": "mdi-school-outline",
        الكلية: "mdi-domain",

        // Service Details
        "نوع التعديل المطلوب": "mdi-file-edit-outline",
        "الفصل الدراسي الحالي": "mdi-clock-time-eight-outline",
        "سبب طلب التعديل": "mdi-comment-question-outline",
        "التخصص السابق": "mdi-history",
        "التخصص الجديد المقترح": "mdi-star-outline",
        الملاحظات: "mdi-note-text-outline",
      };
      return iconMap[key] || "mdi-information-outline";
    },
  },
};
</script>

<style scoped>
.official-info-grid {
  width: 100%;
}

.info-grid-row {
  display: grid;
  /* flex-grow: 1; */
  grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
  gap: 16px;
}

.info-card-elite {
  position: relative;
  background: #ffffff;
  border-radius: 12px;
  padding: 14px 16px;
  border: 1px solid #f1f5f9;
  overflow: hidden;
  cursor: default;
}

/* .info-card-elite:hover {
  transform: translateY(-2px);
  border-color: #dbeafe;
  box-shadow: 0 8px 16px -6px rgba(59, 130, 246, 0.1);
} */

.info-card-inner {
  display: flex;
  align-items: center;
  position: relative;
  z-index: 2;
}

.info-card-icon-wrapper {
  position: relative;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 12px;
  flex-shrink: 0;
}

.icon-blob {
  position: absolute;
  inset: 0;
  background: #f8fafc;
  border-radius: 10px;
  transform: rotate(-2deg);
  transition: all 0.3s ease;
}

.info-card-elite:hover .icon-blob {
  background: #eff6ff;
  transform: rotate(4deg) scale(1.05);
}

.icon-elite {
  color: #64748b;
  z-index: 1;
  transition: all 0.3s ease;
}

.info-card-elite:hover .icon-elite {
  color: #3b82f6;
}

.info-card-body {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.info-label {
  font-size: 10px;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-bottom: 2px;
}

.info-value {
  font-size: 13px;
  font-weight: 800;
  color: #1e293b;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: all 0.3s ease;
}

.info-card-elite:hover .info-value {
  color: #0f172a;
}

@media (max-width: 600px) {
  .info-grid-row {
    grid-template-columns: repeat(auto-fill, minmax(100%, 1fr));
    gap: 12px;
  }

  .info-card-elite {
    padding: 12px 14px;
  }
}

@media (min-width: 601px) and (max-width: 960px) {
  .info-grid-row {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  }
}
</style>
