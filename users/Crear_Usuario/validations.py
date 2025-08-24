import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from users.models import User

def validate_username(username):
    if not re.match(r'^[a-zA-Z0-9_.-]{3,50}$', username):
        raise ValidationError(
            _('El nombre de usuario debe tener entre 3 y 50 caracteres y solo puede contener letras, números, guiones, puntos y guiones bajos.')
        )
    if User.objects.filter(username=username).exists():
        raise ValidationError(_('El nombre de usuario ya está en uso.'))

def validate_email(email):
    if len(email) > 50:
        raise ValidationError(_('El correo electrónico no debe exceder los 50 caracteres.'))
    if User.objects.filter(email=email).exists():
        raise ValidationError(_('El correo electrónico ya está en uso.'))

def validate_password(password):
    if len(password) < 8:
        raise ValidationError(_('La contraseña debe tener al menos 8 caracteres.'))
    if not re.search(r'[A-Z]', password):
        raise ValidationError(_('La contraseña debe contener al menos una letra mayúscula.'))
    if not re.search(r'[a-z]', password):
        raise ValidationError(_('La contraseña debe contener al menos una letra minúscula.'))
    if not re.search(r'[0-9]', password):
        raise ValidationError(_('La contraseña debe contener al menos un número.'))
    if not re.search(r'[\W_]', password):
        raise ValidationError(_('La contraseña debe contener al menos un carácter especial.'))
