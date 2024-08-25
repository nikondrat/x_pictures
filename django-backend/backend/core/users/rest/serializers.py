import requests
from google.auth import transport
from google.oauth2 import id_token

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions

from core.users import models
from core.users.utils import find_user_by_email, get_user_by_email


class RegisterSerializer(serializers.Serializer):
    create = update = None

    email = serializers.EmailField(label=_('Email'))
    password = serializers.CharField(label=_('Password'))

    ip_address = serializers.IPAddressField(label=_('Ip address'), required=False)

    def validate(self, attrs):
        if find_user_by_email(email=attrs['email']):
            raise exceptions.ValidationError({
                'email': [_('A user with such an email already exists!')]
            })
        return attrs


class LoginSerializer(RegisterSerializer):
    def validate(self, attrs):
        user = get_user_by_email(email=attrs['email'])
        if not user:
            raise exceptions.ValidationError({
                '__all__': [_('Invalid username or password!')]
            })

        if not user.check_password(raw_password=attrs['password']):
            raise exceptions.ValidationError({
                'password': [_('Invalid password!')]
            })

        attrs['user'] = user
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='key')
    expires = serializers.DateTimeField()

    class Meta:
        model = models.Token
        fields = (
            'token', 'expires',
        )


class PasswordResetSerializer(serializers.Serializer):
    create = update = None
    email = serializers.EmailField()

    def validate(self, attrs):
        user = get_user_by_email(email=attrs['email'])
        if not user:
            raise exceptions.ValidationError({
                'email': [_('This email was not found in the system!')]
            })
        attrs['user'] = user
        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    create = update = None
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        message = models.EmailMessage.objects.filter(pk=attrs['token']).first()
        if (
                not message or
                message.status in (models.EmailMessage.Status.CANCEL,
                                   models.EmailMessage.Status.SUCCESS,
                                   models.EmailMessage.Status.ERROR) or
                message.type != models.EmailMessage.MessageType.password_reset
        ):
            raise exceptions.ValidationError({
                'token': _('This token has not been found!')
            })
        user = message.user
        if user.decoded_password == attrs['new_password']:
            raise exceptions.ValidationError({
                'new_password': _('The new password should not be similar to the old ones!')
            })

        attrs['user'] = user

        return attrs


class GoogleAuthSerializer(serializers.Serializer):
    create = update = None
    code = serializers.CharField()
    ip_address = serializers.IPAddressField(label=_('Ip address'), required=False)

    @classmethod
    def _google_validate_token(cls, token: str):
        try:
            id_info = id_token.verify_oauth2_token(token, request=transport.requests.Request())
            if 'accounts.google.com' in id_info['iss']:
                return id_info
            raise ValueError()
        except ValueError:
            raise exceptions.ValidationError({
                'code': [_('Invalid google token!')]
            })

    @classmethod
    def _google_validate_code(cls, code: str):
        response = requests.post(
            url='https://oauth2.googleapis.com/token',
            params={
                'code': code,
                'grant_type': 'authorization_code',
                'client_id': settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET_KEY,
                'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise exceptions.ValidationError({
                'code': [_('Invalid google code!')]
            })
        response = response.json()
        return cls._google_validate_token(
            token=response['id_token'],
        )

    def validate(self, attrs):
        result = self._google_validate_code(code=attrs['code'])
        if result['aud'] != settings.GOOGLE_CLIENT_ID:
            raise exceptions.AuthenticationFailed(detail='Invalid google client id')

        attrs['email'] = result['email']
        return attrs


class AlanBaseSerializer(serializers.Serializer):
    create = update = None

    sub_id5 = serializers.CharField(required=False)
