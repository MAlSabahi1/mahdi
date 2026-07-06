<template>
  <!-- <pre dir="ltr">
 {{attr}}
 </pre> -->
  <component ref="componentInput" v-model="value" v-if="shouldRenderField" :is="resolveComponent"
    v-bind="generateFieldProps" :print="print" style="text-align: left !important" />
</template>

<script>

export default {
  props: {
    field: { type: Object, required: {} },
    attr: { type: Object, default: () => ({}) },
    modelValue: {
      type: [Number, String],
      default: null,
    },
  },

  methods: {
    feature(attr) {
      return this.attr[attr];
    },
  },
  computed: {
    field_filter() {
      return {
        ...this.field,
        ...this.attr,
      };
    },
    value: {
      get() {
        if (this.modelValue == null) {
          if (this.field.type === "BooleanField") {
            this.value = this.attr["default"] || this.field.default;
          } else if (this.field.name_list) {
            this.value = this.attr["default"] || this.field.default || this.field.default_val || null;
          } else if (this.field.name_list == null) {
            this.value =
              this.field.default !=
                "<class 'django.db.models.fields.NOT_PROVIDED'>"
                ? this.attr["default"] || this.field.default || null
                : null;
            this.attr["default"] = null;
            this.field.default = null;
          }
        }

        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
    shouldRenderField() {
      if ("depend" in this.attr) return this.attr.depend;
      if ("depend" in this.field) return this.field.depend;

      return true;
    },
    resolveComponent() {
      const is_list = this.field.name_list || this.field.items;
      return (
        {
          JSONField: "custom-text-note",
          CharField: is_list ? "auto-list" : "custom-text-field",
          IntegerField: is_list ? "auto-list" : "custom-text-field",
          DecimalField: "custom-text-field",
          PositiveSmallIntegerField: is_list
            ? "auto-list"
            : "custom-text-field",
          PositiveBigIntegerField: "custom-text-field",
          PositiveIntegerField: "custom-text-field",
          FloatField: "custom-text-field",
          TextField: "custom-text-note",
          ForeignKey: "auto-list",
          OneToOneField: "auto-list",
          BooleanField: "custom-check-box",
          TimeField: "custom-text-field",
          DateField: "custom-text-field",
          DateTimeField: "custom-text-field",
          ImageField: "custom-img",
          FileField: "custom-file",
          ManyToManyField: "auto-list",
        }[this.field.type] || null
      );
    },
    generateFieldProps() {
      const isArabic = this.$i18n.locale === "ar";
      this.field_filter.label =
        this.attr?.label ||
        (isArabic ? this.field_filter.label_ar : this.field_filter.label_en);

      if (this.field.isText) this.field_filter.variant = "text";

      switch (this.field_filter.type) {
        case "TimeField":
          this.field_filter.type = "time";
          break;
        case "PositiveSmallIntegerField":
        case "IntegerField":
        case "PositiveBigIntegerField":
        case "FloatField":
          this.field_filter.type = "number";
          break;
        case "DateField":
          this.field_filter.type = "date";
          break;
        case "DateTimeField":
          this.field_filter.type = "datetime-local";
          break;
        case "ManyToManyField":
          this.field_filter.multiple = true;
          break;
        case "ImageField":
          this.field_filter.width = "200";
          this.field_filter.height = "200";
          break;
        case "FileField":
          if (this.field_filter.null === false)
            this.field_filter.required = true;
          break;
      }

      if (this.attr["items"]) this.field_filter.objects = this.attr["items"];


      var rules = this.attr["rules"]
        ? [...this.generateValidationRules, ...this.attr["rules"]]
        : this.generateValidationRules;

      this.field_filter.rules = rules;

      if (this.field_filter.width > 12)
        this.field_filter.width = this.field_filter.width;
      else if (this.field_filter.width <= 12) {
        this.field_filter.cols =
          this.attr["cols"] || this.field_filter.width || "12";
        this.field_filter.width = null;
      }
      if (this.field_filter.name_list)
        this.field_filter.name = this.field_filter.name_list;


      if (this.field_filter.items && this.field_filter.items?.length > 0) {

        this.field_filter.objects = this.field_filter.items;
      }

      return this.field_filter;
    },

    generateValidationRules() {
      var rules = [];

      if ("rules" in this.field) rules = this.field.rules;
      if ("null" in this.field_filter && !this.field_filter.null) {
        rules.push(this.$required);
      }
      if ("min_value" in this.field_filter && this.field_filter.min_value)
        rules.push(this.$min_value(this.field_filter.min_value));
      if ("max_value" in this.field_filter && this.field_filter.max_value)
        rules.push(this.$max_value(this.field_filter.max_value));
      if ("max_length" in this.field_filter && this.field_filter.max_length)
        rules.push(this.$max_length(this.field_filter.max_length));
      if (this.field_filter.type == "DecimalField")
        rules.push(
          this.$decimal_valid(
            this.field_filter.max_digits,
            this.field_filter.decimal_places
          )
        );
      if (this.field_filter.type == "JSONField") rules.push(this.$validateJson);
      if ("name" in this.field_filter) {
        // if (this.field_filter.name.endsWith("_ar")) rules.push(this.$ar);
        // if (this.field_filter.name.endsWith("_en")) rules.push(this.$en);
        if (this.field_filter.name.includes("phone")) {
          if (this.field_filter.rules) rules.push(this.field_filter.rules);

          rules.push(this.$min_length(6));
          rules.push(this.$max_length(14));

          this.field_filter.type = "number";
        }
      }

      return rules;
    },

    focusFirstElement() {
      this.$refs.componentInput.$el.querySelectorAll(button, [href], input);
    },
  },
  watch: {},
};
</script>
