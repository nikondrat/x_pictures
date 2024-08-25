from datetime import datetime

from django.core.management.base import BaseCommand

from apps.shop.models import PaymentOrder
from apps.shop.gate.base import _conversion_callback


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-s', '--start', type=str, help='start')
        parser.add_argument('-e', '--end', type=str, help='end')

    @classmethod
    def callback(cls, start: datetime, end: datetime):
        for order in PaymentOrder.objects.filter(
            status=PaymentOrder.Status.PAID,
            created__gte=start,
            updated__lte=end,
        ):
            _conversion_callback(order=order)

    def handle(self, *args, **options):
        self.callback(
            start=datetime.strptime(options.get('start'), '%Y-%m-%d %H:%M:%S'),
            end=datetime.strptime(options.get('end'), '%Y-%m-%d %H:%M:%S'),
        )
