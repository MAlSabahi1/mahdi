<template>
  <div class="order-outputs-premium-page">
    <!-- Main Split Layout -->
    <v-row no-gutters class="fill-height">
      <!-- Right Side: Actions & Management -->
      <v-col cols="12" lg="5" xl="4" class="order-lg-1 d-flex flex-column bg-white border-left-system right-panel">
        <!-- Premium Integrated Toolbar -->
        <div class="toolbar-premium px-4 py-3 px-md-6 py-md-5">
          <v-card variant="flat" class="toolbar-card pa-4 rounded-xl border-system shadow-sm">
            <div class="d-flex flex-column gap-4">
              <!-- Top Row: Brand & Status -->
              <div class="d-flex align-center justify-space-between flex-wrap gap-3">
                <div class="d-flex align-center">
                  <div class="brand-icon-wrapper ml-4">
                    <v-avatar color="primary" variant="flat" size="48" class="rounded-lg elevation-4">
                      <v-icon :icon="availableDocument ? 'mdi-file-check' : 'mdi-file-plus-outline'" size="26"
                        color="white"></v-icon>
                    </v-avatar>
                    <div :class="['status-dot', availableDocument ? 'bg-success' : 'bg-warning']"></div>
                  </div>
                  <div>
                    <div class="text-subtitle-1 font-weight-black text-high-emphasis leading-tight">
                      {{ availableDocument ? 'المخرجات المعتمدة' : 'إدارة المخرجات' }}
                    </div>
                    <div class="text-caption font-weight-bold d-flex align-center mt-1">
                      <span :class="availableDocument ? 'text-success' : 'text-warning'">
                        {{ availableDocument ? 'مؤرشف رسمياً' : 'بانتظار الرفع' }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <v-divider></v-divider>

              <!-- Bottom Row: Actions -->
              <div class="d-flex align-center flex-wrap gap-2 w-100">
                <template v-if="availableDocument">
                  <v-btn color="primary" variant="flat" class="flex-grow-1 rounded-lg font-weight-bold btn-hover-effect"
                    prepend-icon="mdi-download" :href="data ? data[fileKey] : request_details[`${type}_document`]"
                    download height="40">
                    تحميل
                  </v-btn>
                  <v-btn color="error" variant="tonal" class="rounded-lg btn-hover-effect" icon="mdi-delete-outline"
                    @click="dialog_delete = true" height="40" width="40"></v-btn>
                </template>
                <template v-else-if="document?.name">
                  <v-btn color="success" variant="flat" class="flex-grow-1 rounded-lg font-weight-bold btn-hover-effect"
                    prepend-icon="mdi-cloud-check" @click="uploadDocument" height="40">
                    حفظ واعتماد
                  </v-btn>
                  <v-btn color="error" variant="tonal" class="rounded-lg btn-hover-effect" icon="mdi-close"
                    @click="document = null" height="40" width="40"></v-btn>
                </template>
                <template v-else>
                  <div class="text-caption text-medium-emphasis flex-grow-1 text-center">
                    يرجى اختيار ملف للبدء
                  </div>
                </template>

                <v-divider vertical class="mx-2 hidden-xs"></v-divider>

                <custom-btn color="primary" variant="outlined"
                  class="flex-grow-1 flex-sm-grow-0 rounded-lg font-weight-bold btn-hover-effect" type="print"
                  :print="`${type}_print`"
                  :print_id="data?.print_report_settings?.[`fk_print_report_setting_for_${type}`] || request_details[`fk_print_report_setting_for_${type}`]"
                  label="طباعة" icon="mdi-printer" height="40" block-mobile />
              </div>
            </div>
          </v-card>
        </div>

        <!-- Scrollable Content Area -->
        <div class="flex-grow-1 overflow-y-auto pa-4 pa-md-8 custom-scrollbar pb-16">
          <div class="max-w-600 mx-auto w-100">
            <!-- Section Header -->
            <div class="section-intro mb-10">
              <div class="d-flex align-center mb-3">
                <div class="section-dot ml-3"></div>
                <h3 class="text-h5 font-weight-black text-primary">إجراءات المستند المخرج</h3>
              </div>
              <p class="text-body-1 text-medium-emphasis leading-relaxed">
                يرجى إدارة ورفع النسخة النهائية المعتمدة من الطلب. تأكد من مطابقة البيانات قبل عملية الحفظ النهائي.
              </p>
            </div>

            <!-- Upload Zone Premium -->
            <v-card v-if="!availableDocument && !document?.name" variant="flat"
              class="upload-zone-premium pa-12 text-center border-dashed-system mb-10" @click="triggerFileInput">
              <div class="upload-visual mb-8">
                <div class="icon-stack">
                  <v-icon icon="mdi-cloud-upload" color="primary" size="72" class="main-icon"></v-icon>
                  <v-icon icon="mdi-plus-circle" color="primary" size="24" class="sub-icon"></v-icon>
                </div>
              </div>
              <div class="text-h4 font-weight-black text-high-emphasis mb-4">رفع الملف النهائي</div>
              <p class="text-body-1 text-medium-emphasis mb-10 leading-relaxed px-6">
                قم بسحب الملف هنا أو انقر لاختياره من جهازك.
                <br />
                <span class="text-primary font-weight-bold">يفضل استخدام صيغة PDF لضمان الجودة.</span>
              </p>
              <v-btn color="primary" variant="flat" size="x-large"
                class="rounded-xl px-16 font-weight-black elevation-12 action-btn-hero">
                اختيار ملف من الجهاز
              </v-btn>
              <div class="text-caption text-disabled mt-8 d-flex align-center justify-center gap-4">
                <span class="d-flex align-center"><v-icon size="14" class="ml-1">mdi-file-pdf-box</v-icon> PDF</span>
                <span class="d-flex align-center"><v-icon size="14" class="ml-1">mdi-image</v-icon> JPG/PNG</span>
                <span class="d-flex align-center"><v-icon size="14" class="ml-1">mdi-weight</v-icon> Max 20MB</span>
              </div>
            </v-card>

            <!-- Status Info Card Premium -->
            <v-card v-else variant="flat"
              class="status-card-premium border-system rounded-2xl overflow-hidden mb-10 shadow-sm">
              <div
                :class="['pa-8 text-center font-weight-black status-banner', availableDocument ? 'bg-success-light text-success' : 'bg-warning-light text-warning']">
                <v-icon :icon="availableDocument ? 'mdi-check-decagram' : 'mdi-timer-sand'" class="ml-3"
                  size="40"></v-icon>
                <div class="text-h5 mt-2">{{ availableDocument ? 'تم الاعتماد والأرشفة' : 'بانتظار الحفظ النهائي' }}
                </div>
              </div>
              <v-card-text class="pa-10">
                <div class="detail-list-premium">
                  <div class="detail-item d-flex justify-space-between py-5 border-bottom">
                    <span class="text-body-1 text-medium-emphasis font-weight-bold">حالة المستند في النظام:</span>
                    <v-chip :color="availableDocument ? 'success' : 'warning'" variant="flat"
                      class="font-weight-black px-6">
                      {{ availableDocument ? 'مؤرشف نهائياً' : 'مسودة قيد الرفع' }}
                    </v-chip>
                  </div>
                  <div class="detail-item d-flex justify-space-between py-5 border-bottom">
                    <span class="text-body-1 text-medium-emphasis font-weight-bold">نوع الوثيقة الرسمية:</span>
                    <span class="text-body-1 font-weight-black text-high-emphasis">مخرجات رسمية معتمدة</span>
                  </div>
                  <div v-if="document?.name" class="detail-item d-flex justify-space-between py-5">
                    <span class="text-body-1 text-medium-emphasis font-weight-bold">اسم الملف المختار:</span>
                    <span class="text-body-1 font-weight-black text-primary d-flex align-center">
                      <v-icon size="18" class="ml-2">mdi-file-document-outline</v-icon>
                      {{ document.name }}
                    </span>
                  </div>
                </div>
              </v-card-text>
            </v-card>

            <!-- Official Guidelines Premium -->
            <v-card variant="flat" class="guidelines-card-premium pa-8 rounded-2xl border-system">
              <div class="d-flex align-center mb-6">
                <v-avatar color="primary" variant="tonal" size="40" class="ml-4">
                  <v-icon icon="mdi-shield-check-outline" size="24"></v-icon>
                </v-avatar>
                <span class="text-h6 font-weight-black text-primary">ضوابط الرفع الرسمية</span>
              </div>
              <div class="guidelines-list">
                <div class="guideline-item d-flex align-start mb-4">
                  <v-icon icon="mdi-check-circle" color="primary" size="18" class="ml-3 mt-1"></v-icon>
                  <span class="text-body-2 font-weight-bold text-medium-emphasis leading-relaxed">يجب أن تكون النسخة
                    المرفوعة
                    مطابقة تماماً للنموذج المعتمد في المعاينة.</span>
                </div>
                <div class="guideline-item d-flex align-start mb-4">
                  <v-icon icon="mdi-check-circle" color="primary" size="18" class="ml-3 mt-1"></v-icon>
                  <span class="text-body-2 font-weight-bold text-medium-emphasis leading-relaxed">تأكد من وضوح الأختام
                    والتوقيعات الرسمية؛ المستندات غير الواضحة سيتم رفضها تلقائياً.</span>
                </div>
                <div class="guideline-item d-flex align-start">
                  <v-icon icon="mdi-check-circle" color="primary" size="18" class="ml-3 mt-1"></v-icon>
                  <span class="text-body-2 font-weight-bold text-medium-emphasis leading-relaxed">يمنع رفع أي ملفات
                    تحتوي على
                    تعديلات يدوية أو طموس غير رسمية.</span>
                </div>
              </div>
            </v-card>
          </div>
        </div>

        <v-form ref="form" class="d-none">
          <v-file-input v-model="document" ref="fileInput" required />
        </v-form>
      </v-col>

      <!-- Left Side: Full Screen Preview -->
      <v-col cols="12" lg="7" xl="8" class="order-lg-2 d-flex flex-column bg-slate-50 border-system-left">
        <!-- Preview Header Premium -->
        <div class="preview-header-premium px-4 py-3 px-md-6 py-md-4 border-bottom bg-white shadow-sm">
          <div class="d-flex align-center justify-space-between">
            <div class="d-flex align-center">
              <div class="preview-icon-box ml-4">
                <v-icon icon="mdi-file-eye" color="primary" size="24"></v-icon>
              </div>
              <div>
                <span class="text-subtitle-1 font-weight-black text-high-emphasis">معاينة النموذج الرسمي</span>
                <div class="text-caption text-medium-emphasis font-weight-bold">عرض حي للنسخة المعتمدة من الطلب</div>
              </div>
            </div>
            <div class="d-flex align-center gap-2">
              <v-chip color="primary" variant="tonal" class="font-weight-black px-4 hidden-sm-and-down" size="small">
                <v-icon start size="14">mdi-file-document</v-icon>
                A4 STANDARD
              </v-chip>
              <v-btn icon="mdi-fullscreen" variant="text" color="medium-emphasis" size="small"></v-btn>
            </div>
          </div>
        </div>

        <!-- Full Height Preview Area -->
        <div class="flex-grow-1 overflow-y-auto bg-preview custom-scrollbar pb-16">
          <div class="preview-viewport pa-4 pa-md-10 pa-xl-16">
            <v-card variant="flat" :id="`${type}_print`" class="document-premium-view mx-auto shadow-2xl">
              <div class="document-content-wrapper">
                <div class="text-center py-4  ">
                  <!-- <span class="rounded border pa-2 bg-grey-lighten-4 font-weight-black px-10  ">بيان حالة </span> -->
                </div>
                <component :is="component"></component>
              </div>
            </v-card>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Confirmation Dialog -->
    <confirm-dialog v-model="dialog_delete" type="warning" type_btn="delete" title="تأكيد الحذف"
      message="هل انت متأكذ من حذف ملف المخرجات ؟ " :confirmBtn="deleteDocument" />
  </div>
</template>

<script>
export default {
  name: "OrderOutputsInput",
  inject: ["context"],
  props: {
    type: String,
    url: { type: String, default: "" },
    stage_id: { type: String, default: "" },
    data: { type: Object, default: null },
    fileKey: { type: String, default: "" },
    uploadFun: { type: Function, default: null },
    deleteFun: { type: Function, default: null },
    template: { type: String, default: "" },
  },
  data() {
    return {
      tab: "document",
      document: [],
      dialog_upload: false,
      request_details: this.context?.request_details ?? {},
      request_id: this.context.request_id,
      dialog_delete: false,
    };
  },
  computed: {
    component() {
      return (
        this.template ||
        this.context.request_details[`${this.type}_template_type`]
      );
    },
    availableDocument() {
      if (this.data) {
        return this.data[this.fileKey] ? true : false;
      } else {
        return this.request_details[`${this.type}_document`] ? true : false;
      }
    },
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.$el.querySelector('input[type="file"]').click();
    },
    async uploadDocument() {
      const { valid } = await this.$refs.form.validate();
      if (valid) {
        const form = new FormData();
        form.append(`${this.type}_document`, this.document);
        if (this.uploadFun) {
          this.uploadFun(form);
        } else {
          await this.$axios
            .post(
              `${this.url || this.context?.url}${this.stage_id || this.request_id
              }/upload-${this.type}/`,
              form,
              {
                headers: {
                  "Content-Type": "multipart/form-data",
                },
              }
            )
            .then((res) => {
              this.document = null;
              if (this.data) {
                this.data[this.fileKey] = res?.data?.data[this.fileKey];
                console.log(this.data);
              } else {
                this.request_details[`${this.type}_document`] =
                  res?.data?.data[`${this.type}_document`];
              }

              this.$snack("add", { message: "تم ادراج الاستمارة بنجاح" });
              this.context.getRequestDetails();
            });
        }
      }
    },
    async deleteDocument() {
      if (this.deleteFun) {
        this.deleteFun();
      } else {
        await this.$axios.delete(
          `${this.url}${this.stage_id || this.request_id}/delete-${this.type}/`
        );
        if (this.data) {
          this.data[this.fileKey] = undefined;
        } else {
          this.request_details[`${this.type}_document`] = undefined;
        }
        this.$snack("del");
      }
    },
    openFile(file) {
      window.open(
        this.setting.url.slice(0, -1) + file,
        "_blank",
        "noopener,noreferrer"
      );
    },
  },
};
</script>

