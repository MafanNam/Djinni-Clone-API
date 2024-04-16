from rest_framework.pagination import PageNumberPagination


class MaxResultsSetPagination(PageNumberPagination):
    """Page Size 100"""

    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 10000


class LargeResultsSetPagination(PageNumberPagination):
    """Page Size 50"""

    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    """Page Size 20"""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 10000


class MediumResultsSetPagination(PageNumberPagination):
    """Page Size 15"""

    page_size = 15
    page_size_query_param = "page_size"
    max_page_size = 10000


class MinimumResultsSetPagination(PageNumberPagination):
    """Page Size 10"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10000
