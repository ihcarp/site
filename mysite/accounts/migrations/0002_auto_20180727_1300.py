# Generated by Django 2.0.7 on 2018-07-27 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='favs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favs', to='trainings.Post'),
        ),
    ]
