from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response

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


class TransactionListCreateAPIView(ListCreateAPIView):
    """Transaction List Create API View."""

    serializer_class = TransactionSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = (
        "processor",
        "account",
    )

    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get the Queryset."""
        return Transaction.objects.all().order_by("-timestamp")

    def create(self, request, *args, **kwargs):
        """Create a Transaction."""
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not request.user.has_perm("transactions.add_transaction"):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        super(TransactionListCreateAPIView, self).create(request, *args, **kwargs)


class TransactionRetrieveAPIView(RetrieveAPIView):
    """Transaction Retrieve API View."""

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
