# Generated by Django 4.1.7 on 2023-05-04 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapp', '0006_alter_ssid_options_ssid_is_connected'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ssid',
            options={'ordering': ['-is_connected', '-max_signal']},
        ),
    ]
