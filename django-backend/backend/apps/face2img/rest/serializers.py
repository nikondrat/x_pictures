from datetime import timedelta

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from apps.face2img import models


class LoraTrainingFaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LoraTrainingFace
        fields = (
            "id",
            "image",
            "created",
        )


class LoraSerializer(serializers.ModelSerializer):
    training_faces = LoraTrainingFaceSerializer(many=True)
    estimated_timestamp = serializers.SerializerMethodField()

    class Meta:
        model = models.Lora
        fields = (
            "id",
            "status",
            "estimated_time",
            "estimated_timestamp",
            "training_time_seconds",
            "training_faces",
            "cost",
            "created",
        )

    @classmethod
    @extend_schema_field(serializers.IntegerField())
    def get_estimated_timestamp(cls, instance: models.Lora):
        dtime = instance.created + timedelta(seconds=instance.estimated_time)
        return int(dtime.timestamp())


class RequestLoraSerializer(serializers.Serializer):
    create = update = None
    pk = serializers.UUIDField()


class CreateLoraSerializer(serializers.Serializer):
    create = update = None
    images = serializers.ListField(child=serializers.ImageField())


class PackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PackImage
        fields = (
            "id",
            "image",
            "sort",
        )


class PackSerializer(serializers.ModelSerializer):
    images = PackImageSerializer(many=True)

    class Meta:
        model = models.Pack
        fields = (
            "id",
            "name",
            "description",
            "category",
            "images",
        )


class RequestPackSerializer(serializers.Serializer):
    create = update = None
    category = serializers.ChoiceField(choices=models.Pack.Category, required=False)


class Face2ImgJobResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Face2ImgJobResult
        fields = (
            "id",
            "image",
            "created",
        )


class Face2ImgJobSerializer(serializers.ModelSerializer):
    lora = LoraSerializer()
    pack = PackSerializer()
    results = Face2ImgJobResultSerializer(many=True)
    estimated_timestamp = serializers.SerializerMethodField()

    class Meta:
        model = models.Face2ImgJob
        fields = (
            "id",
            "lora",
            "pack",
            "results",
            "time_spent",
            "estimated_time",
            "estimated_timestamp",
            "status",
            "cost",
            "created",
        )

    @classmethod
    @extend_schema_field(serializers.IntegerField())
    def get_estimated_timestamp(cls, instance: models.Lora):
        dtime = instance.created + timedelta(seconds=instance.estimated_time)
        return int(dtime.timestamp())


class CreateFace2ImgJobSerializer(serializers.Serializer):
    create = update = None
    lora_id = serializers.UUIDField()
    pack_id = serializers.UUIDField()


class RequestFace2ImgJobSerializer(serializers.Serializer):
    create = update = None
    pk = serializers.UUIDField()
