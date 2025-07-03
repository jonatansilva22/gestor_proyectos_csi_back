from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Repository
from .serializers import RepositorySerializer

class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
