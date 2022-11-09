# Generated by Django 4.1.1 on 2022-11-07 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('agent_ID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('firm', models.CharField(default='None', max_length=50)),
                ('username', models.CharField(default='None', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Bond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issuer', models.CharField(default='None', max_length=50)),
                ('maturity', models.DateField()),
                ('grade', models.IntegerField(choices=[(10, 'AAA'), (9, 'AA'), (8, 'A'), (7, 'BBB'), (6, 'BB'), (5, 'B'), (4, 'CCC'), (3, 'CC'), (2, 'C'), (0, 'D')], default=0)),
                ('value', models.FloatField(default=0.0)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.agent')),
            ],
        ),
        migrations.CreateModel(
            name='DepositOrWithdrawl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Deposit'), (-1, 'Withdraw')], default=1)),
                ('amount', models.FloatField(default=0)),
                ('fulfilled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('file', models.FileField(upload_to='')),
                ('description', models.TextField()),
                ('media_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(default='None', max_length=300)),
                ('value', models.FloatField(default=0.0)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.agent')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(default='NONE', max_length=5)),
                ('value', models.FloatField(default=0.0)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.agent')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(default='None', max_length=300)),
                ('age', models.IntegerField(default=0)),
                ('sex', models.CharField(default='None', max_length=300)),
                ('occupation', models.CharField(default='None', max_length=300)),
                ('balance', models.FloatField(default=0)),
                ('gain', models.FloatField(default=0)),
                ('user_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StockTransaction',
            fields=[
                ('transaction_type', models.IntegerField(choices=[(1, 'Buy'), (-1, 'Sell')], default=1)),
                ('transaction_ID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('volume', models.IntegerField(default=0)),
                ('transaction_date', models.DateField(auto_now=True)),
                ('Stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.stock')),
                ('user_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StockState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0)),
                ('open', models.FloatField(default=0)),
                ('close', models.FloatField(default=0)),
                ('high', models.FloatField(default=0)),
                ('volume', models.FloatField(default=0)),
                ('date', models.DateField(auto_now=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.stock')),
            ],
        ),
        migrations.CreateModel(
            name='StockOwnership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.stock')),
                ('user_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyTransaction',
            fields=[
                ('transaction_type', models.IntegerField(choices=[(1, 'Buy'), (-1, 'Sell')], default=1)),
                ('transaction_ID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('volume', models.IntegerField(default=0)),
                ('transaction_date', models.DateField(auto_now=True)),
                ('Property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.property')),
                ('user_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('value', models.FloatField(default=0)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.property')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyOwnership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.property')),
                ('user_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NewIndicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newPost', models.BooleanField(default=False)),
                ('user_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='forum',
            fields=[
                ('views', models.IntegerField(default=0, editable=False)),
                ('topic', models.CharField(default='Untitled', max_length=300)),
                ('description', models.CharField(default='', max_length=1000)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('user_ID', models.ForeignKey(default='Anonymous', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('comment', models.CharField(max_length=500)),
                ('disc_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.forum')),
                ('user_ID', models.ForeignKey(default='Anonymous', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BondTransaction',
            fields=[
                ('transaction_type', models.IntegerField(choices=[(1, 'Buy'), (-1, 'Sell')], default=1)),
                ('transaction_ID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('transaction_date', models.DateField(auto_now=True)),
                ('volume', models.IntegerField(default=0)),
                ('Bond', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.bond')),
                ('user_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BondState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('value', models.FloatField(default=0)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.bond')),
            ],
        ),
        migrations.CreateModel(
            name='BondOwnership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Discussion_forum.bond')),
                ('user_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]