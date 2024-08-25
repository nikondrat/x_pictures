import pytest
from faker import Faker

from rest_framework.test import APIClient

from typing import Optional


@pytest.fixture(autouse=True, scope='session')
def django_test_environment(django_test_environment):
    from django.apps import apps

    get_models = apps.get_models

    for m in [m for m in get_models()]:
        if not m._meta.managed and not m._meta.abstract:
            m._meta.managed = True


@pytest.fixture(scope='session')
def celery_app(request):
    from backend.celery import app
    app.conf.update(CELERY_ALWAYS_EAGER=True)
    return app


@pytest.fixture(scope='session')
def _import_tasks():
    def wrapper():
        import core.users.tasks
        import apps.profiles.tasks
        import apps.jobs.tasks
        import apps.shop.tasks
        import apps.mailing.tasks

    return wrapper


@pytest.fixture
def send_celery_task(celery_app, _import_tasks):
    _import_tasks()

    def wrapper(name: str, args=None, kwargs=None, **options):
        task = celery_app.tasks[name]
        return task.apply(args, kwargs, **options)
    return wrapper


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def get_api_client(api_client):
    def _get_api_client(user_id: Optional[int] = None) -> APIClient:
        if user_id:
            from core.users.factories import TokenFactory

            token = TokenFactory(user_id=user_id)
            api_client.credentials(
                HTTP_AUTHORIZATION='Token ' + token.key,
            )
        return api_client
    return _get_api_client


@pytest.fixture()
def faker() -> Faker:
    return Faker()


@pytest.fixture()
def user():
    from apps.profiles.factories import ProfileFactory
    return ProfileFactory(balance=20).owner


@pytest.fixture()
def get_user():
    def wrapper():
        from apps.profiles.factories import ProfileFactory
        return ProfileFactory(balance=2).owner
    return wrapper
