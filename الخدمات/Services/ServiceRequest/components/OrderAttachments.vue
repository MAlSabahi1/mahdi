<template>
  <div class="pro-archive-system">
    <!-- Main Shell: Clean Surface Grid -->
    <v-card class="pro-workspace-foundation rounded-xl elevation-0" border>

      <!-- Unified Control Hub: High-Efficiency Header -->
      <div class="pro-control-hub pa-4 pa-md-6 border-bottom">
        <v-row align="center" no-gutters class="ga-5">

          <!-- Modern Search Module -->
          <v-col cols="12" md="4" lg="3">
            <div class="pro-search-box">
              <v-icon icon="mdi-magnify" class="text-slate-400 ml-3" size="20"></v-icon>
              <input v-model="searchQuery" type="text" placeholder="ابحث في سجل الملفات..." class="pro-input-element" />
              <v-fade-transition>
                <v-icon v-if="searchQuery" icon="mdi-close" size="18" class="cursor-pointer text-slate-300"
                  @click="searchQuery = ''"></v-icon>
              </v-fade-transition>
            </div>
          </v-col>

          <v-spacer class="d-none d-md-block" />

          <!-- Workspace Modulation -->
          <v-col cols="12" md="auto">
            <div class="d-flex align-center flex-wrap ga-3 flex-column flex-sm-row">

              <!-- Segmented Toggles: Clear Logic -->
              <div class="pro-logic-rack w-100 w-sm-auto">
                <v-btn-toggle v-model="selectedType" mandatory variant="outlined" divided class="logic-toggle"
                  density="comfortable">
                  <v-btn v-for="type in fileTypes" :key="type.value" :value="type.value" class="logic-btn">
                    {{ type.label }}
                  </v-btn>
                </v-btn-toggle>
              </div>

              <v-divider vertical class="mx-1 d-none d-sm-block" height="32" />

              <!-- High-Performance Action -->
              <!-- <v-btn color="primary" variant="flat" class="pro-action-btn rounded-lg px-6 font-weight-black" height="40"
                prepend-icon="mdi-plus" @click="$emit('add')">
                إضافة ملف
              </v-btn> -->
            </div>
          </v-col>
        </v-row>
      </div>

      <!-- Content Core: CSS Grid 5-Column Layout -->
      <div class="pro-content-canvas pa-4 pa-md-8 bg-slate-50/5">
        <div v-if="filteredFiles.length" class="files-grid-5">
          <div v-for="file in filteredFiles" :key="file.id" class="grid-item">
            <FileCard :item="file" :name="file.name || ''" :size="file.attachment_size || ''" :is_view="true"
              @action="handleAction" @view="viewFile(setting?.url?.slice(0, -1) + (file.file || ''))"
              @download="downloadFile(file.file || '', file.name || '')" />
          </div>
        </div>

        <!-- Dynamic Feedback Narrative -->
        <div v-else class="pro-empty-track d-flex justify-center align-center py-20 w-100">
          <EmptyState :title="attachments.length === 0 ? 'لايوجد بيانات' : 'لا يوجد مرفقات مطابقة'"
            :description="attachments.length === 0 ? 'عفوا لايوجد بيانات لعرضها' : 'لم نتمكن من العثور على أي ملفات في هذا السجل تطابق معايير البحث الحالية.'"
            :icon="attachments.length === 0 ? 'mdi-alert-circle-outline' : 'mdi-file-search-outline'" action-label="" />
          <!-- <EmptyState title="لا يوجد مرفقات مطابقة"
            description="لم نتمكن من العثور على أي ملفات في هذا السجل تطابق معايير البحث الحالية."
            icon="mdi-file-search-outline" :action-label="searchQuery ? '' : 'رفع أول ملف'" @action="$emit('add')" /> -->
        </div>
      </div>
    </v-card>
  </div>
</template>

<script>
import FileCard from "./sub-components/OrderAttachments/FileCard.vue";
import EmptyState from "./sub-components/OrderAttachments/EmptyState.vue";

