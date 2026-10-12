from django.contrib import admin

from .models import IngestDeadLetter, IngestRun, RawLanding


@admin.register(IngestRun)
class IngestRunAdmin(admin.ModelAdmin):
    list_display = ("source", "status", "fetched_count", "imported_count", "error_count", "started_at")
    list_filter = ("source", "status")
    readonly_fields = [field.name for field in IngestRun._meta.fields]


@admin.register(RawLanding)
class RawLandingAdmin(admin.ModelAdmin):
    list_display = ("source", "external_id", "payload_hash", "fetched_at", "replayed_at")
    search_fields = ("source", "external_id", "payload_hash")
    readonly_fields = [field.name for field in RawLanding._meta.fields]


@admin.register(IngestDeadLetter)
class IngestDeadLetterAdmin(admin.ModelAdmin):
    list_display = ("source", "external_id", "status", "attempts", "created_at")
    list_filter = ("source", "status")
    actions = ("replay", "discard")

    @admin.action(description="Replay selected ingest dead letters")
    def replay(self, request, queryset):
        queryset.update(status="replay_requested")

    @admin.action(description="Discard selected ingest dead letters")
    def discard(self, request, queryset):
        queryset.update(status="discarded")
