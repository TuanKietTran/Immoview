import uuid
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("agencies", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("is_superuser", models.BooleanField(default=False, verbose_name="superuser status")),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="last name")),
                ("is_staff", models.BooleanField(default=False, verbose_name="staff status")),
                ("is_active", models.BooleanField(default=True, verbose_name="active")),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("is_staff_immoview", models.BooleanField(default=False)),
            ],
            options={"db_table": "users", "abstract": False},
        ),
        migrations.AddField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.CreateModel(
            name="Membership",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("role", models.CharField(
                    choices=[("owner", "Owner"), ("admin", "Admin"), ("agent", "Agent"), ("viewer", "Viewer")],
                    default="agent",
                    max_length=20,
                )),
                ("is_active", models.BooleanField(default=True)),
                ("joined_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="memberships",
                    to=settings.AUTH_USER_MODEL,
                )),
                ("agency", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="memberships",
                    to="agencies.agencymodel",
                )),
            ],
            options={"db_table": "memberships"},
        ),
        migrations.AddIndex(
            model_name="membership",
            index=models.Index(fields=["user", "is_active"], name="memberships_user_active_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="membership",
            unique_together={("user", "agency")},
        ),
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("actor_user_id", models.UUIDField(blank=True, null=True)),
                ("actor_membership_id", models.UUIDField(blank=True, null=True)),
                ("action", models.CharField(max_length=100)),
                ("resource_type", models.CharField(max_length=50)),
                ("resource_id", models.CharField(max_length=100)),
                ("agency_id", models.UUIDField(blank=True, db_index=True, null=True)),
                ("ip", models.GenericIPAddressField(blank=True, null=True)),
                ("user_agent", models.TextField(blank=True)),
                ("trace_id", models.CharField(blank=True, max_length=64)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={"db_table": "audit_log", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="ApiKey",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("role", models.CharField(
                    choices=[("owner", "Owner"), ("admin", "Admin"), ("agent", "Agent"), ("viewer", "Viewer")],
                    default="agent",
                    max_length=20,
                )),
                ("key_prefix", models.CharField(max_length=16)),
                ("key_hash", models.CharField(max_length=64)),
                ("last_used_at", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("agency", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="api_keys",
                    to="agencies.agencymodel",
                )),
                ("created_by", models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name="created_api_keys",
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={"db_table": "api_keys"},
        ),
    ]
