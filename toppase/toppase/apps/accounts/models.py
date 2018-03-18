# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from oauth2_provider.models import AbstractApplication

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# from ..design.models import Design
from ..cores.lib import get_hostname
from .constants import LANG_TYPE, PROVIDER_CHOICE, SIZE, ALLIGNMENT, FONT, STORE_CAT,STATUS
from .managers import UserManager
from django.db import models
from ..abstract.models import LandingPage



class ConfigEmail(models.Model):
    """this class represents the TemplateConfigured Object"""
    font = models.CharField(max_length=20, choices=FONT, verbose_name=_('Font'), default='AR')
    color_menu = models.CharField(max_length=7, verbose_name=_('Color menu'), default='#ffffff')
    color_call_to_action = models.CharField(max_length=7, verbose_name=_('Color call to action'), default='#ffffff')
    allignment = models.CharField(max_length=20, choices=ALLIGNMENT, verbose_name=_('Alignment'), default='center')
    size = models.CharField(max_length=3, verbose_name=_('Size'),choices=SIZE)

    def __unicode__(self):
        return
    class Meta:
        abstract = True




class StatusDelivery(models.Model):
    name = models.CharField(max_length=15,
                            choices=STATUS,
                            unique=True
                             )
    code = models.CharField(max_length=15,
                            unique=True,
                            primary_key=True
                            )

    def __unicode__(self):
        return self.get_name_display()


class NotificationMixin(models.Model):
    news_letter = models.BooleanField(
        verbose_name=_('News Letter'),
        default=True,
        help_text=_('Get updates on new features activated to your account.')
    )
    via_email = models.BooleanField(
        verbose_name=_('E-mail Notification'),
        help_text=_('Receive notifications when status order change, '
                    'check bellow'),
        default= True
    )
    status_deliveries = models.ManyToManyField(StatusDelivery)
    platform = models.BooleanField(
        verbose_name=_('System notification'),
        default=True,
        help_text=_('Get notification when changes happen in your account')
    )

    class Meta:
        abstract = True


class AccessCMSMixin(models.Model):
    provider = models.CharField(
        verbose_name=_('Provider'),
        max_length=20,
        choices=PROVIDER_CHOICE,
    )
    # request_key = models.CharField(
    #     verbose_name=_('Request key'),
    #     max_length=200,
    #     null=True,
    #     blank=True
    # )
    #
    # request_secret = models.CharField(
    #     verbose_name=_('Request secret'),
    #     max_length=200,
    #     null=True,
    #     blank=True
    # )

    # token = models.CharField(
    #     verbose_name=_('TOKEN'),
    #     max_length=200,
    #     null=True,
    #     blank=True
    # )
    #
    # access_token_secret = models.CharField(
    #     verbose_name=_("Secret token"),
    #     max_length=200,
    #     null=True,
    #     blank=True
    # )

    class Meta:
        abstract = True


class AddressLineMixin(models.Model):
    address_line = models.CharField(
        verbose_name=_('Street Address'),
        max_length=200,
        blank=True,
        null=True
    )
    zip_code = models.CharField(
        verbose_name=_('Zip code'),
        max_length=60,
        blank=True,
        null=True
    )
    city = models.CharField(
        verbose_name=_('City'),
        max_length=60,
        blank=True,
        null=True
    )
    country = models.CharField(
        verbose_name=_('Country'),
        max_length=100,
        default=_('France'),
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

    def complete_address(self):
        return '{}, {} {} {}'.format(self.address_line, self.city,
                                     self.zip_code, self.country)


class PersonMixin(models.Model):
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)

    phone = models.CharField(
        verbose_name=_("Phone number"),
        max_length=20,
        help_text=_("Enter your phone"),
        null=True,
        blank=True,
        unique=True
    )

    class Meta:
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name


