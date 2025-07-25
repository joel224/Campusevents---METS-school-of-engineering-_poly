# Generated by Django 5.1 on 2024-12-18 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0010_remove_eventsupdates_approved_eventsupdates_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsupdates',
            name='msg',
            field=models.CharField(default='None', max_length=45),
        ),
        migrations.AlterField(
            model_name='eventsupdates',
            name='status',
            field=models.CharField(choices=[('approved', 'APPROVED'), ('pending', 'PENDING'), ('rejected', 'REJECTED')], default='pending', max_length=12),
        ),
    ]
