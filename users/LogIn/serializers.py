from rest_framework import serializers
import re

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True, help_text="Email o username")
    password = serializers.CharField(required=True, write_only=True)

    def validate_identifier(self, value):
        """Validar que el identifier sea un email válido o username válido"""
        if not value:
            raise serializers.ValidationError("El identificador es requerido.")
        
        # Si contiene @, validar como email
        if '@' in value:
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, value):
                raise serializers.ValidationError("Formato de email inválido.")
            if len(value) > 50:
                raise serializers.ValidationError("El email no debe exceder los 50 caracteres.")
        else:
            # Validar como username
            if len(value) > 50:
                raise serializers.ValidationError("El username no debe exceder los 50 caracteres.")
            if len(value) < 3:
                raise serializers.ValidationError("El username debe tener al menos 3 caracteres.")
        
        return value

    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')
        if not identifier or not password:
            raise serializers.ValidationError("Identificador y contraseña son requeridos.")
        return data