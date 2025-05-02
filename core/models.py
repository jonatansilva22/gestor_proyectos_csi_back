from django.db import models

class RoleType(models.Model):
    role_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'roles_types'

class PermissionType(models.Model):
    permission_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'permissions_types'

class StatusType(models.Model):
    status_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'status_types'

class WorkGroup(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'works_groups'

class Tool(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'tools'

class Area(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'areas'

class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(RoleType, on_delete=models.DO_NOTHING)  # especificando el nombre de la columna
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True, blank=True)
    project_owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # especificando el nombre de la columna
    group = models.ForeignKey(WorkGroup, on_delete=models.DO_NOTHING, null=True, blank=True)  # especificando el nombre de la columna
    status = models.ForeignKey(StatusType, on_delete=models.DO_NOTHING)  # especificando el nombre de la columna
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'projects'

class Repository(models.Model):
    name = models.CharField(max_length=30)
    repository_url = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)  # especificando el nombre de la columna

    class Meta:
        db_table = 'repositories'

class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # especificando el nombre de la columna
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)  # especificando el nombre de la columna
    permission_type = models.ForeignKey(PermissionType, on_delete=models.DO_NOTHING)  # especificando el nombre de la columna

    class Meta:
        db_table = 'permissions'

class ToolProject(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.DO_NOTHING)  # especificando el nombre de la columna
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)  # especificando el nombre de la columna

    class Meta:
        db_table = 'tools_projects'

class WorkGroupUser(models.Model):
    group = models.ForeignKey(WorkGroup, on_delete=models.DO_NOTHING)  # especificando el nombre de la columna
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # especificando el nombre de la columna

    class Meta:
        db_table = 'works_groups_users'

class AreaProject(models.Model):
    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING)  # especificando el nombre de la columna
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)  # especificando el nombre de la columna

    class Meta:
        db_table = 'areas_projects'
