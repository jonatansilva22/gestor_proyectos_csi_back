from rest_framework import serializers
from projects.models import Project
from PIL import Image

def validate_positive(value):
    if value < 0:
        raise serializers.ValidationError("El valor debe ser positivo.")
    return value

def validate_image_format(image):
    if image is None:
        return image
    img = Image.open(image)
    if img.format not in ['JPEG', 'PNG']:
        raise serializers.ValidationError("Solo se permiten imágenes JPEG o PNG.")
    return image

def validate_name(value, instance=None):
    if not value:
        raise serializers.ValidationError("El nombre es obligatorio.")
    if len(value) < 3:
        raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")

    qs = Project.objects.filter(name__iexact=value)
    if instance:
        qs = qs.exclude(pk=instance.pk)
    if qs.exists():
        raise serializers.ValidationError("Ya existe un proyecto con este nombre.")
    return value

def validate_description(value, instance=None):
    if value and len(value) > 500:
        raise serializers.ValidationError("La descripción no puede superar los 500 caracteres.")
    return value

def validate_dates(start, end):
    if start and end:
        if end < start:
            raise serializers.ValidationError("La fecha final no puede ser anterior a la de inicio.")
        if start > end:
            raise serializers.ValidationError("La fecha de inicio no puede ser posterior a la fecha final.")
    return True