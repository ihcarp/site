# Generated by Django 2.0.7 on 2018-07-21 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0005_auto_20180721_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='no text', max_length=200),
            preserve_default=False,
        ),
    ]
