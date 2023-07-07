from rest_framework.generics import CreateAPIView

from transactions.api.v1.serializers import AccountSerializer
from transactions.models import Account


class AccountRetrieveAPIView(CreateAPIView):
    """
    Account Retrieve API View.

    Permissions required: None

    Use this endpoint to get the transaction details for a user by using a token.
    """

    serializer_class = AccountSerializer
    queryset = Account.objects.all()


