from rest_framework import serializers
from areas.models import Area

def validate_area_name(value, instance=None):
    if not value:
        raise serializers.ValidationError("El nombre del área es obligatorio.")
    if len(value) < 3:
        raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
    qs = Area.objects.filter(name=value)
    if instance:
        qs = qs.exclude(id=instance.id)
    if qs.exists():
        raise serializers.ValidationError("Ya existe un área con este nombre.")
    return value