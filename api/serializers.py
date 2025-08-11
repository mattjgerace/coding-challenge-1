from rest_framework import serializers
from .models import Device, Payload
import base64

class PayloadSerializer(serializers.ModelSerializer):
    devEUI = serializers.CharField(write_only=True)
    data = serializers.CharField(write_only=True)
    rxInfo = serializers.JSONField(source='rx_info')
    txInfo = serializers.JSONField(source='tx_info')

    class Meta:
        model = Payload
        fields = [
            'fCnt',
            'devEUI',
            'data',
            'rxInfo',
            'txInfo',
            'data_hex',
            'status',
            'created_at'
        ]
        read_only_fields = ['data_hex', 'status', 'created_at']

    def create(self, validated_data):
        devEUI = validated_data.pop('devEUI')
        data_b64 = validated_data.pop('data')
        rx_info = validated_data.pop('rx_info', None)
        tx_info = validated_data.pop('tx_info', None)

        device, _ = Device.objects.get_or_create(devEUI=devEUI)

        try:
            data_bytes = base64.b64decode(data_b64)
        except Exception:
            raise serializers.ValidationError({"data": "Invalid base64 encoding"})
        data_hex = data_bytes.hex()

        # Determine pass/fail
        status = "passing" if data_hex == "01" else "failing"

        payload = Payload.objects.create(
            device=device,
            fCnt=validated_data['fCnt'],
            data_hex=data_hex,
            status=status,
            rx_info=rx_info,
            tx_info=tx_info
        )

        device.status = status
        device.save()

        return payload