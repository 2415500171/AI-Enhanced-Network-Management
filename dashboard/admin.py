from django.contrib import admin

# Register your models here.
from .models import InferenceSnapshot, NetworkReading


@admin.register(NetworkReading)
class NetworkReadingAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "traffic_mbps",
        "latency_ms",
        "packet_loss",
        "bandwidth_util",
        "ids_flag",
        "network_state",
    )
    list_filter = ("ids_flag", "network_state", "timestamp")
    search_fields = ("network_state",)
    ordering = ("-timestamp",)


@admin.register(InferenceSnapshot)
class InferenceSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "total",
        "attacks",
        "congestions",
        "normal",
        "predicted_latency",
        "action_status",
    )
    list_filter = ("action_status", "created_at")
    search_fields = ("action_status", "action_message")
    ordering = ("-created_at",)