from django.shortcuts import render, get_object_or_404
from .models import Blog,Category
from django.db.models import Q

def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)  
    posts = Blog.objects.filter(category=category, status="Published")
    
    context = {
        'posts': posts,
        'category': category,
        'categories': Category.objects.all(),
    }
    return render(request, 'posts_by_category.html', context)

def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    context = {
        'single_blog': single_blog,
        'categories': Category.objects.all(),
    }
    return render(request, 'blogs.html', context)

def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.filter(
        Q(title__icontains=keyword) | 
        Q(short_description__icontains=keyword) | 
        Q(blog_body__icontains=keyword), 
        status="Published"
    ) 
    context = {
        'blogs': blogs,
        'keyword': keyword,  # ✅ Add this!
    }
    return render(request, 'search.html', context)