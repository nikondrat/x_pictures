import pytest

from django.urls import reverse
from rest_framework import status

from core.users.models import User
from core.users.factories import UserFactory
from apps.profiles.models import Profile, ProfileType
from apps.jobs.models import GenerateJob
from apps.jobs.factories import GenerateJobFactory, ActionFactory, SDModelFactory, ImageGalleryFactory
from apps.profiles.factories import ProfileFactory, ProfileSubscriptionFactory


@pytest.mark.django_db
class TestProfileAPIViewSet:
    endpoint_me = reverse('profile_set-me')
    endpoint_upload_image = reverse('profile_set-upload_image')
    endpoint_delete_account = reverse('profile_set-delete_account')
    endpoint_change_password = reverse('profile_set-change_password')
    endpoint_image_storage = reverse('profile_set-image_storage')
    raw_endpoint_delete_image_from_storage = 'profile_set-delete_image_from_storage'
    raw_endpoint_liked_image_from_storage = 'liked_image_storage_set-list'

    def tests_me_without_subscription(self, get_api_client):
        profile = ProfileFactory()

        response = get_api_client(user_id=profile.pk).get(self.endpoint_me)
        assert response.status_code == status.HTTP_200_OK

        assert response.json() == {
            'id': profile.pk,
            'image': None,
            'balance': '0.00',
            'type': ProfileType.basic,
            'type_verbose': ProfileType.basic.label,
            'email': profile.owner.email,
            'username': profile.owner.username,
            'is_verified': profile.owner.is_verified,
            'subscription': None,
            'created': profile.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'updated': profile.updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }

    @pytest.mark.parametrize('subscription_id, profile_type', [
        (1, ProfileType.advance),
        (2, ProfileType.advance),
        (3, ProfileType.premium),
        (4, ProfileType.premium),
        (5, ProfileType.super_premium),
    ])
    def tests_me_with_subscription(self, subscription_id: int, profile_type: ProfileType, get_api_client):
        profile = ProfileFactory()
        profile_subscription = ProfileSubscriptionFactory(
            subscription_id=subscription_id,
            profile=profile
        )

        response = get_api_client(user_id=profile.pk).get(self.endpoint_me)
        assert response.status_code == status.HTTP_200_OK

        assert response.json() == {
            'id': profile.pk,
            'image': None,
            'balance': '%.2f' % profile_subscription.subscription.amount,
            'type': profile_type,
            'type_verbose': profile_type.label,
            'email': profile.owner.email,
            'username': profile.owner.username,
            'is_verified': profile.owner.is_verified,
            'subscription': {
                'id': subscription_id,
                'title': profile_subscription.subscription.public_title,
                'is_active': True,
                'start_period': profile_subscription.start_period.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'end_period': profile_subscription.end_period.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            },
            'created': profile.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'updated': profile.updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }

        profile_subscription.is_active = False
        profile_subscription.save()

        response = get_api_client(user_id=profile.pk).get(self.endpoint_me)
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data['subscription'] is None
        assert response_data['type'] == ProfileType.basic

    @pytest.mark.skip()
    def test_upload_image(self, get_api_client):
        import tempfile
        from PIL import Image

        profile = ProfileFactory()
        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        response = get_api_client(user_id=profile.pk).post(self.endpoint_upload_image,
                                                           data={'image': tmp_file})

        assert response.status_code == status.HTTP_201_CREATED
        profile = Profile.objects.get(pk=profile.pk)
        assert response.json() == {
            'id': profile.pk,
            'image': profile.image.url,
            'balance': '0.00',
            'type': ProfileType.basic,
            'type_verbose': ProfileType.basic.label,
            'email': profile.owner.email,
            'username': profile.owner.username,
            'is_verified': profile.owner.is_verified,
            'subscription': None,
            'created': profile.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'updated': profile.updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        profile.delete()

    def test_delete_account(self, get_api_client):
        profile = ProfileFactory()
        response = get_api_client(user_id=profile.owner_id).delete(self.endpoint_delete_account)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Profile.objects.filter(pk=profile.pk).exists()
        assert Profile.objects_with_deleted.get(pk=profile.pk).deleted is not None

    @pytest.mark.parametrize('password, new_password, sent_password, status_code, result_password', (
            ('test', 'test2', 'test', status.HTTP_201_CREATED, 'test2'),
            ('test', 'test2', 'test1', status.HTTP_400_BAD_REQUEST, 'test'),
    ))
    def test_change_password(self, password: str, new_password: str, sent_password: str,
                             status_code: int, result_password: str, get_api_client):
        user = UserFactory(decoded_password=password)
        profile = ProfileFactory(owner=user)
        response = get_api_client(user_id=profile.owner_id).patch(self.endpoint_change_password,
                                                                  data={
                                                                      'password': sent_password,
                                                                      'new_password': new_password,
                                                                  })
        assert response.status_code == status_code
        assert User.objects.get(pk=user.pk).decoded_password == result_password

    @pytest.mark.parametrize('profile_type, img_count, result_img_count', [
        (ProfileType.basic, 20, 5),
        (ProfileType.advance, 30, 10),
        (ProfileType.premium, 150, 100),
        (ProfileType.super_premium, 100, 300),
    ])
    def test_image_storage(self, profile_type: ProfileType, img_count: int, result_img_count: int, get_api_client):
        profile = ProfileFactory(type=profile_type)
        action = ActionFactory(pk=1555)
        sd_model = SDModelFactory(pk=1224)
        for _ in range(img_count):
            GenerateJobFactory(user_id=profile.owner_id, action=action, sd_model=sd_model,
                               status=GenerateJob.Status.SUCCESS, show_in_profile=True)

        for _ in range(10):
            GenerateJobFactory(user_id=profile.owner_id, action=action, sd_model=sd_model,
                               status=GenerateJob.Status.SUCCESS, show_in_profile=False)

        response = get_api_client(user_id=profile.owner_id).get(self.endpoint_image_storage)
        assert response.status_code == status.HTTP_200_OK

        response = response.json()
        assert response['generation_count'] == img_count + 10
        assert response['count'] <= result_img_count
        print(response['results'][0].keys())
        assert set(response['results'][0].keys()) == {'id', 'content', 'sd_model_name',
                                                      'likes', 'is_reaction', 'action_name',
                                                      'filter_words', 'created'}

    def test_delete_image_from_storage(self, get_api_client):
        profile = ProfileFactory()
        action = ActionFactory()
        sd_model = SDModelFactory()

        job = GenerateJobFactory(user_id=profile.owner_id, action=action, sd_model=sd_model,
                                 status=GenerateJob.Status.SUCCESS, show_in_profile=True)

        endpoint = reverse(self.raw_endpoint_delete_image_from_storage, kwargs={'pk': job.id})

        response = get_api_client(user_id=profile.owner_id).delete(endpoint)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not GenerateJob.objects.get(pk=job.pk).show_in_profile

    @pytest.mark.skip('--')
    def test_liked_image_storage(self, get_api_client, user):
        obj1 = ImageGalleryFactory(
            job=GenerateJobFactory(
                status=GenerateJob.Status.SUCCESS,
            )
        )
        ImageGalleryFactory(
            job=GenerateJobFactory(
                status=GenerateJob.Status.SUCCESS,
            )
        )

        response = get_api_client(user_id=user.pk).get(reverse(self.raw_endpoint_liked_image_from_storage))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['results'] == []

        like = obj1.likes.create(author=user)

        response = get_api_client(user_id=user.pk).get(reverse(self.raw_endpoint_liked_image_from_storage))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['results'] == [{
            'id': str(obj1.job_id),
            'content': obj1.image,
            'likes': 1,
            'is_reaction': True,
        }]

        like.is_active = False
        like.save()

        response = get_api_client(user_id=user.pk).get(reverse(self.raw_endpoint_liked_image_from_storage))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['results'] == []
