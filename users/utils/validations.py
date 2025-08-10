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