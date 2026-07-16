"""
Proactive Engine Service
═══════════════════════════════════════
الخدمة المركزية لمحرك الإنذارات المبكرة.
يُستخدم من:
  1. API View (EarlyWarningsEngineView) — لعرض النتائج فورياً في الشاشة
  2. Management Command (run_proactive_engine) — لحقن الإشعارات في الخلفية

مبادئ التصميم:
  - لا تكرار: منطق الفحص في مكان واحد فقط
  - لا قيم مثبتة: كل الأرقام تُقرأ من SystemSetting
  - الحساب من البيانات الأصلية: العمر من birth_date، الخدمة من join_date
"""
from dateutil.relativedelta import relativedelta
from datetime import date, datetime

from systems.personnel.models import PersonnelMaster
from systems.services.infrastructure.models import StatusChangeForm
from core.models.settings import SystemSetting

# ── مستويات الخطورة ──────────────────────────────────────────────────────────
URGENCY_EXCEEDED = 'exceeded'
URGENCY_CRITICAL = 'critical'
URGENCY_HIGH = 'high'
URGENCY_MEDIUM = 'medium'
URGENCY_LOW = 'low'
URGENCY_INFO = 'info'

# ── خريطة الحالات المؤقتة → نوع الاستمارة ────────────────────────────────────
TEMP_STATUS_MAP = {
    'المفرغين للدراسة': 'study_leave',
    'المنتدبين لدى جهات': 'seconded',
    'السجناء': 'imprisoned',
    'المفرغين للمرافقة': 'escort',
}

# ── الحالات النشطة المعتبرة ───────────────────────────────────────────────────
ACTIVE_STATUSES = ['في الخدمة', 'عامل', 'ميدان', 'نشط', 'موجود']
ALL_TRACKED_STATUSES = ACTIVE_STATUSES + list(TEMP_STATUS_MAP.keys())


def calc_age_and_service(person):
    """حساب العمر الحقيقي ومدة الخدمة الفعلية من بيانات الفرد الأساسية."""
    today = date.today()
    age_years = age_months = service_years = service_months = None

    if person.birth_date:
        diff = relativedelta(today, person.birth_date)
        age_years = diff.years
        age_months = diff.months

    if person.join_date:
        diff = relativedelta(today, person.join_date)
        service_years = diff.years
        service_months = diff.months

    return age_years, age_months, service_years, service_months


def build_person_info(person, age_years, age_months, service_years, service_months):
    """بناء dict موحد لبيانات الفرد."""
    return {
        'military_number': person.military_number,
        'full_name': person.full_name,
        'rank': person.current_rank.name if person.current_rank else '—',
        'status': person.current_status.name if person.current_status else '—',
        'unit': person.unit.name if person.unit else (person.branch.name if person.branch else '—'),
        'security_admin': person.security_admin.name if person.security_admin else '—',
        'birth_date': str(person.birth_date) if person.birth_date else None,
        'join_date': str(person.join_date) if person.join_date else None,
        'age_years': age_years,
        'age_months': age_months,
        'service_years': service_years,
        'service_months': service_months,
    }


