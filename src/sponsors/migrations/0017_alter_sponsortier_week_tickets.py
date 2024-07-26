# Generated by Django 4.2.10 on 2024-07-11 20:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sponsors", "0016_rename_tickets_sponsortier_week_tickets"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sponsortier",
            name="week_tickets",
            field=models.IntegerField(
                help_text="The number of full week tickets generated for a sponsor in this tier."
            ),
        ),
    ]
