from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django_ckeditor_5.fields import CKEditor5Field
from PIL import Image
from accounts.models import *
from django.conf import settings
import uuid

  
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    
SECTION = (
        ('Popular', 'Popular'),
        ('Recent', 'Recent'),
        ('Trending', 'Trending'),
        ('Latest Post', 'Latest Post'),
    )

class Post(models.Model):
    LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'success'),
    ('D', 'danger'), 
    ('W', 'warning'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = CKEditor5Field('Text', config_name='extends')
    image = models.ImageField(upload_to="images/")
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    section = models.CharField(choices=SECTION, max_length=100)
    main_post = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now= True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, blank=True, null=True)
    created_on = models.DateField(default=date.today)
    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE, related_name="blog_posts", null=True, blank=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    def get_label_class(self):
        """Returns the full label name for use in the template"""
        label_mapping = dict(self.LABEL_CHOICES)
        return label_mapping.get(self.label, "").lower()  # Converts to lowercase
    

