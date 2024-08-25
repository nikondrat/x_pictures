import uuid

import pytest

from django.urls import reverse
from rest_framework import status

from apps.jobs.models import GenerateJob, ImageGallery
from apps.jobs.factories import GenerateJobFactory, ImageGalleryFactory


@pytest.mark.django_db
class TestImageGalleryAPIViewSet:
    raw_endpoint_list = 'gallery:images_set-list'
    raw_endpoint_detail = 'gallery:images_set-detail'
    raw_endpoint_filters = 'gallery:images_set-get_filters'
    raw_endpoint_reaction = 'gallery:images_set-reaction'

    def test_retrieve(self, api_client):
        response = api_client.get(reverse(self.raw_endpoint_detail,
                                          kwargs={'pk': 1}))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = api_client.get(reverse(self.raw_endpoint_detail,
                                          kwargs={'pk': str(uuid.uuid4())}))
        assert response.status_code == status.HTTP_404_NOT_FOUND

        obj = ImageGalleryFactory(job=GenerateJobFactory(
            status=GenerateJob.Status.SUCCESS,
        ))
        response = api_client.get(reverse(self.raw_endpoint_detail,
                                          kwargs={'pk': str(obj.job_id)}))

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'id': str(obj.job_id),
            'image': obj.get_image_url(),
            'prompt': obj.filter_words,
            'sd_model': {
                'id': obj.job.sd_model_id,
                'title': obj.job.sd_model.public_name,
                'image': None,
                'is_lock': False,
                'available_in': None,
            },
            'action': {
                'id': obj.job.action_id,
                'title': obj.job.action.public_name,
                'image': None,
            },
            'filter_ids': [],
            'likes': 0,
            'is_reaction': False,
            'created': obj.job.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }

    def test_get_filters(self, api_client):
        response = api_client.get(reverse(self.raw_endpoint_filters))
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('tags') is not None

    def test_reaction(self, api_client, get_api_client, user):
        obj = ImageGalleryFactory(job=GenerateJobFactory(
            status=GenerateJob.Status.SUCCESS,
        ))
        assert obj.likes_count == 0

        response = api_client.post(reverse(self.raw_endpoint_reaction, kwargs={'pk': str(obj.job_id)}))
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = get_api_client(user_id=user.pk).post(
            reverse(self.raw_endpoint_reaction, kwargs={'pk': str(uuid.uuid4())}))
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = get_api_client(user_id=user.pk).post(
            reverse(self.raw_endpoint_reaction, kwargs={'pk': str(obj.job_id)}))
        assert response.status_code == status.HTTP_201_CREATED
        after_like_response = response.json()

        assert after_like_response == {
            'id': str(obj.job_id),
            'image': obj.get_image_url(),
            'prompt': obj.filter_words,
            'sd_model': {
                'id': obj.job.sd_model_id,
                'title': obj.job.sd_model.public_name,
                'image': None,
                'is_lock': False,
                'available_in': None,
            },
            'action': {
                'id': obj.job.action_id,
                'title': obj.job.action.public_name,
                'image': None,
            },
            'filter_ids': [],
            'likes': 1,
            'is_reaction': True,
            'created': obj.job.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }

        assert ImageGallery.objects.get(pk=obj.pk).likes_count == 1

        response = get_api_client(user_id=user.pk).post(
            reverse(self.raw_endpoint_reaction, kwargs={'pk': str(obj.job_id)}))
        assert response.status_code == status.HTTP_201_CREATED

        after_dislike_response = response.json()

        assert after_dislike_response == {
            'id': str(obj.job_id),
            'image': obj.get_image_url(),
            'prompt': obj.filter_words,
            'sd_model': {
                'id': obj.job.sd_model_id,
                'title': obj.job.sd_model.public_name,
                'image': None,
                'is_lock': False,
                'available_in': None,
            },
            'action': {
                'id': obj.job.action_id,
                'title': obj.job.action.public_name,
                'image': None,
            },
            'filter_ids': [],
            'likes': 0,
            'is_reaction': False,
            'created': obj.job.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }

        assert ImageGallery.objects.get(pk=obj.pk).likes_count == 0
