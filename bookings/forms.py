from django import forms
from django.core.exceptions import ValidationError
from .models import *


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "state",
            "city",
            "check_in_date",
            "check_out_date",
            "number_of_guests",
            "room_type",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'First Name'}),
            "last_name": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'last Name'}),
            "email": forms.EmailInput(attrs={"class": "form-control", 'placeholder': 'Email'}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Phone Number'}),
            "state": forms.Select(attrs={"class": "form-control", 'placeholder': 'State'}),
            "check_in_date": forms.DateInput(attrs={"id": "check_in_date", "type": "date", "class": "form-control"}),
            "check_out_date": forms.DateInput(attrs={"id": "check_out_date", "type": "date", "class": "form-control"}),
            "number_of_guests": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 10, "placeholder": "Number of Guests"}),
            "room_type": forms.Select(attrs={"class": "form-control", "id": "room_type", "placeholder": "Room Type"}),
        }
