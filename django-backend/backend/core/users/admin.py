import openpyxl
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext as _
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from rangefilter.filters import DateTimeRangeFilterBuilder

from core.users import models


class AlanBaseInline(admin.TabularInline):
    model = models.AlanBase
    extra = 1
    max_num = 1


class UserFromFilter(admin.SimpleListFilter):
    title = _('From')
    parameter_name = 'from'

    def lookups(self, request, model_admin):
        return [
            ('internet', _('From Internet')),
            ('alanbase', _('From Alan Base')),
        ]

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == 'alanbase':
                return queryset.filter(
                    alanbase__isnull=False,
                )
            elif self.value() == 'internet':
                return queryset.filter(
                    alanbase__isnull=True,
                )

        return queryset


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'is_staff', 'date_joined',
    )
    list_display_links = ('id', 'email')
    list_select_related = ('alanbase',)
    list_filter = (
        ('date_joined', DateTimeRangeFilterBuilder(
            title=_('Date joined'),
            default_start=timezone.now() - timezone.timedelta(days=1),
            default_end=timezone.now()
        )),
        UserFromFilter,
        'is_staff', 'deleted_account', 'email_confirmed',
        'auth_provider',
    )
    ordering = []
    search_fields = ('id', 'email', 'is_staff')
    inlines = [AlanBaseInline]

    change_list_template = 'admin/users/change_list.html'

    @classmethod
    def report_unpaid_users(cls, request: HttpRequest) -> HttpResponse:
        from apps.payments.models import Order

        wb = openpyxl.Workbook()

        ws = wb.active
        ws.title = _('Unpaid users')
        ws.append((_('ID'), _('Email'), _('Click ID'), _('Data joined')))

        for user in models.User.objects.exclude(
                orders__status=Order.Status.PAID,
                id__in=('666:672574', '1'),
        ).filter(
            email_confirmed=True,
            deleted_account=False,
        ):
            ws.append((user.pk, user.email, user.click_id, str(user.date_joined.date())))

        response = HttpResponse(content_type='application/vnd.ms-excel')
        wb.save(response)
        filename = 'attachment; filename=%s' % f'unpaid-users-{int(timezone.now().timestamp())}.xlsx'
        response['Content-Disposition'] = filename

        return response

    def get_urls(self):
        from django.urls import re_path

        return super().get_urls() + [
            re_path(r'^report/unpaid-users$', self.report_unpaid_users)
        ]


@admin.register(models.EmailMessage)
class EmailMessageAdmin(admin.ModelAdmin):
    list_display = (
        'key', 'user_id',
        'type', 'status',
    )
    list_filter = (
        'status',
    )
    search_fields = (
        'key', 'user_id',
        'type', 'status'
    )


@admin.register(models.Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = (
        'user_id', 'created',
    )
    search_fields = ('user_id', 'key')
