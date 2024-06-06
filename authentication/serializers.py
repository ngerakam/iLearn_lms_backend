from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'password', 'is_teacher', 'is_student', 'is_superuser', ]
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
        fields  = ['user', 'sub_county', 'id_number', 'phone_number', 'gender', 'age']