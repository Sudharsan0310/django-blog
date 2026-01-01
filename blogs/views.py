from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Blog, Category, Comment
from django.db.models import Q
from django.contrib.auth.decorators import login_required

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
    blog = get_object_or_404(Blog, slug=slug, status='Published')
    
    # Get all comments for this blog
    comments = Comment.objects.filter(blog=blog)
    comment_count = comments.count()
    
    # Handle comment submission
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_text = request.POST.get('comment')
            
            if comment_text:
                Comment.objects.create(
                    user=request.user,
                    blog=blog,
                    comment=comment_text
                )
                messages.success(request, '✅ Your comment has been posted!')
                return redirect('blogs', slug=slug)
            else:
                messages.error(request, '❌ Comment cannot be empty!')
        else:
            messages.error(request, '❌ Please login to post a comment!')
            return redirect('login')
    
    context = {
        'blog': blog,
        'comments': comments,
        'comment_count': comment_count,
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

def categories_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'categories_list.html', context)

@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    blog_slug = comment.blog.slug
    
    # Check if user is the comment owner or staff/superuser
    if request.user == comment.user or request.user.is_staff or request.user.is_superuser:
        comment.delete()
        messages.success(request, '✅ Comment deleted successfully!')
    else:
        messages.error(request, '❌ You do not have permission to delete this comment!')
    
    return redirect('blogs', slug=blog_slug)