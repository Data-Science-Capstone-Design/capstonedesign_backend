# Generated by Django 4.1.2 on 2022-12-07 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_remove_excel_data_main_main_excel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excel_data',
            name='birth',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
