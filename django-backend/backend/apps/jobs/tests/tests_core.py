import decimal
import uuid
from urllib.parse import urljoin

import pytest

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import ValidationError, APIException

from apps.profiles.models import ProfileType, Profile
from apps.profiles.factories import ProfileFactory
from apps.jobs.models import Filter, UndressJob, GenerateJob, InstagramUndressJob, InstagramSource, VideoJob

from apps.jobs.core import UndressService, GenerateService, InstagramUndressService, VideoService


@pytest.mark.django_db
class TestUndressService:

    @pytest.mark.parametrize('profile_type, balance, need_blur, need_watermark, estimated_time, priority, queue', [
        (None, 0, True, True, 60, 1, 'und_free_queue'),
        (ProfileType.basic, 0, True, True, 90, 3, 'und_basic_queue'),
        (ProfileType.basic, 100, False, True, 90, 3, 'und_basic_queue'),
        (ProfileType.advance, 0, True, True, 60, 5, 'und_advance_queue'),
        (ProfileType.advance, 100, False, True, 60, 5, 'und_advance_queue'),
        (ProfileType.premium, 0, True, True, 30, 8, 'und_premium_queue'),
        (ProfileType.premium, 100, False, False, 30, 8, 'und_premium_queue'),
        (ProfileType.super_premium, 0, True, True, 30, 10, 'und_super_premium_queue'),
        (ProfileType.super_premium, 100, False, False, 30, 10, 'und_super_premium_queue'),
    ])
    def test_base_methods(self, profile_type, balance, need_blur, need_watermark, estimated_time, priority, queue):
        assert UndressService.rabbitmq_queue == settings.ML_UNDRESS_QUEUE
        assert UndressService.rabbitmq_routing_key == settings.ML_UNDRESS_QUEUE
        assert UndressService.task_name == 'jobs:create-undress:task'

        profile = ProfileFactory(type=profile_type, balance=balance) if profile_type else None

        assert UndressService.get_need_blur(profile=profile, cost=1) == need_blur
        assert UndressService.get_need_watermark(profile=profile, cost=1) == need_watermark
        assert UndressService.get_estimated_time(profile=profile) == estimated_time
        assert UndressService.get_priority(profile=profile) == priority

        assert UndressService.get_queue_by_priority(priority=priority) == queue

    def test_get_ml_params(self, mocker):
        fil = Filter.objects.get(pk=1)

        assert UndressService.get_ml_params(filter_ids=[fil.pk]) == {
            'prompt': fil.raw_prompt,
            'negative_prompt': fil.raw_negative_prompt,
            'step': 20,
            'sampler_name': 'DPM++ 2M SDE Karras',
        }

    @pytest.mark.parametrize('profile_type, balance, need_blur, need_watermark, estimated_time, pry, queue', [
        # (None, 0, True, True, 60, 1, 'und_free_queue'),
        # (ProfileType.basic, 0, True, True, 90, 3, 'und_basic_queue'),
        (ProfileType.basic, 100, False, True, 90, 3, 'und_basic_queue'),
        # (ProfileType.advance, 0, True, True, 60, 5, 'und_advance_queue'),
        (ProfileType.advance, 100, False, True, 60, 5, 'und_advance_queue'),
        # (ProfileType.premium, 0, True, True, 30, 8, 'und_premium_queue'),
        (ProfileType.premium, 100, False, False, 30, 8, 'und_premium_queue'),
        # (ProfileType.super_premium, 0, True, True, 30, 10, 'und_super_premium_queue'),
        (ProfileType.super_premium, 100, False, False, 30, 10, 'und_super_premium_queue'),
    ])
    def test_make_job_use_task(self, profile_type, balance, need_blur, need_watermark,
                               estimated_time, pry, queue, mocker):
        UndressService.use_task = True
        fake_cost = 1
        fake_image_b64 = 'fake-image-b64'
        fake_mask_b64 = 'fake-mask-b64'

        profile = ProfileFactory(type=profile_type, balance=balance) if profile_type else None
        user = profile.owner if profile else AnonymousUser()

        fil = Filter.objects.get(pk=1)

        def mock_call_rabbitmq(correlation_id, data: dict, priority: int):
            raise AssertionError('Bad logic')

        def mock_call_task(correlation_id, data: dict, priority: int):
            assert data['image_b64'] == fake_image_b64
            assert data['mask_b64'] == fake_mask_b64
            assert data['step'] == 20
            assert data['sampler_name'] == 'DPM++ 2M SDE Karras'
            assert data['prompt'] == fil.raw_prompt
            assert data['negative_prompt'] == fil.raw_negative_prompt

            assert priority == pry

        mocker.patch(
            'apps.jobs.core.base.BaseService.call_rabbitmq',
            new=mock_call_rabbitmq,
        )
        mocker.patch(
            'apps.jobs.core.base.BaseService.call_task',
            return_value=mock_call_task,
        )

        job = UndressService.make_job(
            user=user,
            filter_ids=[fil.pk],
            cost=fake_cost,
            image_b64=fake_image_b64,
            mask_b64=fake_mask_b64,
        )

        assert job.user_id == (user.pk if profile else None)
        assert job.sd_model_id == 1
        assert job.action_id == 1

        assert job.status == UndressJob.Status.PROCESS

        assert job.show_in_profile
        assert job.need_blur == need_blur
        assert job.need_watermark == need_watermark

        assert job.filters.filter(pk=fil.id).exists()

        if profile and balance > 0:
            assert job.cost == fake_cost
            assert Profile.objects.get(pk=profile.pk).balance == balance - fake_cost
        else:
            assert job.cost == 0

    @pytest.mark.parametrize('profile_type, balance, need_blur, need_watermark, estimated_time, pry, queue', [
        # (None, 0, True, True, 60, 1, 'und_free_queue'),
        # (ProfileType.basic, 0, True, True, 90, 3, 'und_basic_queue'),
        (ProfileType.basic, 100, False, True, 90, 3, 'und_basic_queue'),
        # (ProfileType.advance, 0, True, True, 60, 5, 'und_advance_queue'),
        (ProfileType.advance, 100, False, True, 60, 5, 'und_advance_queue'),
        # (ProfileType.premium, 0, True, True, 30, 8, 'und_premium_queue'),
        (ProfileType.premium, 100, False, False, 30, 8, 'und_premium_queue'),
        # (ProfileType.super_premium, 0, True, True, 30, 10, 'und_super_premium_queue'),
        (ProfileType.super_premium, 100, False, False, 30, 10, 'und_super_premium_queue'),
    ])
    def test_make_job_use_rabbitmq(self, profile_type, balance, need_blur, need_watermark,
                                   estimated_time, pry, queue, mocker):
        UndressService.use_task = False
        fake_cost = 1
        fake_image_b64 = 'fake-image-b64'
        fake_mask_b64 = 'fake-mask-b64'

        profile = ProfileFactory(type=profile_type, balance=balance) if profile_type else None
        user = profile.owner if profile else AnonymousUser()

        fil = Filter.objects.get(pk=1)

        def mock_call_task(correlation_id, data: dict, priority: int):
            raise AssertionError('Bad logic')

        def mock_call_rabbitmq(correlation_id, data: dict, priority: int):
            assert data['image_b64'] == fake_image_b64
            assert data['mask_b64'] == fake_mask_b64
            assert data['step'] == 20
            assert data['sampler_name'] == 'DPM++ 2M SDE Karras'
            assert data['prompt'] == fil.raw_prompt
            assert data['negative_prompt'] == fil.raw_negative_prompt

            assert priority == pry

        mocker.patch(
            'apps.jobs.core.base.BaseService.call_rabbitmq',
            new=mock_call_rabbitmq,
        )
        mocker.patch(
            'apps.jobs.core.base.BaseService.call_task',
            return_value=mock_call_task,
        )

        job = UndressService.make_job(
            user=user,
            filter_ids=[fil.pk],
            cost=fake_cost,
            image_b64=fake_image_b64,
            mask_b64=fake_mask_b64,
        )

        assert job.user_id == (user.pk if profile else None)
        assert job.sd_model_id == 1
        assert job.action_id == 1

        assert job.status == UndressJob.Status.PROCESS

        assert job.show_in_profile
        assert job.need_blur == need_blur
        assert job.need_watermark == need_watermark

        assert job.filters.filter(pk=fil.id).exists()

        if profile and balance > 0:
            assert job.cost == fake_cost
            assert Profile.objects.get(pk=profile.pk).balance == balance - fake_cost
        else:
            assert job.cost == 0


