"""
User Model — هوية المستخدم الأساسية
═════════════════════════════════════
Custom User يرث من AbstractUser.
مسؤول فقط عن: الهوية الأساسية للمستخدم.
لا يحتوي على: صلاحيات، جلسات، أمان، بيانات موظفين.
"""
import uuid
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    نموذج المستخدم المخصص — خفيف وواضح.

    الحقول الموروثة من AbstractUser:
        username, password, is_active, is_staff, is_superuser,
        first_name, last_name, email, last_login, date_joined

    الحقول المضافة:
        phone, full_name, created_at, updated_at
    """


    full_name = models.CharField(
        max_length=300,
        blank=True,
        default='',
        verbose_name=_('الاسم الكامل'),
        help_text=_('الاسم الرباعي أو الكامل للمستخدم'),
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name=_('رقم الهاتف'),
    )
    email = models.EmailField(
        blank=True,
        default='',
        verbose_name=_('البريد الإلكتروني'),
    )

    # ── Profile Fields ──
    profile_picture = models.ImageField(
        upload_to='users/profiles/',
        blank=True,
        null=True,
        verbose_name=_('الصورة الشخصية'),
    )
    bio = models.TextField(
        blank=True,
        default='',
        verbose_name=_('النبذة التعريفية'),
    )
    facebook_link = models.URLField(
        blank=True,
        default='',
        verbose_name=_('رابط فيسبوك'),
    )
    x_link = models.URLField(
        blank=True,
        default='',
        verbose_name=_('رابط إكس'),
    )
    linkedin_link = models.URLField(
        blank=True,
        default='',
        verbose_name=_('رابط لينكد إن'),
    )
    instagram_link = models.URLField(
        blank=True,
        default='',
        verbose_name=_('رابط إنستجرام'),
    )

    # ── Timestamps ──
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التحديث'),
    )

    class Meta:
        db_table = 'accounts_user'
        verbose_name = _('مستخدم')
        verbose_name_plural = _('المستخدمون')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self) -> str:
        return self.full_name or self.get_full_name() or self.username

    def get_display_name(self) -> str:
        """الاسم المعروض — يعطي الأولوية لـ full_name."""
        if self.full_name:
            return self.full_name
        django_full = self.get_full_name()
        if django_full:
            return django_full
        return self.username

    def get_short_name(self) -> str:
        """الاسم المختصر للعرض السريع."""
        if self.full_name:
            parts = self.full_name.split()
            return parts[0] if parts else self.username
        return self.first_name or self.username

    @property
    def is_profile_complete(self) -> bool:
        """هل أكمل المستخدم بياناته الأساسية."""
        return bool(self.full_name and self.username)

    def save(self, *args, **kwargs) -> None:
        """مزامنة full_name مع first_name/last_name إذا لم يكن محدداً."""
        if not self.full_name and (self.first_name or self.last_name):
            self.full_name = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)
