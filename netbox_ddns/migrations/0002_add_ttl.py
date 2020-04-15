# Generated by Django 3.0.5 on 2020-04-14 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_ddns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reversezone',
            name='ttl',
            field=models.PositiveIntegerField(default=3600),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zone',
            name='ttl',
            field=models.PositiveIntegerField(default=3600),
            preserve_default=False,
        ),
    ]