# Generated by Django 2.0.7 on 2018-07-30 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0017_auto_20180730_0627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pdf_file',
            field=models.FileField(blank=True, upload_to='uploads/'),
        ),
    ]
