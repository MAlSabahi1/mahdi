<template>
  <v-card class="executive-node-card" :class="{ 'card-active': isHovered }" @mouseenter="isHovered = true"
    @mouseleave="isHovered = false" flat variant="outlined">
    <!-- Professional Identity Wire (Top Signature) -->
    <div class="identity-wire" :style="{ backgroundColor: fileConfig.color }"></div>

    <div class="pa-6 card-internal-grid">
      <!-- Section 1: Resource Signature & Menu -->
      <div class="d-flex justify-space-between align-start mb-5">
        <div class="icon-signature-box" :style="{ color: fileConfig.color, background: fileConfig.color + '0d' }">
          <v-icon :icon="fileConfig?.icon" size="22"></v-icon>
        </div>

        <!-- <v-menu v-if="is_view" location="bottom end" transition="fade-transition" offset="8">
          <template v-slot:activator="{ props: menuProps }">
            <v-btn icon="mdi-dots-vertical" variant="text" color="slate-300" size="small" v-bind="menuProps"
              class="context-menu-trigger"></v-btn>
          </template>
          <v-list class="executive-dropdown-menu pa-1" elevation="2" border>
            <v-list-item v-for="action in actions" :key="action.title" :prepend-icon="action.icon" :title="action.title"
              :color="action.color || 'primary'" class="rounded-lg mb-1 executive-menu-item"
              @click="$emit('action', { type: action.type, item })">
            </v-list-item>
          </v-list>
        </v-menu> -->
      </div>

      <!-- Section 2: Nomenclature Cluster -->
      <div class="nomenclature-shell mb-6">
        <div class="d-flex align-center ga-2 mb-2">
          <span class="ext-classification-tag"
            :style="{ color: fileConfig.color, background: fileConfig.color + '10' }">
            {{ extension }}
          </span>
          <div class="node-registry-divider"></div>
          <span class="registry-text">أرشيف رسمي معتمد</span>
        </div>

        <h3 class="node-primary-title text-right" :title="item?.name">
          {{ item?.name }}
        </h3>
      </div>

      <!-- Section 3: Technical Specs Footer -->
      <div class="node-stats-footer pt-4 border-top">
        <div class="d-flex align-center justify-space-between">
          <div class="specs-matrix-track">
            <div class="matrix-unit">
              <span class="unit-val">{{ fileSize(item?.attachment_size) }}</span>
              <span class="unit-sep">|</span>
              <span class="unit-val">{{ $moment(item?.uploaded_at)?.format("YYYY/MM/DD") }}</span>
            </div>
          </div>

          <!-- Discrete Action Deck -->
          <div class="node-action-deck d-flex ga-1">
            <v-btn variant="text" icon="mdi-eye-outline" color="slate-400" size="x-small" class="action-node-btn"
              @click="$emit('view', item)"></v-btn>
            <v-btn variant="text" icon="mdi-tray-arrow-down" color="primary" size="x-small" class="action-node-btn"
              @click="$emit('download', item)"></v-btn>
          </div>
        </div>
      </div>
    </div>
  </v-card>
</template>

<script>
export default {
  name: "FileCard",
  props: {
    item: { type: Object, required: true },
    name: { type: String, required: true },
    size: { type: String, required: true },
    is_view: { type: Boolean, required: false },
    actions: {
      type: Array,
      default: () => [
        { type: "view", title: "فتح الملف", icon: "mdi-eye-outline" },
        { type: "download", title: "تحميل النسخة", icon: "mdi-download-outline" },
        { type: "edit", title: "تعديل المسمى", icon: "mdi-pencil-outline" },
        { type: "delete", title: "حذف نهائي", icon: "mdi-delete-outline", color: "error" },
      ],
    },
  },
  emits: ["action", "view", "download"],
  data() {
    return {
      isHovered: false,
    };
  },
  computed: {
    extension() {
      // Logic from Original: use item.file
      return this.item?.file.split(".").pop().toUpperCase();
    },
    fileConfig() {
      // Keep New UI Colors/Icons but use 'extension' computed property
      const ext = this.extension.toLowerCase();
      const scheme = {
        pdf: { icon: "mdi-file-pdf-box", color: "#f43f5e" },
        doc: { icon: "mdi-file-word-box", color: "#2563eb" },
        docx: { icon: "mdi-file-word-box", color: "#2563eb" },
        xls: { icon: "mdi-file-excel-box", color: "#10b981" },
        xlsx: { icon: "mdi-file-excel-box", color: "#10b981" },
        jpg: { icon: "mdi-image-outline", color: "#f59e0b" },
        jpeg: { icon: "mdi-image-outline", color: "#f59e0b" },
        png: { icon: "mdi-image-outline", color: "#f59e0b" },
      };
      return scheme[ext] || { icon: "mdi-file-document-outline", color: "#64748b" };
    },
  },
  methods: {
    fileSize(file_size) {
      // Logic from Original: Strict MB calculation
      return (file_size / 1024 / 1024)?.toFixed(2) + "MB";
    },
  },
};
</script>

