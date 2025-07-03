from rest_framework import serializers
from repositories.models import Repository

def validate_repository_name(value, instance=None):
    if not value:
        raise serializers.ValidationError("El nombre del repositorio es obligatorio.")
    if len(value) < 3:
        raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
    
    qs = Repository.objects.filter(name=value)
    if instance:
        qs = qs.exclude(id=instance.id)
    
    if qs.exists():
        raise serializers.ValidationError("Ya existe un repositorio con este nombre.")
    
    return value

def validate_repository_url(value):
    if not value:
        raise serializers.ValidationError("La URL del repositorio es obligatoria.")
    if not value.startswith('http://') and not value.startswith('https://'):
        raise serializers.ValidationError("La URL debe comenzar con http:// o https://.")
    return value
