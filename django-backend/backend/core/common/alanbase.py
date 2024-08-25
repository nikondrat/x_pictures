import requests

from core.common.utils import get_logger

logger = get_logger('alanbase')


class AlanBaseClient:

    goal_url = 'https://x-pictures.postback.alanbase.com/goals/IGx30kur1R'
    event_url = 'https://x-pictures.postback.alanbase.com/events/IGx30kur1R'

    def __init__(self):
        self.session = requests.session()

    def _make_request(self, data: list) -> str:
        response = self.session.post(
            url=self.goal_url,
            json=data,
        )
        response.raise_for_status()
        return response.text

    def make_payment(self, click_id: str, amount: float, payment_id: str, **extra):
        try:
            self._make_request(
                data=[{
                    'click_id': click_id,
                    'goal': '2',
                    'value': amount,
                    'currency': 'USD',
                    'tid': payment_id,
                    'status': 'confirmed',
                    **extra,
                }]
            )
        except Exception as err:
            logger.error(f'Make payment: {click_id} :: Amount: {amount} :: Error: {err}')
        else:
            logger.info(f'Make payment: {click_id} :: Amount: {amount} :: Success')

    def make_payment_without_click_id(self, user_id: str, amount: float, payment_id: str, **extra):
        try:
            self._make_request(
                data=[{
                    'partner_id': 2,
                    'offer_id': 1,
                    'country': 'US',
                    'goal': '2',
                    'value': amount,
                    'currency': 'USD',
                    'tid': payment_id,
                    'custom1': user_id,
                    'status': 'confirmed',
                    **extra,
                }]
            )
        except Exception as err:
            logger.error(f'Make payment user: {user_id} :: Amount: {amount} :: Error: {err}')
        else:
            logger.info(f'Make payment user: {user_id} :: Amount: {amount} :: Success')

    def make_registration(self, click_id: str, user_id: str):
        try:
            self._make_request(
                data=[{
                    'click_id': click_id,
                    'goal': '1',
                    'status': 'confirmed',
                    'tid': user_id,
                }]
            )
        except Exception as err:
            logger.error(f'Make registration: {click_id} :: User ID: {user_id} :: Error: {err}')
        else:
            logger.info(f'Make registration: {click_id} :: User ID: {user_id} :: Success')

    def make_registration_without_click_id(self, user_id: str):
        return
        try:
            self._make_request(
                data=[{
                    'partner_id': 2,
                    'offer_id': 1,
                    'country': 'US',
                    'goal': '1',
                    'tid': user_id,
                    'status': 'confirmed',
                }]
            )
        except Exception as err:
            logger.error(f'Make registration User ID: {user_id} :: Error: {err}')
        else:
            logger.info(f'Make registration User ID: {user_id} :: Success')


client = AlanBaseClient()
