import json
from typing import Optional

import requests
from celery import shared_task

from core.common.utils import get_logger

logger = get_logger('telegram:tasks')


@shared_task(name='telegram:send-text-message:task')
def send_text_message_task(telegram_token: str, chat_ids: list[int], text: str,
                           keyboard: Optional[dict] = None, parse_mode: str = 'html'):
    reply_markup = json.dumps(keyboard)
    for chat_id in chat_ids:
        response = requests.get(
            url=f'https://api.telegram.org/bot{telegram_token}/sendMessage',
            params={
                'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'reply_markup': reply_markup,
            },
        )
        if response.ok:
            logger.info('Telegram send text message: SUCCESS')
        else:
            logger.info(f'Telegram send text message: ERROR :: Response: {response.text}')

    return True
