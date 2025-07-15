from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import WorkGroup
from .serializers import WorkGroupSerializer

class WorkGroupViewSet(viewsets.ModelViewSet):
    queryset = WorkGroup.objects.all()
    serializer_class = WorkGroupSerializer