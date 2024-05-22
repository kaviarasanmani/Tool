from django.urls import path
from .views import RegisterView, LoginView, RefreshTokenView,LogoutView,InfluencerListCreateView, AgencyListView,get_location_info
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet
from django.conf import settings
from django.conf.urls.static import static

from blog.views import *

# router = DefaultRouter()
# router.register(r'userprofiles', UserProfileViewSet,basename='userprofile')




urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('influencers/', InfluencerListCreateView.as_view(), name='influencer-list-'),
    path('agency/', AgencyListView.as_view(), name='agency-list-'),
    path('api/location/', get_location_info, name='location-info'),


]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
