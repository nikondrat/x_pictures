from django.contrib import admin
from django.utils.translation import gettext as _

from apps.profiles import models


class ProfileSubscriptionInline(admin.StackedInline):
    model = models.ProfileSubscription
    extra = 1
    raw_id_fields = ('subscription',)


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'type', 'balance', 'preview_image_tag')
    list_filter = ('type',)
    ordering = (
        '-balance',
        '-created',
    )
    raw_id_fields = ('owner',)
    search_fields = ('owner__id', 'owner__email')
    readonly_fields = ('pk', 'owner', 'type', 'image_tag', 'created', 'updated', 'deleted')
    exclude = ('subscriptions',)
    inlines = (ProfileSubscriptionInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'owner'
        )

    @admin.display(ordering='owner__email', description='Email')
    def email(self, obj: models.Profile):
        return obj.owner.email


@admin.register(models.ProfileSubscription)
class ProfileSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'email', 'subscription', 'is_active')
    list_filter = ('subscription',)
    raw_id_fields = ('profile',)
    search_fields = ('profile__owner__pk', 'profile__owner__email')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'profile', 'profile__owner', 'subscription',
        )

    @admin.display(ordering='profile__owner__email', description=_('Email'))
    def email(self, obj: models.ProfileSubscription):
        return obj.profile.owner.email


@admin.register(models.Patreon)
class ProfilePatreonAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'patreon_id', 'member_id')

    search_fields = ('profile__owner__pk', 'profile__owner__email')
    raw_id_fields = ('profile',)
