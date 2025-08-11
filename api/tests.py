from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Device, Payload
import base64

class PayloadAPITests(APITestCase):

    def setUp(self):
        # Create user & token
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)

        # Create a device
        self.device = Device.objects.create(devEUI="abcdabcdabcdabcd")

        # Endpoint
        self.url = reverse('payloads-list')

        # Common headers
        self.headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}

    def test_create_passing_payload(self):
        """Test creating a payload where data=1 (Base64 'AQ==')"""
        payload_data = {
            "fCnt": 100,
            "devEUI": self.device.devEUI,
            "data": base64.b64encode(b'\x01').decode(),  # AQ==
            "rxInfo": [{"gatewayID": "1234123412341234", "name": "G1", "time": "2022-07-19T11:00:00", "rssi": -57, "loRaSNR": 10}],
            "txInfo": {"frequency": 86810000, "dr": 5}
        }

        response = self.client.post(self.url, payload_data, format='json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload = Payload.objects.get(fCnt=100, device=self.device)
        self.assertEqual(payload.status, "passing")
        self.device.refresh_from_db()
        self.assertEqual(self.device.status, "passing")

    def test_create_failing_payload(self):
        """Test creating a payload where data != 1"""
        payload_data = {
            "fCnt": 101,
            "devEUI": self.device.devEUI,
            "data": base64.b64encode(b'\x02').decode(),
            "rxInfo": [],
            "txInfo": {}
        }

        response = self.client.post(self.url, payload_data, format='json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload = Payload.objects.get(fCnt=101, device=self.device)
        self.assertEqual(payload.status, "failing")
        self.device.refresh_from_db()
        self.assertEqual(self.device.status, "failing")

    def test_duplicate_fcnt_rejected(self):
        """Test that duplicate fCnt for the same device is rejected"""
        Payload.objects.create(
            device=self.device,
            fCnt=100,
            data_hex="01",
            status="passing",
            rx_info={},
            tx_info={}
        )

        payload_data = {
            "fCnt": 100,
            "devEUI": self.device.devEUI,
            "data": base64.b64encode(b'\x01').decode(),
            "rxInfo": [],
            "txInfo": {}
        }

        response = self.client.post(self.url, payload_data, format='json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
