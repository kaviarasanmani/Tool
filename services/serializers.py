from rest_framework import serializers
from .models import Service, ServiceImage,Orders

class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['image']

class ServiceSerializer(serializers.ModelSerializer):
    images = ServiceImageSerializer(many=True, required=False)

    class Meta:
        model = Service
        fields = ['user', 'category', 'title', 'price', 'tags', 'description', 'status', 'created_at', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        service = Service.objects.create(**validated_data)
        for image_data in images_data:
            ServiceImage.objects.create(service=service, **image_data)
        return service

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        # Update the service instance
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        # Handle updating/adding images
        for image_data in images_data:
            image_id = image_data.get('id', None)
            if image_id:
                img = ServiceImage.objects.get(id=image_id, service=instance)
                img.image = image_data.get('image', img.image)
                img.save()
            else:
                ServiceImage.objects.create(service=instance, **image_data)
                
        return instance


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
        read_only_fields = ['ordered_by', 'ordered_at']
