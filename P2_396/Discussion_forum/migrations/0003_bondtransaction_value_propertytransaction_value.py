# Generated by Django 4.1.1 on 2022-11-09 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Discussion_forum', '0002_bondownership_value_propertyownership_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bondtransaction',
            name='value',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='propertytransaction',
            name='value',
            field=models.FloatField(default=0.0),
        ),
    ]
