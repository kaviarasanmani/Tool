from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Bannerviewset, Bannerviewset_Active, CategoryViewSet, TagViewSet, PostViewSet, LikeViewSet, CommentViewSet, FollowViewSet,BlogList,BlogRetrive,calculate_trust_score_view
from django.conf import settings
from django.conf.urls.static import static

# Creating a router and registering our viewsets with it.
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'posts', PostViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'follows', FollowViewSet)
router.register(r'Banner', Bannerviewset)
router.register(r'banner_active',Bannerviewset_Active, basename="banner_active")


urlpatterns = [
    path('blog/', include(router.urls)), 
    path('list/',BlogList.as_view(),name="post_list"),   
    path('list/<pk>',BlogRetrive.as_view(),name="pk"),
    path('calculate-trust-score/', calculate_trust_score_view, name='calculate_trust_score'),


]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
