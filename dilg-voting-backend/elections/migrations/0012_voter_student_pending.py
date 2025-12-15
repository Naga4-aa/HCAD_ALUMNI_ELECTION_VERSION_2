from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("elections", "0011_voter_name_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="voter",
            name="student_id",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="voter",
            name="is_approved",
            field=models.BooleanField(default=False),
        ),
    ]
