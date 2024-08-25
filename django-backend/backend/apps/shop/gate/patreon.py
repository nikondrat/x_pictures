import time
import hashlib
from typing import Optional
from urllib.parse import urljoin
from datetime import datetime, timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from core.common.utils import get_logger
from core.users.models import User
from apps.shop.gate.base import BaseGate, log
from apps.shop.models import Product, Currency, GatewayType, PaymentOrder, PaymentOrderLog

from apps.profiles.models import Profile, Patreon

logger = get_logger("patreon:orders")


def get_patreon_owner_campaign() -> Patreon:
    return Patreon.objects.get(profile__owner__id='000:000000')


class PaymentGate(BaseGate):
    endpoint_url = 'https://www.patreon.com/'
    gateway_type = GatewayType.patreon

    @classmethod
    def is_first_payment_order_in_patreon(cls, profile: Profile) -> bool:
        last_payment_order = PaymentOrder.objects.filter(
            gateway_type=cls.gateway_type,
            status=PaymentOrder.Status.PAID,
            user_id=profile.owner_id,
        ).first()
        return last_payment_order is None

    @classmethod
    def search(cls, patreon: Patreon, data: list[dict] = None):
        from apps.profiles.utils import has_active_subscription

        if not data:
            data = cls.get_patreon_campaign_info()

        for row in data:
            if (
                    str(patreon.member_id) == row.get('id')
                    and row.get('attributes', {}).get('last_charge_status') == 'Paid'
            ):
                last_charge_date = datetime.fromisoformat(row['attributes']['last_charge_date'])
                last_charge_date = datetime(
                    year=last_charge_date.year,
                    month=last_charge_date.month,
                    day=last_charge_date.day,
                    hour=last_charge_date.hour,
                    minute=last_charge_date.minute,
                    second=last_charge_date.second,
                )

                for currently_entitled_tier in row['relationships']['currently_entitled_tiers']['data']:
                    subscription_id = currently_entitled_tier["id"]

                    product: Product = Product.objects.filter(patreon_product_id=subscription_id).first()

                    if not product:
                        continue

                    if product.is_subscription and last_charge_date >= datetime.now() + product.td_lifetime:
                        continue

                    if product.is_subscription and has_active_subscription(profile=patreon.profile):
                        continue

                    invoice_id = cls.generate_invoice_id(
                        patreon_id=patreon.pk,
                        profile_id=patreon.profile_id,
                        product_id=product.id,
                        last_charge_date=last_charge_date
                    )

                    if PaymentOrder.objects.filter(invoice_id=invoice_id).exists():
                        continue

                    return cls.create(
                        invoice_id=invoice_id,
                        user=patreon.profile.owner,
                        product=product,
                        currency=Currency.USD,
                    )

    @classmethod
    def search_v2(cls, members: list[Patreon], data: list[dict] = None):
        from apps.profiles.utils import has_active_subscription

        if not data:
            data = cls.get_patreon_campaign_info()

        members_structure = {
            str(member.member_id): member
            for member in members
        }

        for row in data:
            if (
                    members_structure.get(row.get('id')) and
                    row.get('attributes', {}).get('last_charge_status') == 'Paid'
            ):
                patreon: Patreon = members_structure[row.get('id')]

                last_charge_date = datetime.fromisoformat(row['attributes']['last_charge_date'])
                last_charge_date = datetime(
                    year=last_charge_date.year,
                    month=last_charge_date.month,
                    day=last_charge_date.day,
                    hour=last_charge_date.hour,
                    minute=last_charge_date.minute,
                    second=last_charge_date.second,
                )

                for currently_entitled_tier in row['relationships']['currently_entitled_tiers']['data']:
                    subscription_id = currently_entitled_tier["id"]

                    product: Product = Product.objects.filter(patreon_product_id=subscription_id).first()

                    if not product:
                        continue

                    if product.is_subscription and last_charge_date >= datetime.now() + product.td_lifetime:
                        continue

                    if product.is_subscription and has_active_subscription(profile=patreon.profile):
                        continue

                    invoice_id = cls.generate_invoice_id(
                        patreon_id=patreon.pk,
                        profile_id=patreon.profile_id,
                        product_id=product.id,
                        last_charge_date=last_charge_date
                    )

                    if PaymentOrder.objects.filter(invoice_id=invoice_id).exists():
                        continue

                    try:
                        if cls.is_first_payment_order_in_patreon(profile=patreon.profile):
                            cls.create(
                                invoice_id=invoice_id,
                                user=patreon.profile.owner,
                                product=product,
                                currency=Currency.USD,
                            )
                        else:
                            cls.create(
                                invoice_id=invoice_id,
                                user=patreon.profile.owner,
                                product=product,
                                currency=Currency.USD,
                                is_conversion_callback=False,
                            )
                    except Exception as err:
                        logger.error(f"Error: {err}")
                        continue

    @classmethod
    def generate_invoice_id(cls, patreon_id: int, profile_id, product_id: int, last_charge_date: datetime) -> str:
        string = f'{patreon_id}:{profile_id}:{product_id}:{last_charge_date.date()}'
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    @classmethod
    @transaction.atomic()
    def refresh_token_by_patreon(cls, patreon: Patreon):
        response = cls.make_request(
            method='POST',
            url=urljoin(cls.endpoint_url, '/api/oauth2/token'),
            params={
                'grant_type': 'refresh_token',
                'refresh_token': patreon.refresh_token,
                'client_id': settings.PATREON_CLIENT_ID,
                'client_secret': settings.PATREON_CLIENT_SECRET_KEY,
            }
        )
        patreon.access_token = response['access_token']
        patreon.refresh_token = response['refresh_token']
        patreon.expires_in = timezone.now() + timedelta(seconds=response['expires_in'])
        patreon.token_type = response['token_type']
        patreon.save()
        return patreon

    @classmethod
    def get_patreon_campaign_info(cls) -> list:
        owner_campaign = get_patreon_owner_campaign()
        if owner_campaign.is_expired:
            owner_campaign = cls.refresh_token_by_patreon(patreon=owner_campaign)

        url = (f'https://www.patreon.com/api/oauth2/v2/campaigns/{settings.PATREON_CAMPAIGN_ID}/members'
               '?include=currently_entitled_tiers,address'
               '&fields%5Bmember%5D=full_name,is_follower,last_charge_date,last_charge_status,'
               'lifetime_support_cents,currently_entitled_amount_cents,patron_status,email'
               '&fields%5Btier%5D=amount_cents,created_at,description,discord_role_ids,edited_at,'
               'patron_count,published,published_at,requires_shipping,title,url'
               '&fields%5Baddress%5D=addressee,city,line_1,line_2,phone_number,postal_code,state')

        data = []
        while True:
            response = cls.make_request(
                method='GET',
                url=url,
                headers={'Authorization': owner_campaign.auth_token},
            )

            data.extend(response.get('data', []))

            if response.get('meta', {}).get('pagination', {}).get('cursors', {}).get('next') is None:
                break

            url = response['links']['next']
            time.sleep(0.2)

        return data

    @classmethod
    def get_patreon_info_by_code(cls, code: str) -> dict:
        response = cls.make_request(
            method='POST',
            url=urljoin(cls.endpoint_url, '/api/oauth2/token'),
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            params={
                'code': code,
                'grant_type': 'authorization_code',
                'client_id': settings.PATREON_CLIENT_ID,
                'client_secret': settings.PATREON_CLIENT_SECRET_KEY,
                'redirect_uri': settings.PATREON_REDIRECT_URI,
            },
        )

        return {
            'access_token': response['access_token'],
            'refresh_token': response['refresh_token'],
            'expires_in': response['expires_in'],
            'scope': response['scope'],
            'token_type': response['token_type'],
        }

    @classmethod
    def get_patreon_account_info_by_patreon(cls, patreon: Patreon):
        response = cls.make_request(
            method='GET',
            url=('https://www.patreon.com/api/oauth2/v2/identity?include=memberships.campaign'
                 '&fields%5Bmember%5D=currently_entitled_amount_cents,lifetime_support_cents,'
                 'campaign_lifetime_support_cents,last_charge_status,patron_status,last_charge_date,'
                 'pledge_relationship_start'),
            headers={
                'Authorization': patreon.auth_token,
            },
        )

        member_id = None
        for data in response.get('included', []):
            if (
                    data.get('type') == 'member' and
                    int(data.get('relationships', {})
                                .get('campaign', {})
                                .get('data', {})
                                .get('id', '0')) == settings.PATREON_CAMPAIGN_ID
            ):
                member_id = data['id']
                break

        return {
            'patreon_id': response['data']['id'],
            'member_id': member_id,
        }

    @classmethod
    def activate_patreon(cls, patreon: Patreon) -> tuple[Optional[Patreon], bool]:
        try:
            info = cls.get_patreon_account_info_by_patreon(patreon=patreon)
        except Exception:
            patreon.delete()
            return None, False

        if patreon.patreon_id is None:
            if Patreon.objects.filter(patreon_id=info['patreon_id']).exists():
                patreon.delete()
                return None, False
            patreon.patreon_id = info['patreon_id']
            patreon.save()

        if not info.get('member_id'):
            return patreon, False

        if Patreon.objects.filter(member_id=info['member_id']).exists():
            patreon.delete()
            return None, False

        patreon.member_id = info['member_id']
        patreon.save()

        return patreon, True

    @classmethod
    @transaction.atomic()
    def create(cls, user: User, product: Product, currency: Currency, **options) -> PaymentOrder:
        price = product.get_price_by_currency(currency=currency)
        order = cls.model.objects.create(
            invoice_id=options['invoice_id'],
            payment_url=None,
            user=user,
            gateway_type=cls.gateway_type,
            product=product,
            price=price,
            currency=currency,
            from_shop=options.get('from_shop', False),
            status=PaymentOrder.Status.PAID,
        )
        log(order=order,
            action=PaymentOrderLog.Action.INFO,
            text='Create order')

        cls.after_paid(
            order=order,
            profile=order.user.profile,
            is_conversion_callback=options.get("is_conversion_callback", True),
        )

        return order
