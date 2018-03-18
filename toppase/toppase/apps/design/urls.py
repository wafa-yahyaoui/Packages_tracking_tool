from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from . import views
from views import CreateOrUpadateConfEmailView, CreateOrUpdateConfTriggerView
from ..accounts.views import CreateOrUpdateConfLandigPageView

# from .views import UserLoginView, SendMailView, SendTestView, \
#         CreateOrUpdateTemplatesView, StatisticsView, ReceiveNotificationsView, \
#     ListeMailsView
#
urlpatterns = [
    url(r'^create-templates/email/$',
        CreateOrUpadateConfEmailView.as_view(),
        name='create_templates_email'
        ),
    url(r'^create-templates/landing-page/$',
        CreateOrUpdateConfLandigPageView.as_view(),
        name='create_templates_landing_page'
        ),
    url(r'^create-templates/trigger/$',
        CreateOrUpdateConfTriggerView.as_view(),
        name='create_templates_trigger'
        ),

]

# This router is used for API
router = DefaultRouter()
router.register(r'StatusDelivery', views.StatusDeliveryViewSet)
router.register(r'Store', views.StoreViewSet)
router.register(r'TemplateEmail', views.TemplateemailViewSet)
router.register(r'ContentEmail', views.ContentEmailViewSet)
urlpatterns += [url(r'^api/', include(router.urls)), ]
