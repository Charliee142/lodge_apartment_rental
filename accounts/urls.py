from django.urls import path
from . import views


urlpatterns = [
        path("my_dashboard/", views.my_dashboard, name="my_dashboard" ),
        path("profile_details/", views.profile_details, name="profile_details"),
        path('profile/update/', views.profile_update, name='profile_update'),


        #path('profile/', profile_view, name='profile'),
        #path('edit-profile/', edit_profile, name='edit_profile'),
    ]