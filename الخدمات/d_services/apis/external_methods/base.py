"""
External Method Handler - معالج الدوال الخارجية الآمن
يوفر طريقة آمنة ومركزية لتنفيذ الدوال الديناميكية من قاعدة البيانات
"""
import logging
import re
from typing import Any, Callable, Optional, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class FunctionType(str, Enum):
    """أنواع الدوال الخارجية"""
    VALIDATOR = 'validator'              # validation_procedure_name
    EXECUTION = 'execution'              # execution_procedure_name
    OUTPUT_DATA = 'output_data'          # output_data_function, custom_output_function
    INPUT_DATA = 'input_data'            # input_data_function, custom_input_function
    REQUESTER = 'requester'              # requester_image_function, requester_info_function
    ERP_DATA = 'erp_data'                # erp_data_function


# ربط كل نوع بالملف المخصص له
FUNCTION_TYPE_MODULES = {
    FunctionType.VALIDATOR: 'd_services.apis.external_methods.validators',
    FunctionType.EXECUTION: 'd_services.apis.external_methods.execution',
    FunctionType.OUTPUT_DATA: 'd_services.apis.external_methods.output_data',
    FunctionType.INPUT_DATA: 'd_services.apis.external_methods.input_data',
    FunctionType.REQUESTER: 'd_services.apis.external_methods.requester',
    FunctionType.ERP_DATA: 'd_services.apis.external_methods.erp_data',
}


