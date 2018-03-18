# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import forms as auth_forms
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import Member, Store


class LandingPageForm(forms.ModelForm):
    """This class represents landing page form"""

    class Meta:
        model = Store
        fields = ['l_allignment', 'l_background_image', 'l_color_call_to_action', 'l_color_menu', 'l_font',
                  'l_help_url', 'l_size']
        widgets = {
            'l_allignment': forms.Select(attrs={'class': 'form-control'}),
            'l_background_image': forms.FileInput(attrs={'id': 'background_image_file', 'class': 'custom-file-input'}),
            'l_color_menu': forms.TextInput(attrs={'class': 'form-control'}),
            'l_color_call_to_action': forms.TextInput(attrs={'class': 'form-control'}),
            'l_font': forms.Select(attrs={'class': 'form-control'}),
            'l_help_url': forms.URLInput(attrs={'class': 'form-control'}),
            'l_size': forms.Select(attrs={'class': 'form-control'}),
        }


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email', 'client_id', 'client_secret')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = auth_forms.ReadOnlyPasswordHashField()

    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email', 'password', 'phone',
                  'language', 'is_active', 'is_staff', 'client_id', 'client_secret')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyProfileForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email', 'phone', 'language')

    def __init__(self, *args, **kwargs):
        super(MyProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['language'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].label = "First Name:"
        self.fields['last_name'].label = "Last Name:"
        self.fields['email'].label = "Email:"
        self.fields['phone'].label = "Phone:"
        self.fields['language'].label = "Language:"

    def clean_email(self):
        """
        Ensure the email address is not already registered.
        """
        email = self.cleaned_data.get("email")
        if email is None:
            raise forms.ValidationError(_("This field is required"))
        if email == self.instance.email:
            return email
        qs = Member.objects.filter(email=email)
        if len(qs) == 0:
            return email
        raise forms.ValidationError(_("This email address is already exist"))


class MemberNotificationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('news_letter', 'via_email', 'status_deliveries', 'platform')

    def __init__(self, *args, **kwargs):
        super(MemberNotificationForm, self).__init__(*args, **kwargs)
        self.fields['news_letter'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['via_email'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['status_deliveries'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['platform'].widget.attrs.update({'class': 'form-check-input'})
        # self.fields['first_name'].label = "First Name:"
        # self.fields['last_name'].label = "Last Name:"
        # self.fields['email'].label = "Email:"
        # self.fields['phone'].label = "Phone:"
        # self.fields['language'].label = "Language:"


class MemberStoreSettingsStoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ('company_name',
                  'url',
                  'category',
                  'tracking_url',
                  'language',
                  'zip_code',
                  'city',
                  'country',
                  'address_line')

    def __init__(self, *args, **kwargs):
        super(MemberStoreSettingsStoreForm, self).__init__(*args, **kwargs)
        self.fields['company_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['url'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['tracking_url'].widget.attrs.update({'class': 'form-control'})
        self.fields['language'].widget.attrs.update({'class': 'form-control'})
        self.fields['zip_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control'})
        self.fields['country'].widget.attrs.update({'class': 'form-control'})
        self.fields['address_line'].widget.attrs.update({'class': 'form-control'})


class MemberStoreSettingsDesignForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ('font', 'color_menu', 'logo', 'color_text')

    def __init__(self, *args, **kwargs):
        super(MemberStoreSettingsDesignForm, self).__init__(*args, **kwargs)
        self.fields['font'].widget.attrs.update({'class': 'form-control'})
        self.fields['color_menu'].widget.attrs.update({'class': 'form-control'})
        self.fields['color_text'].widget.attrs.update({'class': 'form-control'})
        self.fields['logo'].widget.attrs.update({'class': 'custom-file-input'})
        self.fields['logo'].widget.attrs.update({'id': 'file_logo'})
        self.fields['logo'].widget.attrs.update({'type': 'file'})


class MemberStoreSettingsCourierForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ('couriers',)

    def __init__(self, *args, **kwargs):
        super(MemberStoreSettingsCourierForm, self).__init__(*args, **kwargs)
        self.fields['couriers'].widget.attrs.update({'class': 'form-control'})
