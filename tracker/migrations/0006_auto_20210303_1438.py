# Generated by Django 3.1.1 on 2021-03-03 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20210303_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
