# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as _
from django.db import models
from constants import STATUS
from ..abstract.models import TemplateEmail
from ..accounts.models import Store, StatusDelivery

class ContentEmail(models.Model):
    text_body = models.TextField(max_length=500, blank=True, null=True, verbose_name='text body',default='default text body')
    text_footer = models.TextField(max_length=500, blank=True, null=True, verbose_name='text footer',default='default text footer')
    # default = StatusDelivery.objects.get(code='IT')
    status_delivery = models.ForeignKey(StatusDelivery, verbose_name="The Email Status", on_delete=models.CASCADE)
    template_email = models.ForeignKey(TemplateEmail,
                                       verbose_name=_('Choose a Template'), related_name='template_email'
                                       )
    store = models.ForeignKey(Store, verbose_name="Configured Email", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('status_delivery', 'store', 'template_email')

    def __unicode__(self):
        return "[%s]%s-%s" % (self.store.name, self.template_email.name, self.status_delivery.code)
