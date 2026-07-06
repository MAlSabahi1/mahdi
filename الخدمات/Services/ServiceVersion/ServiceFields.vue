<template>
    <v-row v-if="processedFields.length > 0">
        <Fields :data="data" :fields="processedFields" :group="true"  />
    </v-row>
</template>

<script>

export default {
    name: "ServiceFields",


    props: {
        data: {
            type: Object,
            required: true,
        },
        fields: {
            type: Array,
            required: true,
            default: () => []
        },

        attrs: {
            type: [Object, String],
            default: () => ({})
        }
    },
    computed: {
        processedFields() {
            return this.processFieldsRules(this.fields);
        },

    },

    methods: {
        getAttrs() {
            if (!this.attrs) return {};
            try {
                // Use Function constructor instead of eval for better security and performance
                // This explicitly passes 'data' to the function scope
                const parser = new Function('data', `return (${this.attrs})`);
                return parser(this.data) ?? {};
            } catch (e) {
                console.error("Error parsing form attributes (attrs):", e);
                return {};
            }
        },

        processFieldsRules(fields) {
            if (!Array.isArray(fields)) return fields;

            return fields.map(field => {
                const processedField = { ...field };

                // تحويل rules من strings إلى functions
                if (Array.isArray(processedField.rules) && processedField.rules.length > 0) {
                    processedField.rules = processedField.rules.map(ruleString => {
                        if (typeof ruleString !== 'string') return ruleString;

                        // التعامل مع القواعد التي تحتوي على بارامترات مثل $min_length:5 أو $startsWith:05
                        let [ruleName, ...args] = ruleString.replace('$', '').split(':');

                        // إرجاع الدالة الفعلية من this (التي تأتي من الـ prototype أو المحقونة عالمياً)
                        if (this[`$${ruleName}`]) {
                            const rule = this[`$${ruleName}`];

                            // إذا كانت الدالة عبارة عن factory (تأخذ بارامترات وتعيد دالة تحقق)
                            if (typeof rule === 'function' && args.length > 0) {
                                // محاولة تحويل الأرقام إذا كانت القيم رقمية
                                const parsedArgs = args.map(arg => isNaN(arg) ? arg : Number(arg));
                                return rule(...parsedArgs);
                            }

                            return rule;
                        }

                        return ruleString;
                    });
                }
                Object.assign(processedField, this.computeFieldAttr(processedField));
                return processedField;
            });
        },

        computeFieldAttr(field) {
            const attr = {};

            // 1. معالجة الاعتماد (depend_field & depend_value)
            if (field.depend_field) {
                if (field?.depend_value) {
                    attr.depend = this.data[field.depend_field] === field.depend_value;
                } else {
                    attr.depend = this.data[field.depend_field];
                }
            } else {
                attr.depend = true;
            }

            // 2. معالجة param للحقول الديناميكية
            if (field.param) {
                attr.param = this.data[field.param];
            }

            // 3. دمج attrs من schema
            const schemaAttrs = this.getAttrs();
            if (schemaAttrs[field.name]) {
                Object.assign(attr, schemaAttrs[field.name]);
            }

            return attr;
        }
    }
};
</script>
