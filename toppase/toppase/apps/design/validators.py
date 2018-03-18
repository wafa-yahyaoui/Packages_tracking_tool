from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


def validate_file(value):
    if value.file.content_type != 'text/csv':
        raise ValidationError(_('Le fichier doit etre de type csv'))