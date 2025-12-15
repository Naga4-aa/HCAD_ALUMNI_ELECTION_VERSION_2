from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("elections", "0012_voter_student_pending"),
    ]

    operations = [
        migrations.AddField(
            model_name="voter",
            name="pin_reset_requested",
            field=models.BooleanField(default=False),
        ),
    ]
