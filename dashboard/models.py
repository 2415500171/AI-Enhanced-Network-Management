from django.db import models

# Create your models here.
class NetworkReading(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    traffic_mbps = models.FloatField()
    latency_ms = models.FloatField()
    packet_loss = models.FloatField()
    bandwidth_util = models.FloatField()
    ids_flag = models.BooleanField(default=False)
    network_state = models.CharField(max_length=32, default="Normal")

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Reading {self.timestamp:%Y-%m-%d %H:%M:%S} | state={self.network_state}"


class InferenceSnapshot(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField(default=0)
    attacks = models.PositiveIntegerField(default=0)
    congestions = models.PositiveIntegerField(default=0)
    normal = models.PositiveIntegerField(default=0)
    predicted_latency = models.FloatField(default=0)
    current_traffic = models.FloatField(default=0)
    current_latency = models.FloatField(default=0)
    action_status = models.CharField(max_length=32, default="Normal")
    action_message = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Snapshot {self.created_at:%Y-%m-%d %H:%M:%S} | latency={self.predicted_latency}"