from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from users.models import User

class Permission(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'permissions'

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
