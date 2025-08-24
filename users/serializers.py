from rest_framework import serializers
from .models import User
from .utils.validators import validate_password as validate_new_password
import bcrypt

class UserSerializer(serializers.ModelSerializer):
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
            'photo',
            'role',
            'created_at',
            'updated_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'current_password': {'write_only': True},
            'new_password': {'write_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def create(self, validated_data):
        raw_password = validated_data.pop('password', None)
        if raw_password:
            try:
                hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
                validated_data['password'] = hashed.decode('utf-8')
            except Exception:
                validated_data['password'] = raw_password
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Rastrear cambios para notificaciones
        cambios_realizados = {}
        
        # Cambio de contraseña con current_password/new_password
        if 'current_password' in validated_data or 'new_password' in validated_data:
            current_password = validated_data.pop('current_password', None)
            new_password = validated_data.pop('new_password', None)

            if not current_password:
                raise serializers.ValidationError({'current_password': 'La contraseña actual es requerida'})
            if not new_password:
                raise serializers.ValidationError({'new_password': 'La nueva contraseña es requerida'})

            # Validar complejidad
            try:
                validate_new_password(new_password)
            except Exception as e:
                raise serializers.ValidationError({'new_password': str(e)})

            # Verificar actual (compatibilidad con hash y texto plano)
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

            # Guardar nueva contraseña hasheada
            try:
                hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                instance.password = hashed.decode('utf-8')
                cambios_realizados['password'] = True
            except Exception:
                instance.password = new_password
                cambios_realizados['password'] = True

        # Si llega 'password' directo, hashear
        if 'password' in validated_data:
            raw = validated_data.pop('password')
            try:
                hashed = bcrypt.hashpw(raw.encode('utf-8'), bcrypt.gensalt())
                validated_data['password'] = hashed.decode('utf-8')
                cambios_realizados['password'] = True
            except Exception:
                validated_data['password'] = raw
                cambios_realizados['password'] = True

        # Rastrear otros cambios
        for attr, value in validated_data.items():
            old_value = getattr(instance, attr, None)
            if old_value != value and attr in ['email', 'username', 'first_name', 'last_name', 'role', 'photo']:
                if attr == 'role':
                    # Para el rol, obtener el nombre legible
                    old_role_name = old_value.name if old_value else 'Sin rol'
                    new_role_name = value.name if value else 'Sin rol'
                    cambios_realizados[attr] = {
                        'anterior': old_role_name,
                        'nuevo': new_role_name
                    }
                else:
                    cambios_realizados[attr] = {
                        'anterior': old_value,
                        'nuevo': value
                    }
            setattr(instance, attr, value)
        
        instance.save()
        
        # Almacenar cambios en el serializer para uso en la vista
        self.cambios_realizados = cambios_realizados
        
        return instance

    # Validaciones de campos de texto
    def validate_first_name(self, value: str):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('El nombre es obligatorio.')
        if len(value) > 50:
            raise serializers.ValidationError('El nombre no debe exceder 50 caracteres.')
        return value

    def validate_last_name(self, value: str):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('El apellido es obligatorio.')
        if len(value) > 50:
            raise serializers.ValidationError('El apellido no debe exceder 50 caracteres.')
        return value
