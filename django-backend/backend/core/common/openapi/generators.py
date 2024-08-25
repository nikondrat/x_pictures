from django.conf import settings

from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.settings import spectacular_settings

from core.common.openapi import preprocessing_hooks


class CustomSchemaGenerator(SchemaGenerator):
    base_title = settings.SPECTACULAR_SETTINGS['TITLE']

    def get_schema(self, request=None, public=False):
        if '/api/schema-jobs/' in request.path:
            spectacular_settings.TITLE = f'{self.base_title} (Jobs view)'
            spectacular_settings.SCHEMA_PATH_PREFIX = r'/api/jobs/'
            spectacular_settings.PREPROCESSING_HOOKS = [
                preprocessing_hooks.wrapped_preprocessing_paths(
                    startswith=['/api/jobs/']
                ),
            ]
        elif '/api/schema-gallery/' in request.path:
            spectacular_settings.TITLE = f'{self.base_title} (Gallery view)'
            spectacular_settings.SCHEMA_PATH_PREFIX = r'/api/gallery/'
            spectacular_settings.PREPROCESSING_HOOKS = [
                preprocessing_hooks.wrapped_preprocessing_paths(
                    startswith=['/api/gallery/']
                ),
            ]
        elif '/api/schema-users/' in request.path:
            spectacular_settings.TITLE = f'{self.base_title} (Users view)'
            spectacular_settings.SCHEMA_PATH_PREFIX = r'/api/'
            spectacular_settings.PREPROCESSING_HOOKS = [
                preprocessing_hooks.wrapped_preprocessing_paths(
                    startswith=['/api/profiles/',
                                '/api/users/']
                ),
            ]
        else:
            spectacular_settings.TITLE = self.base_title
            spectacular_settings.SCHEMA_PATH_PREFIX = r'/api/'
            spectacular_settings.PREPROCESSING_HOOKS = []

        return super().get_schema(request=request, public=public)
