<template>
  <v-form>
    <!-- القسم الأساسي -->
    <v-card class="mb-4 elevation-2" rounded="lg">
      <v-card-title class="text-primary d-flex align-center py-3">
        <v-icon class="me-2">mdi-form-textbox</v-icon>
        <span class="text-h6">الخصائص الأساسية</span>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pt-4">
        <v-row dense>
          <v-col cols="12" md="6">
            <v-select
              v-model="localField.type"
              :items="fieldTypes"
              label="نوع الحقل *"
              variant="outlined"
              density="compact"
              hide-details
              prepend-inner-icon="mdi-shape"
              :menu-props="{ zIndex: 3000 }"
              @update:modelValue="onTypeChange"
            ></v-select>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="localField.name"
              label="اسم الحقل (Name) *"
              variant="outlined"
              density="compact"
              hide-details
              prepend-inner-icon="mdi-identifier"
              :rules="[(v) => !!v || 'اسم الحقل مطلوب']"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="localField.label_ar"
              label="التسمية بالعربية *"
              variant="outlined"
              density="compact"
              hide-details
              prepend-inner-icon="mdi-abjad-arabic"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="localField.label_en"
              label="التسمية بالإنجليزية"
              variant="outlined"
              density="compact"
              hide-details
              prepend-inner-icon="mdi-alphabetical"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="localField.placeholder"
              label="النص المساعد (Placeholder)"
              variant="outlined"
              density="compact"
              hide-details
              prepend-inner-icon="mdi-text-box-outline"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="localField.default"
              label="القيمة الافتراضية"
              variant="outlined"
              density="compact"
              hide-details
              prepend-inner-icon="mdi-star-outline"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="4">
            <v-text-field
              v-model.number="localField.cols"
              label="عدد الأعمدة (اختياري)"
              type="number"
              variant="outlined"
              density="compact"
              hide-details="auto"
              prepend-inner-icon="mdi-view-column"
              :min="1"
              :max="12"
              :rules="[
                (v) => !v || (v >= 1 && v <= 12) || 'يجب أن يكون بين 1 و 12',
              ]"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="4">
            <v-text-field
              v-model="localField.group"
              label="اسم المجموعة"
              variant="outlined"
              density="compact"
              hide-details
              prepend-inner-icon="mdi-group"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="4">
            <v-text-field
              v-model="localField.icon"
              label="الأيقونة"
              variant="outlined"
              density="compact"
              hide-details
              prepend-inner-icon="mdi-emoticon-outline"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="localField.hint"
              label="نص التلميح"
              variant="outlined"
              density="compact"
              hide-details
              prepend-inner-icon="mdi-information-outline"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6" class="d-flex align-center gap-4">
            <v-checkbox
              v-model="localField.null"
              label="السماح بقيمة فارغة"
              color="primary"
              density="compact"
              hide-details
              inset
            ></v-checkbox>
            <v-checkbox
              v-model="localField.disabled"
              label="معطل"
              color="warning"
              density="compact"
              hide-details
              inset
            ></v-checkbox>
            <v-checkbox
              v-model="localField.readonly"
              label="للقراءة فقط"
              color="info"
              density="compact"
              hide-details
              inset
            ></v-checkbox>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- خصائص العلاقات (ForeignKey, ManyToMany, OneToOne) -->
    <v-card
      v-if="
        ['ForeignKey', 'ManyToManyField', 'OneToOneField'].includes(
          localField.type
        )
      "
      class="mb-4 elevation-2"
      rounded="lg"
    >
      <v-card-title class="text-info d-flex align-center py-3">
        <v-icon class="me-2">mdi-link-variant</v-icon>
        <span class="text-h6">خصائص العلاقات</span>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pt-4">
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="localField.name_list"
              label="اسم API *"
              variant="outlined"
              density="compact"
              hide-details
              prepend-inner-icon="mdi-api"
              :rules="[(v) => !!v || 'اسم API مطلوب للعلاقات']"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="localField.model"
              label="اسم النموذج (Model)"
              variant="outlined"
              density="compact"
              hide-details
              prepend-inner-icon="mdi-database"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="localField.param"
              label="معامل ديناميكي (Param)"
              variant="outlined"
              density="compact"
              hide-details
              prepend-inner-icon="mdi-variable"
              hint="اسم الحقل الذي يعتمد عليه هذا الحقل"
              persistent-hint
            ></v-text-field>
          </v-col>

          <v-col
            cols="12"
            md="6"
            v-if="
              ['ForeignKey', 'ManyToManyField', 'OneToOneField'].includes(
                localField.type
              )
            "
          >
            <v-checkbox
              v-model="localField.add"
              :default="false"
              label="السماح بالإضافة (Add)"
              color="success"
              density="compact"
              hide-details
              inset
            ></v-checkbox>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- قواعد التحقق -->
    <!-- <v-card class="mb-4 elevation-2" rounded="lg">
      <v-card-title class="text-success d-flex align-center py-3">
        <v-icon class="me-2">mdi-shield-check</v-icon>
        <span class="text-h6">قواعد التحقق</span>
      </v-card-title>
      <v-divider></v-divider>

      <v-card-text class="pt-4">
        <v-row dense>
          <v-col cols="12" md="4">
            <v-checkbox
              value="$required"
              v-model="localField.rules"
              label="حقل مطلوب (Required)"
              color="error"
              density="compact"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col cols="12" md="4">
            <v-checkbox
              value="$email"
              v-model="localField.rules"
              label="بريد إلكتروني (Email)"
              color="primary"
              density="compact"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col cols="12" md="4">
            <v-checkbox
              value="$numeric"
              v-model="localField.rules"
              label="رقمي (Numeric)"
              color="info"
              density="compact"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col cols="12" md="4">
            <v-checkbox
              value="$ar"
              v-model="localField.rules"
              label="نص عربي فقط"
              color="success"
              density="compact"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col cols="12" md="4">
            <v-checkbox
              value="$ar_num"
              v-model="localField.rules"
              label="عربي + أرقام"
              color="success-darken-2"
              density="compact"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col cols="12" md="4">
            <v-checkbox
              value="$en"
              v-model="localField.rules"
              label="نص إنجليزي فقط"
              color="warning"
              density="compact"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col cols="12" md="4">
            <v-checkbox
              value="$en_num"
              v-model="localField.rules"
              label="إنجليزي + أرقام"
              color="warning-darken-2"
              density="compact"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col cols="12" md="4">
            <v-checkbox
              value="$url"
              v-model="localField.rules"
              label="رابط (URL)"
              color="purple"
              density="compact"
              hide-details
            ></v-checkbox>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card> -->

    <!-- الاعتماد على حقول أخرى -->
    <!-- <v-card class="mb-4 elevation-2" rounded="lg">
      <v-card-title class="text-warning d-flex align-center py-3">
        <v-icon class="me-2">mdi-source-branch</v-icon>
        <span class="text-h6">الاعتماد على حقول أخرى</span>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pt-4">
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="localField.depend_field"
              label="اسم الحقل المعتمد عليه"
              variant="outlined"
              density="compact"
              hide-details
              prepend-inner-icon="mdi-link"
              hint="مثال: is_active"
              persistent-hint
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="localField.depend_value"
              label="القيمة المطلوبة"
              variant="outlined"
              density="compact"
              hide-details
              prepend-inner-icon="mdi-equal"
              hint="مثال: true"
              persistent-hint
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card> -->

    <!-- دالة التحديث -->
    <!-- <v-card class="mb-4 elevation-2" rounded="lg">
      <v-card-title class="text-purple d-flex align-center py-3">
        <v-icon class="me-2">mdi-code-braces</v-icon>
        <span class="text-h6">دالة التحديث (Update Callback)</span>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pt-4">
        <v-textarea
          v-model="localField.update_function"
          label="كود JavaScript للتنفيذ عند التحديث"
          variant="outlined"
          rows="4"
          density="compact"
          prepend-inner-icon="mdi-function"
          hint="مثال: if (value) { data.other_field = null; }"
          persistent-hint
          auto-grow
        ></v-textarea>
      </v-card-text>
    </v-card> -->

    <!-- الخصائص الخاصة بنوع الحقل -->
    <v-card
      v-if="currentFieldProperties.length > 0"
      class="mb-4 elevation-2"
      rounded="lg"
    >
      <v-card-title class="text-indigo d-flex align-center py-3">
        <v-icon class="me-2">mdi-cog</v-icon>
        <span class="text-h6">الخصائص الخاصة بنوع الحقل</span>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pt-4">
        <v-row dense>
          <v-col
            v-for="prop in currentFieldProperties"
            :key="prop.key"
            cols="12"
            :md="prop.cols || 6"
          >
            <component
              :is="getPropertyComponent(prop)"
              v-model="localField[prop.key]"
              v-bind="getPropertyProps(prop)"
              @update:modelValue="onPropertyChange(prop.key, $event)"
            ></component>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- خيارات القوائم -->
    <v-card v-if="showOptions" class="mb-4 elevation-2" rounded="lg">
      <v-card-title class="text-teal d-flex align-center py-3">
        <v-icon class="me-2">mdi-format-list-bulleted</v-icon>
        <span class="text-h6">خيارات القائمة</span>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pt-4">
        <v-row dense class="mb-3">
          <v-col cols="12" md="6">
            <v-checkbox
              v-model="localField.is_items_exists"
              label="عناصر موجودة من API"
              color="primary"
              density="compact"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col cols="12" md="6">
            <v-checkbox
              v-model="localField.multiple"
              label="اختيار متعدد"
              color="info"
              density="compact"
              hide-details
            ></v-checkbox>
          </v-col>
        </v-row>

        <template v-if="!localField.is_items_exists">
          <v-divider class="my-3"></v-divider>
          <div class="text-subtitle-2 mb-2 text-grey-darken-2">
            <v-icon size="small" class="me-1">mdi-playlist-edit</v-icon>
            الخيارات المخصصة
          </div>
          <div
            v-for="(option, optIndex) in localField.items"
            :key="optIndex"
            class="d-flex align-center mb-2 gap-2"
          >
            <v-text-field
              v-model="option.value"
              label="القيمة"
              variant="outlined"
              density="compact"
              hide-details
              class="flex-grow-1"
            ></v-text-field>
            <v-text-field
              v-model="option.title"
              label="النص المعروض"
              variant="outlined"
              density="compact"
              hide-details
              class="flex-grow-1"
            ></v-text-field>
            <v-btn
              @click="removeOption(optIndex)"
              color="error"
              size="small"
              icon="mdi-delete"
              variant="tonal"
            ></v-btn>
          </div>
          <v-btn
            @click="addOption"
            color="primary"
            size="small"
            prepend-icon="mdi-plus"
            variant="tonal"
            class="mt-2"
          >
            إضافة خيار
          </v-btn>
        </template>

        <template v-else>
          <v-divider class="my-3"></v-divider>
          <v-text-field
            v-model="localField.name_list"
            label="اسم API *"
            variant="outlined"
            density="compact"
            hide-details
            prepend-inner-icon="mdi-api"
            :rules="[(v) => !!v || 'اسم API مطلوب']"
          ></v-text-field>
        </template>
      </v-card-text>
    </v-card>
  </v-form>
