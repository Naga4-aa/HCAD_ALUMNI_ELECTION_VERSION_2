# elections/serializers.py
from rest_framework import serializers

from .models import (
    Election,
    Position,
    Candidate,
    Voter,
    Vote,
    Nomination,
    ElectionReminder,
    Notification,
)


class ElectionSerializer(serializers.ModelSerializer):
    phase = serializers.CharField(read_only=True)

    class Meta:
        model = Election
        fields = [
            "id",
            "name",
            "description",
            "nomination_start",
            "nomination_end",
            "voting_start",
            "voting_end",
            "results_at",
            "auto_publish_results",
            "results_published",
            "results_published_at",
            "is_active",
            "mode",
            "demo_phase",
            "phase",
        ]


class PositionSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source="get_name_display", read_only=True)

    class Meta:
        model = Position
        fields = [
            "id",
            "election",
            "name",
            "name_display",
            "is_active",
            "seats",
            "display_order",
        ]


class CandidateSerializer(serializers.ModelSerializer):
    position_name = serializers.CharField(source="position.get_name_display", read_only=True)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = [
            "id",
            "position",
            "position_name",
            "full_name",
            "batch_year",
            "campus_chapter",
            "contact_email",
            "contact_phone",
            "bio",
            "photo",
            "photo_url",
            "is_official",
            "source_nomination",
        ]

    def get_photo_url(self, obj):
        if not obj.photo:
            return None
        request = self.context.get("request") if hasattr(self, "context") else None
        url = obj.photo.url
        return request.build_absolute_uri(url) if request else url


class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = [
            "id",
            "voter_id",
            "student_id",
            "alumni_id",
            "first_name",
            "middle_name",
            "last_name",
            "name",
            "date_of_birth",
            "batch_year",
            "campus_chapter",
            "email",
            "phone",
            "degree_program",
            "employment_status",
            "industry_field",
            "privacy_consent",
            "has_voted",
            "is_active",
            "is_approved",
            "pin_reset_requested",
            "created_at",
        ]
        read_only_fields = ["voter_id", "has_voted", "is_active", "created_at"]


class VoterMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = [
            "name",
            "voter_id",
            "student_id",
            "alumni_id",
            "first_name",
            "middle_name",
            "last_name",
            "has_voted",
            "date_of_birth",
            "batch_year",
            "campus_chapter",
            "email",
            "phone",
            "degree_program",
            "employment_status",
            "industry_field",
            "privacy_consent",
            "is_approved",
            "pin_reset_requested",
        ]


class VoterProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "student_id",
            "alumni_id",
            "date_of_birth",
            "batch_year",
            "campus_chapter",
            "email",
            "phone",
            "degree_program",
            "employment_status",
            "industry_field",
            "privacy_consent",
        ]
        read_only_fields = []


class VoteSerializer(serializers.ModelSerializer):
    voter_name = serializers.CharField(source="voter.name", read_only=True)
    candidate_name = serializers.CharField(source="candidate.full_name", read_only=True)
    position_name = serializers.CharField(source="position.get_name_display", read_only=True)
    election_name = serializers.CharField(source="position.election.name", read_only=True)

    class Meta:
        model = Vote
        fields = [
            "id",
            "voter",
            "voter_name",
            "position",
            "position_name",
            "candidate",
            "candidate_name",
            "election_name",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class VoterRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    middle_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=100)
    student_id = serializers.CharField(max_length=50)
    date_of_birth = serializers.DateField()
    degree_program = serializers.CharField(max_length=200)
    batch_year = serializers.IntegerField()
    campus_chapter = serializers.CharField(max_length=150, required=False, allow_blank=True)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=50)
    employment_status = serializers.CharField(max_length=80)
    industry_field = serializers.CharField(max_length=150)
    privacy_consent = serializers.BooleanField()
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)

    def validate_student_id(self, value):
        value = value.strip()
        if Voter.objects.filter(student_id__iexact=value).exists():
            raise serializers.ValidationError("Student ID already registered.")
        return value

    def validate(self, attrs):
        try:
            year = int(attrs.get("batch_year"))
            if year < 1950 or year > 2100:
                raise serializers.ValidationError({"batch_year": "Batch year looks invalid."})
        except Exception:
            raise serializers.ValidationError({"batch_year": "Batch year is required."})
        if not attrs.get("privacy_consent"):
            raise serializers.ValidationError({"privacy_consent": "Consent is required to register."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        parts = [
            validated_data.get("first_name", "").strip(),
            validated_data.get("middle_name", "").strip(),
            validated_data.get("last_name", "").strip(),
        ]
        validated_data["name"] = " ".join([p for p in parts if p]).strip()
        voter = Voter(**validated_data)
        voter.set_pin(password)
        voter.save()
        return voter

    def validate(self, attrs):
        candidate = attrs.get("candidate")
        position = attrs.get("position")
        if candidate and position and candidate.position_id != position.id:
            raise serializers.ValidationError("Candidate does not belong to the selected position.")
        return attrs


class AdminVoterCreateSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=12)

    class Meta:
        model = Voter
        fields = [
            "id",
            "name",
            "voter_id",
            "batch_year",
            "campus_chapter",
            "email",
            "phone",
            "privacy_consent",
            "pin",
            "has_voted",
            "is_active",
        ]
        read_only_fields = ["voter_id", "has_voted", "is_active"]


class NominationSerializer(serializers.ModelSerializer):
    position_name = serializers.CharField(source="position.get_name_display", read_only=True)
    election_name = serializers.CharField(source="election.name", read_only=True)
    nominator_name = serializers.CharField(source="nominator.name", read_only=True)

    class Meta:
        model = Nomination
        fields = [
            "id",
            "election",
            "election_name",
            "position",
            "position_name",
            "nominator",
            "nominator_name",
            "nominee_full_name",
            "nominee_batch_year",
            "nominee_campus_chapter",
            "contact_email",
            "contact_phone",
            "reason",
            "nominee_photo",
            "is_good_standing",
            "status",
            "rejection_reason",
            "promoted",
            "promoted_at",
            "created_at",
        ]
        read_only_fields = ["nominator", "election", "created_at"]


class NominationCreateSerializer(serializers.Serializer):
    position_id = serializers.IntegerField()
    nominee_full_name = serializers.CharField(max_length=200)
    nominee_batch_year = serializers.IntegerField()
    nominee_campus_chapter = serializers.CharField(max_length=150, required=False, allow_blank=True)
    contact_email = serializers.EmailField(required=False, allow_blank=True)
    contact_phone = serializers.CharField(required=False, allow_blank=True)
    reason = serializers.CharField(required=False, allow_blank=True)
    nominee_photo = serializers.ImageField(required=False, allow_null=True)
    is_good_standing = serializers.BooleanField(required=False)


class BallotSubmitSerializer(serializers.Serializer):
    votes = serializers.DictField(child=serializers.IntegerField())

    def validate(self, attrs):
        if not attrs.get("votes"):
            raise serializers.ValidationError("votes is required")
        return attrs


class AdminStatsSerializer(serializers.Serializer):
    total_voters = serializers.IntegerField()
    total_voted = serializers.IntegerField()
    turnout_percent = serializers.FloatField()


class ElectionReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionReminder
        fields = ["id", "election", "remind_at", "note", "created_at"]
        read_only_fields = ["created_at"]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "type", "message", "is_read", "is_hidden", "created_at"]
        read_only_fields = ["id", "created_at"]
