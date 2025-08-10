import bcrypt
from rest_framework import serializers
from users.models import User
from users.Crear_Usuario.validations import validate_username, validate_email

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[validate_username])
    email = serializers.EmailField(validators=[validate_email])

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'photo',
            'role',
            'created_at',
            'updated_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        self.raw_password = raw_password
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        validated_data['password'] = hashed_password.decode('utf-8')
        return User.objects.create(**validated_data)