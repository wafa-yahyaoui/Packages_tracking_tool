from __future__ import unicode_literals
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text

User = get_user_model()


class AccountBackend(ModelBackend):
    """
    Extends Django's ``AccountBackend`` to allow login via
    email or verification token.
    Args are either ``email`` and ``password``, or ``uidb64``
    and ``token``. In either case, ``is_active`` can also be given.
    For login, is_active is not given, so that the login form can
    raise a specific error for inactive users.
    For password reset, True is given for is_active.
    For signup verification, False is given for is_active.
    """
    def authenticate(self, username=None, password=None, **kwargs):
        # Don't allow to chnage username with email
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        try:
            user = User._default_manager.get_by_natural_key(username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            User().set_password(password)

        if 'uidb64' not in kwargs:
            return
        kwargs["id"] = force_text(urlsafe_base64_decode(kwargs.pop("uidb64")))
        token = kwargs.pop('token')
        try:
            user = User.objects.get(pk=kwargs.get("id"))

        except User.DoesNotExist:
            pass
        else:
            if default_token_generator.check_token(user, token):
                return user

    def get_user(self, user_id):
        try:
            return User._default_manager.get(pk=user_id)
        except User.DoesNotExist:
            return None
