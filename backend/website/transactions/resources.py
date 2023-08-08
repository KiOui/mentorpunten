from import_export import resources
from import_export.fields import Field

from transactions import models
from transactions.models import Account


class AccountResource(resources.ModelResource):
    """Account Resource."""

    balance = Field()

    def dehydrate_balance(self, account: Account):
        """Dehydrate balance out of Account."""
        return account.balance

    class Meta:
        """Meta class."""

        model = models.Account
        fields = [
            "id",
            "name",
            "created_at",
            "balance",
        ]
        export_order = [
            "id",
            "name",
            "created_at",
            "balance",
        ]
