<template>
  <v-card class="notes-container-premium elevation-0">
    <!-- Header -->
    <div class="notes-header-premium px-4 py-4 px-md-6 py-md-5">
      <div class="d-flex align-center justify-space-between flex-wrap gap-3">
        <div class="d-flex align-center">
          <div class="notes-icon-box-premium ml-3">
            <v-icon
              icon="mdi-message-text-outline"
              size="20"
              color="primary"
            ></v-icon>
          </div>
          <div>
            <h3 class="text-subtitle-1 font-weight-black text-slate-900 mb-0">
              الملاحظات
            </h3>
            <span class="text-tiny text-slate-400 font-weight-black"
              >{{ notes_items.length }} ملاحظة مسجلة</span
            >
          </div>
        </div>
        <v-btn
          color="primary"
          variant="flat"
          size="small"
          class="rounded-lg font-weight-black px-4"
          prepend-icon="mdi-plus"
          @click="openDialog()"
        >
          إضافة
        </v-btn>
      </div>
    </div>

    <!-- Ledger Body -->
    <v-card-text class="pa-0 notes-body-premium scroll-y">
      <div v-if="notes_items.length > 0" class="pa-5 d-flex flex-column gap-5">
        <div
          v-for="(note, index) in notes_items"
          :key="index"
          class="note-entry-premium"
        >
          <div class="d-flex align-start">
            <!-- Avatar with Status -->
            <div class="avatar-container ml-4">
              <v-avatar size="42" class="note-avatar-premium">
                <v-img
                  v-if="note.fk_created_by__image"
                  :src="setting?.url?.slice(0, -1) + note.fk_created_by__image"
                  cover
                ></v-img>
                <div v-else class="avatar-placeholder-premium">
                  {{ getInitials(authorName(note) || "U") }}
                </div>
              </v-avatar>
              <div class="status-dot-premium online"></div>
            </div>

            <!-- Content -->
            <div class="flex-grow-1">
              <div class="d-flex align-center justify-space-between mb-1">
                <div class="author-info">
                  <span
                    class="
                      text-subtitle-2
                      font-weight-black
                      text-slate-900
                      block
                    "
                  >
                    {{ authorName(note) || "مستخدم النظام" }}
                  </span>
                  <span class="text-tiny text-slate-400 d-flex align-center">
                    <v-icon
                      icon="mdi-clock-outline"
                      size="10"
                      class="ml-1"
                    ></v-icon>
                    {{ note.created_at || "الآن" }}
                  </span>
                </div>
                <div class="d-flex">
                  <v-btn
                    icon="mdi-delete-outline"
                    variant="text"
                    size="x-small"
                    color="slate-300"
                    class="action-btn"
                    @click="openConfirm(note)"
                  ></v-btn>
                </div>
              </div>

              <div class="note-bubble-premium">
                <p class="note-text-premium">{{ note.content }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div
        v-else
        class="
          empty-notes-premium
          pa-12
          d-flex
          flex-column
          align-center
          justify-center
        "
      >
        <div class="empty-icon-box-premium mb-5">
          <v-icon
            icon="mdi-message-off-outline"
            size="42"
            color="primary"
            class="opacity-20"
          ></v-icon>
        </div>
        <h4 class="text-subtitle-1 font-weight-black text-slate-700 mb-1">
          لا توجد ملاحظات
        </h4>
        <p class="text-caption text-slate-400 text-center px-6">
          لم يتم تسجيل أي ملاحظات على هذا الطلب حتى الآن
        </p>
      </div>
    </v-card-text>
  </v-card>

  <!-- Dialogs -->
  <v-dialog
    v-model="dialog.show"
    max-width="500"
    persistent
    transition="dialog-bottom-transition"
    class="dialog-premium"
  >
    <v-card class="elevation-0 rounded-xl overflow-hidden bg-white">
      <!-- Header -->
      <div
        class="
          dialog-header
          px-6
          py-4
          d-flex
          align-center
          justify-space-between
          bg-white
          border-b
        "
      >
        <div class="d-flex align-center">
          <div class="header-icon-box ml-4">
            <v-icon
              icon="mdi-message-plus-outline"
              color="primary"
              size="24"
            ></v-icon>
          </div>
          <div>
            <h3 class="text-h6 font-weight-bold text-slate-800 mb-0">
              إضافة ملاحظة
            </h3>
            <span class="text-caption text-slate-400">
              أضف ملاحظة جديدة إلى السجل
            </span>
          </div>
        </div>
        <v-btn
          icon="mdi-close"
          variant="text"
          density="comfortable"
          color="slate-400"
          @click="dialog.show = false"
          class="rounded-circle"
        ></v-btn>
      </div>

      <v-divider class="border-slate-100"></v-divider>

      <!-- Body -->
      <v-card-text class="pa-6">
        <v-textarea
          v-model="dialog.note"
          placeholder="اكتب تفاصيل الملاحظة هنا..."
          variant="outlined"
          color="primary"
          class="premium-textarea"
          rows="4"
          auto-grow
          focused
          hide-details
        ></v-textarea>
      </v-card-text>

      <v-divider class="border-slate-100"></v-divider>

      <!-- Footer -->
      <div class="pa-5 d-flex justify-end gap-3 bg-slate-50">
        <v-btn
          variant="text"
          color="slate-500"
          class="font-weight-bold px-6 rounded-lg"
          height="44"
          @click="dialog.show = false"
          :disabled="dialog.loading"
        >
          إلغاء
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          class="font-weight-bold px-8 rounded-lg elevation-2"
          height="44"
          @click="saveNote"
          :loading="dialog.loading"
        >
          إضافة الملاحظة
        </v-btn>
      </div>
    </v-card>
  </v-dialog>

  <BaseConfirm
    v-model="con_show"
    title="حذف الملاحظة"
    message="هل أنت متأكد من رغبتك في حذف هذه الملاحظة؟ لا يمكن التراجع عن هذا الإجراء."
    type="error"
    :loading="loading"
    @confirm="deleteNote"
  ></BaseConfirm>
</template>

<script>
export default {
  name: "OrderNotes",
  inject: ["context"],
  emits: ["add"],
  data() {
    return {
      notes_items: [],
      con_show: false,
      loading: false,
      note_id: null,
      url_get_notes: "d-services/service-requests/id/list-notes/",
      url_post_notes: "d-services/service-requests/id/add-note/",
      url_delete_notes: "d-services/service-requests/id/delete-note/",
      dialog: {
        show: false,
        note: "",
        loading: false,
      },
    };
  },
  created() {
    this.getNotes();
  },
  methods: {
    async getNotes() {
      await this.$axios(
        this.url_get_notes?.replace("id", this.context?.request_id)
      ).then((response) => (this.notes_items = response.data?.data));
    },
    async saveNote() {
      try {
        this.dialog.loading = true;
        await this.$axios
          ?.post(this.url_post_notes?.replace("id", this.context?.request_id), {
            content: this.dialog?.note,
          })
          .then(async (response) => {
            await this.getNotes();
            this.dialog.show = false;
            this.$snack("add", {message: response?.data?.message || 'تم إضافة الملاحظة بنجاح'})
          });
      } catch (error) {
        console.log(error);
      } finally {
        this.dialog.loading = false;
      }
    },
    async deleteNote() {
      try {
        this.loading = true;
        await this.$axios
          ?.delete(
            this.url_delete_notes?.replace("id", this.context?.request_id) +
              `${this.note_id}/`,
            {
              content: this.dialog?.note,
            }
          )
          .then(async (response) => {
            await this.getNotes();
          });
      } catch (error) {
        console.log(error);
      } finally {
        this.con_show = false;
        this.loading = false;
      }
    },

    openDialog() {
      this.dialog.show = true;
      this.dialog.note = null;
    },
    openConfirm(note) {
      this.con_show = true;
      this.note_id = note?.id;
    },
    getInitials(name) {
      if (name) {
        return name
          .split(" ")
          .map((n) => n[0])
          .slice(0, 2)
          .join("");
      }
      return "";
    },
    authorName(note) {
      if (note?.fk_created_by__first_name || note?.fk_created_by__last_name) {
        return `${note?.fk_created_by__first_name || ""} ${
          note?.fk_created_by__last_name || ""
        }`;
      }
      return note?.fk_created_by__username || false;
    },
  },
};
</script>

<style scoped>
.notes-container-premium {
  background: #ffffff;
  border: 1px solid #f1f5f9;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100%;
}

.notes-header-premium {
  background: #ffffff;
  padding: 16px 24px;
  border-bottom: 1px solid #f8fafc;
}

.notes-icon-box-premium {
  width: 40px;
  height: 40px;
  background: #eff6ff;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notes-body-premium {
  flex-grow: 1;
  max-height: 600px;
  background-color: #ffffff;
}

.note-entry-premium {
  position: relative;
  /* transition: all 0.3s ease; */
}

.avatar-container {
  position: relative;
}

.note-avatar-premium {
  border: 2px solid #ffffff;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.avatar-placeholder-premium {
  width: 100%;
  height: 100%;
  background: #f1f5f9;
  color: #2563eb;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-dot-premium {
  position: absolute;
  bottom: 2px;
  left: 2px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2.5px solid #ffffff;
  z-index: 1;
}

.status-dot-premium.online {
  background: #10b981;
}

.note-bubble-premium {
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  border-radius: 18px;
  border-top-right-radius: 4px;
  padding: 16px 20px;
  transition: all 0.3s ease;
}

.note-entry-premium:hover .note-bubble-premium {
  background: #ffffff;
  border-color: #e2e8f0;
  /* box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03); */
}

.note-text-premium {
  font-size: 14px;
  color: #334155;
  line-height: 1.6;
  margin-bottom: 0;
  white-space: pre-wrap;
}

.action-btn {
  opacity: 0;
  transition: all 0.2s ease;
}

.note-entry-premium:hover .action-btn {
  opacity: 1;
}

.empty-icon-box-premium {
  width: 84px;
  height: 84px;
  background: #f8fafc;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px dashed #e2e8f0;
}

.text-tiny {
  font-size: 10px;
}

.text-slate-900 {
  color: #0f172a !important;
}

.text-slate-700 {
  color: #334155 !important;
}

.text-slate-400 {
  color: #94a3b8 !important;
}

.scroll-y {
  overflow-y: auto;
}

.scroll-y::-webkit-scrollbar {
  width: 4px;
}

.scroll-y::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 10px;
}

.gap-5 {
  gap: 20px;
}

/* Dialog Styles */
.header-icon-box {
  width: 44px;
  height: 44px;
  background: #eff6ff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.premium-textarea :deep(.v-field) {
  border-radius: 12px !important;
  border: 1px solid #e2e8f0;
  background-color: #f8fafc;
  transition: all 0.2s ease;
}

.premium-textarea :deep(.v-field__outline) {
  display: none !important;
}

.premium-textarea :deep(.v-field--focused) {
  background-color: #ffffff;
  border-color: #2563eb !important;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08);
  /* Glow effect */
}

.bg-slate-50 {
  background-color: #f8fafc !important;
}

.text-slate-800 {
  color: #1e293b !important;
}

.border-slate-100 {
  border-color: #f1f5f9 !important;
}

.gap-3 {
  gap: 12px;
}
</style>
