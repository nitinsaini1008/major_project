# Generated by Django 4.0.5 on 2022-07-08 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro', '0005_alter_items_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='allorder',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
