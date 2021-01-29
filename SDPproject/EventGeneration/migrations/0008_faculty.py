# Generated by Django 3.1.5 on 2021-01-28 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EventGeneration', '0007_auto_20210126_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='EventGeneration.user')),
                ('designation', models.TextField(max_length=50)),
                ('available', models.BooleanField(default=True)),
            ],
        ),
    ]