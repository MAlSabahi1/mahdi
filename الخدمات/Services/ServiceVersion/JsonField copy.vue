<template>
  <div class="json-field-container">
    <v-textarea
      v-model="value"
      :label="label"
      auto-grow
      rows="10"
      color="yellow-darken-3"
      variant="outlined"
      :error-messages="errorMessages"
      @blur="validateAndEmit"
      :readonly="readonly"
      spellcheck="false"
      class="json-textarea"
    />
  </div>
</template>

  <script>
/**
 * Vue component for editing and validating JavaScript Object Literal data with expressions.
 * It performs syntax validation but emits the raw input string, suitable for storage in a database.
 * NOTE: This component uses Function constructor for parsing, which is powerful but should be used with caution.
 */
export default {
  name: "JsRawExpressionField",

  props: {
    /**
     * The raw JavaScript Object Literal string to be edited.
     */
    modelValue: {
      type: String,
      default: () => null,
    },
    /**
     * The label for the textarea.
     */
    label: {
      type: String,
      default: "JavaScript Object with Expressions (Raw String)",
    },
    /**
     * The number of spaces to use for indentation when formatting the output JSON.
     */
    indentation: {
      type: Number,
      default: 2,
      validator: (val) => val >= 0 && val <= 10, // Indentation should be between 0 and 10
    },
    /**
     * If true, the textarea and button will be disabled.
     */
    readonly: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
    // No need to watch indentation here, as we don't auto-format the raw string
  },

  methods: {
    /**
     * Safely stringifies a JavaScript value into a JSON string.
     * @param {any} value - The value to stringify.
     * @param {number} indent - The number of spaces to use for indentation.
     * @returns {string} The JSON string.
     */
    safeStringify(value, indent) {
      try {
        if (value === null || value === undefined) {
          return "";
        }
        return JSON.stringify(value, null, indent);
      } catch (e) {
        console.error("Error during JSON stringify:", e);
        return "";
      }
    },

    /**
     * Parses the JavaScript Object Literal string using the Function constructor for syntax check.
     * It injects a mock 'data' object to prevent runtime errors from missing variables.
     * @param {string} jsString - The input string.
     * @returns {object} The parsed JavaScript object (evaluated with mock data).
     */
    parseJsObject(jsString) {
      const trimmedString = jsString.trim();
      if (!trimmedString) return {};

      // Mock object to prevent ReferenceErrors for common variables like 'data'
      // We use a Proxy to catch any property access and return undefined,
      // which allows optional chaining (?. ) to work without throwing.
      const mockData = new Proxy(
        {},
        {
          get: (target, prop) => {
            // Allow access to common methods like 'includes' on a mock object
            if (prop === "includes") return () => false;
            // Return a mock object for deep access
            return mockData;
          },
        }
      );

      // Wrap the input string in parentheses to ensure it's treated as an expression
      // and use the Function constructor to execute it.
      const code = `return (${trimmedString})`;

      // Function constructor with 'data' as an argument
      const func = new Function("data", code);

      // Execute the function with the mock object
      return func(mockData);
    },

    /**
     * Validates the internal string for syntax, updates error messages, and emits the raw string if valid.
     */
    validateAndEmit() {
      const jsString = this.value;

      try {
        // 1. Perform Syntax Check: Parse the JS object literal with mock data

        const parsed = this.parseJsObject(jsString);

        // 2. STRICT OBJECT VALIDATION
        // Must be an object, not null, and not an array (to ensure the structure is an object literal)
        if (
          typeof parsed !== "object" ||
          parsed === null ||
          Array.isArray(parsed)
        ) {
          throw new Error(
            "Input must be a valid JavaScript Object Literal ({}). Arrays, strings, numbers, and null are not allowed."
          );
        }

        // Clear errors on successful parse and validation
        this.errorMessages = [];

        // 3. Emit the raw string back to the parent component
        this.$emit("update:modelValue", jsString);
      } catch (e) {
        // Set error message on failure
        let errorMessage = "Invalid JavaScript Object Literal or Expression.";
        if (
          e.message.includes("Input must be a valid JavaScript Object Literal")
        ) {
          errorMessage = e.message;
        } else {
          // For Function constructor errors, show the error message
          errorMessage = "Syntax Error: " + e.message;
        }
        this.errorMessages = [errorMessage];
        // Do NOT emit on invalid input
      }
    },
  },
};
</script>

  <style scoped>
.json-textarea * {
  font-family: "Fira Code", "Consolas", monospace !important;
  font-size: 14px;
}
/* Force LTR direction and left alignment for code/JSON in RTL layouts */
.json-textarea :deep(textarea) {
  text-align: left !important;
  direction: ltr !important;
}
</style>
