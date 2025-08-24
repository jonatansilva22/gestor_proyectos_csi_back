import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_password(password: str):
    if len(password or '') < 8:
        raise ValidationError(_('La contraseña debe tener al menos 8 caracteres.'))
    if not re.search(r'[A-Z]', password):
        raise ValidationError(_('La contraseña debe contener al menos una letra mayúscula.'))
    if not re.search(r'[a-z]', password):
        raise ValidationError(_('La contraseña debe contener al menos una letra minúscula.'))
    if not re.search(r'[0-9]', password):
        raise ValidationError(_('La contraseña debe contener al menos un número.'))
    if not re.search(r'[\W_]', password):
        raise ValidationError(_('La contraseña debe contener al menos un carácter especial.'))

