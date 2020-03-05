# Generated by Django 3.0.3 on 2020-02-29 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("program", "0083_auto_20200226_1853"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventproposal",
            name="allow_video_recording",
            field=models.BooleanField(
                default=False,
                help_text="Recordings are made available under the <b>CC BY-SA 4.0</b> license. Uncheck if you do not want the event recorded, or if you cannot accept the license.",
            ),
        ),
        migrations.AlterField(
            model_name="speakerproposal",
            name="email",
            field=models.EmailField(
                blank=True,
                help_text="The email of the speaker/artist/host. Defaults to the logged in users email if empty.",
                max_length=150,
            ),
        ),
    ]
