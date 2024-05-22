from django.http import JsonResponse
from apiip import apiip
import os

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    InfluencerProfileSerializer,
    UserProfileSerializer,
    LoginSerializer,
    InfluencerProfileSerializerList,
)
from .serializers import TokenRefreshSerializer

from .models import BlacklistedToken
from rest_framework_simplejwt.tokens import AccessToken
from django.utils import timezone
import datetime


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            tokens = serializer.get_tokens(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            access_token = request.headers.get("Authorization").split(" ")[1]
            token = AccessToken(access_token)

            # Blacklist the current token
            BlacklistedToken.objects.create(
                token=access_token,
                user=request.user,
                expiry_date=timezone.now()
                + datetime.timedelta(
                    seconds=token["exp"] - int(timezone.now().timestamp())
                ),
            )

            return Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import viewsets, generics
from .models import UserProfile, InfluencerProfile, AgencyProfile
from .serializers import AgencyProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = None  # No default serializer class set here

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated:
            user_type = user.userprofile.user_type
            if user_type == "creator":
                return InfluencerProfileSerializer
            elif user_type == "agency":
                return AgencyProfileSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            user_type = user.userprofile.user_type
            if user_type == "creator":
                return InfluencerProfile.objects.filter(user=user.userprofile)
            elif user_type == "agency":
                return AgencyProfile.objects.filter(user=user.userprofile)
        return UserProfile.objects.none()

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return super().list(request, *args, **kwargs)


class InfluencerListCreateView(generics.ListCreateAPIView):
    serializer_class = InfluencerProfileSerializerList
    queryset = InfluencerProfile.objects.all()


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AgencyListView(generics.ListCreateAPIView):
    serializer_class = AgencyProfileSerializer
    queryset = AgencyProfile.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0] 
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def get_location_info(request):
    try:
        api_key = '7690f228-ad69-4673-8503-9a7787cd5c99'
        client_ip = get_client_ip(request)
        print(client_ip)

        api_client = apiip(api_key)
        info = api_client.get_location({
            'ip': client_ip,
            'output': "json",
            'fields': "city, countryName, currency.name, ip",
            'languages': "es",
        })
        print(info)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'data': info})