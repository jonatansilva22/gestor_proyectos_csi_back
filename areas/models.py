from django.db import models
from projects.models import Project

# Create your models here.

class Area(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'areas'

    def __str__(self):
        return str(self.name)
    
class AreaProject(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        db_table = 'areas_projects'
  

