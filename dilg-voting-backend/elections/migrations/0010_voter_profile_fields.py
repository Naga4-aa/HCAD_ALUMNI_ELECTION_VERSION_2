from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("elections", "0009_accessgate"),
    ]

    operations = [
        migrations.AddField(
            model_name="voter",
            name="alumni_id",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="voter",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="voter",
            name="degree_program",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name="voter",
            name="employment_status",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="voter",
            name="industry_field",
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
