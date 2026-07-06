<template>
  <component
    :is="embedded ? 'div' : 'custom-dialog'"
    v-model="dialog"
    :title="$t('groupServicePermission') + '(' + title + ')'"
    width="auto"
    min-width="700"
  >
    <v-card rounded="lg" v-if="loading">
      <v-skeleton-loader type="table" height="300" />
    </v-card>
    <div v-else>
      <!-- صلاحيات الخدمة -->
      <v-sheet
        border
        rounded="lg"
        class="mb-4 pa-3 d-flex align-center justify-space-between bg-grey-lighten-5"
      >
        <div class="d-flex align-center">
          <v-avatar color="primary" variant="tonal" size="40" class="me-3">
            <v-icon>mdi-shield-account-outline</v-icon>
          </v-avatar>
          <div>
            <div class="text-subtitle-1 font-weight-bold">صلاحيات الخدمة</div>
            <div class="text-caption text-medium-emphasis">
              تحكم في وصول المجموعات المختلفة لهذه الخدمة
            </div>
          </div>
        </div>

        <div class="d-flex">
          <v-btn
            color="primary"
            variant="elevated"
            prepend-icon="mdi-check-all"
            @click="selectAllAll"
            class="me-2 rounded-pill"
            elevation="1"
          >
            تحديد الكل
          </v-btn>
          <v-btn
            color="error"
            variant="outlined"
            prepend-icon="mdi-minus-circle-outline"
            @click="deselectAllAll"
            class="rounded-pill"
          >
            إلغاء التحديد
          </v-btn>
        </div>
      </v-sheet>

      <div class="right-add-btn">
        <custom-data-table-with-save
          :="{
            headers: headers,
            getData: getData,
            items: items,
            top: false,
          }"
          :click="
            $perm('add', 'group-service-permission') ||
            $perm('edit', 'group-service-permission')
              ? save
              : null
          "
          :canAdd="true"
        ></custom-data-table-with-save>
      </div>
    </div>
  </component>
</template>

