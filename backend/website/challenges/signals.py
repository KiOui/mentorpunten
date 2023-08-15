from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver

from challenges.models import Submission
from transactions.models import Transaction

User = get_user_model()


@receiver(pre_save, sender=Submission)
def create_transactions_on_accept(sender, instance: Submission, **kwargs):
    """Create a Transaction for the amount of points of the challenge when a submission gets accepted."""
    if instance.accepted is None or instance.accepted is False:
        # Submissions that are not accepted don't get a Transaction.
        return instance

    # Get the old Submission (if it exists).
    try:
        obj: Submission | None = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # On create
        obj = None

    if obj is None or (obj.accepted is None or obj.accepted is False):
        # Submission is being created with accepted == True (obj is None) OR Submission is being edited and the
        # accepted value is being set to True now.
        if instance.points_transaction is None:
            instance.points_transaction = Transaction.objects.create(
                account=instance.team.points_account,
                amount=instance.challenge.points,
                description=f"Completed challenge {instance.challenge.name}",
            )

        if (
            instance.coins_transaction is None
            and instance.team.coins_account is not None
        ):
            instance.coins_transaction = Transaction.objects.create(
                account=instance.team.coins_account,
                amount=instance.challenge.points,
                description=f"Completed challenge {instance.challenge.name}",
            )

    return instance
