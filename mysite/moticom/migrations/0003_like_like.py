# Generated by Django 3.2.8 on 2021-11-24 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moticom', '0002_alter_report_cm_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='like',
            field=models.IntegerField(default=0, verbose_name='Like'),
        ),
    ]
