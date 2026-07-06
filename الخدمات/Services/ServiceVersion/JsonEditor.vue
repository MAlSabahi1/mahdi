<template>
  <!-- المحتوى الرئيسي مع التبويبات -->
  <v-card :elevation="3">

    <v-tabs v-model="currentTab" color="primary" class="border-b" height="64">
      <v-tab value="fields" class="text-none">
        <v-icon start>mdi-form-select</v-icon>
        الحقول المضافة
        <v-chip v-if="fields?.length > 0" size="small" color="primary" class="ml-2">
          {{ fields?.length }}
        </v-chip>
      </v-tab>
      <v-tab value="attributes" class="text-none">
        <v-icon start>mdi-cog</v-icon>
        خصائص الحقول
      </v-tab>
      <v-tab value="preview" class="text-none">
        <v-icon start>mdi-eye</v-icon>
        معاينة النموذج
      </v-tab>

      <v-spacer></v-spacer>

      <div class="d-none d-sm-flex align-center px-4" v-if="fields.length > 0">
        <v-chip size="small" variant="flat" color="info" class="me-2">
          {{ fields.length }} حقول
        </v-chip>
        <v-chip size="small" variant="flat" color="error" v-if="requiredFieldsCount > 0">
          {{ requiredFieldsCount }} مطلوب
        </v-chip>
      </div>


      <v-tab value="json" class="text-none">
        <v-icon start>mdi-code-json</v-icon>
        كود JSON
      </v-tab>
    </v-tabs>

    <v-tabs-window v-model="currentTab">
      <!-- تبويب الحقول -->
      <v-tabs-window-item value="fields">
        <div class="pa-6">
          <!-- حالة العدم (Empty State) -->
          <div v-if="fields?.length === 0" class="empty-state-container py-12">
            <v-alert type="info" variant="outlined" prominent border="top"
              class="max-width-600 mx-auto rounded-xl shadow-sm bg-surface">
              <template v-slot:prepend>
                <div class="pulse-container me-4">
                  <v-icon size="48">mdi-form-select</v-icon>
                </div>
              </template>

              <div class="text-h5 font-weight-bold mb-2">ابدأ بناء نموذجك</div>
              <div class="text-body-1 mb-6 text-grey-darken-1">
                لا توجد حقول مضافة حتى الآن. يمكنك إضافة أنواع مختلفة من الحقول مثل النصوص، الأرقام، التواريخ، والعلاقات
                لتخصيص نموذج
                الخدمة.
              </div>

              <v-btn @click="addNewField" color="primary" size="large" prepend-icon="mdi-plus"
                class="px-8 rounded-pill elevation-2" elevation="2">
                إضافة الحقل الأول
              </v-btn>
            </v-alert>
          </div>

          <div v-else class="fields-container" @dragover="onDragOver" @drop="onDrop">
            <v-expansion-panels v-model="openPanels" multiple variant="accordion">
              <v-expansion-panel v-for="(field, index) in fields" :key="field.index" :value="index" draggable="true"
                @dragstart="onDragStart($event, index)" @dragend="onDragEnd" @dragover="onItemDragOver($event, index)"
                class="mb-3 field-panel" :class="{ dragging: dragItemIndex === index }">
                <v-expansion-panel-title class="py-4">
                  <template v-slot:default>
                    <div class="d-flex align-center w-100">
                      <!-- مقبض السحب -->
                      <v-icon class="handle mr-3 text-grey" size="20">
                        mdi-drag-vertical
                      </v-icon>

                      <!-- معلومات الحقل -->
                      <div class="flex-grow-1">
                        <div class="d-flex align-center mb-1">
                          <h4 class="text-subtitle-1 font-weight-medium me-2">
                            {{ field.label_ar || "حقل بدون اسم" }}
                          </h4>
                          <v-chip size="small" :color="getTypeColor(field.type)" variant="flat" class="ml-2">
                            {{ getTypeLabel(field.type) }}
                          </v-chip>
                          <v-icon v-if="field.required" color="error" size="16" class="ml-2">
                            mdi-asterisk
                          </v-icon>
                        </div>
                        <p class="text-caption text-grey mb-0">
                          {{ field.name || `field_${index + 1}` }}
                        </p>
                      </div>

                      <!-- زر الحذف -->
                      <v-btn @click.stop="removeField(index)" icon="mdi-delete-outline" variant="text" color="error"
                        size="small" class="ml-2"></v-btn>
                    </div>
                  </template>

                  <template v-slot:actions="{ expanded }">
                    <v-icon :color="expanded ? 'primary' : 'grey'"
                      :icon="expanded ? 'mdi-chevron-up' : 'mdi-chevron-down'"></v-icon>
                  </template>
                </v-expansion-panel-title>

                <v-expansion-panel-text class="pt-0">
                  <v-divider class="mb-4"></v-divider>
                  <FieldEditor :field="field" :index="index" @update:field="updateField" />
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
            <v-btn @click="addNewField" color="primary" size="small" icon="mdi-plus" variant="tonal"
              title="اضافة حقل جديد">
            </v-btn>
          </div>
        </div>
      </v-tabs-window-item>

      <!-- تبويب الخصائص -->
      <v-tabs-window-item value="attributes">

        <div class="pa-6">
          <JsonField v-model="attrs" :label="'JS'" :indentation="'تنسيق الكود'" />
        </div>
      </v-tabs-window-item>

      <!-- تبويب المعاينة -->
      <v-tabs-window-item value="preview">
        <div class="pa-6">

          <!-- <FormPreview :fields_schema="{ fields: fields, attrs: attrs }" templateType='form' /> -->
        </div>
      </v-tabs-window-item>

      <!-- تبويب JSON -->
      <v-tabs-window-item value="json">
        <div class="pa-6">
          <div class="d-flex justify-space-between align-center mb-4">
            <h3 class="text-h6">كود JSON للنموذج</h3>
            <div class="d-flex ga-2">
              <v-btn @click="copyJson" prepend-icon="mdi-content-copy" variant="outlined" color="primary"
                class="text-none">
                نسخ
              </v-btn>
              <v-btn @click="downloadJson" prepend-icon="mdi-download" variant="elevated" color="primary"
                class="text-none">
                تحميل
              </v-btn>
            </div>
          </div>

          <v-card variant="outlined" class="overflow-hidden">
            <v-card-text class="pa-0">
              <pre class="json-code pa-4" dir="ltr">{{ jsonOutput }}</pre>
            </v-card-text>
          </v-card>
        </div>
      </v-tabs-window-item>
    </v-tabs-window>
  </v-card>

  <!-- حوار تأكيد الحذف المحسن -->
  <v-dialog v-model="deleteDialog" max-width="450" persistent transition="dialog-bottom-transition">
    <v-card class="rounded-xl overflow-hidden shadow-lg border-0">
      <v-toolbar color="error" flat height="4">
      </v-toolbar>

      <v-card-text class="pa-8 pb-4 text-center">
        <!-- أيقونة تحذير كبيرة -->
        <div class="mb-5 d-flex justify-center">
          <v-avatar color="error-lighten-4" size="90" class="elevation-1">
            <v-icon color="error" size="50" class="animate-shake">mdi-alert-outline</v-icon>
          </v-avatar>
        </div>

        <h3 class="text-h5 font-weight-bold mb-3">هل أنت متأكد؟</h3>
        <p class="text-body-1 text-grey-darken-1 lh-relaxed">
          أنت على وشك حذف الحقل
          <span class="text-error font-weight-bold" v-if="fieldToDelete !== null">
            "{{ fields[fieldToDelete]?.label_ar || fields[fieldToDelete]?.name }}"
          </span>.
          هذا الإجراء لا يمكن التراجع عنه.
        </p>
      </v-card-text>

      <v-card-actions class="pa-8 pt-0 ga-3">
        <v-btn @click="deleteDialog = false" variant="outlined" color="grey-darken-1"
          class="flex-grow-1 py-3 rounded-lg text-none" height="48">
          إلغاء
        </v-btn>
        <v-btn @click="confirmDelete" color="error" variant="elevated"
          class="flex-grow-1 py-3 rounded-lg text-none elevation-4" height="48">
          نعم، احذف
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- الإشعارات المحسنة (Premium Floating Snackbar) -->
  <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="4500" location="bottom center" variant="flat"
    class="premium-snackbar" rounded="pill">
    <div class="d-flex align-center py-1">
      <v-avatar :color="getSnackbarIconBg(snackbar.color)" size="32" class="me-3">
        <v-icon color="white" size="20">{{ getSnackbarIcon(snackbar.color) }}</v-icon>
      </v-avatar>
      <span class="text-subtitle-2 font-weight-medium text-white">{{ snackbar.message }}</span>
    </div>

    <template v-slot:actions>
      <v-btn @click="snackbar.show = false" icon="mdi-close" variant="text" size="x-small" color="white"
        class="me-1"></v-btn>
    </template>
  </v-snackbar>
