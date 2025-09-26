from .models import Project, StatusType
from rest_framework import serializers
from projects.utils.validators import (
    validate_name,
    validate_description,
    validate_dates,
    validate_image_format,
)
from areas.models import AreaProject
from areas.serializers import AreaSerializer
from tools.models import ToolProject
from tools.serializers import ToolSerializer
from repositories.models import Repository, RepositoryProject
from repositories.serializers import RepositorySerializer
from workgroups.models import WorkGroup
from workgroups.serializers import WorkGroupSerializer, UserShortSerializer
from users.models import User

class StatusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusType
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    project_owner = UserShortSerializer(read_only=True)
    # Para escritura, recibe el ID del owner
    project_owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='project_owner',
        write_only=True,
        required=False  # <-- Hazlo opcional
    )
    # Escritura
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=StatusType.objects.all(), source='status', write_only=True
    )
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=WorkGroup.objects.all(), source='group', write_only=True, allow_null=True, required=False
    )
    area_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    tool_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    repository_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    # Lectura
    status = StatusTypeSerializer(read_only=True)
    group = WorkGroupSerializer(read_only=True)
    areas = serializers.SerializerMethodField()
    tools = serializers.SerializerMethodField()
    repositories = serializers.SerializerMethodField()

    image = serializers.ImageField(
        validators=[validate_image_format],
        required=False,
        allow_null=True
    )

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'image',
            'description',
            'project_owner',
            'project_owner_id',
            'group',
            'group_id',
            'status',
            'status_id',
            'start_date',
            'end_date',
            'areas',
            'area_ids',
            'tools',
            'tool_ids',
            'repositories',
            'repository_ids',
        ]

    def validate_name(self, value):
        # Si es una actualización (instancia existe)
        instance = getattr(self, 'instance', None)
        if instance:
            if Project.objects.exclude(id=instance.id).filter(name=value).exists():
                raise serializers.ValidationError("Ya existe un proyecto con ese nombre.")
        else:
            if Project.objects.filter(name=value).exists():
                raise serializers.ValidationError("Ya existe un proyecto con ese nombre.")
        return value

    def validate_description(self, value):
        return validate_description(value)

    def validate(self, data):
        validate_dates(data.get('start_date'), data.get('end_date'))
        return data

    def get_areas(self, obj):
        area_projects = AreaProject.objects.filter(project=obj).select_related('area')
        return AreaSerializer([ap.area for ap in area_projects], many=True).data

    def get_tools(self, obj):
        tool_projects = ToolProject.objects.filter(project=obj).select_related('tool')
        return ToolSerializer([tp.tool for tp in tool_projects], many=True).data

    def get_repositories(self, obj):
        repo_projects = RepositoryProject.objects.filter(project=obj).select_related('repository')
        return RepositorySerializer([rp.repository for rp in repo_projects], many=True).data

    def create(self, validated_data):
        area_ids = validated_data.pop('area_ids', [])
        tool_ids = validated_data.pop('tool_ids', [])
        repository_ids = validated_data.pop('repository_ids', [])

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['project_owner'] = request.user

        project = Project.objects.create(**validated_data)

        for area_id in area_ids:
            AreaProject.objects.create(area_id=area_id, project=project)

        for tool_id in tool_ids:
            ToolProject.objects.create(tool_id=tool_id, project=project)

        for repo_id in repository_ids:
            RepositoryProject.objects.create(repository_id=repo_id, project=project)

        return project

    def update(self, instance, validated_data):
        area_ids = validated_data.pop('area_ids', None)
        tool_ids = validated_data.pop('tool_ids', None)
        repository_ids = validated_data.pop('repository_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if area_ids is not None:
            AreaProject.objects.filter(project=instance).delete()
            for area_id in area_ids:
                AreaProject.objects.create(area_id=area_id, project=instance)

        if tool_ids is not None:
            ToolProject.objects.filter(project=instance).delete()
            for tool_id in tool_ids:
                ToolProject.objects.create(tool_id=tool_id, project=instance)

        if repository_ids is not None:
            RepositoryProject.objects.filter(project=instance).delete()
            for repo_id in repository_ids:
                RepositoryProject.objects.create(repository_id=repo_id, project=instance)

        return instance