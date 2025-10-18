from rest_framework import serializers
from .models import WorkGroup, WorkGroupMembership
from users.models import User
from .utils.validators import validate_workgroup_name, validate_duplicate_users
from users.models import User

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'photo']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.photo:
            try:
                ret['photo'] = instance.photo.url  # Aquí va la URL completa
            except Exception:
                ret['photo'] = None
        return ret

class WorkGroupSerializer(serializers.ModelSerializer):
    user_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    users = UserShortSerializer(many=True, read_only=True)

    class Meta:
        model = WorkGroup
        fields = ['id', 'name', 'created_at', 'updated_at', 'user_ids', 'users']

    def validate_name(self, value):
        return validate_workgroup_name(value, self.instance)

    def validate_user_ids(self, value):
        return validate_duplicate_users(value)

    def create(self, validated_data):
        user_ids = validated_data.pop('user_ids', [])
        group = WorkGroup.objects.create(**validated_data)
        for user_id in user_ids:
            WorkGroupMembership.objects.create(group=group, user_id=user_id)
        return group

    def update(self, instance, validated_data):
        user_ids = validated_data.pop('user_ids', None)
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        if user_ids is not None:
            WorkGroupMembership.objects.filter(group=instance).delete()
            for user_id in user_ids:
                WorkGroupMembership.objects.create(group=instance, user_id=user_id)

        return instance
