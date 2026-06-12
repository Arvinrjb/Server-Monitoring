from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class PagePagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    page_size_query_param = 'size'
    max_page_size = 100


class ApiPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100

