from django.shortcuts import render

from blogs.models import Blog, Category
from assignments.models import About

def home(request):
    categories = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured=True, status="Published")
    posts = Blog.objects.filter(status="Published")
    
    # Fetch About Us
    try:
        about = About.objects.first()  # Use .first() instead of .get()
    except:
        about = None

    #Fetch Social Media
    
    
    context = {
        'categories': categories,
        'featured_posts': featured_posts,
        'posts': posts,
        'about': about,  # lowercase 'about'
    }
    return render(request, 'home.html', context)