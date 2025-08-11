from django.db import models

class Device(models.Model):
    devEUI = models.CharField(max_length=32, unique=True)
    status = models.CharField(max_length=10, blank=True, null=True)  # "passing" / "failing"

    def __str__(self):
        return self.devEUI


class Payload(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='payloads')
    fCnt = models.IntegerField()
    data_hex = models.CharField(max_length=255)
    status = models.CharField(max_length=10)  # "passing" / "failing"
    rx_info = models.JSONField()
    tx_info = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('device', 'fCnt')

    def __str__(self):
        return f"{self.device.devEUI} - fCnt:{self.fCnt}"