from rest_framework import serializers
from .models import Area
from .utils.validators import validate_area_name

class AreaSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        return validate_area_name(value, self.instance)

    class Meta:
        model = Area
        fields = '__all__'