# Generated by Django 4.1.3 on 2023-03-07 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_timesheet_db_check_out'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheet_db',
            name='check_out',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
