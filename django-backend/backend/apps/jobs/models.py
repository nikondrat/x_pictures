import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from core.common.utils import PathAndRename
from core.common.mixins import ImageMixin, VideoMixin
from core.users.models import User
from core.users.utils import get_user_by_id
from django.utils.html import mark_safe


class Type(models.IntegerChoices):
    generate = 0, _('Generate')
    undress = 1, _('Undress')
    video = 2, _('Video')


class Tag(ImageMixin, models.Model):
    name = models.CharField(_('Name'), max_length=255)
    image = models.ImageField(_('Image'), upload_to=PathAndRename('tags/'), null=True, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.is_active:
            self.categories.update(is_active=False)
        super().save(*args, **kwargs)


class Category(ImageMixin, models.Model):
    name = models.CharField(_('Name'), max_length=255)
    public_name = models.CharField(_('Public name'), max_length=255)

    image = models.ImageField(_('Image'), upload_to=PathAndRename('categories/'), null=True, blank=True)
    type = models.IntegerField(_('Type'), choices=Type.choices)
    tag = models.ForeignKey(Tag, verbose_name=_('Tag'), on_delete=models.CASCADE,
                            related_name='categories', default=None, null=True, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)

    use_many_filters = models.BooleanField(_('Use many filters'), default=True)

    raw_prompt = models.TextField(_('Raw prompt'), default='')
    raw_negative_prompt = models.TextField(_('Raw negative prompt'), default='')

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.is_active:
            self.filters.update(is_active=False)
        super().save(*args, **kwargs)


class Filter(ImageMixin, models.Model):
    name = models.CharField(_('Name'), max_length=255)
    public_name = models.CharField(_('Public name'), max_length=255)

    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.CASCADE,
                                 related_name='filters')
    image = models.ImageField(_('Image'), upload_to=PathAndRename('filters/'), null=True, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)

    raw_prompt = models.TextField(_('Raw prompt'), default='')
    raw_negative_prompt = models.TextField(_('Raw negative prompt'), default='')

    class Meta:
        verbose_name = _('Filter')
        verbose_name_plural = _('Filters')

    def __str__(self):
        return self.name


class SDModel(ImageMixin, models.Model):
    name = models.CharField(_('Name'), max_length=255)
    public_name = models.CharField(_('Public name'), max_length=255)

    model_name = models.CharField(_('Model name'), max_length=255, default='')
    type = models.IntegerField(_('Type'), choices=Type.choices)
    image = models.ImageField(_('Image'), upload_to=PathAndRename('sd-models/'), null=True, blank=True)

    is_active = models.BooleanField(_('Active'), default=True)
    raw_prompt = models.TextField(_('Raw prompt'), default='')
    raw_negative_prompt = models.TextField(_('Raw negative prompt'), default='')

    class Meta:
        verbose_name = _('SD model')
        verbose_name_plural = _('SD models')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.is_active:
            self.actions.update(is_active=False)
        super().save(*args, **kwargs)


class Action(ImageMixin, models.Model):
    name = models.CharField(_('Name'), max_length=255)
    public_name = models.CharField(_('Public name'), max_length=255)

    sd_model = models.ForeignKey(SDModel, verbose_name=_('SD model'), on_delete=models.CASCADE, related_name='actions')
    image = models.ImageField(_('Image'), upload_to=PathAndRename('actions/'), null=True, blank=True)
    type = models.IntegerField(_('Type'), choices=Type.choices)
    is_active = models.BooleanField(_('Active'), default=True)

    lora_name = models.CharField(_('Lora name'), max_length=255, default='')
    raw_prompt1 = models.TextField(_('Raw prompt'), default='')
    raw_prompt2 = models.TextField(_('Raw prompt'), default='')

    class Meta:
        verbose_name = _('Action')
        verbose_name_plural = _('Actions')

    def __str__(self):
        return self.name


class AbstractJob(models.Model):
    class Status(models.IntegerChoices):
        CREATED = 0, _('Created')
        PROCESS = 1, _('Process')
        SUCCESS = 2, _('Success')
        ERROR = -1, _('Error')

    id = models.UUIDField(_('ID'), primary_key=True, default=uuid.uuid4)
    user_id = models.CharField(_('User ID'), max_length=10, blank=True, null=True)

    status = models.IntegerField(_('Status'), choices=Status.choices, default=Status.CREATED)

    sd_model = models.ForeignKey(SDModel, verbose_name=_('SD model'), on_delete=models.DO_NOTHING)
    filters = models.ManyToManyField(Filter, verbose_name=_('Filters'))
    action = models.ForeignKey(Action, verbose_name=_('Action'), on_delete=models.DO_NOTHING)

    positive_prompt = models.TextField(_('Positive prompt'), default='')
    negative_prompt = models.TextField(_('Negative prompt'), default='')
    step = models.IntegerField(_('Step'), default=20)
    sampler_name = models.CharField(_('Sampler name'), max_length=255, null=True, blank=True)

    estimated_time = models.IntegerField(_('Estimated time'), default=60, help_text=_('In second'))
    time_spent = models.IntegerField(_('Time spent'), default=0, help_text=_('In seconds'))

    cost = models.DecimalField(_('Cost'), max_digits=25, decimal_places=2, default=0)
    show_in_profile = models.BooleanField(_('Show in profile'), default=False)
    need_blur = models.BooleanField(_('Need blur'), default=False)
    need_watermark = models.BooleanField(_('Need watermark'), default=True)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Created'), auto_now=True)

    _user = None

    class Meta:
        abstract = True

    @property
    def user(self) -> User:
        if not self._user:
            self._user = get_user_by_id(user_id=self.user_id)
        return self._user

    @classmethod
    def _get_content_url(cls, content):
        if content:
            return getattr(content, 'url', None)

    @property
    def filter_words(self) -> str:
        return ', '.join(self.filters.values_list('public_name', flat=True))


