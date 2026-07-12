import re
import sys

def modify_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for old, new in replacements:
        if old not in content:
            print(f"Warning: Could not find string to replace in {filepath}:\n{old}\n---")
        content = content.replace(old, new)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Modified {filepath}")

# KYC Portal Template Replacements
kyc_replacements = [
    (
        "العودة للوحة التحكم",
        "{{ t('العودة للوحة التحكم', 'Back to Dashboard') }}"
    ),
    (
        "<span>الوثيقة</span>",
        "<span>{{ t('الوثيقة', 'Document') }}</span>"
    ),
    (
        "<span>المرفقات</span>",
        "<span>{{ t('المرفقات', 'Attachments') }}</span>"
    ),
    (
        "<span>التوثيق</span>",
        "<span>{{ t('التوثيق', 'Verification') }}</span>"
    ),
    (
        "<h2 class=\"step-title\">تحديد نوع الهوية</h2>",
        "<h2 class=\"step-title\">{{ t('تحديد نوع الهوية', 'Select ID Type') }}</h2>"
    ),
    (
        "<p class=\"step-subtitle\">الرجاء اختيار نوع الوثيقة الرسمية للمطابقة الحيوية.</p>",
        "<p class=\"step-subtitle\">{{ t('الرجاء اختيار نوع الوثيقة الرسمية للمطابقة الحيوية.', 'Please select the official document type for biometric matching.') }}</p>"
    ),
    (
        "<h3>البطاقة الشخصية</h3>",
        "<h3>{{ t('البطاقة الشخصية', 'National ID') }}</h3>"
    ),
    (
        "<p>الهوية الوطنية الإلكترونية</p>",
        "<p>{{ t('الهوية الوطنية الإلكترونية', 'Electronic National Identity') }}</p>"
    ),
    (
        "<h3>جواز السفر</h3>",
        "<h3>{{ t('جواز السفر', 'Passport') }}</h3>"
    ),
    (
        "<p>جواز السفر المعتمد</p>",
        "<p>{{ t('جواز السفر المعتمد', 'Approved Passport') }}</p>"
    ),
    (
        "متابعة الخطوة التالية",
        "{{ t('متابعة الخطوة التالية', 'Continue to Next Step') }}"
    ),
    (
        "<h2 class=\"step-title\">إرفاق المستندات والصور</h2>",
        "<h2 class=\"step-title\">{{ t('إرفاق المستندات والصور', 'Attach Documents & Photos') }}</h2>"
    ),
    (
        "<p class=\"step-subtitle\">قم بالتقاط صورة واضحة للوثيقة، وصورة أمامية لوجهك (سيلفي) بدون نظارات.</p>",
        "<p class=\"step-subtitle\">{{ t('قم بالتقاط صورة واضحة للوثيقة، وصورة أمامية لوجهك (سيلفي) بدون نظارات.', 'Take a clear picture of the document and a front picture of your face (selfie) without glasses.') }}</p>"
    ),
    (
        "<div v-if=\"slotStatus.front.state === 'loading'\" class=\"slot-loader\">جاري الفحص...</div>",
        "<div v-if=\"slotStatus.front.state === 'loading'\" class=\"slot-loader\">{{ t('جاري الفحص...', 'Scanning...') }}</div>"
    ),
    (
        "<div v-if=\"slotStatus.back.state === 'loading'\" class=\"slot-loader\">جاري الفحص...</div>",
        "<div v-if=\"slotStatus.back.state === 'loading'\" class=\"slot-loader\">{{ t('جاري الفحص...', 'Scanning...') }}</div>"
    ),
    (
        "<div v-if=\"slotStatus.selfie.state === 'loading'\" class=\"slot-loader\">جاري الفحص...</div>",
        "<div v-if=\"slotStatus.selfie.state === 'loading'\" class=\"slot-loader\">{{ t('جاري الفحص...', 'Scanning...') }}</div>"
    ),
    (
        "<span>{{ selectedDocType === 'PASSPORT' ? 'صفحة بيانات الجواز' : 'الواجهة الأمامية للبطاقة' }}</span>",
        "<span>{{ selectedDocType === 'PASSPORT' ? t('صفحة بيانات الجواز', 'Passport Data Page') : t('الواجهة الأمامية للبطاقة', 'Front of ID Card') }}</span>"
    ),
    (
        "<span class=\"action-text\">اضغط للالتقاط</span>",
        "<span class=\"action-text\">{{ t('اضغط للالتقاط', 'Click to Capture') }}</span>"
    ),
    (
        "<div v-if=\"previews.front && slotStatus.front.state !== 'error'\" class=\"edit-badge\">تعديل</div>",
        "<div v-if=\"previews.front && slotStatus.front.state !== 'error'\" class=\"edit-badge\">{{ t('تعديل', 'Edit') }}</div>"
    ),
    (
        "<div v-if=\"previews.back && slotStatus.back.state !== 'error'\" class=\"edit-badge\">تعديل</div>",
        "<div v-if=\"previews.back && slotStatus.back.state !== 'error'\" class=\"edit-badge\">{{ t('تعديل', 'Edit') }}</div>"
    ),
    (
        "<div v-if=\"previews.selfie && slotStatus.selfie.state !== 'error'\" class=\"edit-badge\">تعديل</div>",
        "<div v-if=\"previews.selfie && slotStatus.selfie.state !== 'error'\" class=\"edit-badge\">{{ t('تعديل', 'Edit') }}</div>"
    ),
    (
        "<span>الواجهة الخلفية للبطاقة</span>",
        "<span>{{ t('الواجهة الخلفية للبطاقة', 'Back of ID Card') }}</span>"
    ),
    (
        "<span>صورة الوجه (سيلفي حي)</span>",
        "<span>{{ t('صورة الوجه (سيلفي حي)', 'Face Photo (Live Selfie)') }}</span>"
    ),
    (
        "<span class=\"action-text\">اضغط لفتح الكاميرا</span>",
        "<span class=\"action-text\">{{ t('اضغط لفتح الكاميرا', 'Click to Open Camera') }}</span>"
    ),
    (
        ">السابق</button>",
        ">{{ t('السابق', 'Previous') }}</button>"
    ),
    (
        ">بدء التوثيق الأمني</button>",
        ">{{ t('بدء التوثيق الأمني', 'Start Security Verification') }}</button>"
    ),
    (
        "<div class=\"target-overlay-label\">{{ selectedDocType === 'PASSPORT' ? 'الجواز' : 'الواجهة الأمامية' }}</div>",
        "<div class=\"target-overlay-label\">{{ selectedDocType === 'PASSPORT' ? t('الجواز', 'Passport') : t('الواجهة الأمامية', 'Front Side') }}</div>"
    ),
    (
        "<div class=\"target-overlay-label\">الواجهة الخلفية</div>",
        "<div class=\"target-overlay-label\">{{ t('الواجهة الخلفية', 'Back Side') }}</div>"
    ),
    (
        "<div class=\"target-overlay-label\">السيلفي الحي</div>",
        "<div class=\"target-overlay-label\">{{ t('السيلفي الحي', 'Live Selfie') }}</div>"
    ),
    (
        "<p class=\"processing-subtitle\">نرجو الانتظار، تتم معالجة وتشفير البيانات حيوياً لضمان أعلى معايير الأمان.</p>",
        "<p class=\"processing-subtitle\">{{ t('نرجو الانتظار، تتم معالجة وتشفير البيانات حيوياً لضمان أعلى معايير الأمان.', 'Please wait, data is being processed and encrypted biometrically to ensure the highest security standards.') }}</p>"
    ),
    (
        "{{ resultData.status === 'APPROVED' ? 'تم الاعتماد بنجاح' : 'فشل التوثيق الأمني' }}",
        "{{ resultData.status === 'APPROVED' ? t('تم الاعتماد بنجاح', 'Successfully Approved') : t('فشل التوثيق الأمني', 'Security Verification Failed') }}"
    ),
    (
        "<strong>سبب الرفض:</strong><br>",
        "<strong>{{ t('سبب الرفض:', 'Rejection Reason:') }}</strong><br>"
    ),
    (
        "<span class=\"label\">الاسم الكامل:</span>",
        "<span class=\"label\">{{ t('الاسم الكامل:', 'Full Name:') }}</span>"
    ),
    (
        "<span class=\"label\">درجة الموثوقية الشاملة:</span>",
        "<span class=\"label\">{{ t('درجة الموثوقية الشاملة:', 'Overall Reliability Score:') }}</span>"
    ),
    (
        "<span class=\"label\">نسبة تطابق الهوية مع الوجه:</span>",
        "<span class=\"label\">{{ t('نسبة تطابق الهوية مع الوجه:', 'ID-to-Face Match Ratio:') }}</span>"
    ),
    (
        "<span class=\"label\">البصمة الرقمية للجهاز (Audit):</span>",
        "<span class=\"label\">{{ t('البصمة الرقمية للجهاز (Audit):', 'Device Digital Fingerprint (Audit):') }}</span>"
    ),
    (
        "<span class=\"label\">زمن الفحص والمعالجة الكلي:</span>",
        "<span class=\"label\">{{ t('زمن الفحص والمعالجة الكلي:', 'Total Processing and Scanning Time:') }}</span>"
    ),
    (
        " ثانية</span>",
        " {{ t('ثانية', 'seconds') }}</span>"
    ),
    (
        ">إغلاق وتأكيد العملية</button>",
        ">{{ t('إغلاق وتأكيد العملية', 'Close and Confirm Process') }}</button>"
    ),
    (
        "بوابة التوثيق الرقمية &copy;",
        "{{ t('بوابة التوثيق الرقمية', 'Digital Verification Portal') }} &copy;"
    ),
    (
        "مزود بتقنية <strong>Vladtion Core AI</strong>",
        "{{ t('مزود بتقنية', 'Powered by') }} <strong>Vladtion Core AI</strong>"
    ),
]

