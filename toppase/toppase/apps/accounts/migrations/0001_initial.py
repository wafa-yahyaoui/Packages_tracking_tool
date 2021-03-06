# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-04 15:57
from __future__ import unicode_literals

import apps.accounts.managers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import oauth2_provider.generators
import oauth2_provider.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('abstract', '0001_initial'),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('client_id', models.CharField(db_index=True, default=oauth2_provider.generators.generate_client_id, max_length=100, unique=True)),
                ('redirect_uris', models.TextField(blank=True, help_text='Allowed URIs list, space separated', validators=[oauth2_provider.validators.validate_uris])),
                ('client_type', models.CharField(choices=[('confidential', 'Confidential'), ('public', 'Public')], max_length=32)),
                ('authorization_grant_type', models.CharField(choices=[('authorization-code', 'Authorization code'), ('implicit', 'Implicit'), ('password', 'Resource owner password-based'), ('client-credentials', 'Client credentials')], max_length=32)),
                ('client_secret', models.CharField(blank=True, db_index=True, default=oauth2_provider.generators.generate_client_secret, max_length=255)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('skip_authorization', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('news_letter', models.BooleanField(default=True, help_text='Get updates on new features activated to your account.', verbose_name='News Letter')),
                ('via_email', models.BooleanField(default=True, help_text='Receive notifications when status order change, check bellow', verbose_name='E-mail Notification')),
                ('platform', models.BooleanField(default=True, help_text='Get notification when changes happen in your account', verbose_name='System notification')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('phone', models.CharField(blank=True, help_text='Enter your phone', max_length=20, null=True, unique=True, verbose_name='Phone number')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email address')),
                ('username', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'French'), ('gr', 'Germany'), ('es', 'Spain')], default='en', help_text='Choose your preferred language', max_length=50, verbose_name='Language')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', apps.accounts.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(verbose_name='Link')),
                ('image', models.ImageField(upload_to=b'', verbose_name='Image')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('address_line', models.CharField(blank=True, max_length=200, null=True, verbose_name='Street Address')),
                ('zip_code', models.CharField(blank=True, max_length=60, null=True, verbose_name='Zip code')),
                ('city', models.CharField(blank=True, max_length=60, null=True, verbose_name='City')),
                ('country', models.CharField(blank=True, default='France', max_length=100, null=True, verbose_name='Country')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('phone', models.CharField(blank=True, help_text='Enter your phone', max_length=20, null=True, unique=True, verbose_name='Phone number')),
                ('email', models.EmailField(max_length=255, primary_key=True, serialize=False, unique=True, verbose_name='Email address')),
                ('ip_address', models.CharField(blank=True, max_length=180, null=True, verbose_name='Ip Address')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('text', models.CharField(max_length=200, verbose_name='Text Courier')),
                ('code', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True, verbose_name='Code Courier')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200, verbose_name='Text')),
                ('url', models.URLField(verbose_name='URL')),
            ],
        ),
        migrations.CreateModel(
            name='StatusDelivery',
            fields=[
                ('name', models.CharField(choices=[('IT', 'In Transit'), ('DL', 'Delivered'), ('OFD', 'Out for delivery'), ('RTG', 'Ready togo'), ('FA', 'Failed attempt')], max_length=15, unique=True)),
                ('code', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(choices=[('shopify', 'Shopify'), ('prestashop', 'PrestaShop'), ('woocommerce', 'WooCommerce'), ('opencard', 'OpenCard'), ('magento', 'Magento')], max_length=20, verbose_name='Provider')),
                ('address_line', models.CharField(blank=True, max_length=200, null=True, verbose_name='Street Address')),
                ('zip_code', models.CharField(blank=True, max_length=60, null=True, verbose_name='Zip code')),
                ('city', models.CharField(blank=True, max_length=60, null=True, verbose_name='City')),
                ('country', models.CharField(blank=True, default='France', max_length=100, null=True, verbose_name='Country')),
                ('font', models.CharField(choices=[('AR', 'Arial'), ('ARB', 'Arial Black'), ('CN', 'Courier New')], default='AR', max_length=20, verbose_name='Font')),
                ('color_menu', models.CharField(default='#ffffff', max_length=7, verbose_name='Color menu')),
                ('color_call_to_action', models.CharField(default='#ffffff', max_length=7, verbose_name='Color call to action')),
                ('allignment', models.CharField(choices=[('center', 'center'), ('left', 'left'), ('right', 'right')], default='center', max_length=20, verbose_name='Alignment')),
                ('size', models.CharField(choices=[('8', '8'), ('10', '10'), ('12', '12'), ('14', '14'), ('16', '16'), ('18', '18'), ('20', '20'), ('24', '24')], max_length=3, verbose_name='Size')),
                ('l_font', models.CharField(choices=[('AR', 'Arial'), ('ARB', 'Arial Black'), ('CN', 'Courier New')], default='AR', max_length=20, verbose_name='Landing page Font')),
                ('l_color_menu', models.CharField(default='#00ff00', max_length=7, verbose_name='Landing page  Color menu')),
                ('l_color_call_to_action', models.CharField(default='#ff0000', max_length=7, verbose_name='Landing page  Color call to action')),
                ('l_allignment', models.CharField(choices=[('center', 'center'), ('left', 'left'), ('right', 'right')], default='center', max_length=20, verbose_name='Landing page Alignment')),
                ('l_size', models.CharField(choices=[('8', '8'), ('10', '10'), ('12', '12'), ('14', '14'), ('16', '16'), ('18', '18'), ('20', '20'), ('24', '24')], default='12', max_length=3, verbose_name='Landing page  Size')),
                ('l_background_image', models.ImageField(upload_to=b'', verbose_name='Landing page  Background image')),
                ('l_help_url', models.URLField(verbose_name='Landing page  HELP URL')),
                ('color_text', models.CharField(default='#ffffff', max_length=7, verbose_name='Color menu')),
                ('company_name', models.CharField(max_length=200, verbose_name='Company Name')),
                ('name', models.CharField(max_length=200, verbose_name='Store Name')),
                ('url', models.URLField(verbose_name='Store URL')),
                ('tracking_url', models.URLField(verbose_name='Tracking URL')),
                ('logo', models.ImageField(help_text="We recommend using a logo that's at most 150px tall.", upload_to=b'', verbose_name='Logo')),
                ('category', models.CharField(choices=[('fa', 'Fashion'), ('jw', 'Jewelery'), ('ga', 'Games')], max_length=150, verbose_name='Category')),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'French'), ('gr', 'Germany'), ('es', 'Spain')], default='en', help_text='Choose your preferred language', max_length=50, verbose_name='Language')),
                ('advert', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Advert', verbose_name='Landing page  Advert')),
                ('couriers', models.ManyToManyField(to='accounts.Courier')),
                ('landing_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abstract.LandingPage', verbose_name='Landing page')),
                ('members', models.ManyToManyField(related_name='stores', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='link',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='accounts.Store'),
        ),
        migrations.AddField(
            model_name='member',
            name='status_deliveries',
            field=models.ManyToManyField(to='accounts.StatusDelivery'),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accounts_member', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='member',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
