from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from permissions.utils.utils import user_has_permission

from projects.models import Project
from repositories.models import Repository
from areas.models import Area
from workgroups.models import WorkGroup
from tools.models import Tool
from users.models import User

from users.Crear_Usuario.serializers import UserSerializer
from projects.Serializers import StatusTypeSerializer, ProjectSerializer
from repositories.serializers import RepositorySerializer
from areas.serializers import AreaSerializer
from tools.serializers import ToolSerializer
from workgroups.serializers import WorkGroupSerializer


# Base genérica para validar permisos por acción
class PermissionValidatedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    view_perm = None
    add_perm = None
    change_perm = None
    delete_perm = None

    def list(self, request, *args, **kwargs):
        if not user_has_permission(request.user, self.view_perm):
            return Response({'error': 'No tienes permiso para ver esta lista'}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not user_has_permission(request.user, self.view_perm):
            return Response({'error': 'No tienes permiso para ver este elemento'}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not user_has_permission(request.user, self.add_perm):
            return Response({'error': 'No tienes permiso para agregar'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not user_has_permission(request.user, self.change_perm):
            return Response({'error': 'No tienes permiso para modificar'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not user_has_permission(request.user, self.delete_perm):
            return Response({'error': 'No tienes permiso para eliminar'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


# ViewSet especializado para usuarios con validación de acceso propio
class UserPermissionValidatedViewSet(PermissionValidatedViewSet):
    """
    ViewSet especializado para usuarios que permite a los colaboradores (role=3)
    acceder solo a su propio perfil, mientras que admin y superadmin pueden acceder a todos.
    """
    
    def _can_access_user(self, request, user_id=None):
        """Verifica si el usuario puede acceder al perfil solicitado"""
        # Si es admin (1) o superadmin (2), puede acceder a cualquier usuario
        if request.user.role and request.user.role.id in [1, 2]:
            return True
        
        # Si es colaborador (3), solo puede acceder a su propio perfil
        if request.user.role and request.user.role.id == 3:
            return str(request.user.id) == str(user_id)
        
        return False
    
    def retrieve(self, request, *args, **kwargs):
        """Permite ver un usuario específico con validación de acceso propio"""
        if not user_has_permission(request.user, self.view_perm):
            return Response({'error': 'No tienes permiso para ver este elemento'}, status=status.HTTP_403_FORBIDDEN)
        
        # Validar acceso al usuario específico
        user_id = kwargs.get('pk')
        if not self._can_access_user(request, user_id):
            return Response({'error': 'Solo puedes acceder a tu propio perfil'}, status=status.HTTP_403_FORBIDDEN)
        
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Permite actualizar usuario con validación de acceso propio"""
        if not user_has_permission(request.user, self.change_perm):
            return Response({'error': 'No tienes permiso para modificar'}, status=status.HTTP_403_FORBIDDEN)
        
        # Validar acceso al usuario específico
        user_id = kwargs.get('pk')
        if not self._can_access_user(request, user_id):
            return Response({'error': 'Solo puedes modificar tu propio perfil'}, status=status.HTTP_403_FORBIDDEN)
        
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Permite actualización parcial con validación de acceso propio"""
        print(f"=== PARTIAL UPDATE INICIADO ===")
        print(f"Usuario solicitante: {request.user.id} (rol: {getattr(request.user.role, 'id', None)})")
        print(f"Usuario a modificar: {kwargs.get('pk')}")
        print(f"Datos recibidos: {request.data}")
        
        if not user_has_permission(request.user, self.change_perm):
            print("ERROR: Usuario sin permisos change_user")
            return Response({'error': 'No tienes permiso para modificar'}, status=status.HTTP_403_FORBIDDEN)
        
        # Validar acceso al usuario específico
        user_id = kwargs.get('pk')
        if not self._can_access_user(request, user_id):
            print("ERROR: Usuario intentando modificar perfil ajeno")
            return Response({'error': 'Solo puedes modificar tu propio perfil'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            print("Llamando a super().partial_update()")
            result = super().partial_update(request, *args, **kwargs)
            print(f"Resultado exitoso: {result.status_code}")
            return result
        except Exception as e:
            print(f"ERROR en partial_update: {str(e)}")
            print(f"Tipo de error: {type(e)}")
            raise