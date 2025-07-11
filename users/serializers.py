from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import PhoneOtp
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User = get_user_model()


class PhoneOtpSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    class Meta:
        model = PhoneOtp
        fields = ['phone_number']


class JobSeekerRegistrationSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['phone_number', 'otp']

    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        otp = validated_data.get('otp', None)
        user = User.objects.create_user(phone_number=phone_number, otp=otp, role='job_seeker')
        return user


class EmployerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'password','role']


    def create(self, validated_data):
        phone = validated_data.get('phone_number', None)
        otp = validated_data.get('otp', None)
        email = validated_data.get('email', None)
        password = validated_data.get('password', None)

        user = User.objects.create_employer(
            email=email,
            password=password,
            role="employer"
        )
        return user


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "bio"]

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.save()
        return instance
    


