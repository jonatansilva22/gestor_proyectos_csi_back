from django.db import models
from projects.models import Project

# Create your models here.

class Tool(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='tools_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tools'

    def __str__(self):
        return str(self.name)
    
class ToolProject(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tools_projects'