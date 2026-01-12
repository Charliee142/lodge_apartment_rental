from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   path('admin/', admin.site.urls),
    path('', include('properties.urls')),
    path('booking/', include('bookings.urls')),
    path('accounts/', include('accounts.urls')),
    path('blog_posts/', include('blogapp.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('accounts/', include('allauth.urls')),  # Allauth URL configuration
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
