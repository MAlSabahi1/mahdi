<template>
  <div class="executive-log-node" :class="{ 'is-hovered': isHovered }" @mouseenter="isHovered = true"
    @mouseleave="isHovered = false">
    <!-- Node Master Segment -->
    <div class="pa-4 pa-sm-6 pa-md-7 pb-0">
      <div class="d-flex align-center justify-space-between flex-wrap ga-4 mb-6">
        <!-- Responsive Track Chassis -->
        <div class="d-flex align-center ga-4 w-100 w-sm-auto">
          <div class="evolution-track-chassis flex-grow-1 flex-sm-grow-0">
            <div class="status-node old">{{ entry.old_status_display }}</div>
            <div class="track-arrow">
              <v-icon icon="mdi-chevron-left" size="18" color="primary"></v-icon>
            </div>
            <div class="status-node new">{{ entry.new_status_display }}</div>
          </div>
        </div>

        <!-- Meta Info (Stamps) -->
        <div class="chronicle-meta d-flex ga-2 ga-sm-3 ml-auto ml-sm-0">
          <div class="meta-capsule">
            <v-icon icon="mdi-calendar-range" size="14" class="ml-1 ml-sm-2" color="slate-400"></v-icon>
            <span class="d-none d-xs-inline">{{ entry.date || '---' }}</span>
            <span class="d-inline d-xs-none">{{ entry.date ? entry.date.split('-').slice(1).join('-') : '---' }}</span>
          </div>
          <div class="meta-capsule">
            <v-icon icon="mdi-clock-check-outline" size="14" class="ml-1 ml-sm-2" color="slate-400"></v-icon>
            <span>{{ entry.time }}</span>
          </div>
        </div>
      </div>

      <!-- User Identity & Action Hub -->
      <div class="d-flex align-center justify-space-between flex-wrap ga-4 ga-sm-5 pb-6 border-bottom-matrix">
        <div class="authority-profile">
          <div class="avatar-halo d-none d-xs-block">
            <v-avatar size="40" sm="44" color="white" class="elevation-1">
              <v-icon color="primary" size="22" sm="24">mdi-account-tie-circle-outline</v-icon>
            </v-avatar>
          </div>
          <div class="authority-registry">
            <h4 class="auth-name">{{ entry.user }}</h4>
            <div class="auth-badge">
              <span class="badge-dot-live"></span>
              المسؤول عن الإجراء
            </div>
          </div>
        </div>

        <v-btn color="primary" variant="tonal" class="prime-note-btn rounded-lg px-4 px-sm-6 font-weight-black"
          height="38" sm="40" prepend-icon="mdi-pencil-plus" @click="$emit('logEntry', entry)">
          إضافة ملاحظة
        </v-btn>
      </div>
    </div>

    <!-- Technical Documentation Matrix (Notes Feed) -->
    <div v-if="entry.notes && entry.notes.length" class="technical-matrix-footer pa-4 pa-sm-6 pa-md-7">
      <div class="matrix-marker d-flex align-center ga-3 mb-4">
        <div class="marker-line"></div>
        <span class="marker-label">الملاحظات الإدارية</span>
      </div>

      <div class="notes-deployment-stack">
        <div v-for="(note, idx) in entry.notes" :key="idx" class="matrix-entry-card pa-3 pa-sm-4 rounded-xl">
          <div class="entry-header d-flex align-center justify-space-between flex-wrap ga-2 mb-3">
            <div class="d-flex align-center ga-2">
              <div class="ident-icon-box">
                <v-icon icon="mdi-card-account-details-outline" size="12" color="primary"></v-icon>
              </div>
              <span class="entry-author">{{ note.user }}</span>
            </div>
            <span class="entry-time">{{ note.time }}</span>
          </div>
          <div class="entry-content-box pa-3 pa-sm-4 rounded-lg">
            <p class="entry-text">
              {{ note.text }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LogEntryCard",
  props: {
    entry: { type: Object, required: true },
    topDetails: { type: Boolean, default: true },
  },
  emits: ["logEntry"],
};
</script>

<style scoped>

.executive-log-node {
  font-family: 'Noto Sans Arabic', 'Plus Jakarta Sans', sans-serif;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  contain: content;
}

@media (min-width: 600px) {
  .executive-log-node {
    border-radius: 24px;
  }
}

.executive-log-node.is-hovered {
  border-color: #3b82f6;
  box-shadow: 0 10px 30px -10px rgba(37, 99, 235, 0.1);
}

.executive-log-node::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, #2563eb, #3b82f6);
}

.evolution-track-chassis {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f8fafc;
  padding: 4px;
  border-radius: 10px;
  border: 1px solid #f1f5f9;
}

.status-node {
  font-size: 11px;
  font-weight: 800;
  padding: 5px 12px;
  border-radius: 8px;
  text-align: center;
}

.status-node.old {
  color: #64748b;
  background: #ffffff;
  border: 1px solid #e2e8f0;
}

.status-node.new {
  color: #2563eb;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
}

@media (max-width: 600px) {
  .status-node {
    font-size: 10px;
    padding: 3px 8px;
    min-width: 60px;
  }

  .track-arrow .v-icon {
    font-size: 14px !important;
  }
}

.chronicle-meta {
  flex-wrap: nowrap;
}

.meta-capsule {
  display: flex;
  align-items: center;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  color: #64748b;
}

.authority-profile {
  display: flex;
  align-items: center;
  gap: 12px;
}

.auth-name {
  font-size: 14px;
  font-weight: 850;
  color: #1e293b;
  margin-bottom: 2px;
}

.auth-badge {
  font-size: 10px;
  font-weight: 800;
  color: #64748b;
  display: flex;
  align-items: center;
  gap: 4px;
}

.badge-dot-live {
  width: 6px;
  height: 6px;
  background: #10b981;
  border-radius: 50%;
}

.prime-note-btn {
  font-size: 12px;
  text-transform: none;
}

.technical-matrix-footer {
  background: #fafbfc;
  border-top: 1px solid #f1f5f9;
}

.matrix-marker .marker-line {
  width: 20px;
  height: 3px;
  background: #2563eb;
  border-radius: 10px;
}

.marker-label {
  font-size: 10px;
  font-weight: 900;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.matrix-entry-card {
  background: #ffffff;
  border: 1px solid #f1f5f9;
  margin-bottom: 12px;
}

.entry-author {
  font-size: 12px;
  font-weight: 800;
  color: #334155;
}

.entry-time {
  font-size: 10.5px;
  font-weight: 600;
  color: #94a3b8;
}

.entry-content-box {
  background: #f8fafc;
  border: 1px solid #f1f5f9;
}

.entry-text {
  font-size: 13px;
  font-weight: 500;
  color: #475569;
  line-height: 1.6;
  margin-bottom: 0;
}

@media (max-width: 600px) {
  .entry-text {
    font-size: 12px;
    line-height: 1.5;
  }

  .auth-name {
    font-size: 13px;
  }

  .meta-capsule {
    padding: 3px 8px;
    font-size: 10px;
  }
}

.border-bottom-matrix {
  border-bottom: 1px solid #f1f5f9;
}

@media (max-width: 600px) {
  .status-node {
    font-size: 10px;
    padding: 4px 8px;
  }

  .authority-profile {
    width: 100%;
  }

  .prime-note-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
