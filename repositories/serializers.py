from rest_framework import serializers
from .models import Repository
from .utils.validators import validate_repository_name, validate_repository_url

class RepositorySerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        return validate_repository_name(value, self.instance)

    def validate_repository_url(self, value):
        return validate_repository_url(value)

    class Meta:
        model = Repository
        fields = '__all__'