@pytest.mark.django_db
class TestGenerateService:

    @pytest.mark.parametrize('profile_type, balance, need_blur, need_watermark, estimated_time, priority, queue', [
        (None, 0, True, True, 60, 1, 'gen_free_queue'),
        (ProfileType.basic, 0, True, True, 90, 3, 'gen_basic_queue'),
        (ProfileType.basic, 100, False, True, 90, 3, 'gen_basic_queue'),
        (ProfileType.advance, 0, True, True, 60, 5, 'gen_advance_queue'),
        (ProfileType.advance, 100, False, True, 60, 5, 'gen_advance_queue'),
        (ProfileType.premium, 0, True, True, 30, 8, 'gen_premium_queue'),
        (ProfileType.premium, 100, False, False, 30, 8, 'gen_premium_queue'),
        (ProfileType.super_premium, 0, True, True, 30, 10, 'gen_super_premium_queue'),
        (ProfileType.super_premium, 100, False, False, 30, 10, 'gen_super_premium_queue'),
    ])
    def test_base_methods(self, profile_type, balance, need_blur, need_watermark, estimated_time, priority, queue):
        assert GenerateService.rabbitmq_queue == settings.ML_GENERATE_QUEUE
        assert GenerateService.rabbitmq_routing_key == settings.ML_GENERATE_QUEUE
        assert GenerateService.task_name == 'jobs:create-generate:task'

        profile = ProfileFactory(type=profile_type, balance=balance) if profile_type else None

        assert GenerateService.get_need_blur(profile=profile, cost=1) == need_blur
        assert GenerateService.get_need_watermark(profile=profile, cost=1) == need_watermark
        assert GenerateService.get_estimated_time(profile=profile) == estimated_time
        assert GenerateService.get_priority(profile=profile) == priority
        assert GenerateService.get_size(profile=profile) == (570, 768)

        assert GenerateService.get_queue_by_priority(priority=priority) == queue

    @pytest.mark.parametrize('profile_type, balance, need_blur, need_watermark, estimated_time, pry, queue', [
        (None, 0, True, True, 60, 1, 'und_free_queue'),
        (ProfileType.basic, 0, True, True, 90, 3, 'und_basic_queue'),
        (ProfileType.basic, 100, False, True, 90, 3, 'und_basic_queue'),
        (ProfileType.advance, 0, True, True, 60, 5, 'und_advance_queue'),
        (ProfileType.advance, 100, False, True, 60, 5, 'und_advance_queue'),
        (ProfileType.premium, 0, True, True, 30, 8, 'und_premium_queue'),
        (ProfileType.premium, 100, False, False, 30, 8, 'und_premium_queue'),
        (ProfileType.super_premium, 0, True, True, 30, 10, 'und_super_premium_queue'),
        (ProfileType.super_premium, 100, False, False, 30, 10, 'und_super_premium_queue'),
    ])
    def test_make_job_use_task(self, profile_type, balance, need_blur, need_watermark,
                               estimated_time, pry, queue, mocker):
        GenerateService.use_task = True
        fake_cost = 1

        profile = ProfileFactory(type=profile_type, balance=balance) if profile_type else None
        user = profile.owner if profile else AnonymousUser()

        fil = Filter.objects.get(pk=1)

        def mock_call_rabbitmq(correlation_id, data: dict, priority: int):
            raise AssertionError('Bad logic')

        def mock_call_task(correlation_id, data: dict, priority: int):
            assert data['step'] == 20
            assert data['cfg_scale'] == 7
            assert data['sampler_name'] == 'DPM++ 2M SDE Karras'

            assert priority == pry

        mocker.patch(
            'apps.jobs.core.base.BaseService.call_rabbitmq',
            new=mock_call_rabbitmq,
        )
        mocker.patch(
            'apps.jobs.core.base.BaseService.call_task',
            return_value=mock_call_task,
        )

        job = GenerateService.make_job(
            user=user,
            filter_ids=[fil.pk],
            cost=fake_cost,
            sd_model_id=3,
            action_id=3,
        )

        assert job.user_id == (user.pk if profile else None)
        assert job.sd_model_id == 3
        assert job.action_id == 3

        assert job.status == GenerateJob.Status.PROCESS

        assert job.show_in_profile == (True if profile else False)
        assert job.need_blur == need_blur
        assert job.need_watermark == need_watermark

        assert job.filters.filter(pk=fil.id).exists()

        if profile and balance > 0:
            assert job.cost == fake_cost
            assert Profile.objects.get(pk=profile.pk).balance == balance - fake_cost
        else:
            assert job.cost == 0

    @pytest.mark.parametrize('profile_type, balance, need_blur, need_watermark, estimated_time, pry, queue', [
        (None, 0, True, True, 60, 1, 'und_free_queue'),
        (ProfileType.basic, 0, True, True, 90, 3, 'und_basic_queue'),
        (ProfileType.basic, 100, False, True, 90, 3, 'und_basic_queue'),
        (ProfileType.advance, 0, True, True, 60, 5, 'und_advance_queue'),
        (ProfileType.advance, 100, False, True, 60, 5, 'und_advance_queue'),
        (ProfileType.premium, 0, True, True, 30, 8, 'und_premium_queue'),
        (ProfileType.premium, 100, False, False, 30, 8, 'und_premium_queue'),
        (ProfileType.super_premium, 0, True, True, 30, 10, 'und_super_premium_queue'),
        (ProfileType.super_premium, 100, False, False, 30, 10, 'und_super_premium_queue'),
    ])
    def test_make_job_use_rabbitmq(self, profile_type, balance, need_blur, need_watermark,
                                   estimated_time, pry, queue, mocker):
        GenerateService.use_task = False
        fake_cost = 1

        profile = ProfileFactory(type=profile_type, balance=balance) if profile_type else None
        user = profile.owner if profile else AnonymousUser()

        fil = Filter.objects.get(pk=1)

        def mock_call_task(correlation_id, data: dict, priority: int):
            raise AssertionError('Bad logic')

        def mock_call_rabbitmq(correlation_id, data: dict, priority: int):
            assert data['step'] == 20
            assert data['cfg_scale'] == 7
            assert data['sampler_name'] == 'DPM++ 2M SDE Karras'

            assert priority == pry

        mocker.patch(
            'apps.jobs.core.base.BaseService.call_rabbitmq',
            new=mock_call_rabbitmq,
        )
        mocker.patch(
            'apps.jobs.core.base.BaseService.call_task',
            return_value=mock_call_task,
        )

        job = GenerateService.make_job(
            user=user,
            filter_ids=[fil.pk],
            cost=fake_cost,
            sd_model_id=3,
            action_id=3,
        )

        assert job.user_id == (user.pk if profile else None)
        assert job.sd_model_id == 3
        assert job.action_id == 3

        assert job.status == GenerateJob.Status.PROCESS

        assert job.show_in_profile == (True if profile else False)
        assert job.need_blur == need_blur
        assert job.need_watermark == need_watermark

        assert job.filters.filter(pk=fil.id).exists()

        if profile and balance > 0:
            assert job.cost == fake_cost
            assert Profile.objects.get(pk=profile.pk).balance == balance - fake_cost
        else:
            assert job.cost == 0