class ExternalMethodHandler:
    """
    معالج آمن للدوال الخارجية
    يستخدم لتنفيذ الدوال المحددة في قاعدة البيانات بطريقة آمنة
    """
    
    # تعبير نمطي للتحقق من صحة اسم الدالة
    VALID_FUNCTION_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
    
    # قائمة الدوال المحظورة
    FORBIDDEN_FUNCTIONS = {
        'eval', 'exec', 'compile', 'open', 'input', '__import__',
        'getattr', 'setattr', 'delattr', 'globals', 'locals',
        'vars', 'dir', 'type', 'isinstance', 'issubclass',
    }
    
    # قائمة الدوال المتجاهلة
    IGNORE_FUNCTIONS = [
        'Any', 'Dict', 'Optional', 'Tuple', 'List',
        'StudentLevel', 'StudentSemester', 'StudentSubject', 'StudentBatch',
        'PaymentStatusChoice', 'GrantStatusChoice', 'DiscountStatusChoice',
        'Sum', 'AcademicStatusChoice', 'StudentStatusChoice', 'GenderChoice',
        'logger', 'StudyTypeChoice', 'LevelStudentStatusChoice', 'Decimal',
        'MOCK_FINANCIAL_DATA_PATH',
    ]
    
    @classmethod
    def validate_function_name(cls, function_name: str) -> Tuple[bool, str]:
        """التحقق من صحة اسم الدالة"""
        if not function_name:
            return False, "اسم الدالة مطلوب"
        
        if not isinstance(function_name, str):
            return False, "اسم الدالة يجب أن يكون نصاً"
        
        function_name = function_name.strip()
        
        if not cls.VALID_FUNCTION_PATTERN.match(function_name):
            return False, f"اسم الدالة '{function_name}' يحتوي على أحرف غير مسموحة"
        
        if function_name.lower() in cls.FORBIDDEN_FUNCTIONS:
            logger.warning(f"محاولة استدعاء دالة محظورة: {function_name}")
            return False, f"الدالة '{function_name}' غير مسموح باستدعائها"
        
        if function_name.startswith('__'):
            return False, "لا يمكن استدعاء الدوال الخاصة"
        
        return True, ""
    
    @classmethod
    def _import_module(cls, module_path: str):
        """استيراد موديول بطريقة آمنة"""
        import importlib
        try:
            return importlib.import_module(module_path)
        except ImportError as e:
            logger.error(f"فشل استيراد الوحدة {module_path}: {e}")
            return None
    
    @classmethod
    def get_function(cls, function_name: str, function_type: FunctionType = None) -> Optional[Callable]:
        """
        جلب دالة من الملف المخصص لها
        
        Args:
            function_name: اسم الدالة
            function_type: نوع الدالة (يحدد الملف المخصص)
        """
        is_valid, error_message = cls.validate_function_name(function_name)
        if not is_valid:
            logger.warning(f"اسم دالة غير صالح: {function_name} - {error_message}")
            return None
        
        try:
            # إذا تم تحديد النوع، ابحث في الملف المخصص فقط
            if function_type:
                module_path = FUNCTION_TYPE_MODULES.get(function_type)
                if module_path:
                    module = cls._import_module(module_path)
                    if module and hasattr(module, function_name):
                        func = getattr(module, function_name)
                        if callable(func):
                            return func
                logger.warning(f"الدالة '{function_name}' غير موجودة في ملف {function_type.value}")
                return None
            
            # البحث في جميع الملفات (للتوافق العكسي)
            for f_type, module_path in FUNCTION_TYPE_MODULES.items():
                module = cls._import_module(module_path)
                if module and hasattr(module, function_name):
                    func = getattr(module, function_name)
                    if callable(func):
                        return func
            
            logger.warning(f"الدالة '{function_name}' غير موجودة في أي من الملفات المسموحة")
            return None
            
        except Exception as e:
            logger.error(f"خطأ في جلب الدالة '{function_name}': {e}")
            return None
    
    @classmethod
    def call_function(cls, function_name: str, *args, function_type: FunctionType = None, **kwargs) -> Tuple[bool, Any]:
        """
        استدعاء دالة بطريقة آمنة
        
        Args:
            function_name: اسم الدالة
            function_type: نوع الدالة (يحدد الملف المخصص)
            *args, **kwargs: المعاملات المراد تمريرها للدالة
        """
        func = cls.get_function(function_name, function_type)
        
        if func is None:
            return False, f"الدالة '{function_name}' غير متوفرة"
        
        try:
            logger.info(f"تنفيذ الدالة: {function_name} (نوع: {function_type.value if function_type else 'all'})")
            result = func(*args, **kwargs)
            logger.info(f"تم تنفيذ الدالة '{function_name}' بنجاح")
            return True, result
            
        except Exception as e:
            logger.error(f"خطأ في تنفيذ الدالة '{function_name}': {e}")
            return False, str(e)
    
    @classmethod
    def function_exists(cls, function_name: str, function_type: FunctionType = None) -> bool:
        """التحقق من وجود دالة"""
        return cls.get_function(function_name, function_type) is not None
    
    @classmethod
    def list_available_functions(cls, function_type: FunctionType = None) -> list:
        """
        قائمة الدوال المتاحة
        
        Args:
            function_type: نوع الدالة (اختياري) - إذا لم يتم تحديده يجلب الكل
        """
        functions = []
        
        try:
            modules_to_search = {}
            if function_type:
                module_path = FUNCTION_TYPE_MODULES.get(function_type)
                if module_path:
                    modules_to_search = {function_type: module_path}
            else:
                modules_to_search = FUNCTION_TYPE_MODULES
            
            for f_type, module_path in modules_to_search.items():
                module = cls._import_module(module_path)
                if module:
                    for name in dir(module):
                        if (not name.startswith('_') 
                            and callable(getattr(module, name))
                            and name not in cls.FORBIDDEN_FUNCTIONS
                            and name not in cls.IGNORE_FUNCTIONS
                            and name not in functions):
                            functions.append(name)
            
            return functions
        except Exception as e:
            logger.error(f"خطأ في جلب قائمة الدوال: {e}")
            return []
    
    @classmethod
    def get_functions_details(cls, function_type: FunctionType = None) -> list:
        """
        قائمة الدوال المتاحة مع تفاصيلها
        
        Args:
            function_type: نوع الدالة (اختياري) - إذا لم يتم تحديده يجلب الكل
        """
        functions = []
        seen_names = set()
        
        try:
            modules_to_search = {}
            if function_type:
                module_path = FUNCTION_TYPE_MODULES.get(function_type)
                if module_path:
                    modules_to_search = {function_type: module_path}
            else:
                modules_to_search = FUNCTION_TYPE_MODULES
            
            for f_type, module_path in modules_to_search.items():
                module = cls._import_module(module_path)
                if not module:
                    continue
                
                for name in dir(module):
                    if name.startswith('_') or name in cls.FORBIDDEN_FUNCTIONS:
                        continue
                    if name in cls.IGNORE_FUNCTIONS:
                        continue
                    if name in seen_names:
                        continue
                    if not name.startswith('call_'):
                        continue
                    
                    func = getattr(module, name)
                    if not callable(func):
                        continue
                    
                    seen_names.add(name)
                    functions.append({
                        'name': name,
                        'description': func.__doc__ or '',
                        'type': f_type.value,
                    })
            
            return functions
        except Exception as e:
            logger.error(f"خطأ في جلب تفاصيل الدوال: {e}")
            return []


# Django Validator for function names
def validate_function_name(value):
    """
    Django validator للتحقق من أن الدالة موجودة في القائمة المسموحة
    """
    from django.core.exceptions import ValidationError
    
    if not value:
        return
    
    available = ExternalMethodHandler.list_available_functions()
    if value not in available:
        raise ValidationError(
            f"الدالة '{value}' غير موجودة. الدوال المتاحة: {', '.join(available)}"
        )
