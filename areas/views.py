from django.shortcuts import render

#Create your views here.
from rest_framework import viewsets
from .models import Area
from .serializers import AreaSerializer
from permissions.utils.utils import user_has_permission
from users.utils.validations import PermissionValidatedViewSet
from rest_framework.permissions import IsAuthenticated

class AreaViewSet(PermissionValidatedViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    view_perm = 'view_areas'
    add_perm = 'add_area'
    change_perm = 'change_area'
    delete_perm = 'delete_area'
    permission_classes = [IsAuthenticated]