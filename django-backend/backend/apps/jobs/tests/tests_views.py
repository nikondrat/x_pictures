from datetime import timedelta

import pytest

from django.urls import reverse
from rest_framework import status

from apps.jobs.models import UndressJob, GenerateJob
from apps.jobs.models import Type, Tag, Category, Filter, SDModel, Action

from core.users.factories import UserFactory
from apps.profiles.factories import ProfileFactory
from apps.jobs.factories import TagFactory, CategoryFactory, FilterFactory, SDModelFactory, ActionFactory
from apps.jobs.factories import UndressJobFactory, GenerateJobFactory


@pytest.fixture(autouse=True)
def remove_0002_custom_migrations():
    Tag.objects.all().delete()
    Category.objects.all().delete()
    Filter.objects.all().delete()
    Action.objects.all().delete()
    SDModel.objects.all().delete()


@pytest.mark.django_db
class TestUndressAPIViewSet:
    raw_endpoint_get_filters = 'undress_set-get_filters'
    raw_endpoint_create = 'undress_set-list'
    raw_endpoint_retrieve = 'undress_set-detail'
    raw_endpoint_list = 'undress_set-list'

    def test_get_filter(self, api_client, get_api_client):
        from apps.jobs.config import COST_UNDRESS, COST_UNDRESS_WITHOUT_MASK

        category1 = CategoryFactory(id=1, tag=None, type=Type.undress)
        filter1 = FilterFactory(id=1, category=category1)
        filter2 = FilterFactory(id=2, category=category1)

        category2 = CategoryFactory(id=2, tag=None, type=Type.undress)
        filter3 = FilterFactory(id=3, category=category2)
        filter4 = FilterFactory(id=4, category=category2)

        response1 = get_api_client(user_id=UserFactory().id).get(reverse(self.raw_endpoint_get_filters))
        assert response1.status_code == status.HTTP_200_OK

        assert response1.json() == {
            'cost': float(COST_UNDRESS),
            'cost_without_mask': float(COST_UNDRESS_WITHOUT_MASK),
            'categories': [
                {
                    'id': category1.id,
                    'title': category1.public_name,
                    'use_many_filters': category1.use_many_filters,
                    'filters': [
                        {
                            'id': filter1.id,
                            'title': filter1.public_name,
                        },
                        {
                            'id': filter2.id,
                            'title': filter2.public_name,
                        }
                    ],
                },
                {
                    'id': category2.id,
                    'title': category2.public_name,
                    'use_many_filters': category2.use_many_filters,
                    'filters': [
                        {
                            'id': filter3.id,
                            'title': filter3.public_name,
                        },
                        {
                            'id': filter4.id,
                            'title': filter4.public_name,
                        }
                    ],
                }
            ]
        }

        response2 = api_client.get(reverse(self.raw_endpoint_get_filters))
        assert response2.status_code == status.HTTP_200_OK

        assert response2.json() == response1.json()

    @pytest.mark.parametrize('job_status, need_watermark, need_blur, has_image', (
            (UndressJob.Status.CREATED, False, True, False),
            (UndressJob.Status.CREATED, True, False, False),
            (UndressJob.Status.PROCESS, False, True, False),
            (UndressJob.Status.PROCESS, True, False, False),
            (UndressJob.Status.ERROR, False, True, False),
            (UndressJob.Status.ERROR, False, False, False),
            (UndressJob.Status.SUCCESS, False, True, True),
            (UndressJob.Status.SUCCESS, False, False, True),
            (UndressJob.Status.SUCCESS, True, False, True),
    ))
    def test_retrieve(self, job_status, need_watermark, need_blur, has_image, get_api_client, api_client):
        job = UndressJobFactory(
            status=job_status,
            need_blur=need_blur,
            need_watermark=need_watermark,
            user_id=None,
        )

        response = api_client.get(reverse(self.raw_endpoint_retrieve, kwargs={'pk': job.pk}))
        if job.status in (UndressJob.Status.CREATED,
                          UndressJob.Status.PROCESS):
            assert response.status_code == status.HTTP_201_CREATED
        else:
            assert response.status_code == status.HTTP_200_OK

        content = None
        if has_image:
            if not need_watermark:
                content = job.without_watermark_image
            elif need_blur:
                content = job.blur_image
            else:
                content = job.image

        assert response.json() == {
            'id': str(job.id),
            'status': job.status,
            'content': content,
            'estimated_time': job.estimated_time,
            'estimated_timestamp': int((job.created + timedelta(seconds=job.estimated_time)).timestamp()),
            'time_spent': job.time_spent,
            'created': job.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'updated': job.updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'is_blur': need_blur,
            'user_balance': '0.00',
        }

    def test_list(self, get_api_client, api_client):
        response = api_client.get(reverse(self.raw_endpoint_list))
        assert response.status_code == status.HTTP_403_FORBIDDEN

        user1 = UserFactory()
        ProfileFactory(owner=user1)
        user2 = UserFactory()
        ProfileFactory(owner=user2)

        UndressJobFactory(user_id=user2.pk, status=UndressJob.Status.SUCCESS, show_in_profile=True)

        response = get_api_client(user_id=user1.pk).get(reverse(self.raw_endpoint_list))
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

        job = UndressJobFactory(user_id=user1.pk, status=UndressJob.Status.SUCCESS, show_in_profile=True)

        UndressJobFactory(user_id=user1.pk, status=UndressJob.Status.CREATED, show_in_profile=True)
        UndressJobFactory(user_id=user1.pk, status=UndressJob.Status.SUCCESS, show_in_profile=False)
        UndressJobFactory(user_id=user1.pk, status=UndressJob.Status.ERROR, show_in_profile=True)

        response = get_api_client(user_id=user1.pk).get(reverse(self.raw_endpoint_list))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json() == [{
            'id': str(job.pk),
            'status': job.status,
            'content': job.content,
            'estimated_time': job.estimated_time,
            'estimated_timestamp': int((job.created + timedelta(seconds=job.estimated_time)).timestamp()),
            'time_spent': job.time_spent,
            'created': job.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'updated': job.updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'is_blur': job.need_blur,
            'user_balance': '0.00',
        }]

        for _ in range(10):
            UndressJobFactory(user_id=user1.pk, status=UndressJob.Status.SUCCESS, show_in_profile=True)

        response = get_api_client(user_id=user1.pk).get(reverse(self.raw_endpoint_list))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 10


