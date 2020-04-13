from django.db import models
from django.contrib.auth.models import User
from enum import Enum


class SlotStatus(Enum):   # A subclass of Enum
    AVAILABLE = "Available"
    COMPLETED = "Completed"
    EXPIRED = "Expired"
    BOOKED = "Booked"


class Slot(models.Model):
    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    booked_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='my_booked_slots')
    start_time = models.DateTimeField()
    duration = models.DurationField()
    status = models.CharField(max_length=50, choices=[(status, status.value) for status in SlotStatus], default=SlotStatus.AVAILABLE)

    class Meta:
        managed = True
        db_table = 'slot'

    @classmethod
    def get_by_user(cls, user_id):
        return cls.objects.filter(booked_by_id=user_id, status=SlotStatus.BOOKED)
