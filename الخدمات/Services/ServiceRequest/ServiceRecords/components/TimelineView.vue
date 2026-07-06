<template>
  <div class="academic-timeline-system pa-0">
    <v-fade-transition mode="out-in">
      <!-- Direct Loading State -->
      <div
        v-if="loading && internalLogs.length === 0"
        key="loading"
        class="d-flex flex-column align-center justify-center py-10 py-sm-20"
        style="min-height: 300px"
      >
        <v-progress-circular
          indeterminate
          color="primary"
          size="44"
          width="3"
        />
        <div class="loader-meta mt-6 text-center">
          <h3 class="loader-h">تحديث السجل</h3>
          <p class="loader-p">جاري مزامنة بيانات النشاط</p>
        </div>
      </div>

      <!-- Clean Empty State -->
      <div
        v-else-if="internalLogs.length === 0"
        key="empty"
        class="
          d-flex
          flex-column
          align-center
          justify-center
          py-10 py-sm-20
          text-center
        "
        style="min-height: 300px"
      >
        <div class="empty-state-shell mb-6">
          <v-icon size="40" color="slate-200"
            >mdi-text-box-search-outline</v-icon
          >
        </div>
        <div class="monolith-intel px-4">
          <h3 class="intel-h">لا توجد أنشطة مسجلة</h3>
          <p class="intel-p mx-auto">
            سيتم عرض كافة الإجراءات فور البدء في معالجة هذا الطلب
          </p>
        </div>
      </div>

      <!-- Stable Timeline Feed -->
      <div v-else key="content" class="timeline-deployment-matrix pb-10">
        <v-timeline
          side="end"
          align="start"
          line-color="slate-200"
          line-thickness="2"
          :density="$vuetify.display.smAndDown ? 'compact' : 'comfortable'"
          class="elite-custom-timeline"
        >
          <v-timeline-item
            v-for="log in filteredLogs"
            :key="log.id"
            dot-color="white"
            size="x-small"
            class="mb-6 mb-md-8"
          >
            <template #icon>
              <div class="timeline-dot-core"></div>
            </template>

            <div class="timeline-content-wrapper pr-0 pr-md-4">
              <LogEntryCard
                :entry="log"
                @logEntry="$emit('add-note', $event)"
              />
            </div>
          </v-timeline-item>
        </v-timeline>

        <!-- Search Void State -->
        <v-fade-transition>
          <div
            v-if="filteredLogs.length === 0"
            class="
              d-flex
              flex-column
              align-center
              justify-center
              py-16
              text-center
            "
            style="min-height: 250px"
          >
            <v-icon size="44" color="slate-100" class="mb-4"
              >mdi-clipboard-text-search-outline</v-icon
            >
            <div class="void-text">
              لم يتم العثور على نتائج تطابق معايير البحث
            </div>
          </div>
        </v-fade-transition>
      </div>
    </v-fade-transition>
  </div>
</template>

<script>
import LogEntryCard from "./LogEntryCard.vue";

export default {
  name: "TimelineView",
  components: { LogEntryCard },

  props: {
    // request_id: { type: [Number, String], required: true },
    logs: { type: Array, default: () => [] },
    searchQuery: { type: String, default: "" },
  },

  inject: ["context"],
  data() {
    return {
      url: this.context.url,
      url_request_logs: "d-services/request-logs/",
      request_id: this.context.request_id,
      logs: [],
      loading: false,
      submitting: false,
      noteDialog: false,
      selectedLog: null,
      noteText: "",
      internalLogs: [],
    };
  },

  computed: {
    filteredLogs() {
      if (!this.searchQuery) return this.internalLogs;

      const query = this.searchQuery.toLowerCase();
      return this.internalLogs.filter((log) => {
        const inUser = log.user?.toLowerCase().includes(query);
        const inOldStatus = log.old_status_display
          ?.toLowerCase()
          .includes(query);
        const inNewStatus = log.new_status_display
          ?.toLowerCase()
          .includes(query);
        const inNotes = log.notes?.some((n) =>
          n.text?.toLowerCase().includes(query)
        );

        return inUser || inOldStatus || inNewStatus || inNotes;
      });
    },
  },

  mounted() {
    this.fetchLogs();
  },

  methods: {
    async fetchLogs() {
      this.loading = true;
      try {
        const res = await this.$axios.get(
          `${this.url_request_logs}status-changes/`,
          {
            params: { request_id: this.request_id },
          }
        );

        this.internalLogs = res.data.data || [];
      } catch (e) {
        console.error("Error fetching logs:", e);
      } finally {
        this.loading = false;
      }
    },

    openNoteDialog(log) {
      this.selectedLog = log;
      this.noteText = "";
      this.noteDialog = true;
    },
    async saveNote(entry, note) {
      try {
        await this.$axios.post(
          `${this.url_request_logs}${entry.id}/add-note/`,
          {
            // request_id: this.request_id,
            note: note,
          }
        );

        if (!entry.notes) this.entry.notes = [];
        entry.notes.push({
          user: this.context?.user?.name,
          text: note,
          time: new Date().toLocaleString(),
        });
        return true;
      } catch (e) {
        console.error("Error adding note:", e);
      } finally {
        throw e;
      }
    },
  },
};
</script>

<style scoped>
.academic-timeline-system {
  width: 100%;
}

.loader-h {
  font-size: 1.25rem;
  font-weight: 900;
  color: #0f172a;
}

.loader-p {
  font-size: 14px;
  color: #64748b;
  font-weight: 600;
}

.empty-state-shell {
  width: 64px;
  height: 64px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.intel-h {
  font-size: 1.15rem;
  font-weight: 900;
  color: #1e293b;
}

.intel-p {
  font-size: 13px;
  color: #64748b;
  max-width: 320px;
  line-height: 1.5;
}

.elite-custom-timeline {
  padding-left: 0 !important;
}

.timeline-dot-core {
  width: 10px;
  height: 10px;
  background: #ffffff;
  border: 3px solid rgb(var(--v-theme-primary));
  border-radius: 50%;
}

.void-text {
  font-size: 13.5px;
  color: #94a3b8;
  font-weight: 700;
}
</style>
