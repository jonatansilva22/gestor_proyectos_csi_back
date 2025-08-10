from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

#Create your views here.
from rest_framework import viewsets
from .models import WorkGroup
from .serializers import WorkGroupSerializer
from permissions.utils.utils import user_has_permission
from users.utils.validations import PermissionValidatedViewSet

class WorkGroupViewSet(PermissionValidatedViewSet):
    queryset = WorkGroup.objects.all()
    serializer_class = WorkGroupSerializer
    view_perm = 'view_groups'
    add_perm = 'add_group'
    change_perm = 'change_group'
    delete_perm = 'delete_group'
    permission_classes = [IsAuthenticated]