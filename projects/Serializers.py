from .models import Project, StatusType
from rest_framework import serializers
from projects.utils.validators import (
    validate_name,
    validate_description,
    validate_dates,
    validate_image_format,
)

class StatusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusType
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    status = StatusTypeSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=StatusType.objects.all(), source='status', write_only=True
    )
    image = serializers.ImageField(
        validators=[validate_image_format],
        required=False,
        allow_null=True
    )

    def validate_name(self, value):
        return validate_name(value)

    def validate_description(self, value):
        return validate_description(value)

    def validate(self, data):
        start = data.get('start_date')
        end = data.get('end_date')
        validate_dates(start, end)
        return data

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'image',
            'description',
            'project_owner',
            'group',
            'status',
            'status_id',
            'start_date',
            'end_date',
        ]
