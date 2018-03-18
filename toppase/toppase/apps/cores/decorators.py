from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def business_user_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                         login_url='/accounts/login/'):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.is_active and not u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
