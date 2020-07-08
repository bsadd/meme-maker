from rest_framework.pagination import PageNumberPagination

from coreapp import constants


class StandardResultsSetPagination(PageNumberPagination):
    page_size = constants.DEFAULT_PAGE_SIZE
    page_size_query_param = 'page-size'
    max_page_size = constants.MAX_PAGE_SIZE
