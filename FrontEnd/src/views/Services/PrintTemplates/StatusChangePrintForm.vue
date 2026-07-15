<template>
  <div class="print-preview-container relative" :style="{ '--th-bg-color': headerBgColor, '--th-text-color': headerTextColor }">
    
    <!-- Floating Color Picker (Hidden in Print) -->
    <div class="fixed top-4 right-4 bg-white p-4 rounded-xl shadow-2xl border border-gray-300 z-50 print:hidden flex flex-col gap-3 w-56" dir="rtl">
      <h4 class="font-bold text-sm text-gray-800 border-b pb-1">تجربة الألوان (لن تظهر بالطباعة)</h4>
      
      <div>
        <label class="text-xs font-bold text-gray-600 block mb-1">
          خلفية الأعمدة
        </label>
        <div class="flex items-center gap-2 mb-1">
          <input type="color" v-model="headerBgColor" class="w-10 h-8 cursor-pointer rounded shrink-0" />
          <input type="text" :value="headerBgColor" readonly class="w-full text-xs font-sans text-center bg-gray-100 border border-gray-300 rounded p-1 text-gray-800 cursor-text select-all" dir="ltr" />
        </div>
      </div>
      
      <div>
        <label class="text-xs font-bold text-gray-600 block mb-1">
          لون النص
        </label>
        <div class="flex items-center gap-2 mb-1">
          <input type="color" v-model="headerTextColor" class="w-10 h-8 cursor-pointer rounded shrink-0" />
          <input type="text" :value="headerTextColor" readonly class="w-full text-xs font-sans text-center bg-gray-100 border border-gray-300 rounded p-1 text-gray-800 cursor-text select-all" dir="ltr" />
        </div>
      </div>

      <button @click="headerBgColor = '#f0f0f0'; headerTextColor = '#000000'" class="mt-1 w-full bg-gray-200 hover:bg-gray-300 text-gray-800 text-xs font-bold py-1.5 rounded transition">
        إعادة للافتراضي (رمادي)
      </button>
    </div>

    <!-- Double Border Container (Thick outer, thin inner) -->
    <div class="outer-border h-full flex flex-col relative z-10">
      
      <!-- Top Header (ReportHeader Style) -->
      <div class="border-[1.5px] border-gray-900 rounded-lg p-2 pt-2 pb-0 flex justify-between items-start text-sm font-bold text-gray-900 relative bg-white mx-1 mt-1">
        
        <!-- Right: Logo/Republic Info (Dynamic) -->
        <div class="text-right w-1/3 space-y-1 pr-1 leading-tight font-amiri">
          <img src="/images/yemen_calligraphy_cropped.png" alt="الجمهورية اليمنية" class="h-7 w-auto inline-block mb-1" />
          <p class="text-[14px]">وزارة الداخلية</p>
          
          <template v-if="isCentralAdmin">
            <p class="text-[13.5px]">وكيل قطاع الموارد البشرية</p>
            <p class="text-[13.5px]">الإدارة العامة للقوى البشرية</p>
            <p class="text-[13.5px]">لجنة بناء الامدادات</p>
          </template>
          
          <template v-else>
            <p class="text-[13.5px]">شرطة م / {{ governorateName }}</p>
            <p class="text-[13.5px]">إدارة القوى البشرية</p>
          </template>
        </div>
        
        <!-- Center: Emblem Image & Bismillah -->
        <div class="text-center w-1/3 flex flex-col justify-center items-center">
          <img src="/images/bismillah_cropped.png" alt="بسم الله الرحمن الرحيم" class="h-7 w-auto max-w-full object-contain mb-1" />
          <img src="/images/logo/yemen_logo_clean.png" alt="شعار الجمهورية" class="h-auto max-h-[5.5rem] w-auto max-w-full object-contain" />
        </div>
        
        <!-- Left: Document Info -->
        <div class="w-1/3 flex justify-end pl-1 pt-1 font-amiri">
          <div class="space-y-1.5 text-[14px] leading-tight font-bold">
            <div class="flex items-center">
              <span class="w-[5rem] text-right">الـرقـــــــــم/</span>
              <span class="tracking-widest">.......................</span>
            </div>
            
            <div class="flex items-center">
              <span class="w-[5rem] text-right">التاريــــــــخ/</span>
              <div class="flex justify-between items-center w-full font-sans font-bold text-[13px] tracking-wider">
                <span>{{ new Date().toLocaleDateString('en-GB') }}</span>
                <span class="font-serif font-normal mr-1">م</span>
              </div>
            </div>
            
            <div class="flex items-center">
              <span class="w-[5rem] text-right">الــمـوافـــــق/</span>
              <span class="tracking-widest">.......................</span>
            </div>
            
            <div class="flex items-center">
              <span class="w-[5rem] text-right">الـمـرفـقــــات/</span>
              <span class="tracking-widest">.......................</span>
            </div>
          </div>
        </div>
        
      </div> <!-- End Header -->

      <!-- Divider (Thin) -->
      <div class="w-full h-[1.5px] bg-black mt-2 mb-1"></div>

      <!-- Main Content -->
      <div class="flex-grow px-2 flex flex-col relative">
        
        <!-- Document Title -->
        <div class="text-center mt-4 mb-4 flex justify-center items-center w-full">
          <div class="border border-gray-500 bg-gray-100/50 rounded px-6 py-1.5">
            <h2 class="text-[18px] font-black text-black leading-tight tracking-tight" style="font-family: 'Cairo', sans-serif !important;">
              {{ formTitle }}
            </h2>
          </div>
        </div>

        <!-- Section 1: Personal Data (Modern UI) -->
        <div class="section-container">
          <h3 class="section-title">أولاً: البيانات الشخصية</h3>
          <div class="table-wrapper">
            <table class="official-table">
              <thead>
                <tr>
                  <th class="w-[12%]">الرتبة</th>
                  <th class="w-[18%]">الرقم العسكري</th>
                  <th class="w-[38%]">الاسم</th>
                  <th class="w-[16%]">الوحدة</th>
                  <th class="w-[16%]">{{ form?.form_type === 'martyr' ? 'نوع الحالة' : 'السرية' }}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="font-bold">{{ form?.personnel?.rank || form?.personnel?.rank_name || form?.personnel?.current_rank?.name || '—' }}</td>
                  <td class="font-bold font-sans tracking-widest text-[15px]">{{ form?.personnel?.military_number || '—' }}</td>
                  <td class="font-bold">{{ form?.personnel?.full_name || '—' }}</td>
                  <td class="font-bold">{{ form?.personnel?.security_admin_name || form?.personnel?.security_admin || form?.personnel?.central_department_name || form?.personnel?.central_department || '—' }}</td>
                  <td class="font-bold">{{ form?.personnel?.central_department_name || form?.personnel?.branch_name || form?.personnel?.division_name || form?.personnel?.unit_name || '—' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Section 2: Birth & Residence Data -->
        <div class="section-container mt-1">
          <h3 class="section-title">ثانياً: بيانات الميلاد والاقامة الحالية</h3>
          <div class="table-wrapper">
            <table class="official-table">
            <thead>
              <tr>
                <th class="w-[20%]">الرقم الوطني</th>
                <th class="w-[25%]">محل الميلاد</th>
                <th class="w-[25%]">محل الاقامة الحالية</th>
                <th class="w-[15%]">جهة الاصدار</th>
                <th class="w-[15%]">تاريخ الاصدار</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="font-bold font-sans tracking-widest text-[15px] align-middle">{{ form?.form_data?.national_id || form?.personnel?.national_id || '—' }}</td>
                
                <!-- Birth Place Grid -->
                <td class="p-0 align-top" style="padding: 0 !important; height: 1px;">
                  <div class="grid grid-cols-4 w-full h-full text-center" style="grid-template-rows: auto 1fr; gap: 0;">
                    <!-- Headers -->
                    <div class="text-[8px] tracking-tighter font-normal border-b border-l border-black py-0.5 print-bg-gray flex items-center justify-center leading-none">المحافظة</div>
                    <div class="text-[8px] tracking-tighter font-normal border-b border-l border-black py-0.5 print-bg-gray flex items-center justify-center leading-none">المديرية</div>
                    <div class="text-[8px] tracking-tighter font-normal border-b border-l border-black py-0.5 print-bg-gray flex items-center justify-center leading-none">العزلة</div>
                    <div class="text-[8px] tracking-tighter font-normal border-b border-black py-0.5 print-bg-gray flex items-center justify-center leading-none">القرية</div>
                    
                    <!-- Data -->
                    <div class="py-1 px-0.5 font-bold text-[9px] border-l border-black flex items-center justify-center leading-tight break-words whitespace-normal">{{ getLocationObj('birth').gov }}</div>
                    <div class="py-1 px-0.5 font-bold text-[9px] border-l border-black flex items-center justify-center leading-tight break-words whitespace-normal">{{ getLocationObj('birth').dist }}</div>
                    <div class="py-1 px-0.5 font-bold text-[9px] border-l border-black flex items-center justify-center leading-tight break-words whitespace-normal">{{ getLocationObj('birth').subDist }}</div>
                    <div class="py-1 px-0.5 font-bold text-[9px] flex items-center justify-center leading-tight break-words whitespace-normal">{{ getLocationObj('birth').village }}</div>
                  </div>
                </td>

                <!-- Residence Grid -->
                <td class="p-0 align-top" style="padding: 0 !important; height: 1px;">
                  <div class="grid grid-cols-4 w-full h-full text-center" style="grid-template-rows: auto 1fr; gap: 0;">
                    <!-- Headers -->
                    <div class="text-[8px] tracking-tighter font-normal border-b border-l border-black py-0.5 print-bg-gray flex items-center justify-center leading-none">المحافظة</div>
                    <div class="text-[8px] tracking-tighter font-normal border-b border-l border-black py-0.5 print-bg-gray flex items-center justify-center leading-none">المديرية</div>
                    <div class="text-[8px] tracking-tighter font-normal border-b border-l border-black py-0.5 print-bg-gray flex items-center justify-center leading-none">العزلة</div>
                    <div class="text-[8px] tracking-tighter font-normal border-b border-black py-0.5 print-bg-gray flex items-center justify-center leading-none">القرية</div>
                    
                    <!-- Data -->
                    <div class="py-1 px-0.5 font-bold text-[9px] border-l border-black flex items-center justify-center leading-tight break-words whitespace-normal">{{ getLocationObj('residence').gov }}</div>
                    <div class="py-1 px-0.5 font-bold text-[9px] border-l border-black flex items-center justify-center leading-tight break-words whitespace-normal">{{ getLocationObj('residence').dist }}</div>
                    <div class="py-1 px-0.5 font-bold text-[9px] border-l border-black flex items-center justify-center leading-tight break-words whitespace-normal">{{ getLocationObj('residence').subDist }}</div>
                    <div class="py-1 px-0.5 font-bold text-[9px] flex items-center justify-center leading-tight break-words whitespace-normal">{{ getLocationObj('residence').village }}</div>
                  </div>
                </td>

                <td class="font-bold align-middle">{{ form?.form_data?.id_issue_place || form?.form_data?.id_issuer || form?.personnel?.id_issue_place || form?.personnel?.id_issuer || '—' }}</td>
                <td class="font-bold font-sans text-[14px] align-middle whitespace-nowrap" dir="ltr">{{ formatDate(form?.form_data?.id_issue_date || form?.personnel?.id_issue_date || '') || '—' }}</td>
              </tr>
            </tbody>
          </table>
          </div>
        </div>

        <!-- Section 3: Status Data (Dynamic) -->
        <div class="section-container mt-2">
          <h3 class="section-title">ثالثاً بيــانات الحـــــالة</h3>
          <div class="table-wrapper">
            <table class="official-table">
            <thead>
              <tr>
                <th v-for="field in dynamicSpecificFields" :key="'h-'+field.key" :style="{ width: getFieldWidth(field.key, dynamicSpecificFields.length, dynamicSpecificFields) }">
                  {{ field.label }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td v-for="field in dynamicSpecificFields" :key="'d-'+field.key" :class="[field.key === 'martyrdom_location' || field.key === 'death_location' ? 'p-0 align-top' : 'font-bold text-[14px]']" :style="field.key === 'martyrdom_location' || field.key === 'death_location' ? 'padding: 0 !important; height: 1px;' : ''">
                  <div v-if="field.key === 'martyrdom_location' || field.key === 'death_location'" class="grid grid-cols-4 w-full h-full text-center" style="grid-template-rows: auto 1fr; gap: 0;">
                    <!-- Headers -->
                    <div class="text-[8px] tracking-tighter font-normal border-b border-l border-black py-0.5 print-bg-gray flex items-center justify-center leading-none">المحافظة</div>
                    <div class="text-[8px] tracking-tighter font-normal border-b border-l border-black py-0.5 print-bg-gray flex items-center justify-center leading-none">المديرية</div>
                    <div class="text-[8px] tracking-tighter font-normal border-b border-l border-black py-0.5 print-bg-gray flex items-center justify-center leading-none">العزلة</div>
                    <div class="text-[8px] tracking-tighter font-normal border-b border-black py-0.5 print-bg-gray flex items-center justify-center leading-none">القرية</div>
                    
                    <!-- Data -->
                    <div class="py-1 px-0.5 font-bold text-[9px] border-l border-black flex items-center justify-center leading-tight break-words whitespace-normal">{{ parseLocationString(field.value).gov }}</div>
                    <div class="py-1 px-0.5 font-bold text-[9px] border-l border-black flex items-center justify-center leading-tight break-words whitespace-normal">{{ parseLocationString(field.value).dist }}</div>
                    <div class="py-1 px-0.5 font-bold text-[9px] border-l border-black flex items-center justify-center leading-tight break-words whitespace-normal">{{ parseLocationString(field.value).subDist }}</div>
                    <div class="py-1 px-0.5 font-bold text-[9px] flex items-center justify-center leading-tight break-words whitespace-normal">{{ parseLocationString(field.value).village }}</div>
                  </div>
                  <span v-else :class="field.isDate || field.isNumber ? 'font-sans tracking-wider text-[13px] whitespace-nowrap inline-block' : ''" :dir="field.isDate || field.isNumber ? 'ltr' : 'rtl'">
                    {{ field.isDate ? formatDate(field.value) : (field.value !== undefined && field.value !== null && field.value !== '' ? field.value : '—') }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
          </div>
        </div>

        <!-- Section 4: Attachments -->
        <div class="section-container mt-2 mb-1">
          <h3 class="section-title">المرفقــات : -</h3>
          <div class="table-wrapper">
            <table class="official-table">
            <thead>
              <tr>
                <th class="w-[8%]">م</th>
                <th class="w-[62%]">نوع الوثيقة</th>
                <th class="w-[15%]">مرفق</th>
                <th class="w-[15%]">غير مرفق</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(att, idx) in allAttachments" :key="idx">
                <td class="font-bold font-sans text-[14px]">{{ Number(idx) + 1 }}</td>
                <td class="font-bold text-[14px] text-right px-4">{{ translateAttachment(att) }}</td>
                <td class="font-sans font-bold text-lg leading-none">{{ (att.id || att.file) ? '✔' : '' }}</td>
                <td></td>
              </tr>
            </tbody>
          </table>
          </div>
        </div>

        <!-- Letter Body Section -->
        <div class="letter-body mt-4 px-3 text-justify flex-grow">
          <!-- Addressee -->
          <div class="flex justify-between items-end mb-5">
            <h2 class="text-[20px] font-black text-black tracking-wide" style="font-family: 'Cairo', sans-serif;">
              الأخ / مدير عــــــام القوى البشريـــــة
            </h2>
            <h2 class="text-[21px] font-black text-black tracking-widest" style="font-family: 'Cairo', sans-serif;">
              المحتـــــــرم
            </h2>
          </div>
          
          <!-- Greeting -->
          <div class="text-center mb-2 mt-2">
            <span class="inline-block text-[22px] font-bold text-black" style="font-family: 'Samt7017', 'Aref Ruqaa', serif;">
              تحيـــــة طيبـــــة وبعـــــد ،،،
            </span>
          </div>
          
          <p v-for="(paragraph, index) in letterText" :key="index" class="font-normal text-[16px] mb-3 leading-[1.8] text-justify text-black whitespace-pre-wrap" style="font-family: 'Cairo', sans-serif;">
            {{ paragraph }}
          </p>
          <p class="text-center text-[15px] font-bold text-black mb-1 mt-3" style="font-family: 'Samt7017', 'Aref Ruqaa', serif;">
            وتقبلــــوا خالــــص تحياتنــــا ،،،
          </p>
        </div>

        <!-- Signatures & Approvals (Report Format) -->
        <div class="mt-auto pt-1 pb-1">
          <div class="border-[1.5px] border-gray-900 rounded-lg p-1.5 pb-2 grid grid-cols-3 gap-1 text-[11px] font-bold text-gray-900 text-center relative mx-1">
            <!-- Frame Title -->
            <div class="absolute -top-2.5 right-6 bg-white px-2 font-bold text-gray-900 text-[11px]">التوقيعات والاعتمادات</div>
            
            <!-- Right: Preparer -->
            <div class="space-y-1.5 flex flex-col items-start text-right pr-2">
              <p class="mb-0.5 font-bold text-[11.5px]">إعداد (قسم الخدمات)</p>
              <div class="space-y-0.5 w-full max-w-[170px]">
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">الاسم:</span> <span class="flex-1 text-right">............................</span></p>
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">الرتبة:</span> <span class="flex-1 text-right">............................</span></p>
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">التوقيع:</span> <span class="flex-1 text-right">............................</span></p>
              </div>
            </div>
            
            <!-- Center: Reviewer -->
            <div class="space-y-1.5 flex flex-col items-center">
              <p class="mb-0.5 font-bold text-[11.5px]">مراجعة (مدير إدارة القوى البشرية)</p>
              <div class="space-y-0.5 w-full max-w-[170px]">
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">الاسم:</span> <span class="flex-1 text-right">............................</span></p>
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">الرتبة:</span> <span class="flex-1 text-right">............................</span></p>
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">التوقيع:</span> <span class="flex-1 text-right">............................</span></p>
              </div>
            </div>
            
            <!-- Left: Approver -->
            <div class="space-y-1.5 flex flex-col items-end text-right pl-2">
              <p class="mb-0.5 font-bold text-[11.5px]">اعتماد (مدير عام شرطة المحافظة/الوحدة)</p>
              <div class="space-y-0.5 w-full max-w-[170px]">
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">الاسم:</span> <span class="flex-1 text-right">............................</span></p>
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">الرتبة:</span> <span class="flex-1 text-right">............................</span></p>
                <div class="flex items-center relative"><span class="w-10 text-right z-10 text-[11.5px] mt-0.5">التوقيع:</span> 
                  <div class="flex-1 text-right relative z-10">
                    <span class="leading-none">............................</span>
                    <!-- Official Seal Area -->
                    <div class="absolute bottom-[-5px] right-2 w-10 h-10 border border-dashed border-gray-400 rounded-full flex items-center justify-center opacity-60 z-0 -rotate-12 pointer-events-none">
                      <span class="text-gray-400 text-[6.5px] font-black text-center leading-tight">الختم<br>الرسمي</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Security Tracking Footer & QR Code -->
          <div class="flex items-center justify-between text-[6.5px] text-gray-500 font-medium border-t border-gray-400 pt-1 mt-1.5 mx-1">
            <div class="space-y-0.5 text-right flex-1 font-sans">
              <p>طُبع بواسطة: <span class="font-bold text-gray-800">النظام</span> | بتاريخ: <span class="font-bold text-gray-800" dir="ltr">{{ new Date().toLocaleString('en-GB') }}</span></p>
              <p>المرجع (REF): <span class="font-bold text-gray-800 font-mono tracking-wider">TX-{{ String(form?.id || '').padStart(6, '0') }}</span></p>
            </div>
            
            <!-- QR Code Dummy -->
            <div class="flex items-center gap-1 pr-3 border-r border-gray-300">
              <svg class="h-5 w-5 text-gray-900" viewBox="0 0 33 33" fill="currentColor" shape-rendering="crispEdges">
                <path d="M0 0h9v9H0zM2 2v5h5V2zM24 0h9v9h-9zM26 2v5h5V2zM0 24h9v9H0zM2 26v5h5v-5zM12 0h2v2h-2zM16 0h5v2h-5zM22 0h1v2h-1zM10 2h2v3h-2zM14 2h1v1h-1zM16 3h2v2h-2zM20 3h1v2h-1zM10 6h3v2h-3zM14 5h1v1h-1zM17 6h5v2h-5zM12 9h2v2h-2zM15 9h1v3h-1zM17 9h2v1h-2zM20 9h3v1h-3zM25 10h2v2h-2zM28 10h5v1h-5zM0 10h2v1H0zM3 10h2v2H3zM6 10h2v3H6zM9 10h2v2H9zM12 12h2v2h-2zM17 11h2v3h-2zM21 11h2v1h-2zM27 12h2v1h-2zM31 12h2v2h-2zM0 12h1v3H0zM2 13h2v1H2zM9 13h2v1H9zM20 13h1v3h-1zM23 13h3v2h-3zM29 14h2v2h-2zM4 14h1v1H4zM6 14h1v3H6zM8 15h3v2H8zM12 15h1v1h-1zM14 15h2v3h-2zM18 15h1v2h-1zM27 15h1v2h-1zM32 15h1v3h-1zM1 16h2v2H1zM4 16h1v2H4zM12 17h1v1h-1zM17 17h1v3h-1zM20 17h2v2h-2zM23 16h2v1h-2zM26 18h2v2h-2zM29 17h2v1h-2zM7 18h1v3H7zM9 18h2v1H9zM12 19h4v2h-4zM19 19h1v1h-1zM22 18h3v1h-3zM28 19h1v3h-1zM31 19h2v1h-2zM0 20h2v2H0zM3 20h3v1H3zM9 20h2v2H9zM17 21h2v1h-2zM20 20h1v2h-1zM23 20h1v1h-1zM25 21h2v2h-2zM30 21h3v2h-3zM2 23h2v1H2zM5 22h3v2H5zM11 22h2v1h-2zM14 21h2v2h-2zM18 23h3v1h-3zM22 22h2v1h-2zM25 24h1v1h-1zM27 24h5v2h-5zM10 24h3v1h-3zM14 24h2v2h-2zM17 25h1v1h-1zM19 25h2v2h-2zM22 24h2v3h-2zM25 26h1v3h-1zM28 27h2v2h-2zM31 26h2v1h-2zM10 26h1v2h-1zM12 27h2v2h-2zM15 26h1v2h-1zM17 27h2v2h-2zM20 28h1v3h-1zM22 28h1v1h-1zM27 28h1v1h-1zM32 28h1v2h-1zM10 29h2v2h-2zM13 30h1v3h-1zM15 29h2v1h-2zM18 30h1v3h-1zM22 30h2v1h-2zM25 30h2v3h-2zM29 31h3v2h-3zM10 32h2v1h-2zM15 31h2v2h-2zM21 32h3v1h-3z" />
              </svg>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import yemenLogo from '@/assets/yemen_logo.jpg'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// --- Interactive Color Testing ---
const headerBgColor = ref('#e8ede1') // Default Zaiti Light
const headerTextColor = ref('#1a2415') // Default Dark Text

// Determine if user is central admin
const isCentralAdmin = computed(() => {
  const user = authStore.user as any
  if (!user) return false
  if (user.is_superuser) return true
  
  const roleCode = user.role?.code || user.authz_profile?.role_code
  const supervisesAll = user.supervises_all || user.authz_profile?.supervises_all
  
  return roleCode === 'SYSTEM_ADMIN' || supervisesAll
})

// Get governorate name for right header
const governorateName = computed(() => {
  const user = authStore.user as any
  if (!user) return '............'
  
  if (user.city) return user.city

  const roleName = user.role?.name || user.authz_profile?.role_name || ''
  const displayName = authStore.displayName || ''
  
  const textToParse = displayName.includes('أمن') || displayName.includes('محافظة') ? displayName : roleName
  
  if (textToParse) {
    if (textToParse.includes('محافظة')) {
      return textToParse.split('محافظة')[1].trim()
    } else if (textToParse.includes('أمن')) {
      return textToParse.split('أمن')[1].trim()
    }
    return textToParse
  }
  
  return '............'
})

const props = defineProps<{
  form: any
}>()

const formTitle = computed(() => {
  const titles: Record<string, string> = {
    martyr: 'استمارة إثبات حالة (شهيد)',
    death: 'استمارة إثبات حالة (وفاة)',
    retirement_age: 'استمارة إثبات حالة (بلوغ السن القانوني)',
    medical_unfit: 'استمارة إثبات حالة (عدم اللياقة الصحية)',
    missing: 'استمارة إثبات حالة (مفقود)',
    imprisoned: 'استمارة إثبات حالة (مسجون)',
    seconded: 'استمارة إثبات حالة (منتدب)',
    escort: 'استمارة إثبات حالة (مرافق)',
    study_leave: 'استمارة إثبات حالة (مفرغ لدراسة)',
    end_of_service: 'استمارة إثبات حالة (إنهاء مدة)',
    retired: 'استمارة إثبات حالة (محال للتقاعد)',
    correction: 'استمارة إثبات حالة (تصحيح بيانات)',
  }
  return titles[props.form?.form_type] || `استمارة إثبات حالة (${props.form?.form_type_display || ''})`
})

interface FormField { key: string; label: string; value?: any; isDate?: boolean; isNumber?: boolean }

const fieldTranslations: Record<string, string> = {
  rank: 'الرتبة',
  unit: 'الوحدة',
  company: 'السرية',
  category: 'الفئة',
  full_name: 'الاسم',
  id_issuer: 'جهة إصدار الهوية',
  birth_place: 'محل الميلاد',
  national_id: 'الرقم الوطني',
  id_issue_date: 'تاريخ إصدار الهوية',
  martyrdom_date: 'تاريخ الاستشهاد',
  martyrdom_location: 'مكان الاستشهاد',
  martyrdom_cause: 'سبب الاستشهاد',
  military_number: 'الرقم العسكري',
  current_residence: 'مقر السكن الحالي',
  occurrence_context: 'نوع الحالة',
  assignment_order: 'أمر التكليف',
  operations_report: 'رقم بلاغ العمليات',
  appointment_ruling: 'حكم تنصيب',
  attorney_id: 'هوية الوكيل',
  power_of_attorney: 'وكالة شرعية',
  heir_ruling: 'انحصار ورثة',
  death_certificate: 'شهادة وفاة',
  death_date: 'تاريخ الوفاة',
  death_place: 'مكان الوفاة',
  death_reason: 'سبب الوفاة',
  case_type: 'نوع الحالة',
  ruling_date: 'تاريخ الحكم',
  ruling_duration: 'مدة الحكم',
  arrest_date: 'تاريخ التوقيف',
  arrest_authority: 'جهة التوقيف',
  study_type: 'نوع الدراسة',
  institution: 'جهة الدراسة',
  duration: 'مدة الدراسة',
  start_date: 'تاريخ البدء',
  end_date: 'تاريخ الانتهاء',
  vip_name: 'اسم الشخصية',
  vip_position: 'منصب الشخصية',
  order_source: 'مصدر الامر',
  order_copy: 'نسخة من أمر التكليف بالمرافقة',
  'order copy': 'نسخة من أمر التكليف بالمرافقة',
  study_order: 'نسخة من أمر التفرغ الدراسي',
  'study order': 'نسخة من أمر التفرغ الدراسي',
  secondment_place: 'جهة الانتداب',
  destination: 'جهة الانتداب',
  delegate_to: 'جهة الانتداب',
  delegate_purpose: 'سبب الانتداب',
  reason: 'سبب الانتداب',
  decision_number: 'رقم القرار',
  referral_date: 'تاريخ الاحالة',
  retirement_date: 'تاريخ التقاعد',
  disease_type: 'نوع المرض أو الإصابة',
  decision_source: 'مصدر القرار',
  disability_percentage: 'نسبة العجز',
  notes: 'ملاحظات',
  birth_date: 'تاريخ الميلاد',
  join_date: 'تاريخ الالتحاق',
  age: 'العمر',
  gender: 'الجنس',
  effective_date: 'تاريخ النفاذ',
  decision_date: 'تاريخ القرار',
  'decision date': 'تاريخ القرار',
  certified_id: 'نسخة من البطاقة العسكرية/الشخصية',
  'certified id': 'نسخة من البطاقة العسكرية/الشخصية',
  personal_request: 'الطلب الشخصي',
  'personal request': 'الطلب الشخصي',
  approval_document: 'مذكرة الاعتماد',
  'approval document': 'مذكرة الاعتماد',
  memo: 'مذكرة',
  medical_report: 'تقرير طبي',
  'medical report': 'تقرير طبي',
  ministry_approval: 'موافقة الوزارة',
  'ministry approval': 'موافقة الوزارة',
  court_ruling: 'حكم المحكمة',
  'court ruling': 'حكم المحكمة',
  ruling_type: 'نوع الحكم',
  'ruling type': 'نوع الحكم',
  sentence_start_date: 'تاريخ بداية الحكم',
  'sentence start date': 'تاريخ بداية الحكم',
  sentence_end_date: 'تاريخ نهاية الحكم',
  'sentence end date': 'تاريخ نهاية الحكم',
  agent_id: 'هوية الوكيل',
  'agent id': 'هوية الوكيل',
  legal_power_of_attorney: 'وكالة شرعية',
  'legal power of attorney': 'وكالة شرعية',
  personnel_id: 'صورة الهوية (فرد)',
  'personnel id': 'صورة الهوية (فرد)',
  national_id_front: 'صورة البطاقة (أمامي)',
  'national id front': 'صورة البطاقة (أمامي)',
  secondment_order: 'نسخة من الأمر',
  'secondment order': 'نسخة من الأمر',
  ruling_copy: 'نسخة من الحكم',
  // حقول FormRegistry المضافة
  death_cause: 'سبب الوفاة',
  death_location: 'مكان الوفاة',
  missing_date: 'تاريخ الفقدان',
  missing_location: 'مكان الفقدان',
  court_ruling_date: 'تاريخ الحكم الشرعي',
  legal_status: 'حالة الإجراءات',
  medical_source: 'مصدر القرار الطبي',
  injury_context: 'سبب الحالة',
  injury_date: 'تاريخ الوقوع',
  original_medical_decision: 'القرار الطبي الأصل',
  recent_photo: 'صورة حديثة',
  service_years: 'سنوات الخدمة',
  dignitary_name: 'اسم الشخصية',
  dignitary_position: 'منصب الشخصية',
  settlement_type: 'نوع التسوية',
  to_rank: 'الرتبة المستهدفة',
  demotion_reason: 'سبب التنزيل',
  due_date: 'تاريخ الاستحقاق',
  new_military_number: 'الرقم العسكري الجديد',
  university_degree_type: 'نوع المؤهل الجامعي',
}

function translateField(key: string) {
  if (!key) return ''
  const normalizedKey = String(key).toLowerCase().trim()
  const replacedKey = normalizedKey.replace(/_/g, ' ')
  return fieldTranslations[normalizedKey] || fieldTranslations[replacedKey] || String(key).replace(/_/g, ' ')
}

// الحقول المعروضة في أقسام 1 و 2 — لا تُكرر في قسم 3
const EXCLUDED_FROM_STATUS_KEYS = new Set([
  'category',
  'rank', 'military_number', 'full_name', 'name', 'unit', 'company',
  'security_admin', 'central_department', 'branch',
  'national_id', 'id_issue_date', 'id_issue_place', 'id_issuer',
  'birth_governorate', 'birth_district', 'birth_sub_district', 'birth_village',
  'birth_governorate_name', 'birth_district_name', 'birth_sub_district_name', 'birth_village_name',
  'residence_governorate', 'residence_district', 'residence_sub_district', 'residence_village',
  'residence_governorate_name', 'residence_district_name', 'residence_sub_district_name', 'residence_village_name',
  'birth_place', 'current_residence',
  'birth_gov_id', 'birth_district_id', 'birth_sub_district_id', 'birth_village_id',
  'residence_gov_id', 'residence_district_id', 'residence_sub_district_id', 'residence_village_id',
  'notes',
])

const dynamicSpecificFields = computed<FormField[]>(() => {
  const fd = props.form?.form_data || {}
  const p = props.form?.personnel || {}
  const fields: FormField[] = []

  // ── العمود الأول دائماً: الفئة ──
  fields.push({
    key: 'category',
    label: 'الفئة',
    value: fd.category || props.form?.form_type_display || '—'
  })

  // ── ترتيب الحقول كما في الاستمارات الرسمية (تخطيط الأعمدة من اليمين لليسار بعد الفئة وقبل الملاحظات) ──
  const ORDER_MAP: Record<string, string[]> = {
    death: ['case_type', 'death_date', 'occurrence_context', 'death_location'],
    martyr: ['martyrdom_date', 'occurrence_context', 'martyrdom_location'],
    imprisoned: ['case_type', 'ruling_date', 'ruling_duration', 'arrest_date', 'arrest_authority'],
    seconded: ['secondment_place', 'reason', 'order_source', 'start_date', 'end_date'],
    escort: ['dignitary_name', 'dignitary_position', 'order_source', 'start_date', 'end_date'],
    study_leave: ['study_type', 'institution', 'order_source', 'duration', 'start_date', 'end_date'],
    end_of_service: ['birth_date', 'join_date', 'age', 'gender'],
    retirement_age: ['birth_date', 'join_date', 'age', 'gender'],
    retired: ['birth_date', 'join_date', 'decision_number', 'referral_date'],
    medical_unfit: ['disease_type', 'medical_source', 'disability_percentage', 'injury_context'],
    missing: ['missing_date', 'missing_location', 'court_ruling_date', 'legal_status']
  }

  const ft = props.form?.form_type || ''
  const orderedKeys = ORDER_MAP[ft] || Object.keys(fd).filter(k => !EXCLUDED_FROM_STATUS_KEYS.has(k))

  // ── عرض الحقول بالترتيب ──
  for (const key of orderedKeys) {
    if (EXCLUDED_FROM_STATUS_KEYS.has(key)) continue
    
    let finalValue = fd[key]
    if ((finalValue === undefined || finalValue === null || finalValue === '') && key === 'birth_date') finalValue = p.birth_date
    if ((finalValue === undefined || finalValue === null || finalValue === '') && key === 'join_date') finalValue = p.join_date

    let label = translateField(key)
    if (key === 'occurrence_context') {
      if (ft === 'martyr') label = 'سبب الاستشهاد'
      else label = 'سبب الوفاة'
    }
    if (key === 'case_type') {
      if (ft === 'imprisoned') label = 'نوع القضية'
      else label = 'نوع الحالة'
    }
    // Handle aliases for seconded
    if (ft === 'seconded') {
      if (key === 'destination' || key === 'delegate_to' || key === 'secondment_place') label = 'جهة الانتداب'
      if (key === 'reason' || key === 'delegate_purpose' || key === 'purpose') label = 'سبب الانتداب'
      if (key === 'start_date' || key === 'duration_from' || key === 'date_from') label = 'تاريخ البدء'
      if (key === 'end_date' || key === 'duration_to' || key === 'date_to') label = 'تاريخ الانتهاء'
    }
    // Handle aliases for study_leave
    if (ft === 'study_leave') {
      if (key === 'institution') label = 'مكان الدراسة'
      if (key === 'duration') label = 'مدة الدراسة'
    }
    
    // Translate gender value if present
    if (key === 'gender') {
      if (finalValue === 'M') finalValue = 'ذكر'
      if (finalValue === 'F') finalValue = 'أنثى'
    }

    const isDate = finalValue ? String(finalValue).match(/^\d{4}-\d{2}-\d{2}/) !== null : false
    const isNumber = finalValue ? (!isNaN(Number(finalValue)) && String(finalValue).trim() !== '') : false
    
    // إظهار الحقل فقط إذا كان له قيمة، باستثناء الحقول الأساسية
    if (finalValue !== undefined && finalValue !== null && finalValue !== '') {
      fields.push({ key, label, value: finalValue, isDate, isNumber })
    } else if (ORDER_MAP[ft] && ORDER_MAP[ft].includes(key)) {
      // إظهار أعمدة الاستمارات الرسمية حتى لو كانت فارغة (—)
      fields.push({ key, label, value: '—', isDate, isNumber })
    }
  }

  // ── العمود الأخير دائماً: ملاحظات ──
  fields.push({
    key: 'notes',
    label: 'ملاحظات',
    value: fd.notes || props.form?.notes || ''
  })

  // ── حماية: إذا لم يكن هناك حقول (استمارة فارغة) ──
  if (fields.length <= 2) {
    fields.splice(1, 0, { key: 'effective_date', label: 'التاريخ الفعلي', value: props.form?.effective_date, isDate: true })
  }

  return fields
})

function formatLocation(prefix: 'birth' | 'residence') {
  const p = props.form?.personnel || {}
  const fd = props.form?.form_data || {}
  
  // جمع كل الأجزاء: محافظة - مديرية - عزلة - قرية
  const gov = fd[`${prefix}_governorate_name`] || fd[`${prefix}_governorate`] || p[`${prefix}_governorate_name`] || p[`${prefix}_governorate`]
  const dist = fd[`${prefix}_district_name`] || fd[`${prefix}_district`] || p[`${prefix}_district_name`] || p[`${prefix}_district`]
  const subDist = fd[`${prefix}_sub_district_name`] || p[`${prefix}_sub_district_name`]
  const village = fd[`${prefix}_village_name`] || p[`${prefix}_village_name`]
  
  const parts = [gov, dist, subDist, village].filter(Boolean)
  if (parts.length > 0) return parts.join(' - ')
  
  // Fallback to direct keys like 'birth_place' or 'current_residence'
  const fallbackKey = prefix === 'birth' ? 'birth_place' : 'current_residence'
  if (fd[fallbackKey]) return fd[fallbackKey]
  if (p[fallbackKey]) return p[fallbackKey]
  
  return '—'
}

function getLocationObj(prefix: 'birth' | 'residence') {
  const p = props.form?.personnel || {}
  const fd = props.form?.form_data || {}
  
  const gov = fd[`${prefix}_governorate_name`] || fd[`${prefix}_governorate`] || p[`${prefix}_governorate_name`] || p[`${prefix}_governorate`] || '—'
  const dist = fd[`${prefix}_district_name`] || fd[`${prefix}_district`] || p[`${prefix}_district_name`] || p[`${prefix}_district`] || '—'
  const subDist = fd[`${prefix}_sub_district_name`] || p[`${prefix}_sub_district_name`] || '—'
  const village = fd[`${prefix}_village_name`] || p[`${prefix}_village_name`] || '—'
  
  return { gov, dist, subDist, village }
}

function parseLocationString(str: any) {
  if (!str || typeof str !== 'string') return { gov: '—', dist: '—', subDist: '—', village: '—' }
  // Split by hyphen, en-dash, or em-dash
  const parts = str.split(/[-–—]/).map(s => s.trim()).filter(s => s !== '')
  return {
    gov: parts[0] || '—',
    dist: parts[1] || '—',
    subDist: parts[2] || '—',
    village: parts[3] || '—'
  }
}

const letterText = computed(() => {
  const ft = props.form?.form_type || ''
  const display = props.form?.form_data?.category || props.form?.form_type_display || '—'
  
  // النص الخاص باستمارة الوفاة (كما في الصورة المرفقة)
  if (ft === 'death') {
    return [
      `موضحاً لكم اعلاه بيانات حالة المذكور والتي بموجبها تم ضمه على فئة (${display}) ومرفق لكم الاوليات الاصل ونؤكد صحتها. نأمل التوجيه الى المختصين باستكمال الاجراءات بحسب النظام.`
    ]
  }


  // النص الخاص باستمارة منتدب
  if (ft === 'seconded') {
    return [
      `موضحاً لكم اعلاه بيانات حالة المذكور والتي بموجبها تم ضمه على فئة (المنتدبين) ومرفق لكم الاوليات\n١- نسخة من الامر.                  ٢- نسخة من البطاقة العسكرية والشخصية معمدة.`,
      `نأمل التوجيه الى المختصين باستكمال الاجراءات بحسب النظام.`
    ]
  }

  // النص الخاص باستمارة مفرغ للدراسة
  if (ft === 'study_leave') {
    return [
      `موضحاً لكم اعلاه بيانات حالة المذكور والتي بموجبها تم ضمه على فئة (المفرغين للدراسة) ومرفق لكم الاوليات\n١- نسخة من الامر.                  ٢- نسخة من البطاقة العسكرية والشخصية معمدة.`,
      `نأمل التوجيه الى المختصين باستكمال الاجراءات بحسب النظام.`
    ]
  }
  
  // النص الافتراضي لبقية الاستمارات (حتى يتم تزويدنا بصورها)
  return [
    `موضحاً لكم اعلاه بيانات حالة المذكور والتي بموجبها تم ضمه على فئة (${display}) ومرفق لكم الاوليات الموضحة في جدول المرفقات أعلاه وتؤكد صحتها.`,
    `نأمل التوجيه الى المختصين باستكمال الاجراءات بحسب النظام.`
  ]
})

function formatDate(val: any) {
  if (!val || typeof val !== 'string') return val;
  const match = val.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (match) {
    return `${match[3]}/${match[2]}/${match[1]}`;
  }
  return val;
}

function getFieldWidth(key: string, totalFields: number, fields: FormField[]) {
  const hasLocationField = fields.some(f => f.key === 'martyrdom_location' || f.key === 'death_location')
  if (hasLocationField) {
    if (key === 'martyrdom_location' || key === 'death_location') {
      return '45%' // Give location grids plenty of space
    }
    const remainingFields = totalFields - 1;
    return `${55 / remainingFields}%` // Distribute rest equally
  }
  return `${100 / totalFields}%` // Default equal distribution
}

const allAttachments = computed(() => {
  if (props.form?.attachments && props.form.attachments.length > 0) return props.form.attachments;
  if (props.form?.required_attachments && props.form.required_attachments.length > 0) return props.form.required_attachments;
  
  return [
    { label: 'نسخة من البطاقة العسكرية/الشخصية معمدة' },
    { label: 'الطلب الشخصي' },
    { label: 'مذكرة التغطية' }
  ];
})

function translateAttachment(att: any) {
  if (typeof att === 'string') return translateField(att)
  return translateField(att?.label || att?.document_type_display || att?.document_type || att?.name || att?.key) || String(att)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400;1,700&family=Aref+Ruqaa:wght@400;700&family=Cairo:wght@400;700;900&display=swap');

@font-face {
  font-family: 'Samt7017';
  src: url('/fonts/samt7017.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

.print-preview-container {
  font-family: 'Amiri', serif !important;
  width: 210mm;
  /* Use min-height instead of fixed height so it doesn't get abruptly cut off if slightly larger, but fit to A4 print naturally */
  min-height: 296mm; 
  background: white;
  margin: 0 auto;
  box-sizing: border-box;
  padding: 0mm 0mm; /* Zero padding to perfectly expand to the edges */
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  color: #000;
}

/* Outer Border mimicking paper */
.outer-border {
  border: 1.5px solid #000;
  outline: 3px solid #000;
  outline-offset: -4px;
  padding: 3px;
}

/* Header Meta Box */
.header-meta-table {
  width: 200px;
  border-collapse: collapse;
  border: 1.5px solid #000;
  font-size: 13.5px;
  font-weight: 700;
}
.header-meta-table td {
  border: 1px solid #000;
  padding: 1px 4px;
}
.header-meta-table .meta-label {
  width: 50px;
  border-left: 1.5px solid #000;
  text-align: right;
  vertical-align: middle;
}
.header-meta-table .meta-value {
  text-align: center;
  vertical-align: middle;
}

/* Double Divider Line */
.header-divider {
  width: 100%;
  height: 3px;
  border-top: 2.5px solid #000;
  border-bottom: 1px solid #000;
}

/* Section Titles (Modern Global Style) */
.section-title {
  color: #1f2937; /* gray-800 */
  display: flex;
  align-items: center;
  font-family: 'Cairo', sans-serif;
  font-size: 14.5px;
  font-weight: 700;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}
.section-title::after {
  content: '';
  flex-grow: 1;
  height: 1px;
  background-color: #d1d5db; /* gray-300 */
  margin-right: 0.75rem;
}

/* Standard Tables */
.section-container {
  width: 100%;
}
.table-wrapper {
  width: 100%;
  border: 2px solid #000;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 2px;
}
.official-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  background-color: transparent;
  table-layout: fixed;
  word-wrap: break-word;
  overflow-wrap: break-word;
}
.official-table th {
  background-color: var(--th-bg-color, #e8ede1) !important;
  box-shadow: inset 0 0 0 1000px var(--th-bg-color, #e8ede1) !important;
  color: var(--th-text-color, #1a2415) !important;
  font-family: 'Cairo', sans-serif;
  font-weight: 700;
  font-size: 12px;
  border-bottom: 1.5px solid #000;
  border-left: 1.5px solid #000;
  padding: 3px;
  -webkit-print-color-adjust: exact !important;
  print-color-adjust: exact !important;
}
.official-table td {
  border-bottom: 1.5px solid #000;
  border-left: 1.5px solid #000;
  padding: 3px 2px;
  font-family: 'Cairo', sans-serif;
  font-weight: 600;
  font-size: 12.5px;
  color: #0f172a;
}
.official-table th:last-child,
.official-table td:last-child {
  border-left: none;
}
.official-table tbody tr:last-child td {
  border-bottom: none;
}
</style>

<style>
/* ── Global Print Rules to bypass Vue scoped CSS limitations ── */
@media print {
  @page {
    size: A4;
    margin: 0mm; 
  }
  
  html, body {
    margin: 0 !important;
    padding: 0 !important;
    background: white !important;
  }
  
  /* Force background colors to print even if 'Background Graphics' is unchecked in print dialog */
  .print-bg-gray {
    background-color: #f3f4f6 !important;
    box-shadow: inset 0 0 0 1000px #f3f4f6 !important;
  }

  /* Force colors on ALL elements, regardless of Tailwind or Scoped CSS */
  * {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    color-adjust: exact !important;
  }

  /* Enforce strict A4 geometry so browser auto-scaling works flawlessly */
  .print-preview-container {
    zoom: 0.86 !important; /* Shrinks everything perfectly by 14% */
    width: 244mm !important; /* 210mm / 0.86 = 244mm. This completely eliminates the white margins! */
    max-width: 244mm !important;
    height: 338mm !important; /* 290mm / 0.86 = 337mm. Forces it to stretch to exactly 1 A4 page! */
    max-height: 338mm !important;
    margin: 0 auto !important;
    padding: 0 !important; /* Removed padding to make the border touch the absolute edge of the paper */
    overflow: hidden !important; /* Prevent ANY possibility of page 2 */
  }

  /* Restore Flexbox so mt-auto pushes signatures to the absolute bottom! */
  .outer-border {
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important;
    border: 6px double #000 !important; /* Extremely robust official border for print */
    outline: none !important; /* Chrome strips outline in print, so we disable it */
    padding: 6px !important; /* Space inside the thick border */
  }
  
  .letter-body {
    flex-grow: 1 !important; /* Let the body stretch naturally */
  }

  /* Shrink table padding to save vertical space */
  .official-table th { padding: 1px !important; }
  .official-table td { padding: 1px 2px !important; }

  /* Reduce whitespace around the main form title */
  .flex-grow > .text-center.mt-4.mb-4 {
    margin-top: 0.25rem !important;
    margin-bottom: 0.25rem !important;
  }

  .mt-auto {
    margin-top: auto !important; /* This now pushes the signature to the bottom of the 338mm page! */
  }

  /* Hide SweetAlert notifications/toasts during print */
  .swal2-container {
    display: none !important;
  }
}
</style>
