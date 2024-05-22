from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Banner, BannerCategory, Category, Tag, Post, Like, Comment, Follow

admin.site.register(Banner)
admin.site.register(BannerCategory)

User = get_user_model()

# Inline Admins
class LikeInline(admin.TabularInline):
    model = Like
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class FollowInline(admin.TabularInline):
    model = Follow
    fk_name = 'follower'  # Specify the foreign key in case of ambiguity
    extra = 1

# Custom Admin actions
def make_published(modeladmin, request, queryset):
    queryset.update(status='published')
make_published.short_description = "Mark selected posts as Published"

# Model Admins
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'published_at')
    list_filter = ('status', 'created_at', 'published_at', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)
    actions = [make_published]
    inlines = [LikeInline, CommentInline]

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user  # Set author to current user, if not set
        super().save_model(request, obj, form, change)

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']

class CustomUserAdmin(BaseUserAdmin):
    inlines = [FollowInline]
    list_display = BaseUserAdmin.list_display + ('is_staff',)  # Example extension

# Register your models here
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.unregister(User)  # Unregister the original admin to avoid conflicts
admin.site.register(User, CustomUserAdmin)
