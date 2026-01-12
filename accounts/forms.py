from django import forms
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)  # Add email as a form field

    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'state', 'city', 'profile_picture', 'email']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email  # Pre-fill the email field

    def save(self, commit=True):
        profile = super().save(commit=False)
        if 'email' in self.cleaned_data:
            profile.user.email = self.cleaned_data['email']  # Update user email
            profile.user.save()  # Save the user model
        if commit:
            profile.save()
        return profile
