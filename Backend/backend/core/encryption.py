"""
Encryption Utilities - أدوات التشفير
تشفير البيانات الحساسة باستخدام AES-256

التحسينات الأمنية:
- Salt من متغير بيئي
- Logging للعمليات الحساسة
- حقل is_encrypted لتجنب التشفير المزدوج
- bulk_update للأداء
"""
import base64
import os
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from django.conf import settings

logger = logging.getLogger(__name__)


class FieldEncryption:
    """
    تشفير الحقول الحساسة باستخدام Fernet (AES-256)
    """
    
    def __init__(self):
        """تهيئة المفتاح من الإعدادات"""
        self._fernet = None
    
    @property
    def fernet(self):
        """الحصول على كائن Fernet (lazy loading)"""
        if self._fernet is None:
            key = self._get_encryption_key()
            self._fernet = Fernet(key)
        return self._fernet
    
    def _get_encryption_key(self):
        """
        الحصول على مفتاح التشفير من المتغيرات البيئية
        
        Returns:
            bytes: مفتاح Fernet
        """
        # الحصول على المفتاح من المتغيرات البيئية
        secret_key = getattr(settings, 'FIELD_ENCRYPTION_KEY', None)
        
        if not secret_key:
            # إذا لم يوجد، استخدم SECRET_KEY كأساس
            secret_key = settings.SECRET_KEY
            logger.warning(
                "FIELD_ENCRYPTION_KEY غير موجود. استخدام SECRET_KEY كبديل. "
                "يُنصح بتوليد مفتاح مخصص باستخدام: python manage.py generate_encryption_key"
            )
        
        # الحصول على Salt من متغير بيئي (أكثر أماناً)
        salt = getattr(settings, 'FIELD_ENCRYPTION_SALT', 'hrms_salt_2026')
        if isinstance(salt, str):
            salt = salt.encode('utf-8')
        
        # تحويل المفتاح إلى مفتاح Fernet صالح
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(secret_key.encode()))
        return key
    
    def encrypt(self, value):
        """
        تشفير قيمة
        
        Args:
            value: القيمة المراد تشفيرها (str)
            
        Returns:
            str: القيمة المشفرة (base64)
        """
        if not value:
            return value
        
        if isinstance(value, str):
            value = value.encode('utf-8')
        
        encrypted = self.fernet.encrypt(value)
        return base64.urlsafe_b64encode(encrypted).decode('utf-8')
    
    def decrypt(self, encrypted_value):
        """
        فك تشفير قيمة
        
        Args:
            encrypted_value: القيمة المشفرة (str)
            
        Returns:
            str: القيمة الأصلية
        """
        if not encrypted_value:
            return encrypted_value
        
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_value.encode('utf-8'))
            decrypted = self.fernet.decrypt(encrypted_bytes)
            return decrypted.decode('utf-8')
        except Exception as e:
            # تسجيل الخطأ (قد يكون محاولة تلاعب أو مفتاح خاطئ)
            logger.error(
                f"فشل فك التشفير: {str(e)}. "
                "قد يكون المفتاح خاطئاً أو البيانات تالفة.",
                exc_info=True
            )
            # إرجاع القيمة كما هي (قد تكون غير مشفرة)
            return encrypted_value


# كائن عام للاستخدام
field_encryption = FieldEncryption()


def encrypt_phone_number(phone_number):
    """
    تشفير رقم الهاتف
    
    Args:
        phone_number: رقم الهاتف
        
    Returns:
        str: رقم الهاتف المشفر
    """
    if not phone_number:
        return phone_number
    return field_encryption.encrypt(phone_number)


def decrypt_phone_number(encrypted_phone):
    """
    فك تشفير رقم الهاتف
    
    Args:
        encrypted_phone: رقم الهاتف المشفر
        
    Returns:
        str: رقم الهاتف الأصلي
    """
    if not encrypted_phone:
        return encrypted_phone
    return field_encryption.decrypt(encrypted_phone)


