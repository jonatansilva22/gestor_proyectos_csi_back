from django.db import models
from projects.models import Project

# Create your models here.

class Repository(models.Model):
    name = models.CharField(max_length=50)
    repository_url = models.URLField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'repositories'

    def __str__(self):
        return str(self.name)