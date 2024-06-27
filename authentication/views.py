import time, datetime, random, string, secrets
#
from django.core.mail import send_mail
from django.http import QueryDict
from django.db import transaction
from django.contrib.auth.hashers import make_password
#
from rest_framework import exceptions,status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
#
from .models import User, UserProfile, SiteSetup,SiteAddress, SiteAbout
from .serializers import UserSerializer, ProfileUserSerializer, SiteSetupSerializer

class RegisterAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def generate_random_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for i in range(length))
        return password

    def post(self, request):
        if not request.user.is_superuser:
            return Response({"error": "You are not allowed to access this"})
        data = request.data

        role = data.get('selectedRole')
        user_data = {
            "first_name": data.get('first_name'),
            "last_name": data.get('last_name'),
            "email": data.get('email'),
            "is_teacher": role == 'teacher',
            "is_student": role == 'student',
            "is_superuser": role == 'admin'
        }

        random_password = self.generate_random_password()
        user_data['tfa_secret'] = random_password  # Store the temporary password in tfa_secret

        user = User.objects.create(**user_data)
        user.set_password(random_password)
        user.save()

        # Delay for 2 seconds
        time.sleep(2)

        # Retrieve the user's profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.gender = data.get('gender', 'None')
        profile.save()

        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = User.objects.all()
    
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

class UserRetriveView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        user = User.objects.get(pk=pk)
    
        serializer = UserSerializer(user)

        return Response(serializer.data)
    def put(self, request,pk=None):
        user = User.objects.get(pk=request.data['id'])
        user.email = request.data['email']
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.is_superuser = request.data['is_superuser']
        user.is_teacher = request.data['is_teacher']
        user.is_student = request.data['is_student']
        user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data)
    
    def delete(self,request,pk=None):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({
            "message":f"The user: {user.email} is deleted successfully",
        })
   
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise NotFound("This profile is not found")

        serializer = ProfileUserSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request, pk=None):
        user = User.objects.get(pk=pk)
        profile = UserProfile.objects.get(user=user)
        with transaction.atomic():
            user = User.objects.get(pk=pk)
            profile = UserProfile.objects.get(user=user)

            # Update user's first and last names
            user.first_name = request.data.get('first_name', user.first_name)
            user.last_name = request.data.get('last_name', user.last_name)
            new_password = request.data.get('new_password')
            if new_password:
                user.password = make_password(new_password)  # Hash the new password

            profile.about_me = request.data.get('about_me', profile.about_me)
            profile_image = request.FILES.get('profile_image')
            if profile_image:
                profile.profle_image.save(profile_image.name, profile_image) 

            # Save user and profile models
            user.save()
            profile.save()

            # Serialize the updated profile data
            serializer = ProfileUserSerializer(profile)
            return Response(serializer.data)
class SiteSetupDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            site_setup = SiteSetup.objects.first()  # Assuming there's only one instance
            if not site_setup:
                return Response({"message": "Site setup not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = SiteSetupSerializer(site_setup)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        try:
            site_setup = SiteSetup.objects.first()  # Assuming there's only one instance
            login_image = request.FILES.get('login_image')

            # Convert request.data to QueryDict if it's not already
            if not isinstance(request.data, QueryDict):
                request.data._mutable = True

            # Handle the nested abouts and addresses
            abouts = {
                key.replace('abouts[', '').replace(']', ''): value
                for key, value in request.data.items() if key.startswith('abouts[')
            }

            addresses = {
                key.replace('addresses[', '').replace(']', ''): value
                for key, value in request.data.items() if key.startswith('addresses[')
            }

            if not site_setup:
                # Create a new SiteSetup instance
                site_setup = SiteSetup.objects.create(
                    title=request.data.get('title', ''),
                    card1_name=request.data.get('card1_name', ''),
                    card1=request.data.get('card1', ''),
                    card2_name=request.data.get('card2_name', ''),
                    card2=request.data.get('card2', ''),
                    card3_name=request.data.get('card3_name', ''),
                    card3=request.data.get('card3', ''),
                    hero_name=request.data.get('hero_name', ''),
                    hero_message=request.data.get('hero_message', ''),
                )
            else:
                # Update the existing SiteSetup instance
                site_setup.title = request.data.get('title', site_setup.title)
                site_setup.card1_name = request.data.get('card1_name', site_setup.card1_name)
                site_setup.card1 = request.data.get('card1', site_setup.card1)
                site_setup.card2_name = request.data.get('card2_name', site_setup.card2_name)
                site_setup.card2 = request.data.get('card2', site_setup.card2)
                site_setup.card3_name = request.data.get('card3_name', site_setup.card3_name)
                site_setup.card3 = request.data.get('card3', site_setup.card3)
                site_setup.hero_name = request.data.get('hero_name', site_setup.hero_name)
                site_setup.hero_message = request.data.get('hero_message', site_setup.hero_message)

            if login_image:
                site_setup.login_image.save(login_image.name, login_image)
            
            site_setup.save()

            if abouts:
                print("Abouts received: ", abouts)
                about, _ = SiteAbout.objects.get_or_create(site=site_setup)
                about.about_message = abouts.get('about_message', about.about_message)
                about.save()
                print("About updated: ", about.about_message)
            else:
                print("No abouts")

            if addresses:
                print("Addresses received: ", addresses)
                address, _ = SiteAddress.objects.get_or_create(site=site_setup)
                address.email_contact = addresses.get('email_contact', address.email_contact)
                address.phone_contact = addresses.get('phone_contact', address.phone_contact)
                address.location_address = addresses.get('location_address', address.location_address)
                address.save()
                print("Address updated: ", address.email_contact, address.phone_contact, address.location_address)
            else:
                print("No Addresses")
                
            serializer = SiteSetupSerializer(site_setup)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)