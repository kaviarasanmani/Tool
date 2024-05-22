from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(BlacklistedToken)


@admin.register(InfluencerProfile)
class InfluencerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender']
    # search_fields = ['useremail', 'email']
    list_filter = ['gender']

@admin.register(AgencyProfile)
class AgencyProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'contact_person_name']
    search_fields = ['user__email', 'company_name', 'contact_person_name']