from rest_framework.response import Response
from rest_framework import views, status
from datetime import datetime

from api.models.slot import Slot
from api.serializers.slot_serializer import SlotSerializer, BookSlotSerializer, SlotViewSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class SlotView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        slots = Slot.get_by_user(request.user.id)
        return Response(SlotViewSerializer(slots, many=True).data)


class BookSlotView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookSlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(booked_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)
