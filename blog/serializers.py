from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Category, Tag, Post, Like, Comment, Follow,Banner , BannerCategory

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    author = UserSerializer(read_only=True)  # Include author details in serialized data

    class Meta:
        model = Post
        fields = "__all__"

    def create(self, validated_data):
        categories_data = validated_data.pop("categories", [])
        tags_data = validated_data.pop("tags", [])
        post = Post.objects.create(**validated_data)
        post.categories.set(categories_data)
        post.tags.set(tags_data)
        return post


# class LikeSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)  # Include user details in serialized data


#     class Meta:
#         model = Like
#         fields = '__all__'
class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Assuming UserSerializer is properly secure

    class Meta:
        model = Like
        fields = ["id", "post", "user", "created_at"]

    def validate(self, data):
        user = self.context["request"].user
        post = data["post"]
        if Like.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError("You have already liked this post.")
        return data


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Include user details in serialized data

    class Meta:
        model = Comment
        fields = "__all__"


class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    followed = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = "__all__"


class CommentSerializerList(serializers.ModelSerializer):
    user = (
        serializers.StringRelatedField()
    )  # Displays the username of the author # Display the username directly

    class Meta:
        model = Comment
        fields = ("id", "user", "content")


class blogSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # Displays the username of the author
    comments = CommentSerializerList(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    categories = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    featured_image = serializers.ImageField(use_url=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "slug",
            "author",
            "content",
            "excerpt",
            "created_at",
            "updated_at",
            "published_at",
            "status",
            "categories",
            "tags",
            "featured_image",
            "comments",
            "likes_count",
            "comments_count",
        )

    def get_likes_count(self, obj):
        return Like.objects.filter(post=obj).count()

    def get_comments_count(self, obj):
        return obj.comments.count()  #


class banner_serializer(serializers.ModelSerializer):
    class Meta:
        
        model = Banner
        fields = "__all__"