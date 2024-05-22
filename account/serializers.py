from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = UserProfile
        fields = ["user", "user_type"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError(
                "Unable to log in with provided credentials."
            )
        return user

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get("refresh")
        try:

            # Attempt to create a new RefreshToken object from the given refresh token
            refresh = RefreshToken(refresh_token)
            # Return the new access token as part of the validated data
            return {"access": str(refresh.access_token)}
        except TokenError as e:
            # If there is a token error (e.g., token is expired or invalid), raise an InvalidToken exception
            raise InvalidToken from e


class InfluencerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerProfile
        fields = "__all__"


class AgencyProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.user.username")
    first_name = serializers.ReadOnlyField(source="user.user.first_name")
    last_name = serializers.ReadOnlyField(source="user.user.last_name")
    email = serializers.ReadOnlyField(source="user.user.email")

    class Meta:
        model = AgencyProfile
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "company_name",
            "contact_person_name",
            "mobile_number",
            "website",
            "category",
            "address",
            "brand_logo",
            "country",
            "facebook_link",
            "twitter_link",
            "instagram_link",
        ]


from rest_framework import serializers
from .models import InfluencerProfile


class InfluencerProfileSerializerList(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.user.username")
    first_name = serializers.ReadOnlyField(source="user.user.first_name")
    last_name = serializers.ReadOnlyField(source="user.user.last_name")
    email = serializers.ReadOnlyField(source="user.user.email")

    class Meta:
        model = InfluencerProfile
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "mobile_number",
            "gender",
            "birthday_date",
            "language",
            "category",
            "city",
            "postcode",
            "address",
            "country",
            "bio",
            "facebook_link",
            "twitter_link",
            "instagram_link",
            "youtube_link",
            "profile_pic",
        ]