<script>
export default {
  props: {
    modelValue: Boolean,
    service: Object,
    embedded: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      loading: false,
      items: [],
      url: "d-services/group-service-permissions/",
      group_items: [],
    };
  },
  async created() {
    this.group_items = await this.$dataList().Groupes.method();
  },
  computed: {
    dialog: {
      get() {
        return this.modelValue;
      },
      set(val) {
        this.$emit("update:modelValue", val);
      },
    },
    title() {
      return this.service?.name_ar || "";
    },
    headers() {
      const permissions = [
        { key: "create", title: "إنشاء", type: { name: "check" } },
        { key: "start", title: "بدء", type: { name: "check" } },
        { key: "reject", title: "رفض", type: { name: "check" } },
        { key: "cancel", title: "إلغاء", type: { name: "check" } },
        { key: "lock", title: "قفل", type: { name: "check" } },
        { key: "unlock", title: "فتح", type: { name: "check" } },
        { key: "read", title: "قراءة", type: { name: "check" } },
        { key: "update", title: "تعديل", type: { name: "check" } },
        { key: "delete", title: "حذف", type: { name: "check" } },
        { key: "print", title: "طباعة", type: { name: "check" } },
        { key: "complete", title: "تسليم", type: { name: "check" } },
        { key: "assign_grant", title: "تعيين منحة", type: { name: "check" } },
        { key: "reject_grant", title: "رفض منحة", type: { name: "check" } },
        {
          key: "approve_grant",
          title: "موافقة على منحة",
          type: { name: "check" },
        },
        { key: "cancel_grant", title: "إلغاء منحة", type: { name: "check" } },
        { key: "update_grant", title: "تعديل منحة", type: { name: "check" } },
        { key: "add_discount", title: "إضافة خصم", type: { name: "check" } },
        { key: "update_discount", title: "تعديل خصم", type: { name: "check" } },
        { key: "reject_discount", title: "رفض خصم", type: { name: "check" } },
        {
          key: "approve_discount",
          title: "موافقة على خصم",
          type: { name: "check" },
        },
        { key: "cancel_discount", title: "إلغاء خصم", type: { name: "check" } },
        {
          key: "get_input_data",
          title: "جلب بيانات المدخل",
          type: { name: "check" },
        },
        {
          key: "get_output_data",
          title: "جلب بيانات المخرج",
          type: { name: "check" },
        },
        {
          key: "upload_input",
          title: "رفع ملف المدخل",
          type: { name: "check" },
        },
        {
          key: "upload_output",
          title: "رفع ملف المخرج",
          type: { name: "check" },
        },
        {
          key: "delete_input",
          title: "حذف ملف المدخل",
          type: { name: "check" },
        },
        {
          key: "delete_output",
          title: "حذف ملف المخرج",
          type: { name: "check" },
        },
      ];

      return [
        {
          title: this.$t("group"),
          key: "fk_group",
          field: {
            name: "fk_group",
            type: "ForeignKey",
            null: false,
            name_list: "Groupes",
            objects: this.group_items,
            width: "200",
          },
        },
        // {
        //   title: "تحديد الكل",
        //   key: "select_all",
        //   field: (field_data) => ({
        //     name: "select_all",
        //     type: "BooleanField",
        //     update: () => {
        //       const val = field_data.select_all;
        //       permissions.forEach((p) => {
        //         field_data[p.key] = val;
        //         if (!field_data.group_permissions)
        //           field_data.group_permissions = [];
        //         const keyUpper = p.key.toUpperCase();
        //         const index = field_data.group_permissions.indexOf(keyUpper);
        //         if (val) {
        //           if (index === -1) field_data.group_permissions.push(keyUpper);
        //         } else {
        //           if (index !== -1)
        //             field_data.group_permissions.splice(index, 1);
        //         }
        //       });
        //     },
        //   }),
        // },
        ...permissions.map((p) => ({
          title: p.title,
          key: p.key,
          type: p.type,
          field: (field_data) => ({
            name: p.key,
            type: "BooleanField",
            null: true,
            width: "50px",
            update: () => {
              if (!field_data.group_permissions)
                field_data.group_permissions = [];

              const keyUpper = p.key.toUpperCase();
              const index = field_data.group_permissions.indexOf(keyUpper);

              if (field_data[p.key]) {
                // Add if not exists
                if (index === -1) {
                  field_data.group_permissions.push(keyUpper);
                }
              } else {
                // Remove if exists
                if (index !== -1) {
                  field_data.group_permissions.splice(index, 1);
                }
              }
            },
          }),
        })),
      ];
    },
  },
  methods: {
    async getData() {
      if (!this.service?.id) return;
      this.loading = true;
      await this.$axios(`${this.url}`, {
        params: {
          fk_service: this.service?.id,
        },
      })
        .then((response) => {
          this.items = (response.data?.groups ?? []).map((item) => {
            const permissions = item.permissions || [];
            const booleanFields = {};
            permissions.forEach((perm) => {
              booleanFields[perm.toLowerCase()] = true;
            });

            const allSelected =
              permissions.length > 0 && permissions.length === 21;

            return {
              ...item,
              ...booleanFields,
              group_permissions: [...permissions],
              select_all: allSelected,
            };
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    async save() {
      console.log('##################################',this.items);
      const payload = {
        fk_service: this.service.id,
        groups: this.items.map((item) => ({
          fk_group: item.fk_group,
          permissions: item.group_permissions || [],
        })),
      };
      return await this.$axios.post(this.url, payload).then((res) => {
        this.$snack("add", { message: res.data.message });
      });
    },
    selectAllAll() {
      const permissionKeys = [
        "create",
        "start",
        "reject",
        "cancel",
        "lock",
        "unlock",
        "read",
        "update",
        "delete",
        "print",
        "complete",
        "assign_grant",
        "reject_grant",
        "approve_grant",
        "cancel_grant",
        "update_grant",
        "add_discount",
        "update_discount",
        "reject_discount",
        "approve_discount",
        "cancel_discount",
        "get_input_data",
        "get_output_data",
        "upload_input",
        "upload_output",
        "delete_input",
        "delete_output",
      ];
      this.items.forEach((item) => {
        item.select_all = true;
        if (!item.group_permissions) item.group_permissions = [];
        permissionKeys.forEach((key) => {
          item[key] = true;
          const keyUpper = key.toUpperCase();
          if (!item.group_permissions.includes(keyUpper)) {
            item.group_permissions.push(keyUpper);
          }
        });
      });
    },
    deselectAllAll() {
      const permissionKeys = [
        "create",
        "start",
        "reject",
        "cancel",
        "lock",
        "unlock",
        "read",
        "update",
        "delete",
        "print",
        "complete",
        "assign_grant",
        "reject_grant",
        "approve_grant",
        "cancel_grant",
        "update_grant",
        "add_discount",
        "update_discount",
        "reject_discount",
        "approve_discount",
        "cancel_discount",
        "get_input_data",
        "get_output_data",
        "upload_input",
        "upload_output",
        "delete_input",
        "delete_output",
      ];
      this.items.forEach((item) => {
        item.select_all = false;
        item.group_permissions = [];
        permissionKeys.forEach((key) => {
          item[key] = false;
        });
      });
    },
  },
  watch: {
    dialog(val) {
      if (val) {
        this.getData();
      }
    },
    "service.id": {
      handler(val) {
        if (val && this.embedded) {
          this.getData();
        }
      },
      immediate: true,
    },
    "items.length"(val) {
      this.items?.forEach((prerequisite, index) => {
        prerequisite.order = index + 1;
      });
    },
  },
};
</script>

<style scoped>
.right-add-btn :deep(td:has(button)) {
  text-align: start !important;
}
</style>
