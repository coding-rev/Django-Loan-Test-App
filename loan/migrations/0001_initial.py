# Generated by Django 4.1.5 on 2023-01-28 09:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='Euro', max_length=50, unique=True)),
                ('symbol', models.CharField(max_length=5, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('signature_date', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('signed_amount', models.FloatField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='loan_country', to='loan.country')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='loan_currency', to='loan.currency')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='loan_sector', to='loan.sector')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
