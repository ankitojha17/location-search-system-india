from rest_framework import serializers

class LocationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    state = serializers.CharField(max_length=100)
    description = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)

def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value.title() 