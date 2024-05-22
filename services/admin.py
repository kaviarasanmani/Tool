from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Service)
admin.site.register(Category)
admin.site.register(ServiceImage)
admin.site.register(Tag)
admin.site.register(Orders)