@pytest.fixture()
def instagram_undress_job_process(user):
    def wrap(user_id: str = None, status: InstagramUndressJob.Status = None,
             detail_status: InstagramUndressJob.DetailStatus = None):
        return InstagramUndressJob.objects.create(
            user_id=user_id or user.pk,
            status=status or InstagramUndressJob.Status.PROCESS,
            detail_status=detail_status or InstagramUndressJob.DetailStatus.PROCESS_PARSER,
            link='https://www.instagram.com',
            link_type=InstagramUndressJob.LinkType.account,
        )

    return wrap


@pytest.mark.django_db
class TestInstagramUndressService:
    @pytest.mark.parametrize('profile_type, estimated_time', [
        (ProfileType.basic, 180),
        (ProfileType.advance, 180),
        (ProfileType.premium, 180),
        (ProfileType.super_premium, 180),
    ])
    def test_get_parser_estimated_time(self, profile_type: ProfileType, estimated_time: int):
        profile = ProfileFactory(type=profile_type)

        assert InstagramUndressService.get_parser_estimated_time(profile) == estimated_time

    @pytest.mark.parametrize('profile_type, queue', [
        (ProfileType.basic, 'inst_basic_queue'),
        (ProfileType.advance, 'inst_advance_queue'),
        (ProfileType.premium, 'inst_premium_queue'),
        (ProfileType.super_premium, 'inst_super_premium_queue'),
    ])
    def test_get_queue_by_profile_type(self, profile_type: ProfileType, queue: str):
        profile = ProfileFactory(type=profile_type)

        assert InstagramUndressService.get_queue_by_profile_type(profile.type) == queue

    @pytest.mark.parametrize('is_ok, status', [
        (True, False),
        (False, False),
    ])
    def test_get_link_type_error(self, is_ok, status, mocker):
        class MockResponse:
            ok = is_ok

            @classmethod
            def json(cls):
                return {'status': status}

        mocker.patch(
            'apps.jobs.core.instagram_undress.requests.get',
            return_value=MockResponse,
        )

        with pytest.raises(ValidationError):
            InstagramUndressService.get_link_type(
                link='https://fake-link',
            )

    @pytest.mark.parametrize('link, raw_type, correct_type', (
            ('https://fake-limk', 'account', InstagramUndressJob.LinkType.account),
            ('https://fake-limk', 'image', InstagramUndressJob.LinkType.photo),
    ))
    def test_get_link_success(self, link, raw_type, correct_type, mocker):
        def mock_requests_get(url: str, params: dict):
            assert url == urljoin(settings.INSTAGRAM_PARSER_URL, '/check_url')
            assert params == {
                'link_or_username': link,
                'scode': settings.INSTAGRAM_PARSER_SCODE,
            }

            class MockResponse:
                ok = True

                @classmethod
                def json(cls):
                    return {
                        'status': True,
                        'type': raw_type,
                    }

            return MockResponse

        mocker.patch(
            'apps.jobs.core.instagram_undress.requests.get',
            new=mock_requests_get
        )

        assert InstagramUndressService.get_link_type(link=link) == correct_type

    def test_create_step1_not_found_balance(self):
        profile = ProfileFactory(balance=decimal.Decimal('0.2'))

        with pytest.raises(ValidationError):
            InstagramUndressService.create_step1(
                user=profile.owner,
                link='https://fake-link',
                cost=decimal.Decimal('0.3')
            )

    @pytest.mark.parametrize('is_ok, status', [
        (True, False),
        (False, False),
    ])
    def test_create_step1_parser_die(self, is_ok, status, mocker, user):
        class MockResponse:
            ok = is_ok

            @classmethod
            def json(cls):
                return {'status': status}

        mocker.patch(
            'apps.jobs.core.instagram_undress.requests.post',
            return_value=MockResponse,
        )
        mocker.patch(
            'apps.jobs.core.instagram_undress.Service.get_link_type',
            return_value=InstagramUndressJob.LinkType.account,
        )

        with pytest.raises(APIException):
            InstagramUndressService.create_step1(
                user=user,
                link='https://fake-link',
                cost=decimal.Decimal('0.3'),
            )

    @pytest.mark.parametrize('profile_type, q', [
        (ProfileType.basic, 'inst_basic_queue'),
        (ProfileType.advance, 'inst_advance_queue'),
        (ProfileType.premium, 'inst_premium_queue'),
        (ProfileType.super_premium, 'inst_super_premium_queue'),
    ])
    @pytest.mark.parametrize('status, detail_status, link_type', [
        (InstagramUndressJob.Status.PROCESS, InstagramUndressJob.DetailStatus.PROCESS_PARSER,
         InstagramUndressJob.LinkType.account),
        (InstagramUndressJob.Status.PROCESS, InstagramUndressJob.DetailStatus.PROCESS_PARSER,
         InstagramUndressJob.LinkType.photo),
    ])
    def test_create_step1_success(self, profile_type, q, status, detail_status, link_type, mocker):
        fake_task_id = str(uuid.uuid4())
        fake_link = 'https://fake-link'
        profile = ProfileFactory(balance=decimal.Decimal('3'), type=profile_type)

        def mock_request_post(url, json):
            assert url == urljoin(settings.INSTAGRAM_PARSER_URL, '/task')
            assert json == {
                'qty': 12,
                'link_or_username': fake_link,
                'scode': settings.INSTAGRAM_PARSER_SCODE,
            }

            class MockResponse:
                ok = True

                @classmethod
                def json(cls):
                    return {
                        'status': True,
                        'task_id': fake_task_id,
                    }

            return MockResponse

        def mock_current_app_send_task(name: str, kwargs: dict, queue: str):
            assert name == 'jobs:inst-parser-control:task'
            assert kwargs == {
                'pk': fake_task_id,
            }
            assert queue == q

        mocker.patch(
            'apps.jobs.core.instagram_undress.Service.get_link_type',
            return_value=link_type,
        )
        mocker.patch(
            'apps.jobs.core.instagram_undress.requests.post',
            new=mock_request_post,
        )
        mocker.patch(
            'apps.jobs.core.instagram_undress.current_app.send_task',
            new=mock_current_app_send_task,
        )

        job = InstagramUndressService.create_step1(
            user=profile.owner,
            link=fake_link,
            cost=decimal.Decimal('0.3'),
        )

        assert Profile.objects.get(pk=profile.pk).balance == decimal.Decimal('2.7')
        assert job.pk == fake_task_id
        assert job.user_id == profile.owner_id
        assert job.status == status
        assert job.detail_status == detail_status
        assert job.link == fake_link
        assert job.link_type == link_type
        assert job.parser_estimated_time == 180

    def test_check_step1_not_found(self, mocker, user, instagram_undress_job_process):
        class MockResponse:
            ok = True
            status_code = 404

        mocker.patch(
            'apps.jobs.core.instagram_undress.requests.get',
            return_value=MockResponse,
        )

        job = instagram_undress_job_process(user_id=user.pk)

        InstagramUndressService.check_step1(
            user=user,
            job=job,
        )

        job = InstagramUndressJob.objects.get(pk=job.pk)
        assert job.status == InstagramUndressJob.Status.ERROR
        assert job.detail_status == InstagramUndressJob.DetailStatus.ERROR_PARSER

    def test_check_step1_status_error(self, mocker, user, instagram_undress_job_process):
        class MockResponse:
            ok = True
            status_code = 200

            @classmethod
            def json(cls):
                return {'status': -1}

        mocker.patch(
            'apps.jobs.core.instagram_undress.requests.get',
            return_value=MockResponse,
        )

        job = instagram_undress_job_process(user_id=user.pk)

        InstagramUndressService.check_step1(
            user=user,
            job=job,
        )

        job = InstagramUndressJob.objects.get(pk=job.pk)
        assert job.status == InstagramUndressJob.Status.ERROR
        assert job.detail_status == InstagramUndressJob.DetailStatus.ERROR_PARSER

    def test_check_step1_status_expired(self, mocker, user, instagram_undress_job_process):
        class MockResponse:
            ok = True
            status_code = 200

            @classmethod
            def json(cls):
                return {'status': -2}

        mocker.patch(
            'apps.jobs.core.instagram_undress.requests.get',
            return_value=MockResponse,
        )

        job = instagram_undress_job_process(user_id=user.pk)

        InstagramUndressService.check_step1(
            user=user,
            job=job,
        )

        job = InstagramUndressJob.objects.get(pk=job.pk)
        assert job.status == InstagramUndressJob.Status.ERROR
        assert job.detail_status == InstagramUndressJob.DetailStatus.EXPIRED_PARSER

    def test_check_step1_status_success(self, mocker, faker, instagram_undress_job_process):
        profile = ProfileFactory(type=ProfileType.premium)
        job = instagram_undress_job_process(user_id=profile.owner_id)

        fake_link1 = faker.unique.url()
        fake_link2 = faker.unique.url()
        fake_link3 = faker.unique.url()

        def mock_requests_get(url: str, params: dict):
            assert url == urljoin(settings.INSTAGRAM_PARSER_URL, '/task')
            assert params == {
                'task_id': str(job.pk),
                'scode': settings.INSTAGRAM_PARSER_SCODE,
            }

            class MockResponse:
                ok = True
                status_code = 200

                @classmethod
                def json(cls):
                    return {
                        'status': 2,
                        'links': [
                            fake_link1,
                            fake_link2,
                            fake_link3,
                        ],
                    }

            return MockResponse

        def mock_current_app_send_task(name: str, kwargs: dict, queue: str):
            assert name == 'jobs:inst-make-make:task'
            assert kwargs == {
                'pk': str(job.pk),
            }
            assert queue == 'inst_premium_queue'

        mocker.patch(
            'apps.jobs.core.instagram_undress.requests.get',
            new=mock_requests_get,
        )

        mocker.patch(
            'apps.jobs.core.instagram_undress.current_app.send_task',
            new=mock_current_app_send_task,
        )

        InstagramUndressService.check_step1(
            user=profile.owner,
            job=job,
        )

        job = InstagramUndressJob.objects.get(pk=job.pk)
        assert job.status == InstagramUndressJob.Status.PROCESS
        assert job.detail_status == InstagramUndressJob.DetailStatus.PROCESS_MAKE_MASK

        assert job.sources.filter(
            image_url__in=[fake_link1,
                           fake_link2,
                           fake_link3]
        ).count() == 3

    @pytest.mark.parametrize('detail_status', [
        InstagramUndressJob.DetailStatus.CREATED_MAKE_MASK,
        InstagramUndressJob.DetailStatus.PROCESS_MAKE_MASK,
        InstagramUndressJob.DetailStatus.SUCCESS_MAKE_MASK,
    ])
    def test_check_step1_after_or_process_mask(self, detail_status, user, instagram_undress_job_process):
        job = instagram_undress_job_process(
            user_id=user.pk,
            detail_status=detail_status,
        )

        new_job = InstagramUndressService.check_step1(
            user=user,
            job=job,
        )

        assert new_job.status == job.status
        assert new_job.detail_status == job.detail_status

    @pytest.mark.parametrize('balance, sources_count', [
        (decimal.Decimal('10'), 12),
        (decimal.Decimal('1'), 3),
        (decimal.Decimal('0'), 5),
    ])
    def test_create_step2_not_enough_balance(self, balance, sources_count, faker, instagram_undress_job_process):
        profile = ProfileFactory(balance=balance)
        job = instagram_undress_job_process(user_id=profile.owner_id)

        for _ in range(sources_count):
            InstagramSource.objects.create(job=job, image_url=faker.unique.url())

        with pytest.raises(ValidationError):
            InstagramUndressService.create_step2(
                user=profile.owner,
                job=job,
                cost=decimal.Decimal('1.3'),
                filter_ids=[1],
                exclude_ids=[],
                custom_masks={},
            )

    def test_create_step2_success(self, mocker, faker, instagram_undress_job_process):
        profile = ProfileFactory(balance=decimal.Decimal('12'), type=ProfileType.premium)
        main_job = instagram_undress_job_process(user_id=profile.owner_id)

        source1 = InstagramSource.objects.create(job=main_job, image_url=faker.unique.url())
        source2 = InstagramSource.objects.create(job=main_job, image_url=faker.unique.url())
        source3 = InstagramSource.objects.create(job=main_job, image_url=faker.unique.url())

        fake_filter_ids = {source1.pk: [1]}
        fake_cost = decimal.Decimal('1.3')

        def mock_make_single_undress_job(job: InstagramUndressJob, source: InstagramSource,
                                         filter_ids: list, params: dict, estimated_time: int, need_blur: bool,
                                         need_watermark: bool, cost: decimal.Decimal,
                                         queue: str, undress_queue: str, custom_masks: dict):
            assert job == main_job
            assert source in (source1, source2, source3)
            assert filter_ids == [1]
            assert list(params.keys()) == ['prompt', 'negative_prompt', 'step', 'sampler_name']
            assert estimated_time == 30
            assert not need_blur
            assert not need_watermark
            assert cost == fake_cost
            assert queue == 'inst_premium_queue'
            assert undress_queue == 'und_premium_queue'
            assert custom_masks == {}

        mocker.patch(
            'apps.jobs.core.instagram_undress.Service._make_single_undress_job',
            new=mock_make_single_undress_job,
        )

        InstagramUndressService.create_step2(
            user=profile.owner,
            job=main_job,
            cost=fake_cost,
            filter_ids=fake_filter_ids,
            exclude_ids=[],
            custom_masks={},
        )

        assert Profile.objects.get(pk=profile.pk).balance == decimal.Decimal('8.1')

        new_main_job = InstagramUndressJob.objects.get(pk=main_job.pk)
        assert new_main_job.detail_status == InstagramUndressJob.DetailStatus.PROCESS_JOB

    def test_make_single_undress_job(self):
        pass


