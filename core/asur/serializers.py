from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if value.content_type != 'application/json':
            raise serializers.ValidationError("Только файлы JSON разрешены для загрузки.")
        return value
