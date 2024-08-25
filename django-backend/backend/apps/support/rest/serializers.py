from rest_framework import serializers


class SupportMessageSerializer(serializers.Serializer):
    create = update = None

    name = serializers.CharField()
    email = serializers.EmailField()
    message = serializers.CharField()
