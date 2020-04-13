from django.contrib.auth.models import User, Group
from rest_framework import serializers
from datetime import date, datetime, timedelta
from api.models.slot import Slot, SlotStatus


class BaseSlotSerializer(serializers.Serializer):

    def validate_date(self, input_date):
        today = date.today()
        if input_date < today:
            raise serializers.ValidationError("Date should be of future")
        return input_date

    def time_difference(self, end_time, start_time):
        return datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)

    def get_duration(self, duration):
        if 'h' in duration:
            return timedelta(hours=int(duration[0:-1]))
        if 'm' in duration:
            return timedelta(minutes=int(duration[0:-1]))


class SlotSerializer(BaseSlotSerializer):
    date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    duration = serializers.CharField(default='1h')

    def validate(self, data):
        if data["start_time"] > data["end_time"]:
            raise serializers.ValidationError("Start time should be smaller than end_time")
        if (self.time_difference(data["end_time"], data["start_time"])).seconds % 3600 != 0:
            raise serializers.ValidationError("Difference between start and end time should be only in hours")
        return data

    def create(self, validated_data):
        time_diff = self.time_difference(validated_data["end_time"], validated_data["start_time"])
        slots = []
        for i in range(0, int(time_diff.seconds/3600)):
            start_datetime = datetime.combine(validated_data["date"], validated_data["start_time"])
            # TODO : created_by_id
            slot = Slot.objects.create(start_time=self.get_start_time(start_datetime, i),
                                       duration=self.get_duration(validated_data["duration"]),
                                       created_by=validated_data["created_by"])
            slots.append(slot)
        return validated_data

    def get_start_time(self, start_time, delta):
        return start_time.replace(hour=start_time.hour + delta)


class SlotViewSerializer(BaseSlotSerializer):
    start_time = serializers.DateTimeField()
    duration = serializers.CharField(default='1h')


class BookSlotSerializer(BaseSlotSerializer):
    date = serializers.DateField()
    start_time = serializers.TimeField()
    duration = serializers.CharField(default='1h')

    def validate(self, data):
        start_datetime = datetime.combine(data["date"], data["start_time"])
        slot = Slot.objects.filter(start_time=start_datetime, status= SlotStatus.AVAILABLE).first()
        if slot:
            data["slot"] = slot
        else:
            raise serializers.ValidationError("Slot is not available for the requested time.")
        return data

    def create(self, validated_data):
        slot = validated_data["slot"]
        slot.booked_by = validated_data["booked_by"]
        slot.status = SlotStatus.BOOKED
        slot.save()
        return validated_data
