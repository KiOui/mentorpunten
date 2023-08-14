from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    ListCreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tournaments import models
from tournaments.api.v1 import serializers

from store.models import Item as StoreItem
from transactions.models import Transaction


class TournamentFilter(FilterSet):
    """Tournament FilterSet."""

    class Meta:
        """Meta class."""

        model = models.Tournament
        fields = {
            "store": ("exact", "isnull"),
        }


class TournamentListAPIView(ListAPIView):
    """Tournament List API View."""

    serializer_class = serializers.TournamentSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = TournamentFilter
    search_fields = (
        "name",
        "slug",
    )

    def get_queryset(self):
        """Get the queryset."""
        return models.Tournament.objects.all().order_by("active_from")


class TournamentRetrieveAPIView(RetrieveAPIView):
    """Tournament Retrieve API View."""

    serializer_class = serializers.TournamentSerializer

    def get_queryset(self):
        """Get the queryset."""
        return models.Tournament.objects.all()


class TeamListAPIView(ListAPIView):
    """Team List API View."""

    serializer_class = serializers.TeamSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = (
        "tournament",
        "members",
    )
    search_fields = ("name",)

    def get_queryset(self):
        """Get the queryset."""
        return models.Team.objects.all()


class TeamRetrieveAPIView(RetrieveAPIView):
    """Team Retrieve API View."""

    serializer_class = serializers.TeamSerializer

    def get_queryset(self):
        """Get the queryset."""
        return models.Team.objects.all()


class ItemListCreateAPIView(ListCreateAPIView):
    """Item List Create API View."""

    serializer_class = serializers.ItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Item.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = (
        "item",
        "property_of",
        "used",
    )

    def get_queryset(self):
        """Get Queryset."""
        if self.request.user.has_perm("tournaments.view_items"):
            return self.queryset
        else:
            # Only show items that are bought by a user's teams.
            return self.queryset.filter(property_of__members__in=[self.request.user])

    def create(self, request, *args, **kwargs):
        """Create an Item."""
        item_id = request.data.get("item", None)
        if item_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            item = StoreItem.objects.get(id=item_id)
        except StoreItem.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        property_of_id = request.data.get("property_of", None)
        possible_teams = models.Team.objects.filter(
            id=property_of_id, members__in=[request.user]
        )
        if len(possible_teams) == 0:
            # Team does not exist or user is not a member of the team.
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            property_of = possible_teams[0]

        if property_of.coins_account.balance < item.price:
            return Response(status=status.HTTP_403_FORBIDDEN)

        transaction = Transaction.objects.create(
            account=property_of.coins_account,
            amount=item.price * -1,
            description=f"Bought item {item}",
            processor=request.user,
        )

        item_bought = models.Item.objects.create(
            name=item.name,
            price=item.price,
            description=item.description,
            item=item,
            transaction=transaction,
            property_of=property_of,
            used=False,
        )

        serializer = self.get_serializer(item_bought)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ItemUpdateAPIView(UpdateAPIView):
    """Item Update API View."""

    serializer_class = serializers.ItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Item.objects.all()

    def get_queryset(self):
        """Get Queryset."""
        if self.request.user.has_perm("tournaments.view_items"):
            return self.queryset
        else:
            # Only show items that are bought by a user's teams.
            return self.queryset.filter(property_of__members__in=[self.request.user])

    def update(self, request, *args, **kwargs):
        """Update an Item."""
        if request.user.has_perm("tournaments.change_item"):
            return super(ItemUpdateAPIView, self).update(request, *args, **kwargs)
        else:
            # Only update the 'used' property of an Item.
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            used = request.data.get("used", None)
            if request.user not in instance.team.members.all():
                return Response(status=status.HTTP_403_FORBIDDEN)

            if used is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if instance.used and not used:
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer = self.get_serializer(
                instance, data={"used": request.data.get("used")}, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
