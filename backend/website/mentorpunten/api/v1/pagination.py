from rest_framework.pagination import LimitOffsetPagination


class StandardResultsSetPagination(LimitOffsetPagination):
    """Standard Results Set Pagination."""

    max_limit = 100
    default_limit = 50
