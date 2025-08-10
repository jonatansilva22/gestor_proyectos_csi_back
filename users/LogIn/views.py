from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .serializers import LoginSerializer
import bcrypt
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.permissions import AllowAny

class LogInView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    # Generar token JWT
                    payload = {
                        'user_id': user.id,
                        'email': user.email,
                        'exp': datetime.utcnow() + timedelta(hours=24),
                        'iat': datetime.utcnow(),
                    }
                    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                    return Response({'message': 'Login exitoso', 'token': token}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)