kyc_js_replacements = [
    (
        "import CameraModal from '../components/ui/CameraModal.vue'",
        "import CameraModal from '../components/ui/CameraModal.vue'\nimport { useUIState } from '../composables/useUIState'"
    ),
    (
        "// State variables\nconst state = ref('upload')",
        "// State variables\nconst uiState = useUIState()\nconst t = (ar, en) => uiState.state.currentLanguage === 'en' ? en : ar\n\nconst state = ref('upload')"
    ),
    (
        "const analysisTexts = [\n  \"جاري مسح واستخراج البيانات من الوثيقة (OCR)...\",\n  \"فحص حيوية الوجه والأمان (Liveness Detection)...\",\n  \"مطابقة السمات الحيوية بين الوجه والبطاقة (FaceMatch)...\",\n  \"تشفير البيانات وتوليد درجة الموثوقية النهائية...\"\n]\nconst currentAnalysisText = ref(analysisTexts[0])",
        "const analysisTexts = computed(() => [\n  t(\"جاري مسح واستخراج البيانات من الوثيقة (OCR)...\", \"Scanning and extracting data from document (OCR)...\"),\n  t(\"فحص حيوية الوجه والأمان (Liveness Detection)...\", \"Face liveness and security check (Liveness Detection)...\"),\n  t(\"مطابقة السمات الحيوية بين الوجه والبطاقة (FaceMatch)...\", \"Biometric matching between face and ID (FaceMatch)...\"),\n  t(\"تشفير البيانات وتوليد درجة الموثوقية النهائية...\", \"Encrypting data and generating final reliability score...\")\n])\nconst currentAnalysisText = computed(() => analysisTexts.value[analysisPhase.value] || '')"
    ),
    (
        "currentAnalysisText.value = analysisTexts[0];",
        "// currentAnalysisText is computed"
    ),
    (
        "currentAnalysisText.value = analysisTexts[0]",
        "// currentAnalysisText is computed"
    ),
    (
        "currentAnalysisText.value = analysisTexts[1]",
        "// currentAnalysisText is computed"
    ),
    (
        "currentAnalysisText.value = analysisTexts[2]",
        "// currentAnalysisText is computed"
    ),
    (
        "currentAnalysisText.value = analysisTexts[3]",
        "// currentAnalysisText is computed"
    ),
    (
        "return selectedDocType.value === 'PASSPORT' ? 'تصوير الجواز' : 'تصوير الواجهة الأمامية'",
        "return selectedDocType.value === 'PASSPORT' ? t('تصوير الجواز', 'Capture Passport') : t('تصوير الواجهة الأمامية', 'Capture Front Side')"
    ),
    (
        "return 'تصوير الواجهة الخلفية'",
        "return t('تصوير الواجهة الخلفية', 'Capture Back Side')"
    ),
    (
        "return 'التقاط صورة شخصية'",
        "return t('التقاط صورة شخصية', 'Capture Selfie')"
    ),
    (
        "data.message || 'الصورة غير مطابقة'",
        "data.message || t('الصورة غير مطابقة', 'Image does not match')"
    ),
    (
        "slotStatus[type].message = 'تعذر الاتصال بخادم التحقق'",
        "slotStatus[type].message = t('تعذر الاتصال بخادم التحقق', 'Failed to connect to verification server')"
    ),
    (
        "alert(\"خطأ أثناء الإرسال للتقييم المركزي.\")",
        "alert(t(\"خطأ أثناء الإرسال للتقييم المركزي.\", \"Error sending for central evaluation.\"))"
    ),
    (
        "alert(\"تعذر الاتصال بالخادم المركزي.\")",
        "alert(t(\"تعذر الاتصال بالخادم المركزي.\", \"Failed to connect to central server.\"))"
    )
]

