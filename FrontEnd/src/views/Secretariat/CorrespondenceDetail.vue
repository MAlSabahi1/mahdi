<template>
  <admin-layout>
    <!-- Breadcrumbs Navigation -->
    <nav class="flex mb-6" aria-label="Breadcrumb">
      <ol class="flex flex-wrap items-center gap-2 text-xs font-bold text-slate-550 dark:text-slate-400">
        <li class="inline-flex items-center">
          <router-link to="/" class="hover:text-brand-500 dark:hover:text-brand-400 transition flex items-center gap-1.5">
            <Inbox class="w-3.5 h-3.5" />
            الرئيسية
          </router-link>
        </li>
        <li class="flex items-center gap-2">
          <ChevronRight class="w-3 h-3 text-slate-400 rtl:rotate-180" />
          <router-link to="/secretariat/correspondences" class="hover:text-brand-500 dark:hover:text-brand-400 transition">نظام السكرتارية</router-link>
        </li>
        <li class="flex items-center gap-2" v-if="correspondence">
          <ChevronRight class="w-3 h-3 text-slate-400 rtl:rotate-180" />
          <router-link 
            :to="{ path: '/secretariat/correspondences', query: { type: correspondence.type } }"
            class="hover:text-brand-500 dark:hover:text-brand-400 transition text-brand-600 dark:text-brand-400 font-extrabold"
          >
            المراسلات {{ correspondence.type === 'incoming' ? 'الواردة' : 'الصادرة' }}
          </router-link>
        </li>
        <li class="flex items-center gap-2" aria-current="page">
          <ChevronRight class="w-3 h-3 text-slate-400 rtl:rotate-180" />
          <span class="text-slate-800 dark:text-slate-200">تفاصيل المعاملة</span>
        </li>
      </ol>
    </nav>

    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-32 space-y-4">
      <div class="relative w-16 h-16">
        <div class="absolute inset-0 rounded-full border-4 border-brand-500/20"></div>
        <div class="absolute inset-0 rounded-full border-4 border-t-brand-600 animate-spin"></div>
      </div>
      <div class="text-slate-500 dark:text-slate-400 font-bold text-sm">جاري تحميل بيانات المعاملة...</div>
    </div>

    <!-- Error State -->
    <div v-else-if="!correspondence" class="text-center py-20 bg-white dark:bg-slate-900 border border-slate-150 dark:border-slate-850 rounded-3xl p-8 shadow-theme-md max-w-xl mx-auto">
      <div class="w-20 h-20 bg-red-50 dark:bg-red-950/20 text-red-500 flex items-center justify-center rounded-full mx-auto mb-5 shadow-theme-xs">
        <ShieldAlert class="w-10 h-10" />
      </div>
      <h3 class="text-xl font-black text-slate-900 dark:text-white">فشل العثور على المراسلة</h3>
      <p class="text-slate-500 dark:text-slate-400 text-sm mt-2">المراسلة غير موجودة أو تم نقلها لمستودع أرشيف آخر.</p>
      <router-link to="/secretariat/correspondences" class="mt-6 inline-flex items-center gap-2 px-5 py-2.5 bg-brand-500 hover:bg-brand-600 text-white text-xs font-black rounded-xl transition shadow-theme-xs">
        العودة للمراسلات
      </router-link>
    </div>

    <!-- Main Content Redesign -->
    <div v-else class="space-y-6 animate-fade-in">
      <!-- Premium Theme-Integrated Header Panel (Light/Dark Cohesive) -->
      <div class="relative overflow-hidden bg-white dark:bg-slate-900 rounded-3xl p-6 md:p-8 text-slate-800 dark:text-white shadow-sm border border-slate-200/80 dark:border-slate-800 transition-all duration-300">
        <!-- Subtle Premium Gradient Glow -->
        <div class="absolute inset-0 bg-gradient-to-r from-slate-50/50 via-white to-slate-50/30 dark:from-slate-900 dark:via-slate-950/40 dark:to-slate-900 pointer-events-none"></div>
        <div class="absolute -left-24 -bottom-24 w-96 h-96 bg-brand-500/5 dark:bg-brand-500/10 rounded-full blur-3xl pointer-events-none"></div>
        
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 relative z-10">
          <div class="space-y-4">
            <div class="flex flex-wrap items-center gap-2.5">
              <!-- Type Badge -->
              <span
                :class="[
                  'px-3.5 py-1.5 rounded-xl text-xxs font-black tracking-wide uppercase shadow-sm border flex items-center gap-1.5',
                  correspondence.type === 'incoming' 
                    ? 'bg-blue-50 text-blue-700 border-blue-200/60 dark:bg-blue-950/70 dark:text-blue-300 dark:border-blue-800/40' 
                    : 'bg-emerald-50 text-emerald-700 border-emerald-200/60 dark:bg-emerald-950/70 dark:text-emerald-300 dark:border-emerald-800/40'
                ]"
              >
                <component :is="correspondence.type === 'incoming' ? Inbox : Send" class="w-3.5 h-3.5" />
                {{ correspondence.type === 'incoming' ? 'وارد رقمي' : 'صادر رسمي' }}
              </span>

              <!-- Reference Badge -->
              <span class="bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700/65 text-slate-750 dark:text-slate-300 px-3.5 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 shadow-sm">
                <FileText class="w-3.5 h-3.5 text-slate-500 dark:text-slate-400" />
                المرجع: <span class="text-slate-900 dark:text-white font-mono font-black">{{ correspondence.reference_number }}</span>
              </span>

              <!-- Confidentiality Badge -->
              <span 
                :class="[
                  'px-3.5 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 shadow-sm border',
                  correspondence.confidentiality_level === 'normal' ? 'bg-slate-50 border-slate-200 text-slate-750 dark:bg-slate-800 dark:border-slate-700 dark:text-slate-350' :
                  correspondence.confidentiality_level === 'confidential' ? 'bg-blue-50 border-blue-200 text-blue-700 dark:bg-blue-955/50 dark:border-blue-900/40 dark:text-blue-350' :
                  correspondence.confidentiality_level === 'very_confidential' ? 'bg-amber-50 border-amber-200 text-amber-700 dark:bg-amber-955/50 dark:border-amber-900/40 dark:text-amber-350' :
                  'bg-red-50 border-red-200 text-red-700 dark:bg-red-955/50 dark:border-red-900/45 dark:text-red-300'
                ]"
              >
                <ShieldAlert class="w-3.5 h-3.5" />
                السرية: {{ 
                  correspondence.confidentiality_level === 'normal' ? 'عادي' :
                  correspondence.confidentiality_level === 'confidential' ? 'سري' :
                  correspondence.confidentiality_level === 'very_confidential' ? 'سري للغاية' : 'سري جداً'
                }}
              </span>

              <!-- Urgency Badge -->
              <span 
                :class="[
                  'px-3.5 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 shadow-sm border',
                  correspondence.urgency_level === 'normal' ? 'bg-slate-50 border-slate-200 text-slate-750 dark:bg-slate-800 dark:border-slate-700 dark:text-slate-350' :
                  correspondence.urgency_level === 'urgent' ? 'bg-orange-50 border-orange-200 text-orange-700 dark:bg-orange-955/50 dark:border-orange-900/40 dark:text-orange-300' :
                  correspondence.urgency_level === 'very_urgent' ? 'bg-amber-50 border-amber-200 text-amber-700 dark:bg-amber-955/50 dark:border-amber-900/40 dark:text-amber-350' :
                  'bg-red-50 border-red-200 text-red-700 dark:bg-red-955/50 dark:border-red-900/45 dark:text-red-300'
                ]"
              >
                <AlertTriangle class="w-3.5 h-3.5" />
                الاستعجال: {{ 
                  correspondence.urgency_level === 'normal' ? 'عادي' :
                  correspondence.urgency_level === 'urgent' ? 'عاجل' :
                  correspondence.urgency_level === 'very_urgent' ? 'عاجل جداً' : 'فوري'
                }}
              </span>
            </div>

            <!-- Subject Text -->
            <div class="space-y-1.5">
              <span class="text-slate-400 dark:text-slate-500 text-xxs font-black uppercase tracking-wider block">موضوع المعاملة الرسمية</span>
              <h1 class="text-2xl md:text-3.5xl font-black tracking-tight text-slate-900 dark:text-white font-serif leading-tight">
                {{ correspondence.subject }}
              </h1>
            </div>

            <!-- Date Metadata -->
            <div class="flex flex-wrap items-center gap-4 text-slate-500 dark:text-slate-400 text-xs font-bold">
              <span class="flex items-center gap-1.5">
                <Calendar class="w-4 h-4 text-slate-450 dark:text-slate-550" />
                تاريخ تسجيل المعاملة بالمنظومة: <span class="text-slate-800 dark:text-slate-200">{{ correspondence.date }}</span>
              </span>
            </div>
          </div>
          
          <!-- Status Dropdown Switcher -->
          <div class="flex flex-wrap items-center gap-3">
            <div class="flex items-center gap-3 bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/60 p-4 rounded-2xl self-start lg:self-auto shadow-sm">
              <span class="text-slate-650 dark:text-slate-300 text-xs font-black pr-1 flex items-center gap-1.5">
                <Clock class="w-4 h-4 text-amber-555 dark:text-amber-400" />
                حالة القيد والمتابعة:
              </span>
              <select
                v-model="correspondence.status"
                @change="updateStatus"
                class="bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 text-slate-800 dark:text-white rounded-xl px-4 py-2 text-xs font-black focus:outline-none focus:ring-2 focus:ring-brand-500 cursor-pointer shadow-sm transition-all duration-300"
              >
                <option value="new">جديدة (غير مستلمة)</option>
                <option value="in_progress">قيد الفرز والمتابعة</option>
                <option value="completed">مكتملة ومؤرشفة</option>
              </select>
            </div>

            <!-- Outgoing covering letter generator button — only for secretariat managers -->
            <button
              v-if="authStore.hasPermission('secretariat.covering_letter.create')"
              type="button"
              @click="generateCoveringLetter"
              class="flex items-center gap-1.5 px-4 py-3 bg-gradient-to-r from-brand-500 to-indigo-650 hover:from-brand-600 hover:to-indigo-750 text-white rounded-2xl text-xs font-black cursor-pointer transition shadow-md hover:shadow-lg duration-300"
            >
              <Send class="w-4 h-4" />
              توليد خطاب تغطية الرد (صادر)
            </button>
          </div>
        </div>
      </div>

      <!-- High-End Interactive Journey Steps Dashboard -->
      <div class="bg-white dark:bg-gray-900 border border-slate-200/80 dark:border-gray-850 rounded-3xl p-6 shadow-theme-sm">
        <div class="flex items-center gap-2 mb-6 border-b border-gray-100 dark:border-gray-800/60 pb-3">
          <TrendingUp class="w-5 h-5 text-brand-500" />
          <h3 class="text-sm font-black text-slate-800 dark:text-white">مخطط سير المعاملة الرقمية</h3>
        </div>

        <div class="max-w-4xl mx-auto flex flex-col md:flex-row items-stretch md:items-center justify-between gap-6 md:gap-4 relative">
          <!-- Step 1: Registered -->
          <div class="flex items-center gap-4 relative z-10 w-full md:w-auto p-3.5 rounded-2xl bg-brand-50/50 dark:bg-brand-950/20 border border-brand-100/60 dark:border-brand-900/40">
            <div class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm bg-brand-500 text-white shadow-md shadow-brand-500/20">
              <Check class="w-5 h-5" />
            </div>
            <div class="text-right">
              <p class="text-xs font-black text-slate-800 dark:text-white">قيد وتسجيل المعاملة</p>
              <p class="text-[10px] text-slate-400 dark:text-slate-500 font-bold mt-0.5">تم التحقق وإسناد المرجع</p>
            </div>
          </div>

          <div class="hidden md:block flex-grow h-1 mx-2 bg-gradient-to-r from-brand-500 to-brand-500"></div>

          <!-- Step 2: In progress -->
          <div 
            :class="[
              'flex items-center gap-4 relative z-10 w-full md:w-auto p-3.5 rounded-2xl border transition-all duration-300',
              correspondence.status !== 'new'
                ? 'bg-brand-50/50 dark:bg-brand-950/20 border-brand-100/60 dark:border-brand-900/40'
                : 'bg-slate-50 dark:bg-slate-850 border-slate-200 dark:border-slate-800 opacity-60'
            ]"
          >
            <div 
              :class="[
                'w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm shadow-md transition-all duration-300',
                correspondence.status !== 'new' ? 'bg-brand-500 text-white shadow-brand-500/20' : 'bg-slate-200 dark:bg-slate-800 text-slate-550 dark:text-slate-405'
              ]"
            >
              <component :is="correspondence.status !== 'new' ? Check : Clock" class="w-5 h-5" />
            </div>
            <div class="text-right">
              <p class="text-xs font-black text-slate-800 dark:text-white">قيد المتابعة والإحالة</p>
              <p class="text-[10px] text-slate-400 dark:text-slate-500 font-bold mt-0.5">تكليف المتابعين والمهام</p>
            </div>
          </div>

          <div 
            :class="[
              'hidden md:block flex-grow h-1 mx-2 transition-all duration-300',
              correspondence.status === 'completed' ? 'bg-brand-500' : 'bg-slate-200 dark:bg-slate-800'
            ]"
          ></div>

          <!-- Step 3: Completed -->
          <div 
            :class="[
              'flex items-center gap-4 relative z-10 w-full md:w-auto p-3.5 rounded-2xl border transition-all duration-300',
              correspondence.status === 'completed'
                ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-100/60 dark:border-emerald-900/40 animate-pulse-subtle'
                : 'bg-slate-50 dark:bg-slate-850 border-slate-200 dark:border-slate-800 opacity-60'
            ]"
          >
            <div 
              :class="[
                'w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm shadow-md transition-all duration-300',
                correspondence.status === 'completed' ? 'bg-emerald-500 text-white shadow-emerald-500/20' : 'bg-slate-200 dark:bg-slate-800 text-slate-550 dark:text-slate-400'
              ]"
            >
              <component :is="correspondence.status === 'completed' ? Check : Archive" class="w-5 h-5" />
            </div>
            <div class="text-right">
              <p class="text-xs font-black text-slate-800 dark:text-white">الأرشفة والإغلاق النهائي</p>
              <p class="text-[10px] text-slate-400 dark:text-slate-500 font-bold mt-0.5">الحفظ النهائي في الأرشيف</p>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Details Card -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Information Card -->
          <div class="bg-white dark:bg-gray-900 border border-slate-200/80 dark:border-slate-850 rounded-3xl p-6 shadow-theme-sm">
            <div class="flex items-center gap-2 mb-6 border-b border-gray-100 dark:border-gray-800/60 pb-3.5">
              <div class="p-2.5 bg-brand-50 dark:bg-brand-950/40 text-brand-500 dark:text-brand-400 rounded-xl shadow-theme-xs">
                <FileText class="w-5 h-5" />
              </div>
              <h3 class="text-lg font-bold text-slate-850 dark:text-white">بيانات المعاملة الأساسية</h3>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Sender / Receiver Info -->
              <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-900/40 border border-slate-100 dark:border-slate-800/50 shadow-theme-xs">
                <span class="block text-xxs font-black text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2">
                  {{ correspondence.type === 'incoming' ? 'جهة الإرسال المصدرة' : 'جهة الاستلام المستهدفة' }}
                </span>
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-550 flex items-center justify-center shadow-inner flex-shrink-0">
                    <Building class="w-5 h-5" />
                  </div>
                  <span class="text-slate-900 dark:text-white font-extrabold text-[15px]">
                    {{ correspondence.type === 'incoming' ? correspondence.sender || 'غير محدد' : correspondence.receiver || 'غير محدد' }}
                  </span>
                </div>
              </div>
              
              <!-- Date Card -->
              <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-900/40 border border-slate-100 dark:border-slate-800/50 shadow-theme-xs">
                <span class="block text-xxs font-black text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2">تاريخ تسجيل المعاملة</span>
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-950/40 text-amber-550 flex items-center justify-center shadow-inner flex-shrink-0">
                    <Calendar class="w-5 h-5" />
                  </div>
                  <span class="text-slate-900 dark:text-white font-extrabold text-[15px]">{{ correspondence.date }}</span>
                </div>
              </div>

              <!-- Paper Barcode Card -->
              <div v-if="correspondence.barcode_data" class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-900/40 border border-slate-100 dark:border-slate-800/50 shadow-theme-xs">
                <span class="block text-xxs font-black text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2">الباركود الورقي للملف الورقي</span>
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800/40 text-slate-500 flex items-center justify-center shadow-inner flex-shrink-0">
                    <Barcode class="w-5 h-5" />
                  </div>
                  <span class="text-slate-900 dark:text-white font-mono font-black text-[15px]">{{ correspondence.barcode_data }}</span>
                </div>
              </div>
              
              <!-- Tracking UUID & QR Code Card -->
              <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-900/40 border border-slate-100 dark:border-slate-800/50 shadow-theme-xs md:col-span-2 flex flex-col md:flex-row items-center justify-between gap-4">
                <div class="flex items-center gap-3 w-full md:w-auto">
                  <div class="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-550 flex items-center justify-center shadow-inner flex-shrink-0">
                    <QrCode class="w-5 h-5" />
                  </div>
                  <div class="overflow-hidden">
                    <span class="block text-xxs font-black text-slate-400 dark:text-slate-500 uppercase tracking-wider">رمز التتبع الرقمي الفريد (QR)</span>
                    <span class="text-slate-900 dark:text-white font-mono text-xs block truncate select-all">{{ correspondence.tracking_token }}</span>
                  </div>
                </div>
                <!-- QR Code Image -->
                <div class="flex-shrink-0 flex items-center gap-2 bg-white p-2 rounded-xl border border-slate-200 shadow-sm">
                  <img :src="`https://api.qrserver.com/v1/create-qr-code/?size=80x80&data=${encodeURIComponent(getTrackingUrl())}`" alt="Tracking QR Code" class="w-16 h-16" />
                </div>
              </div>
              
              <!-- Directives / Notes Panel -->
              <div class="md:col-span-2">
                <span class="block text-xs font-black text-slate-455 dark:text-slate-550 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <Bookmark class="w-4 h-4 text-brand-500" />
                  توجيهات وشروحات القيادة العليا
                </span>
                <div class="relative p-5 rounded-2xl bg-amber-50/40 dark:bg-amber-950/10 border border-amber-500/20 leading-relaxed font-semibold shadow-theme-xs">
                  <div class="absolute top-4 right-4 text-amber-500/10 select-none font-serif text-6xl leading-none">“</div>
                  <p class="text-slate-750 dark:text-slate-350 text-[14.5px] whitespace-pre-line pr-6 relative z-10 leading-relaxed font-medium">
                    {{ correspondence.notes || 'لا توجد ملاحظات أو توجيهات مدونة لهذه المراسلة.' }}
                  </p>
                </div>
              </div>

              <!-- Linked/Related Correspondences Section -->
              <div class="md:col-span-2 border-t border-slate-100 dark:border-slate-800/60 pt-4 mt-2">
                <span class="block text-xs font-black text-slate-455 dark:text-slate-550 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <Link2 class="w-4 h-4 text-indigo-500" />
                  المعاملات المرتبطة والردود
                </span>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <!-- Parent Correspondence -->
                  <div v-if="correspondence.parent_correspondence" class="p-4 rounded-xl bg-indigo-50/30 dark:bg-indigo-950/10 border border-indigo-500/10 shadow-theme-xs flex items-center justify-between">
                    <div>
                      <span class="block text-[10px] text-indigo-500 font-black mb-1">رد على الخطاب الوارد:</span>
                      <router-link :to="`/secretariat/correspondences/${correspondence.parent_correspondence}`" class="text-xs font-bold text-slate-850 dark:text-slate-200 hover:text-brand-500 transition duration-300">
                        عرض المراسلة الأصلية 🔗
                      </router-link>
                    </div>
                  </div>
                  
                  <!-- Replies (Child correspondences) -->
                  <div v-if="correspondence.replies && correspondence.replies.length > 0" class="p-4 rounded-xl bg-green-50/30 dark:bg-green-950/10 border border-green-500/10 shadow-theme-xs md:col-span-2">
                    <span class="block text-[10px] text-green-555 font-black mb-1.5">الردود الصادرة المرتبطة:</span>
                    <div class="space-y-1.5">
                      <div v-for="reply in correspondence.replies" :key="reply.id" class="flex items-center justify-between text-xs border-b border-dashed border-slate-100 dark:border-slate-800 pb-1.5 last:border-0 last:pb-0">
                        <router-link :to="`/secretariat/correspondences/${reply.id}`" class="font-bold text-slate-700 dark:text-slate-300 hover:text-brand-500 transition">
                          {{ reply.reference_number }} - {{ reply.subject }}
                        </router-link>
                        <span class="text-[10px] px-1.5 py-0.5 bg-green-105 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded font-bold">مكتملة</span>
                      </div>
                    </div>
                  </div>
                  
                  <!-- If neither -->
                  <div v-if="!correspondence.parent_correspondence && (!correspondence.replies || correspondence.replies.length === 0)" class="text-xs text-slate-400 font-medium py-1">
                    لا توجد مراسلات مرتبطة أو ردود مقيدة لهذه المعاملة بعد.
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- Sequential Referrals & Directives Card -->
          <div class="bg-white dark:bg-gray-900 border border-slate-200/80 dark:border-slate-850 rounded-3xl p-6 shadow-theme-sm">
            <div class="flex justify-between items-center mb-6 border-b border-gray-100 dark:border-gray-800/60 pb-3.5">
              <div class="flex items-center gap-2">
                <div class="p-2.5 bg-brand-50 dark:bg-brand-950/40 text-brand-500 dark:text-brand-400 rounded-xl shadow-theme-xs">
                  <TrendingUp class="w-5 h-5" />
                </div>
                <h3 class="text-lg font-bold text-slate-855 dark:text-white">الإحالات والتوجيهات المتسلسلة (دورة حياة المعاملة)</h3>
              </div>
              <!-- Only show 'Add Referral' button to task managers (secretariat) -->
              <button
                v-if="authStore.hasPermission('secretariat.task.manage')"
                @click="showReferralForm = !showReferralForm"
                class="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-50 text-slate-700 hover:bg-slate-100 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-750 text-xs font-black transition-all duration-300 cursor-pointer shadow-theme-xs border border-slate-200 dark:border-slate-700"
              >
                <Plus class="w-4 h-4" />
                <span>{{ showReferralForm ? 'إلغاء' : 'إحالة وتوجيه جديدة' }}</span>
              </button>
            </div>

            <!-- Add Referral Form -->
            <div v-if="showReferralForm" class="mb-6 p-5 bg-slate-50/50 dark:bg-slate-855/40 border border-slate-200 dark:border-slate-800 rounded-2xl animate-fade-in">
              <form @submit.prevent="submitReferral" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-xs font-black text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-1.5">الموظف المحال إليه (المكلف بالتنفيذ) *</label>
                    <select
                      v-model="referralForm.referred_to"
                      required
                      class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-gray-800 px-4 py-2.5 text-sm text-slate-800 dark:text-white cursor-pointer focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition duration-300 font-bold"
                    >
                      <option value="" disabled>اختر الموظف...</option>
                      <option v-for="emp in employees" :key="emp.military_number" :value="emp.military_number">
                        {{ emp.full_name }} ({{ emp.military_number }})
                      </option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-xs font-black text-slate-400 dark:text-slate-550 uppercase tracking-wider mb-1.5">تاريخ الإنجاز المطلوب *</label>
                    <input
                      v-model="referralForm.due_date"
                      type="date"
                      required
                      class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-gray-800 px-4 py-2.5 text-sm text-slate-800 dark:text-white cursor-pointer focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition duration-300 font-bold"
                    />
                  </div>
                </div>

                <div>
                  <label class="block text-xs font-black text-slate-400 dark:text-slate-550 uppercase tracking-wider mb-1.5">شرح وتوجيهات المدير العام أو رئيس القسم *</label>
                  <textarea
                    v-model="referralForm.instructions"
                    required
                    rows="3"
                    placeholder="اكتب التوجيهات الرسمية الواجب اتباعها عند استلام المعاملة..."
                    class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-gray-800 px-4 py-2.5 text-sm text-slate-800 dark:text-white focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition duration-300 font-bold"
                  ></textarea>
                </div>

                <div class="flex justify-end gap-2">
                  <button
                    type="submit"
                    :disabled="submittingReferral"
                    class="px-5 py-2.5 text-xs font-black text-white bg-brand-500 hover:bg-brand-600 rounded-xl shadow-theme-xs disabled:opacity-50 transition cursor-pointer"
                  >
                    {{ submittingReferral ? 'جاري تسجيل الإحالة...' : 'تأكيد إحالة المعاملة' }}
                  </button>
                </div>
              </form>
            </div>

            <!-- Referrals Timeline / List -->
            <div v-if="!referralsList || referralsList.length === 0" class="text-center py-12 bg-slate-50/50 dark:bg-slate-850/10 rounded-2xl border border-dashed border-slate-200 dark:border-slate-800 text-sm text-slate-500">
              <TrendingUp class="w-12 h-12 mx-auto text-slate-300 dark:text-slate-700 mb-3" />
              لم يتم إجراء أي إحالات متسلسلة لهذه المعاملة بعد.
            </div>

            <div v-else class="space-y-6 relative border-r-2 border-slate-200 dark:border-slate-800 mr-4 pr-6 py-2">
              <div
                v-for="(refItem, index) in referralsList"
                :key="refItem.id"
                class="relative space-y-2 animate-fade-in"
              >
                <!-- Dot icon indicator -->
                <div class="absolute -right-[31px] top-1.5 w-4 h-4 rounded-full border-2 border-brand-500 bg-white dark:bg-slate-900 flex items-center justify-center">
                  <div class="w-1.5 h-1.5 rounded-full bg-brand-500"></div>
                </div>

                <div class="flex flex-wrap items-center justify-between gap-2">
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-black text-brand-600 dark:text-brand-400">الإحالة #{{ referralsList.length - index }}</span>
                    <span class="text-slate-400 text-[10px]">|</span>
                    <span class="text-slate-500 dark:text-slate-400 text-xxs font-bold">
                      تمت في: {{ new Date(refItem.created_at).toLocaleDateString('ar-YE', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }) }}
                    </span>
                  </div>
                  
                  <span
                    :class="[
                      'px-2 py-0.5 rounded text-[10px] font-bold w-max text-center',
                      refItem.status === 'pending' ? 'bg-amber-50 text-amber-700 dark:bg-amber-950/20 dark:text-amber-400' :
                      refItem.status === 'completed' ? 'bg-green-50 text-green-700 dark:bg-green-950/20 dark:text-green-400' :
                      'bg-slate-100 text-slate-650 dark:bg-slate-855'
                    ]"
                  >
                    {{ 
                      refItem.status === 'pending' ? 'قيد المتابعة' :
                      refItem.status === 'completed' ? 'تم الإنجاز' : 'أخرى'
                    }}
                  </span>
                </div>

                <div class="p-4 bg-slate-50 dark:bg-slate-900/60 border border-slate-205 dark:border-slate-800 rounded-2xl shadow-theme-xs">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs font-bold text-slate-705 dark:text-slate-350 mb-3 border-b border-slate-200/50 dark:border-slate-850 pb-2">
                    <div>
                      <span class="text-slate-400 font-medium">المحيل (الموجه):</span> {{ refItem.referred_by_name || 'المدير العام' }}
                    </div>
                    <div>
                      <span class="text-slate-400 font-medium">المحال إليه (المكلف):</span> {{ refItem.referred_to_name || 'موظف مختص' }}
                    </div>
                  </div>

                  <div class="text-xs text-slate-650 dark:text-slate-400 leading-relaxed">
                    <span class="block text-xxs font-black text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-1">التوجيهات والشرح:</span>
                    <p class="whitespace-pre-line font-medium pr-1">{{ refItem.instructions }}</p>
                  </div>

                  <!-- Employee Response Notes -->
                  <div v-if="refItem.notes" class="mt-3 pt-2.5 border-t border-dashed border-slate-200 dark:border-slate-800 text-xs leading-relaxed bg-green-50/20 dark:bg-green-950/5 p-3 rounded-xl">
                    <span class="block text-xxs font-black text-green-600 dark:text-green-400 uppercase tracking-wider mb-1">رد الموظف وملاحظات الإنجاز:</span>
                    <p class="whitespace-pre-line font-bold pr-1 text-slate-800 dark:text-slate-200">{{ refItem.notes }}</p>
                  </div>

                  <!-- Completion Actions for Assigned Personnel -->
                  <div v-if="authStore.user?.username === refItem.referred_to && refItem.status === 'pending'" class="mt-4 pt-3 border-t border-dashed border-slate-200 dark:border-slate-800 flex justify-end">
                    <button
                      type="button"
                      @click="completeReferralTask(refItem.id)"
                      class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-xs font-black rounded-xl cursor-pointer transition shadow-theme-xs flex items-center gap-1.5"
                    >
                      <Check class="w-3.5 h-3.5" />
                      تأكيد إنجاز التوجيه والمعاملة
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Digital Archive Vault (Attachments Section) -->
          <div class="bg-white dark:bg-gray-900 border border-slate-200/85 dark:border-slate-850 rounded-3xl p-6 shadow-theme-sm">
            <div class="flex justify-between items-center mb-6 border-b border-gray-100 dark:border-gray-800/60 pb-3.5">
              <div class="flex items-center gap-2">
                <div class="p-2.5 bg-brand-50 dark:bg-brand-950/40 text-brand-500 dark:text-brand-400 rounded-xl shadow-theme-xs">
                  <FolderOpen class="w-5 h-5" />
                </div>
                <h3 class="text-lg font-bold text-slate-850 dark:text-white">مستودع الأرشيف الرقمي المرفق</h3>
              </div>
              <button
                @click="showUploadForm = !showUploadForm"
                class="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-50 text-slate-700 hover:bg-slate-100 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-750 text-xs font-black transition-all duration-300 cursor-pointer shadow-theme-xs border border-slate-200 dark:border-slate-700"
              >
                <Plus class="w-4 h-4" />
                <span>{{ showUploadForm ? 'إلغاء الإرفاق' : 'إرفاق وثيقة جديدة' }}</span>
              </button>
            </div>

            <!-- Upload attachment form (Advanced Dropzone Style) -->
            <div v-if="showUploadForm" class="mb-6 p-5 bg-slate-50/50 dark:bg-slate-850/40 border border-slate-200 dark:border-slate-800 rounded-2xl animate-fade-in">
              <form @submit.prevent="handleUpload" class="space-y-4">
                <div>
                  <label class="block text-xs font-black text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-1.5">عنوان المستند المرفق *</label>
                  <input
                    v-model="attachmentForm.title"
                    type="text"
                    required
                    placeholder="مثال: صورة المذكرة الرسمية، الرد الرسمي المعمد، إلخ"
                    class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-gray-800 px-4 py-2.5 text-sm text-slate-800 dark:text-white focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition duration-300 font-bold"
                  />
                </div>
                
                <!-- Dropzone Style File Upload -->
                <div>
                  <label class="block text-xs font-black text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2">اختر الملف المؤرشف *</label>
                  <div class="relative border-2 border-dashed border-slate-300 dark:border-slate-700 rounded-xl p-6 hover:bg-slate-100/50 dark:hover:bg-slate-800/30 transition-all duration-300 flex flex-col items-center justify-center text-center cursor-pointer">
                    <input
                      type="file"
                      required
                      @change="onFileSelected"
                      class="absolute inset-0 w-full h-full opacity-0 cursor-pointer animate-none"
                    />
                    
                    <div v-if="selectedFilePreview" class="flex flex-col items-center">
                      <img :src="selectedFilePreview" class="w-32 h-20 object-cover rounded-lg mb-2 shadow-sm border border-slate-200" />
                      <p class="text-xs font-bold text-brand-600 dark:text-brand-400">تم اختيار الصورة بنجاح</p>
                      <p class="text-[10px] text-slate-400 mt-0.5">{{ attachmentForm.file?.name }}</p>
                    </div>
                    <div v-else-if="attachmentForm.file" class="flex flex-col items-center">
                      <FileText class="w-10 h-10 text-brand-500 mb-2" />
                      <p class="text-xs font-bold text-brand-600 dark:text-brand-400">تم اختيار المستند بنجاح</p>
                      <p class="text-[10px] text-slate-400 mt-0.5">{{ attachmentForm.file.name }}</p>
                    </div>
                    <div v-else class="flex flex-col items-center">
                      <Paperclip class="w-10 h-10 text-slate-400 dark:text-slate-650 mb-2" />
                      <p class="text-sm font-bold text-slate-700 dark:text-slate-300">
                        اضغط لتصفح الملف من جهازك
                      </p>
                      <p class="text-xxs text-slate-400 dark:text-slate-500 mt-1">يُقبل جميع أنواع الملفات المعتمدة (PDF، صور، مستندات)</p>
                    </div>
                  </div>
                </div>

                <div class="flex justify-end gap-2 pt-2">
                  <button
                    type="submit"
                    :disabled="uploading"
                    class="px-5 py-2.5 text-xs font-black text-white bg-brand-500 hover:bg-brand-600 rounded-xl shadow-theme-xs disabled:opacity-50 transition cursor-pointer"
                  >
                    {{ uploading ? 'جاري رفع الملف...' : 'حفظ المستند بالأرشيف' }}
                  </button>
                </div>
              </form>
            </div>

            <!-- Attachments grid list -->
            <div v-if="!correspondence.attachments || correspondence.attachments.length === 0" class="text-center py-12 bg-slate-50/50 dark:bg-slate-850/10 rounded-2xl border border-dashed border-slate-200 dark:border-slate-800 text-sm text-slate-500">
              <FolderOpen class="w-12 h-12 mx-auto text-slate-300 dark:text-slate-700 mb-3" />
              لا توجد مستندات مرفقة مؤرشفة حالياً لهذه المعاملة.
            </div>
            
            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4 animate-fade-in">
              <div
                v-for="file in correspondence.attachments"
                :key="file.id"
                class="flex flex-col p-4 bg-slate-50 dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-2xl hover:shadow-md hover:-translate-y-0.5 transition-all duration-300 shadow-theme-xs"
              >
                <!-- Thumbnail Preview (Image or File Icon Banner) -->
                <div v-if="isImage(file.file)" class="relative w-full h-36 rounded-xl overflow-hidden mb-3 bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-center group/img">
                  <img :src="file.file" alt="Attachment Preview" class="w-full h-full object-cover transition-transform duration-500 group-hover/img:scale-110" />
                  <div class="absolute inset-0 bg-black/40 opacity-0 group-hover/img:opacity-100 transition-opacity duration-300 flex items-center justify-center gap-2">
                    <a :href="file.file" target="_blank" class="p-2 bg-white/20 hover:bg-white/30 backdrop-blur-md rounded-full text-white transition-all duration-350 transform translate-y-2 group-hover/img:translate-y-0">
                      <Eye class="w-5 h-5" />
                    </a>
                  </div>
                </div>
                <div v-else class="relative w-full h-36 rounded-xl bg-slate-100/50 dark:bg-slate-850/50 border border-slate-200 dark:border-slate-800 flex flex-col items-center justify-center mb-3">
                  <FileText class="w-10 h-10 text-slate-400 dark:text-slate-600 mb-1" />
                  <span class="text-[10px] font-black text-slate-450 dark:text-slate-500 uppercase">{{ getFileExtension(file.file) }}</span>
                </div>

                <div class="flex items-center gap-3 overflow-hidden mb-4">
                  <div class="overflow-hidden">
                    <span class="block text-sm font-black text-slate-850 dark:text-white truncate" :title="file.title">
                      {{ file.title }}
                    </span>
                    <span class="block text-[10px] text-slate-450 dark:text-slate-500 mt-0.5 font-bold">
                      تاريخ الأرشفة: {{ new Date(file.uploaded_at).toLocaleDateString('ar-YE', { year: 'numeric', month: 'long', day: 'numeric' }) }}
                    </span>
                  </div>
                </div>
                
                <div class="flex items-center justify-between mt-auto pt-3.5 border-t border-slate-100 dark:border-slate-800/60">
                  <span class="text-[10px] bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 px-2.5 py-0.5 rounded font-black uppercase">
                    وثيقة معمدة
                  </span>
                  
                  <div class="flex items-center gap-2">
                    <a
                      :href="file.file"
                      target="_blank"
                      class="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-750 text-slate-700 dark:text-slate-350 text-xs font-black transition-all duration-300 shadow-theme-xs border border-slate-200 dark:border-slate-700"
                      title="تحميل"
                    >
                      <Download class="w-3.5 h-3.5" />
                      تحميل
                    </a>
                    <button
                      @click="deleteFile(file.id)"
                      class="p-2 text-slate-450 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/20 rounded-lg transition-all duration-300 cursor-pointer"
                      title="حذف"
                    >
                      <Trash2 class="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar Actions & Linked Tasks -->
        <div class="space-y-6">
          <!-- Officer in Charge Card -->
          <div class="bg-white dark:bg-gray-900 border border-slate-200/80 dark:border-slate-850 rounded-3xl p-6 shadow-theme-sm">
            <h3 class="text-xs font-black text-slate-455 dark:text-slate-500 uppercase tracking-wider mb-4">مسؤول المراسلة وقيد التسجيل</h3>
            <div class="flex items-center gap-3 p-3.5 bg-slate-50 dark:bg-slate-900/30 border border-slate-100 dark:border-slate-800/60 rounded-2xl shadow-theme-xs">
              <div class="w-11 h-11 rounded-full bg-brand-50 dark:bg-brand-900/20 text-brand-600 dark:text-brand-400 flex items-center justify-center font-black shadow-inner flex-shrink-0 text-base">
                {{ (correspondence.created_by_name || 'U').charAt(0).toUpperCase() }}
              </div>
              <div class="overflow-hidden">
                <span class="block text-sm font-black text-slate-850 dark:text-white truncate">بواسطة: {{ correspondence.created_by_name || 'مسؤول السكرتارية' }}</span>
                <span class="block text-xs text-slate-450 dark:text-slate-500 truncate mt-0.5">جهة الاختصاص: {{ correspondence.security_admin_name || 'إدارة الأمن' }}</span>
              </div>
            </div>
          </div>

          <!-- Tasks list and Add Task linked to correspondence -->
          <div class="bg-white dark:bg-gray-900 border border-slate-200/80 dark:border-slate-850 rounded-3xl p-6 shadow-theme-sm">
            <div class="flex justify-between items-center mb-4 border-b border-gray-100 dark:border-gray-855 pb-3">
              <div class="flex items-center gap-2">
                <div class="p-2 bg-brand-50 dark:bg-brand-950/40 text-brand-500 dark:text-brand-400 rounded-xl">
                  <Briefcase class="w-4 h-4" />
                </div>
                <h3 class="text-base font-black text-slate-850 dark:text-white">مهام المتابعة والتكليف</h3>
              </div>
              <!-- Only show 'Add Task' button to users with task management permission -->
              <button
                v-if="authStore.hasPermission('secretariat.task.manage')"
                @click="showTaskForm = !showTaskForm"
                class="inline-flex items-center gap-1 text-xs font-black text-brand-600 hover:text-brand-700 dark:text-brand-400 cursor-pointer transition-all duration-300"
              >
                <Plus class="w-3.5 h-3.5" />
                {{ showTaskForm ? 'إلغاء' : 'تكليف جديد' }}
              </button>
            </div>

            <!-- Task Form -->
            <div v-if="showTaskForm" class="mb-5 p-4 bg-slate-50 dark:bg-slate-850/40 border border-slate-200 dark:border-slate-800 rounded-2xl animate-fade-in space-y-4">
              <div>
                <label class="block text-xs font-black text-slate-450 dark:text-slate-500 uppercase tracking-wider mb-1">عنوان التكليف أو الأمر *</label>
                <input
                  v-model="taskForm.title"
                  type="text"
                  required
                  placeholder="مثال: مراجعة المستند والتأكد من الصلاحيات"
                  class="w-full rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-3 py-2 text-sm text-slate-800 dark:text-white focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition duration-300"
                />
              </div>
              <div>
                <label class="block text-xs font-black text-slate-455 dark:text-slate-500 uppercase tracking-wider mb-1">تفاصيل ومبررات المهمة</label>
                <textarea
                  v-model="taskForm.description"
                  rows="2"
                  placeholder="اكتب التوجيهات أو الملاحظات التفصيلية هنا..."
                  class="w-full rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-3 py-2 text-sm text-slate-800 dark:text-white focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition duration-300"
                ></textarea>
              </div>
              <div>
                <label class="block text-xs font-black text-slate-455 dark:text-slate-500 uppercase tracking-wider mb-1">الموظف المسؤول *</label>
                <select
                  v-model="taskForm.assigned_to"
                  required
                  class="w-full rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-3 py-2 text-sm text-slate-800 dark:text-white cursor-pointer focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition duration-300"
                >
                  <option value="" disabled>اختر الموظف...</option>
                  <option v-for="emp in employees" :key="emp.military_number" :value="emp.military_number">
                    {{ emp.full_name }} ({{ emp.military_number }})
                  </option>
                </select>
              </div>
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="block text-xs font-black text-slate-455 dark:text-slate-500 uppercase tracking-wider mb-1">تاريخ الاستحقاق *</label>
                  <input
                    v-model="taskForm.due_date"
                    type="date"
                    required
                    class="w-full rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-3 py-2 text-sm text-slate-800 dark:text-white cursor-pointer focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition duration-300"
                  />
                </div>
                <div>
                  <label class="block text-xs font-black text-slate-455 dark:text-slate-500 uppercase tracking-wider mb-1">الأولوية</label>
                  <select
                    v-model="taskForm.priority"
                    class="w-full rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-3 py-2 text-sm text-slate-800 dark:text-white cursor-pointer focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition duration-300"
                  >
                    <option value="low">منخفضة</option>
                    <option value="medium">متوسطة</option>
                    <option value="high">عالية</option>
                  </select>
                </div>
              </div>
              <div class="flex justify-end pt-1">
                <button
                  type="button"
                  @click="handleAddTask"
                  class="px-5 py-2 text-xs font-black text-white bg-brand-500 hover:bg-brand-600 rounded-xl cursor-pointer transition shadow-theme-xs"
                >
                  حفظ وتكليف
                </button>
              </div>
            </div>

            <!-- Linked Tasks list -->
            <div v-if="linkedTasks.length === 0" class="text-center py-8 text-xs text-slate-500">
              <Briefcase class="w-10 h-10 mx-auto text-slate-350 dark:text-slate-700 mb-2" />
              لا توجد مهام متابعة نشطة لهذه المراسلة.
            </div>
            <div v-else class="space-y-3">
              <div
                v-for="task in linkedTasks"
                :key="task.id"
                :class="[
                  'p-4 border rounded-2xl bg-slate-50 dark:bg-slate-900/20 hover:shadow-md transition-all duration-300 shadow-theme-xs',
                  task.priority === 'high' ? 'border-red-500/20' : 'border-slate-205 dark:border-slate-800'
                ]"
              >
                <div class="flex justify-between items-start gap-2">
                  <span class="text-sm font-black text-slate-850 dark:text-white leading-snug">{{ task.title }}</span>
                  <span
                    :class="[
                      'text-xxs px-2.5 py-0.5 rounded-full font-black',
                      task.status === 'completed' ? 'bg-green-50 text-green-700 dark:bg-green-950/20 dark:text-green-400' :
                      task.status === 'in_progress' ? 'bg-amber-50 text-amber-700 dark:bg-amber-950/20 dark:text-amber-400' :
                      'bg-slate-100 text-slate-700 dark:bg-gray-800 dark:text-gray-400'
                    ]"
                  >
                    {{ task.status_display }}
                  </span>
                </div>
                <p class="mt-2 text-xs text-slate-650 dark:text-slate-400 font-medium whitespace-pre-line">{{ task.description }}</p>
                <div v-if="task.notes" class="mt-2.5 p-3 rounded-xl bg-green-50/20 dark:bg-green-950/5 border border-dashed border-green-500/20 text-xs">
                  <span class="block text-xxs font-black text-green-600 dark:text-green-400 uppercase tracking-wider mb-1">رد الموظف وملاحظات الإنجاز:</span>
                  <p class="font-bold text-slate-800 dark:text-slate-200 whitespace-pre-line">{{ task.notes }}</p>
                </div>
                <div class="mt-3 flex flex-col gap-1.5 text-xxs text-slate-450 dark:text-slate-500 font-bold">
                  <div class="flex items-center gap-1">
                    <UserCheck class="w-3.5 h-3.5 text-brand-500" />
                    <span class="text-slate-400">المكلف:</span>
                    <span class="text-slate-800 dark:text-slate-300 font-extrabold">{{ task.assigned_to_name || 'غير محدد' }}</span>
                  </div>
                  <div class="flex justify-between items-center mt-2 pt-2 border-t border-slate-150 dark:border-slate-800/40">
                    <span class="flex items-center gap-0.5">الاستحقاق: {{ task.due_date }}</span>
                    <span
                      :class="[
                        'font-black uppercase text-[9px] px-2 py-0.5 rounded-md',
                        task.priority === 'high' ? 'bg-red-50 text-red-650 dark:bg-red-950/30' :
                        task.priority === 'medium' ? 'bg-amber-50 text-amber-650 dark:bg-amber-950/30' : 'bg-slate-100 text-slate-650 dark:bg-slate-850'
                      ]"
                    >
                      أولوية: {{ task.priority_display }}
                    </span>
                  </div>

                  <!-- Task Actions for Assignee -->
                  <div v-if="authStore.user?.username === task.assigned_to" class="mt-3 pt-2 border-t border-dashed border-slate-200 dark:border-slate-800 flex gap-2">
                    <button
                      v-if="task.status === 'pending'"
                      type="button"
                      @click="handleAcceptTask(task)"
                      class="flex-1 py-1.5 px-3 text-center text-[10px] font-black text-white bg-amber-500 hover:bg-amber-600 rounded-lg cursor-pointer transition"
                    >
                      استلام المهمة وبدء العمل
                    </button>
                    <button
                      v-if="task.status === 'in_progress'"
                      type="button"
                      @click="handleCompleteTask(task)"
                      class="flex-1 py-1.5 px-3 text-center text-[10px] font-black text-white bg-green-600 hover:bg-green-750 rounded-lg cursor-pointer transition"
                    >
                      تأكيد إنجاز المهمة وتسليم الكشف
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import api from '@/lib/api'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useSecretariatStore } from '@/stores/secretariat'
import { usePersonnelStore } from '@/stores/personnel'
import { useAuthStore } from '@/stores/auth'
import Swal from 'sweetalert2'

