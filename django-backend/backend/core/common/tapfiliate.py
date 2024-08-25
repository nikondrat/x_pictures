import requests

from django.conf import settings

from core.common.utils import get_logger

logger = get_logger('tapfiliate')


class TapfiliateClient:
    headers = {
        'Content-Type': 'application/json',
        'Api-Key': settings.TAPFILIATE_API_KEY,
    }

    def __init__(self):
        self.session = requests.session()

    def _make_request(self, data: dict) -> dict:
        response = self.session.post(
            url='https://api.tapfiliate.com/1.6/conversions/',
            headers=self.headers,
            json=data,
        )
        response.raise_for_status()
        return response.json()

    def make_payment(self, user_id: str, payment_id: str | int, amount: float):
        try:
            self._make_request(
                data={
                    'customer_id': user_id,
                    'external_id': str(payment_id),
                    'amount': amount,
                }
            )
        except Exception as err:
            logger.error(f'Make payment: {user_id} :: Amount: {amount} :: Error: {err}')
        else:
            logger.info(f'Make payment: {user_id} :: Amount: {amount} :: Success')


client = TapfiliateClient()
