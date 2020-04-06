from django.test import TestCase
from rest_framework.test import APIClient
from api.models.slot import Slot
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import date, datetime, timedelta
import json


class TestSlotApi(TestCase):

    def setUp(self):
        self.slot = Slot.objects.create(start_time='2021-01-01 10:00', duration=timedelta(hours=1))
        self.admin = User.objects.create(username="admin", email="admin@yopmail.com", password="admin123")
        self.client = APIClient()
        # token = Token.objects.get(user__username=self.admin.username)
        self.client.force_authenticate(user=self.admin)

    def test_create_slot_with_past_date(self):
        request_body = {
            "date": "2019-06-06",
            "start_time": "13:30:00",
            "end_time": "15:30:00",
            "duration": "1h"
        }
        response = self.client.post("/api/v1/slots/", request_body, format='json')
        self.assertEqual(response.status_code, 400)
        response_body = json.loads(response.content)
        self.assertDictEqual(response_body, {"date":["Date should be of future"]})

    def test_create_slot_with_invalid_date_format(self):
        request_body = {
            "date": "2019-16-06",
            "start_time": "13:30:00",
            "end_time": "15:30:00"
        }
        response = self.client.post("/api/v1/slots/", request_body, format='json')
        self.assertEqual(response.status_code, 400)
        response_body = json.loads(response.content)
        self.assertDictEqual(response_body, {"date":["Date has wrong format. Use one of these formats instead: YYYY-MM-DD."]})

    def test_create_slot_with_invalid_start_time(self):
        request_body = {
            "date": "2050-06-06",
            "start_time": "33:30:00",
            "end_time": "15:30:00"
        }
        response = self.client.post("/api/v1/slots/", request_body, format='json')
        self.assertEqual(response.status_code, 400)
        response_body = json.loads(response.content)
        self.assertDictEqual(response_body, {'start_time': ['Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]].']})

    def test_create_slot_with_invalid_end_time(self):
        request_body = {
            "date": "2050-06-06",
            "start_time": "13:30:00",
            "end_time": "25:30:00",
        }
        response = self.client.post("/api/v1/slots/", request_body, format='json')
        self.assertEqual(response.status_code, 400)
        response_body = json.loads(response.content)
        self.assertDictEqual(response_body, {"end_time":["Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]]."]})

    def test_create_slot_without_authentication(self):
        request_body = {
            "date": "2050-06-06",
            "start_time": "13:30:00",
            "end_time": "15:30:00",
        }
        self.client.force_authenticate(user=None)
        response = self.client.post("/api/v1/slots/", request_body, format='json')
        self.assertEqual(response.status_code, 401)

    def test_create_slot_with_valid_data(self):
        request_body = {
            "date": "2050-06-06",
            "start_time": "13:30:00",
            "end_time": "15:30:00",
        }
        response = self.client.post("/api/v1/slots/", request_body, format='json')
        self.assertEqual(response.status_code, 200)
        slots = Slot.objects.filter(start_time__gte='2050-06-06')
        self.assertEqual(len(slots), 2)
