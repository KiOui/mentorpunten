from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView

from mentorpunten.api.v1.pagination import StandardResultsSetPagination
from transactions.api.v1.serializers import AccountSerializer, TransactionSerializer
from transactions.models import Account, Transaction


class AccountRetrieveAPIView(CreateAPIView):
    """
    Account Retrieve API View.

    Permissions required: None

    Use this endpoint to get the transaction details for a user by using a token.
    """

    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class TransactionListAPIView(ListCreateAPIView):
    """Transaction List API View."""

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("account", "processor",)

    pagination_class = StandardResultsSetPagination


class TransactionRetrieveAPIView(RetrieveAPIView):
    """Transaction Retrieve API View."""

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()