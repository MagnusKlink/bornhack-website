# Generated by Django 3.0.3 on 2020-02-14 00:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("program", "0075_eventfeedback"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventfeedback",
            name="approved",
            field=models.BooleanField(
                default=False,
                help_text="Approve feedback? It will not be visible to Event owner before it is approved.",
            ),
        ),
        migrations.AlterField(
            model_name="eventfeedback",
            name="rating",
            field=models.IntegerField(
                choices=[(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
                help_text="Rating/Score (5 is best)",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="eventfeedback", unique_together={("user", "event")},
        ),
    ]