<template>
  <!-- Header/Title (Optional, can be inside a fieldset or just a title) -->
  <v-alert
    v-if="service_schema.name_ar"
    class="mb-2"
    border="start"
    variant="tonal"
    color="primary"
  >
    <div class="text-h6">{{ service_schema.name_ar }}</div>
    <div class="text-caption">{{ service_schema.description_ar }}</div>
  </v-alert>

  <v-card elevation="0" class="card border ma-n2">
    <v-card-title class="bg-primary text-white py-3 px-4">
      <div class="d-flex flex-wrap align-center justify-space-between">
        <div class="d-flex align-center">
          <v-icon start> mdi-file-document-edit</v-icon>
          <span class="text-subtitle-1 font-weight-bold">{{
            `نموذج طلب خدمة - ${service_schema?.fk_service__name} `
          }}</span>
          <v-chip size="small" density="compact" class="ms-1">
            <span class="text-caption">{{ service_schema.fk_service__code }}</span>
          </v-chip>
        </div>
        <div class="d-flex align-center flex-wrap" style="gap: 16px; font-size: 0.85rem">
          <v-chip size="small" density="compact" class="py-3">
            <span class="text-caption me-1">رقم الطلب: </span>
            <span>{{ service_schema.next_request_number }}</span>
          </v-chip>
          <div class="d-flex align-center">
            <v-icon class="me-1" size="small" color="grey-lighten-1">mdi-calendar</v-icon>
            <span>{{ service_schema.request_date?.split("T")[0] }}</span>
          </div>
          <div class="d-flex align-center">
            <v-icon class="me-1" size="small" color="grey-lighten-1"
              >mdi-clock-outline</v-icon
            >
            <span>{{
              new Date(service_schema.request_date)?.toLocaleString("en-US", {
                hour: "numeric",
                minute: "2-digit",
                hour12: true,
              })
            }}</span>
          </div>
          <back-to class="bg-white" @click="$router.back()" />
        </div>
      </div>
    </v-card-title>

    <v-card-text class="pa-3 card_content">
      <VAlert border="start" variant="tonal" color="primary" closable v-if="request_id">
        <div>ملاحظة التعديل</div>
        <div class="text-caption">لا يمكن التعديل الا على بيانات الخدمة</div>
      </VAlert>

      <!-- Service Information Section -->

      <!-- Applicant Info Section -->
      <v-card flat :disabled="request_id">
        <filter-fields
          v-if="service_schema?.target_audience_schema?.fields"
          :label="'فئة الجمهور المستهدف'"
          prependIcon="mdi-account-group-outline"
          class="px-5 pt-3"
        >
          <v-skeleton-loader
            v-if="loading_schema"
            type="list-item-two-line"
          ></v-skeleton-loader>
          <v-form ref="audience_form" v-else>
            <!-- Target Audience -->

            <v-row
              dense
              v-if="service_schema?.target_audience_schema?.fields?.length > 0"
            >
              <fields
                :data="selected_service.target_audience_data"
                :fields="service_schema?.target_audience_schema?.fields ?? []"
                :attr="
                  service_schema?.target_audience_schema?.attrs(
                    selected_service?.target_audience_data
                  )
                "
                :group="true"
              >
                <!-- this.getAttrs(
                  this.selected_service?.target_audience_data || {},
                  service_schema?.target_audience_schema?.attrs ?? '{}'
                ) -->
              </fields>
            </v-row>
          </v-form>
        </filter-fields>
      </v-card>

      <!-- Service Data Section -->

      <filter-fields
        prependIcon="mdi-cog-outline"
        PHIcon="mdi-database-off-outline"
        :style="{ 'max-height: 200px': service_schema.component_type }"
        :placeholder="!service_schema.component_type"
        :PHText="$t('no_service_data')"
        :label="'بيانات الخدمة'"
      >
        <v-skeleton-loader v-if="loading_schema" type="article"></v-skeleton-loader>
        <template v-else>
          <v-form ref="service_form" v-if="service_schema.component_type == 'form'">
            <!-- Form Type -->

            <v-row>
              <fields
                :data="selected_service.version_data"
                :fields="service_schema?.version_schema?.fields ?? []"
                :attr="
                  service_schema?.version_schema?.attrs(
                    Object?.assign(selected_service?.version_data, {
                      ...selected_service?.target_audience_data,
                    })
                  )
                "
                :group="true"
              >
              </fields>
            </v-row>
          </v-form>
          <!-- Wizard Type -->
          <VStepper
            complete-icon="mdi-check"
            v-model="step_index"
            class="border mx-2"
            flat
            v-if="service_schema.component_type == 'wizard'"
            @click.prevent
          >
            <VStepperItem
              v-for="(step, index) in service_schema?.version_schema ?? []"
              :key="index"
              :title="step.title"
              :value="index"
              editable
              :icon="step.icon"
              class="elevation-1"
              color="primary"
              :error="form_valid[index] === false"
            >
            </VStepperItem>

            <VStepperWindow>
              <template
                v-for="(step, index) in service_schema?.version_schema ?? []"
                :key="index"
              >
                <v-form ref="service_form" v-model="form_valid[index]">
                  <VStepperWindowItem :value="index" eager>
                    <v-row>
                      <fields
                        :fields="step.fields"
                        :data="selected_service.version_data"
                        :attr="
                          step?.attrs(
                            Object?.assign(selected_service?.version_data, {
                              ...selected_service?.target_audience_data,
                            })
                          )
                        "
                        :group="true"
                      ></fields>
                    </v-row>
                  </VStepperWindowItem>
                </v-form>
              </template>
            </VStepperWindow>
          </VStepper>
        </template>
      </filter-fields>

      <!-- Attachments -->
      <v-card flat :disabled="request_id">
        <filter-fields :label="'مرفقات الطلب'" prependIcon="mdi-paperclip">
          <template v-slot>
            <div class="pa-2 w-80">
              <file-uploader v-model="attachments_list"></file-uploader>
            </div>
            <!-- Attachments List -->
            <!--<v-form ref="attachments_form">
              <v-row
                v-for="(attachment, index) in attachments_list"
                :key="index"
                class="mb-2 align-center"
              >
                <v-col cols="12" md="3">
                  <v-text-field
                    v-model="attachment.name"
                    label="اسم المرفق"
                    :rules="[$required, $max_length(255)]"
                    variant="outlined"
                    density="compact"
                    hide-details
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="4">
                  <v-file-input
                    v-model="attachment.file"
                    label="الملف"
                    :rules="[$required]"
                    variant="outlined"
                    density="compact"
                    hide-details
                    prepend-icon=""
                    prepend-inner-icon="mdi-paperclip"
                  ></v-file-input>
                </v-col>
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="attachment.description"
                    :rules="[$max_length(1000)]"
                    label="الوصف"
                    variant="outlined"
                    density="compact"
                    hide-details
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="1" class="text-center">
                  <v-btn
                    icon="mdi-delete"
                    color="error"
                    variant="text"
                    size="small"
                    @click="removeAttachment(index)"
                  ></v-btn>
                </v-col>
              </v-row> -->
            <!-- Add Button -->
            <!-- <v-row>
                <v-col cols="12">
                  <v-btn
                    color="primary"
                    variant="tonal"
                    prepend-icon="mdi-plus"
                    @click="addAttachment"
                    size="small"
                  >
                    إضافة مرفق
                  </v-btn>
                </v-col>
              </v-row> -->
            <!-- Existing Attachments (if editing) -->
            <!-- <fieldset class="pa-2 border rounded mt-4" v-if="request_id">
                <legend class="px-4">المرفقات المتواجدة حاليا</legend>
                <view-request-attachments :request_id="request_id" />
              </fieldset> -->
            <!-- <v-alert type="info" variant="text" density="compact" class="mt-2">
                * ملاحظة: يمكن إضافة أكثر من مرفق
              </v-alert>
            </v-form>-->
          </template>
        </filter-fields>
      </v-card>
      <!-- Base Audience -->
      <!-- <v-card flat :disabled="request_id">
        <filter-fields :label="'البيانات الاساسية'" prependIcon="mdi-school-outline">
          <v-skeleton-loader v-if="loading_schema" type="table-row@3"></v-skeleton-loader>
          <v-form ref="form" v-else>
            <v-row>
              <v-col
                cols="12"
                v-if="service_schema?.base_audience_schema?.fields?.length > 0"
              >
                <v-row dense>
                  <fields
                    :data="selected_service.base_component_data"
                    :fields="service_schema?.base_audience_schema?.fields ?? []"
                    :attr="
                      service_schema?.base_audience_schema?.attrs(
                        selected_service?.base_component_data
                      )
                    "
                    :group="true"
                  >
                  </fields>
                </v-row>
              </v-col>
            </v-row>
          </v-form>
        </filter-fields>
      </v-card> -->
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn @click="clearRequestService" variant="tonal" class="ms-2">مسح</v-btn>
      <custom-btn
        type="save"
        density="default"
        class="ms-2 rounded-lg"
        append-icon="mdi-send mdi-rotate-180"
        :click="saveServiceRequest"
        :loading="loading"
        >طلب</custom-btn
      >
    </v-card-actions>
  </v-card>
