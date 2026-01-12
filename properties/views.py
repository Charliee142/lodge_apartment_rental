from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from properties.models import *
from bookings.models import *
from blogapp.models import *
from django.contrib import messages


@login_required
def like_apartment(request):
    apartment_id = request.GET.get('apartment_id', None)
    if apartment_id:
        try:
            apartment = Apartment.objects.get(id=int(apartment_id))
            apartment.likes += 1
            apartment.save()
            return JsonResponse({'likes': apartment.likes})
        except Apartment.DoesNotExist:
            return JsonResponse({'error': 'Apartment not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def index(request):
    apartments = Apartment.objects.all() 
    posts = Post.objects.filter(is_published=True).order_by("-created_on")[:5]

    context = {
        "apartments": apartments, 
        "posts": posts, 
    }
    return render(request, 'properties/index.html', context)

def properties(request):
    apartments = Apartment.objects.all()
    context = {
        "apartments": apartments,
    }
    return render(request, 'properties/properties.html', context)

def apartment_details(request, apartment_id):
    apartment = get_object_or_404(Apartment, pk=apartment_id)
    primary_image = apartment.apartment_images.filter(is_primary=True).first()  # Get the primary image
     # Check if the user already has a pending booking for this apartment
    has_pending_booking = False  # Default to False
    if request.user.is_authenticated:  # Check if user is logged in
        has_pending_booking = Booking.objects.filter(user=request.user, apartment=apartment, status='Pending').exists()

    context = {
        "apartment": apartment,
        'primary_image': primary_image,
        'has_pending_booking': has_pending_booking,
    }
    return render(request, 'properties/apartment_details.html', context)

def gallery_view(request):
    items = GalleryItem.objects.all()
    context = {
        "items": items,
    }
    return render(request, 'properties/gallery.html', context)

def about(request):
    return render(request, 'properties/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        contact = Contact(
            name = name,
            email = email,
            message = message,    
        )
        contact.save()
        return redirect('index')
    return render(request, 'properties/contact.html')

def service(request):
    return render(request, 'properties/service.html')

def search_properties(request):
    query = request.POST.get('search', '')  # Get the search query from the POST request
    results = []
    
    if query:
        # Perform a case-insensitive search on relevant fields
        results = Apartment.objects.filter(
            Q(name__icontains=query) | Q(location__icontains=query) | Q(description__icontains=query)
        )

    # Pass the query and results to the template
    context = {
        'results': results,
        'query': query,
        'results_count': len(results),  # Use len() to get the total number of results
    }
    return render(request, 'properties/search_results.html', context)

def submit_review(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    
    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment")

        Rating.objects.create(apartment=apartment, user=request.user, rating=rating, comment=comment)
    return redirect("apartment_details", apartment_id=apartment.id)

def add_to_favorites(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)

    # Check if the apartment is already a favorite
    favorite, created = Favorite.objects.get_or_create(user=request.user, apartment=apartment)

    if created:
        messages.success(request, f"{apartment.name} has been added to your favorites.")
    else:
        messages.info(request, f"{apartment.name} is already in your favorites.")

    return redirect('my_favorites')

def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('apartment')
    return render(request, 'properties/my_favorites.html', {'favorites': favorites}) 

def remove_favorite(request, apartment_id):
    favorite = get_object_or_404(Favorite, apartment_id=apartment_id)
    favorite.delete()
    messages.success(request, "Favorite has been removed.")
    return redirect('my_favorites')

@login_required
def my_properties(request):
    apartments = Apartment.objects.filter(owner=request.user)
    return render(request, "properties/my_properties.html", {"apartments": apartments})

@login_required
def edit_apartment(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)

    if request.method == "POST":
        apartment.name = request.POST.get("name")
        apartment.location = request.POST.get("location")
        apartment.price = request.POST.get("price")
        apartment.description = request.POST.get("description")
        apartment.status = request.POST.get("status")
        apartment.save()
        return redirect("my_properties")

    return render(request, "properties/edit_apartment.html", {"apartment": apartment})

@login_required
def create_apartment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        price = request.POST.get("price")
        description = request.POST.get("description")
        status = request.POST.get("status")

        apartment = Apartment.objects.create(
            name=name,
            location=location,
            price=price,
            description=description,
            owner=request.user,  # Assign logged-in user as owner
            status=status,
        )
        return redirect("apartment_list")  # Redirect to the apartment list page

    return render(request, "apartment_form.html")


@login_required
def delete_apartment(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    apartment.delete()
    return redirect("my_properties")