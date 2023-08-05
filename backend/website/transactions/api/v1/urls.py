from django.urls import path
from transactions.api.v1.views import (
    AccountRetrieveAPIView,
    TransactionListAPIView,
    TransactionRetrieveAPIView,
)

urlpatterns = [
    path("", TransactionListAPIView.as_view(), name="transaction_listcreate"),
    path(
        "<int:pk>/", TransactionRetrieveAPIView.as_view(), name="transaction_retrieve"
    ),
    path("account/", AccountRetrieveAPIView.as_view(), name="account_retrieve"),
]
