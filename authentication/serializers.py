from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'password', 'is_teacher', 'is_student', 'is_admin', ]
        extra_kwargs = {
            'password': {'write_only': True },
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class ProfileUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields  = ['user',  'gender', 'about_me', 'get_profile_image']


class SiteAboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteAbout
        fields = ['about_message']

class SiteAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteAddress
        fields = ['email_contact', 'phone_contact', 'location_address']

class SiteSetupSerializer(serializers.ModelSerializer):
    abouts = SiteAboutSerializer()
    addresses = SiteAddressSerializer()

    class Meta:
        model = SiteSetup
        fields = [
            'title', 'card1_name', 'card1', 'card2_name', 'card2',
            'card3_name', 'card3', 'hero_name', 'hero_message',
            'get_site_image', 'abouts', 'addresses'
        ]
