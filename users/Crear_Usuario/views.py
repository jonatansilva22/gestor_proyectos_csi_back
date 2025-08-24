from django.shortcuts import render
from rest_framework import viewsets
from users.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from permissions.utils.utils import user_has_permission
from users.utils.validations import UserPermissionValidatedViewSet
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


def notificar_cambios_usuario(user_email, username, cambios_realizados, cambio_por_admin=False, admin_username=None):
    """
    Notifica al usuario sobre cambios realizados en su perfil
    """
    if cambio_por_admin:
        subject = 'Cambios en tu perfil realizados por administrador'
        introduccion = f'Hola {username},\n\nUn administrador ({admin_username}) ha realizado cambios en tu perfil:'
    else:
        subject = 'Confirmación de cambios en tu perfil'
        introduccion = f'Hola {username},\n\nSe han realizado cambios en tu perfil:'

    # Construir lista de cambios
    cambios_texto = []
    for campo, info in cambios_realizados.items():
        if campo == 'password':
            cambios_texto.append("• Contraseña actualizada")
        elif campo == 'email':
            cambios_texto.append(f"• Correo electrónico: {info['anterior']} → {info['nuevo']}")
        elif campo == 'username':
            cambios_texto.append(f"• Nombre de usuario: {info['anterior']} → {info['nuevo']}")
        elif campo == 'first_name':
            cambios_texto.append(f"• Nombre: {info['anterior']} → {info['nuevo']}")
        elif campo == 'last_name':
            cambios_texto.append(f"• Apellido: {info['anterior']} → {info['nuevo']}")
        elif campo == 'role':
            cambios_texto.append(f"• Rol: {info['anterior']} → {info['nuevo']}")
        elif campo == 'photo':
            cambios_texto.append("• Foto de perfil actualizada")

    cambios_listado = '\n'.join(cambios_texto)
    
    if cambio_por_admin:
        nota_seguridad = '\n\nSi no esperabas estos cambios, por favor contacta al administrador del sistema.'
    else:
        nota_seguridad = '\n\nSi no realizaste estos cambios, por favor contacta al administrador del sistema inmediatamente.'

    message = f"""
{introduccion}

{cambios_listado}
{nota_seguridad}

Saludos,
CSI PRO.
"""
    
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print(f"Notificación de cambios enviada a {user_email}")
    except Exception as e:
        print(f"Error enviando notificación de cambios: {e}")


class UserViewSet(UserPermissionValidatedViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
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
    
    def perform_update(self, serializer):
        # Obtener información antes de guardar
        instance = serializer.instance
        user_email = instance.email
        username = instance.username
        
        # Determinar si el cambio lo hace el propio usuario o un admin
        usuario_actual = self.request.user
        es_cambio_por_admin = (usuario_actual.id != instance.id)
        admin_username = usuario_actual.username if es_cambio_por_admin else None
        
        # Guardar cambios
        updated_instance = serializer.save()
        
        # Obtener cambios detectados por el serializer
        cambios_realizados = getattr(serializer, 'cambios_realizados', {})
        
        # Si hubo cambios, enviar notificación
        if cambios_realizados:
            # Usar el email actual para envío (en caso de que se haya cambiado el email, usar el nuevo)
            email_para_envio = updated_instance.email
            username_para_envio = updated_instance.username
            
            notificar_cambios_usuario(
                email_para_envio,
                username_para_envio, 
                cambios_realizados,
                cambio_por_admin=es_cambio_por_admin,
                admin_username=admin_username
            )