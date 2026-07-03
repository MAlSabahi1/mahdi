"""
Excel Reconciliation Processor — محرك المطابقة عبر Excel
═══════════════════════════════════════════════════════════
ينتمي لطبقة Infrastructure لأنه يتعامل مع ملفات Excel وقاعدة البيانات.
يُحقق واجهة IReconciliationProcessor المعرّفة في طبقة الـ Use Cases.

المسؤوليات:
1. قراءة ملف Excel المصدر
2. جلب البيانات من قاعدة البيانات
3. مقارنة وتصنيف النتائج
4. إرجاع ReconciliationResult (Value Object)
"""
from __future__ import annotations

import logging
from difflib import SequenceMatcher
from typing import Dict, List, Optional

import openpyxl

from systems.personnel.models import PersonnelMaster
from ...domain.value_objects.reconciliation import ReconciliationResult

logger = logging.getLogger(__name__)

# نسبة التشابه الدنيا للبحث التقريبي بالاسم
FUZZY_THRESHOLD = 0.85

# الحقول الحساسة (لا يمكن تطبيقها تلقائياً)
SENSITIVE_FIELDS = frozenset(['full_name', 'rank', 'national_id'])

# خريطة الأعمدة العربية → أسماء الحقول
ARABIC_FIELD_MAP: Dict[str, str] = {
    'الرقم العسكري': 'military_number',
    'الاسم الكامل': 'full_name',
    'الاسم': 'full_name',
    'الرتبة': 'rank',
    'الرقم الوطني': 'national_id',
    'الحالة': 'current_status',
    'الحالة الحالية': 'current_status',
    'المؤهل': 'qualification',
}


