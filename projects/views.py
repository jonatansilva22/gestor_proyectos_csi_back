from django.shortcuts import render
from rest_framework import viewsets
from .Serializers import ProjectSerializer, StatusTypeSerializer
from .models import Project, StatusType

from permissions.utils.utils import user_has_permission
from users.utils.validations import PermissionValidatedViewSet
from rest_framework.permissions import IsAuthenticated

#Create your views here.
class StatusTypeViewSet(viewsets.ModelViewSet):
    queryset = StatusType.objects.all() # type: ignore[attr-defined]
    serializer_class = StatusTypeSerializer

class ProjectViewSet(PermissionValidatedViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    view_perm = 'view_projects'
    add_perm = 'add_project'
    change_perm = 'change_project'
    delete_perm = 'delete_project'
    permission_classes = [IsAuthenticated]