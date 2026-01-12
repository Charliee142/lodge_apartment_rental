from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    profession = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def check_completion(self):
        """Check if all required fields are filled."""
        required_fields = [self.phone_number, self.address, self.profile_picture]
        return all(required_fields)

    def save(self, *args, **kwargs):
        """Automatically update is_completed based on profile completeness."""
        self.is_completed = self.check_completion()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Profile"