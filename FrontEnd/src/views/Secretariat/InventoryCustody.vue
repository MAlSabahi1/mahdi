<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('secretariat.inventory.title')" />
    <div class="space-y-6">
      <!-- Tabs Selector -->
      <div class="flex gap-2 p-1.5 bg-gray-100 dark:bg-gray-800 rounded-2xl w-fit">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          @click="activeTab = tab.value"
          :class="[
            'px-5 py-2 rounded-xl text-sm font-semibold transition cursor-pointer',
            activeTab === tab.value
              ? 'bg-white dark:bg-gray-900 text-gray-900 dark:text-white shadow-theme-xs'
              : 'text-gray-500 hover:text-gray-900 dark:hover:text-white'
          ]"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Tab 1: Stock Items -->
      <div v-if="activeTab === 'stock'" class="space-y-6 animate-fade-in">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between bg-white dark:bg-gray-900 p-5 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-theme-sm">
          <div class="flex flex-1 flex-col gap-4 sm:flex-row sm:items-center">
            <div class="relative max-w-xs w-full">
              <input
                v-model="stockSearch"
                type="text"
                placeholder="البحث في المخزن..."
                class="w-full rounded-lg border border-gray-300 bg-gray-50 py-2.5 px-4 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                @input="onStockSearch"
              />
            </div>
            <div class="w-full sm:w-48">
              <select
                v-model="stockTypeFilter"
                class="w-full rounded-lg border border-gray-300 bg-gray-50 py-2.5 px-3 text-sm text-gray-900 focus:border-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                @change="fetchStock"
              >
                <option value="">التصنيف: الكل</option>
                <option value="stationery">قرطاسية ومواد مكتبية</option>
                <option value="furniture">أثاث مكتبي</option>
                <option value="equipment">أجهزة وتجهيزات</option>
                <option value="other">أخرى</option>
              </select>
            </div>
          </div>
          <button
            @click="showAddItemModal = true"
            class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white hover:bg-brand-600 transition shadow-theme-xs cursor-pointer"
          >
            + {{ $t('secretariat.inventory.add_item') }}
          </button>
        </div>

        <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
            <thead class="bg-gray-50 dark:bg-gray-800/50">
              <tr>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">كود المادة</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">اسم المادة</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">التصنيف</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">الكمية المتوفرة</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">حد الطلب الأدنى</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">الوحدة</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-800 bg-white dark:bg-gray-900">
              <tr v-if="loading" class="text-center py-6"><td colspan="5" class="py-6 text-sm text-gray-500">جاري التحميل...</td></tr>
              <tr v-else-if="stockItems.length === 0" class="text-center py-6"><td colspan="5" class="py-6 text-sm text-gray-500">لا توجد مواد مخزنية.</td></tr>
              <tr v-else v-for="item in stockItems" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/30 transition">
                <td class="px-6 py-4 text-sm font-semibold text-gray-950 dark:text-white">{{ item.code }}</td>
                <td class="px-6 py-4 text-sm text-gray-850 dark:text-gray-300 font-medium">{{ item.name }}</td>
                <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{{ item.type_display }}</td>
                <td class="px-6 py-4 text-sm">
                  <span
                    :class="[
                      'font-bold',
                      item.quantity_in_stock <= item.minimum_stock_level ? 'text-red-500 flex items-center gap-1.5' : 'text-gray-900 dark:text-white'
                    ]"
                  >
                    {{ item.quantity_in_stock }}
                    <span v-if="item.quantity_in_stock <= item.minimum_stock_level" class="text-[10px] px-1.5 py-0.5 bg-red-50 text-red-650 rounded-md dark:bg-red-950/40 dark:text-red-400 font-black">منخفض</span>
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400 font-mono">{{ item.minimum_stock_level }}</td>
                <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{{ item.unit }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tab 2: Stationery Requests -->
      <div v-if="activeTab === 'requests'" class="space-y-6 animate-fade-in">
        <div class="flex justify-between items-center bg-white dark:bg-gray-900 p-5 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-theme-sm">
          <h3 class="text-base font-bold text-gray-900 dark:text-white">طلبات صرف القرطاسية والمستلزمات</h3>
          <button
            @click="showAddRequestModal = true"
            class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white hover:bg-brand-600 transition shadow-theme-xs cursor-pointer"
          >
            + {{ $t('secretariat.inventory.add_request') }}
          </button>
        </div>

        <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
            <thead class="bg-gray-50 dark:bg-gray-800/50">
              <tr>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">طالب الصرف</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">المادة المطلوبة</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">الكمية</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">الحالة</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">ملاحظات</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">الإجراءات</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-800 bg-white dark:bg-gray-900">
              <tr v-if="loading" class="text-center py-6"><td colspan="6" class="py-6 text-sm text-gray-500">جاري التحميل...</td></tr>
              <tr v-else-if="requests.length === 0" class="text-center py-6"><td colspan="6" class="py-6 text-sm text-gray-500">لا توجد طلبات صرف حالياً.</td></tr>
              <tr v-else v-for="req in requests" :key="req.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/30 transition">
                <td class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white">{{ req.requested_by_name }}</td>
                <td class="px-6 py-4 text-sm text-gray-850 dark:text-gray-300 font-medium">{{ req.item_name }}</td>
                <td class="px-6 py-4 text-sm font-bold text-gray-950 dark:text-white">{{ req.quantity }}</td>
                <td class="px-6 py-4 text-sm">
                  <span
                    :class="[
                      'px-2 py-0.5 rounded-full text-xxs font-semibold',
                      req.status === 'approved' ? 'bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300' :
                      req.status === 'rejected' ? 'bg-red-50 text-red-700 dark:bg-red-900/30 dark:text-red-300' :
                      'bg-amber-50 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300'
                    ]"
                  >
                    {{ req.status_display }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400 max-w-xs truncate">{{ req.notes || '-' }}</td>
                <td class="px-6 py-4 text-sm flex gap-2">
                  <template v-if="req.status === 'pending'">
                    <button
                      @click="processRequest(req.id, 'approved')"
                      class="px-2.5 py-1 text-xxs font-bold text-white bg-green-500 hover:bg-green-600 rounded-lg cursor-pointer"
                    >
                      موافقة
                    </button>
                    <button
                      @click="processRequest(req.id, 'rejected')"
                      class="px-2.5 py-1 text-xxs font-bold text-white bg-red-500 hover:bg-red-600 rounded-lg cursor-pointer"
                    >
                      رفض
                    </button>
                  </template>
                  <span v-else class="text-gray-400">-</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tab 3: Custody Log -->
      <div v-if="activeTab === 'custody'" class="space-y-6 animate-fade-in">
        <div class="flex justify-between items-center bg-white dark:bg-gray-900 p-5 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-theme-sm">
          <h3 class="text-base font-bold text-gray-900 dark:text-white">سجلات عهد الموظفين النشطة والتالفة</h3>
          <button
            @click="showAddCustodyModal = true"
            class="flex items-center gap-2 rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white hover:bg-brand-600 transition shadow-theme-xs cursor-pointer"
          >
            + {{ $t('secretariat.inventory.add_custody') }}
          </button>
        </div>

        <div class="rounded-2xl border border-gray-200 bg-white shadow-theme-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
            <thead class="bg-gray-50 dark:bg-gray-800/50">
              <tr>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">المستلم (الموظف)</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">المادة العهدة</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">الكمية</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">تاريخ الاستلام</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">تاريخ الإرجاع</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">الحالة</th>
                <th class="px-6 py-4 text-start text-xs font-semibold text-gray-500 dark:text-gray-400">الإجراءات</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-800 bg-white dark:bg-gray-900">
              <tr v-if="loading" class="text-center py-6"><td colspan="7" class="py-6 text-sm text-gray-500">جاري التحميل...</td></tr>
              <tr v-else-if="custodies.length === 0" class="text-center py-6"><td colspan="7" class="py-6 text-sm text-gray-500">لا توجد عهد مسجلة.</td></tr>
              <tr v-else v-for="cust in custodies" :key="cust.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/30 transition">
                <td class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white">{{ cust.assigned_to_name }}</td>
                <td class="px-6 py-4 text-sm text-gray-850 dark:text-gray-300 font-medium">{{ cust.item_name }}</td>
                <td class="px-6 py-4 text-sm font-bold text-gray-950 dark:text-white">{{ cust.quantity }}</td>
                <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{{ cust.date_assigned }}</td>
                <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{{ cust.date_returned || 'في العهدة' }}</td>
                <td class="px-6 py-4 text-sm">
                  <span
                    :class="[
                      'px-2.5 py-0.5 rounded-full text-xxs font-semibold',
                      cust.status === 'returned' ? 'bg-green-50 text-green-700 dark:bg-green-900/30' :
                      cust.status === 'damaged' ? 'bg-red-50 text-red-700 dark:bg-red-900/30' :
                      'bg-blue-50 text-blue-700 dark:bg-blue-900/30'
                    ]"
                  >
                    {{ cust.status_display }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm">
                  <template v-if="cust.status === 'assigned'">
                    <button
                      @click="returnCustody(cust.id)"
                      class="px-2.5 py-1 text-xxs font-bold text-white bg-indigo-500 hover:bg-indigo-600 rounded-lg cursor-pointer"
                    >
                      إرجاع العهدة
                    </button>
                  </template>
                  <span v-else class="text-gray-450">-</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <!-- Add Item Modal -->
    <div v-if="showAddItemModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm">
      <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-2xl shadow-xl overflow-hidden border border-gray-200 dark:border-gray-800 animate-fade-in">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center bg-gray-50 dark:bg-gray-800/50">
          <h3 class="text-sm font-bold text-gray-900 dark:text-white">إضافة مادة مخزنية جديدة</h3>
          <button @click="showAddItemModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl font-bold cursor-pointer">&times;</button>
        </div>
        <form @submit.prevent="submitAddItem" class="p-6 space-y-4">
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">كود المادة/الباركود *</label>
            <input v-model="itemForm.code" type="text" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">اسم المادة *</label>
            <input v-model="itemForm.name" type="text" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">التصنيف *</label>
            <select v-model="itemForm.type" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm">
              <option value="stationery">قرطاسية ومواد مكتبية</option>
              <option value="furniture">أثاث مكتبي</option>
              <option value="equipment">أجهزة وتجهيزات</option>
              <option value="other">أخرى</option>
            </select>
          </div>
          <div class="grid grid-cols-3 gap-2">
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">الكمية الابتدائية *</label>
              <input v-model.number="itemForm.quantity_in_stock" type="number" required min="0" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">حد الطلب الأدنى *</label>
              <input v-model.number="itemForm.minimum_stock_level" type="number" required min="0" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">الوحدة *</label>
              <input v-model="itemForm.unit" type="text" required placeholder="مثال: حبة، كرتون" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
            </div>
          </div>
          <div class="flex justify-end gap-2 pt-4 border-t border-gray-200 dark:border-gray-800">
            <button type="button" @click="showAddItemModal = false" class="px-4 py-2 text-xs font-medium text-gray-700 bg-white border rounded-lg hover:bg-gray-50">إلغاء</button>
            <button type="submit" class="px-4 py-2 text-xs font-medium text-white bg-brand-500 rounded-lg hover:bg-brand-600">إضافة</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Add Request Modal -->
    <div v-if="showAddRequestModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm">
      <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-2xl shadow-xl overflow-hidden border border-gray-200 dark:border-gray-800 animate-fade-in">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center bg-gray-50 dark:bg-gray-800/50">
          <h3 class="text-sm font-bold text-gray-900 dark:text-white">تقديم طلب صرف مواد/قرطاسية</h3>
          <button @click="showAddRequestModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl font-bold cursor-pointer">&times;</button>
        </div>
        <form @submit.prevent="submitAddRequest" class="p-6 space-y-4">
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">الموظف طالب الصرف *</label>
            <select v-model="requestForm.requested_by" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm">
              <option value="" disabled>اختر الموظف...</option>
              <option v-for="emp in employees" :key="emp.id" :value="emp.id">
                {{ emp.full_name }} ({{ emp.military_number }})
              </option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">المادة المطلوبة *</label>
            <select v-model="requestForm.item" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm">
              <option value="" disabled>اختر المادة...</option>
              <option v-for="item in stockItems" :key="item.id" :value="item.id">
                {{ item.name }} (كود: {{ item.code }}) - متوفر: {{ item.quantity_in_stock }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">الكمية المطلوبة *</label>
            <input v-model.number="requestForm.quantity" type="number" required min="1" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">ملاحظات/مبررات الصرف</label>
            <textarea v-model="requestForm.notes" rows="2" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm"></textarea>
          </div>
          <div class="flex justify-end gap-2 pt-4 border-t border-gray-200 dark:border-gray-800">
            <button type="button" @click="showAddRequestModal = false" class="px-4 py-2 text-xs font-medium text-gray-700 bg-white border rounded-lg hover:bg-gray-50">إلغاء</button>
            <button type="submit" class="px-4 py-2 text-xs font-medium text-white bg-brand-500 rounded-lg hover:bg-brand-600">تقديم الطلب</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Add Custody Modal -->
    <div v-if="showAddCustodyModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm">
      <div class="w-full max-w-md bg-white dark:bg-gray-900 rounded-2xl shadow-xl overflow-hidden border border-gray-200 dark:border-gray-800 animate-fade-in">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center bg-gray-50 dark:bg-gray-800/50">
          <h3 class="text-sm font-bold text-gray-900 dark:text-white">إسناد عهدة جديدة لموظف</h3>
          <button @click="showAddCustodyModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl font-bold cursor-pointer">&times;</button>
        </div>
        <form @submit.prevent="submitAddCustody" class="p-6 space-y-4">
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">الموظف المستلم *</label>
            <select v-model="custodyForm.assigned_to" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm">
              <option value="" disabled>اختر الموظف...</option>
              <option v-for="emp in employees" :key="emp.id" :value="emp.id">
                {{ emp.full_name }} ({{ emp.military_number }})
              </option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">المادة (الأثاث/الأجهزة) *</label>
            <select v-model="custodyForm.item" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm">
              <option value="" disabled>اختر المادة...</option>
              <!-- filter items to keep furniture / equipment / others -->
              <option v-for="item in stockItems" :key="item.id" :value="item.id">
                {{ item.name }} ({{ item.type_display }}) - متوفر: {{ item.quantity_in_stock }}
              </option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">الكمية *</label>
              <input v-model.number="custodyForm.quantity" type="number" required min="1" class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">تاريخ التسليم *</label>
              <input v-model="custodyForm.date_assigned" type="date" required class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm" />
            </div>
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">ملاحظات وتفاصيل العهدة</label>
            <textarea v-model="custodyForm.notes" rows="2" placeholder="الرقم التسلسلي للجهاز، تفاصيل حالة الأثاث، إلخ..." class="w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm"></textarea>
          </div>
          <div class="flex justify-end gap-2 pt-4 border-t border-gray-200 dark:border-gray-800">
            <button type="button" @click="showAddCustodyModal = false" class="px-4 py-2 text-xs font-medium text-gray-700 bg-white border rounded-lg hover:bg-gray-50">إلغاء</button>
            <button type="submit" class="px-4 py-2 text-xs font-medium text-white bg-brand-500 rounded-lg hover:bg-brand-600">إسناد العهدة</button>
          </div>
        </form>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useSecretariatStore } from '@/stores/secretariat'
import { usePersonnelStore } from '@/stores/personnel'

const store = useSecretariatStore()
const personnelStore = usePersonnelStore()

const activeTab = ref('stock')
const loading = ref(false)

const tabs = [
  { label: 'المواد المخزنية', value: 'stock' },
  { label: 'طلبات صرف القرطاسية', value: 'requests' },
  { label: 'سجلات العهد', value: 'custody' }
]

// Data lists
const stockItems = ref<any[]>([])
const requests = ref<any[]>([])
const custodies = ref<any[]>([])
const employees = ref<any[]>([])

// Search / Filters
const stockSearch = ref('')
const stockTypeFilter = ref('')

// Modals toggles
const showAddItemModal = ref(false)
const showAddRequestModal = ref(false)
const showAddCustodyModal = ref(false)

// Forms templates
const itemForm = ref({
  code: '',
  name: '',
  type: 'stationery',
  quantity_in_stock: 0,
  minimum_stock_level: 5,
  unit: 'حبة'
})

const requestForm = ref({
  requested_by: '',
  item: '',
  quantity: 1,
  notes: ''
})

const custodyForm = ref({
  item: '',
  assigned_to: '',
  quantity: 1,
  date_assigned: new Date().toISOString().split('T')[0],
  notes: ''
})

async function fetchStock() {
  loading.value = true
  try {
    const params: any = {}
    if (stockSearch.value) params.search = stockSearch.value
    if (stockTypeFilter.value) params.type = stockTypeFilter.value
    const res = await store.fetchInventoryItems(params)
    stockItems.value = res.results || []
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function fetchRequests() {
  loading.value = true
  try {
    const res = await store.fetchInventoryRequests()
    requests.value = res.results || []
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function fetchCustodies() {
  loading.value = true
  try {
    const res = await store.fetchCustodies()
    custodies.value = res.results || []
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

let searchTimeout: any = null
function onStockSearch() {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchStock()
  }, 350)
}

// Process approvals
async function processRequest(id: number, status: 'approved' | 'rejected') {
  try {
    await store.updateInventoryRequest(id, { status })
    fetchRequests()
    fetchStock() // stock count might change
  } catch (err) {
    console.error(err)
  }
}

async function returnCustody(id: number) {
  if (!confirm('هل تم استرداد هذه العهدة وإرجاعها للمستودع؟')) return
  try {
    await store.updateCustody(id, {
      status: 'returned',
      date_returned: new Date().toISOString().split('T')[0]
    })
    fetchCustodies()
  } catch (err) {
    console.error(err)
  }
}

// Forms submit
async function submitAddItem() {
  try {
    await store.createInventoryItem(itemForm.value)
    showAddItemModal.value = false
    itemForm.value = { code: '', name: '', type: 'stationery', quantity_in_stock: 0, minimum_stock_level: 5, unit: 'حبة' }
    fetchStock()
  } catch (err) {
    console.error(err)
  }
}

async function submitAddRequest() {
  try {
    await store.createInventoryRequest(requestForm.value)
    showAddRequestModal.value = false
    requestForm.value = { requested_by: '', item: '', quantity: 1, notes: '' }
    fetchRequests()
  } catch (err) {
    console.error(err)
  }
}

async function submitAddCustody() {
  try {
    await store.createCustody(custodyForm.value)
    showAddCustodyModal.value = false
    custodyForm.value = { item: '', assigned_to: '', quantity: 1, date_assigned: new Date().toISOString().split('T')[0], notes: '' }
    fetchCustodies()
  } catch (err) {
    console.error(err)
  }
}

// Watch active tab to load data
watch(activeTab, (newTab) => {
  if (newTab === 'stock') fetchStock()
  if (newTab === 'requests') fetchRequests()
  if (newTab === 'custody') fetchCustodies()
})

onMounted(async () => {
  fetchStock()
  // Fetch employees
  await personnelStore.fetchPersonnel()
  employees.value = personnelStore.records || []
})
</script>
