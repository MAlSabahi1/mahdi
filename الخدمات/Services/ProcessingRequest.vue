<template>
  <v-card>
    <v-card-title class="py-2">
      <div class="d-flex align-center justify-space-between">
        <div>
          <v-avatar size="40" variant="tonal" class="ml-3">
            <v-icon color="primary">mdi-briefcase-check-outline</v-icon>
          </v-avatar>
          <span class="text-h6 font-weight-bold"> بيانات الطلب</span>
        </div>
        <div>
          <v-icon size="large" color="primary" @click="getRequestServiceDetails()" class="me-2"> mdi-refresh-circle </v-icon>
          <v-chip>
            <span> رقم الطلب# {{ request.id }} </span>
          </v-chip>
        </div>
      </div>
    </v-card-title>
    <v-card-text>
      <v-divider></v-divider>
      <v-list>
        <v-row dense>
          <v-col cols="12" lg="3" md="4" sm="6">
            <v-list-item>
              <template v-slot:prepend>
                <v-avatar variant="tonal" size="small">
                  <v-icon color="primary"> mdi-account </v-icon>
                </v-avatar>
              </template>
              <v-list-item-content>
                <v-list-item-title> مقدم الطلب</v-list-item-title>
                <v-list-item-subtitle>
                  <span class="text-h5">{{ request.requested_by_name }}</span>
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col cols="12" lg="3" md="4" sm="6">
            <v-list-item>
              <template v-slot:prepend>
                <v-avatar variant="tonal" size="small">
                  <v-icon color="primary"> mdi-cog </v-icon>
                </v-avatar>
              </template>
              <v-list-item-content>
                <v-list-item-title>الخدمة</v-list-item-title>
                <v-list-item-subtitle>
                  {{ request.service_name }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col cols="12" lg="3" md="4" sm="6">
            <v-list-item>
              <template v-slot:prepend>
                <v-avatar variant="tonal" size="small">
                  <v-icon color="primary"> mdi-bullseye </v-icon>
                </v-avatar>
              </template>
              <v-list-item-content>
                <v-list-item-title> أولوية الطلب</v-list-item-title>
                <v-list-item-subtitle>
                  <v-chip size="small">
                    {{ request.priority_display }}
                  </v-chip>
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col cols="12" lg="3" md="4" sm="6">
            <v-list-item>
              <template v-slot:prepend>
                <v-avatar variant="tonal" size="small">
                  <v-icon color="primary"> mdi-account-cog </v-icon>
                </v-avatar>
              </template>

              <v-list-item-content>
                <v-list-item-title> المعالج الحالي</v-list-item-title>
                <v-list-item-subtitle>
                  {{
                    request.assigned_to_name
                      ? request.assigned_to_name
                      : "لم يتم اسناد الطلب"
                  }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col cols="12" lg="3" md="4" sm="6">
            <v-list-item>
              <template v-slot:prepend>
                <v-avatar variant="tonal" size="small">
                  <v-icon color="primary"> mdi-check-circle-outline </v-icon>
                </v-avatar>
              </template>
              <v-list-item-title> حالة الطلب</v-list-item-title>
              <v-list-item-subtitle>
                <v-chip size="small">
                  {{ request.status_display }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>
          </v-col>
          <v-col cols="12" lg="3" md="4" sm="6">
            <v-list-item>
              <template v-slot:prepend>
                <v-avatar variant="tonal" size="small">
                  <v-icon color="primary"> mdi-sitemap </v-icon>
                </v-avatar>
              </template>
              <v-list-item-title> المرحلة الحالية</v-list-item-title>
              <v-list-item-subtitle>
                <v-chip size="small">
                  {{ request.current_stage_name }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>
          </v-col>
          <v-col cols="12" lg="3" md="4" sm="6">
            <v-list-item>
              <template v-slot:prepend>
                <v-avatar variant="tonal" size="small">
                  <v-icon color="primary"> mdi-calendar </v-icon>
                </v-avatar>
              </template>
              <v-list-item-title> تاريخ الانشاء</v-list-item-title>
              <v-list-item-subtitle>
                <v-chip size="small">
                  {{ request.created_at }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>
          </v-col>
          <v-col cols="12" lg="3" md="4" sm="6" v-if="request.sla_deadline">
            <v-list-item>
              <template v-slot:prepend>
                <v-avatar variant="tonal" size="small">
                  <v-icon color="primary"> mdi-clock-outline </v-icon>
                </v-avatar>
              </template>
              <v-list-item-title>الموعد النهائي</v-list-item-title>
              <v-list-item-subtitle>
                <v-chip size="small">
                  {{ request.sla_deadline }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>
          </v-col>
        </v-row>
      </v-list>
    </v-card-text>
  </v-card>
  <v-card class="mt-2">
    <v-card-title class="py-2">
      <div class="d-flex align-center justify-space-between">
        <div>
          <v-avatar size="40" variant="tonal" class="ml-3">
            <v-icon color="primary">mdi-cog</v-icon>
          </v-avatar>
          <span class="text-h6 font-weight-bold">اجراءات سير العمل</span>
        </div>
        <div>
          <v-chip>
            {{ request.current_stage_type }}
          </v-chip>
        </div>
      </div>
    </v-card-title>
    <v-divider></v-divider>
    <v-card-text>
      <v-row>
        <v-col cols="12" md="4" sm="4" lg="2">
          <v-tabs
            v-model="tab"
            :direction="$vuetify.display?.xs ? 'horizontal' : 'vertical'"
            class="border-b text-medium-emphasis"
            variant="solo"
          >
            <v-tab
              v-for="action in actions"
              :key="action"
              :value="action.value"
              :prepend-icon="action.icon"
              :text="action.title"
              class="border mb-2"
              :color="action.color"
              :disabled="action.disabled"
            >
            </v-tab>
          </v-tabs>
        </v-col>
        <v-col cols="12" md="8" sm="8" lg="10">
          <v-sheet class="w-100 border rounded pa-4 pt-0 h-100">
            <div class="text-h6 my-2">
              <v-chip color="primary">
                {{ request.current_stage_name }}
              </v-chip>
            </div>
            <v-table density="compact" class="border rounded my-2" v-if="tab">
              <thead>
                <tr>
                  <th class="font-weight-black">{{ $t("name") }}</th>
                  <th class="font-weight-black">{{ $t("data") }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, key) in request.display_data" :key="item">
                  <td class="text-medium-emphasis">{{ key }}:</td>
                  <td>{{ item }}</td>
                </tr>
              </tbody>
            </v-table>
            <v-tabs-window v-model="tab" v-if="tab">
              <v-tabs-window-item class="mt-2" value="approve">
                <v-textarea
                  v-model="data.comment"
                  color="grey"
                  clearable
                  variant="outlined"
                  label="ملاحظات الموافقة على الطلب"
                >
                </v-textarea>
                <v-btn
                  color="success"
                  class="rounded-lg"
                  append-icon="mdi-check-circle"
                  @click="approveRequestService()"
                  :disabled="request?.fk_current_stage_type != 1"
                  >موافقة</v-btn
                >
              </v-tabs-window-item>
              <v-tabs-window-item class="mt-2" value="reject">
                <v-textarea
                  color="error"
                  v-model="data.comment"
                  clearable
                  variant="outlined"
                  label="سبب الرفض"
                >
                </v-textarea>
                <v-btn
                  color="error"
                  class="rounded-lg"
                  append-icon="mdi-cancel"
                  @click="rejectRequestService()"
                  :disabled="request?.fk_current_stage_type != 1"
                  >رفض</v-btn
                >
              </v-tabs-window-item>
              <v-tabs-window-item class="mt-2" value="transfer">
                <v-autocomplete
                  v-model="data.target_user_id"
                  :items="service_users"
                  label="اختر معالج الطلب"
                  item-title="full_name"
                  item-value="id"
                  class="mt-2"
                  density="compact"
                  color="primary"
                  clearable
                  variant="outlined"
                  prepend-inner-icon="mdi-account-cog"
                >
                </v-autocomplete>
                <v-textarea
                  v-model="data.comment"
                  color="primary"
                  clearable
                  variant="outlined"
                  label="ملاحظات التحويل"
                >
                </v-textarea>
                <v-btn
                  color="primary"
                  class="rounded-lg"
                  append-icon="mdi-briefcase-arrow-left-right-outline"
                  @click="transferRequestService()"
                  >تحويل</v-btn
                >
              </v-tabs-window-item>
              <v-tabs-window-item class="mt-2" value="review">
                <v-textarea
                  color="primary"
                  v-model="data.comment"
                  clearable
                  variant="outlined"
                  label="ملاحظات المراجعة"
                >
                </v-textarea>
                <v-btn
                  color="primary"
                  class="rounded-lg"
                  append-icon="mdi-eye"
                  @click="reviewRequestService()"
                  >مراجعة</v-btn
                >
              </v-tabs-window-item>
              <v-tabs-window-item class="mt-2" value="comment">
                <v-textarea
                  color="primary"
                  v-model="data.comment"
                  clearable
                  variant="outlined"
                  label="التعليق"
                >
                </v-textarea>
                <v-btn
                  color="primary"
                  class="rounded-lg"
                  append-icon="mdi-comment-text-multiple"
                  @click="commentRequestService()"
                  >اضافة تعليق</v-btn
                >
              </v-tabs-window-item>
              <v-tabs-window-item class="mt-2" value="notification">
                <v-textarea
                  color="primary"
                  v-model="data.comment"
                  clearable
                  variant="outlined"
                  label="ملاحظات الاشعار"
                >
                </v-textarea>
                <v-btn
                  color="primary  "
                  class="rounded-lg"
                  append-icon="mdi-bell-ring"
                  @click="notificationRequestService()"
                  >اشعار مقدم الطلب</v-btn
                >
              </v-tabs-window-item>
              <v-tabs-window-item class="mt-2" value="return">
                <v-autocomplete
                  v-model="data.target_stage_id"
                  :items="
                    service_stages?.filter(
                      (stage) => stage.id != this.request.fk_current_stage
                    )
                  "
                  label="اختر المرحلة الهدف"
                  item-title="name"
                  item-value="id"
                  class="mt-2"
                  density="compact"
                  color="primary"
                  clearable
                  variant="outlined"
                  prepend-inner-icon="mdi-sitemap"
                >
                </v-autocomplete>
                <v-textarea
                  color="primary"
                  v-model="data.comment"
                  clearable
                  variant="outlined"
                  label="سبب ارجاع الطلب"
                >
                </v-textarea>
                <v-btn
                  color="primary"
                  class="rounded-lg"
                  append-icon="mdi-arrow-u-left-top-bold"
                  @click="returnRequestService()"
                  >ارجاع الطلب</v-btn
                >
              </v-tabs-window-item>
            </v-tabs-window>
            <v-card v-else class="ma-2 pa-6 text-center" flat>
              <v-avatar variant="tonal" color="grey-darken-1" size="70">
                <v-icon size="40"> mdi-cog </v-icon>
              </v-avatar>
              <div class="text-h6 mt-3">لم يتم تحديد الاجراء لهذا الطلب</div>
              <div class="text-body-2 text-grey mt-1">
                الرجاء اختيار احد الاجراءات من القائمة للمتابعة.
              </div>
            </v-card>
          </v-sheet>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>
<script>
export default {
  data() {
    return {
      drawer: false,
      request_id: this.$route.params?.request_id,
      request: {},
      tab: null,
      data: {},
      url: "d-services/services/instances/",
      url_services: "d-services/workflow/services/",
      service_stages: [],
      service_users: [],
    };
  },
  async created() {
    await this.getRequestServiceDetails();
    await this.getRequestServiceStages();
    await this.getUsersHasRquestServiceAccess();
  },

  methods: {
    // الحصول على بيانات الخدمة
    async getRequestServiceDetails() {
      this.request = {}
      return await this.$axios(`${this.url}${this.request_id}/details/`).then(
        (response) => {
          this.tab = undefined;
          this.request = response.data;
        }
      );
    },
    // اعتماد المرحلة الحالية للطلب
    async approveRequestService() {
      return await this.$axios
        .post(`${this.url}${this.request_id}/approve/`, this.data)
        .then((response) => {
          this.$alert("update", { message: response.data });
          this.getRequestServiceDetails();
        });
    },
    // رفض المرحلة الحالية للطلب
    async rejectRequestService() {
      return await this.$axios
        .post(`${this.url}${this.request_id}/reject/`, this.data)
        .then((response) => {
          this.$alert("update", { message: response.data });
          this.getRequestServiceDetails();
        });
    },
    // رفض المرحلة الحالية للطلب
    async transferRequestService() {
      return await this.$axios
        .post(`${this.url}${this.request_id}/transfer/`, this.data)
        .then((response) => {
          this.$alert("update", { message: response.data });
          this.getRequestServiceDetails();
        });
    },
    // مراجعة المرحلة الحالية للطلب
    async reviewRequestService() {
      return await this.$axios
        .post(`${this.url}${this.request_id}/review/`, this.data)
        .then((response) => {
          this.$alert("update", { message: response.data });
          this.getRequestServiceDetails();
        });
    },
    // اشعار على المرحلة الحالية للطلب
    async notificationRequestService() {
      return await this.$axios
        .post(`${this.url}${this.request_id}/acknowledge/`, this.data)
        .then((response) => {
          this.$alert("update", { message: response.data });
          this.getRequestServiceDetails();
        });
    },
    // تعليق على المرحلة الحالية للطلب
    async commentRequestService() {
      return await this.$axios
        .post(`${this.url}${this.request_id}/comment/`, this.data)
        .then((response) => {
          this.$alert("update", { message: response.data });
          this.getRequestServiceDetails();
        });
    },
    // تعليق على المرحلة الحالية للطلب
    async returnRequestService() {
      return await this.$axios
        .post(`${this.url}${this.request_id}/return/`, this.data)
        .then((response) => {
          this.$alert("update", { message: response.data });
          this.data.target_stage_id = null;
          this.getRequestServiceDetails();
        });
    },

    //  الحصول على مرحل سير عمل الطلب
    async getRequestServiceStages() {
      return await this.$axios(
        `${this.url_services}${this.request.fk_service}/workflow-stages/`
      ).then((response) => {
        this.service_stages = response.data;
      });
    },
    //  الحصول على المستخدمين الذين يملكون صلاحيات على الخدمة
    async getUsersHasRquestServiceAccess() {
      return await this.$axios(
        `${this.url}${this.request.id}/users-has-access/`
      ).then((response) => {
        this.service_users = response.data;
      });
    },
  },
  computed: {
    actions() {
      return [
        {
          value: "approve",
          title: "موافقة",
          icon: "mdi-check-circle",
          color: "success",
          disabled: this.request.fk_current_stage_type != 1,
        },
        {
          value: "reject",
          title: this.$t("reject"),
          icon: "mdi-cancel",
          color: "error",
          disabled: this.request.fk_current_stage_type != 1,
        },
        {
          value: "transfer",
          title: "تحويل الطلب",
          icon: "mdi-share-circle",
          color: "primary",
          disabled:
            this.request.fk_current_stage_type != 1 &&
            this.request.fk_current_stage_type != 2,
        },
        {
          value: "review",
          title: this.$t("review"),
          icon: "mdi-eye",
          color: "primary",
          disabled: this.request.fk_current_stage_type != 2,
        },

        {
          value: "comment",
          title: this.$t("comment"),
          icon: "mdi-comment-text-multiple",
          color: "primary",
          disabled: this.request.fk_current_stage_type != 2,
        },
        {
          value: "notification",
          title: "اشعار مقدم الطلب",
          icon: "mdi-bell-ring",
          color: "primary",
          disabled:
            this.request.fk_current_stage_type != 3 &&
            this.request.fk_current_stage_type != 4,
        },
        {
          value: "return",
          title: "ارجاع الطلب",
          icon: "mdi-arrow-u-left-top-bold",
          color: "primary",
          disabled: false,
        },
      ].sort((a, b) => a?.disabled - b?.disabled);
    },
  },
};
</script>
