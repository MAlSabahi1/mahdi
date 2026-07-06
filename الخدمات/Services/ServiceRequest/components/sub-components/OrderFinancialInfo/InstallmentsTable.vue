<template>
  <div class="installments-container">
    <!-- Desktop Table View -->
    <div class="d-none d-md-block">
      <v-table class="premium-table">
        <thead>
          <tr>
            <th class="text-right">المعرف</th>
            <!-- <th class="text-right">فترة القسط</th> -->
            <th class="text-right">مبلغ القسط</th>
            <th class="text-right">المبلغ المستحق</th>
            <th class="text-right">رقم الحافظة</th>
            <th class="text-right" v-if="hasGrant">مبلغ المنحة</th>
            <th class="text-right" v-if="hasGrant">حافظة الجهة المانحة</th>
            <th class="text-right" v-if="hasDiscount">مبلغ التخفيض</th>
            <th class="text-right">تاريخ الاستحقاق</th>
            <th class="text-right">الحالة</th>
            <th class="text-center">الإجراءات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in items" :key="item.id" class="table-row">
            <td>
              <div class="id-badge">#{{ 1000 + index }}</div>
            </td>
            <!-- <td>
              <div class="font-weight-black text-slate-800">{{ item.period }}</div>
            </td> -->
            <td>
              <div class="amount-display">
                <span class="amount-val">{{
                  formatCurrency(item.amount)
                }}</span>
                <span class="amount-unit mr-1">{{ item?.currency__data?.symbol }}</span>
              </div>
            </td>
            <td>
              <div class="amount-display">
                <span class="amount-val">{{
                  formatCurrency(item.due_amount)
                }}</span>
                <span class="amount-unit mr-1">{{ item?.currency__data?.symbol }}</span>
              </div>
            </td>
            <td>
              <div class="id-badge">{{ item?.student_invoice_number }}</div>
            </td>

            <td v-if="hasGrant">
              <div class="amount-display">
                <span class="amount-val">{{
                  formatCurrency(item.grant_amount)
                }}</span>
                <span class="amount-unit mr-1">{{ item?.currency__data?.symbol }}</span>
              </div>
            </td>
            <td v-if="hasGrant">
              <div class="id-badge">{{ item?.grant_invoice_number }}</div>
            </td>
            <td v-if="hasDiscount">
              <div class="amount-display">
                <span class="amount-val">{{
                  formatCurrency(item.discount_amount)
                }}</span>
                <span class="amount-unit mr-1">{{ item?.currency__data?.symbol }}</span>
              </div>
            </td>
            <td>
              <div class="date-display">
                <v-icon
                  icon="mdi-calendar-clock-outline"
                  size="16"
                  class="ml-2 text-slate-400"
                ></v-icon>
                <span class="font-weight-bold text-slate-600">{{
                  item.due_date
                }}</span>
              </div>
            </td>
            <td>
              <v-chip
                :color="getStatusColor(item.payment_status)"
                size="small"
                variant="flat"
                class="font-weight-black px-4 rounded-lg"
              >
                <v-icon start size="14" class="ml-1">
                  {{ getStatusIcon(item.payment_status) }}
                </v-icon>
                {{
                  item.payment_status === "paid" ? "تم السداد" : "بانتظار الدفع"
                }}
              </v-chip>
            </td>
            <td>
              <div class="d-flex justify-center ga-2">
                <!-- icon="mdi-cash-register" -->
                <v-btn
                  v-if="item.payment_status !== 'paid'"
                  prepend-icon="mdi-cash-register"
                  color="success"
                  variant="outlined"
                  class="rounded-lg"
                  :loading="item?.is_loading"
                  @click="createInstallmentInvoices(item)"
                >
                  تسديد
                </v-btn>
                <v-btn
                  icon="mdi-eye"
                  density="comfortable"
                  color="primary"
                  variant="outlined"
                  class="rounded-lg"
                  @click="(dialog_show = true), (selected_installment = item)"
                >
                </v-btn>
                <!-- <div class="d-flex ga-2">
            <v-btn v-if="item.payment_status !== 'paid'" block color="success" variant="flat"
              prepend-icon="mdi-cash-register" class="rounded-xl font-weight-black" height="40"
              @click="$emit('pay', item)">سداد القسط</v-btn>
            <div class="d-flex ga-2 w-100" v-else>
              <v-btn class="flex-grow-1 rounded-xl font-weight-black" color="primary" variant="tonal"
                prepend-icon="mdi-pencil-outline" height="40" @click="$emit('edit', item)">تعديل</v-btn>
              <v-btn icon="mdi-delete-outline" color="error" variant="tonal" class="rounded-xl" width="40" height="40"
                @click="$emit('delete', item)"></v-btn>
            </div>
          </div> -->
              </div>
            </td>
          </tr>
        </tbody>
      </v-table>
    </div>
    <custom-dialog v-model="dialog_show" height="80vh" :title="$t('print')">
      <template v-slot>
        <div class="d-flex flex-column position-relative">
          <v-btn
            id="printbtn"
            icon
            density="compact"
            class="ma-3 print-btn ms-auto position-sticky"
            style="top: 10px; z-index: 99"
            :title="$t('print')"
            elevation="0"
            color="#f8f8f8"
            border="thin"
            rounded
            @click="printInvoice"
          >
            <v-icon size="16" color="grey">mdi-printer</v-icon>
          </v-btn>
        </div>

        <v-sheet
          class="mx-auto document-sheet position-relative overflow-hidden"
          id="request_invoice"
        >
          <v-card class="ma-2 pa-2">
            <div class="text-center mb-4">
              <div class="text-h6">فاتورة رسمية / سند قبض</div>
            </div>
            <v-row class="mt-2 text-caption">
              <v-col
                ><span>
                  رقم الطلب:
                </span>
                <span>
                  {{ selected_installment?.request_number }}
                </span>
              </v-col
              >
              <v-col class="text-end"> <span>
                تاريخ الاستحقاق:
                </span>
                <span>
                  {{selected_installment?.due_date}}
                  </span>
              </v-col>
            </v-row>

            <v-card class="mb-4" variant="outlined">
              <v-card-title class="bg-grey-lighten-3">
                بيانات مقدم الطلب
              </v-card-title>
              <v-card-text>
                <v-row dense>
                  <v-col cols="6">
                    <span>
                      الاسم:
                    </span>
                    <span>
                      {{ selected_installment?.requester_name }}
                    </span>
                  </v-col>
                  <v-col cols="6">
                    <span>
                      الرقم الجامعي:
                    </span>
                    <span>
                      {{}}
                    </span>
                  </v-col>
                </v-row>
                <v-table class="mt-3">
                  <thead>
                    <tr>
                      <th>الخدمة</th>
                      <th>رقم الفاتورة</th>
                      <th>المبلغ</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{{ selected_installment?.service_name }}</td>
                      <td>
                        {{ selected_installment?.student_invoice_number }}
                      </td>
                      <td>{{ selected_installment?.due_amount }} {{selected_installment?.currency__data?.symbol}}</td>
                    </tr>
                  </tbody>
                </v-table>
              </v-card-text>
            </v-card>
            <v-divider class="py-2 my-2"></v-divider>
            <v-card v-if="selected_installment?.grant_amount>0" class="mb-4" outlined variant="outlined" >
              <v-card-title class="bg-grey-lighten-3">
                بيانات الجهة المانحة
              </v-card-title>
              <v-card-text>
                <v-row dense>
                  <v-col cols="6">
                    <span>
                      اسم الجهة:
                    </span>

                     <span>
                      {{selected_installment?.fk_grant_source__name_ar}}
                     </span>
                    </v-col>
                  <v-col cols="6">
                    <span>
                      نسبة التحمل :
                    </span>

                     <span>
                      %{{selected_installment?.fk_grant_source__grant_percentage}}
                     </span>
                    </v-col>
                </v-row>
                <v-table class="mt-3">
                  <thead>
                    <tr>
                      <th>الخدمة</th>
                      <th>رقم الفاتورة</th>
                      <th>المبلغ</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{{ selected_installment?.service_name }}</td>
                      <td>{{ selected_installment?.grant_invoice_number }}</td>
                      <td>{{ selected_installment?.grant_amount }} {{selected_installment?.currency__data?.symbol}}</td>
                    </tr>
                  </tbody>
                </v-table>
              </v-card-text>
            </v-card>
              <v-row class="" >
                <v-col cols="12" md="6" lg="6"></v-col>
                <v-col cols="12" md="6" lg="6">
                  <v-table density="compact">
                     <thead>
                    <tr>
                      <th>البند</th>
                      <th>المبلغ</th>
                      <th>العملة</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="text-blue">
                      <td>اجمالي الفاتورة</td>
                      <td>{{ selected_installment?.amount }}</td>
                      <td>{{selected_installment?.currency__data?.symbol}}</td>
                    </tr>
                    <tr class="text-orange" v-if="selected_installment?.discount_amount>0">
                      <td>الخصم</td>
                      <td>-{{ selected_installment?.discount_amount }}</td>
                      <td>{{selected_installment?.currency__data?.symbol}}</td>
                    </tr>
                    <tr class="text-orange" v-if="selected_installment?.grant_amount>0">
                      <td>دعم الجهة المانحة</td>
                      <td>-{{ selected_installment?.grant_amount }}</td>
                      <td>{{selected_installment?.currency__data?.symbol}}</td>
                    </tr>
                    <tr  class="text-h6" v-if="selected_installment?.due_amount>0">
                      <td>المبلغ المستحق</td>
                      <td>{{ selected_installment?.due_amount }}</td>
                      <td>{{selected_installment?.currency__data?.symbol}}</td>
                    </tr>
                    <tr class="text-success">
                      <td>المبلغ المدفوع</td>
                      <td>{{ selected_installment?.amount_paid }}</td>
                      <td>{{selected_installment?.currency__data?.symbol}}</td>
                    </tr>
                    <tr class="text-error text-h6">
                      <td>المبلغ المتبقي</td>
                      <td>{{ calcRemainingAmount(selected_installment?.due_amount,selected_installment?.amount_paid) }}</td>
                      <td>{{selected_installment?.currency__data?.symbol}}</td>
                    </tr>
                  </tbody>
                  </v-table>
                </v-col>
              </v-row>
              <!-- <div>
               <span>
                 اجمالي الفاتورة:
               </span>
                <span>
                  {{ selected_installment?.amount }} {{selected_installment?.currency}}
                </span>
              </div>
              <div class="me-4">
                <span>
                  الخصم:
                </span>
                <span v-if="selected_installment?.discount_amount>0">
                  -{{ selected_installment?.discount_amount }} {{selected_installment?.currency}}
                </span>
              </div> -->
          </v-card>

        </v-sheet>
      </template>
    </custom-dialog>

    <!-- Mobile Card View -->
    <div class="d-md-none">
      <div class="pa-4 ga-y-4 d-flex flex-column">
        <v-card
          v-for="(item, index) in items"
          :key="item.id"
          variant="flat"
          class="mobile-installment-card border-system pa-4"
        >
          <div class="d-flex justify-space-between align-center mb-4">
            <div class="id-badge">#{{ 1000 + index }}</div>
            <v-chip
              :color="getStatusColor(item.payment_status)"
              size="x-small"
              variant="flat"
              class="font-weight-black px-3"
            >
              {{
                item.payment_status === "paid" ? "تم السداد" : "بانتظار الدفع"
              }}
            </v-chip>
          </div>

          <div class="d-flex align-center mb-4">
            <v-avatar color="slate-50" size="36" class="ml-3 rounded-lg">
              <v-icon
                icon="mdi-calendar-text"
                size="18"
                color="slate-400"
              ></v-icon>
            </v-avatar>
            <div>
              <div class="text-caption text-slate-400 font-weight-bold mb-0">
                فترة القسط
              </div>
              <div class="text-body-2 font-weight-black text-slate-800">
                {{ item.period }}
              </div>
            </div>
          </div>

          <v-row no-gutters class="mb-4">
            <v-col cols="6">
              <div class="text-caption text-slate-400 font-weight-bold mb-1">
                المبلغ المستحق
              </div>
              <div class="amount-display">
                <span class="amount-val-mobile">{{
                  formatCurrency(item.amount)
                }}</span>
                <span class="amount-unit-mobile mr-1">ر.س</span>
              </div>
            </v-col>
            <v-col cols="6" class="text-left">
              <div class="text-caption text-slate-400 font-weight-bold mb-1">
                تاريخ الاستحقاق
              </div>
              <div class="text-body-2 font-weight-bold text-slate-600">
                {{ item.due_date }}
              </div>
            </v-col>
          </v-row>
        </v-card>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="items.length === 0" class="text-center py-16">
      <v-avatar color="slate-50" size="80" class="mb-4">
        <v-icon
          icon="mdi-calendar-blank-outline"
          size="40"
          color="slate-200"
        ></v-icon>
      </v-avatar>
      <h4 class="text-h6 font-weight-black text-slate-400">
        لا توجد أقساط مالية مسجلة
      </h4>
      <p class="text-body-2 text-slate-300 font-weight-bold">
        سيتم عرض الأقساط هنا عند إضافتها للطلب
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "InstallmentsTable",
  props: {
    items: { type: Array, required: true },
    title: { type: String, default: "جدول الأقساط والدفعات" },
    subtitle: {
      type: String,
      default: "إدارة ومتابعة المواعيد النهائية للسداد",
    },
    icon: { type: String, default: "mdi-credit-card-clock-outline" },
    addLabel: { type: String, default: "إضافة قسط مالي" },
  },
  emits: ["add", "print", "pay", "edit", "delete"],
  inject: ["context"],

  data() {
    return {
      url: this.context.url,
      requestId: this.context.request_id,
      invoices_data: [],
      is_loading: false,
      selected_installment: null,
      dialog_show: false,
    };
  },
  computed: {
    hasGrant() {
      return this.items?.filter((item) => item?.grant_amount > 0)?.length > 0;
    },
    hasDiscount() {
      return (
        this.items?.filter((item) => item?.discount_amount > 0)?.length > 0
      );
    },
  },
  methods: {
    printInvoice() {
      this.$shared.printReport("request_invoice");
    },
    calcRemainingAmount(amount,paid_amount){
      amount = amount?amount:0
      paid_amount = paid_amount?paid_amount:0
      return amount - paid_amount
    },

    async createInstallmentInvoices(installment) {
      installment.is_loading = true;
      await this.$axios
        .post(
          `${this.url}${this.requestId}/create-installment-invoices/${installment.id}/`
        )
        .then((res) => {
          this.invoices_data = res.data?.data ?? res.data;
          this.$alert("add", res.data);
          this.context?.getRequestDetails();
        })
        .finally(() => {
          installment.is_loading = false;
        });
    },
    formatCurrency(val) {
      return new Intl.NumberFormat("ar-SA").format(val);
    },
    getStatusColor(status) {
      return status === "paid" ? "success" : "warning";
    },
    getStatusIcon(status) {
      return status === "paid" ? "mdi-check-circle" : "mdi-clock-outline";
    },
  },
};
</script>

