# Generated migration for Position model and Department enhancements

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_database_constraints'),
    ]

    operations = [
        # Add level field to Department
        migrations.AddField(
            model_name='department',
            name='level',
            field=models.IntegerField(
                choices=[(1, 'إدارة رئيسية'), (2, 'فرع'), (3, 'قسم')],
                default=1,
                verbose_name='المستوى'
            ),
        ),
        
        # Add description field to JobTitle
        migrations.AddField(
            model_name='jobtitle',
            name='description',
            field=models.TextField(blank=True, verbose_name='الوصف'),
        ),
        
        # Remove unique constraint from Department.name
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=200, verbose_name='اسم الإدارة'),
        ),
        
        # Add unique_together constraint
        migrations.AlterUniqueTogether(
            name='department',
            unique_together={('name', 'parent')},
        ),
        
        # Add index for level
        migrations.AddIndex(
            model_name='department',
            index=models.Index(fields=['level'], name='core_depart_level_idx'),
        ),
        
        # Create Position model
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='المنصب')),
                ('level', models.IntegerField(help_text='1=أعلى مستوى (وزير)، 10=أدنى مستوى', verbose_name='المستوى الإداري')),
                ('requires_rank', models.ForeignKey(
                    blank=True,
                    help_text='الحد الأدنى من الرتبة المطلوبة لهذا المنصب',
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='positions',
                    to='core.rank',
                    verbose_name='الرتبة المطلوبة'
                )),
            ],
            options={
                'verbose_name': 'منصب',
                'verbose_name_plural': 'المناصب',
                'db_table': 'core_position',
                'ordering': ['level', 'name'],
            },
        ),
        
        # Add index for Position.level
        migrations.AddIndex(
            model_name='position',
            index=models.Index(fields=['level'], name='core_positi_level_idx'),
        ),
    ]
