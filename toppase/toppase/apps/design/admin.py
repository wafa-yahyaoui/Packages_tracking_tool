# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
#
# class MailAdmin(admin.ModelAdmin):
#     """This class represents the mail class in the admin's interface """
#     list_display = ('receiver', 'status', 'mass_mail')
#     list_filter = ('receiver', 'status', 'mass_mail')
#     search_fields = ('receiver', 'status', 'mass_mail')
#
#
# class MassMailAdmin(admin.ModelAdmin):
#     """This class represents the Mass mail class in the admin Interface"""
#     list_display = ('subject', 'sender', 'template_configured')
#     list_filter = ('subject', 'sender', 'template_configured')
#     search_fields = ('subject', 'sender')
#
#
# class ConfigEmailAdmin(admin.ModelAdmin):
#     """This class represents the templateConfigured
#     class in the admin Interface"""
#
#     list_display = ('template_Email', 'welcome_message', 'logo', 'owner', 'statusTemplateConf',)
#     list_filter = ('template_Email', 'welcome_message', 'logo', 'owner', 'statusTemplateConf',)
#     search_fields = ('template_Email', 'welcome_message', 'logo', 'owner', 'statusTemplateConf',)
#
#
# # Register your models here.
# admin.site.register(LandingPage)
# admin.site.register(Email)
# # admin.site.register(Template)

# admin.site.register(TemplateEmail)
# admin.site.register(StatusDelivery)
# admin.site.register(ContentEmail)
# admin.site.register(LandingPage)
admin.site.register(ContentEmail)




