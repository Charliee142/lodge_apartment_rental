from django.urls import path
from . import views 


urlpatterns = [
    path("", views.index, name="blog"),
    path("post/<slug:slug>/", views.post, name="post"),
    path('category/<slug:slug>/', views.category, name='category'),
    path('search/', views.search, name='search'),
]