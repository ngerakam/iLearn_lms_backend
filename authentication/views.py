import time, datetime, random, string
from django.core.mail import send_mail
from rest_framework import exceptions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from .models import User, UserProfile
from .serializers import UserSerializer, ProfileUserSerializer

class RegisterAPIView(APIView):
    def post(self, request):
            data = request.data

            # create a user
            if data['selectedRole'] == 'admin':
                user = User.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    is_teacher = False,
                    is_student = False,
                    is_superuser = True
                )
                user.set_password(data['first_name'])
                user.save()
            elif data['selectedRole'] == 'student':
                user = User.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    is_teacher = False,
                    is_student = True,
                    is_superuser = False
                )
                user.set_password(data['first_name'])
                user.save()
            elif data['selectedRole'] == 'teacher':
                user = User.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    is_teacher = True,
                    is_student = False,
                    is_superuser = False
                )
                user.set_password(data['first_name'])
                user.save()

            # Delay for 2 seconds
            time.sleep(2)
            # Retrieve the user's profile
            profile, created = UserProfile.objects.get_or_create(user=user)

            if data['gender'] == '':
                profile.gender="None"
            else:
                profile.gender = data['gender']

            profile.save()

            serializer = UserSerializer(user)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()

            return Response(serializer.data)
    
class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect password')

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({'message': 'success'}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite='Lax'
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite='Lax'
        )

        return response

class UserProfileAPIView(APIView):

    def get(self, request, pk=None):
        user = request.user
        profile = UserProfile.objects.filter(user=user).first()

        if profile:
            serializer = ProfileUserSerializer(profile)
            return Response(serializer.data)
        else:
            return Response({"message": "This profile is not found"}, status=404)


class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response({'message': 'success'}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite='Lax'
        )

        return response
