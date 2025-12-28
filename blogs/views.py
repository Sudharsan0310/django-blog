from django.shortcuts import render, get_object_or_404
from .models import Blog,Category

def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)  
    posts = Blog.objects.filter(category=category, status="Published")
    
    context = {
        'posts': posts,
        'category': category,
        'categories': Category.objects.all(),
    }
    return render(request, 'posts_by_category.html', context)