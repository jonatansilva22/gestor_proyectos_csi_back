import imghdr
from rest_framework import serializers
from tools.models import Tool

def validate_tool_name(value, instance=None):
    if not value:
        raise serializers.ValidationError("El nombre de la herramienta es obligatorio.")
    if len(value) < 3:
        raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
    
    qs = Tool.objects.filter(name=value)
    if instance:
        qs = qs.exclude(id=instance.id)
    
    if qs.exists():
        raise serializers.ValidationError("Ya existe una herramienta con este nombre.")
    
    return value

def validate_tool_image(value):
    if not value:
        raise serializers.ValidationError("La imagen es obligatoria.")
    
    valid_types = ['image/jpeg', 'image/png', 'image/jpg']
    if value.content_type not in valid_types:
        raise serializers.ValidationError("La imagen debe ser de tipo jpg, jpeg o png.")
    
    return value

