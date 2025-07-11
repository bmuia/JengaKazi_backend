from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (
    PhoneOtpSerializer,
    JobSeekerRegistrationSerializer,
    EmployerRegistrationSerializer,
    UpdateUserProfileSerializer
)
from django.contrib.auth import authenticate
from .api import send_otp
from .models import PhoneOtp, CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated



class SendOtpView(APIView):
    def post(self, request):
        serializer = PhoneOtpSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            return send_otp(phone_number)
        return Response(serializer.errors, status=400)


class JobSeekerRegistrationView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp = request.data.get("otp")

        try:
            phone_otp = PhoneOtp.objects.get(phone_number=phone_number)
        except PhoneOtp.DoesNotExist:
            return Response({'error': 'Phone number not found'}, status=404)

        if phone_otp.otp != otp:
            return Response({'error': 'Invalid OTP'}, status=400)

        serializer = JobSeekerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            phone_otp.delete()
            return Response({'message': 'Job seeker registered successfully'}, status=201)
        return Response(serializer.errors, status=400)


class EmployerRegistrationView(APIView):
    def post(self, request):
        serializer = EmployerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Employer registered successfully'}, status=201)
        return Response(serializer.errors, status=400)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        email = request.data.get('email')
        password = request.data.get('password')

        # 🔓 HACKATHON-STYLE LOGIN: Just Phone Number (for Job Seekers)
        if phone_number and not otp:
            try:
                user = CustomUser.objects.get(phone_number=phone_number)
            except CustomUser.DoesNotExist:
                return Response({"error": "User does not exist"}, status=404)

            tokens = get_tokens_for_user(user)
            return Response({
                "message": "Login successful via phone (no OTP)",
                "tokens": tokens,
                "role": user.role
            })

        # ✅ Standard Phone + OTP (if needed later)
        elif phone_number and otp:
            try:
                phone_otp = PhoneOtp.objects.get(phone_number=phone_number)
            except PhoneOtp.DoesNotExist:
                return Response({"error": "Phone number not found"}, status=404)

            if phone_otp.otp != otp:
                return Response({"error": "Invalid OTP"}, status=400)

            try:
                user = CustomUser.objects.get(phone_number=phone_number)
            except CustomUser.DoesNotExist:
                return Response({"error": "User does not exist"}, status=404)

            phone_otp.delete()
            tokens = get_tokens_for_user(user)
            return Response({
                "message": "Login successful via phone + OTP",
                "tokens": tokens,
                "role": user.role
            })

        # ✅ Email + Password Login (Employer)
        elif email and password:
            user = authenticate(request, email=email, password=password)
            if user:
                tokens = get_tokens_for_user(user)
                return Response({
                    "message": "Login successful via email + password",
                    "tokens": tokens,
                    "role": user.role
                })
            else:
                return Response({"error": "Invalid credentials"}, status=400)

        return Response({"error": "Invalid login request"}, status=400)

 
    
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateUserProfileSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)