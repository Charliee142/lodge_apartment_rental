from django.contrib import admin
from .models import *



class ApartmentImageInline(admin.TabularInline):
    model = ApartmentImage
    extra = 1  # Number of extra forms to display

class ApartmentAdmin(admin.ModelAdmin):
    inlines = [ApartmentImageInline]
    list_display = ('name', 'price', 'status')
    search_fields = ('name', 'status')


admin.site.register(Feature)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(ApartmentImage)
admin.site.register(GalleryItem)
admin.site.register(Rating)
admin.site.register(Favorite)
admin.site.register(Contact)