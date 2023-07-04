from rest_framework.generics import CreateAPIView

from mentorpunten.api.openapi import CustomAutoSchema
from transactions.api.v1.serializers import AccountSerializer
from transactions.models import Account


class AccountRetrieveAPIView(CreateAPIView):
    """
    Account Retrieve API View.

    Permissions required: None

    Use this endpoint to get the transaction details for a user by using a token.
    """

    schema = CustomAutoSchema(
        request_schema={
            "type": "object",
            "properties": {"token": {"type": "string", "example": "string"}},
        }
    )

    serializer_class = AccountSerializer
    queryset = Account.objects.all()
