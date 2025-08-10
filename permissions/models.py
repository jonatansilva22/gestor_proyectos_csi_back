from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from users.models import User, RoleType

class Permission(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'permissions'

    def str(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(RoleType, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        db_table = 'role_permissions'
        unique_together = ('role', 'permission')

    def str(self):
        return f"{self.role.name} - {self.permission.name}"

class UserObjectPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    # Parte genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'user_object_permissions'
        unique_together = ('user', 'permission', 'content_type', 'object_id')

class UserModelPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Apunta al modelo (e.g., Project, Area)

    class Meta:
        db_table = 'user_model_permissions'
        unique_together = ('user', 'permission', 'content_type')