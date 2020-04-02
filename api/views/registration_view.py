from rest_framework.response import Response
from rest_framework import views, status
from datetime import datetime

from api.serializers.slot_serializer import SlotSerializer, BookSlotSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from api.serializers.user_serializer import UserSerializer


class RegistrationView(views.APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)