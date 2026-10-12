from django.contrib import admin

from .infrastructure.models import ListingAuditEvent, ListingModel, PhotoModel


@admin.register(ListingModel)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "offer_type", "duplicate_key", "created_at")
    list_filter = ("status", "offer_type")
    search_fields = ("title", "city", "postcode", "duplicate_key")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ListingAuditEvent)
class ListingAuditEventAdmin(admin.ModelAdmin):
    list_display = ("listing", "from_status", "to_status", "actor_id", "created_at")
    list_filter = ("from_status", "to_status")
    readonly_fields = [field.name for field in ListingAuditEvent._meta.fields]


@admin.register(PhotoModel)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("listing", "order", "processed", "created_at")