@pytest.mark.django_db
class TestVideoService:
    def test_get_ml_params(self):
        params = VideoService.get_ml_params(
            [3], sd_model_id=2,
            action_id=2,
        )

        assert set(params.keys()) == {
            'prompt', 'negative_prompt',
            'step', 'sampler_name', 'cfg_scale',
            'guidance_scale',
        }

        assert params['guidance_scale'] == 7.5

    @pytest.mark.parametrize('profile_type, result', [
        (ProfileType.basic, 'vid_basic_queue'),
        (ProfileType.advance, 'vid_advance_queue'),
        (ProfileType.premium, 'vid_premium_queue'),
        (ProfileType.super_premium, 'vid_super_premium_queue'),
    ])
    def test_get_queue_by_priority(self, profile_type: ProfileType, result: str):
        profile = ProfileFactory(type=profile_type)
        priority = VideoService.get_priority(profile=profile)
        assert VideoService.get_queue_by_priority(priority=priority) == result

    def test_get_need_blur(self, user):
        with pytest.raises(NotImplementedError):
            VideoService.get_need_blur(
                profile=user.profile,
                cost=decimal.Decimal('1'),
            )

    @pytest.mark.parametrize('profile_type, result', [
        (ProfileType.basic, 150),
        (ProfileType.advance, 150),
        (ProfileType.premium, 150),
        (ProfileType.super_premium, 150),
    ])
    def test_get_estimated_time(self, profile_type: ProfileType, result: int):
        profile = ProfileFactory(type=profile_type)
        assert VideoService.get_estimated_time(profile=profile) == result

    def test_get_frames(self, user):
        assert VideoService.get_frames(profile=user.profile) == 63

    def test_make_job_error(self):
        from rest_framework.exceptions import PermissionDenied
        user_anonymous = AnonymousUser()
        user_without_balance = ProfileFactory(balance=0)

        with pytest.raises(PermissionDenied):
            VideoService.make_job(
                user=user_anonymous,
                filter_ids=[1],
                cost=decimal.Decimal('4'),
            )

        with pytest.raises(PermissionDenied):
            VideoService.make_job(
                user=user_without_balance.owner,
                filter_ids=[1],
                cost=decimal.Decimal('4'),
            )

    def test_make_job_success(self, mocker):
        profile = ProfileFactory(
            balance=decimal.Decimal('10'),
            type=ProfileType.super_premium,
        )

        def mock_call_task(correlation_id, data: dict, priority: int):
            assert data['next_queue'] == 'vid_super_premium_queue'
            assert data['frames'] == 63
            assert priority == 10

        mocker.patch(
            'apps.jobs.core.base.BaseService.call_task',
            new=mock_call_task,
        )

        job = VideoService.make_job(
            user=profile.owner,
            filter_ids=[2],
            cost=decimal.Decimal('4'),
            sd_model_id=2,
        )

        assert job.user_id == profile.pk
        assert job.sd_model_id == 2
        assert job.cost == decimal.Decimal('4')
        assert job.status == VideoJob.Status.PROCESS
        assert job.show_in_profile
        assert not job.need_watermark
