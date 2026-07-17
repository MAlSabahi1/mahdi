<template>
  <div class="print-preview-container relative" style="--th-bg-color: #f0f0f0; --th-text-color: #000000">
    <div class="outer-border h-full flex flex-col relative z-10">
      
      <!-- Top Header -->
      <div class="border-[1.5px] border-gray-900 rounded-lg p-2 pt-2 pb-0 flex justify-between items-start text-sm font-bold text-gray-900 relative bg-white mx-1 mt-1">
        
        <!-- Right: Logo/Republic Info -->
        <div class="text-right w-1/3 space-y-1 pr-1 leading-tight font-amiri text-black">
          <img src="/images/yemen_calligraphy_cropped.png" alt="الجمهورية اليمنية" class="h-7 w-auto inline-block mb-1" />
          <p class="text-[14px]">وزارة الداخلية</p>
          <p class="text-[13.5px]">وكيل قطاع الموارد البشرية</p>
          <p class="text-[13.5px]">الإدارة العامة للقوى البشرية</p>
          <p class="text-[13.5px]">{{ departmentName || 'لجنة بناء الامدادات' }}</p>
        </div>
        
        <!-- Center: Emblem Image & Bismillah -->
        <div class="text-center w-1/3 flex flex-col justify-center items-center">
          <img src="/images/bismillah_cropped.png" alt="بسم الله الرحمن الرحيم" class="h-7 w-auto max-w-full object-contain mb-1" />
          <img src="/images/logo/yemen_logo_clean.png" alt="شعار الجمهورية" class="h-auto max-h-[5.5rem] w-auto max-w-full object-contain" />
        </div>
        
        <!-- Left: Document Info (Slot for flexibility) -->
        <div class="w-1/3 flex justify-end pl-1 pt-1 font-amiri text-black">
          <slot name="document-info">
            <div class="space-y-1.5 text-[14px] leading-tight font-bold">
              <div class="flex items-center">
                <span class="w-[5rem] text-right">الـرقـــــــــم/</span>
                <span class="font-sans font-bold text-[13px] tracking-wider">{{ documentNumber || '.......................' }}</span>
              </div>
              <div class="flex items-center">
                <span class="w-[5rem] text-right">التاريــــــــخ/</span>
                <div class="flex justify-between items-center w-full font-sans font-bold text-[13px] tracking-wider">
                  <span>{{ documentDate || new Date().toLocaleDateString('en-GB') }}</span>
                  <span class="font-serif font-normal mr-1">م</span>
                </div>
              </div>
              <div class="flex items-center">
                <span class="w-[5rem] text-right">الــمـوافـــــق/</span>
                <span class="tracking-widest">.......................</span>
              </div>
              <div class="flex items-center">
                <span class="w-[5rem] text-right">الـمـرفـقــــات/</span>
                <span class="font-bold underline text-[12px]">{{ attachmentsText || '.......................' }}</span>
              </div>
            </div>
          </slot>
        </div>
        
      </div> <!-- End Header -->

      <!-- Divider (Thin) -->
      <div class="w-full h-[1.5px] bg-black mt-2 mb-1"></div>

      <!-- Main Content Area -->
      <div class="flex-grow px-2 flex flex-col relative">
        <slot name="body"></slot>
      </div>

      <!-- Signatures & Approvals -->
      <div class="mt-auto pt-1 pb-1">
        <slot name="signatures">
          <div class="border-[1.5px] border-gray-900 rounded-lg p-1.5 pb-2 grid grid-cols-3 gap-1 text-[11px] font-bold text-gray-900 text-center relative mx-1">
            <div class="absolute -top-2.5 right-6 bg-white px-2 font-bold text-gray-900 text-[11px]">التوقيعات والاعتمادات</div>
            
            <div class="space-y-1.5 flex flex-col items-start text-right pr-2">
              <p class="mb-0.5 font-bold text-[11.5px]">إعداد (قسم الخدمات)</p>
              <div class="space-y-0.5 w-full max-w-[170px]">
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">الاسم:</span> <span class="flex-1 text-right">............................</span></p>
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">الرتبة:</span> <span class="flex-1 text-right">............................</span></p>
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">التوقيع:</span> <span class="flex-1 text-right">............................</span></p>
              </div>
            </div>
            
            <div class="space-y-1.5 flex flex-col items-center">
              <p class="mb-0.5 font-bold text-[11.5px]">مراجعة (مدير إدارة القوى البشرية)</p>
              <div class="space-y-0.5 w-full max-w-[170px]">
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">الاسم:</span> <span class="flex-1 text-right">............................</span></p>
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">الرتبة:</span> <span class="flex-1 text-right">............................</span></p>
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">التوقيع:</span> <span class="flex-1 text-right">............................</span></p>
              </div>
            </div>
            
            <div class="space-y-1.5 flex flex-col items-end text-right pl-2">
              <p class="mb-0.5 font-bold text-[11.5px]">اعتماد (مدير عام شرطة المحافظة)</p>
              <div class="space-y-0.5 w-full max-w-[170px]">
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">الاسم:</span> <span class="flex-1 text-right">............................</span></p>
                <p class="flex items-center"><span class="w-10 text-right text-[11.5px]">الرتبة:</span> <span class="flex-1 text-right">............................</span></p>
                <div class="flex items-center relative"><span class="w-10 text-right z-10 text-[11.5px] mt-0.5">التوقيع:</span> 
                  <div class="flex-1 text-right relative z-10">
                    <span class="leading-none">............................</span>
                    <div class="absolute bottom-[-5px] right-2 w-10 h-10 border border-dashed border-gray-400 rounded-full flex items-center justify-center opacity-60 z-0 -rotate-12 pointer-events-none">
                      <span class="text-gray-400 text-[6.5px] font-black text-center leading-tight">الختم<br>الرسمي</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </slot>
        
        <!-- Security Tracking Footer -->
        <div class="flex items-center justify-between text-[6.5px] text-gray-500 font-medium border-t border-gray-400 pt-1 mt-1.5 mx-1">
          <div class="space-y-0.5 text-right flex-1 font-sans">
            <p>طُبع بواسطة: <span class="font-bold text-gray-800">{{ printedBy || 'النظام' }}</span> | بتاريخ: <span class="font-bold text-gray-800" dir="ltr">{{ new Date().toLocaleString('en-GB') }}</span></p>
            <p v-if="referenceNumber">المرجع (REF): <span class="font-bold text-gray-800 font-mono tracking-wider">{{ referenceNumber }}</span></p>
          </div>
          <div class="flex items-center gap-1 pr-3 border-r border-gray-300">
            <!-- Dummy QR -->
            <svg class="h-5 w-5 text-gray-900" viewBox="0 0 33 33" fill="currentColor" shape-rendering="crispEdges">
              <path d="M0 0h9v9H0zM2 2v5h5V2zM24 0h9v9h-9zM26 2v5h5V2zM0 24h9v9H0zM2 26v5h5v-5zM12 0h2v2h-2zM16 0h5v2h-5zM22 0h1v2h-1zM10 2h2v3h-2zM14 2h1v1h-1zM16 3h2v2h-2zM20 3h1v2h-1zM10 6h3v2h-3zM14 5h1v1h-1zM17 6h5v2h-5zM12 9h2v2h-2zM15 9h1v3h-1zM17 9h2v1h-2zM20 9h3v1h-3zM25 10h2v2h-2zM28 10h5v1h-5zM0 10h2v1H0zM3 10h2v2H3zM6 10h2v3H6zM9 10h2v2H9zM12 12h2v2h-2zM17 11h2v3h-2zM21 11h2v1h-2zM27 12h2v1h-2zM31 12h2v2h-2zM0 12h1v3H0zM2 13h2v1H2zM9 13h2v1H9zM20 13h1v3h-1zM23 13h3v2h-3zM29 14h2v2h-2zM4 14h1v1H4zM6 14h1v3H6zM8 15h3v2H8zM12 15h1v1h-1zM14 15h2v3h-2zM18 15h1v2h-1zM27 15h1v2h-1zM32 15h1v3h-1zM1 16h2v2H1zM4 16h1v2H4zM12 17h1v1h-1zM17 17h1v3h-1zM20 17h2v2h-2zM23 16h2v1h-2zM26 18h2v2h-2zM29 17h2v1h-2zM7 18h1v3H7zM9 18h2v1H9zM12 19h4v2h-4zM19 19h1v1h-1zM22 18h3v1h-3zM28 19h1v3h-1zM31 19h2v1h-2zM0 20h2v2H0zM3 20h3v1H3zM9 20h2v2H9zM17 21h2v1h-2zM20 20h1v2h-1zM23 20h1v1h-1zM25 21h2v2h-2zM30 21h3v2h-3zM2 23h2v1H2zM5 22h3v2H5zM11 22h2v1h-2zM14 21h2v2h-2zM18 23h3v1h-3zM22 22h2v1h-2zM25 24h1v1h-1zM27 24h5v2h-5zM10 24h3v1h-3zM14 24h2v2h-2zM17 25h1v1h-1zM19 25h2v2h-2zM22 24h2v3h-2zM25 26h1v3h-1zM28 27h2v2h-2zM31 26h2v1h-2zM10 26h1v2h-1zM12 27h2v2h-2zM15 26h1v2h-1zM17 27h2v2h-2zM20 28h1v3h-1zM22 28h1v1h-1zM27 28h1v1h-1zM32 28h1v2h-1zM10 29h2v2h-2zM13 30h1v3h-1zM15 29h2v1h-2zM18 30h1v3h-1zM22 30h2v1h-2zM25 30h2v3h-2zM29 31h3v2h-3zM10 32h2v1h-2zM15 31h2v2h-2zM21 32h3v1h-3z" />
            </svg>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  departmentName?: string
  documentNumber?: string
  documentDate?: string
  attachmentsText?: string
  printedBy?: string
  referenceNumber?: string
}>()
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
  width: 210mm;
  min-height: 297mm; 
  background: white;
  margin: 0 auto;
  box-sizing: border-box;
  color: #000;
  padding: 10px;
}

.outer-border {
  border: 1.5px solid #000;
  outline: 3px solid #000;
  outline-offset: -4px;
  padding: 3px;
}
</style>

<style>
@media print {
  @page portrait-page {
    size: A4 portrait;
    margin: 5mm !important;
  }
  
  html, body {
    margin: 0 !important;
    padding: 0 !important;
    background: white !important;
    height: auto !important;
  }
  
  * {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    color-adjust: exact !important;
  }

  .print-preview-container {
    page: portrait-page;
    width: 100% !important; 
    min-height: 270mm !important;
    height: auto !important;
    margin: 0 auto !important;
    padding: 0 !important;
    box-shadow: none !important;
    box-sizing: border-box !important;
    page-break-after: always;
    page-break-inside: avoid;
  }

  .outer-border {
    display: flex !important;
    flex-direction: column !important;
    min-height: 270mm !important;
    height: auto !important;
    border: 3px solid #000 !important; 
    outline: 1px solid #000 !important;
    outline-offset: 2px !important;
    padding: 4px !important; 
    box-sizing: border-box !important;
  }
}
</style>
