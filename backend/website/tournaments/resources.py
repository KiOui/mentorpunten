from django.contrib.auth import get_user_model
from django.db.models import Count
from import_export import resources
from import_export.fields import Field

from tournaments import models

User = get_user_model()


class TeamResource(resources.ModelResource):
    """Team Resource."""

    def __init__(self, **kwargs):
        """Initialize Team Resource."""
        super(TeamResource, self).__init__(**kwargs)
        self.added_members_fullname_fields = dict()

    def get_maximum_members_of_team(self, queryset) -> int:
        """Get maximum members of team."""
        member_count_list = queryset.annotate(member_count=Count("members")).order_by(
            "-member_count"
        )
        if member_count_list.count() > 0:
            return member_count_list.first().member_count
        else:
            return 0

    def before_export(self, queryset, *args, **kwargs):
        """Initialize by creating a field for each member ID."""
        maximum_member_count = self.get_maximum_members_of_team(queryset)

        for i in range(1, maximum_member_count + 1):
            attribute_id = f"member__fullname__{i}"
            self.fields[attribute_id] = Field(
                column_name=attribute_id, attribute=attribute_id, readonly=True
            )
            self.added_members_fullname_fields[attribute_id] = i - 1

    def export_members_field(self, field, obj):
        """Export the custom members fields."""
        member_iterator = self.added_members_fullname_fields[field.attribute]
        if obj.members.all().count() > member_iterator:
            return obj.members.all()[member_iterator]
        return None

    def export_field(self, field, obj):
        """Check for added member fields before exporting."""
        if field.attribute in self.added_members_fullname_fields.keys():
            return self.export_members_field(field, obj)
        else:
            return super(TeamResource, self).export_field(field, obj)

    def must_import_by_fullname_members(self, row):
        """Test whether import by fullname members must be run."""
        return "member__fullname__1" in row.keys()

    def must_import_by_username_members(self, row):
        """Test whether import by username members must be run."""
        return "member__username__1" in row.keys()

    def lookup_member_fullname(self, member_full_name):
        """Lookup a member in storage by full name."""
        try:
            return User.objects.get(full_name=member_full_name)
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            return None

    def lookup_member_username(self, member_username):
        """Lookup a member in storage by username."""
        try:
            return User.objects.get(username=member_username)
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            return None

    def construct_member_ids_from_fullname_columns(self, row):
        """Construct member ids from member__ key columns."""
        next_member_column_id = 1
        next_member_column_name = "member__fullname__{}".format(next_member_column_id)
        members = []
        while next_member_column_name in row.keys():
            next_member = row[next_member_column_name]

            if next_member:
                member_obj = self.lookup_member_fullname(next_member)
                if member_obj is not None:
                    members.append(member_obj.id)

            next_member_column_id = next_member_column_id + 1
            next_member_column_name = "member__fullname__{}".format(
                next_member_column_id
            )
        return ",".join(map(str, members))

    def construct_member_ids_from_username_columns(self, row):
        """Construct member ids from member__ key columns."""
        next_member_column_id = 1
        next_member_column_name = "member__username__{}".format(next_member_column_id)
        members = []
        while next_member_column_name in row.keys():
            next_member = row[next_member_column_name]

            if next_member:
                member_obj = self.lookup_member_username(next_member)
                if member_obj is not None:
                    members.append(member_obj.id)

            next_member_column_id = next_member_column_id + 1
            next_member_column_name = "member__username__{}".format(
                next_member_column_id
            )
        return ",".join(map(str, members))

    def before_import_row(self, row, row_number=None, **kwargs):
        """Get the team members as names, if they exist."""
        members_column = row.get("members", None)
        if members_column is not None:
            # Members column is used.
            return

        if self.must_import_by_fullname_members(row):
            # Key value full name columns used.
            row["members"] = self.construct_member_ids_from_fullname_columns(row)
        elif self.must_import_by_username_members(row):
            # Key value username columns used.
            row["members"] = self.construct_member_ids_from_username_columns(row)

    class Meta:
        """Meta class."""

        model = models.Team
        fields = [
            "id",
            "name",
            "tournament",
            "members",
            "points_account",
            "coins_account,",
        ]
        export_order = [
            "id",
            "name",
            "tournament",
            "members",
            "points_account",
            "coins_account",
        ]
