import decimal
import uuid

import pytest

from django.urls import reverse
from django.conf import settings
from rest_framework import status

from core.users.models import User, Token, EmailMessage, AlanBase
from apps.profiles.models import ProfileType
from apps.jobs.models import GenerateJob, UndressJob, Type as JobType
from core.users.factories import UserFactory, EmailMessageFactory, AlanBaseFactory
from apps.jobs.factories import GenerateJobFactory, UndressJobFactory


@pytest.mark.django_db
class TestRegisterAPIView:
    endpoint = reverse('register')

    @pytest.mark.parametrize('click_id, job_type', [
        (None, None),
        (None, JobType.generate),
        (None, JobType.undress),
        (uuid.uuid4(), None),
        (uuid.uuid4(), JobType.generate),
        (uuid.uuid4(), JobType.undress),
    ])
    def test_register__success(self, click_id, job_type, api_client, faker, mocker):
        email = faker.unique.email()
        password = faker.unique.password()

        def mock_send_task(name: str, kwargs):
            assert name == 'users:send_email_task'
            message = EmailMessage.objects.get(pk=kwargs['email_message_id'])
            assert message.status == EmailMessage.Status.CREATE
            assert message.type == EmailMessage.MessageType.verification
            assert message.user.email == email

        mocker.patch(
            'core.users.rest.views.RegisterAPIView.post_registration',
            return_value=None,
        )

        mocker.patch(
            'core.users.services.current_app.send_task',
            new=mock_send_task
        )

        endpoint = self.endpoint
        if click_id:
            endpoint += f'?click_id={click_id}'

        job = None
        if job_type == JobType.generate:
            job = GenerateJobFactory(user_id=None, status=GenerateJob.Status.SUCCESS, need_blur=True)
            endpoint += f'?generate_job_id={job.pk}' if not click_id else f'&generate_job_id={job.pk}'
        elif job_type == JobType.generate:
            job = UndressJobFactory(user_id=None, status=UndressJob.Status.SUCCESS, need_blur=True)
            endpoint += f'?undress_job_id={job.pk}' if not click_id else f'&undress_job_id={job.pk}'

        response = api_client.post(endpoint, data={
            'email': email,
            'password': password,
        })

        assert response.status_code == status.HTTP_200_OK

        assert set(response.json().keys()) == {'token', 'expires'}

        user = Token.objects.get(key=response.json()['token']).user
        assert user.email == email
        assert user.decoded_password == password
        assert user.auth_provider == User.AuthProvider.email

        assert user.profile is not None
        assert user.profile.type == ProfileType.basic
        assert user.profile.balance == decimal.Decimal('25.0')

        if click_id:
            assert user.click_id == str(click_id)

        if job and job_type == JobType.generate:
            updated_job = GenerateJob.objects.get(pk=job.pk)
            assert not updated_job.need_blur
            assert updated_job.user == user
        elif job and job_type == JobType.undress:
            updated_job = UndressJob.objects.get(pk=job.pk)
            assert not updated_job.need_blur
            assert updated_job.user == user

    def test_register__duplicate_email(self, api_client, faker):
        user = UserFactory()
        response = api_client.post(self.endpoint, data={
            'email': user.email,
            'password': faker.unique.password(),
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLoginAPIView:
    endpoint = reverse('login')

    def test_login__success(self, api_client):
        user = UserFactory()

        response = api_client.post(self.endpoint, data={
            'email': user.email,
            'password': user.decoded_password,
        })

        assert response.status_code == status.HTTP_200_OK
        assert set(response.json().keys()) == {'token', 'expires'}

        assert Token.objects.get(key=response.json()['token']).user == user

    def test_login__invalid_email(self, api_client, faker):
        response = api_client.post(self.endpoint, data={
            'email': faker.unique.email(),
            'password': faker.unique.password(),
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login__invalid_password(self, api_client, faker):
        user = UserFactory()
        response = api_client.post(self.endpoint, data={
            'email': user.email,
            'password': faker.unique.password(),
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_verification_view(api_client, user):
    assert user.profile.balance == 20

    message = EmailMessageFactory(
        user_id=user.pk,
        type=EmailMessage.MessageType.verification,
        status=EmailMessage.Status.SENT,
    )

    response = api_client.get(reverse('verification', kwargs={'token': message.key}))
    assert response.status_code == status.HTTP_302_FOUND

    assert EmailMessage.objects.get(pk=message.pk).status == EmailMessage.Status.SUCCESS

    assert User.objects.get(pk=user.pk).profile.balance == decimal.Decimal('40')


@pytest.mark.django_db
def test_refresh_verification_view(get_api_client, mocker):
    user = UserFactory(email_confirmed=False)

    message = EmailMessageFactory(
        user_id=user.pk,
        type=EmailMessage.MessageType.verification,
        status=EmailMessage.Status.SENT,
    )

    def mock_send_task(name: str, kwargs):
        assert name == 'users:send_email_task'
        msg = EmailMessage.objects.get(pk=kwargs['email_message_id'])
        assert msg != message
        assert msg.status == EmailMessage.Status.CREATE
        assert msg.type == EmailMessage.MessageType.verification
        assert msg.user.email == user.email

    mocker.patch(
        'core.users.services.current_app.send_task',
        new=mock_send_task
    )

    response = get_api_client(user_id=user.pk).post(reverse('refresh_verification'))
    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert EmailMessage.objects.get(pk=message.pk).status == EmailMessage.Status.CANCEL


@pytest.mark.django_db
class TestPasswordResetAPIViewSet:
    endpoint_password_reset_send = reverse('password_reset_set-send')
    endpoint_password_reset_set = reverse('password_reset_set-set')

    def test_send_message__error(self, api_client, faker):
        response = api_client.post(self.endpoint_password_reset_send,
                                   data={
                                       'email': faker.unique.email(),
                                   })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_send_message__success(self, api_client, mocker):
        user = UserFactory()

        def mock_send_task(name: str, kwargs):
            assert name == 'users:send_email_task'
            msg = EmailMessage.objects.get(pk=kwargs['email_message_id'])
            assert msg.status == EmailMessage.Status.CREATE
            assert msg.type == EmailMessage.MessageType.password_reset
            assert msg.user.email == user.email

        mocker.patch(
            'core.users.services.current_app.send_task',
            new=mock_send_task
        )

        response = api_client.post(self.endpoint_password_reset_send,
                                   data={
                                       'email': user.email,
                                   })
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_set_new_password__not_found(self, api_client, faker):
        response = api_client.post(self.endpoint_password_reset_set, data={
            'token': 'fake-token',
            'new_password': faker.unique.password(),
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize('message_status, message_type', [
        (EmailMessage.Status.CANCEL, EmailMessage.MessageType.password_reset),
        (EmailMessage.Status.SUCCESS, EmailMessage.MessageType.password_reset),
        (EmailMessage.Status.ERROR, EmailMessage.MessageType.password_reset),
        (EmailMessage.Status.SENT, EmailMessage.MessageType.verification),
        (EmailMessage.Status.CREATE, EmailMessage.MessageType.verification),
    ])
    def test_set_new_password__400(self, message_status, message_type, api_client, faker):
        message = EmailMessageFactory(
            status=message_status,
            type=message_type,
        )
        response = api_client.post(self.endpoint_password_reset_set, data={
            'token': message.key,
            'new_password': faker.unique.password(),
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize('message_status, message_type', [
        (EmailMessage.Status.SENT, EmailMessage.MessageType.password_reset),
        (EmailMessage.Status.CREATE, EmailMessage.MessageType.password_reset),
    ])
    def test_set_new_password__incorrect_password(self, message_status, message_type, api_client, faker):
        user = UserFactory()
        message = EmailMessageFactory(
            status=message_status,
            type=message_type,
            user_id=user.pk,
        )
        response = api_client.post(self.endpoint_password_reset_set, data={
            'token': message.key,
            'new_password': user.decoded_password,
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize('message_status, message_type', [
        (EmailMessage.Status.SENT, EmailMessage.MessageType.password_reset),
        (EmailMessage.Status.CREATE, EmailMessage.MessageType.password_reset),
    ])
    def test_set_new_password__success(self, message_status, message_type, api_client, faker):
        user = UserFactory()
        message = EmailMessageFactory(
            status=message_status,
            type=message_type,
            user_id=user.pk,
        )
        new_password = faker.unique.password()

        assert user.decoded_password != new_password

        response = api_client.post(self.endpoint_password_reset_set, data={
            'token': message.key,
            'new_password': new_password,
        })
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert EmailMessage.objects.get(pk=message.pk).status == EmailMessage.Status.SUCCESS
        assert User.objects.get(pk=user.pk).decoded_password == new_password


@pytest.mark.django_db
class TestSocialMediaAuthAPIViewSet:
    endpoint_google_auth = reverse('social_media_set-google_auth')

    @pytest.mark.parametrize('click_id', [
        None, uuid.uuid4()
    ])
    def test_google_auth__register(self, click_id, api_client, faker, mocker):
        email = faker.unique.email()
        fake_code = 'fake-code'

        def mock_google_validate_code(_, code: str):
            assert code == fake_code
            return {'email': email, 'aud': settings.GOOGLE_CLIENT_ID}

        mocker.patch(
            'core.users.rest.serializers.GoogleAuthSerializer._google_validate_code',
            new=mock_google_validate_code
        )

        mocker.patch(
            'core.users.rest.views.SocialMediaAuthAPIViewSet.post_registration',
            return_value=None,
        )

        response = api_client.post(
            self.endpoint_google_auth,
            data={
                'code': fake_code,
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert set(response.json().keys()) == {'token', 'expires'}

        user = Token.objects.get(key=response.json()['token']).user
        assert user.email == email
        assert user.decoded_password == settings.SOCIAL_SECRET
        assert user.auth_provider == User.AuthProvider.google

    @pytest.mark.parametrize('click_id, has_click_id', [
        (uuid.uuid4(), True),
        (None, False),
        (None, True),
    ])
    def test_google_auth__success(self, click_id, has_click_id, api_client, faker, mocker):
        user = UserFactory(auth_provider=User.AuthProvider.google)

        if has_click_id:
            AlanBaseFactory(user=user)
        else:
            AlanBaseFactory(user=user, click_id=None)

        fake_code = 'fake_code'

        def mock_google_validate_code(_, code: str):
            assert code == fake_code
            return {'email': user.email, 'aud': settings.GOOGLE_CLIENT_ID}

        mocker.patch(
            'core.users.rest.serializers.GoogleAuthSerializer._google_validate_code',
            new=mock_google_validate_code
        )

        mocker.patch(
            'core.users.rest.views.SocialMediaAuthAPIViewSet.post_registration',
            return_value=None,
        )

        endpoint_google_auth = self.endpoint_google_auth
        if click_id:
            endpoint_google_auth += f'?click_id={click_id}'

        response = api_client.post(
            endpoint_google_auth,
            data={
                'code': fake_code,
            }
        )

        token_user = Token.objects.get(key=response.json()['token']).user
        assert token_user == user

        if has_click_id:
            assert user.click_id != click_id
        else:
            assert user.click_id == (str(click_id) if click_id else click_id)


@pytest.mark.django_db
class TestMarketingAPIViewSet:
    endpoint_alanbase = reverse('marketing_set-alanbase')

    @pytest.mark.parametrize('has_alanbase', (
        True, False
    ))
    def test_alanbase(self, has_alanbase, get_api_client):
        user = UserFactory()
        fake_sub_id5 = 'sub_id5'

        alanbase = None
        if has_alanbase:
            alanbase = AlanBaseFactory(user=user)

        response = get_api_client(user_id=user.pk).patch(self.endpoint_alanbase,
                                                         data={
                                                             'sub_id5': fake_sub_id5
                                                         })

        assert response.status_code == status.HTTP_204_NO_CONTENT

        ab = AlanBase.objects.get(user=user)
        assert ab.sub_id5 == fake_sub_id5
        if alanbase:
            assert ab.sub_id5 != alanbase.sub_id5
            assert ab.click_id == alanbase.click_id
