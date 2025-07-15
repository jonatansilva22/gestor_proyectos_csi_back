from rest_framework import serializers
from workgroups.models import WorkGroup, WorkGroupMembership

def validate_workgroup_name(value, instance=None):
    if not value:
        raise serializers.ValidationError("El nombre del grupo es obligatorio.")
    if len(value) < 3:
        raise serializers.ValidationError("El nombre del grupo debe tener al menos 3 caracteres.")

    qs = WorkGroup.objects.filter(name=value)
    if instance:
        qs = qs.exclude(id=instance.id)

    if qs.exists():
        raise serializers.ValidationError("Ya existe un grupo con este nombre.")

    return value

def validate_duplicate_users(user_ids):
    if len(user_ids) != len(set(user_ids)):
        raise serializers.ValidationError("No puedes asignar usuarios duplicados al grupo.")
    return user_ids
