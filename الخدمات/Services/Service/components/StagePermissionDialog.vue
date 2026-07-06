<template>
  <component
    :is="embedded ? 'div' : 'custom-dialog'"
    v-model="dialog"
    :title="$t('stage_permissions') + '(' + title + ')'"
    width="auto"
    min-width="700"
  >
    <v-card rounded="lg" v-if="loading">
      <v-skeleton-loader type="table" height="300" />
    </v-card>
    <div v-else>
      <!-- صلاحيات المراحل -->
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
            <div class="text-subtitle-1 font-weight-bold">
              {{ $t("stage_permissions") }}
            </div>
            <div class="text-caption text-medium-emphasis">
              تحكم في وصول الصلاحيات المختلفة لهذه المرحلة
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
      <auto-list
        v-model="filter.service_workflow_steps"
        name="ServiceWorkflowSteps"
        cols="3"
        :param="service.id"
        :add="false"
        :rules="[$required]"
        @update:modelValue="getData"
      />
      <div
        :class="{
          'disabled-row': !filter.service_workflow_steps,
        }"
      >
        <custom-data-table-with-save
          :="{
            headers: headers,
            getData: getData,
            items: items,
            top: false,
          }"
          :click="
            $perm('add', 'stage-permission') ||
            $perm('edit', 'stage-permission')
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
import dataList from '@/utils/DataAutoList';
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
      user_perms: {},
      url: "d-services/stage-permissions/",
      user_items: [],
      filter: {},
    };
  },
  async created() {
    // if(this.service?.id)
    // this.user_items = await dataList(this.service.id).AccessServiceUsers.method();
    this.user_items = await dataList().User.method();
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
        { key: "start", title: "بدء", type: { name: "check" } },
        { key: "approve", title: "موافقة", type: { name: "check" } },
        { key: "execute", title: "تنفيذ", type: { name: "check" } },
        {
          key: "input",
          title: "طباعه ورفع الاستمارة",
          type: { name: "check" },
        },
        { key: "output", title: "طباعه ورفع المخرج", type: { name: "check" } },
        { key: "reject", title: "رفض", type: { name: "check" } },
        { key: "cancel", title: "إلغاء", type: { name: "check" } },
        { key: "complete", title: "تسليم", type: { name: "check" } },
        {
          key: "checklist_add",
          title: "إضافة عنصر للقائمة",
          type: { name: "check" },
        },
        {
          key: "checklist_delete",
          title: "حذف عنصر من القائمة",
          type: { name: "check" },
        },
        {
          key: "checklist_check",
          title: "تحقق من عنصر",
          type: { name: "check" },
        },
        {
          key: "checklist_uncheck",
          title: "إلغاء تحقق من عنصر",
          type: { name: "check" },
        },
        {
          key: "advance",
          title: "الانتقال الى الخطوة التالية",
          type: { name: "check" },
        },
        {
          key: "return",
          title: "ارجاع الى الخطوة السابقة",
          type: { name: "check" },
        },
      ];

      return [
        {
          title: this.$t("action_by_name"),
          key: "fk_user",
          field: {
            name: "user",
            type: "ForeignKey",
            null: false,
            name_list: "User",
            objects: this.user_items,
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
        //         if (!field_data.user_permissions)
        //           field_data.user_permissions = [];
        //         const keyUpper = p.key.toUpperCase();
        //         const index = field_data.user_permissions.indexOf(keyUpper);
        //         if (val) {
        //           if (index === -1) field_data.user_permissions.push(keyUpper);
        //         } else {
        //           if (index !== -1)
        //             field_data.user_permissions.splice(index, 1);
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
            update: () => {
              if (!field_data.user_permissions)
                field_data.user_permissions = [];

              const keyUpper = p.key.toUpperCase();
              const index = field_data.user_permissions.indexOf(keyUpper);

              if (field_data[p.key]) {
                // Add if not exists
                if (index === -1) {
                  field_data.user_permissions.push(keyUpper);
                }
              } else {
                // Remove if exists
                if (index !== -1) {
                  field_data.user_permissions.splice(index, 1);
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
      if (this.filter.service_workflow_steps) {
        if (!this.service?.id) return;
        this.loading = true;
        await this.$axios(`${this.url}`, {
          params: {
            fk_workflow_step: this.filter?.service_workflow_steps,
          },
        })
          .then((response) => {
            this.items = (response.data?.users ?? []).map((user) => {
              const permissions = user.permissions || [];
              const booleanFields = {};
              permissions.forEach((perm) => {
                booleanFields[perm.toLowerCase()] = true;
              });

              const allSelected =
                permissions.length > 0 && permissions.length === 8;

              return {
                ...user,
                ...booleanFields,
                user_permissions: [...permissions],
                select_all: allSelected,
              };
            });
          })
          .finally(() => {
            this.loading = false;
          });
      }
    },
    async save() {
      const payload = {
        fk_workflow_step: this.filter?.service_workflow_steps,
        users: this.items.map((item) => ({
          fk_user: item.fk_user,
          permissions: item.user_permissions || [],
        })),
      };
      return await this.$axios.post(this.url, payload).then((res) => {
        this.$alert("add", { message: res.data });
      });
    },
    selectAllAll() {
      const permissionKeys = [
        "start",
        "approve",
        "execute",
        "input",
        "output",
        "reject",
        "cancel",
        "complete",
        "checklist_add",
        "checklist_delete",
        "checklist_check",
        "checklist_uncheck",
        "advance",
        "return",
      ];
      this.items.forEach((item) => {
        item.select_all = true;
        if (!item.user_permissions) item.user_permissions = [];
        permissionKeys.forEach((key) => {
          item[key] = true;
          const keyUpper = key.toUpperCase();
          if (!item.user_permissions.includes(keyUpper)) {
            item.user_permissions.push(keyUpper);
          }
        });
      });
    },
    deselectAllAll() {
      const permissionKeys = [
        "start",
        "approve",
        "execute",
        "input",
        "output",
        "reject",
        "cancel",
        "complete",
        "checklist_add",
        "checklist_delete",
        "checklist_check",
        "checklist_uncheck",
        "advance",
        "return",
      ];
      this.items.forEach((item) => {
        item.select_all = false;
        item.user_permissions = [];
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
      } else {
        this.filter.service_workflow_steps = null;
        this.items = [];
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
  },
};
</script>
