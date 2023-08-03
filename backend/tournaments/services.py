from django.contrib.auth import get_user_model

from tournaments.models import Tournament, Team

User = get_user_model()


def get_team_for_user(user: User, tournament: Tournament):
    """
    Get the team a User is in for a specific Tournament.

    We can not enforce at the database level that a User is in multiple Teams for a specific Tournament, that is why
    it could happen that the database becomes partly corrupted and a User is registered for multiple Teams for a
    Tournament. In such cases, we always pick the first Team as the Team a User is participating in. Always use this
    function to retrieve the Team for a specific User.
    """
    return Team.objects.filter(members__in=[user], tournament=tournament).first()
