from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.jobs import models
from rangefilter.filters import DateTimeRangeFilterBuilder


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'preview_image_tag')
    readonly_fields = ('image_tag',)

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'is_active', 'preview_image_tag')
    list_filter = ('type', 'is_active', 'tag')
    readonly_fields = ('image_tag',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'tag'
        )

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(models.Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'is_active', 'preview_image_tag')
    list_filter = ('category', 'is_active')
    readonly_fields = ('image_tag',)
    raw_id_fields = ('category',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'category'
        )

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(models.SDModel)
class SDModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'is_active', 'preview_image_tag')
    list_filter = ('type', 'is_active')
    readonly_fields = ('image_tag',)

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(models.Action)
class ActionAdmin(admin.ModelAdmin):
    list_select_related = ('sd_model',)
    list_display = ('id', 'name', 'type', 'is_active', 'preview_image_tag')
    list_filter = ('type', 'is_active', 'sd_model')
    readonly_fields = ('image_tag',)

    def has_add_permission(self, request, obj=None):
        return False


class AbstractJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'status', 'created')
    raw_id_fields = (
        'sd_model',
    )
    search_fields = ('pk',)
    list_filter = ('status',
                   ('created', DateTimeRangeFilterBuilder(
                       title=_('Created'),
                       default_start=timezone.now() - timezone.timedelta(days=1),
                       default_end=timezone.now()
                   )))
    ordering = []
    readonly_fields = ('id', 'sd_model', 'status', 'cost', 'created', 'updated')


@admin.register(models.UndressJob)
class UndressJobAdmin(AbstractJobAdmin):
    list_display = AbstractJobAdmin.list_display + (
        'preview_image_tag',
    )
    raw_id_fields = AbstractJobAdmin.raw_id_fields + ('action',)
    readonly_fields = AbstractJobAdmin.readonly_fields + (
        'image_tag', 'action', 'created', 'updated'
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'sd_model', 'action'
        )


@admin.register(models.GenerateJob)
class GenerateJobAdmin(AbstractJobAdmin):
    list_display = AbstractJobAdmin.list_display + (
        'preview_image_tag',
    )
    raw_id_fields = AbstractJobAdmin.raw_id_fields + ('action',)
    readonly_fields = AbstractJobAdmin.readonly_fields + (
        'image_tag', 'action', 'created', 'updated'
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'sd_model', 'action'
        )


@admin.register(models.ProxyGenerateJob)
class ProxyGenerateJobAdmin(admin.ModelAdmin):
    raw_id_fields = ('job',)


class InstagramSourceInline(admin.TabularInline):
    model = models.InstagramSource
    fields = ('pk', 'preview_image_tag')
    readonly_fields = ('pk', 'preview_image_tag')
    show_change_link = True
    extra = 0


class UndressJobInline(admin.TabularInline):
    model = models.InstagramUndressJob.jobs.through
    readonly_fields = ['pk',]
    fields = ('pk',)
    show_change_link = False
    extra = 0


@admin.register(models.InstagramUndressJob)
class InstagramUndressJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'link_type', 'status', 'detail_status', 'created')
    search_fields = ('pk',)
    list_filter = ('status', 'detail_status', 'link_type',
                   ('created', DateTimeRangeFilterBuilder(
                       title=_('Created'),
                       default_start=timezone.now() - timezone.timedelta(days=1),
                       default_end=timezone.now()
                   )))
    ordering = (
        '-created',
        'status',
    )
    exclude = (
        'jobs', 'sources'
    )
    readonly_fields = ('id', 'status', 'detail_status', 'link_type', 'created', 'updated')

    inlines = (
        InstagramSourceInline,
        UndressJobInline,
    )


@admin.register(models.InstagramSource)
class InstagramSource(admin.ModelAdmin):
    list_display = ('job', 'preview_image_tag')
    readonly_fields = ('job', 'image_tag')
    search_fields = ('id', 'job_id', 'image_url')


@admin.register(models.VideoJob)
class VideoJobAdmin(admin.ModelAdmin):
    list_display = AbstractJobAdmin.list_display + (
        'preview_video_tag',
    )
    list_filter = ('status',
                   ('created', DateTimeRangeFilterBuilder(
                       title=_('Created'),
                       default_start=timezone.now() - timezone.timedelta(days=1),
                       default_end=timezone.now()
                   )))
    ordering = []
    raw_id_fields = ('sd_model',)
    readonly_fields = ('video_tag',)


@admin.register(models.ImageGallery)
class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'preview_image_tag', 'reaction',)
    search_fields = ('id', 'job__id')
    raw_id_fields = ('job',)
    list_filter = ()
    ordering = []
    readonly_fields = ('pk', 'image_tag')

    @admin.display(description='Likes')
    def reaction(self, obj: models.ImageGallery):
        return obj.likes.count()

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'job', 'job__sd_model', 'job__action'
        ).prefetch_related(
            'likes',
        )


@admin.register(models.VideoGallery)
class VideoGalleryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'preview_video_tag', 'reaction',)
    raw_id_fields = ('job',)
    search_fields = ('id', 'job__id')
    list_filter = ()
    ordering = ()
    readonly_fields = ('pk', 'video_tag')

    @admin.display(description='Likes')
    def reaction(self, obj: models.ImageGallery):
        return obj.likes.count()

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'job', 'job__sd_model',
        ).prefetch_related(
            'likes',
        )


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'created')
    raw_id_fields = ('author',)
