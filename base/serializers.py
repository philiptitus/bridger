from rest_framework import serializers
from .models import CustomUser as Userr
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
import json
from dataclasses import field
from rest_framework import serializers
from string import ascii_lowercase, ascii_uppercase
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import *
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from .utils import *








class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    bio = serializers.SerializerMethodField(read_only=True)
    date_joined = serializers.SerializerMethodField(read_only=True)



    




    class Meta:
        model = Userr
        fields = '__all__'


    def get__id(self, obj):
        return obj.id
    
    def get_isAdmin(self, obj):
        return obj.is_staff

        
    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email

        return name
    
    def get_bio(self, obj):
        bio = obj.bio


        return bio
    
    def get_avi(self, obj):
        avi = obj.avi


        return avi


    def get_date_joined(self, obj):
        date_joined = obj.date_joined


        return date_joined
    

    



class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Userr
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'bio', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    





class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if Userr.objects.filter(email=email).exists():
            user = Userr.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            abslink = f"http://localhost:3000/#/password-reset-confirm/{uidb64}/{token}/"
            print(abslink)
            email_body = f"Hi {user.first_name}, use the link below to reset your password: {abslink} Hurry Up The Link Expires in Two Minutes"
            data = {
                'email_body': email_body,
                'email_subject': "Reset your Password",
                'to_email': user.email
            }
            send_normal_email(data)

        return super().validate(attrs)
    

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=3, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = Userr.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Reset link is invalid or has expired", 401)

            if password != confirm_password:
                raise AuthenticationFailed("Passwords do not match")

            # Validate password using Django's password validators
            try:
                validate_password(password, user)
            except ValidationError as e:
                raise ValidationError(detail=str(e))

            user.set_password(password)
            user.save()

            # Send email notifying the user of the password change
            email_body = f"Hi {user.first_name}, your password For GALLERY has been successfully changed If This Was Not You Change It Back Immediately."
            email_subject = "Password Change Notification"
            to_email = user.email
            data = {
                'email_body': email_body,
                'email_subject': email_subject,
                'to_email': to_email
            }
            send_normal_email(data)

            return user
        except Exception as e:
            raise AuthenticationFailed("Link is invalid or has expired")


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'



class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class SavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Savings
        fields = '__all__'


















