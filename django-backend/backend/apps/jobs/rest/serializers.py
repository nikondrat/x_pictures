from datetime import timedelta

from django.utils.translation import gettext as _
from rest_framework import serializers, exceptions

from drf_spectacular.utils import extend_schema_field

from apps.profiles.models import ProfileType
from apps.jobs import models
from apps.jobs.rest.utils import get_sd_model_available_in


DEFAULT_PROMPT = "2D Vector Illustration of a child with soccer ball Art for Sublimation, Design Art, Chrome  Art, Painting Painting and Stunning  Artwork, Highly Detailed Digital  Painting, Airbrush Art, Highly Detailed Digital Artwork, Dramatic Artwork, stained antique yellow copper paint, digital airbrush art, detailed by Mark Brooks, Chicano airbrush art, Swagger! snake Culture"
DEFAULT_NEGATIVE_PROMPT = "low resolution, low details"


class BaseJobSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField(required=None, default=None)
    is_blur = serializers.BooleanField(source='need_blur')
    user_balance = serializers.SerializerMethodField()
    estimated_timestamp = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'status', 'content',
            'estimated_time', 'estimated_timestamp',
            'time_spent', 'created', 'updated',
            'is_blur', 'user_balance',
        )

    @classmethod
    @extend_schema_field(serializers.URLField())
    def get_content(cls, instance: models.AbstractJob):
        return instance.content

    @extend_schema_field(serializers.DecimalField(max_digits=25, decimal_places=2, default=0))
    def get_user_balance(self, instance: models.AbstractJob):
        if self.context.get('user') and self.context['user'].is_authenticated:
            return str(self.context['user'].profile.balance)
        elif instance.user:
            return str(instance.user.profile.balance)
        else:
            return '0.00'

    @classmethod
    @extend_schema_field(serializers.IntegerField())
    def get_estimated_timestamp(cls, instance: models.AbstractJob):
        dtime = instance.created + timedelta(seconds=instance.estimated_time)
        return int(dtime.timestamp())


class RequestJobSerializer(serializers.Serializer):
    create = update = None
    pk = serializers.UUIDField(label=_('Job id'))


class FilterSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='public_name')

    class Meta:
        model = models.Filter
        fields = ('id', 'title')


class CategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='public_name')
    filters = FilterSerializer(many=True)

    class Meta:
        model = models.Category
        fields = ('id', 'title', 'use_many_filters', 'filters')


class TagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name')
    categories = CategorySerializer(many=True)

    class Meta:
        model = models.Tag
        fields = ('id', 'title', 'categories')


class ActionSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='public_name')

    class Meta:
        model = models.Action
        fields = ('id', 'title', 'image')


class SDModelSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='public_name')
    is_lock = serializers.BooleanField()
    available_in = serializers.IntegerField(default=None, help_text=_('Subscription id'))

    class Meta:
        model = models.SDModel
        fields = ('id', 'title', 'image', 'is_lock', 'available_in')

    def to_representation(self, instance: models.SDModel):
        available_in = get_sd_model_available_in(sd_model=instance)

        if self.context['user'].is_anonymous:
            is_lock = available_in is not None
        elif available_in == 6:
            is_lock = self.context['user'].profile.type not in [ProfileType.advance, ProfileType.premium,
                                                                ProfileType.super_premium]
        elif available_in == 5:
            is_lock = self.context['user'].profile.type not in [ProfileType.premium, ProfileType.super_premium]
        else:
            is_lock = False

        image_url = instance.image.url if instance.image else None
        return dict(
            id=instance.id,
            title=instance.public_name,
            image=image_url,
            is_lock=is_lock,
            available_in=available_in,
        )


class UndressFilterSerializer(serializers.Serializer):
    create = update = None
    cost = serializers.FloatField()
    cost_without_mask = serializers.FloatField()
    categories = CategorySerializer(many=True)


class GenerateFilterSerializer(serializers.Serializer):
    create = update = None

    cost = serializers.FloatField()
    current_sd_model_id = serializers.IntegerField()
    tags = TagSerializer(many=True)
    sd_models = SDModelSerializer(many=True)
    actions = ActionSerializer(many=True)


class InstagramUndressFilterSerializer(serializers.Serializer):
    create = update = None
    parsing_cost = serializers.FloatField()
    undress_cost_per_image = serializers.FloatField()
    categories = CategorySerializer(many=True)


class VideoJobFilterSerializer(serializers.Serializer):
    create = update = None
    cost = serializers.FloatField()
    current_sd_model_id = serializers.IntegerField()
    tags = TagSerializer(many=True)
    sd_models = SDModelSerializer(many=True)


class CreateUndressJobSerializer(serializers.Serializer):
    create = update = None
    filter_ids = serializers.ListSerializer(child=serializers.IntegerField(), required=True)
    image_b64 = serializers.CharField(label=_('Image Base64'), required=True)
    mask_b64 = serializers.CharField(label=_('Mask Base64'), required=True)


