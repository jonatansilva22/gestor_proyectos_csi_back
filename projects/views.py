from django.shortcuts import render
from rest_framework import viewsets
from .Serializers import ProjectSerializer, StatusTypeSerializer
from .models import Project, StatusType

# Create your views here.

class StatusTypeViewSet(viewsets.ModelViewSet):
    queryset = StatusType.objects.all() # type: ignore[attr-defined]
    serializer_class = StatusTypeSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all() # type: ignore[attr-defined]
    serializer_class = ProjectSerializer


