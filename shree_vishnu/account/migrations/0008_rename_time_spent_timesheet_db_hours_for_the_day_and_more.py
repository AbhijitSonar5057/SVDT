# Generated by Django 4.1.7 on 2023-03-09 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_timesheet_db_check_out'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timesheet_db',
            old_name='time_spent',
            new_name='hours_for_the_day',
        ),
        migrations.AddField(
            model_name='timesheet_db',
            name='check_in_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timesheet_db',
            name='check_out_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='timesheet_db',
            name='check_in',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='timesheet_db',
            name='check_out',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='timesheet_db',
            name='emp_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='timesheet_db',
            name='parts_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.parts_db'),
        ),
        migrations.AlterField(
            model_name='timesheet_db',
            name='projet_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.project_db'),
        ),
        migrations.AlterField(
            model_name='timesheet_db',
            name='task_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.task_db'),
        ),
    ]
