# Generated by Django 3.1.5 on 2021-01-29 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectAllocation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='highest_cpi',
            field=models.CharField(default=1, max_length=4),
            preserve_default=False,
        ),
    ]