// Lucide Icons Import
import { 
  FileText, Calendar, ArrowRight, User, CheckCircle2, Clock, 
  ShieldAlert, Paperclip, Plus, Trash2, Download, ExternalLink, 
  Check, AlertCircle, Briefcase, ChevronRight, File, Archive, Send, Inbox,
  UserCheck, Building, Bookmark, TrendingUp, AlertTriangle, FolderOpen, Eye,
  Barcode, QrCode, Link2
} from 'lucide-vue-next'

const { t } = useI18n()
const store = useSecretariatStore()
const personnelStore = usePersonnelStore()
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const loading = ref(true)
const uploading = ref(false)
const correspondence = ref<any>(null)
const linkedTasks = ref<any[]>([])
const employees = ref<any[]>([])

const showUploadForm = ref(false)
const showTaskForm = ref(false)

const attachmentForm = ref({
  title: '',
  file: null as File | null
})

const selectedFilePreview = ref<string | null>(null)

const taskForm = ref({
  title: '',
  description: '',
  assigned_to: '',
  priority: 'medium',
  due_date: new Date(Date.now() + 86400000 * 3).toISOString().split('T')[0], // 3 days in future
  related_correspondence: ''
})

function isImage(url: string) {
  if (!url) return false
  const ext = url.split('.').pop()?.toLowerCase()
  return ['jpg', 'jpeg', 'png', 'webp', 'gif', 'svg'].includes(ext || '')
}

