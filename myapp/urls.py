from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site
    path('backend/', admin.site.urls),
    path('api/v1/', include('account.urls')),
    path('api/v1/', include('blog.urls')),
    path('services/',include('services.urls')),

]
