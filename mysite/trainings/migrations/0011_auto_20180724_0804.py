# Generated by Django 2.0.7 on 2018-07-24 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0010_auto_20180724_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
