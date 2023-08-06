from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from challenges.models import Submission
from transactions.models import Transaction

User = get_user_model()


@receiver(pre_save, sender=Submission)
def create_transaction_on_accept(sender, instance: Submission, **kwargs):
    """Create a Transaction for the amount of points of the challenge when a submission gets accepted."""
    if instance.transaction is not None:
        # Submissions with a Transaction don't get a new Transaction.
        return instance

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
        # Submission is being created with accepted == True (obj is None) OR Submission is being edited and the accepted
        # value is being set to True now.
        instance.transaction = Transaction.objects.create(
            account=instance.team.account,
            amount=instance.challenge.points,
            description=f"Completed challenge {instance.challenge.name}",
        )

    return instance
