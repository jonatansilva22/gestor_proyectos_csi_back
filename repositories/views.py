from django.shortcuts import render

#Create your views here.
from rest_framework import viewsets
from .models import Repository
from .serializers import RepositorySerializer
from permissions.utils.utils import user_has_permission
from users.utils.validations import PermissionValidatedViewSet
from rest_framework.permissions import IsAuthenticated

class RepositoryViewSet(PermissionValidatedViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    view_perm = 'view_repository'
    add_perm = 'add_repository'
    change_perm = 'change_repository'
    delete_perm = 'delete_repository'
    permission_classes = [IsAuthenticated]