# Generated by Django 4.1.7 on 2023-03-05 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapp', '0005_alter_ssid_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ssid',
            options={'ordering': ['is_connected', '-max_signal']},
        ),
        migrations.AddField(
            model_name='ssid',
            name='is_connected',
            field=models.BooleanField(null=True),
        ),
    ]