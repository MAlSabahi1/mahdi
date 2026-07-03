# Generated migration for ForceType model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_add_head_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='اسم التصنيف')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='الكود')),
                ('category', models.CharField(
                    choices=[
                        ('basic', 'أساسي'),
                        ('committee', 'لجان'),
                        ('newcomer', 'مستجدين')
                    ],
                    max_length=20,
                    verbose_name='الفئة'
                )),
                ('rank_type', models.CharField(
                    choices=[
                        ('officer', 'ضباط'),
                        ('personnel', 'أفراد'),
                        ('both', 'كلاهما')
                    ],
                    max_length=20,
                    verbose_name='نوع الرتبة'
                )),
                ('is_outside_payroll', models.BooleanField(default=False, verbose_name='خارج الصرف')),
                ('description', models.TextField(blank=True, verbose_name='الوصف')),
                ('order', models.IntegerField(default=0, verbose_name='الترتيب')),
            ],
            options={
                'verbose_name': 'تصنيف القوة',
                'verbose_name_plural': 'تصنيفات القوة',
                'db_table': 'core_force_type',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.AddIndex(
            model_name='forcetype',
            index=models.Index(fields=['category'], name='core_force__categor_idx'),
        ),
        migrations.AddIndex(
            model_name='forcetype',
            index=models.Index(fields=['rank_type'], name='core_force__rank_ty_idx'),
        ),
    ]
