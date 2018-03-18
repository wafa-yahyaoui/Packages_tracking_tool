# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-04 15:57
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=120, verbose_name='Status')),
                ('tracking_id', models.CharField(max_length=150, verbose_name='Tracking Id')),
                ('origin', models.CharField(blank=True, max_length=120, null=True, verbose_name='  place')),
                ('destination', models.CharField(blank=True, max_length=120, null=True, verbose_name='Destination place')),
                ('date_estimation', models.DateField(blank=True, null=True)),
                ('rate', models.IntegerField(blank=True, default=0, null=True, verbose_name='Rate')),
                ('note', models.TextField(blank=True, help_text='Add a note', null=True, verbose_name='Note')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date Created')),
                ('reason', models.TextField(blank=True, help_text='Add reason', null=True, verbose_name='Reason')),
                ('events_history', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('accept_test_flag', models.BooleanField(default=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Client')),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Courier')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='OrderCSV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_csv', models.FileField(error_messages={'required': 'Please enter a valid file!'}, upload_to='uploads/')),
            ],
            options={
                'verbose_name': 'Order CSV',
                'verbose_name_plural': 'Order CSV',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('sku', models.CharField(max_length=120, primary_key=True, serialize=False, unique=True, verbose_name='SKU')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('url', models.URLField(blank=True, null=True, verbose_name='URL')),
                ('url_image', models.URLField(blank=True, null=True, verbose_name='URL IMAGE')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='file_csv',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trackings.OrderCSV'),
        ),
        migrations.AddField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, related_name='orders', to='trackings.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='accounts.Store'),
        ),
    ]