export default {
  name: "OrderAttachments",
  inject: ["context"],

  components: {
    FileCard,
    EmptyState,
  },
  props: {
    files: { type: Array, required: true },
  },
  emits: ["add", "view", "edit", "download", "delete"],
  data() {
    return {
      dialog: {},
      showFilters: false,
      searchQuery: "",
      selectedType: "all",
      fileTypes: [
        { label: "الكل", value: "all" },
        { label: "صور", value: "img" },
        { label: "pdf", value: "pdf" },
        { label: "docx", value: "docx" },
        { label: "xls", value: "xls" },
        { label: "xlsx", value: "xlsx" },
        { label: "أخرى", value: "أخرى" },
      ],
    };
  },
  computed: {
    attachments() {
      return this.context?.request_details?.attachments || [];
    },
    filteredFiles() {
      return this.attachments.filter((file) => {
        const matchesSearch = file.name
          .toLowerCase()
          .includes(this.searchQuery.toLowerCase());
        if (this.selectedType == "img") {
          const matchesType =
            this.selectedType === "all" ||
            ["jpg", "jpeg", "png"]?.includes(file?.attachment_extension);
          return matchesSearch && matchesType;
        } else {
          const matchesType =
            this.selectedType === "all" ||
            file?.attachment_extension == this.selectedType;
          return matchesSearch && matchesType;
        }
      });
    },
  },
  methods: {
    downloadFile(url, filename) {
      const link = document?.createElement("a");
      link.href = url;
      link.setAttribute("download", filename || "");
      document?.body?.appendChild(link);
      link?.click();
      document?.body?.removeChild(link);
    },
    viewFile(url) {
      window?.open(url, "_blank");
    },
    // handleAction({ type, item }) {
    //   console.log(type);
    //   switch (type) {
    //     case "edit":
    //       this.dialog.is_upload = false;
    //       this.dialog.show = true;
    //       break;

    //     default:
    //       break;
    //   }
    // },
  },
};
</script>

<style scoped>

.pro-archive-system {
  font-family: 'Noto Sans Arabic', 'Plus Jakarta Sans', sans-serif !important;
}

.pro-workspace-foundation {
  background: white;
  border-color: #e2e8f0 !important;
  border-radius: 12px !important;
  overflow: hidden;
}

.pro-control-hub {
  background: white;
  border-bottom: 1px solid #e2e8f0 !important;
}

/* Pro Search Box */
.pro-search-box {
  display: flex;
  align-items: center;
  background: #f1f5f9;
  border: 1px solid transparent;
  border-radius: 8px;
  padding: 0 14px;
  height: 40px;
  transition: all 0.2s ease;
}

.pro-search-box:focus-within {
  background: white;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.08);
}

.pro-input-element {
  border: none;
  background: transparent;
  outline: none;
  flex: 1;
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

/* Pro Logic Toggles */
.logic-toggle {
  border-color: #e2e8f0 !important;
  border-radius: 8px !important;
  background: #f8fafc;
}

.logic-btn {
  text-transform: none !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  letter-spacing: 0 !important;
  color: #64748b !important;
}

.logic-btn.v-btn--active {
  background-color: #eff6ff !important;
  color: #2563eb !important;
}

.pro-action-btn {
  text-transform: none !important;
  font-size: 14px !important;
  letter-spacing: 0 !important;
}

.pro-content-canvas {
  min-height: 600px;
}

@media (max-width: 600px) {
  .pro-control-hub {
    padding: 16px !important;
  }

  .pro-search-box {
    height: 38px;
    padding: 0 12px;
  }

  .pro-input-element {
    font-size: 13px;
  }

  .logic-toggle {
    width: 100%;
  }

  .logic-btn {
    font-size: 12px !important;
    padding: 0 12px !important;
  }

  .pro-action-btn {
    width: 100%;
    font-size: 13px !important;
    height: 38px !important;
  }

  .pro-content-canvas {
    padding: 16px !important;
    min-height: 400px;
  }
}

@media (max-width: 400px) {
  .pro-control-hub {
    padding: 12px !important;
  }

  .pro-search-box {
    height: 36px;
  }

  .logic-btn {
    font-size: 11px !important;
    padding: 0 8px !important;
  }

  .pro-action-btn {
    font-size: 12px !important;
    padding: 0 12px !important;
  }
}

/* CSS Grid: 5-Column Professional Layout */
.files-grid-5 {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 24px;
}

.grid-item {
  min-width: 0;
  /* Prevent grid blowout */
}

/* Responsive Grid Adjustments */
@media (max-width: 1600px) {
  .files-grid-5 {
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
  }
}

@media (max-width: 1280px) {
  .files-grid-5 {
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
  }
}

@media (max-width: 960px) {
  .files-grid-5 {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
}

@media (max-width: 600px) {
  .files-grid-5 {
    grid-template-columns: 1fr;
    gap: 14px;
  }
}
</style>