function getFileExtension(url: string) {
  if (!url) return 'FILE'
  return url.split('.').pop()?.toUpperCase() || 'FILE'
}

async function fetchDetails() {
  loading.value = true
  try {
    const id = route.params.id as string
    const res = await store.fetchCorrespondenceById(id)
    correspondence.value = res
    
    // Fetch linked tasks
    const tasksRes = await store.fetchTasks({ related_correspondence: id })
    linkedTasks.value = tasksRes.results || []

    // Fetch referrals
    await fetchReferralsList()

    // Fetch personnel for task assignment
    if (employees.value.length === 0) {
      await personnelStore.fetchPersonnel()
      employees.value = personnelStore.records || []
    }
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function updateStatus() {
  try {
    const id = route.params.id as string
    await store.updateCorrespondence(id, { status: correspondence.value.status })
    // fetch again to update displays
    const res = await store.fetchCorrespondenceById(id)
    correspondence.value = res
  } catch (err) {
    console.error(err)
  }
}

function onFileSelected(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    const file = target.files[0]
    attachmentForm.value.file = file
    if (file.type.startsWith('image/')) {
      selectedFilePreview.value = URL.createObjectURL(file)
    } else {
      selectedFilePreview.value = null
    }
  }
}

async function handleUpload() {
  if (!attachmentForm.value.file || !attachmentForm.value.title) return
  uploading.value = true
  try {
    const id = route.params.id as string
    const formData = new FormData()
    formData.append('correspondence', id)
    formData.append('title', attachmentForm.value.title)
    formData.append('file', attachmentForm.value.file)

    await store.uploadAttachment(formData)
    showUploadForm.value = false
    attachmentForm.value = { title: '', file: null }
    selectedFilePreview.value = null
    
    // Refresh
    const res = await store.fetchCorrespondenceById(id)
    correspondence.value = res
  } catch (err) {
    console.error(err)
  } finally {
    uploading.value = false
  }
}

async function deleteFile(fileId: number) {
  if (!confirm('هل أنت متأكد من رغبتك في حذف هذا الملف المرفق؟')) return
  try {
    await store.deleteAttachment(fileId)
    const id = route.params.id as string
    const res = await store.fetchCorrespondenceById(id)
    correspondence.value = res
  } catch (err) {
    console.error(err)
  }
}

async function handleAddTask() {
  if (!taskForm.value.title) {
    Swal.fire({ icon: 'warning', title: 'الرجاء إدخال عنوان التكليف' })
    return
  }
  if (!taskForm.value.assigned_to) {
    Swal.fire({ icon: 'warning', title: 'الرجاء اختيار الموظف المكلف' })
    return
  }
  try {
    const id = route.params.id as string
    taskForm.value.related_correspondence = id
    await store.createTask(taskForm.value)
    
    Swal.fire({ icon: 'success', title: 'تم حفظ وإسناد التكليف بنجاح', timer: 1500, showConfirmButton: false })
    
    // reset task form
    taskForm.value = {
      title: '',
      description: '',
      assigned_to: '',
      priority: 'medium',
      due_date: new Date(Date.now() + 86400000 * 3).toISOString().split('T')[0],
      related_correspondence: ''
    }
    showTaskForm.value = false
    
    // Refresh tasks list
    const tasksRes = await store.fetchTasks({ related_correspondence: id })
    linkedTasks.value = tasksRes.results || []
  } catch (err: any) {
    console.error(err)
    const errMsg = err.response?.data?.error || err.response?.data?.detail || 'حدث خطأ أثناء حفظ التكليف'
    Swal.fire({ icon: 'error', title: 'فشل حفظ التكليف', text: JSON.stringify(errMsg) })
  }
}

async function handleAcceptTask(task: any) {
  try {
    await store.updateTask(task.id, { status: 'in_progress' })
    Swal.fire({
      icon: 'success',
      title: 'تم استلام المهمة بنجاح وبدء العمل',
      timer: 1500,
      showConfirmButton: false
    })
    // Refresh tasks list
    const id = route.params.id as string
    const tasksRes = await store.fetchTasks({ related_correspondence: id })
    linkedTasks.value = tasksRes.results || []
  } catch (err: any) {
    console.error(err)
    Swal.fire({
      icon: 'error',
      title: 'حدث خطأ أثناء استلام المهمة',
      text: err.response?.data?.error || ''
    })
  }
}

async function handleCompleteTask(task: any) {
  const { value: notes } = await Swal.fire({
    title: 'إكمال التكليف/المهمة',
    input: 'textarea',
    inputLabel: 'ملاحظات الإنجاز ونتائج العمل',
    inputPlaceholder: 'اكتب هنا ما تم إنجازه أو أي ملاحظات...',
    inputAttributes: {
      'aria-label': 'اكتب هنا ما تم إنجازه أو أي ملاحظات'
    },
    showCancelButton: true,
    confirmButtonText: 'تأكيد الإكمال وتوقيع الكشف',
    cancelButtonText: 'إلغاء',
    inputValidator: (value) => {
      if (!value) {
        return 'يجب كتابة ملاحظات الإنجاز لتأكيد اكتمال المهمة!'
      }
    }
  })

  if (notes) {
    try {
      await store.updateTask(task.id, {
        status: 'completed',
        notes: notes
      })
      Swal.fire({
        icon: 'success',
        title: 'تم تأكيد إكمال المهمة بنجاح',
        timer: 1500,
        showConfirmButton: false
      })
      // Refresh tasks list
      const id = route.params.id as string
      const tasksRes = await store.fetchTasks({ related_correspondence: id })
      linkedTasks.value = tasksRes.results || []
    } catch (err: any) {
      console.error(err)
      Swal.fire({
        icon: 'error',
        title: 'حدث خطأ أثناء إكمال المهمة',
        text: err.response?.data?.detail || err.response?.data?.error || 'ليس لديك الصلاحية الكافية لإتمام الإجراء'
      })
    }
  }
}

function generateCoveringLetter() {
  if (!correspondence.value) return
  
  const todayStr = new Date().toLocaleDateString('ar-YE', { day: 'numeric', month: 'long', year: 'numeric' }) + "م"
  const bodyText = `إشارة إلى مذكرتكم ذات الرقم (${correspondence.value.reference_number}) والتاريخ ${correspondence.value.date}م بشأن موضوع (${correspondence.value.subject})، وعطفاً على ذلك نرفق لكم الكشوفات والتقارير المطلوبة لإنجاز الخدمة لشهر ${new Date().toLocaleString('ar-YE', { month: 'long' })}...`

  router.push({
    path: '/secretariat/document-requests',
    query: {
      subject: `الرد على: ${correspondence.value.subject}`,
      recipient: correspondence.value.sender,
      refNo: `رقم الرد/${correspondence.value.reference_number}`,
      body: bodyText
    }
  })
}

const showReferralForm = ref(false)
const submittingReferral = ref(false)
const referralsList = ref<any[]>([])

const referralForm = ref({
  referred_to: '',
  instructions: '',
  due_date: new Date(Date.now() + 86400000 * 3).toISOString().split('T')[0] // 3 days in future
})

function getTrackingUrl() {
  if (!correspondence.value) return ''
  return `${window.location.origin}/secretariat/correspondences/${correspondence.value.id}?token=${correspondence.value.tracking_token}`
}

async function fetchReferralsList() {
  try {
    const id = route.params.id as string
    const res = await store.fetchReferrals({ correspondence: id })
    referralsList.value = res.results || []
  } catch (err) {
    console.error(err)
  }
}

async function submitReferral() {
  if (!referralForm.value.referred_to || !referralForm.value.instructions) {
    Swal.fire({ icon: 'warning', title: 'الرجاء إدخال الحقول المطلوبة' })
    return
  }
  submittingReferral.value = true
  try {
    const id = route.params.id as string
    const data = {
      correspondence: id,
      referred_to: referralForm.value.referred_to,
      instructions: referralForm.value.instructions,
      due_date: referralForm.value.due_date
    }
    await store.createReferral(data)
    Swal.fire({ icon: 'success', title: 'تم تسجيل إحالة المعاملة بنجاح', timer: 1500, showConfirmButton: false })
    
    // Reset Form
    referralForm.value = {
      referred_to: '',
      instructions: '',
      due_date: new Date(Date.now() + 86400000 * 3).toISOString().split('T')[0]
    }
    showReferralForm.value = false
    
    // Refresh Referrals List
    await fetchReferralsList()
  } catch (err: any) {
    console.error(err)
    const errMsg = err.response?.data?.error || err.response?.data?.detail || 'فشل إحالة المعاملة'
    Swal.fire({ icon: 'error', title: 'فشل إحالة المعاملة', text: JSON.stringify(errMsg) })
  } finally {
    submittingReferral.value = false
  }
}

async function completeReferralTask(referralId: number) {
  try {
    const { value: responseNotes, isConfirmed } = await Swal.fire({
      title: 'تأكيد إنجاز التوجيه والعمل',
      text: 'يرجى كتابة شرح أو ملاحظات الإنجاز أدناه (مثال: تم حصر الموقوفين وتجهيز الكشف وإرساله لقسم الرواتب):',
      input: 'textarea',
      inputPlaceholder: 'اكتب تفاصيل الإنجاز هنا...',
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: 'تأكيد وإرسال الرد',
      cancelButtonText: 'إلغاء',
      inputValidator: (value) => {
        if (!value) {
          return 'يجب كتابة ملاحظات الإنجاز لتوضيح ما تم عمله!'
        }
      }
    })
    
    if (!isConfirmed) return
    
    await api.patch(`/secretariat/referrals/${referralId}/`, { 
      status: 'completed',
      notes: responseNotes
    })
    Swal.fire({ icon: 'success', title: 'تم تأكيد الإنجاز بنجاح', timer: 1500, showConfirmButton: false })
    
    await fetchReferralsList()
  } catch (err) {
    console.error(err)
    Swal.fire({ icon: 'error', title: 'فشل تحديث حالة التوجيه' })
  }
}

onMounted(() => {
  fetchDetails()
})
</script>
