from django.db import models
from projects.models import Project
from cloudinary.models import CloudinaryField

# Create your models here.

class Tool(models.Model):
    name = models.CharField(max_length=100)
    image = CloudinaryField('image', folder='tools_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tools'

    def __str__(self):
        return str(self.name)
    
class ToolProject(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tools_projects')

    class Meta:
        db_table = 'tools_projects'