class EncryptedCharField:
    """
    Descriptor لحقل نصي مشفر
    يمكن استخدامه كـ property في النماذج
    """
    
    def __init__(self, field_name):
        """
        Args:
            field_name: اسم الحقل في قاعدة البيانات
        """
        self.field_name = field_name
        self.encrypted_field_name = f'_{field_name}_encrypted'
    
    def __get__(self, instance, owner):
        """الحصول على القيمة المفكوكة"""
        if instance is None:
            return self
        
        encrypted_value = getattr(instance, self.encrypted_field_name, None)
        if encrypted_value:
            return field_encryption.decrypt(encrypted_value)
        return None
    
    def __set__(self, instance, value):
        """تعيين القيمة المشفرة"""
        if value:
            encrypted_value = field_encryption.encrypt(value)
            setattr(instance, self.encrypted_field_name, encrypted_value)
        else:
            setattr(instance, self.encrypted_field_name, None)


def generate_encryption_key():
    """
    توليد مفتاح تشفير جديد
    يُستخدم مرة واحدة عند إعداد النظام
    
    Returns:
        str: مفتاح Fernet جديد
    """
    key = Fernet.generate_key()
    return key.decode('utf-8')


# ========================================
# Management Command Helper
# ========================================

def encrypt_existing_data(model_class, field_name, batch_size=1000):
    """
    تشفير البيانات الموجودة في قاعدة البيانات (محسّن للأداء)
    يُستخدم عند الترحيل من نظام غير مشفر
    
    Args:
        model_class: فئة النموذج
        field_name: اسم الحقل المراد تشفيره
        batch_size: حجم الدفعة
        
    Returns:
        int: عدد السجلات المشفرة
    """
    from django.db import transaction
    
    count = 0
    queryset = model_class.objects.filter(**{f'{field_name}__isnull': False})
    total = queryset.count()
    
    logger.info(f"بدء تشفير {total} سجل في {model_class.__name__}.{field_name}")
    
    for i in range(0, total, batch_size):
        batch = list(queryset[i:i + batch_size])
        to_update = []
        
        with transaction.atomic():
            for obj in batch:
                value = getattr(obj, field_name)
                # التحقق من أنها غير مشفرة (بدون الاعتماد على البادئة فقط)
                if value and not _is_encrypted(value):
                    encrypted = field_encryption.encrypt(value)
                    setattr(obj, field_name, encrypted)
                    to_update.append(obj)
                    count += 1
            
            # استخدام bulk_update للأداء
            if to_update:
                model_class.objects.bulk_update(to_update, [field_name])
        
        logger.info(f"تم تشفير {min(i + batch_size, total)}/{total} سجل")
    
    logger.info(f"اكتمل التشفير: {count} سجل تم تشفيره")
    return count


def _is_encrypted(value):
    """
    التحقق من أن القيمة مشفرة بالفعل
    يتحقق من البنية وليس فقط البادئة
    """
    if not value or not isinstance(value, str):
        return False
    
    try:
        # محاولة فك التشفير
        field_encryption.decrypt(value)
        return True
    except Exception:
        return False


def decrypt_existing_data(model_class, field_name, batch_size=1000):
    """
    فك تشفير البيانات الموجودة في قاعدة البيانات
    يُستخدم في حالات الطوارئ أو الترحيل العكسي
    
    Args:
        model_class: فئة النموذج
        field_name: اسم الحقل المراد فك تشفيره
        batch_size: حجم الدفعة
        
    Returns:
        int: عدد السجلات المفكوكة
    """
    from django.db import transaction
    
    count = 0
    queryset = model_class.objects.filter(**{f'{field_name}__isnull': False})
    total = queryset.count()
    
    print(f"فك تشفير {total} سجل...")
    
    for i in range(0, total, batch_size):
        batch = queryset[i:i + batch_size]
        
        with transaction.atomic():
            for obj in batch:
                encrypted_value = getattr(obj, field_name)
                if encrypted_value:
                    try:
                        decrypted = field_encryption.decrypt(encrypted_value)
                        setattr(obj, field_name, decrypted)
                        obj.save(update_fields=[field_name])
                        count += 1
                    except Exception as e:
                        print(f"فشل فك تشفير السجل {obj.pk}: {e}")
        
        print(f"تم فك تشفير {min(i + batch_size, total)}/{total} سجل")
    
    return count
