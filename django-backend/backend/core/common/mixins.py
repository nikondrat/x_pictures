import re

from django.db import models
from django.utils.html import mark_safe


class DatetimeMixin:
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class ByUserEmailSearchMixin:
    email_regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request=request, queryset=queryset, search_term=search_term)

        if re.match(self.email_regex, search_term.strip()):
            from core.users.models import User
            queryset |= self.model.objects.filter(
                user_id__in=User.objects.filter(email=search_term.strip()).values_list('pk', flat=True),
            )

        return queryset, use_distinct


class ImageMixin:
    @property
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" />')

    @property
    def preview_image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')


class VideoMixin:
    @property
    def video_tag(self):
        if self.video:
            template = (
                '<video controls>\n'
                f'<source src="{self.video.url}" type="video/mp4">\n'
                '</video>'
            )
            return mark_safe(template)

    @property
    def preview_video_tag(self):
        if self.preview:
            return mark_safe(f'<img src="{self.preview.url}" width="50" height="50" />')
        elif self.video:
            template = (
                '<video width="50" height="50" controls>\n'
                f'<source src="{self.video.url}" type="video/mp4">\n'
                '</video>'
            )
            return mark_safe(template)
