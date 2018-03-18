

def settings(request=None):
    """
    Render to template parameter settings
    :param request:
    :return:
    """
    settings_dict = {}
    from django.conf import settings
    for k in settings.TEMPLATE_ACCESSIBLE_SETTINGS:
        settings_dict[k] = getattr(settings, k, '')
    return {"settings": settings_dict}
