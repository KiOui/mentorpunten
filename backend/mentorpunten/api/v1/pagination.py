from rest_framework.pagination import LimitOffsetPagination


class StandardResultsSetPagination(LimitOffsetPagination):
    """Standard Results Set Pagination."""

    page_size = 50
    max_page_size = 100