class CreateUndressJobWithoutMaskSerializer(serializers.Serializer):
    create = update = None
    filter_ids = serializers.ListSerializer(child=serializers.IntegerField(), required=True)
    image_b64 = serializers.CharField(label=_('Image Base64'), required=True)


class CreateGenerateJobSerializer(serializers.Serializer):
    create = update = None

    filter_ids = serializers.ListSerializer(child=serializers.IntegerField(), required=True)
    sd_model_id = serializers.IntegerField(required=False, default=1)
    action_id = serializers.IntegerField(required=False, default=1)


class CreateWhiteGenerateJobSerializer(serializers.Serializer):
    create = update = None
    sd_model_id = serializers.IntegerField(required=False, default=12)
    prompt = serializers.CharField(required=False, default=DEFAULT_PROMPT)
    negative_prompt = serializers.CharField(required=False, default=DEFAULT_NEGATIVE_PROMPT)


class CreateVideoJobSerializer(serializers.Serializer):
    create = update = None
    filter_ids = serializers.ListSerializer(child=serializers.IntegerField(), required=True)
    sd_model_id = serializers.IntegerField(required=False, default=9)


class UndressJobSerializer(BaseJobSerializer):
    class Meta(BaseJobSerializer.Meta):
        model = models.UndressJob


class GenerateJobSerializer(BaseJobSerializer):
    class Meta(BaseJobSerializer.Meta):
        model = models.GenerateJob


class InstagramUndressParsingSerializer(serializers.Serializer):
    create = update = None
    link = serializers.URLField()
    qty = serializers.IntegerField(required=False, default=12)


class CreateInstagramUndressJobSerializer(serializers.Serializer):
    create = update = None
    id = serializers.UUIDField(required=False)
    filter_ids = serializers.DictField(required=True)
    exclude_ids = serializers.ListSerializer(child=serializers.IntegerField(), required=False)
    custom_masks = serializers.DictField(required=False)

    def validate(self, attrs):
        job = models.InstagramUndressJob.objects.filter(
            pk=attrs['id']
        ).prefetch_related(
            'sources', 'jobs',
        ).first()
        if not job:
            raise exceptions.NotFound('Job not found')

        attrs['job'] = job
        return attrs


class InstagramSourceSerializer(serializers.ModelSerializer):
    basic_mask_url = serializers.SerializerMethodField()

    class Meta:
        model = models.InstagramSource
        fields = (
            'id', 'image_url',
            'basic_mask_url',
        )

    @classmethod
    @extend_schema_field(field=serializers.URLField(required=False))
    def get_basic_mask_url(cls, instance: models.InstagramSource):
        if instance.basic_mask:
            return instance.basic_mask.url


class InstagramUndressJobSerializer(serializers.ModelSerializer):
    current_status = serializers.IntegerField(source='detail_status')
    parser_estimated_timestamp = serializers.SerializerMethodField()
    user_balance = serializers.SerializerMethodField()
    sources = InstagramSourceSerializer(many=True)
    jobs = UndressJobSerializer(many=True)

    class Meta:
        model = models.InstagramUndressJob
        fields = (
            'id', 'current_status', 'link_type',
            'sources', 'jobs', 'parser_estimated_time',
            'parser_estimated_timestamp', 'parser_time_spent',
            'created', 'updated', 'user_balance'
        )

    @extend_schema_field(serializers.DecimalField(max_digits=25, decimal_places=2, default=0))
    def get_user_balance(self, instance: models.InstagramUndressJob):
        if self.context.get('user') and self.context['user'].is_authenticated:
            return str(self.context['user'].profile.balance)
        elif instance.user:
            return str(instance.user.profile.balance)
        else:
            return '0.00'

    @classmethod
    @extend_schema_field(serializers.IntegerField())
    def get_parser_estimated_timestamp(cls, instance: models.InstagramUndressJob):
        dtime = instance.created + timedelta(seconds=instance.parser_estimated_time)
        return int(dtime.timestamp())


class VideoJobSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField(required=None, default=None)
    user_balance = serializers.SerializerMethodField()
    estimated_timestamp = serializers.SerializerMethodField()

    class Meta(BaseJobSerializer.Meta):
        model = models.VideoJob
        fields = (
            'id', 'status', 'preview', 'content',
            'estimated_time', 'estimated_timestamp',
            'time_spent', 'created', 'updated',
            'user_balance',
        )

    @classmethod
    @extend_schema_field(serializers.URLField())
    def get_content(cls, instance: models.AbstractJob):
        return instance.content

    @extend_schema_field(serializers.DecimalField(max_digits=25, decimal_places=2, default=0))
    def get_user_balance(self, instance: models.AbstractJob):
        if self.context.get('user') and self.context['user'].is_authenticated:
            return str(self.context['user'].profile.balance)
        elif instance.user:
            return str(instance.user.profile.balance)
        else:
            return '0.00'

    @classmethod
    @extend_schema_field(serializers.IntegerField())
    def get_estimated_timestamp(cls, instance: models.AbstractJob):
        dtime = instance.created + timedelta(seconds=instance.estimated_time)
        return int(dtime.timestamp())
