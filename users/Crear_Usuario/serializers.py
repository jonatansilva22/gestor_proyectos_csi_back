import bcrypt
from rest_framework import serializers
from users.models import User
from users.Crear_Usuario.validations import (
    validate_username,
    validate_email,
    validate_password as validate_new_password,
)

class UserSerializer(serializers.ModelSerializer):
    # Remover validadores automáticos - los manejaremos manualmente
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    # Campos auxiliares para cambio de contraseña en perfil
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    # Campo calculado para el nombre del rol
    role_name = serializers.SerializerMethodField()

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
            'role_name',
            'created_at',
            'updated_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False}, 
            'photo': {'required': False},
            'role': {'required': False},
            'current_password': {'write_only': True, 'required': False},
            'new_password': {'write_only': True, 'required': False},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        self.raw_password = raw_password
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        validated_data['password'] = hashed_password.decode('utf-8')
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Rastrear cambios para notificaciones
        cambios_realizados = {}
        
        # Flujo de cambio de contraseña mediante current_password + new_password
        if 'current_password' in validated_data or 'new_password' in validated_data:
            current_password = validated_data.pop('current_password', None)
            new_password = validated_data.pop('new_password', None)

            if not current_password:
                raise serializers.ValidationError({'current_password': 'La contraseña actual es requerida'})
            if not new_password:
                raise serializers.ValidationError({'new_password': 'La nueva contraseña es requerida'})

            # Validar nueva contraseña
            try:
                validate_new_password(new_password)
            except Exception as e:
                raise serializers.ValidationError({'new_password': str(e)})

            # Verificar actual (hash bcrypt o texto plano)
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

            # Guardar nuevo hash
            hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            instance.password = hashed.decode('utf-8')
            cambios_realizados['password'] = True

        # Permitir actualización directa de password (flujos admin)
        if 'password' in validated_data:
            raw = validated_data.pop('password')
            hashed = bcrypt.hashpw(raw.encode('utf-8'), bcrypt.gensalt())
            instance.password = hashed.decode('utf-8')
            cambios_realizados['password'] = True

        # Actualizar solo los campos que fueron enviados explícitamente
        # Esto preserva campos no enviados (como role, photo cuando no se cambia, etc.)
        for attr, value in validated_data.items():
            old_value = getattr(instance, attr, None)
            if old_value != value:
                # Rastrear cambio para notificación
                if attr in ['email', 'username', 'first_name', 'last_name', 'role', 'photo']:
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
        
        # Solo guardar si hubo cambios
        instance.save()
        
        # Almacenar cambios en el serializer para uso en la vista
        self.cambios_realizados = cambios_realizados
        
        return instance

    # Validaciones de nombre y apellido
    def validate_first_name(self, value: str):
        if value is not None:  # Solo validar si se proporciona el campo
            value = (value or '').strip()
            if not value:
                raise serializers.ValidationError('El nombre no puede estar vacío.')
            if len(value) > 50:
                raise serializers.ValidationError('El nombre no debe exceder 50 caracteres.')
        return value

    def validate_last_name(self, value: str):
        if value is not None:  # Solo validar si se proporciona el campo
            value = (value or '').strip()
            if not value:
                raise serializers.ValidationError('El apellido no puede estar vacío.')
            if len(value) > 50:
                raise serializers.ValidationError('El apellido no debe exceder 50 caracteres.')
        return value
    
    def validate(self, attrs):
        """Validación general que diferencia entre creación y actualización"""
        # Si estamos creando un usuario, algunos campos son obligatorios
        if not self.instance:  # Creación
            required_fields = ['username', 'first_name', 'last_name', 'email', 'password', 'role']
            for field in required_fields:
                if field not in attrs or not attrs[field]:
                    raise serializers.ValidationError({field: f'Este campo es obligatorio para crear un usuario.'})
        
        return attrs
    
    def validate_username(self, value):
        """Validación de username que considera actualizaciones"""
        if value is not None:
            # Validación de formato
            import re
            if not re.match(r'^[a-zA-Z0-9_.-]{3,50}$', value):
                raise serializers.ValidationError(
                    'El nombre de usuario debe tener entre 3 y 50 caracteres y solo puede contener letras, números, guiones, puntos y guiones bajos.'
                )
            
            # Validación de unicidad (excluyendo el usuario actual en actualizaciones)
            queryset = User.objects.filter(username=value)
            if self.instance:  # Actualización
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError('El nombre de usuario ya está en uso.')
        
        return value
    
    def validate_email(self, value):
        """Validación de email que considera actualizaciones"""
        if value is not None:
            # Validación de longitud
            if len(value) > 50:
                raise serializers.ValidationError('El correo electrónico no debe exceder los 50 caracteres.')

            #validacion del correo
            if not value.lower().endswith('@unison.mx'):
                raise serializers.ValidationError('El correo electrónico debe pertenecer al dominio @unison.mx.')
            
            # Validación de unicidad (excluyendo el usuario actual en actualizaciones)
            queryset = User.objects.filter(email=value)
            if self.instance:  # Actualización
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError('El correo electrónico ya está en uso.')
        
        return value
    
    def get_role_name(self, obj):
        """Obtener el nombre del rol"""
        if obj.role:
            return obj.role.name
        return None