</template>

<script>
import { VSelect, VTextField, VSwitch } from "vuetify/components";
export default {
  name: "FieldEditor",
  props: {
    field: {
      type: Object,
      required: true,
    },
    index: {
      type: Number,
      required: true,
    },
  },
  components: {
    VSelect,
    VTextField,
    VSwitch,
  },
  data() {
    return {
      localField: {
        add: false, // قيمة افتراضية إجبارية false
        ...this.field,
        rules: this.field.rules || [], // تهيئة rules كمصفوفة
      },
      fieldTypes: [
        { title: "نص بطول محدد", value: "CharField" },
        { title: "نص طويل", value: "TextField" },
        { title: "رابط", value: "URLField" },
        { title: "عدد صحيح", value: "IntegerField" },
        { title: "عدد صحيح كبير", value: "BigIntegerField" },
        { title: "عدد صحيح صغير", value: "SmallIntegerField" },
        { title: "عدد صحيح موجب", value: "PositiveIntegerField" },
        { title: "عدد صحيح كبير موجب", value: "PositiveBigIntegerField" },
        { title: "عدد صحيح صغير موجب", value: "PositiveSmallIntegerField" },
        { title: "عدد عشري", value: "FloatField" },
        { title: "عدد عشري دقيق", value: "DecimalField" },
        { title: "تاريخ", value: "DateField" },
        { title: "تاريخ ووقت", value: "DateTimeField" },
        { title: "وقت", value: "TimeField" },
        { title: "مدة زمنية", value: "DurationField" },
        { title: "منطقي", value: "BooleanField" },
        { title: "منطقي مع قيمة فارغة", value: "NullBooleanField" },
        { title: "علاقة", value: "ForeignKey" },
        { title: "علاقة متعددة", value: "ManyToManyField" },
        { title: "علاقة واحد الى واحد", value: "OneToOneField" },
        { title: "ملف", value: "FileField" },
        { title: "صورة", value: "ImageField" },
        // { title: "قائمة", value: "ArrayField" },
        { title: "حقل JSON", value: "JSONField" },
      ],

      // تعريف الخصائص الخاصة بكل نوع حقل
      fieldProperties: {
        CharField: [
          {
            key: "min_length",
            label: "الحد الأدنى للأحرف",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: null,
          },
          {
            key: "max_length",
            label: "الحد الأقصى للأحرف",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: 255,
          },
          {
            key: "pattern",
            label: "نمط regex",
            type: "text",
            component: "v-text-field",
            density: "compact",
          },
          {
            key: "startsWith",
            label: "يجب أن يبدأ بـ",
            type: "text",
            component: "v-text-field",
            density: "compact",
          },
        ],
        IntegerField: [
          {
            key: "min_value",
            label: "الحد الأدنى",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: -2147483648,
          },
          {
            key: "max_value",
            label: "الحد الأقصى",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: 2147483647,
          },
          {
            key: "step",
            label: "خطوة الزيادة",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: 1,
          },
        ],
        BigIntegerField: [
          {
            key: "min_value",
            label: "الحد الأدنى",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: -9223372036854775808,
          },
          {
            key: "max_value",
            label: "الحد الأقصى",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: 9223372036854775808,
          },
          {
            key: "step",
            label: "خطوة الزيادة",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: 1,
          },
        ],
        SmallIntegerField: [
          {
            key: "min_value",
            label: "الحد الأدنى",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: -32768,
          },
          {
            key: "max_value",
            label: "الحد الأقصى",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: 32768,
          },
          {
            key: "step",
            label: "خطوة الزيادة",
            type: "number",
            component: "v-text-field",
            density: "compact",
          },
        ],
        PositiveIntegerField: [
          {
            key: "min_value",
            label: "الحد الأدنى",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: 0,
            disabled: true,
          },
          {
            key: "max_value",
            label: "الحد الأقصى",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: 2147483647,
          },
          {
            key: "step",
            label: "خطوة الزيادة",
            type: "number",
            component: "v-text-field",
            density: "compact",
          },
        ],
        PositiveBigIntegerField: [
          {
            key: "min_value",
            label: "الحد الأدنى",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: 0,
            disabled: true,
          },
          {
            key: "max_value",
            label: "الحد الأقصى",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: 9223372036854775808,
          },
          {
            key: "step",
            label: "خطوة الزيادة",
            type: "number",
            component: "v-text-field",
            density: "compact",
          },
        ],
        PositiveSmallIntegerField: [
          {
            key: "min_value",
            label: "الحد الأدنى",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: 0,
            desabled: true,
          },
          {
            key: "max_value",
            label: "الحد الأقصى",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: 32768,
          },
          {
            key: "step",
            label: "خطوة الزيادة",
            type: "number",
            component: "v-text-field",
            density: "compact",
          },
        ],
        DecimalField: [
          {
            key: "max_digits",
            label: "إجمالي الأرقام",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: 10,
          },
          {
            key: "decimal_places",
            label: "الأرقام العشرية",
            type: "number",
            component: "v-text-field",
            density: "compact",
            default: 2,
          },
          {
            key: "min_value",
            label: "الحد الأدنى",
            type: "number",
            component: "v-text-field",
            density: "compact",
          },
          {
            key: "max_value",
            label: "الحد الأقصى",
            type: "number",
            component: "v-text-field",
            density: "compact",
          },
        ],
        FloatField: [
          {
            key: "min_value",
            label: "الحد الأدنى",
            type: "number",
            component: "v-text-field",
            density: "compact",
          },
          {
            key: "max_value",
            label: "الحد الأقصى",
            type: "number",
            component: "v-text-field",
            density: "compact",
          },
        ],
        EmailField: [
          {
            key: "pattern",
            label: "نمط التحقق",
            type: "text",
            component: "v-text-field",
            density: "compact",
            defaultValue: "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
          },
        ],
        TextField: [
          {
            key: "rows",
            label: "عدد الأسطر",
            type: "number",
            component: "v-text-field",
            density: "compact",
            defaultValue: 3,
          },
          {
            key: "max_length",
            label: "الحد الأقصى للأحرف",
            type: "number",
            component: "v-text-field",
            density: "compact",
          },
          {
            key: "min_length",
            label: "الحد الأدنى للأحرف",
            type: "number",
            component: "v-text-field",
            density: "compact",
          },
          {
            key: "startsWith",
            label: "يجب أن يبدأ بـ",
            type: "text",
            component: "v-text-field",
            density: "compact",
          },
        ],
        select: [
          {
            key: "multiple",
            label: "متعدد الاختيارات",
            type: "boolean",
            component: "v-checkbox",
            density: "compact",
          },
          {
            key: "chips",
            label: "عرض Chips",
            type: "boolean",
            component: "v-checkbox",
            density: "compact",
          },
          {
            key: "clearable",
            label: "قابل للإزالة",
            type: "boolean",
            component: "v-checkbox",
            density: "compact",
          },
        ],
        checkbox: [
          {
            key: "indeterminate",
            label: "حالة غير محددة",
            type: "boolean",
            component: "v-checkbox",
            density: "compact",
          },
        ],
        radio: [
          {
            key: "row",
            label: "عرض أفقي",
            type: "boolean",
            component: "v-checkbox",
            density: "compact",
            defaultValue: true,
          },
        ],
        date: [
          {
            key: "min",
            label: "أقرب تاريخ",
            type: "date",
            component: "v-text-field",
            density: "compact",
          },
          {
            key: "max",
            label: "أبعد تاريخ",
            type: "date",
            component: "v-text-field",
            density: "compact",
          },
        ],
        time: [
          {
            key: "min",
            label: "أقرب وقت",
            type: "time",
            component: "v-text-field",
            density: "compact",
          },
          {
            key: "max",
            label: "أبعد وقت",
            type: "time",
            component: "v-text-field",
            density: "compact",
          },
          {
            key: "format",
            label: "التنسيق",
            type: "select",
            component: "v-select",
            density: "compact",
            items: [
              { title: "24 ساعة", value: "24hr" },
              { title: "12 ساعة", value: "12hr" },
            ],
          },
        ],
        file: [
          {
            key: "multiple",
            label: "متعدد الملفات",
            type: "boolean",
            component: "v-checkbox",
            density: "compact",
          },
          {
            key: "accept",
            label: "أنواع الملفات المقبولة",
            type: "text",
            component: "v-text-field",
            density: "compact",
            hint: "مثال: .pdf,.jpg,.png",
          },
          {
            key: "maxSize",
            label: "الحد الأقصى للحجم (MB)",
            type: "number",
            component: "v-text-field",
            density: "compact",
          },
        ],
        ForeignKey: [
          {
            key: "add",
            label: "السماح بالإضافة",
            type: "boolean",
            component: "v-checkbox",
            defaultValue: false,
          },
        ],
        ManyToManyField: [
          {
            key: "add",
            label: "السماح بالإضافة",
            type: "boolean",
            component: "v-checkbox",
            defaultValue: false,
          },
        ],
        OneToOneField: [
          {
            key: "add",
            label: "السماح بالإضافة",
            type: "boolean",
            component: "v-checkbox",
            defaultValue: false,
          },
        ],
        range: [
          {
            key: "min",
            label: "الحد الأدنى",
            type: "number",
            component: "v-text-field",
            density: "compact",
            defaultValue: 0,
          },
          {
            key: "max",
            label: "الحد الأقصى",
            type: "number",
            component: "v-text-field",
            density: "compact",
            defaultValue: 100,
          },
          {
            key: "step",
            label: "خطوة الزيادة",
            type: "number",
            component: "v-text-field",
            density: "compact",
            defaultValue: 1,
          },
          {
            key: "thumbLabel",
            label: "تسمية الإبهام",
            type: "boolean",
            component: "v-checkbox",
            density: "compact",
            defaultValue: true,
          },
        ],
        color: [
          {
            key: "mode",
            label: "نمط الألوان",
            type: "select",
            component: "v-select",
            density: "compact",
            items: [
              { title: "HEX", value: "hexa" },
              { title: "RGB", value: "rgba" },
              { title: "HSL", value: "hsla" },
            ],
            defaultValue: "hexa",
          },
          {
            key: "dotSize",
            label: "حجم النقطة",
            type: "number",
            component: "v-text-field",
            density: "compact",
            defaultValue: 25,
          },
          {
            key: "swatches",
            label: "عرض الألوان المفضلة",
            type: "boolean",
            component: "v-checkbox",
            density: "compact",
            defaultValue: true,
          },
        ],
        switch: [
          {
            key: "inset",
            label: "نمط داخلي",
            type: "boolean",
            component: "v-checkbox",
            density: "compact",
          },
        ],
        rating: [
          {
            key: "length",
            label: "عدد النجوم",
            type: "number",
            component: "v-text-field",
            density: "compact",
            defaultValue: 5,
          },
          {
            key: "size",
            label: "حجم النجوم",
            type: "number",
            component: "v-text-field",
            density: "compact",
            defaultValue: 24,
          },
          {
            key: "halfIncrements",
            label: "نصف تقييم",
            type: "boolean",
            component: "v-checkbox",
            density: "compact",
          },
        ],
      },
    };
  },
  computed: {
    showOptions() {
      return [
        "CharField",
        "IntegerField",
        "BigIntegerField",
        "SmallIntegerField",
        "PositiveIntegerField",
        "PositiveBigIntegerField",
        "PositiveSmallIntegerField",
      ].includes(this.localField.type);
    },
    showDefaultValue() {
      return !["checkbox", "file", "switch", "rating"].includes(
        this.localField.type
      );
    },
    currentFieldProperties() {
      return this.fieldProperties[this.localField.type] || [];
    },
  },
  watch: {
    localField: {
      handler(newVal) {
        // تحويل الخصائص الرقمية من string إلى number
        const numericProps = [
          "cols",
          "min_length",
          "max_length",
          "min_value",
          "max_value",
          "step",
          "rows",
          "max_digits",
          "decimal_places",
          "maxSize",
        ];

        const cleanedField = { ...newVal };
        numericProps.forEach((prop) => {
          if (
            cleanedField[prop] !== undefined &&
            cleanedField[prop] !== null &&
            cleanedField[prop] !== ""
          ) {
            const numValue = Number(cleanedField[prop]);
            if (!isNaN(numValue)) {
              cleanedField[prop] = numValue;
            }
          }
        });

        // مزامنة القواعد التلقائية (التي لا يتعامل معها مكون Field الأصلي)
        let updatedRules = Array.isArray(cleanedField.rules)
          ? [...cleanedField.rules]
          : [];

        // أداء المزامنة لـ min_length
        updatedRules = updatedRules.filter(
          (r) => typeof r === "string" && !r.startsWith("$min_length:")
        );
        if (cleanedField.min_length) {
          updatedRules.push(`$min_length:${cleanedField.min_length}`);
        }

        // أداء المزامنة لـ startsWith
        updatedRules = updatedRules.filter(
          (r) => typeof r === "string" && !r.startsWith("$startsWith:")
        );
        if (cleanedField.startsWith) {
          updatedRules.push(`$startsWith:${cleanedField.startsWith}`);
        }

        // أداء المزامنة للأنواع الخاصة
        const specialTypeRules = [
          "$IntegerField",
          "$PositiveSmallIntegerField",
        ];
        updatedRules = updatedRules.filter(
          (r) => typeof r === "string" && !specialTypeRules.includes(r)
        );
        if (cleanedField.type === "IntegerField") {
          updatedRules.push("$IntegerField");
        } else if (cleanedField.type === "PositiveSmallIntegerField") {
          updatedRules.push("$PositiveSmallIntegerField");
        }

        // حفظ rules كـ strings للتخزين في JSON
        cleanedField.rules = [...new Set(updatedRules.filter((r) => r))];

        this.$emit("update:field", this.index, cleanedField);
      },
      deep: true,
    },
  },
  methods: {
    onTypeChange() {
      // حفظ القيم المشتركة
      const commonProps = {
        name: this.localField.name,
        label_ar: this.localField.label_ar,
        label_en: this.localField.label_en,
        placeholder: this.localField.placeholder,
        cols: this.localField.cols,
        group: this.localField.group,
        null: this.localField.null,
        default: this.localField.default,
        icon: this.localField.icon,
        hint: this.localField.hint,
        disabled: this.localField.disabled,
        readonly: this.localField.readonly,
        input_type: this.localField.input_type,
        rules: this.localField.rules || [], // مصفوفة قواعد التحقق
        depend_field: this.localField.depend_field,
        depend_value: this.localField.depend_value,
        update_function: this.localField.update_function,
      };

      // إعادة تعيين الحقل مع الحفاظ على الخصائص المشتركة
      const newType = this.localField.type;
      this.localField = {
        ...commonProps,
        type: newType,
        add: false, // قيمة افتراضية إجبارية false عند تغيير النوع
      };

      // إعادة تعيين الخيارات عند تغيير النوع
      if (!this.showOptions) {
        this.localField.items = [];
      }

      // إعادة تعيين الخصائص الخاصة بالنوع الجديد
      this.initializeTypeSpecificProperties();
    },

    initializeTypeSpecificProperties() {
      const typeProps = this.fieldProperties[this.localField.type] || [];
      typeProps.forEach((prop) => {
        this.localField[prop.key] = prop.default;
      });

      // تعيين input_type تلقائياً للحقول الرقمية
      const integerTypes = [
        "IntegerField",
        "BigIntegerField",
        "SmallIntegerField",
        "PositiveIntegerField",
        "PositiveBigIntegerField",
        "PositiveSmallIntegerField",
        "FloatField",
        "DecimalField",
      ];

      if (integerTypes.includes(this.localField.type)) {
        this.localField.input_type = "number";
      } else if (this.localField.type === "DateField") {
        this.localField.input_type = "date";
      } else if (this.localField.type === "TimeField") {
        this.localField.input_type = "time";
      } else if (this.localField.type === "DateTimeField") {
        this.localField.input_type = "datetime-local";
      } else if (this.localField.type === "URLField") {
        this.localField.input_type = "url";
      }
    },

    getPropertyComponent(prop) {
      return prop.component || "v-text-field";
    },

    getPropertyProps(prop) {
      const baseProps = {
        label: prop.label,
        variant: "outlined",
        density: "compact",
        hideDetails: true,
        type: prop.type === "number" ? "number" : "text",
      };

      if (prop.component === "v-select" && prop.items) {
        baseProps.items = prop.items;
      }

      return baseProps;
    },

    onPropertyChange(key, value) {
      this.localField[key] = value;
    },
    addOption() {
      if (!this.localField.items) {
        this.localField.items = [];
      }
      this.localField.items.push({
        title: "",
        value: "",
      });
    },

    removeOption(index) {
      this.localField.items.splice(index, 1);
    },
  },
  created() {
    // التأكد من أن rules مصفوفة reactive
    if (!Array.isArray(this.localField.rules)) {
      this.$set(this.localField, "rules", []);
    }
  },
  mounted() {
    this.initializeTypeSpecificProperties();
  },
};
</script>
