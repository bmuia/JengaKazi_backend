import africastalking
from .utils import generate_otp
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import PhoneOtp

def send_otp(phone_number):
    username = "jengakazi"
    api_key = settings.API_KEY
    africastalking.initialize(username, api_key)
    
    sms = africastalking.SMS

    otp = generate_otp() 
    message = f"Your OTP code is: {otp}"
    recipients = [phone_number] 

    PhoneOtp.objects.update_or_create(
        phone_number=phone_number,
        defaults={"otp": otp}
    )

    try:
        response = sms.send(message, recipients)
        return Response({"message": "OTP sent successfully", "otp": otp, "at_response": response},
                        status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Failed to send OTP", "details": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