class ExcelReconciliationProcessor:
    """
    محرك المطابقة — يُحقق واجهة IReconciliationProcessor.

    يقرأ ملف Excel، يقارن مع قاعدة البيانات، ويعيد ReconciliationResult.
    يستخدمه ExecuteReconciliationUseCase عبر Dependency Injection.
    """

    def process(
        self,
        file_path: str,
        key_field: str,
        task_type: str,
    ) -> ReconciliationResult:
        """
        نقطة الدخول الرئيسية — يُستدعى من الـ Use Case.

        Args:
            file_path: المسار الكامل لملف Excel
            key_field: حقل الربط (military_number | national_id)
            task_type: نوع المطابقة (attendance | payroll | qualification)

        Returns:
            ReconciliationResult: نتيجة المطابقة (Value Object ثابت)
        """
        logger.info(
            f"بدء مطابقة | type={task_type} | key={key_field} | file={file_path}"
        )

        # 1. قراءة ملف Excel
        file_data = self._read_excel(file_path)
        logger.info(f"تم قراءة {len(file_data)} صف من الملف")

        # 2. جلب بيانات قاعدة البيانات
        db_data = self._get_db_data(key_field)
        logger.info(f"تم جلب {len(db_data)} فرد من قاعدة البيانات")

        # 3. مقارنة وتصنيف
        comparison = self._compare(file_data, db_data, key_field)

        # 4. تحويل إلى Value Object
        matched_count = len(comparison["matched"])
        unmatched_count = (
            len(comparison["different"])
            + len(comparison["new_in_file"])
            + len(comparison["missing_from_file"])
        )
        errors = [
            f"تنبيه حساس: {alert['key']} — {alert.get('name', '')}"
            for alert in comparison.get("sensitive_alerts", [])
        ]

        result = ReconciliationResult(
            matched=matched_count,
            unmatched=unmatched_count,
            errors=errors,
        )

        logger.info(f"اكتملت المطابقة | {result.summary}")
        return result

    # ──────────────────────────────────────────────
    # Private: قراءة Excel
    # ──────────────────────────────────────────────

    def _read_excel(self, file_path: str) -> List[Dict]:
        """قراءة ملف Excel وتحويله لقائمة قواميس."""
        wb = openpyxl.load_workbook(file_path, data_only=True, read_only=True)
        ws = wb.active

        headers = []
        rows_data = []

        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i == 0:
                headers = [str(cell).strip() if cell else "" for cell in row]
                continue

            if not row or not row[0]:
                continue

            row_dict = {}
            for col_idx, header in enumerate(headers):
                if col_idx < len(row):
                    row_dict[header] = str(row[col_idx]).strip() if row[col_idx] else ""

            rows_data.append(row_dict)

        wb.close()
        return rows_data

    # ──────────────────────────────────────────────
    # Private: جلب بيانات DB
    # ──────────────────────────────────────────────

    def _get_db_data(self, key_field: str) -> Dict[str, PersonnelMaster]:
        """جلب بيانات الأفراد من قاعدة البيانات وفهرستها بالمفتاح."""
        qs = PersonnelMaster.objects.select_related(
            "current_rank", "current_status", "central_department"
        ).all()

        db_map: Dict[str, PersonnelMaster] = {}
        for person in qs.iterator(chunk_size=2000):
            key = getattr(person, key_field, "")
            if key:
                db_map[str(key)] = person

        return db_map

    # ──────────────────────────────────────────────
    # Private: مقارنة وتصنيف
    # ──────────────────────────────────────────────

    def _compare(
        self,
        file_data: List[Dict],
        db_data: Dict[str, PersonnelMaster],
        key_field: str,
    ) -> Dict:
        """مقارنة بيانات الملف مع قاعدة البيانات وتصنيف النتائج."""
        matched = []
        different = []
        new_in_file = []
        sensitive_alerts = []
        file_keys = set()

        for row in file_data:
            key = row.get("الرقم العسكري", "") or row.get("الرقم الوطني", "")
            if not key:
                continue

            file_keys.add(key)

            if key not in db_data:
                # بحث تقريبي بالاسم
                name = row.get("الاسم الكامل", "") or row.get("الاسم", "")
                fuzzy = self._fuzzy_match(name, db_data) if name else None

                new_in_file.append(
                    {"key": key, "file_data": row, "fuzzy_suggestion": fuzzy}
                )
                continue

            # موجود في كلاهما → مقارنة التفاصيل
            person = db_data[key]
            diffs = self._find_differences(row, person)

            if not diffs:
                matched.append({"key": key, "name": person.full_name})
            else:
                sensitive = [d for d in diffs if d["field"] in SENSITIVE_FIELDS]
                non_sensitive = [d for d in diffs if d["field"] not in SENSITIVE_FIELDS]

                if sensitive:
                    sensitive_alerts.append(
                        {"key": key, "name": person.full_name, "alerts": sensitive}
                    )
                if non_sensitive:
                    different.append(
                        {
                            "key": key,
                            "name": person.full_name,
                            "personnel_id": person.pk,
                            "differences": non_sensitive,
                        }
                    )

        # المفقودون من الملف
        missing_from_file = [
            {
                "key": k,
                "name": p.full_name,
                "status": p.current_status.name if p.current_status else "",
            }
            for k, p in db_data.items()
            if k not in file_keys
        ]

        return {
            "matched": matched,
            "different": different,
            "new_in_file": new_in_file,
            "missing_from_file": missing_from_file,
            "sensitive_alerts": sensitive_alerts,
        }

    # ──────────────────────────────────────────────
    # Private: البحث عن الاختلافات
    # ──────────────────────────────────────────────

    def _find_differences(self, file_row: Dict, person: PersonnelMaster) -> List[Dict]:
        """مقارنة صف الملف مع بيانات الفرد."""
        db_values = {
            "military_number": person.military_number,
            "full_name": person.full_name,
            "rank": person.current_rank.name if person.current_rank else "",
            "national_id": person.national_id or "",
            "current_status": (
                person.current_status.name if person.current_status else ""
            ),
        }

        diffs = []
        for arabic_name, field_name in ARABIC_FIELD_MAP.items():
            if arabic_name in file_row and field_name in db_values:
                file_val = file_row[arabic_name].strip()
                db_val = str(db_values[field_name]).strip()

                if file_val and db_val and file_val != db_val:
                    diffs.append(
                        {
                            "field": field_name,
                            "field_arabic": arabic_name,
                            "file_value": file_val,
                            "db_value": db_val,
                        }
                    )

        return diffs

    # ──────────────────────────────────────────────
    # Private: بحث تقريبي بالاسم
    # ──────────────────────────────────────────────

    def _fuzzy_match(
        self, name: str, db_data: Dict[str, PersonnelMaster]
    ) -> Optional[Dict]:
        """بحث تقريبي بالاسم باستخدام Levenshtein (SequenceMatcher ≥ 85%)."""
        best_match = None
        best_ratio = 0.0

        for key, person in db_data.items():
            ratio = SequenceMatcher(None, name, person.full_name).ratio()
            if ratio > best_ratio and ratio >= FUZZY_THRESHOLD:
                best_ratio = ratio
                best_match = {
                    "key": key,
                    "name": person.full_name,
                    "similarity": round(ratio * 100, 1),
                }

        return best_match
