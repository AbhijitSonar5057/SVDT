# Generated by Django 4.1.7 on 2023-03-09 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_rename_time_spent_timesheet_db_hours_for_the_day_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_db',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
