# Generated by Django 3.1.5 on 2021-07-17 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stick_protocol', '0010_auto_20210711_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encryptionsenderkey',
            name='chainId',
            field=models.IntegerField(default=0),
        ),
    ]
