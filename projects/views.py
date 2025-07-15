from rest_framework import viewsets
from .models import Project, StatusType
from .Serializers import ProjectSerializer, StatusTypeSerializer

class StatusTypeViewSet(viewsets.ModelViewSet):
    queryset = StatusType.objects.all()
    serializer_class = StatusTypeSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('id')\
        .select_related('group', 'status', 'project_owner')\
        .prefetch_related('areas_projects__area', 'tools_projects__tool', 'repositories_projects__repository')

    serializer_class = ProjectSerializer