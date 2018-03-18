# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import QueryDict
from django.template.response import TemplateResponse
from rest_framework import viewsets

from .forms import ConfigEmailForm
from .models import StatusDelivery, ContentEmail
from .serializers import StatusDeliverySerializer, StoreSerializer, ContentEmailSerializer, TemplateEmailSerializer
from .utils import update_context, SplitPostRequest
from .constants import STATUS_VIEW

from ..abstract.models import TemplateEmail
from ..accounts.models import Store


class CreateOrUpadateConfEmailView(TemplateView):
    """ Create or update configured Email view """
    template_name = "design/loyalty_email.html"

    def post(self, request):
        success_msg = False
        form_config_email = ConfigEmailForm(request.POST, instance=request.user.get_store())
        context = {"form_config_email": form_config_email, }
        instance_ = request.user.get_content_emails()
        context.update(update_context(instance_, request.POST))
        if form_config_email.is_valid():
            form_config_email.save()
            success_msg = True
        status = request.POST
        out_dict = SplitPostRequest(status)
        for key in out_dict:
            if key in STATUS_VIEW:
                a = QueryDict('', mutable=True)
                a.update(out_dict[key])
                context[STATUS_VIEW[key]].data = a
                if context[STATUS_VIEW[key]].is_valid():
                    success_msg = True
                    context[STATUS_VIEW[key]].save()

        if success_msg:
            messages.success(request, _('Saved successfully! '))
        else:
            messages.error(request,
                           _('An error was occurred during the validation of form'))

        form_config_email = ConfigEmailForm(instance=request.user.get_store())
        context = {"form_config_email": form_config_email}
        instance_ = request.user.get_content_emails()
        context.update(update_context(instance_))
        return TemplateResponse(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        form_config_email = ConfigEmailForm(instance=request.user.get_store())
        context = {"form_config_email": form_config_email}
        instance_ = request.user.get_content_emails()
        context.update(update_context(instance_))

        return TemplateResponse(request, self.template_name, context)


class CreateOrUpdateConfLandingPageView(TemplateView):
    """ Create or update configured Email view """
    template_name = "design/loyalty_landing_page.html"


class CreateOrUpdateConfTriggerView(TemplateView):
    """ Create or update configured trigger view """
    template_name = "design/loyalty_trigger.html"


class StatusDeliveryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail`
    actions for Status class.
    Necessary for API Implementation.
    """
    queryset = StatusDelivery.objects.all()
    serializer_class = StatusDeliverySerializer


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
       This viewset automatically provides `list` and `detail` actions
        for Store class.
       Necessary for API Implementation.
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class TemplateemailViewSet(viewsets.ReadOnlyModelViewSet):
    """
        This viewset automatically provides `list` and `detail` actions
        for Store class.
        Necessary for API Implementation.
    """
    queryset = TemplateEmail.objects.all()
    serializer_class = TemplateEmailSerializer


class ContentEmailViewSet(viewsets.ReadOnlyModelViewSet):
    """
       This viewset automatically provides `list` and `detail` actions
        for ConfigEmail class.
       Necessary for API Implementation.
    """
    queryset = ContentEmail.objects.all()
    serializer_class = ContentEmailSerializer
