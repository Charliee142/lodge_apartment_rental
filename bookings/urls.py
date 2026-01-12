from django.urls import path
from . import views

urlpatterns = [
    # "c/<uuid:uuid_slug>" means the part after /c/ is validated as a UUID
    path("booking/<str:pk>/", views.book_apartment, name="book_apartment"),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('booking_lists/', views.user_dashboard, name='user_dashboard'),
    path('review-booking/<int:booking_id>/<str:action>/', views.review_booking, name='review_booking'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('landlord-dashboard/', views.landlord_dashboard, name='landlord_dashboard'),
    path('approve-booking/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('reject-booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),


    path("booking_history/", views.past_bookings, name="past_bookings"),
    path("booking_history/<int:booking_id>/", views.booking_detail, name="booking_detail"),
]

