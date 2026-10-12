import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff_immoview", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_staff_immoview = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return self.email


class Role(models.TextChoices):
    OWNER = "owner", "Owner"
    ADMIN = "admin", "Admin"
    AGENT = "agent", "Agent"
    VIEWER = "viewer", "Viewer"


ROLE_RANK: dict[str, int] = {
    Role.VIEWER: 0,
    Role.AGENT: 1,
    Role.ADMIN: 2,
    Role.OWNER: 3,
}


class Membership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "shared.User", on_delete=models.CASCADE, related_name="memberships"
    )
    agency = models.ForeignKey(
        "agencies.AgencyModel", on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.AGENT)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "memberships"
        unique_together = [["user", "agency"]]
        indexes = [models.Index(fields=["user", "is_active"], name="memberships_user_active_idx")]

    def __str__(self) -> str:
        return f"{self.user.email} @ {self.agency_id} ({self.role})"

    def has_min_role(self, min_role: str) -> bool:
        return ROLE_RANK.get(self.role, -1) >= ROLE_RANK.get(min_role, 99)


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor_user_id = models.UUIDField(null=True, blank=True)
    actor_membership_id = models.UUIDField(null=True, blank=True)
    action = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=50)
    resource_id = models.CharField(max_length=100)
    agency_id = models.UUIDField(null=True, blank=True, db_index=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    trace_id = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "audit_log"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.pk and AuditLog.objects.filter(pk=self.pk).exists():
            raise ValueError("AuditLog records are append-only")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("AuditLog records cannot be deleted")


class OutboxEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_type = models.CharField(max_length=120)
    aggregate_type = models.CharField(max_length=80)
    aggregate_id = models.CharField(max_length=100)
    payload = models.JSONField(default=dict)
    status = models.CharField(max_length=20, default="pending")
    attempts = models.PositiveSmallIntegerField(default=0)
    available_at = models.DateTimeField(auto_now_add=True, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "outbox_events"
        indexes = [models.Index(fields=["status", "available_at"])]


class IdempotencyRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=255)
    endpoint = models.CharField(max_length=255)
    request_hash = models.CharField(max_length=64)
    response_code = models.PositiveSmallIntegerField(null=True, blank=True)
    response_body = models.JSONField(null=True, blank=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "idempotency_records"
        constraints = [models.UniqueConstraint(fields=["key", "endpoint"], name="idempotency_key_endpoint")]


class DeadLetterTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_name = models.CharField(max_length=200)
    payload = models.JSONField(default=dict)
    error = models.TextField()
    attempts = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=20, default="pending")
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "dead_letter_tasks"
        indexes = [models.Index(fields=["status", "created_at"])]


class ApiKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agency = models.ForeignKey(
        "agencies.AgencyModel", on_delete=models.CASCADE, related_name="api_keys"
    )
    created_by = models.ForeignKey(
        "shared.User", on_delete=models.SET_NULL, null=True, related_name="created_api_keys"
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.AGENT)
    key_prefix = models.CharField(max_length=16)
    key_hash = models.CharField(max_length=64)
    last_used_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "api_keys"

    def __str__(self) -> str:
        return f"{self.name} ({self.key_prefix}…)"
