import hmac
import json
import hashlib
from urllib.parse import urljoin

from django.conf import settings
from rest_framework.request import Request
from rest_framework.permissions import BasePermission


class IvendPayApiKeyPermission(BasePermission):
    def has_permission(self, request: Request, view):
        return request.META.get('HTTP_X_API_KEY') == settings.IVENDPAY_API_KEY


class PayAdmitSignaturePermission(BasePermission):
    def has_permission(self, request: Request, view):
        if request.META.get('HTTP_SIGNATURE') is None:
            return False
        signature = hmac.new(settings.PAYADMIT_SIGNING_KEY.encode(), request.body, hashlib.sha256).hexdigest()
        return request.META['HTTP_SIGNATURE'] == signature


class OnlyWithSubscriptionPermission(BasePermission):
    def has_permission(self, request: Request, view):
        return (
            not request.user.profile.is_free and
            request.user.profile.subscriptions.filter(is_active=True).exists()
        )


class ArkPayWebhookSignaturePermission(BasePermission):

    @classmethod
    def is_signature_valid(cls, signature: str, data: dict):
        from apps.shop.gate.ark_pay import check_signature
        return check_signature(
            method='POST',
            uri=urljoin(settings.DOMAIN, '/api/shop/webhook/ark-pay/'),
            body=json.dumps(data, separators=(',', ':')),
            # body=json.dumps(data),
            secret_key=settings.ARK_PAY_SECRET_KEY,
            received_signature=signature,
        )

    def has_permission(self, request: Request, view):
        return (
                request.META.get('HTTP_SIGNATURE') and
                self.is_signature_valid(signature=request.META['HTTP_SIGNATURE'], data=request.data)
        )
