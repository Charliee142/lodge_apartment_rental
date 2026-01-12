from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .forms import *


def my_dashboard(request):
    return render(request, "account/dashboard/my_dashboard.html")


def profile_details(request):
    profile = getattr(request.user, "profile", None)
    
    if not profile:
        return redirect("profile_update")  # Redirect if no profile exists

    # Ensure None values are handled correctly
    required_fields = [
        str(getattr(profile, "first_name", "") or "").strip(),
        str(getattr(profile, "last_name", "") or "").strip(),
        str(getattr(profile, "phone_number", "") or "").strip(),
        str(getattr(profile, "address", "") or "").strip(),
        str(getattr(profile, "state", "") or "").strip(),
        str(getattr(profile, "city", "") or "").strip(),
        str(getattr(request.user, "email", "") or "").strip(),
    ]
    
    filled_fields = sum(1 for field in required_fields if field)  # Count non-empty fields
    total_fields = len(required_fields)
    completion_percentage = int((filled_fields / total_fields) * 100) if total_fields else 0

    # Example check for 2FA (adjust based on your implementation)
    two_factor_enabled = getattr(profile, "two_factor_enabled", False)

    context = {
        "profile": profile,
        "completion_percentage": completion_percentage,
        "two_factor_enabled": two_factor_enabled,
    }

    return render(request, "account/partials/profile_details.html", context)


def profile_update(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Ensure profile exists
    form = ProfileUpdateForm(instance=profile)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            
            # Recalculate completion percentage after updating profile
            required_fields = [
                profile.first_name, profile.last_name, profile.phone_number,
                profile.address, profile.state, profile.city, request.user.email
            ]
            filled_fields = sum(1 for field in required_fields if str(field).strip())
            total_fields = len(required_fields)
            completion_percentage = int((filled_fields / total_fields) * 100) if total_fields else 0

            return render(request, "account/partials/profile_details.html", {
                "profile": profile,
                "completion_percentage": completion_percentage
            })

    return render(request, 'account/dashboard/profile_update.html', {'form': form})


"""@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile after update
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})"""