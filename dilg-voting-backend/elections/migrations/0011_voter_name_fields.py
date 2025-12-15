from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("elections", "0010_voter_profile_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="voter",
            name="first_name",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="voter",
            name="middle_name",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="voter",
            name="last_name",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
