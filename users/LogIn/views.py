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
    
    def find_user_by_identifier(self, identifier):
        """
        Busca un usuario por email o username basado en el formato del identifier
        Si contiene @, busca por email; sino, busca por username
        """
        try:
            if '@' in identifier:
                # Buscar por email
                user = User.objects.get(email=identifier)
            else:
                # Buscar por username
                user = User.objects.get(username=identifier)
            return user
        except User.DoesNotExist:
            return None
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            password = serializer.validated_data['password']
            
            # Buscar usuario por email o username
            user = self.find_user_by_identifier(identifier)
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                # Generar token JWT
                payload = {
                    'user_id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'exp': datetime.utcnow() + timedelta(hours=24),
                    'iat': datetime.utcnow(),
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                return Response({
                    'message': 'Login exitoso', 
                    'token': token,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)