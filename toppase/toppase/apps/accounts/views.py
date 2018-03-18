# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.contrib.auth import forms as auth_forms
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from ..cores.decorators import business_user_required
from .models import ConfigTracking, Member, Store
from .forms import MemberNotificationForm, MemberStoreSettingsStoreForm, MemberStoreSettingsDesignForm, \
    MemberStoreSettingsCourierForm, MyProfileForm, LandingPageForm


logger = logging.getLogger(__name__)


class BusinessMemberPermissionMixin(object):
    @method_decorator(business_user_required)
    def dispatch(self, request, *args, **kwargs):
        if 'store_id' in kwargs:
            store_id = kwargs.get('store_id')
            get_object_or_404()
        else:
            return HttpResponseForbidden()
        return super(BusinessMemberPermissionMixin, self).dispatch(request, *args,
                                                                   **kwargs)


class LoginBusinessView(auth_views.LoginView):
    template_name = "accounts/login.html"
    redirect_field_name = reverse_lazy("profile")


class LogoutView(auth_views.LogoutView):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    next_page = 'login'


class PasswordResetBusinessView(auth_views.PasswordResetView):
    template_name = "accounts/password_reset_email.html"
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'


# ******************

# class PasswordResetDoneBusinessView(auth_views.PasswordResetDoneView):
#     template_name = ""

class CreateOrUpdateConfLandigPageView(FormView):
    form_class = LandingPageForm
    template_name = 'design/loyalty_landing_page.html'
    def form_valid(self, form):
        Store.objects.update_or_create(
            owner=self.request.user,
            defaults={
                'l_font': form.cleaned_data["l_font"],
                'l_color_menu': form.cleaned_data["l_color_menu"],
                'l_color_call_to_action': form.cleaned_data["l_color_call_to_action"],
                'l_allignment': form.cleaned_data['l_allignment'],
                'l_size': form.cleaned_data["l_size"],
                'l_background_image': form.cleaned_data["l_background_image"],
                'l_help_url': form.cleaned_data["l_help_url"],
            }
        )
        return render(self.request, self.template_name, {'form': form, 'saved': True})


class UpdateMemberBusinessView(TemplateView):
    """ Update information related to Client view """
    template_name = "accounts/my_profile_user.html"

    def post(self, request, *args, **kwargs):
        # Profile form
        success_msg = False
        form_my_profile = MyProfileForm(request.POST, instance=request.user)
        form_change_password = auth_forms.PasswordChangeForm(data=request.POST, user=request.user)

        if form_my_profile.is_valid():
            form_my_profile.save()
            success_msg = True
        password_valid = form_change_password.is_valid()

        if password_valid:
            form_change_password.save()
            update_session_auth_hash(request, request.user)
            success_msg = True
        elif request.POST['old_password'] == '' \
            and request.POST['new_password1'] == '' \
            and request.POST['new_password2'] == '':
            success_msg = True
        else:
            success_msg = False

        if success_msg:
            messages.success(request, _('Saved successfully! '))
        else:
            messages.error(request,
                           _('An error was occurred during the validation of form'))

        context = {"form_my_profile": form_my_profile,
                   "form_change_password": form_change_password,
                   "success_msg": success_msg

                   }

        return TemplateResponse(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        form_my_profile = MyProfileForm(instance=request.user)
        form_change_password = auth_forms.PasswordChangeForm(user=request.user)
        context = {
            "form_my_profile": form_my_profile,
            "form_change_password": form_change_password,

        }
        return TemplateResponse(request, self.template_name, context)

    @method_decorator(business_user_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateMemberBusinessView, self).dispatch(request, *args,
                                                              **kwargs)


class UpdateMemberBusinessNotificationView(TemplateView):
    template_name = 'accounts/my_profile_notifications.html'

    def post(self, request, *args, **kwargs):
        # Notification form
        success_msg = False
        form_notifications = MemberNotificationForm(request.POST, instance=request.user)

        if form_notifications.is_valid():
            form_notifications.save()
            success_msg = True

        if success_msg:
            messages.success(request, _('Saved successfully! '))
        else:
            messages.error(request,
                           _('An error was occurred during the validation of form'))

        context = {"form_notifications": form_notifications,
                   "success_msg": success_msg
                   }

        return TemplateResponse(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        form_notifications = MemberNotificationForm(instance=request.user)
        context = {"form_notifications": form_notifications,
                   }
        return TemplateResponse(request, self.template_name, context)

    @method_decorator(business_user_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateMemberBusinessNotificationView, self).dispatch(request, *args,
                                                                          **kwargs)


class UpdateMemberBusinessSettingsStoreView(TemplateView):
    template_name = 'accounts/store_settings_store.html'

    def post(self, request, *args, **kwargs):
        # Notification form
        form_store = MemberStoreSettingsStoreForm(request.POST, instance=request.user.get_store())

        if form_store.is_valid():
            form_store.save()
            messages.success(request, _('Saved successfully! '))
        else:
            messages.error(request,
                           _('An error was occurred during the validation of form'))

        context = {"form_store": form_store,
                   "api_key": self.request.user.client_id,
                   "api_secret": self.request.user.client_secret,
                   }

        return TemplateResponse(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        form_store = MemberStoreSettingsStoreForm(instance=request.user.get_store())
        context = {"form_store": form_store,
                   "api_key": self.request.user.client_id,
                   "api_secret": self.request.user.client_secret,
                   }
        return TemplateResponse(request, self.template_name, context)

    @method_decorator(business_user_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateMemberBusinessSettingsStoreView, self).dispatch(request, *args,
                                                                           **kwargs)


class UpdateMemberBusinessSettingsStoreDesignView(TemplateView):
    template_name = 'accounts/store_settings_design.html'

    def post(self, request, *args, **kwargs):
        # Notification form
        success_msg = False
        form_design = MemberStoreSettingsDesignForm(request.POST, instance=request.user.get_store())

        if form_design.is_valid():
            form_design.save()
            success_msg = True

        if success_msg:
            messages.success(request, _('Saved successfully! '))
        else:
            messages.error(request,
                           _('An error was occurred during the validation of form'))

        context = {"form_design": form_design,
                   "success_msg": success_msg
                   }

        return TemplateResponse(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        form_design = MemberStoreSettingsDesignForm(instance=request.user.get_store())
        context = {"form_design": form_design,
                   }
        return TemplateResponse(request, self.template_name, context)

    @method_decorator(business_user_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateMemberBusinessSettingsStoreDesignView, self).dispatch(request, *args,
                                                                                 **kwargs)


class UpdateMemberBusinessSettingsStoreCourierView(TemplateView):
    template_name = 'accounts/store_settings_courier.html'

    def post(self, request, *args, **kwargs):
        # Notification form
        success_msg = False
        form_courier = MemberStoreSettingsCourierForm(request.POST, instance=request.user.get_store())

        if form_courier.is_valid():
            form_courier.save()
            success_msg = True

        if success_msg:
            messages.success(request, _('Saved successfully! '))
        else:
            messages.error(request,
                           _('An error was occurred during the validation of form'))

        context = {"form_courier": form_courier,
                   "success_msg": success_msg
                   }

        return TemplateResponse(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        form_courier = MemberStoreSettingsCourierForm(instance=request.user.get_store())
        context = {"form_courier": form_courier,
                   }
        return TemplateResponse(request, self.template_name, context)

    @method_decorator(business_user_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateMemberBusinessSettingsStoreCourierView, self).dispatch(request, *args,
                                                                                  **kwargs)
