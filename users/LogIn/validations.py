def validate_email(email):
    if len(email) > 50:
        raise ValidationError("El correo electrónico no debe exceder los 50 caracteres.")

def validate_password(password):
    if len(password) < 8:
        raise ValidationError("La contraseña debe tener al menos 8 caracteres.")