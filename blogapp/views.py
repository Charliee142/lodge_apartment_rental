from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
	recent_post = Post.objects.filter(section='Recent').order_by('-id')[0:4]
	main_post = Post.objects.filter(main_post=True)[0:1]
	categories = Category.objects.all()
	posts = Post.objects.all().filter(is_published=True).order_by('-created_on')

	
    # Add Paginator
	paginator = Paginator(posts, 4) 
	page = request.GET.get('page')
	
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	

	context = {
        'main_post':main_post,
        'recent_post':recent_post,
        'categories':categories,
        'posts': posts,
    }
	return render(request, "blog_home.html", context)	


def post(request, slug):
	requested_post = Post.objects.get(slug=slug)
	categories = Category.objects.all()

	# Related Posts
 	## Get all the tags related to this article
	## Filter all posts that contain tags which are related to the current post, and exclude the current post
	


	context={
        'categories':categories,
		'post': requested_post,
		
	}

	return render(request, "blog_single.html", context)


def category(request, slug):
	posts = Post.objects.filter(categories__slug=slug).filter(is_published=True)
	requested_category = Category.objects.get(slug=slug)
	categories = Category.objects.all()
	recent_post = Post.objects.filter(section='Recent').order_by('-id')[0:4]
	main_post = Post.objects.filter(main_post=True)[0:1]

	 # Add Paginator
	paginator = Paginator(posts, 1) 
	page = request.GET.get('page')
	
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	

	context = {
		'posts': posts,
		'main_post':main_post,
		'recent_post':recent_post,
		'category': requested_category,
		'categories': categories,
		
	}
	return render(request, "category.html", context)


def search(request):
	categories = Category.objects.all()


	""" search function  """
	query = request.POST.get("search")
	if query:
		posts = Post.objects.filter(is_published=True).filter(title__icontains=query)
	else:
		posts = []

	context = {
		'categories':categories,
		'posts':posts,
		'query': query,
	}
	return render(request, "search.html", context)


@login_required
def author_profile(request, pk):
    """View to display the author's profile."""
    """View to display the author's profile."""
    author =  Profile.objects.get(profile_id=pk)
    return render(request, 'author/author_profile.html', {'author': author})