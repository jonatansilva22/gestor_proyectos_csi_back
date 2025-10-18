# users/serializers.py
import bcrypt
from rest_framework import serializers
from users.models import User
from users.utils.validators import validate_password as validate_new_password

class UserSerializer(serializers.ModelSerializer):
    # Campos auxiliares para cambio de contraseña en perfil
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'current_password',
            'new_password',
            'photo',   # CloudinaryField se maneja directamente
            'role',
            'created_at',
            'updated_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False}, 
            'role': {'required': False},
            'current_password': {'write_only': True, 'required': False},
            'new_password': {'write_only': True, 'required': False},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.photo:
            try:
                data['photo_url'] = instance.photo.url
            except Exception:
                data['photo_url'] = None
        else:
            data['photo_url'] = None
        return data

    # -----------------------------
    # Crear usuario
    # -----------------------------
    def create(self, validated_data):
        raw_password = validated_data.pop('password', None)
        if raw_password:
            hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
            validated_data['password'] = hashed_password.decode('utf-8')

        # DRF y Cloudinary manejan el campo photo automáticamente
        user = User.objects.create(**validated_data)
        return user

    # -----------------------------
    # Actualizar usuario
    # -----------------------------
    def update(self, instance, validated_data):
        # Cambio de foto
        if 'photo' in validated_data:
            instance.photo = validated_data.pop('photo')

        # Cambio de contraseña con current_password/new_password
        current_password = validated_data.pop('current_password', None)
        new_password = validated_data.pop('new_password', None)
        if current_password or new_password:
            if not current_password:
                raise serializers.ValidationError({'current_password': 'La contraseña actual es requerida'})
            if not new_password:
                raise serializers.ValidationError({'new_password': 'La nueva contraseña es requerida'})

            # Validar nueva contraseña
            try:
                validate_new_password(new_password)
            except Exception as e:
                raise serializers.ValidationError({'new_password': str(e)})

            # Verificar contraseña actual
            ok = False
            try:
                if instance.password and instance.password.startswith('$2'):
                    ok = bcrypt.checkpw(current_password.encode('utf-8'), instance.password.encode('utf-8'))
                else:
                    ok = instance.password == current_password
            except Exception:
                ok = instance.password == current_password

            if not ok:
                raise serializers.ValidationError({'current_password': 'La contraseña actual es incorrecta'})

            hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            instance.password = hashed.decode('utf-8')

        # Cambio directo de password
        if 'password' in validated_data:
            raw = validated_data.pop('password')
            hashed = bcrypt.hashpw(raw.encode('utf-8'), bcrypt.gensalt())
            instance.password = hashed.decode('utf-8')

        # Actualizar otros campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    # -----------------------------
    # Validaciones
    # -----------------------------
    def validate_first_name(self, value: str):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('El nombre no puede estar vacío.')
        if len(value) > 50:
            raise serializers.ValidationError('El nombre no debe exceder 50 caracteres.')
        return value

    def validate_last_name(self, value: str):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('El apellido no puede estar vacío.')
        if len(value) > 50:
            raise serializers.ValidationError('El apellido no debe exceder 50 caracteres.')
        return value

    def validate_username(self, value):
        import re
        if not re.match(r'^[a-zA-Z0-9_.-]{3,50}$', value):
            raise serializers.ValidationError(
                'El nombre de usuario debe tener entre 3 y 50 caracteres y solo puede contener letras, números, guiones, puntos y guiones bajos.'
            )
        queryset = User.objects.filter(username=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('El nombre de usuario ya está en uso.')
        return value

    def validate_email(self, value):
        if len(value) > 50:
            raise serializers.ValidationError('El correo electrónico no debe exceder los 50 caracteres.')
        if not value.lower().endswith('@unison.mx'):
            raise serializers.ValidationError('El correo electrónico debe pertenecer al dominio @unison.mx.')
        queryset = User.objects.filter(email=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('El correo electrónico ya está en uso.')
        return value
