from django.contrib import admin

from apps.face2img import models


@admin.register(models.Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    search_fields = ['name', 'id']
    list_filter = ["is_active"]


@admin.register(models.PackImage)
class PackImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'pack', 'image', 'sort')
    search_fields = ['pack__name', "pack__id", "id"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'pack'
        )


@admin.register(models.Lora)
class LoraAdmin(admin.ModelAdmin):
    list_display = ('id', 'lora_name', 'user', 'status', 'created')
    search_fields = ['lora_name', 'id', "user__email", "user__id"]
    list_filter = ['status']
    raw_id_fields = ('user',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user'
        )


@admin.register(models.LoraTrainingFace)
class LoraTrainingFaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'lora', 'image', 'created')
    search_fields = ['lora__lora_name', 'lora__id', "id"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'lora'
        )


@admin.register(models.Face2ImgJob)
class Face2ImgJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'status', 'created')
    search_fields = ['id', "user__email", "user__id"]
    list_filter = ['status']
    raw_id_fields = ('user', 'lora', 'pack')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user'
        )


@admin.register(models.Face2ImgJobResult)
class Face2ImgJobResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'image', 'created')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'job'
        )