def run_engine_scan():
    """
    تشغيل المحرك الاستباقي الكامل.
    يقرأ كل الإعدادات من قاعدة البيانات، يفحص كل الأفراد،
    ويُعيد (warnings, stats, settings_used).
    """
    # ── 1. جلب جميع الإعدادات من قاعدة البيانات ──────────────────────────
    retirement_age = SystemSetting.get_setting('retirement_age_general', 60)
    min_service_years = SystemSetting.get_setting('min_service_years', 35)
    warning_months = SystemSetting.get_setting('early_warning_months', 6)
    temp_warning_days = SystemSetting.get_setting('temp_status_warning_days', 30)

    settings_used = {
        'retirement_age': retirement_age,
        'min_service_years': min_service_years,
        'warning_months': warning_months,
        'temp_warning_days': temp_warning_days,
    }

    personnel = PersonnelMaster.objects.select_related(
        'current_status', 'current_rank', 'security_admin', 'branch', 'unit'
    ).filter(
        current_status__name__in=ALL_TRACKED_STATUSES
    )

    warnings = []
    stats = {
        'exceeded_age': 0,
        'exceeded_service': 0,
        'approaching': 0,
        'missing_data': 0,
        'temp_status_ending': 0,
        'total': 0,
    }

    today = date.today()

    for person in personnel:
        age_years, age_months, service_years, service_months = calc_age_and_service(person)
        person_info = build_person_info(person, age_years, age_months, service_years, service_months)

        # ── A. فحص البيانات الناقصة ─────────────────────────────────────
        missing = []
        if not person.birth_date:
            missing.append('تاريخ الميلاد')
        if not person.join_date:
            missing.append('تاريخ الالتحاق')

        if missing:
            warnings.append({
                **person_info,
                'warning_type': 'missing_data',
                'urgency': URGENCY_INFO,
                'message': f'بيانات ناقصة: {", ".join(missing)} — لا يمكن حساب الأعمار والمدد',
                'category': 'personnel',
            })
            stats['missing_data'] += 1
            continue

        # ── B. فحص بلوغ/تجاوز السن ─────────────────────────────────────
        if age_years is not None:
            if age_years >= retirement_age:
                months_over = (age_years - retirement_age) * 12 + (age_months or 0)
                warnings.append({
                    **person_info,
                    'warning_type': 'age_exceeded',
                    'urgency': URGENCY_EXCEEDED,
                    'message': f'تجاوز السن القانوني للتقاعد ({retirement_age} سنة) بـ {months_over} شهر',
                    'category': 'retirement',
                })
                stats['exceeded_age'] += 1
            else:
                months_remaining = (retirement_age - age_years) * 12 - (age_months or 0)
                if months_remaining <= 1:
                    urgency = URGENCY_CRITICAL
                    msg = f'سيبلغ السن القانوني خلال أقل من شهر'
                elif months_remaining <= 3:
                    urgency = URGENCY_HIGH
                    msg = f'سيبلغ السن القانوني خلال {months_remaining} شهر'
                elif months_remaining <= 6:
                    urgency = URGENCY_MEDIUM
                    msg = f'سيبلغ السن القانوني خلال {months_remaining} شهر'
                elif months_remaining <= 12:
                    urgency = URGENCY_LOW
                    msg = f'سيبلغ السن القانوني خلال {months_remaining} شهر (أقل من سنة)'
                else:
                    urgency = None

                if urgency:
                    warnings.append({
                        **person_info,
                        'warning_type': 'age_approaching',
                        'urgency': urgency,
                        'months_remaining': months_remaining,
                        'message': msg,
                        'category': 'retirement',
                    })
                    stats['approaching'] += 1

        # ── C. فحص مدة الخدمة ───────────────────────────────────────────
        if service_years is not None and service_years >= min_service_years:
            years_over = service_years - min_service_years
            warnings.append({
                **person_info,
                'warning_type': 'service_exceeded',
                'urgency': URGENCY_EXCEEDED if years_over >= 2 else URGENCY_HIGH,
                'message': f'أكمل مدة الخدمة ({min_service_years} سنة) ويتجاوزها بـ {years_over} سنة',
                'category': 'retirement',
            })
            stats['exceeded_service'] += 1

        # ── D. فحص انتهاء الحالات المؤقتة ───────────────────────────────
        if person.current_status and person.current_status.name in TEMP_STATUS_MAP:
            form_type = TEMP_STATUS_MAP[person.current_status.name]
            latest_form = StatusChangeForm.objects.filter(
                personnel=person,
                form_type=form_type,
                status='approved'
            ).order_by('-effective_date', '-created_at').first()

            if latest_form and latest_form.form_data and 'end_date' in latest_form.form_data:
                end_date_str = latest_form.form_data.get('end_date')
                if end_date_str:
                    try:
                        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                        days_left = (end_date - today).days

                        if days_left < 0:
                            warnings.append({
                                **person_info,
                                'warning_type': 'temp_status_ended',
                                'urgency': URGENCY_EXCEEDED,
                                'message': f'انتهت فترة ({person.current_status.name}) منذ {-days_left} يوم ولم يُتخذ إجراء.',
                                'category': 'services',
                            })
                            stats['temp_status_ending'] += 1
                        elif days_left <= temp_warning_days:
                            warnings.append({
                                **person_info,
                                'warning_type': 'temp_status_ending_soon',
                                'urgency': URGENCY_HIGH if days_left <= 7 else URGENCY_MEDIUM,
                                'message': f'ستنتهي فترة ({person.current_status.name}) بعد {days_left} يوم.',
                                'category': 'services',
                            })
                            stats['temp_status_ending'] += 1
                    except (ValueError, TypeError):
                        pass

    stats['total'] = len(warnings)

    # ── ترتيب حسب الخطورة ────────────────────────────────────────────────
    urgency_order = {
        URGENCY_EXCEEDED: 0, URGENCY_CRITICAL: 1, URGENCY_HIGH: 2,
        URGENCY_MEDIUM: 3, URGENCY_LOW: 4, URGENCY_INFO: 5,
    }
    warnings.sort(key=lambda w: urgency_order.get(w.get('urgency', 'info'), 5))

    return warnings, stats, settings_used
