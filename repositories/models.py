from django.db import models
from projects.models import Project

# Create your models here.

class Repository(models.Model):
    name = models.CharField(max_length=50)
    repository_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'repositories'

    def __str__(self):
        return str(self.name)
    
class RepositoryProject(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='repositories_projects')

    class Meta:
        db_table = 'repositories_projects'