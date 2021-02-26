# Generated by Django 3.1.5 on 2021-02-26 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EventGeneration', '0009_auto_20210226_1333'),
        ('ProjectAllocation', '0006_allocated_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocated_project',
            name='event_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='EventGeneration.event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EventGeneration.student'),
        ),
        migrations.AddField(
            model_name='team',
            name='event',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='EventGeneration.event'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Guide_Pref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProjectAllocation.project')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EventGeneration.student')),
            ],
        ),
    ]
