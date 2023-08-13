# Generated by Django 4.2.3 on 2023-08-12 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tournaments", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="team",
            old_name="account",
            new_name="points_account",
        ),
        migrations.AlterField(
            model_name="team",
            name="tournament",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="teams",
                to="tournaments.tournament",
            ),
        ),
    ]