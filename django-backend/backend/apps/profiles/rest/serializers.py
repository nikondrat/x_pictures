from typing import Optional

from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework import exceptions

from drf_spectacular.utils import extend_schema_field

from apps.profiles import models
from apps.jobs.models import GenerateJob, VideoJob
from apps.jobs.models import ImageGallery, VideoGallery


class ProfileSubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='subscription.pk')
    title = serializers.CharField(source='subscription.public_title')

    class Meta:
        model = models.ProfileSubscription
        fields = (
            'id', 'title', 'is_active', 'start_period', 'end_period',
        )


class ProfileDetailSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='owner.pk')
    email = serializers.CharField(source='owner.email')
    username = serializers.CharField(source='owner.username')
    is_verified = serializers.BooleanField(source='owner.is_verified')
    type_verbose = serializers.CharField(source='get_type_display')
    subscription = serializers.SerializerMethodField(required=False, default=None)

    class Meta:
        model = models.Profile
        fields = (
            'id', 'image', 'balance', 'type', 'type_verbose',
            'email', 'username', 'is_verified',
            'subscription', 'created', 'updated',
        )

    @classmethod
    @extend_schema_field(ProfileSubscriptionSerializer())
    def get_subscription(cls, instance: models.Profile):
        if active_subscription := instance.subscriptions.filter(is_active=True).first():
            return ProfileSubscriptionSerializer(active_subscription).data


class UploadImageSerializer(serializers.Serializer):
    create = update = None
    image = serializers.CharField(label=_('Image Base64'))


class ChangePasswordSerializer(serializers.Serializer):
    create = update = None

    password = serializers.CharField(label=_('Old password'), required=True)
    new_password = serializers.CharField(label=_('New password'), required=True)

    def validate(self, attrs):
        user = self.context['user']
        if user.decoded_password != attrs['password']:
            raise exceptions.ValidationError({
                'password': _('Invalid password'),
            })
        return attrs


class UpdateProfileSerializer(serializers.Serializer):
    create = update = None

    username = serializers.CharField()


class ImageStorageSerializer(serializers.ModelSerializer):
    sd_model_name = serializers.CharField(source='sd_model.public_name')
    action_name = serializers.CharField(source='action.public_name')
    likes = serializers.SerializerMethodField()
    is_reaction = serializers.SerializerMethodField()

    class Meta:
        model = GenerateJob
        fields = (
            'id', 'content', 'sd_model_name',
            'action_name', 'filter_words',
            'likes', 'is_reaction',
            'created'
        )

    @classmethod
    @extend_schema_field(field=serializers.IntegerField())
    def get_likes(cls, instance: GenerateJob):
        image, _ = ImageGallery.objects.get_or_create(job=instance)
        return image.likes_count

    @classmethod
    @extend_schema_field(field=serializers.BooleanField())
    def get_is_reaction(cls, instance: GenerateJob):
        image, _ = ImageGallery.objects.get_or_create(job=instance)
        return image.likes.filter(author_id=instance.user_id, is_active=True).exists()


class LikedImageStorageSerializer(serializers.Serializer):
    create = update = None

    id = serializers.UUIDField()
    content = serializers.URLField()
    likes = serializers.IntegerField()
    is_reaction = serializers.BooleanField()

    def to_representation(self, instance: ImageGallery):
        content = instance.get_image_url()
        if self.context['user'].pk == instance.job.user_id:
            content = instance.job.content

        return dict(
            id=instance.job_id,
            content=content,
            likes=instance.likes_count,
            is_reaction=True,
        )


class VideoStorageSerializer(serializers.ModelSerializer):
    sd_model_name = serializers.CharField(source='sd_model.public_name')
    likes = serializers.SerializerMethodField()
    is_reaction = serializers.SerializerMethodField()

    class Meta:
        model = VideoJob
        fields = (
            'id', 'content', 'sd_model_name',
            'filter_words', 'likes', 'is_reaction',
            'created'
        )

    @classmethod
    @extend_schema_field(field=serializers.IntegerField())
    def get_likes(cls, instance: GenerateJob):
        video, _ = VideoGallery.objects.get_or_create(job=instance)
        return video.likes_count

    @classmethod
    @extend_schema_field(field=serializers.BooleanField())
    def get_is_reaction(cls, instance: GenerateJob):
        video, _ = VideoGallery.objects.get_or_create(job=instance)
        return video.likes.filter(author_id=instance.user_id, is_active=True).exists()


class LikedVideoStorageSerializer(serializers.Serializer):
    create = update = None

    id = serializers.UUIDField()
    content = serializers.URLField()
    likes = serializers.IntegerField()
    is_reaction = serializers.BooleanField()

    def to_representation(self, instance: VideoGallery):
        content = instance.get_video_url()
        if self.context['user'].pk == instance.job.user_id:
            content = instance.job.content

        return dict(
            id=instance.job_id,
            content=content,
            likes=instance.likes_count,
            is_reaction=True,
        )


class CreatePatreonSerializer(serializers.Serializer):
    create = update = None
    code = serializers.CharField()

    def validate(self, attrs):
        from apps.shop.gate.patreon import PaymentGate
        attrs['patreon_info'] = PaymentGate.get_patreon_info_by_code(
            code=attrs['code'],
        )
        return attrs


class PatreonSerializer(serializers.Serializer):
    create = update = None
    is_connected = serializers.BooleanField()
    is_activated = serializers.BooleanField()
    is_member = serializers.BooleanField()

    def to_representation(self, instance: models.Patreon):
        return {
            'is_connected': True,
            'is_activated': instance.patreon_id is not None,
            'is_member': instance.member_id is not None,
        }