class UndressJob(ImageMixin, AbstractJob):
    image = models.ImageField(_('Image'), upload_to=PathAndRename('undress-jobs/'), null=True, blank=True)
    blur_image = models.ImageField(_('Image blur'), upload_to=PathAndRename('blur-undress-jobs/'),
                                   null=True, blank=True)
    without_watermark_image = models.ImageField(_('Without watermark image'),
                                                upload_to=PathAndRename('without-watermark-undress-jobs/'),
                                                null=True, blank=True)

    class Meta:
        verbose_name = _('Undress job')
        verbose_name_plural = _('Undress jobs')

    @property
    def content(self) -> str:
        if self.need_blur:
            return self._get_content_url(self.blur_image)
        if not self.need_watermark:
            return self._get_content_url(self.without_watermark_image)
        else:
            return self._get_content_url(self.image)


class GenerateJob(ImageMixin, AbstractJob):
    image = models.ImageField(_('Image'), upload_to=PathAndRename('generate-jobs/'), null=True, blank=True)
    blur_image = models.ImageField(_('Image blur'), upload_to=PathAndRename('blur-generate-jobs/'),
                                   null=True, blank=True)
    without_watermark_image = models.ImageField(_('Without watermark image'),
                                                upload_to=PathAndRename('without-watermark-undress-jobs/'),
                                                null=True, blank=True)

    class Meta:
        verbose_name = _('Generate job')
        verbose_name_plural = _('Generate jobs')

    @property
    def content(self) -> str:
        if self.need_blur:
            return self._get_content_url(self.blur_image)
        if not self.need_watermark:
            return self._get_content_url(self.without_watermark_image)
        else:
            return self._get_content_url(self.image)


class ProxyGenerateJob(models.Model):
    """Fake generate job"""
    job = models.OneToOneField(GenerateJob, verbose_name=_('Generate job'),
                               on_delete=models.CASCADE,
                               related_name='fake_job', primary_key=True)

    status = GenerateJob.Status.PROCESS
    content = None
    user = None
    estimated_time = 60
    time_spent = 0
    need_blur = True

    class Meta:
        verbose_name = _('Fake job')
        verbose_name_plural = _('Fake jobs')

    @property
    def id(self):
        return self.job.id

    @property
    def created(self):
        return timezone.now()

    updated = created


