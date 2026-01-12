from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("apartment/<int:apartment_id>/", views.apartment_details, name="apartment_details"),
    path("properties/", views.properties, name="properties"),
    path("gallery/", views.gallery_view, name="gallery"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("service/", views.service, name="service"),
    path("search/", views.search_properties, name="search"),
    path("submit_review/<int:apartment_id>/", views.submit_review, name="submit_review"),
    path('like/', views.like_apartment, name='like_apartment'),
    path("add-to-favorites/<int:apartment_id>/", views.add_to_favorites, name="add_to_favorites"),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
    path('remove-favorite/<int:apartment_id>/', views.remove_favorite, name='remove_favorite'),
    path('edit-apartment/<int:apartment_id>/', views.edit_apartment, name='edit_apartment'),
    path('delete-apartment/<int:apartment_id>/', views.delete_apartment, name='delete_apartment'),
    
   
]