</template>

<script>


export default {
  name: "JsonEditor",
  props: {
    fields: {
      type: Array,
      default: () => [],
    },
    attrs: {
      type: {},
      default: () => { },
    },
  },
  emits: ["update:fields", "update:attrs"],

  data() {
    return {
      currentTab: "fields",
      openPanels: [],
      nextFieldId: 1,
      dragItemIndex: null,
      dragOverItemIndex: null,
      deleteDialog: false,
      fieldToDelete: null,
      // الإشعارات
      snackbar: {
        show: false,
        message: "",
        color: "success",
      },
      value: null,
    };
  },

  computed: {
    fields: {
      get() {
        return this.fields;
      },
      set(value) {
        this.$emit("update:fields", value);
      },
    },
    attrs: {
      get() {
        return this.attrs;
      },
      set(value) {
        this.$emit("update:attrs", value);
      },
    },
    jsonOutput() {
      return JSON.stringify(this.fields, null, 2);
    },

    requiredFieldsCount() {
      return this.fields.filter((field) => field.required).length;
    },

    fieldTypesCount() {
      return new Set(this.fields.map((field) => field.type)).size;
    },

    validFieldsCount() {
      return this.fields.filter((field) => field.name && field.label).length;
    },
  },

  methods: {
    addNewField() {
      const newField = {
        index: this.nextFieldId++,
        name: `field_${Date.now()}`,
        type: "CharField",
        label_ar: "",
        label_en: "",
        null: false,
        placeholder: "",
        default: "",
      };

      this.fields.push(newField);
      this.openPanels.push(this.fields?.length - 1);
      this.showSnackbar("تم إضافة حقل جديد بنجاح", "success");

      // التبديل إلى تبويب الحقول إذا لم يكن نشطاً
      if (this.currentTab !== "fields") {
        this.currentTab = "fields";
      }
    },

    updateField(index, updatedField) {
      this.fields.splice(index, 1, updatedField);
    },

    removeField(index) {
      this.fieldToDelete = index;
      this.deleteDialog = true;
    },

    confirmDelete() {
      const index = this.fieldToDelete;
      this.fields.splice(index, 1);
      this.openPanels = this.openPanels.filter(
        (panelIndex) => panelIndex !== index
      );
      this.deleteDialog = false;
      this.fieldToDelete = null;
      this.showSnackbar("تم حذف الحقل بنجاح", "success");
    },

    // دوال السحب والإفلات
    onDragStart(event, index) {
      this.dragItemIndex = index;
      event.dataTransfer.effectAllowed = "move";
      event.dataTransfer.setData("text/plain", index.toString());
    },

    onDragOver(event) {
      event.preventDefault();
      event.dataTransfer.dropEffect = "move";
    },

    onItemDragOver(event, index) {
      event.preventDefault();
      this.dragOverItemIndex = index;
    },

    onDrop(event) {
      event.preventDefault();

      if (this.dragItemIndex !== null && this.dragOverItemIndex !== null) {
        this.moveItem(this.dragItemIndex, this.dragOverItemIndex);
        this.showSnackbar("تم إعادة ترتيب الحقول بنجاح", "info");
      }

      this.dragItemIndex = null;
      this.dragOverItemIndex = null;
    },

    onDragEnd() {
      this.dragItemIndex = null;
      this.dragOverItemIndex = null;
    },

    moveItem(fromIndex, toIndex) {
      if (fromIndex === toIndex) return;

      const item = this.fields.splice(fromIndex, 1)[0];
      this.fields.splice(toIndex, 0, item);
      console.log(item);
      // تحديث اللوحات المفتوحة
      const fromPanel = this.openPanels.indexOf(fromIndex);
      if (fromPanel !== -1) {
        this.openPanels.splice(fromPanel, 1);
        this.openPanels.push(toIndex);
      }
    },

    getTypeColor(type) {
      const colors = {
        CharField: "blue",
        TextField: "green",
        URLField: "orange",
        EmailField: "red",
        IntegerField: "purple",
        BigIntegerField: "purple",
        SmallIntegerField: "purple",
        PositiveIntegerField: "purple",
        PositiveBigIntegerField: "purple",
        PositiveSmallIntegerField: "purple",
        FloatField: "deep-orange",
        DecimalField: "pink",
        DateField: "amber",
        DateTimeField: "amber",
        TimeField: "amber",
        DurationField: "amber",
        BooleanField: "brown",
        NullBooleanField: "brown",
        ForeignKey: "indigo",
        ManyToManyField: "indigo",
        OneToOneField: "indigo",
        FileField: "pink",
        ImageField: "pink",
        ArrayField: "cyan",
        JSONField: "cyan",
      };
      return colors[type] || "grey";
    },

    getTypeLabel(type) {
      const labels = {
        CharField: "نص بطول محدد",
        TextField: "نص طويل",
        URLField: "رابط",
        EmailField: "بريد الكتروني",
        IntegerField: "عدد صحيح",
        BigIntegerField: "عدد صحيح كبير",
        SmallIntegerField: "عدد صحيح صغير",
        PositiveIntegerField: "عدد صحيح موجب",
        PositiveBigIntegerField: "عدد صحيح كبير موجب",
        PositiveSmallIntegerField: "عدد صحيح صغير موجب",
        FloatField: "عدد عشري",
        DecimalField: "عدد عشري دقيق",
        DateField: "تاريخ",
        DateTimeField: "تاريخ ووقت",
        TimeField: "وقت",
        DurationField: "مدة زمنية",
        BooleanField: "منطقي",
        NullBooleanField: "منطقي مع قيمة فارغة",
        ForeignKey: "علاقة",
        ManyToManyField: "علاقة متعددة",
        OneToOneField: "علاقة واحد الى واحد",
        FileField: "ملف",
        ImageField: "صورة",
        ArrayField: "قائمة",
        JSONField: "حقل JSON",
      };
      return labels[type] || type;
    },

    getSnackbarIcon(color) {
      const icons = {
        success: "mdi-check-circle",
        error: "mdi-alert-octagon",
        warning: "mdi-alert-outline",
        info: "mdi-information-outline",
      };
      return icons[color] || "mdi-information";
    },

    getSnackbarIconBg(color) {
      const bgs = {
        success: "rgba(255,255,255,0.15)",
        error: "rgba(255,255,255,0.15)",
        warning: "rgba(255,255,255,0.15)",
        info: "rgba(255,255,255,0.15)",
      };
      return bgs[color] || "rgba(255,255,255,0.15)";
    },

    resetFields() {
      this.fields = [];
      this.openPanels = [];
      this.nextFieldId = 1;
      this.showSnackbar("تم إعادة تعيين جميع الحقول", "warning");
    },

    copyJson() {
      try {
        navigator.clipboard.writeText(this.jsonOutput);
        this.showSnackbar("تم نسخ JSON إلى الحافظة", "success");
      } catch (error) {
        this.showSnackbar("فشل في نسخ JSON", "error");
      }
    },

    downloadJson() {
      try {
        const blob = new Blob([this.jsonOutput], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `form-fields-${new Date().toISOString().split("T")[0]
          }.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        this.showSnackbar("تم تحميل ملف JSON", "success");
      } catch (error) {
        this.showSnackbar("فشل في تحميل الملف", "error");
      }
    },



    showSnackbar(message, color) {
      this.snackbar.message = message;
      this.snackbar.color = color;
      this.snackbar.show = true;
    },
  },


};
</script>

<style scoped>
.handle {
  cursor: grab;
}

.handle:active {
  cursor: grabbing;
}

.fields-container {
  min-height: 200px;
  position: relative;
}

.field-panel {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.field-panel:hover {
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.08);
}

.field-panel.dragging {
  opacity: 0.4;
  transform: scale(0.98);
  border: 2px dashed rgb(var(--v-theme-primary));
}

.pulse-container {
  background: rgba(var(--v-theme-info), 0.1);
  border-radius: 50%;
  padding: 16px;
  animation: pulse-animation 2s infinite;
}

@keyframes pulse-animation {
  0% {
    box-shadow: 0 0 0 0 rgba(var(--v-theme-info), 0.4);
  }

  70% {
    box-shadow: 0 0 0 20px rgba(var(--v-theme-info), 0);
  }

  100% {
    box-shadow: 0 0 0 0 rgba(var(--v-theme-info), 0);
  }
}

.max-width-600 {
  max-width: 600px;
}

.empty-state-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.json-code {
  font-family: "Cascadia Code", "Fira Code", "Monaco", monospace;
  font-size: 13px;
  line-height: 1.6;
  background-color: #1e1e1e;
  color: #d4d4d4;
  border-radius: 8px;
  max-height: 500px;
  overflow-y: auto;
}

/* Custom Scrollbar */
.json-code::-webkit-scrollbar {
  width: 8px;
}

.json-code::-webkit-scrollbar-track {
  background: #252526;
}

.json-code::-webkit-scrollbar-thumb {
  background: #37373d;
  border-radius: 4px;
}

.json-code::-webkit-scrollbar-thumb:hover {
  background: #46464d;
}

/* Animations */
.v-tabs-window-item {
  transition: all 0.4s ease-in-out;
}

.shadow-sm {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
}

.premium-snackbar {
  margin-bottom: 24px;
}

.premium-snackbar :deep(.v-snackbar__content) {
  padding: 8px 16px !important;
  /* backdrop-filter: blur(8px); */
  background: rgba(var(--v-theme-surface-variant), 0.95);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15) !important;
}

.animate-shake {
  animation: shake 0.8s cubic-bezier(.36, .07, .19, .97) both;
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
  perspective: 1000px;
}

@keyframes shake {

  10%,
  90% {
    transform: translate3d(-1px, 0, 0);
  }

  20%,
  80% {
    transform: translate3d(2px, 0, 0);
  }

  30%,
  50%,
  70% {
    transform: translate3d(-4px, 0, 0);
  }

  40%,
  60% {
    transform: translate3d(4px, 0, 0);
  }
}

.lh-relaxed {
  line-height: 1.6;
}

.shadow-lg {
  box-shadow: 0 15px 50px -12px rgba(0, 0, 0, 0.25) !important;
}
</style>
