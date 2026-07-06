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
  <v-sheet class="w-100 border rounded pa-4 pt-0 mt-2">
    <v-tabs
      v-model="tab"
      slider-color="primary"
      color="primary"
      class="border-b text-medium-emphasis"
      variant="solo"
    >
      <v-tab
        value="data"
        prepend-icon="mdi-form-select"
        text="البيانات المرسلة"
        class="elevation-2"
      >
      </v-tab>
      <v-tab
        value="attachments"
        prepend-icon="mdi-file-multiple"
        text="مرفقات الطلب"
        class="elevation-2"
      >
      </v-tab>
      <v-tab
        value="history"
        prepend-icon="mdi-clipboard-text-clock"
        text="سجل اجراءات الطلب"
        class="elevation-2"
      >
      </v-tab>
      <v-tab
        value="comments"
        prepend-icon="mdi-comment-text-multiple"
        text="التعليقات"
        class="elevation-2"
      >
      </v-tab>
    </v-tabs>
    <v-tabs-window v-model="tab">
      <v-tabs-window-item value="data">
        <v-table density="compact" class="border rounded mt-2">
          <thead>
            <tr>
              <th class="font-weight-black">{{ $t("name") }}</th>
              <th class="font-weight-black">{{ $t("data") }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, key) in request.display_data" :key="item">
              <td class="text-medium-emphasis">{{ key }}:</td>
              <td>
                <v-chip-group multiple v-if="typeof item =='object'">
                  <v-chip v-for="tag in item" :key="tag">
                    {{tag}}
                  </v-chip>
                </v-chip-group>
                <span v-else>
                  {{item}}
                </span>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-tabs-window-item>
      <v-tabs-window-item value="attachments">
        <v-card >
          <v-card-text>
            <v-card
              v-for="(file, index) in request?.files"
              :key="index"
              class="pa-2 mb-2 border border-dashed"
            >
              <div class="d-flex justify-space-between align-center">
                <div class="text-medium-emphasis">
                  {{ file.name }}
                </div>
                <v-btn-group variant="outlined" divided density="compact">
                  <v-btn color="primary">
                    <v-icon>mdi-download</v-icon>
                  </v-btn>

                </v-btn-group>
              </div>
            </v-card>
          </v-card-text>
        </v-card>
      </v-tabs-window-item>
      <v-tabs-window-item value="history">
        <v-timeline density="compact" class="mt-4">
          <template v-for="(stage, index) in request.history" :key="index">
            <v-timeline-item size="small" dot-color="primary" icon="mdi-history">
              <v-card class="rounded-lg">
                <v-card-title>
                  <div class="d-flex align-center">
                    <v-avatar
                      variant="tonal"
                      size="30"
                      :color="getStageStyle(1)?.color"
                      class="me-2"
                    >
                      <v-icon>mdi-cog-outline</v-icon>
                    </v-avatar>
                    <div>
                      <div class="text-h6 font-weight-bold me-2">
                        {{ stage.action_name }}
                      </div>
                      <!-- <div class="text-caption">description</div> -->
                    </div>
                    <v-spacer> </v-spacer>
                    <v-chip v-if="stage.stage">
                      {{ stage.stage }}
                    </v-chip>
                  </div>
                </v-card-title>
                <v-card-text>
                  <v-list-item prepend-icon="mdi-account-cog" density="compact">
                    <v-list-item-subtitle>
                      {{ stage.action_by }}
                    </v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item
                    prepend-icon="mdi-clock-outline"
                    density="compact"
                  >
                    <v-list-item-subtitle>
                      <v-chip size="small">
                        {{ stage.created_at }}
                      </v-chip>
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-card-text>
              </v-card>
            </v-timeline-item>
          </template>
        </v-timeline>
      </v-tabs-window-item>
      <v-tabs-window-item value="comments">
        <v-timeline density="compact" class="mt-4">
          <template v-for="(stage, index) in request.history" :key="index">
            <v-timeline-item size="small"  dot-color="primary" icon="mdi-comment-text-multiple">
              <v-card class="rounded-lg">
                <v-card-title>
                  <div class="d-flex align-center">
                    <div>
                      <v-list-item density="compact">
                        <template v-slot:prepend>
                          <v-avatar size="40" variant="tonal">
                            <v-icon color="primary">mdi-account-cog</v-icon>
                          </v-avatar>
                        </template>
                        <v-list-item-title>
                          {{ stage.action_by }}
                        </v-list-item-title>
                        <v-list-item-subtitle>
                          {{ stage.action_by_role }}
                        </v-list-item-subtitle>
                      </v-list-item>
                    </div>
                    <v-spacer> </v-spacer>
                    <v-chip size="small">
                      {{ stage.created_at }}
                    </v-chip>
                  </div>
                </v-card-title>
                <v-card-text>
                  <v-divider></v-divider>
                  <div class="border rounded-lg pa-4 mt-2">
                    {{ stage.comments }}
                  </div>
                </v-card-text>
              </v-card>
            </v-timeline-item>
          </template>
        </v-timeline>
      </v-tabs-window-item>
    </v-tabs-window>
  </v-sheet>
</template>
<script>
export default {
  data() {
    return {
      drawer: false,
      request_id: this.$route.params?.request_id,
      request: {},
      tab: "data",
      stage_styles: {
        1: {
          icon: "mdi-check-circle",
          color: "success",
        },
        2: {
          icon: "mdi-eye",
          color: "primary",
        },
        3: {
          icon: "mdi-bell-ring",
          color: "warning",
        },
        4: {
          icon: "mdi-auto-fiex",
          color: "",
        },
        defaults: {
          icon: "mdi-sitemap",
          color: "grey",
        },
      },
      url: "d-services/services/instances/",
    };
  },
  async created() {
    await this.getRequestServiceDetails();
  },

  methods: {
    // الحصول على بيانات الخدمة
    async getRequestServiceDetails() {
      return await this.$axios(`${this.url}${this.request_id}/details/`).then(
        (response) => (this.request = response.data)
      );
    },



    // الحصول على نمط تصميم المرحلة
    getStageStyle(stage) {
      return this.stage_styles[stage] || this.stage_styles.default;
    },
  },
};
</script>
