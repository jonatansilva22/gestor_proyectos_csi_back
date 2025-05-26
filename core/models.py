# from django.db import models

# class RoleType(models.Model):
#     role_name = models.CharField(max_length=20)

# class PermissionType(models.Model):
#     permission_name = models.CharField(max_length=20)

# class StatusType(models.Model):
#     status_name = models.CharField(max_length=20)

# class WorkGroup(models.Model):
#     name = models.CharField(max_length=30)

# class Tool(models.Model):
#     name = models.CharField(max_length=50)

# class Area(models.Model):
#     name = models.CharField(max_length=30)

# class User(models.Model):
#     username = models.CharField(max_length=30)
#     email = models.CharField(max_length=30)
#     password = models.CharField(max_length=255)
#     role = models.ForeignKey(RoleType, on_delete=models.DO_NOTHING) 
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class Project(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.CharField(max_length=500, null=True, blank=True)
#     project_owner = models.ForeignKey(User, on_delete=models.DO_NOTHING) 
#     group = models.ForeignKey(WorkGroup, on_delete=models.DO_NOTHING, null=True, blank=True) 
#     status = models.ForeignKey(StatusType, on_delete=models.DO_NOTHING)  
#     start_date = models.DateTimeField(null=True, blank=True)
#     end_date = models.DateTimeField(null=True, blank=True)

# class Repository(models.Model):
#     name = models.CharField(max_length=30)
#     repository_url = models.CharField(max_length=100)
#     project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)  

# class Permission(models.Model):
#     user = models.ForeignKey(User, on_delete=models.DO_NOTHING)  
#     project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)  
#     permission_type = models.ForeignKey(PermissionType, on_delete=models.DO_NOTHING)  

# class ToolProject(models.Model):
#     tool = models.ForeignKey(Tool, on_delete=models.DO_NOTHING)  
#     project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)  

# class WorkGroupUser(models.Model):
#     group = models.ForeignKey(WorkGroup, on_delete=models.DO_NOTHING)  
#     user = models.ForeignKey(User, on_delete=models.DO_NOTHING)  
# class AreaProject(models.Model):
#     area = models.ForeignKey(Area, on_delete=models.DO_NOTHING)  
#     project = models.ForeignKey(Project, on_delete=models.DO_NOTHING) 