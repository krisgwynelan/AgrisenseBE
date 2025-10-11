from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import PasswordResetOTP
from .serializers import SensorReadingSerializer, DailySummarySerializer


@api_view(['POST'])
def register_user(request):
    data = request.data
    try:
        if User.objects.filter(email=data['email']).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=data['email'],  # using email as username
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password']
        )
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # check if email exists
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)

        # check password validity
        user = authenticate(username=email, password=password)
        if user is None:
            return Response({'detail': 'Incorrect password.'}, status=status.HTTP_401_UNAUTHORIZED)

        # successful login
        return Response({
            'message': 'Login successful',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def send_reset_otp(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
        otp = get_random_string(length=6, allowed_chars='0123456789')

        # Save or update OTP
        PasswordResetOTP.objects.update_or_create(user=user, defaults={'otp': otp})

        # Send the email
        send_mail(
            'AgriSense Password Reset OTP',
            f'Your OTP for password reset is: {otp}',
            'noreply@agrisense.com',
            [email],
            fail_silently=False,
        )
        return Response({'message': 'OTP sent to your email'}, status=200)
    except User.DoesNotExist:
        return Response({'message': 'Email not found'}, status=404)

@api_view(['POST'])
def verify_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')

    try:
        user = User.objects.get(email=email)
        reset_record = PasswordResetOTP.objects.get(user=user)

        if reset_record.otp == otp:
            return Response({'message': 'OTP verified'}, status=200)
        else:
            return Response({'message': 'Invalid OTP'}, status=400)

    except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
        return Response({'message': 'Invalid request'}, status=400)

@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if new_password != confirm_password:
        return Response({'message': 'Passwords do not match'}, status=400)

    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        # Clean up OTP
        PasswordResetOTP.objects.filter(user=user).delete()

        return Response({'message': 'Password reset successful'}, status=200)

    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=404)



@api_view(['POST'])
def store_sensor_reading(request):
    serializer = SensorReadingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def store_daily_summary(request):
    serializer = DailySummarySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)