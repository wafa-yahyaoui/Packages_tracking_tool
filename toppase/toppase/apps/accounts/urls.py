from django.conf.urls import url
from django.contrib.auth.views import password_reset_confirm
from .views import LoginBusinessView, LogoutView, UpdateMemberBusinessView, PasswordResetBusinessView, UpdateMemberBusinessSettingsStoreCourierView, UpdateMemberBusinessSettingsStoreView, UpdateMemberBusinessSettingsStoreDesignView, UpdateMemberBusinessNotificationView


_password_reset = 'password/reset/'
_verify_pattern_token = "/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})"

urlpatterns = [
    # Login Client
    url(r'^user/login/',
        LoginBusinessView.as_view(),
        name='login'),
    # Logout Client
    url(r'^user/logout/',
        LogoutView.as_view(),
        name='logout'),
    # Update Profile Business
    url(r'^user/profile/$',
        UpdateMemberBusinessView.as_view(),
        name='profile'),
    # Update Member Notifiaction Settings
    url(r'^user/profile/notifications$',
        UpdateMemberBusinessNotificationView.as_view(),
        name='notification-settings'),

    url(r'^%s$' % _password_reset,
        PasswordResetBusinessView.as_view(),
        name='reset-password-client'),
    # Landing Page view
    # url(r'^Landing_page/$',
    #     CreateOrUpdateLandigPageView.as_view(),
    #     name='Landing-page'
    #     ),
    # url(r'^%s%s/$' %
    #     (_password_reset, _verify_pattern_token),
    #     password_reset_confirm,
    #     {'template_name': 'accounts/change_password_landing_page.html',
    #      'post_reset_redirect': 'accounts/login/'},
    #     name="password-verify-business"),


# Update Member Store Settings
    url(r'^user/store/(?P<store_id>[0-9]+)/settings/$',
        UpdateMemberBusinessSettingsStoreView.as_view(),
        name='store-settings'),
    url(r'^user/store/(?P<store_id>[0-9]+)/settings/design/$',
        UpdateMemberBusinessSettingsStoreDesignView.as_view(),
        name='store-settings-design'),
    url(r'^user/store/(?P<store_id>[0-9]+)/settings/courier$',
        UpdateMemberBusinessSettingsStoreCourierView.as_view(),
        name='store-settings-courier'),

]
