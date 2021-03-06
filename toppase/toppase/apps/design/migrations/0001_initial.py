# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-04 15:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('abstract', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_body', models.TextField(blank=True, default='default text body', max_length=500, null=True, verbose_name='text body')),
                ('text_footer', models.TextField(blank=True, default='default text footer', max_length=500, null=True, verbose_name='text footer')),
                ('status_delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.StatusDelivery', verbose_name='The Email Status')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Store', verbose_name='Configured Email')),
                ('template_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='template_email', to='abstract.TemplateEmail', verbose_name='Choose a Template')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='contentemail',
            unique_together=set([('status_delivery', 'store', 'template_email')]),
        ),
    ]