kyc_reject_reasons = [
    (
        "if (code === 'SLOT_MISMATCH_FRONT_UPLOADED_ID_CARD_BACK') return 'لقد قمت بإرفاق الواجهة الخلفية للبطاقة في خانة الواجهة الأمامية. يرجى التأكد من اختيار الصورة الصحيحة في المكان المخصص.'",
        "if (code === 'SLOT_MISMATCH_FRONT_UPLOADED_ID_CARD_BACK') return t('لقد قمت بإرفاق الواجهة الخلفية للبطاقة في خانة الواجهة الأمامية. يرجى التأكد من اختيار الصورة الصحيحة في المكان المخصص.', 'You have attached the back of the card in the front side field. Please ensure the correct image is selected.')"
    ),
    (
        "if (code === 'SLOT_MISMATCH_FRONT_UPLOADED_PASSPORT') return 'لقد قمت بإرفاق صورة جواز سفر في خانة البطاقة الشخصية. يرجى تحديد الخيار الصحيح لنوع الوثيقة في الخطوة السابقة.'",
        "if (code === 'SLOT_MISMATCH_FRONT_UPLOADED_PASSPORT') return t('لقد قمت بإرفاق صورة جواز سفر في خانة البطاقة الشخصية. يرجى تحديد الخيار الصحيح لنوع الوثيقة في الخطوة السابقة.', 'You have attached a passport photo in the national ID field. Please select the correct document type.')"
    ),
    (
        "if (code === 'SLOT_MISMATCH_BACK_UPLOADED_ID_CARD_FRONT') return 'لقد قمت بإرفاق الواجهة الأمامية للبطاقة في خانة الواجهة الخلفية. يرجى إرفاق ظهر البطاقة هنا.'",
        "if (code === 'SLOT_MISMATCH_BACK_UPLOADED_ID_CARD_FRONT') return t('لقد قمت بإرفاق الواجهة الأمامية للبطاقة في خانة الواجهة الخلفية. يرجى إرفاق ظهر البطاقة هنا.', 'You have attached the front of the card in the back side field. Please attach the back of the card here.')"
    ),
    (
        "if (code === 'SLOT_MISMATCH_BACK_UPLOADED_PASSPORT') return 'تم رفع صورة جواز سفر في خانة خلفية البطاقة.'",
        "if (code === 'SLOT_MISMATCH_BACK_UPLOADED_PASSPORT') return t('تم رفع صورة جواز سفر في خانة خلفية البطاقة.', 'A passport photo was uploaded in the back of card field.')"
    ),
    (
        "if (code === 'SLOT_MISMATCH_PASSPORT_UPLOADED_ID_CARD_FRONT' || code === 'SLOT_MISMATCH_PASSPORT_UPLOADED_ID_CARD_BACK') return 'لقد قمت بإرفاق بطاقة شخصية في خانة جواز السفر.'",
        "if (code === 'SLOT_MISMATCH_PASSPORT_UPLOADED_ID_CARD_FRONT' || code === 'SLOT_MISMATCH_PASSPORT_UPLOADED_ID_CARD_BACK') return t('لقد قمت بإرفاق بطاقة شخصية في خانة جواز السفر.', 'You have attached a national ID in the passport field.')"
    ),
    (
        "if (code === 'NOT_YEMENI_PASSPORT') return 'الجواز المرفق غير مدعوم في النظام. يُسمح فقط باستخدام جوازات السفر الصادرة عن الجمهورية اليمنية.'",
        "if (code === 'NOT_YEMENI_PASSPORT') return t('الجواز المرفق غير مدعوم في النظام. يُسمح فقط باستخدام جوازات السفر الصادرة عن الجمهورية اليمنية.', 'The attached passport is not supported. Only passports issued by the Republic of Yemen are allowed.')"
    ),
    (
        "if (code === 'POOR_QUALITY' || code === 'M01') return 'الوثيقة غير واضحة أو تحتوي على إضاءة شديدة/انعكاسات. يرجى إعادة التصوير في مكان بإضاءة جيدة لكي يتمكن النظام من قراءة بياناتك.'",
        "if (code === 'POOR_QUALITY' || code === 'M01') return t('الوثيقة غير واضحة أو تحتوي على إضاءة شديدة/انعكاسات. يرجى إعادة التصوير في مكان بإضاءة جيدة لكي يتمكن النظام من قراءة بياناتك.', 'The document is unclear or has severe glare/reflections. Please retake the photo in a well-lit area.')"
    ),
    (
        "if (code === 'INVALID_DOCUMENT') return 'يرجى التأكد من إرفاق وثيقة هوية يمنية رسمية صحيحة، كاملة، ومقروءة تماماً.'",
        "if (code === 'INVALID_DOCUMENT') return t('يرجى التأكد من إرفاق وثيقة هوية يمنية رسمية صحيحة، كاملة، ومقروءة تماماً.', 'Please ensure you attach a valid, complete, and fully readable official Yemeni identity document.')"
    ),
    (
        "if (code === 'NO_FACE_FOUND') return 'لم يتم العثور على وجه واضح في صورة السيلفي أو البطاقة. تأكد من أن وجهك ظاهر بالكامل.'",
        "if (code === 'NO_FACE_FOUND') return t('لم يتم العثور على وجه واضح في صورة السيلفي أو البطاقة. تأكد من أن وجهك ظاهر بالكامل.', 'No clear face was found in the selfie or ID photo. Ensure your face is fully visible.')"
    ),
    (
        "if (code === 'FACE_MISMATCH') return 'الوجه الموجود في السيلفي لا يتطابق مع صورة الشخص الموجودة في وثيقة الهوية.'",
        "if (code === 'FACE_MISMATCH') return t('الوجه الموجود في السيلفي لا يتطابق مع صورة الشخص الموجودة في وثيقة الهوية.', 'The face in the selfie does not match the person in the identity document.')"
    ),
    (
        "if (code === 'SPOOF_DETECTED') return 'اكتشف النظام محاولة تلاعب أمني (تصوير من شاشة أو صورة ورقية بدلاً من وجه حي). يرجى التوثيق المباشر.'",
        "if (code === 'SPOOF_DETECTED') return t('اكتشف النظام محاولة تلاعب أمني (تصوير من شاشة أو صورة ورقية بدلاً من وجه حي). يرجى التوثيق المباشر.', 'Security manipulation attempt detected (photo from a screen or paper). Please use direct verification.')"
    ),
    (
        "if (code === 'SCREENSHOT_DETECTED') return 'تم اكتشاف أن الصورة لقطة شاشة وليست صورة حية. يرجى التقاط صورة مباشرة بالكاميرا.'",
        "if (code === 'SCREENSHOT_DETECTED') return t('تم اكتشاف أن الصورة لقطة شاشة وليست صورة حية. يرجى التقاط صورة مباشرة بالكاميرا.', 'The image is a screenshot, not a live photo. Please capture a live photo with the camera.')"
    ),
    (
        "if (code === 'DEEPFACE_SPOOF') return 'اكتشف النظام أن الصورة ليست لوجه حقيقي حي. يرجى التقاط صورة سيلفي مباشرة.'",
        "if (code === 'DEEPFACE_SPOOF') return t('اكتشف النظام أن الصورة ليست لوجه حقيقي حي. يرجى التقاط صورة سيلفي مباشرة.', 'The image is not of a real live face. Please capture a live selfie.')"
    ),
    (
        "if (code === 'FFT_SPOOF') return 'تم اكتشاف أنماط ترددية تشير إلى تصوير من شاشة إلكترونية. يرجى التقاط صورة مباشرة.'",
        "if (code === 'FFT_SPOOF') return t('تم اكتشاف أنماط ترددية تشير إلى تصوير من شاشة إلكترونية. يرجى التقاط صورة مباشرة.', 'Frequency patterns indicating a photo of an electronic screen were detected. Please capture a live photo.')"
    ),
    (
        "if (code === 'LBP_SPOOF') return 'تم اكتشاف أن نسيج الصورة غير طبيعي (شاشة أو طباعة). يرجى التقاط صورة حية مباشرة.'",
        "if (code === 'LBP_SPOOF') return t('تم اكتشاف أن نسيج الصورة غير طبيعي (شاشة أو طباعة). يرجى التقاط صورة حية مباشرة.', 'Unnatural image texture detected (screen or print). Please capture a direct live photo.')"
    ),
    (
        "if (code === 'STATIC_IMAGE') return 'تم اكتشاف أن الصورة ثابتة تماماً بدون أي حركة طبيعية. يرجى التقاط صورة سيلفي حية.'",
        "if (code === 'STATIC_IMAGE') return t('تم اكتشاف أن الصورة ثابتة تماماً بدون أي حركة طبيعية. يرجى التقاط صورة سيلفي حية.', 'The image is completely static without natural movement. Please capture a live selfie.')"
    ),
    (
        "if (code === 'LOW_FUSION_SCORE') return 'مستوى التحقق من الحيوية منخفض. يرجى التقاط صورة سيلفي واضحة في إضاءة جيدة.'",
        "if (code === 'LOW_FUSION_SCORE') return t('مستوى التحقق من الحيوية منخفض. يرجى التقاط صورة سيلفي واضحة في إضاءة جيدة.', 'Liveness verification score is low. Please capture a clear selfie in good lighting.')"
    ),
    (
        "if (code && code.startsWith('FORENSICS_')) return 'تم اكتشاف محاولة تزييف في الصورة. يرجى التقاط صورة سيلفي حقيقية مباشرة بالكاميرا.'",
        "if (code && code.startsWith('FORENSICS_')) return t('تم اكتشاف محاولة تزييف في الصورة. يرجى التقاط صورة سيلفي حقيقية مباشرة بالكاميرا.', 'A forgery attempt was detected in the image. Please capture a real live selfie with the camera.')"
    ),
    (
        "if (code === 'F03') return 'الوثيقة مرفوضة بسبب انخفاض مستوى الموثوقية الأمنية.'",
        "if (code === 'F03') return t('الوثيقة مرفوضة بسبب انخفاض مستوى الموثوقية الأمنية.', 'The document is rejected due to low security reliability level.')"
    ),
    (
        "return code || 'تم إيقاف العملية تلقائياً لعدم استيفاء المعايير الأمنية.'",
        "return code || t('تم إيقاف العملية تلقائياً لعدم استيفاء المعايير الأمنية.', 'Process stopped automatically for not meeting security standards.')"
    )
]

