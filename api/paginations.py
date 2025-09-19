from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


# Page number pagination
class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page-num'  # Allow client to set page number
    max_page_size = 100  # Maximum page size limit

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        })

# Limit-offset pagination
class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
    limit_query_param = 'limit'
    offset_query_param = 'offset'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.count,
            'limit': self.get_limit(self.request),
            'offset': self.get_offset(self.request),
            'results': data
        })