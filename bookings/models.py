from django.db import models
from django.conf import settings
import uuid



class Booking(models.Model):
    # Room types
    SINGLE = "single"
    DOUBLE = "double"
    SUITE = "suite"

    ROOM_TYPE_CHOICES = [
        (SINGLE, "Single Room"),
        (DOUBLE, "Double Room"),
        (SUITE, "Suite"),
    ]

    # Booking statuses
    PENDING = "Pending"
    CONFIRMED = "Approved"
    COMPLETED = "Completed"
    CANCELED = "Canceled"
    

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Approved"),
        (COMPLETED, "Completed"),
        (CANCELED, "Canceled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    apartment = models.ForeignKey("properties.Apartment", on_delete=models.CASCADE, related_name="bookings")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True,)
    state = models.CharField(max_length=50, null=True, blank=True,)
    city = models.CharField(max_length=50, null=True, blank=True,)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField()
    room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="reviewed_bookings")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.check_in_date} to {self.check_out_date}"