@pytest.mark.django_db
class TestGenerateAPIViewSet:
    raw_endpoint_get_filters = 'generate_set-get_filters'
    raw_endpoint_create = 'generate_set-list'
    raw_endpoint_retrieve = 'generate_set-detail'
    raw_endpoint_list = 'generate_set-list'

    def test_get_filter(self, api_client, get_api_client):
        from apps.jobs.rest.views import GenerateAPIViewSet

        tag1 = TagFactory(id=1)
        category1 = CategoryFactory(id=1, tag=tag1, type=Type.generate)
        filter1 = FilterFactory(id=1, category=category1)

        tag2 = TagFactory(id=2)
        category2 = CategoryFactory(id=2, tag=tag2, type=Type.generate)
        filter2 = FilterFactory(id=2, category=category2)

        sd_model1 = SDModelFactory(id=2, type=Type.generate)        # Default
        action1 = ActionFactory(id=1, sd_model=sd_model1)

        sd_model2 = SDModelFactory(id=3, type=Type.generate)
        action2 = ActionFactory(id=2, sd_model=sd_model2)

        response = get_api_client(user_id=ProfileFactory().pk).get(reverse(self.raw_endpoint_get_filters))

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'cost': float(GenerateAPIViewSet.job_cost),
            'current_sd_model_id': sd_model1.id,
            'tags': [
                {
                    'id': tag1.id,
                    'title': tag1.name,
                    'categories': [{
                        'id': category1.id,
                        'title': category1.public_name,
                        'use_many_filters': category1.use_many_filters,
                        'filters': [{
                            'id':  filter1.id,
                            'title':  filter1.public_name,
                        }],
                    }],
                },
                {
                    'id': tag2.id,
                    'title': tag2.name,
                    'categories': [{
                        'id': category2.id,
                        'title': category2.public_name,
                        'use_many_filters': category2.use_many_filters,
                        'filters': [{
                            'id':  filter2.id,
                            'title':  filter2.public_name,
                        }],
                    }],
                }
            ],
            'sd_models': [
                {
                    'id': sd_model1.id,
                    'title': sd_model1.public_name,
                    'image': sd_model1.image,
                    'is_lock': False,
                    'available_in': None,
                },
                {
                    'id': sd_model2.id,
                    'title': sd_model2.public_name,
                    'image': sd_model2.image,
                    'is_lock': True,
                    'available_in': 6,
                }
            ],
            'actions': [
                {
                    'id': action1.id,
                    'title': action1.public_name,
                    'image': action1.image,
                }
            ]
        }

        response = api_client.get(reverse(self.raw_endpoint_get_filters) + f'?sd_model_id={sd_model2.id}')
        assert response.status_code == status.HTTP_200_OK

        assert response.json() == {
            'cost': float(GenerateAPIViewSet.job_cost),
            'current_sd_model_id': sd_model2.id,
            'tags': [
                {
                    'id': tag1.id,
                    'title': tag1.name,
                    'categories': [{
                        'id': category1.id,
                        'title': category1.public_name,
                        'use_many_filters': category1.use_many_filters,
                        'filters': [{
                            'id':  filter1.id,
                            'title':  filter1.public_name,
                        }],
                    }],
                },
                {
                    'id': tag2.id,
                    'title': tag2.name,
                    'categories': [{
                        'id': category2.id,
                        'title': category2.public_name,
                        'use_many_filters': category2.use_many_filters,
                        'filters': [{
                            'id':  filter2.id,
                            'title':  filter2.public_name,
                        }],
                    }],
                }
            ],
            'sd_models': [
                {
                    'id': sd_model1.id,
                    'title': sd_model1.public_name,
                    'image': sd_model1.image,
                    'is_lock': False,
                    'available_in': None,
                },
                {
                    'id': sd_model2.id,
                    'title': sd_model2.public_name,
                    'image': sd_model2.image,
                    'is_lock': True,
                    'available_in': 6,
                }
            ],
            'actions': [
                {
                    'id': action2.id,
                    'title': action2.public_name,
                    'image': action2.image,
                }
            ]
        }

    def test_list(self, get_api_client, api_client):
        response = api_client.get(reverse(self.raw_endpoint_list))
        assert response.status_code == status.HTTP_403_FORBIDDEN

        user1 = UserFactory()
        ProfileFactory(owner=user1)
        user2 = UserFactory()
        ProfileFactory(owner=user2)

        GenerateJobFactory(user_id=user2.pk, status=UndressJob.Status.SUCCESS, show_in_profile=True)

        response = get_api_client(user_id=user1.pk).get(reverse(self.raw_endpoint_list))
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

        job = GenerateJobFactory(user_id=user1.pk, status=GenerateJob.Status.SUCCESS, show_in_profile=True)

        GenerateJobFactory(user_id=user1.pk, status=GenerateJob.Status.CREATED, show_in_profile=True)
        GenerateJobFactory(user_id=user1.pk, status=GenerateJob.Status.SUCCESS, show_in_profile=False)
        GenerateJobFactory(user_id=user1.pk, status=GenerateJob.Status.ERROR, show_in_profile=True)

        response = get_api_client(user_id=user1.pk).get(reverse(self.raw_endpoint_list))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json() == [{
            'id': str(job.pk),
            'status': job.status,
            'content': job.content,
            'estimated_time': job.estimated_time,
            'estimated_timestamp': int((job.created + timedelta(seconds=job.estimated_time)).timestamp()),
            'time_spent': job.time_spent,
            'created': job.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'updated': job.updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'is_blur': job.need_blur,
            'user_balance': '0.00',
        }]

        for _ in range(10):
            GenerateJobFactory(user_id=user1.pk, status=GenerateJob.Status.SUCCESS, show_in_profile=True)

        response = get_api_client(user_id=user1.pk).get(reverse(self.raw_endpoint_list))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 10