</template>

<script>
import dataList from "@/utils/DataAutoListPortal";
export default {
  data() {
    return {
      fk_service: this.$route.params?.fk_service,
      test: null,
      selected_service: {
        fk_service: null,
        version_data: {},
        target_audience_data: {},
        base_component_data: {},
        attachments: [], // Re-adding for v-model
      },
      service_schema: {},
      form_valid: [],
      valid: false,
      step_index: 0,
      request_id: this.$route.query?.request_id,
      url_schema: "d-services/service-schema/",
      url_request_service: "d-services/service-requests/",
      loading: false, // For submit button state
      loading_schema: false,

      // Attachment
      attachments_list: [],

      attrsData: {},
    };
  },
  async created() {
    this.selected_service.fk_service =
      Number(this.$route.params?.fk_service || this.$route.query?.fk_service) || null;

    if (this.request_id) {
      await this.getRequestService();
    }

    if (this.selected_service.fk_service) {
      await this.getServiceSchema();
    }
  },
  methods: {
    setAttrs(ser_schema) {
      if (ser_schema?.target_audience_schema) {
        this.service_schema.target_audience_schema.attrs = this.getAttrs(
          this.selected_service?.target_audience_data,
          ser_schema?.target_audience_schema?.attrs,
          ser_schema?.target_audience_schema
        );
      }
      if (ser_schema?.version_schema) {
        if (Array.isArray(ser_schema?.version_schema)) {
          ser_schema?.version_schema?.forEach((step, index) => {
            step.attrs = this.getAttrs(
              this.selected_service?.version_data,
              step?.attrs,
              step
            );
          });
        } else {
          ser_schema.version_schema.attrs = this.getAttrs(
            this.selected_service?.version_data,
            ser_schema?.version_schema?.attrs,
            ser_schema?.version_schema
          );
        }
      }
      // if(ser_schema?.version_schema?.fields){

      // }
      // if (ser_schema?.base_audience_schema) {
      //   ser_schema.base_audience_schema.attrs = this.getAttrs(
      //     this.selected_service?.base_component_data || {},
      //     ser_schema?.base_audience_schema?.attrs,
      //     ser_schema?.base_audience_schema
      //   );
      // }
    },

    convertToJSON(jsonString) {
      try {
        return JSON.parse(jsonString);
      } catch (error) {
        return {};
      }
    },
    // دالة جلب كود خصائص الحقول
    getAttrs(data, attrs, schema = false) {
      schema?.fields?.forEach((field) => {
        data[field?.name] = data[field?.name] || null;
      });

      if (!attrs) return (data) => {};
      if (typeof attrs === "string") {
        attrs = this.convertToJSON(attrs);
      }
      // if (typeof attrs === "object") return (data) => attrs;
      try {
        if (schema) {
          return (data) => {
            // var attr = eval("(" + attrs + ")");
            // const func = this.getFormAttributes(attrs);
            // var attr = func(data);
            var attr = {};

            Object.entries(data).map(([key, val]) => {
              const p = attrs[key];
              attr[key] = {};
              // if (p?.param) attr[key].param = data[p?.param];
              if (p?.param) {
                let paramValue = data[p?.param];
                if (p.param === "fk_org") {
                  paramValue = this.$state.organization_id;
                }
                attr[key].param = paramValue;
              }
              if (p?.name_list) {
                attr[key].name_list = p?.name_list;
              }
              if (p?.depend) {
                attr[key].depend = data[p?.depend] ? true : false;
              }
              if (p?.add) {
                attr[key].add = p?.add;
              }
            });

            for (const field of schema?.fields) {
              if (attr[field?.name]?.name_list && !field?.name_list) {
                field.name_list = attr[field?.name]?.name_list;
              }
              if (field?.name_list) {
                if (!attr[field?.name]) {
                  attr[field?.name] = {};
                }
                if (field.name_list === "StudentsCoursesForServices") {
                  const paramVal = attr[field?.name].param || this.$state.organization_id;
                  attr[field?.name].param =
                    typeof paramVal == "object" ? paramVal : { org: paramVal };
                }

                const auto_list = dataList(
                  attr[field?.name] ? attr[field?.name]?.param : false
                )[field?.name_list];

                const { label, title, value } = auto_list || {};

                attr[field?.name].selectObject = (val, object) => {
                  if (val) {
                    if (Array?.isArray(val) && Array.isArray(object)) {
                      data[`${field?.name}_name`] = object?.map(
                        (v) => v[title || "name"]
                      );
                    } else if (object) {
                      data[`${field?.name}_name`] = object[title || "name"];
                      if (field?.is_main) {
                        Object.entries(object).forEach(([k, v]) => {
                          data[k] = v;
                        });
                      }
                    }
                  }
                };
                // attr[field?.name].returnObject = true;

                // attr[field?.name].update = (val) => {
                //   if (val) {
                //     if (!Array?.isArray(val)) {
                //       data[`${field?.name}_name`] = val[title || "name"];

                //       data[field?.name] = val[value ?? "id"]

                //     } else {
                //       data[`${field?.name}_name`] = val?.map(
                //         (v) => v[title || "name"]
                //       );
                //       data[field?.name] = val?.map((v) => v[value || "id"]);
                //     }
                //   }
                // };
              }
            }

            return attr;
          };
        }
        // else {
        //   return eval("(" + attrs + ")");
        // }
      } catch (e) {
        console.log(e);
        return {};
      }
    },

    // getStepAttr(data, attrs) {
    //   if (Object?.values(attrs)?.length) {
    //     var attr = eval("(" + attrs + ")");

    //     return attr;
    //   }

    //   return {};
    // },

    // الحصول على بيانات الخدمة وتفاصيلها (مثل الجمهور المستهدف)
    async getServiceSchema() {
      this.loading_schema = true;
      try {
        const response = await this.$axios.get(
          `${this.url_schema}${this.selected_service.fk_service}/`
        );
        this.service_schema = response.data?.data ?? {};

        this.setAttrs(this.service_schema);
      } catch (error) {
        console.error("Error fetching service details", error);
      } finally {
        this.loading_schema = false;
      }
    },

    // دالة انشاء وتعديل طلب الخدمة
    async saveServiceRequest() {
      await this.validateForms();
      if (!this.valid) return;

      try {
        this.loading = true;
        var formData = new FormData();
        var updateFormData = new FormData();
        const data = {
          fk_service: this.selected_service.fk_service,
          version_data: this.selected_service.version_data,
          target_audience_data: this.selected_service.target_audience_data,
          base_component_data: this.selected_service.base_component_data,
        };
        formData.append("data", JSON.stringify(data));
        updateFormData.append(
          "data",
          JSON.stringify({ version_data: this.selected_service.version_data })
        );

        // Handle new attachments structure
        this.attachments_list.forEach((attachment, index) => {
          formData.append(`attachments[${index}][name]`, attachment.name || "");
          formData.append(`attachments[${index}][file]`, attachment.fileObj);
          formData.append(
            `attachments[${index}][description]`,
            attachment.description || ""
          );
        });

        const request = this.selected_service?.id
          ? this.$axios.put(
              `${this.url_request_service}${this.selected_service.id}/`,
              updateFormData,
              { headers: { "Content-Type": "multipart/form-data" } }
            )
          : this.$axios.post(this.url_request_service, formData);

        await request;

        this.$snack(this.selected_service?.id ? "update" : "add");
        setTimeout(() => {
          this.$router.push({
            name: "service-requests",
            fk_service: this.selected_service.id,
          });
        }, 1500);
        // this.$router.back();
      } finally {
        this.loading = false;
      }
    },
    async validateForms() {
      let isAudienceValid = true;
      if (
        this.$refs.audience_form &&
        this.service_schema?.target_audience_schema?.fields?.length > 0
      ) {
        const valid = await this.$refs.audience_form.validate();
        isAudienceValid = valid;
      }

      // let isBaseValid = true;
      // if (
      //   this.$refs.base_form &&
      //   this.service_schema?.base_audience_schema?.fields?.length > 0
      // ) {
      //   const valid = await this.$refs.base_form.validate();
      //   isBaseValid = valid;
      // }
      let isServiceValid = true;

      const forms = this.$refs.service_form;

      if (Array.isArray(forms)) {
        forms?.forEach(async (form, index) => {
          this.form_valid[index] = (await form.validate()?.valid) ?? false;
        });
        const validationPromises = forms.map((form) => form.validate());
        const validationResults = await Promise.all(validationPromises);

        isServiceValid = validationResults.every((result) => result.valid === true);
      } else if (forms) {
        const { valid } = await forms?.validate();
        isServiceValid = valid;
      }
      this.valid = isAudienceValid && isServiceValid;
    },

    // الحصول على بيانات الخدمة
    async getRequestService() {
      if (this.request_id) {
        return await this.$axios(`${this.url_request_service}${this.request_id}/`).then(
          async (response) => {
            this.$snack("success", { message: response.data?.message });
            this.selected_service = response.data?.data;
            if (!this.selected_service.base_component_data) {
              this.selected_service.base_component_data = {};
            }
            if (!this.selected_service.target_audience_data) {
              this.selected_service.target_audience_data = {};
            }
          }
        );
      }
    },

    clearRequestService() {
      if (Array.isArray(this.$refs.service_form)) {
        this.$refs.service_form?.forEach((form) => {
          form.reset();
        });
      } else if (this.$refs.service_form) {
        this.$refs.service_form.reset();
      }
      if (this.$refs.audience_form) {
        this.$refs.audience_form.reset();
      }
      // if (this.$refs.base_form) {
      //   this.$refs.base_form.reset();
      // }
      // this.$refs.attachments_form.reset();
      this.attachments_list = [];
      // this.step_index = 0;
    },
  },
  computed: {
    // attrs_selected_services() {
    //   let params = {};
    //   const schema = this.service_schema.target_audience_schema  || {};
    //   if(Object.keys(schema)?.length==0) return {}
    //   const fields = schema?.fields || []
    //   const attrs = schema?.attrs;
    //   console.log(schema['attrs']);
    //   let data = this.selected_service.target_audience_data;
    //   Object.entries(data).map(
    //     ([key, val]) => {
    //       const p = attrs[key];
    //       params[key] = {};
    //       if (p?.param)
    //         params[key].param =
    //           data[p?.param];
    //     }
    //   );
    //   for (const field of fields) {
    //     if (field?.name_list) {
    //       const { label, title, value } = this.$mpot dataList(
    //         attrs[field?.name] ? attrs[field?.name]?.param : false
    //       )[field?.name_list];
    //       if (!params[field?.name]) {
    //         params[field?.name] = {};
    //       }
    //       params[field?.name].returnObject = true;
    //       params[field?.name].update = (val) => {
    //         if (val && !Array?.isArray(val)) {
    //           data[`${field?.name}_name`] = val[title || "name"];
    //           data[field?.name] = val[value ?? "id"];
    //         } else if (Array?.isArray(val)) {
    //           data[`${field?.name}_name`] = val?.map(
    //             (v) => v[title || "name"]
    //           );
    //           data[field?.name] = val?.map((v) => v[value || "id"]);
    //         }
    //       };
    //     }
    //   }
    //   return params;
    // },
  },
};
</script>

<style scoped>
/* Add any custom transitions or overrides */
.gap-2 {
  gap: 8px;
}

.card {
  height: 100% !important;
  display: flex;
  flex-direction: column;
}
.card_content {
  flex: 1 1 auto;
  overflow-y: auto;
}
</style>
