from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
import json
from django.utils.timezone import now
from datetime import timedelta
from django.contrib import messages
from .forms import *
from properties.models import  *
from django.utils.dateparse import parse_date


@login_required
def book_apartment(request, pk):
    apartment = get_object_or_404(Apartment, id=pk)
    form = BookingForm()  # Initialize form
    profile = request.user.profile

    # Fetch booked dates for this apartment
    booked_dates = Booking.objects.filter(apartment=apartment, status="Approved").values_list("check_in_date", "check_out_date")

    # Check if apartment is available for booking
    if not apartment.is_available():
        messages.error(request, "This apartment is currently occupied and cannot be booked.")
        return redirect("properties")  # Redirect to the apartment listing page
    
    # Check if profile is incomplete
    required_fields = [
        profile.first_name, profile.last_name, profile.phone_number,
        profile.address, profile.state, profile.city, request.user.email
    ]
    if not all(required_fields):
        messages.error(request, "⚠️ Your profile is incomplete. Please update it before booking.")
        return redirect("profile_details")
    
    # Convert booked dates to a list of disabled days
    blocked_dates = []
    for check_in_date, check_out_date in booked_dates:
        date_range = [check_in_date + timedelta(days=i) for i in range((check_out_date - check_in_date).days + 1)]
        blocked_dates.extend(date_range)

    # Convert dates to JSON format for frontend JavaScript
    blocked_dates_json = json.dumps([date.strftime("%m-%d-%Y") for date in blocked_dates])

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.apartment = apartment
            booking.user = request.user

           
            # Validation: Ensure check-in is not in the past
            if booking.check_in_date < now().date():
                messages.error(request, "❌ Check-in date cannot be in the past. Please select a valid date.")
                return render(request, "booking/book_apartment.html", {
                    "form": form,
                    "apartment": apartment,
                    "blocked_dates": blocked_dates_json
                })

            # Validation: Check-out must be after check-in
            if booking.check_out_date <= booking.check_in_date:
                messages.error(request, "❌ Check-out date must be after check-in date.")
                return render(request, "booking/book_apartment.html", {
                    "form": form,
                    "apartment": apartment,
                    "blocked_dates": blocked_dates_json
                })

            booking.save()  # Save booking after validation

            # Send email notification to landlord
            landlord_email = apartment.owner.email
            subject = f"You have a new booking request from {request.user.username} for {apartment.name}."

            # Render email template with booking details
            html_message = render_to_string('emails/email_booking_notification.html', {
                'landlord_name': apartment.owner.username,
                'apartment_name': apartment.name,
                'renter_name': booking.first_name,  # Assuming booking model has first_name
                'email': booking.email,
                'phone_number': booking.phone_number,
                'state': booking.state,
                'city': booking.city,
                'number_of_guests': booking.number_of_guests,
                'room_type': booking.room_type,
                'check_in_date': booking.check_in_date,
                'check_out_date': booking.check_out_date,
                'landlord_dashboard_url': request.build_absolute_uri('/landlord-dashboard/')
            })
            plain_message = strip_tags(html_message)  # Strip HTML for plain text fallback

            send_mail(
                subject,
                plain_message,
                'charlespeter142@gmail.com',  # Sender
                [landlord_email],  # Recipient
                html_message=html_message,
                fail_silently=False
            )

            # Generate greeting based on time of booking
            current_hour = now().hour
            if current_hour < 12:
                greeting = "Good Morning"
            elif 12 <= current_hour < 18:
                greeting = "Good Afternoon"
            else:
                greeting = "Good Evening"

            # Success message with formatted details
            messages.success(request, f"""
                {greeting}, {request.user.username}!
                Your booking at {apartment.name} has been confirmed. 
                Check-in: {booking.check_in_date.strftime('%A, %d %B %Y')} 
                Check-out: {booking.check_out_date.strftime('%A, %d %B %Y')}
                Guests: {booking.number_of_guests}""")
            # Proceed with booking logic here
            messages.success(request, "Apartment booked successfully!")
            return redirect("booking_success")

    # Render the booking page with blocked dates
    return render(request, "booking/book_apartment.html", {
        "form": form,
        "apartment": apartment,
        "blocked_dates": blocked_dates_json,
    })


def booking_success(request):
    booking = Booking.objects.all()
    context = {
        "booking": booking,
    }
    return render(request, 'booking/booking_success.html', context)


@login_required
def user_dashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking/user_dashboard.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == "Pending":
        booking.status = "Canceled"
        booking.save()
        messages.success(request, "Booking canceled successfully.")
    else:
        messages.error(request, "You cannot cancel this booking.")
    return redirect('user_dashboard')


@login_required
def landlord_dashboard(request):
    apartments = Apartment.objects.filter(owner=request.user)
    bookings = Booking.objects.filter(apartment__in=apartments, status="Pending").order_by('-created_at')
    return render(request, 'booking/landlord_dashboard.html', {'bookings': bookings})


@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, apartment__owner=request.user)
    booking.status = "Approved"
    booking.save()
    messages.success(request, "Booking approved successfully.")
    return redirect('landlord_dashboard')

@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, apartment__owner=request.user)
    booking.status = "Canceled"
    booking.save()
    messages.success(request, "Booking rejected successfully.")
    return redirect('landlord_dashboard')


@staff_member_required
def review_booking(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id)
    if action == "approve":
        booking.status = "Approved"
        booking.reviewed_by = request.user
        booking.save()
        messages.success(request, "Booking approved successfully.")
    elif action == "reject":
        booking.status = "canceled"
        booking.reviewed_by = request.user
        booking.save()
        messages.info(request, "Booking rejected.")
    return redirect("user_dashboard")


def send_booking_email(booking, recipient_email):
    subject = f"New Booking Request for {booking.apartment.name}"
    text_content = (
        f"You have a new booking request from {booking.user.username}.\n"
        f"Check-in Date: {booking.check_in_date}\n"
        f"Check-out Date: {booking.check_out_date}\n"
        f"Guests: {booking.number_of_guests}\n"
        f"Please log in to approve or reject this booking."
    )
    html_content = f"""
    <html>
        <body>
            <h3>New Booking Request</h3>
            <p><strong>From:</strong> {booking.user.username}</p>
            <p><strong>Check-in Date:</strong> {booking.check_in_date}</p>
            <p><strong>Check-out Date:</strong> {booking.check_out_date}</p>
            <p><strong>Guests:</strong> {booking.number_of_guests}</p>
            <p>Please log in to approve or reject this booking.</p>
        </body>
    </html>
    """
    email = EmailMultiAlternatives(subject, text_content, "from@example.com", [recipient_email])
    email.attach_alternative(html_content, "text/html")
    email.send()



@login_required
def past_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-check_in_date")

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date and end_date:
        bookings = bookings.filter(check_in_date__gte=parse_date(start_date), check_out_date__lte=parse_date(end_date))

    return render(request, "booking/past_bookings.html", {"bookings": bookings})


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, "booking/booking_detail.html", {"booking": booking})