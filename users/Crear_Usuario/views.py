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
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
import threading

def credenciales_email(user_email, username, password):
    """
    Envía credenciales por email al usuario recién creado usando un template HTML.
    """
    try:
        subject = 'Tus credenciales de acceso'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user_email]

        # Renderizar el template HTML
        html_message = render_to_string('email/credenciales.html', {
            'username': username,
            'password': password,
        })

        # Crear el correo con HTML
        email = EmailMultiAlternatives(
            subject=subject,
            body='Tu cuenta ha sido creada exitosamente.',  # Texto plano de respaldo
            from_email=from_email,
            to=recipient_list,
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
        return {
            'enviado': True,
            'error': None,
            'mensaje': f'Credenciales enviadas exitosamente a {user_email}'
        }
    except Exception as e:
        return {
            'enviado': False,
            'error': 'error_envio',
            'mensaje': f'Error al enviar email: {str(e)}'
        }


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
    except Exception as e:
        pass


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
        raw_password = self.request.data.get('password') or self.request.data.get('new_password')

        def enviar_email_async():
            print("Enviando correo a:", user.email)
            email_status = credenciales_email(user.email, user.username, raw_password)
            print("Resultado del envío:", email_status)
            serializer.email_status = email_status

        if raw_password:
            threading.Thread(target=enviar_email_async).start()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Preparar respuesta con información del usuario creado
        response_data = serializer.data
        
        # Agregar información del estado del email si está disponible
        email_status = getattr(serializer, 'email_status', None)
        if email_status:
            response_data['email_info'] = {
                'enviado': email_status['enviado'],
                'mensaje': email_status['mensaje']
            }
            if not email_status['enviado']:
                response_data['email_info']['error'] = email_status['error']
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
    
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

        # Si hubo cambios, NO enviar notificación por correo
        # (Elimina o comenta la siguiente línea)
        # if cambios_realizados:
        #     notificar_cambios_usuario(
        #         updated_instance.email,
        #         updated_instance.username,
        #         cambios_realizados,
        #         cambio_por_admin=es_cambio_por_admin,
        #         admin_username=admin_username
        #     )