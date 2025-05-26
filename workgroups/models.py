from django.db import models
from users.models import User

# Create your models here.

class WorkGroup(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'work_groups'

    def __str__(self):
        return str(self.name)
    
class WorkGroupMembership(models.Model):
    group = models.ForeignKey(WorkGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'work_groups_memberships'
