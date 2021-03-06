# Generated by Django 3.1.5 on 2021-02-26 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EventGeneration', '0009_auto_20210226_1333'),
        ('ProjectAllocation', '0008_auto_20210226_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide_pref',
            name='guide_1',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='guide_1', to='EventGeneration.faculty'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guide_pref',
            name='guide_2',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='guide_2', to='EventGeneration.faculty'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guide_pref',
            name='guide_3',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='guide_3', to='EventGeneration.faculty'),
            preserve_default=False,
        ),
    ]
