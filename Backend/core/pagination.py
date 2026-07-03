"""
Custom Pagination Classes
"""
from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DynamicPageSizePagination(PageNumberPagination):
    """
    Pagination class that allows clients to set page_size via query parameter.
    Returns unified format: {success, count, next, previous, results}
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('success', True),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'required': ['success', 'count', 'results'],
            'properties': {
                'success': {'type': 'boolean', 'example': True},
                'count': {'type': 'integer', 'example': 123},
                'next': {'type': 'string', 'nullable': True, 'format': 'uri'},
                'previous': {'type': 'string', 'nullable': True, 'format': 'uri'},
                'results': schema,
            },
        }
