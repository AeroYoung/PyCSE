# Generated by Django 2.2.4 on 2019-08-09 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('civil', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='single_score',
            field=models.FloatField(default=1.0, verbose_name='分值'),
        ),
    ]
