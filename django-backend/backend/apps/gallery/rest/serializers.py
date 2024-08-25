from django.utils.translation import gettext as _
from rest_framework import serializers, exceptions

from apps.jobs import models
from apps.jobs.rest.serializers import SDModelSerializer, ActionSerializer, TagSerializer


class RequestImageGalleryDetailSerializer(serializers.Serializer):
    create = update = None
    pk = serializers.UUIDField(required=True)

    @classmethod
    def get_or_404(cls, job_id: str):
        gallery = models.ImageGallery.objects.select_related(
            'job__action', 'job__sd_model',
        ).prefetch_related(
            'job__filters',
        ).filter(job_id=job_id).first()
        if gallery:
            return gallery

        job = models.GenerateJob.objects.filter(pk=job_id).first()
        if job:
            return models.ImageGallery.objects.create(
                job=job,
            )
        raise exceptions.NotFound()

    def validate(self, attrs):
        attrs['obj'] = self.get_or_404(job_id=attrs['pk'])
        return attrs


class RequestVideoGalleryDetailSerializer(serializers.Serializer):
    create = update = None
    pk = serializers.UUIDField(required=True)

    def validate(self, attrs):
        attrs['obj'] = models.VideoGallery.objects.filter(job_id=attrs['pk']).first()
        if not attrs['obj']:
            raise exceptions.NotFound()
        return attrs


class RequestImageGallerySerializer(serializers.Serializer):
    create = update = None
    query = serializers.CharField(required=False)
    sd_model_id = serializers.IntegerField(required=False)
    action_id = serializers.IntegerField(required=False)
    filter_ids = serializers.CharField(required=False)

    def validate(self, attrs):
        if attrs.get('filter_ids'):
            try:
                attrs['filter_ids'] = list(map(int, attrs['filter_ids'].split(',')))
            except Exception:
                raise exceptions.ValidationError({
                    'filter_ids': _('Incorrect value')
                })
        return attrs


class RequestVideoGallerySerializer(serializers.Serializer):
    create = update = None
    query = serializers.CharField(required=False)
    sd_model_id = serializers.IntegerField(required=False)
    filter_ids = serializers.CharField(required=False)

    def validate(self, attrs):
        if attrs.get('filter_ids'):
            try:
                attrs['filter_ids'] = list(map(int, attrs['filter_ids'].split(',')))
            except Exception:
                raise exceptions.ValidationError({
                    'filter_ids': _('Incorrect value')
                })
        return attrs


class CollectionSerializer(serializers.Serializer):
    name = serializers.CharField()
    filter_ids = serializers.ListSerializer(child=serializers.IntegerField())


class ImageGalleryFilterSerializer(serializers.Serializer):
    create = update = None
    collections = serializers.ListSerializer(child=CollectionSerializer())
    tags = TagSerializer(many=True)


class ImageGallerySerializer(serializers.Serializer):
    create = update = None

    id = serializers.UUIDField()
    image = serializers.ImageField()
    prompt = serializers.CharField()
    likes = serializers.IntegerField()
    is_reaction = serializers.BooleanField()
    created = serializers.DateTimeField()

    def get_image_url(self, instance: models.ImageGallery):
        image = instance.get_image_url()
        if not self.context['user'].is_anonymous and self.context['user'].pk == instance.job.user_id:
            image = instance.job.content
        return image

    def get_reaction(self, instance: models.ImageGallery):
        is_reaction = False
        if not self.context['user'].is_anonymous:
            is_reaction = instance.likes.filter(author=self.context['user'], is_active=True).exists()
        return is_reaction

    def to_representation(self, instance: models.ImageGallery):
        likes_structure = self.context['likes_structure'].get(instance.pk, {
            'count': 0,
            'is_reaction': False
        })

        return dict(
            id=instance.job.pk,
            image=self.get_image_url(instance=instance),
            prompt=instance.filter_words,
            likes=likes_structure['count'],
            is_reaction=likes_structure['is_reaction'],
            created=instance.job.created,
        )


class ImageGalleryDetailSerializer(ImageGallerySerializer):
    sd_model = SDModelSerializer()
    action = ActionSerializer()
    filter_ids = serializers.ListSerializer(child=serializers.IntegerField())

    def to_representation(self, instance: models.ImageGallery):
        data = super().to_representation(instance=instance)

        data.update({
            'sd_model': SDModelSerializer(instance.job.sd_model, context=self.context).data,
            'action': ActionSerializer(instance.job.action).data,
            'filter_ids': instance.job.filters.values_list('id', flat=True),
        })

        return data


class VideoGallerySerializer(serializers.Serializer):
    create = update = None

    id = serializers.UUIDField()
    video = serializers.FileField()
    prompt = serializers.CharField()
    likes = serializers.IntegerField()
    is_reaction = serializers.BooleanField()
    created = serializers.DateTimeField()

    def get_video_url(self, instance: models.VideoGallery):
        video = instance.get_video_url()
        if not self.context['user'].is_anonymous and self.context['user'].pk == instance.job.user_id:
            video = instance.job.content
        return video

    def get_reaction(self, instance: models.VideoGallery):
        is_reaction = False
        if not self.context['user'].is_anonymous:
            is_reaction = instance.likes.filter(author=self.context['user'], is_active=True).exists()
        return is_reaction

    def to_representation(self, instance: models.VideoGallery):
        return dict(
            id=instance.job.pk,
            video=self.get_video_url(instance=instance),
            prompt=instance.filter_words,
            likes=instance.likes_count,
            is_reaction=self.get_reaction(instance=instance),
            created=instance.job.created,
        )


class VideoGalleryDetailSerializer(ImageGallerySerializer):
    sd_model = SDModelSerializer()
    filter_ids = serializers.ListSerializer(child=serializers.IntegerField())

    def to_representation(self, instance: models.ImageGallery):
        data = super().to_representation(instance=instance)

        data.update({
            'sd_model': SDModelSerializer(instance.job.sd_model, context=self.context).data,
            'filter_ids': instance.job.filters.values_list('id', flat=True),
        })

        return data