class Member(AbstractBaseUser, PersonMixin, PermissionsMixin,
             NotificationMixin, AbstractApplication,):
    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )

    language = models.CharField(
        verbose_name=_('Language'),
        max_length=50,
        choices=LANG_TYPE,
        default=LANG_TYPE[0][0],
        help_text=_('Choose your preferred language'),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_short_name(self):
        return self.email

    def get_store(self):
        try:
            print "-------------"
            store = self.store_set.all()[0]
            print "-------------"
            print self.store_set.all()
            print store
            return store
        except IndexError as e:
            Exception(_("%s" % e))

    def get_content_emails(self):
        try:
            print "************++++++++++++++++++++++++++"
            store = self.get_store()
            print store
            print "************"
            content_email = store.contentemail_set.all()
            return content_email
        except IndexError as e:
            Exception(_("%s" % e))

    @property
    def is_business_member(self):
        """ Is the user of type business member """
        return not self.is_staff

    def get_store(self):
        try:
            return self.stores.all()[0]
        except IndexError as e:
            Exception(_("%s" % e))


class Courier(models.Model):
    text = models.CharField(
        verbose_name=_('Text Courier'),
        max_length=200
    )
    code = models.CharField(
        verbose_name=_('Code Courier'),
        max_length=200,
        unique=True,
        primary_key=True
    )

    def __unicode__(self):
        return "%s-%s" % (self.code, self.text)


class ConfigEmail(models.Model):
    """this class represents the TemplateConfigured Object"""
    font = models.CharField(max_length=20, choices=FONT, verbose_name=_('Font'), default='AR')
    color_menu = models.CharField(max_length=7, verbose_name=_('Color menu'), default='#ffffff')
    color_call_to_action = models.CharField(max_length=7, verbose_name=_('Color call to action'), default='#ffffff')
    allignment = models.CharField(max_length=20, choices=ALLIGNMENT, verbose_name=_('Alignment'), default='center')
    size = models.CharField(max_length=3, verbose_name=_('Size'), choices=SIZE)

    def __unicode__(self):
        return "configured Email"

    class Meta:
        abstract = True


class Advert(models.Model):
    link = models.URLField(verbose_name=_('Link'))
    image = models.ImageField(verbose_name=_('Image'))


class ConfigTracking(models.Model):
    l_font = models.CharField(max_length=20, choices=FONT, verbose_name=_('Landing page Font'), default='AR')
    l_color_menu = models.CharField(max_length=7, verbose_name=_('Landing page  Color menu'), default='#00ff00')
    l_color_call_to_action = models.CharField(max_length=7, verbose_name=_('Landing page  Color call to action'),
                                              default='#ff0000')
    l_allignment = models.CharField(max_length=20, choices=ALLIGNMENT, verbose_name=_('Landing page Alignment'),
                                    default='center')
    l_size = models.CharField(max_length=3, verbose_name=_('Landing page  Size'), choices=SIZE,default='12')
    l_background_image = models.ImageField(
        verbose_name=_('Landing page  Background image')
    )
    l_help_url = models.URLField(verbose_name=_('Landing page  HELP URL'))
    advert = models.ForeignKey(Advert, verbose_name=_("Landing page  Advert"), on_delete=models.CASCADE,null=True,blank=True)
    landing_page = models.ForeignKey(LandingPage, verbose_name=_("Landing page"), on_delete=models.CASCADE)

    def __unicode__(self):
        return "configue Tracking"

    class Meta:
        abstract = True


class Design(ConfigEmail, ConfigTracking):
    color_text = models.CharField(max_length=7,
                                  verbose_name=_('Color menu'),
                                  default='#ffffff')
    class Meta :
        abstract = True
    def __unicode__(self):
        return "design class"


class Store(Design, AccessCMSMixin, AddressLineMixin):
    company_name = models.CharField(
        verbose_name=_('Company Name'),
        max_length=200
    )
    name = models.CharField(
        verbose_name=_('Store Name'),
        max_length=200
    )
    url = models.URLField(
        verbose_name=_('Store URL')
    )

    tracking_url = models.URLField(
        verbose_name=_('Tracking URL')
    )

    logo = models.ImageField(
        verbose_name=_('Logo'),
        help_text=_("We recommend using a logo that's at most 150px tall.")
    )
    members = models.ManyToManyField(Member, related_name='stores')
    category = models.CharField(
        verbose_name=_('Category'),
        max_length=150,
        choices=STORE_CAT,
    )
    couriers = models.ManyToManyField(
        Courier
    )

    language = models.CharField(
        verbose_name=_('Language'),
        max_length=50,
        choices=LANG_TYPE,
        default=LANG_TYPE[0][0],
        help_text=_('Choose your preferred language'),
    )

    def __unicode__(self):
        return "%s - Site: %s" % (self.name, self.url)

    def get_hostname(self):
        hostname = get_hostname(self.url)
        return hostname.replace('www.', '')
    def get_staff(self):
        staff_list=[]
        for staff_member in self.members.values():
            staff_list.append(staff_member['email'])
        return staff_list

    def get_couriers(self):
        couriers_list=[]
        for courier in self.couriers.values():
            couriers_list.append(courier['code'])
        return couriers_list


class Client(PersonMixin, AddressLineMixin):
    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        unique=True,
        primary_key=True
    )
    ip_address = models.CharField(
        verbose_name=_('Ip Address'),
        max_length=180,
        null=True,
        blank=True
    )
    def __unicode__(self):
        return self.email

class Link(models.Model):

    store= models.ForeignKey(Store, related_name='links')
    text = models.CharField(
        verbose_name=_('Text'),
        max_length=200
    )
    url= models.URLField(
        verbose_name=_('URL')
    )

# TODO Change it when we add return feature
# class AccessCourier(models.Model):
#     user_id = models.CharField()
#     password = models.CharField(
#         verbose_name=_('password'),
#         max_length=128
#     )
#     store = models.ForeignKey(Store)
#     courier = models.ForeignKey(Courier)
#
#     class Meta:
#         unique_together = ('store', 'courier')
#         verbose_name_plural = _('Access Courier')
