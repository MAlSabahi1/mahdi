# Generated migration for adding head field to organizational structure

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_directorate_governorate_division_and_more'),
        ('personnel', '0005_suggestedcorrection_governorate'),
    ]

    operations = [
        migrations.AddField(
            model_name='governorate',
            name='head',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='governed_governorate',
                to='personnel.personnelmaster',
                verbose_name='المدير'
            ),
        ),
        migrations.AddField(
            model_name='directorate',
            name='head',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='governed_directorate',
                to='personnel.personnelmaster',
                verbose_name='المدير'
            ),
        ),
        migrations.AddField(
            model_name='division',
            name='head',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='governed_division',
                to='personnel.personnelmaster',
                verbose_name='رئيس القسم'
            ),
        ),
        migrations.AddField(
            model_name='unit',
            name='head',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='governed_unit',
                to='personnel.personnelmaster',
                verbose_name='رئيس الوحدة'
            ),
        ),
    ]
