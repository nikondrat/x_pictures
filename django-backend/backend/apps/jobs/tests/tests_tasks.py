import uuid
from datetime import timedelta

from django.utils import timezone

import pytest
from freezegun import freeze_time

from apps.jobs.models import UndressJob, GenerateJob, InstagramUndressJob
from apps.jobs.factories import GenerateJobFactory, UndressJobFactory, InstagramUndressJobFactory

from apps.jobs.services import NovitaV3Provider


@pytest.mark.django_db
def test_close_timeout_jobs_task(send_celery_task):
    with freeze_time(timezone.now() - timedelta(minutes=14)):
        job1 = GenerateJobFactory()
        job2 = UndressJobFactory(status=UndressJob.Status.PROCESS)
    with freeze_time(timezone.now() - timedelta(minutes=9)):
        job3 = GenerateJobFactory(status=GenerateJob.Status.PROCESS)
        job4 = UndressJobFactory()

    job5 = GenerateJobFactory()
    job6 = UndressJobFactory(status=UndressJob.Status.PROCESS)

    assert UndressJob.objects.filter(status__in=(UndressJob.Status.CREATED, UndressJob.Status.PROCESS)).count() == 3
    assert GenerateJob.objects.filter(status__in=(GenerateJob.Status.CREATED, GenerateJob.Status.PROCESS)).count() == 3

    send_celery_task('jobs:close-timeout-jobs:task')

    assert GenerateJob.objects.get(pk=job1.pk).status == GenerateJob.Status.ERROR
    assert UndressJob.objects.get(pk=job2.pk).status == UndressJob.Status.ERROR

    assert GenerateJob.objects.get(pk=job3.pk).status == GenerateJob.Status.PROCESS
    assert UndressJob.objects.get(pk=job4.pk).status == UndressJob.Status.CREATED

    assert GenerateJob.objects.get(pk=job5.pk).status == GenerateJob.Status.CREATED
    assert UndressJob.objects.get(pk=job6.pk).status == UndressJob.Status.PROCESS


@pytest.mark.django_db
def test_close_timeout_inst_jobs_task(send_celery_task):
    with freeze_time(timezone.now() - timedelta(minutes=21)):
        job1 = InstagramUndressJobFactory(
            status=InstagramUndressJob.Status.PROCESS,
            detail_status=InstagramUndressJob.DetailStatus.PROCESS_PARSER,
        )
        job2 = InstagramUndressJobFactory(
            status=InstagramUndressJob.Status.PROCESS,
            detail_status=InstagramUndressJob.DetailStatus.PROCESS_MAKE_MASK,
        )
        job3 = InstagramUndressJobFactory(
            status=InstagramUndressJob.Status.PROCESS,
            detail_status=InstagramUndressJob.DetailStatus.PROCESS_JOB,
        )

    with freeze_time(timezone.now() - timedelta(minutes=9)):
        job4 = InstagramUndressJobFactory(
            status=InstagramUndressJob.Status.PROCESS,
            detail_status=InstagramUndressJob.DetailStatus.PROCESS_PARSER,
        )
        job5 = InstagramUndressJobFactory(
            status=InstagramUndressJob.Status.PROCESS,
            detail_status=InstagramUndressJob.DetailStatus.PROCESS_MAKE_MASK,
        )
        job6 = InstagramUndressJobFactory(
            status=InstagramUndressJob.Status.PROCESS,
            detail_status=InstagramUndressJob.DetailStatus.PROCESS_JOB,
        )

    send_celery_task('jobs:close-timeout-jobs:task')

    new_job1 = InstagramUndressJob.objects.get(pk=job1.pk)
    assert new_job1.status == InstagramUndressJob.Status.ERROR
    assert new_job1.detail_status == InstagramUndressJob.DetailStatus.EXPIRED_PARSER

    new_job2 = InstagramUndressJob.objects.get(pk=job2.pk)
    assert new_job2.status == InstagramUndressJob.Status.ERROR
    assert new_job2.detail_status == InstagramUndressJob.DetailStatus.EXPIRED_MAKE_MASK

    new_job3 = InstagramUndressJob.objects.get(pk=job3.pk)
    assert new_job3.status == InstagramUndressJob.Status.ERROR
    assert new_job3.detail_status == InstagramUndressJob.DetailStatus.EXPIRED_JOB

    new_job4 = InstagramUndressJob.objects.get(pk=job4.pk)
    assert new_job4.status == InstagramUndressJob.Status.PROCESS
    assert new_job4.detail_status == InstagramUndressJob.DetailStatus.PROCESS_PARSER

    new_job5 = InstagramUndressJob.objects.get(pk=job5.pk)
    assert new_job5.status == InstagramUndressJob.Status.PROCESS
    assert new_job5.detail_status == InstagramUndressJob.DetailStatus.PROCESS_MAKE_MASK

    new_job6 = InstagramUndressJob.objects.get(pk=job6.pk)
    assert new_job6.status == InstagramUndressJob.Status.PROCESS
    assert new_job6.detail_status == InstagramUndressJob.DetailStatus.PROCESS_JOB


