# Generated by Django 4.2.3 on 2023-08-14 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
        ("transactions", "0002_alter_transaction_options"),
        ("tournaments", "0004_team_coins_account"),
    ]

    operations = [
        migrations.AddField(
            model_name="tournament",
            name="store",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="store.store",
            ),
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("price", models.PositiveIntegerField()),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("used", models.BooleanField(default=False)),
                ("used_at", models.DateTimeField(blank=True, null=True)),
                (
                    "item",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="bought_items",
                        to="store.item",
                    ),
                ),
                (
                    "property_of",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="tournaments.team",
                    ),
                ),
                (
                    "transaction",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="transactions.transaction",
                    ),
                ),
            ],
        ),
    ]
