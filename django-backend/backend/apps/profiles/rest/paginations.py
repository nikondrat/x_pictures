from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from apps.profiles.rest.utils import get_generation_count


class StoragePagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('num_pages', self.page.paginator.num_pages),
            ('generation_count', get_generation_count(self.request.user)),
        ]))

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'example': 123,
                },
                'next': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'https://api.example.org/api/profiles/image-storage/?{page_query_param}=4'.format(
                        page_query_param=self.page_query_param)
                },
                'previous': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'https://api.example.org/api/profiles/image-storage/?{page_query_param}=4'.format(
                        page_query_param=self.page_query_param)
                },
                'results': schema,
                'num_pages': {
                    'type': 'integer',
                    'example': 123,
                },
                'generation_count': {
                    'example': 100,
                }
            },
        }


class LikedStoragePagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('num_pages', self.page.paginator.num_pages),
        ]))