@pytest.mark.django_db
def test_close_success_inst_jobs(send_celery_task):
    job = InstagramUndressJobFactory(
        status=InstagramUndressJob.Status.PROCESS,
        detail_status=InstagramUndressJob.DetailStatus.PROCESS_JOB,
    )

    sub_job1 = UndressJobFactory(status=UndressJob.Status.SUCCESS,
                                 action_id=1, sd_model_id=1)
    job.jobs.add(sub_job1.pk)

    sub_job2 = UndressJobFactory(status=UndressJob.Status.ERROR,
                                 action_id=1, sd_model_id=1)
    job.jobs.add(sub_job2.pk)

    sub_job3 = UndressJobFactory(status=UndressJob.Status.PROCESS,
                                 action_id=1, sd_model_id=1)
    job.jobs.add(sub_job3.pk)

    send_celery_task('jobs:close-success-inst-jobs:task')

    new_job = InstagramUndressJob.objects.get(pk=job.pk)
    assert new_job.status == job.status
    assert new_job.detail_status == job.detail_status

    sub_job3.status = UndressJob.Status.SUCCESS
    sub_job3.save()

    send_celery_task('jobs:close-success-inst-jobs:task')

    new_job = InstagramUndressJob.objects.get(pk=job.pk)
    assert new_job.status == InstagramUndressJob.Status.SUCCESS
    assert new_job.detail_status == InstagramUndressJob.DetailStatus.SUCCESS_JOB


@pytest.mark.django_db
def test_inst_parser_control_task(send_celery_task, mocker):
    main_job = InstagramUndressJobFactory(
        status=InstagramUndressJob.Status.PROCESS,
        detail_status=InstagramUndressJob.DetailStatus.PROCESS_PARSER,
    )

    def mock_check_step1(job):
        assert job == main_job
        job.detail_status = InstagramUndressJob.DetailStatus.PROCESS_MAKE_MASK
        job.save()
        return job

    mocker.patch(
        'apps.jobs.core.instagram_undress.Service.check_step1',
        side_effect=[
            main_job,
            main_job,
            mock_check_step1(main_job),
        ]
    )

    mocker.patch(
        'apps.jobs.tasks.time.sleep',
        return_value=None,
    )

    assert send_celery_task(
        'jobs:inst-parser-control:task',
        kwargs={'pk': str(main_job.pk)}
    )

    new_main_job = InstagramUndressJob.objects.get(pk=main_job.pk)

    assert new_main_job.status == InstagramUndressJob.Status.PROCESS
    assert new_main_job.detail_status == InstagramUndressJob.DetailStatus.PROCESS_MAKE_MASK


@pytest.mark.django_db
class TestNovitaV3Provider:

    def test_lower_get_task_result(self, mocker):
        fake_api_key = str(uuid.uuid4())
        fake_task_id = str(uuid.uuid4())

        class MockResponse:
            def raise_for_status(self): ...

            def json(self): ...

        def mock_request(method: str, url: str, headers: dict, params: dict):
            assert method == 'GET'
            assert url == 'https://api.novita.ai/v3/async/task-result'
            assert headers == {
                'Authorization': f'Bearer {fake_api_key}'
            }
            assert params == {
                'task_id': fake_task_id,
            }

            return MockResponse()

        mocker.patch(
            'apps.jobs.services.requests.request',
            new=mock_request,
        )

        NovitaV3Provider(fake_api_key)._get_task_result(
            task_id=fake_task_id,
        )

    def test_lower_create_task(self, mocker):
        fake_api_key = str(uuid.uuid4())
        fake_task_id = str(uuid.uuid4())
        fake_payload = {}

        class MockResponse:
            def raise_for_status(self): ...

            def json(self):
                return {'task_id': fake_task_id}

        def mock_request(method: str, url: str, headers: dict, json: dict):
            assert method == 'POST'
            assert url == 'https://api.novita.ai/v3/async/txt2video'
            assert headers == {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {fake_api_key}'
            }
            assert json == fake_payload
            return MockResponse()

        mocker.patch(
            'apps.jobs.services.requests.request',
            new=mock_request,
        )

        assert NovitaV3Provider(fake_api_key)._create_task(
            payload=fake_payload,
        ) == fake_task_id
