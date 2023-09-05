from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')

class ChefAccountSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = ChefUser
        fields = ('id', 'email', 'first_name', 'last_name','password', 'password_repeat', 'bio', 'profile_picture')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_repeat', None)
        profile_picture = validated_data.pop('profile_picture', None)
        chef_account = ChefUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            bio=validated_data.get('bio', ''),
        )
        chef_account.set_password(validated_data['password'])
        chef_account.save()
        chefs_group, created = Group.objects.get_or_create(name='Chefs')
        chef_account.groups.add(chefs_group)
        if profile_picture:
            chef_account.profile_picture = profile_picture
            chef_account.save()
        return chef_account

class ChefLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Unable to login with given credentials")
        else:
            raise serializers.ValidationError("Must include email and password fields")
        return data
    