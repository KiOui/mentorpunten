# Generated by Django 4.2.3 on 2023-08-12 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("transactions", "0002_alter_transaction_options"),
        ("tournaments", "0003_alter_team_points_account"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="coins_account",
            field=models.OneToOneField(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="coins_team",
                to="transactions.account",
            ),
        ),
    ]
