<template>
  <div  class="service-records-canvas pa-0">
    <div class="records-prime-wrapper">
      <!-- Simplified Professional Header (Performance & Responsive) -->
      <div class="sticky-dock-layer">
        <div class="dock-inner-matrix">
          <RecordsHeader
            :title="pageTitle"
            :icon="pageIcon"
            :loading="isExporting"
            v-model:search="searchQuery"
            @export="handleExport"
            @refresh="refreshData"
          />
        </div>
      </div>

      <!-- Global Archive Feed Arena (Responsive Padding) -->
      <div class="feed-arena">
        <v-row>
          <v-col cols="12" xl="10" xxl="8">
            <div class="timeline-stabilizer-high-perf">
              <TimelineView
                ref="timeline"
                :search-query="searchQuery"
                @add-note="openNoteModal"
                @note-saved="
                  showFeedback(
                    'تم حفظ الملاحظة بنجاح',
                    'success',
                    'mdi-check-circle'
                  )
                "
              />
            </div>
          </v-col>
        </v-row>
      </div>
    </div>

    <!-- Note Entry Portal (Centralized Elite Dialog) -->
    <NoteModal
      v-model="noteModal"
      :title="noteModalTitle"
      :entry="selectedEntry"
      @save="saveNote"
    />

    <!-- High-Performance Feedback Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3500"
      :location="$vuetify.display.smAndDown ? 'bottom' : 'top left'"
      class="prime-system-snackbar"
      flat
    >
      <div class="d-flex align-center ga-3 px-1">
        <div class="snack-icon-shell">
          <v-icon size="20" color="white">{{ snackbar.icon }}</v-icon>
        </div>
        <div class="snack-logic-stack">
          <div class="snack-label-prime">النظام</div>
          <div class="snack-content-prime">{{ snackbar.text }}</div>
        </div>
      </div>

      <template v-slot:actions>
        <v-btn
          icon="mdi-close"
          variant="text"
          color="white"
          size="x-small"
          @click="snackbar.show = false"
        />
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import RecordsHeader from "./components/RecordsHeader.vue";
import TimelineView from "./components/TimelineView.vue";
import NoteModal from "./components/NoteModal.vue";

export default {
  name: "ServiceRecords",

  components: {
    RecordsHeader,
    TimelineView,
    NoteModal,
  },

  data() {
    return {
      pageTitle: "سجل النشاط",
      pageIcon: "mdi-history",
      noteModalTitle: "إضافة ملاحظة",
      noteModal: false,
      selectedEntry: null,
      searchQuery: "",

      // Feedback System
      snackbar: {
        show: false,
        text: "",
        color: "success",
        icon: "mdi-check-circle",
      },
      isExporting: false,
    };
  },

  methods: {
    refreshData() {
      if (this.$refs.timeline) {
        this.$refs.timeline.fetchLogs();
        this.showFeedback("تم تحديث البيانات بنجاح", "success", "mdi-refresh");
      }
    },
    async handleExport() {
      if (this.isExporting) return;

      const logs = this.$refs.timeline?.internalLogs || [];
      if (logs.length === 0) {
        this.showFeedback(
          "لا توجد بيانات لتصديرها حالياً",
          "warning",
          "mdi-alert-circle-outline"
        );
        return;
      }

      this.isExporting = true;
      this.showFeedback(
        "جاري إنشاء التقرير...",
        "info",
        "mdi-file-clock-outline"
      );

      try {
        await new Promise((resolve) => setTimeout(resolve, 800));

        const headers = [
          "المسؤول",
          "الحالة السابقة",
          "الحالة الجديدة",
          "التاريخ",
          "الوقت",
          "الملاحظات",
        ];
        const rows = logs.map((log) => [
          log.user,
          log.old_status_display,
          log.new_status_display,
          log.date,
          log.time,
          log.notes?.map((n) => n.text).join(" | ") || "",
        ]);

        const csvContent =
          "\uFEFF" +
          [
            headers.join(","),
            ...rows.map((r) => r.map((cell) => `"${cell}"`).join(",")),
          ].join("\n");

        const blob = new Blob([csvContent], {
          type: "text/csv;charset=utf-8;",
        });
        const link = document.createElement("a");
        const url = URL.createObjectURL(blob);
        const fileName = `تقرير_العمليات_${
          new Date().toISOString().split("T")[0]
        }.csv`;

        link.setAttribute("href", url);
        link.setAttribute("download", fileName);
        link.click();
        URL.revokeObjectURL(url);

        this.showFeedback(
          "تم تحميل التقرير بنجاح",
          "success",
          "mdi-file-check-outline"
        );
      } catch (error) {
        this.showFeedback("فشل في إنشاء التقرير", "error", "mdi-alert-circle");
      } finally {
        this.isExporting = false;
      }
    },
    showFeedback(text, color = "success", icon = "mdi-check-circle") {
      this.snackbar.text = text;
      this.snackbar.color = color;
      this.snackbar.icon = icon;
      this.snackbar.show = true;
    },
    openNoteModal(entry) {
      this.selectedEntry = entry;
      this.noteModal = true;
    },
    async saveNote(note) {
      try {
        await this.$refs.timeline.saveNote(this.selectedEntry, note);
        this.showFeedback(
          "تم حفظ الملاحظة بنجاح",
          "success",
          "mdi-check-circle"
        );
        this.noteModal = false;
      } catch (error) {
        this.showFeedback("فشل في حفظ الملاحظة", "error", "mdi-alert-circle");
      }
    },
  },
};
</script>

<style scoped>
.service-records-canvas {
  min-height: 100vh;
  background-color: #f8fafc;
  position: relative;
  overflow-x: hidden;
  font-family: "Noto Sans Arabic", "Plus Jakarta Sans", sans-serif;
}

.records-prime-wrapper {
  position: relative;
  z-index: 1;
}

.sticky-dock-layer {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.dock-inner-matrix {
  width: 100%;
}

.feed-arena {
  padding-bottom: 80px;
}

.timeline-stabilizer-high-perf {
  contain: content;
}

.prime-system-snackbar :deep(.v-snackbar__wrapper) {
  border-radius: 12px !important;
  background: #1e293b !important;
  box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.2) !important;
}

.snack-icon-shell {
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.snack-label-prime {
  font-size: 9px;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
  margin-bottom: 1px;
}

.snack-content-prime {
  font-size: 13.5px;
  font-weight: 700;
  color: #f8fafc;
}
</style>
