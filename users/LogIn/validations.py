import re
from rest_framework import serializers

def validate_email(email):
    if len(email) > 50:
        raise serializers.ValidationError("El correo electrónico no debe exceder los 50 caracteres.")

def validate_password(password):
    if len(password) < 8:
        raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")

def validate_username(username):
    if len(username) > 50:
        raise serializers.ValidationError("El username no debe exceder los 50 caracteres.")
    if len(username) < 3:
        raise serializers.ValidationError("El username debe tener al menos 3 caracteres.")

def validate_identifier(identifier):
    """
    Valida que el identifier sea un email válido o username válido
    """
    if not identifier:
        raise serializers.ValidationError("El identificador es requerido.")
    
    # Si contiene @, validar como email
    if '@' in identifier:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, identifier):
            raise serializers.ValidationError("Formato de email inválido.")
        validate_email(identifier)
    else:
        # Validar como username
        validate_username(identifier)
    
    return identifier