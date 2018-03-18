# from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ContentEmail, StatusDelivery
from ..abstract.models import TemplateEmail
from ..accounts.models import Store


class StatusDeliverySerializer(serializers.HyperlinkedModelSerializer):
    """This class represents the StatusdeliverySerializer"""

    class Meta:
        model = StatusDelivery
        fields = '__all__'


class StoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Store
        fields = ('url','name', 'city',)


class TemplateEmailSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TemplateEmail
        fields = ('url','name', 'html', 'text')


class ContentEmailSerializer(serializers.HyperlinkedModelSerializer):
    """This class represents the ContentEmailSerializer """

    class Meta:
        model = ContentEmail
        fields = ('text_body', 'text_footer','store', 'status_delivery', 'template_email')

