from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AnonymousUser

from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import get_authorization_header

from core.users.models import Token


class ApiTokenAuthentication(TokenAuthentication):
    model = Token

    def get_token_from_header(self, request: Request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return token

    def authenticate(self, request: Request):
        token = self.get_token_from_header(request=request)
        return self.authenticate_credentials(key=token)

    def authenticate_credentials(self, key: str):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if token.is_expired:
            raise exceptions.AuthenticationFailed(_('Token has expired.'))

        if not token.user:
            raise exceptions.AuthenticationFailed(_('User not found'))

        if not token.user.is_anonymous and token.user.deleted_account:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        return token.user, token


class UserOrAnonymousAuthentication(ApiTokenAuthentication):
    @classmethod
    def anonymous_credentials(cls) -> tuple[AnonymousUser, str]:
        return AnonymousUser(), 'Token anonymous'

    def authenticate(self, request: Request):
        token = self.get_token_from_header(request=request)
        if not token:
            return self.anonymous_credentials()
        return self.authenticate_credentials(key=token)
