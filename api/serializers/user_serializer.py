from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_email(self, email):
        user = User.objects.filter(email=email).first()
        if user:
            raise serializers.ValidationError("User with this email already existing")
        return email

    def validate_username(self, username):
        user = User.objects.filter(username=username).first()
        if user:
            raise serializers.ValidationError("User with this username already existing")
        return username

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user