camera_modal_replacements = [
    (
        "import { ref, watch, nextTick } from 'vue'",
        "import { ref, watch, nextTick } from 'vue'\nimport { useUIState } from '../../composables/useUIState'\n\nconst uiState = useUIState()\nconst t = (ar, en) => uiState.state.currentLanguage === 'en' ? en : ar"
    ),
    (
        "<span>التقاط بالكاميرا</span>",
        "<span>{{ t('التقاط بالكاميرا', 'Capture with Camera') }}</span>"
    ),
    (
        "<span>رفع ملف</span>",
        "<span>{{ t('رفع ملف', 'Upload File') }}</span>"
    ),
    (
        "<p>جاري التحقق من الحيوية...</p>",
        "<p>{{ t('جاري التحقق من الحيوية...', 'Verifying Liveness...') }}</p>"
    ),
    (
        "alert('متصفحك لا يدعم فتح الكاميرا مباشرة (بسبب قيود الأمان). سيتم فتح كاميرا الهاتف الأساسية بدلاً من ذلك.')",
        "alert(t('متصفحك لا يدعم فتح الكاميرا مباشرة (بسبب قيود الأمان). سيتم فتح كاميرا الهاتف الأساسية بدلاً من ذلك.', 'Your browser does not support direct camera access (due to security restrictions). The primary phone camera will be opened instead.'))"
    )
]

files_to_modify = [
    "/home/mahdi/Desktop/project_compny/vladtion/frontend/src/views/OfficialKycPortal.vue",
    "/home/mahdi/Desktop/project_compny/vladtion/frontend/src/components/ui/CameraModal.vue"
]

print("Modifying OfficialKycPortal.vue...")
modify_file(files_to_modify[0], kyc_replacements + kyc_js_replacements + kyc_reject_reasons)

print("Modifying CameraModal.vue...")
modify_file(files_to_modify[1], camera_modal_replacements)

