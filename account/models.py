from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=10,
        choices=(("creator", "Creator"), ("agency", "Agency"), ("admin", "Admin")),
    )

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def __str__(self):
        return f"Blacklisted token for {self.user}"


class InfluencerProfile(models.Model):
    # user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    mobile_number = models.CharField(_("mobile number"), max_length=15, blank=True)
    GENDER_CHOICES = [
        ("M", _("Male")),
        ("F", _("Female")),
        ("O", _("Other")),
    ]
    gender = models.CharField(
        _("gender"), max_length=1, choices=GENDER_CHOICES, blank=True
    )
    birthday_date = models.DateField(_("birthday date"), null=True, blank=True)
    language = models.CharField(_("language"), max_length=50, blank=True)
    category = models.CharField(_("category"), max_length=50, blank=True)
    city = models.CharField(_("city"), max_length=50, blank=True)
    postcode = models.CharField(_("postcode"), max_length=6, blank=True)
    address = models.CharField(_("address"), max_length=255, blank=True)
    country = models.CharField(_("country"), max_length=100, blank=True)
    bio = models.TextField(_("bio"), blank=True)
    facebook_link = models.URLField(_("Facebook link"), blank=True)
    twitter_link = models.URLField(_("Twitter link"), blank=True)
    instagram_link = models.URLField(_("Instagram link"), blank=True)
    youtube_link = models.CharField(_("Youtube link"),max_length=20,blank= True)
    profile_pic = models.ImageField(
        _("profile picture"), upload_to="profile_pics/", null=True, blank=True
    )


class AgencyProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    company_name = models.CharField(_("company name"), max_length=100)
    contact_person_name = models.CharField(_("contact person name"), max_length=100)
    mobile_number = models.CharField(_("mobile number"), max_length=15, blank=True)
    website = models.URLField(_("website"), blank=True)
    category = models.CharField(_("category"), max_length=100, blank=True)
    address = models.CharField(_("address"), max_length=255, blank=True)
    brand_logo = models.ImageField(
        _("brand logo"), upload_to="brand_logos/", null=True, blank=True
    )
    country = models.CharField(_("country"), max_length=100)
    facebook_link = models.URLField(_("Facebook link"), blank=True)
    twitter_link = models.URLField(_("Twitter link"), blank=True)
    instagram_link = models.URLField(_("Instagram link"), blank=True)