<style scoped>

.order-outputs-premium-page {
  font-family: 'Almarai', sans-serif !important;
  height: 100vh;
  width: 100%;
  /* overflow: hidden; */
  background-color: #ffffff;
}

/* Toolbar Premium */
.toolbar-premium {
  z-index: 10;
  background-color: #ffffff;
  position: sticky;
  top: 0;
}

.toolbar-card {
  background-color: #ffffff !important;
}

.brand-icon-wrapper {
  position: relative;
}

.status-dot {
  position: absolute;
  bottom: -2px;
  right: -2px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid white;
}

/* Right Side Styles */
.border-left-system {
  border-left: 1px solid #f1f5f9;
}

.section-dot {
  width: 8px;
  height: 8px;
  background-color: rgb(var(--v-theme-primary));
  border-radius: 50%;
}

/* Upload Zone Premium */
.upload-zone-premium {
  background: linear-gradient(145deg, #ffffff 0%, #f8faff 100%) !important;
  border-radius: 24px !important;
  cursor: pointer;
}

.upload-zone-premium:hover {
  background: #f8fafc !important;
  border-color: rgb(var(--v-theme-primary)) !important;
}

.border-dashed-system {
  border: 2px dashed #e2e8f0 !important;
}

.upload-visual {
  display: flex;
  justify-content: center;
}

.icon-stack {
  position: relative;
  width: 100px;
  height: 100px;
  background-color: #f1f5f9;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-zone-premium:hover .icon-stack {
  background-color: white;
}

.sub-icon {
  position: absolute;
  bottom: 15px;
  right: 15px;
  background: white;
  border-radius: 50%;
}

/* Status Card Premium */
.status-card-premium {
  background-color: #ffffff !important;
}

.status-banner {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.bg-success-light {
  background-color: #f0fdf4 !important;
}

.bg-warning-light {
  background-color: #fffbeb !important;
}

.border-bottom {
  border-bottom: 1px solid #f1f5f9;
}

/* Left Side Preview */
.bg-slate-50 {
  background-color: #f8fafc;
}

.bg-preview {
  background-color: #f1f5f9;
}

.preview-icon-box {
  width: 44px;
  height: 44px;
  background-color: #f0f7ff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.document-premium-view {
  width: 100%;
  max-width: 850px;
  min-height: 1123px;
  background-color: #ffffff !important;
  border-radius: 4px !important;
}

.document-content-wrapper {
  padding: 60px;
}

.shadow-2xl {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
}

.border-system {
  border: 1px solid #e2e8f0 !important;
}

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Buttons & Effects */

.btn-hover-effect:hover {
  background-color: #f8fafc;
}

.action-btn-hero {
  letter-spacing: 0.5px !important;
  text-transform: none !important;
}

/* Utilities */
.max-w-600 {
  max-width: 600px;
}

.leading-tight {
  line-height: 1.25;
}

.leading-relaxed {
  line-height: 1.8;
}

.gap-2 {
  gap: 8px;
}

.gap-3 {
  gap: 12px;
}

.gap-4 {
  gap: 16px;
}

.right-panel {
  border-left: 1px solid #e2e8f0;
}

/* Responsive */
@media (max-width: 1279px) {

  /* Changed from 1263px to standard lg breakpoint */
  .order-outputs-premium-page {
    height: auto !important;
    overflow: visible !important;
    min-height: 100vh;
  }

  /* Safe Area for Mobile Scroll */
  .order-outputs-premium-page {
    height: auto !important;
    overflow-y: auto !important;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 0 !important;
  }

  /* Inner containers expend naturally */
  .fill-height {
    height: auto !important;
    display: block !important;
  }

  /* Force content wrapper to be tall and visible */
  .right-panel,
  .border-left-system {
    height: auto !important;
    overflow: visible !important;
  }

  /* Apply padding directly to the scrollable area to prevent overlap */
  /* .flex-grow-1.overflow-y-auto {
    padding-bottom: 250px !important;
  } */

  .preview-viewport,
  .document-content-wrapper {
    padding-bottom: 0 !important;
  }

  .right-panel {
    border-left: none !important;
    border-bottom: 1px solid #e2e8f0;
  }

  .document-content-wrapper {
    padding: 20px;
  }

  .preview-viewport {
    padding: 16px !important;
  }

  /* Disable internal scrolling on mobile, let page scroll */
  .overflow-y-auto {
    overflow-y: visible !important;
    height: auto !important;
    flex-grow: 0 !important;
  }

  /* Compact Mode for Mobile */
  .text-h5 {
    font-size: 1.1rem !important;
  }

  .text-h6 {
    font-size: 1rem !important;
  }

  .text-body-1 {
    font-size: 0.9rem !important;
  }

  .toolbar-premium,
  .preview-header-premium {
    padding: 12px !important;
  }

  .upload-zone-premium {
    padding: 24px !important;
  }

  .icon-stack {
    width: 70px;
    height: 70px;
  }

  .main-icon {
    font-size: 40px !important;
  }

  .sub-icon {
    font-size: 18px !important;
    bottom: 8px;
    right: 8px;
  }

  .action-btn-hero {
    height: 48px !important;
    font-size: 0.95rem !important;
    padding: 0 24px !important;
  }

  .document-premium-view {
    min-height: auto !important;
    /* Allow auto height on mobile preview */
  }

  /* Safe Area for Mobile Scroll */
  .order-outputs-premium-page {
    padding-bottom: 80px !important;
  }
}

@media print {
  .order-outputs-premium-page {
    background: white !important;
    height: auto !important;
    overflow: visible !important;
  }

  .v-col {
    width: 100% !important;
    flex: 0 0 100% !important;
    max-width: 100% !important;
  }

  .toolbar-premium,
  .preview-header-premium,
  .order-lg-1 {
    display: none !important;
  }

  .document-premium-view {
    box-shadow: none !important;
    border: none !important;
  }

  .document-content-wrapper {
    padding: 0 !important;
  }
}
</style>
