from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import uuid


class Apartment(models.Model):
    STATUS_CHOICES = [
        ('vacant', 'Vacant'),
        ('occupied', 'Occupied'),
        ('under maintenance', 'Under Maintenance'),
         ('Reserved', 'Reserved'),
    ]
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    owner=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='apartments')
    features = models.ManyToManyField('Feature', blank=True) # e.g., "WiFi, TV, AC"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='vacant')
    images = models.ImageField(upload_to='property_images/')
    apartment_video = models.FileField(upload_to='property_videos/', null=True, blank=True)  # Allows null values
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def is_available(self):
        return self.status == 'vacant'
 
    def __str__(self):
        return self.name
    

class ApartmentImage(models.Model):
    apartment = models.ForeignKey(Apartment, related_name='apartment_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='apartments/images/')
    description = models.CharField(max_length=255, blank=True, null=True)  # Optional description for the image
    is_primary = models.BooleanField(default=False)  # Optional flag to mark a primary image

    def __str__(self):
        return f"Image for {self.apartment.name} - {self.id}"
    

class GalleryItem(models.Model):
    CATEGORY_CHOICES = [
        ('villas', 'Villas'),
        ('apartments', 'Apartments'),
        ('interior', 'Interior'),
        ('properties', 'Properties'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)

    def __str__(self):
        return self.name
    

class Feature(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, blank=True, null=True)  # Optional: store icon name or class

    def __str__(self):
        return self.name
    

class Rating(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} rated {self.apartment.name} - {self.rating}"
    

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='favorited_by')
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'apartment')

    def __str__(self):
        return f"{self.user.username} favorited {self.apartment.name}"


class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    message =  models.TextField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