<style scoped>

.executive-node-card {
  font-family: 'Noto Sans Arabic', 'Plus Jakarta Sans', sans-serif !important;
  background-color: #ffffff;
  border: 1px solid #e2e8f0 !important;
  border-radius: 12px !important;
  position: relative;
  overflow: hidden;
  height: 100%;
}

.executive-node-card:hover {
  background-color: #f8fafc;
  border-color: #cbd5e1 !important;
}

.identity-wire {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2.5px;
  opacity: 0.15;
  transition: opacity 0.3s ease;
}

.card-active .identity-wire {
  opacity: 1;
}

/* Icon Signature Styling */
.icon-signature-box {
  width: 46px;
  height: 46px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease;
}

.card-active .icon-signature-box {
  transform: scale(1.05);
}

/* Nomenclature Detail */
.ext-classification-tag {
  font-size: 11.5px;
  font-weight: 800;
  padding: 3px 12px;
  border-radius: 8px;
  letter-spacing: 0.5px;
}

.node-registry-divider {
  width: 1px;
  height: 12px;
  background-color: #e2e8f0;
}

.registry-text {
  font-size: 11px;
  font-weight: 700;
  color: #94a3b8;
  letter-spacing: 0.3px;
}

.node-primary-title {
  font-size: 16px;
  font-weight: 800;
  color: #1e293b;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 3em;
  transition: color 0.2s ease;
}

.card-active .node-primary-title {
  color: #2563eb;
}

/* Stats Footer Detail */
.node-stats-footer {
  border-color: #f1f5f9 !important;
}

.matrix-unit {
  display: flex;
  align-items: center;
  font-size: 11px;
  font-weight: 700;
  color: #94a3b8;
}

.unit-sep {
  margin: 0 8px;
  opacity: 0.3;
}

.unit-val {
  color: #64748b;
}

/* Action Deck Controls */
.action-node-btn {
  border-radius: 8px !important;
}

.action-node-btn:hover {
  background-color: rgba(0, 0, 0, 0.05);
  color: #2563eb !important;
}

.executive-dropdown-menu {
  border-radius: 10px !important;
  border: 1px solid #e2e8f0 !important;
}

.executive-menu-item :deep(.v-list-item-title) {
  font-size: 13px !important;
  font-weight: 700 !important;
}

/* Responsive Adjustments */
@media (max-width: 960px) {
  .executive-node-card .pa-6 {
    padding: 18px !important;
  }

  .icon-signature-box {
    width: 42px;
    height: 42px;
  }

  .node-primary-title {
    font-size: 15px;
  }

  .ext-classification-tag {
    font-size: 10.5px;
    padding: 2px 10px;
  }

  .registry-text {
    font-size: 10px;
  }
}

@media (max-width: 600px) {
  .executive-node-card .pa-6 {
    padding: 16px !important;
  }

  .icon-signature-box {
    width: 40px;
    height: 40px;
  }

  .node-primary-title {
    font-size: 14px;
    height: 2.8em;
  }

  .ext-classification-tag {
    font-size: 10px;
    padding: 2px 8px;
  }

  .registry-text {
    display: none;
  }

  .node-registry-divider {
    display: none;
  }

  .matrix-unit {
    font-size: 10px;
  }

  .unit-sep {
    margin: 0 5px;
  }

  .action-node-btn {
    min-width: 28px !important;
    width: 28px !important;
    height: 28px !important;
  }

  .node-action-deck {
    gap: 4px !important;
  }
}

@media (max-width: 400px) {
  .executive-node-card .pa-6 {
    padding: 14px !important;
  }

  .icon-signature-box {
    width: 36px;
    height: 36px;
  }

  .node-primary-title {
    font-size: 13px;
  }
}
</style>
