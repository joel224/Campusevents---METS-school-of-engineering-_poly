# Generated by Django 5.1 on 2025-01-20 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0022_prize'),
    ]

    operations = [
        migrations.AddField(
            model_name='judgeregister',
            name='experience',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='judgeregister',
            name='qualification',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
