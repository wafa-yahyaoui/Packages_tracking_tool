# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from oauth2_provider.admin import get_access_token_model, get_grant_model, get_application_model, get_refresh_token_model

from .forms import UserChangeForm, UserCreationForm
from .models import Member, Courier, Store, StatusDelivery, Client, LandingPage, Advert, Link


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone',)}),
        ('Permissions', {'fields': ('is_staff',)}),
        ('OAUTH TOKEN', {'fields': ('client_id', 'client_secret')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'client_id', 'client_secret')}
        ),

    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
#admin.site.unregister(Member)

admin.site.register(Courier)
admin.site.register(Store)
admin.site.register(Client)
admin.site.register(StatusDelivery)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
#admin.site.unregister(AbstractApplication)


Application = get_application_model()
Grant = get_grant_model()
AccessToken = get_access_token_model()
RefreshToken = get_refresh_token_model()

admin.site.unregister(Grant)
admin.site.unregister(Application)
admin.site.unregister(AccessToken)
admin.site.unregister(RefreshToken)
admin.site.register(Member, UserAdmin)



admin.site.register(Advert)
admin.site.register(Link)

