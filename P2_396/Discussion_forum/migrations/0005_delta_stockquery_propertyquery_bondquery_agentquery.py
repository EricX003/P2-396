# Generated by Django 4.1.1 on 2022-11-09 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Discussion_forum', '0004_remove_bondownership_value_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='delta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('gl', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='StockQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.stock')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.property')),
            ],
        ),
        migrations.CreateModel(
            name='BondQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bond', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.bond')),
            ],
        ),
        migrations.CreateModel(
            name='AgentQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.agent')),
            ],
        ),
    ]