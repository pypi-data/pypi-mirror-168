from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class AdminPaginationClass(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'limit': self.get_page_size(self.request),
            'results': data
        })


class CustomResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'limit': self.get_page_size(self.request),
            'results': data
        })
