from django.db import models
from account.models import UserProfile

# Create your models here.

class Category(models.Model):
    name  = models.CharField(max_length=255)

status_choice = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
)

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

from django.contrib.auth.models import User

class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Ensure to specify max_digits and decimal_places
    tags = models.ManyToManyField('Tag', related_name='services')
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    created_at = models.DateTimeField(auto_now_add=True)
class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='service_images/')

    def __str__(self):
        return f"Image for {self.service.title} - ID {self.service.id}"

class Orders(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('reported', 'Reported'),
        ('canceled', 'Canceled'),
        ('job_done', 'Job Done'),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    order_title = models.CharField(max_length=255)
    delivery_date = models.DateField()
    description = models.TextField()  # 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Ensure to specify max_digits and decimal_places
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Orders")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.order_title
