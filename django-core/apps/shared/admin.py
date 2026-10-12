from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import ApiKey, AuditLog, DeadLetterTask, IdempotencyRecord, Membership, OutboxEvent, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    list_display = ["email", "first_name", "last_name", "is_staff", "is_staff_immoview", "is_active"]
    list_filter = ["is_staff", "is_staff_immoview", "is_active"]
    search_fields = ["email", "first_name", "last_name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_staff_immoview", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "agency", "role", "is_active", "joined_at"]
    list_filter = ["role", "is_active"]
    search_fields = ["user__email", "agency__name"]
    raw_id_fields = ["user", "agency"]


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["action", "resource_type", "resource_id", "actor_user_id", "agency_id", "created_at"]
    list_filter = ["action", "resource_type"]
    search_fields = ["action", "resource_type", "resource_id"]
    readonly_fields = [f.name for f in AuditLog._meta.get_fields()]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(OutboxEvent)
class OutboxEventAdmin(admin.ModelAdmin):
    list_display = ["event_type", "aggregate_type", "aggregate_id", "status", "attempts", "created_at"]
    list_filter = ["status", "event_type"]
    readonly_fields = [f.name for f in OutboxEvent._meta.fields]


@admin.register(IdempotencyRecord)
class IdempotencyRecordAdmin(admin.ModelAdmin):
    list_display = ["key", "endpoint", "response_code", "expires_at", "created_at"]
    search_fields = ["key", "endpoint"]
    readonly_fields = [f.name for f in IdempotencyRecord._meta.fields]


@admin.register(DeadLetterTask)
class DeadLetterTaskAdmin(admin.ModelAdmin):
    list_display = ["task_name", "status", "attempts", "created_at"]
    list_filter = ["status", "task_name"]
    readonly_fields = ["id", "created_at"]


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ["name", "agency", "role", "key_prefix", "is_active", "last_used_at", "created_at"]
    list_filter = ["role", "is_active"]
    search_fields = ["name", "agency__name"]
    readonly_fields = ["key_hash", "key_prefix", "created_at", "last_used_at"]
    raw_id_fields = ["agency", "created_by"]