<style scoped>
.installments-container {
  width: 100%;
}

.premium-table :deep(thead th) {
  background-color: #f8fafc !important;
  color: #64748b !important;
  font-size: 13px !important;
  font-weight: 800 !important;
  padding: 20px 24px !important;
  border-bottom: 2px solid #e2e8f0 !important;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.premium-table :deep(tbody td) {
  padding: 20px 24px !important;
  border-bottom: 1px solid #f1f5f9 !important;
  font-size: 14px;
}

.table-row:hover {
  background-color: #f8fafc;
}

.id-badge {
  background: #f1f5f9;
  color: #64748b;
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 800;
  display: inline-block;
}

.amount-val {
  font-size: 1.15rem;
  font-weight: 900;
  color: #0f172a;
}

.amount-val-mobile {
  font-size: 1rem;
  font-weight: 900;
  color: #0f172a;
}

.amount-unit {
  font-size: 0.85rem;
  font-weight: 700;
  color: #94a3b8;
}

.amount-unit-mobile {
  font-size: 0.75rem;
  font-weight: 700;
  color: #94a3b8;
}

.date-display {
  display: flex;
  align-items: center;
}

.mobile-installment-card {
  background: #ffffff;
  border-radius: 16px;
}

.ga-2 {
  gap: 8px;
}

.ga-y-4 {
  row-gap: 16px;
}

.text-slate-800 {
  color: #1e293b !important;
}

.text-slate-600 {
  color: #475569 !important;
}

.text-slate-400 {
  color: #94a3b8 !important;
}

.text-slate-300 {
  color: #cbd5e1 !important;
}

.text-slate-200 {
  color: #e2e8f0 !important;
}

.border-system {
  border: 1px solid #e2e8f0 !important;
}
</style>
