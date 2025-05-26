from django.db import models
from users.models import User
from workgroups.models import WorkGroup

# Create your models here.
class StatusType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'status_types'

    def __str__(self):
        return str(self.name)

class Project(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='projects_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    project_owner = models.ForeignKey(User, on_delete=models.PROTECT)
    group = models.ForeignKey(WorkGroup, on_delete=	models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(StatusType, on_delete=models.PROTECT)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True,blank=True)

    class Meta:
        db_table = 'projects'

    def __str__(self):
        return str(self.name)