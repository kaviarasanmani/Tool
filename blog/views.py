# views.py
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import api_view
from .models import Banner, Category, Tag, Post, Like, Comment, Follow
from .serializers import (
    CategorySerializer,
    TagSerializer,
    PostSerializer,
    LikeSerializer,
    CommentSerializer,
    FollowSerializer,
    banner_serializer,
    blogSerializer,
)
from .permissions import IsAuthorOrAdmin
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .score import *

class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Category instances."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Tag instances."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Post instances."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]

    def perform_create(self, serializer):
        """Save the post instance with the current user as the author."""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["get"], url_path="likes-count")
    def likes_count(self, request, pk=None):
        """Returns the number of likes for a specific post."""
        post = self.get_object()
        likes_count = (
            post.likes.count()
        )  # Assuming your Like model has a related name 'likes' in Post model
        return Response({"likes_count": likes_count}, status=status.HTTP_200_OK)


class LikeViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Like instances."""

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def toggle_like(self, request, pk=None):
        post = Post.objects.get(pk=pk)  # Get the post by ID
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()  # If like already existed, delete it
            return Response(
                {"status": "like removed"}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response({"status": "like added"}, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Comment instances."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdmin]

    def perform_create(self, serializer):
        """Save the comment instance with the current user as the user."""
        serializer.save(user=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Follow instances."""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Create a follow relationship, setting the current user as the follower."""
        serializer.save(follower=self.request.user)


class BlogList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = blogSerializer


class BlogRetrive(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = blogSerializer


class Bannerviewset(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = banner_serializer


class Bannerviewset_Active(viewsets.ModelViewSet):
    serializer_class = banner_serializer

    def get_queryset(self):
        banner_category = self.request.query_params.get("banner_category")

        queryset = Banner.objects.filter(status="active")

        if banner_category:
            queryset = queryset.filter(banner_category=banner_category)

        return queryset

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .score import (
    initialize_youtube_client,
    get_channel_details,
    get_recent_video_ids,
    fetch_video_comments,
    sentiment_analysis,
    get_video_engagement_metrics,
    calculate_trust_score,
    API_KEY
)

@api_view(['POST'])
def calculate_trust_score_view(request):
    youtube = initialize_youtube_client(API_KEY)
    channel_id = request.data.get('channel_id')
    if channel_id:
        channel_details = get_channel_details(youtube, channel_id)
        if channel_details:
            video_ids = get_recent_video_ids(youtube, channel_id)
            engagement_metrics = get_video_engagement_metrics(youtube, video_ids)
            all_comments = []
            for video_id in video_ids:
                comments = fetch_video_comments(youtube, video_id)
                all_comments.extend(comments)
            sentiment_score = sentiment_analysis(all_comments)
            trust_score = calculate_trust_score(channel_details, engagement_metrics, sentiment_score)
            return Response({'trust_score': trust_score})
        else:
            return Response({'error': 'Channel details not found.'}, status=400)
    else:
        return Response({'error': 'Channel ID not provided.'}, status=400)
