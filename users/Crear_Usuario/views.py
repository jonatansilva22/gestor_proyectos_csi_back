from django.shortcuts import render
from rest_framework import viewsets
from users.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from permissions.utils.utils import user_has_permission
from users.utils.validations import PermissionValidatedViewSet
from django.core.mail import send_mail
from django.conf import settings

def credenciales_email(user_email, username, password):
    subject = 'Tus credenciales de acceso'
    message = f"""
Hola {username},

Tu cuenta ha sido creada exitosamente.

Usuario: {username}
Contraseña: {password}


Saludos,
CSI PRO.
"""
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        print(f"Error enviando correo: {e}")


class UserViewSet(PermissionValidatedViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    view_perm = 'view_user'
    add_perm = 'add_user'
    change_perm = 'change_user'
    delete_perm = 'delete_user'
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = serializer.save()
        raw_password = getattr(serializer, 'raw_password', None)
        if raw_password:
            credenciales_email(user.email, user.username, raw_password)