class InstagramUndressJob(models.Model):
    class Status(models.IntegerChoices):
        CREATED = 0, _('Created')
        PROCESS = 1, _('Process')
        SUCCESS = 2, _('Success')
        ERROR = -1, _('Error')

    class DetailStatus(models.IntegerChoices):
        # Step 1
        CREATED_PARSER = 0, _('Created parser')
        PROCESS_PARSER = 1, _('Process parser')
        SUCCESS_PARSER = 2, _('Success parser')
        # Step 2
        CREATED_MAKE_MASK = 3, _('Created make mask')
        PROCESS_MAKE_MASK = 4, _('Process make mask')
        SUCCESS_MAKE_MASK = 5, _('Success make mask')
        # Step 3
        CREATED_JOB = 6, _('Created job')
        PROCESS_JOB = 7, _('Process job')
        SUCCESS_JOB = 8, _('Success job')
        # Error
        ERROR_PARSER = -9, _('Error parser')
        ERROR_MAKE_MASK = -10, _('Error make mask')
        ERROR_JOB = -11, _('Error job')
        # Expired
        EXPIRED_PARSER = -12, _('Expired parser')
        EXPIRED_MAKE_MASK = -113, _('Expired make mask')
        EXPIRED_JOB = 14, _('Expired job')

    class LinkType(models.TextChoices):
        account = 'account', _('Account')
        photo = 'photo', _('Photo')

    id = models.UUIDField(_('ID'), primary_key=True, default=uuid.uuid4)
    user_id = models.CharField(_('User ID'), max_length=10, blank=True, null=True)

    status = models.IntegerField(_('Status'), choices=Status.choices, default=Status.CREATED)
    detail_status = models.IntegerField(_('Detail status'), choices=DetailStatus.choices,
                                        default=DetailStatus.CREATED_PARSER)

    link = models.URLField(_('Account link'))
    link_type = models.CharField(_('Link type'), choices=LinkType.choices,
                                 default=LinkType.account, max_length=255)

    parser_estimated_time = models.IntegerField(_('Parser estimated time'), default=60, help_text=_('In second'))
    parser_time_spent = models.IntegerField(_('Parser time spent'), default=0, help_text=_('In seconds'))

    jobs = models.ManyToManyField(UndressJob, verbose_name=_('Jobs'))

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Created'), auto_now=True)

    _user = None

    class Meta:
        verbose_name = _('Instagram undress job')
        verbose_name_plural = _('Instagram undress jobs')

    def __str__(self):
        return f'Link: {self.link}'

    @property
    def user(self) -> User:
        if not self._user:
            self._user = get_user_by_id(user_id=self.user_id)
        return self._user

    @property
    def is_parsing(self) -> bool:
        return self.detail_status in (
            self.DetailStatus.CREATED_PARSER,
            self.DetailStatus.PROCESS_PARSER,
        )

    @property
    def is_make_mask(self) -> bool:
        return self.detail_status in (
            self.DetailStatus.CREATED_MAKE_MASK,
            self.DetailStatus.PROCESS_MAKE_MASK,
            self.DetailStatus.SUCCESS_MAKE_MASK,
        )

    @property
    def is_success_make_mask(self) -> bool:
        return self.detail_status >= self.DetailStatus.SUCCESS_MAKE_MASK

    @property
    def is_error(self) -> bool:
        return self.detail_status in (
            self.DetailStatus.ERROR_JOB,
            self.DetailStatus.ERROR_PARSER,
            self.DetailStatus.ERROR_MAKE_MASK,
        )


class InstagramSource(models.Model):
    job = models.ForeignKey(InstagramUndressJob, verbose_name=_('Job'), on_delete=models.CASCADE,
                            related_name='sources')
    image_url = models.URLField(_('Image url'))
    basic_mask = models.ImageField(_('Basic mask'), upload_to=PathAndRename('instagram-source-masks/'),
                                   default=None, blank=True, null=True)

    class Meta:
        verbose_name = _('Instagram source')
        verbose_name_plural = _('Instagram sources')

    @property
    def image_tag(self):
        return mark_safe(f'<img src="{self.image_url}" />')

    @property
    def preview_image_tag(self):
        return mark_safe(f'<img src="{self.image_url}" width="50" height="50" />')


class VideoJob(VideoMixin, AbstractJob):
    video = models.FileField(_('Vidoe'), upload_to=PathAndRename('video-jobs/'), null=True, blank=True)
    without_watermark_video = models.FileField(_('Without watermark video'),
                                               upload_to=PathAndRename('without-watermark-video-jobs/'),
                                               null=True, blank=True)
    preview = models.ImageField(_('Preview'), upload_to=PathAndRename('video-previews/'), null=True, blank=True,
                                default=None)

    need_blur = action = None

    class Meta:

        verbose_name = _('Video job')
        verbose_name_plural = _('Video jobs')

    @property
    def content(self) -> str:
        if not self.need_watermark:
            return self._get_content_url(self.without_watermark_video)
        else:
            return self._get_content_url(self.video)


class Like(models.Model):
    author = models.ForeignKey(User, verbose_name=_('Author'), on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    is_active = models.BooleanField(_('Active'), default=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Created'), auto_now=True)

    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')


class ImageGallery(ImageMixin, models.Model):
    job = models.OneToOneField(GenerateJob, verbose_name=_('Generate job'), on_delete=models.CASCADE,
                               related_name='gallery', db_index=True)

    likes = GenericRelation(Like, related_query_name='image_galley', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['job']),
        ]
        verbose_name = _('Image Gallery')
        verbose_name_plural = _('Image Gallery')

    @property
    def likes_count(self) -> int:
        return self.likes.filter(is_active=True).count()

    @property
    def image(self):
        return self.job.image

    @property
    def filter_words(self) -> str:
        return self.job.filter_words

    def get_image_url(self) -> str:
        if self.image:
            return self.image.url


class VideoGallery(VideoMixin, models.Model):
    job = models.OneToOneField(VideoJob, verbose_name=_('Video job'), on_delete=models.CASCADE,
                               related_name='gallery', db_index=True)

    likes = GenericRelation(Like, related_query_name='video_gallery', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['job']),
        ]
        verbose_name = _('Video Gallery')
        verbose_name_plural = _('Video Gallery')

    @property
    def likes_count(self) -> int:
        return self.likes.filter(is_active=True).count()

    @property
    def preview(self):
        return self.job.preview

    @property
    def video(self):
        return self.job.video

    @property
    def filter_words(self) -> str:
        return self.job.filter_words

    def get_video_url(self) -> str:
        if self.video:
            return self.video.url
