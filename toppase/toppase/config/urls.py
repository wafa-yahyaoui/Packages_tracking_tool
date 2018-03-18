"""toppase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

# from toppase.utils.views import RobotsTextView

urlpatterns = [
    # Admin
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),

    # Account - Login Business
    url(r'^', include('apps.accounts.urls')),
    # Design
    url(r'^loyalty/', include('apps.design.urls')),

    # Tracking - Business
    url(r'^tracking/', include('apps.trackings.urls')),

    #Oauth2 prvider

    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Robots
    # url(r'^robots.txt$', RobotsTextView.as_view()),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

if not settings.DJANGO_STATICFILES:
    # Static and Media files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        # DEBUG TOOLBAR
        url(r'__debug__/', include(debug_toolbar.urls)),
    ]
