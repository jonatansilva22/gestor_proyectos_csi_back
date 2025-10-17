from rest_framework import serializers
from tools.models import Tool
from tools.utils.validators import validate_tool_name, validate_tool_image

class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'

    def validate(self, data):
        if not self.instance and not data.get("image"):
            raise serializers.ValidationError({"image": "La imagen es obligatoria."})
        return data

    def validate_name(self, value):
        return validate_tool_name(value, instance=self.instance)

    def validate_image(self, value):
        return validate_tool_image(value)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            try:
                data['image'] = instance.image.url  # Devuelve la URL Cloudinary
            except Exception:
                data['image'] = None
        else:
            data['image'] = None
        return data

