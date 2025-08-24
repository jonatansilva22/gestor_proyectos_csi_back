from django.db import models

#Create your models here.
class RoleType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'role_types'

    def str(self):
        return str(self.name)


class User(models.Model):
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='users_images/', blank=True, null=True)
    role = models.ForeignKey(RoleType, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_authenticated(self):
        return True

    class Meta:
        db_table = 'users'

    def str(self):
        return str(self.username)
