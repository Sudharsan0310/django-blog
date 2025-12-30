from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blogs.models import Blog, Category
from django.contrib import messages
from django.utils import timezone

@login_required(login_url='login')
def dashboard(request):
    # Get user's blog posts
    user_posts = Blog.objects.filter(author=request.user)
    
    # Get all categories (only for admin/staff users)
    if request.user.is_staff or request.user.is_superuser:
        categories = Category.objects.all().order_by('-created_at')
    else:
        categories = None
    
    context = {
        'user_posts': user_posts,
        'categories': categories,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def add_category(request):
    # Only allow admin/staff to add categories
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'You do not have permission to add categories!')
        return redirect('dashboard')
    
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        
        if category_name:
            # Check if category already exists
            if Category.objects.filter(category_name__iexact=category_name).exists():
                messages.error(request, f'Category "{category_name}" already exists!')
            else:
                Category.objects.create(
                    category_name=category_name,
                    created_at=timezone.now(),
                    updated_at=timezone.now()
                )
                messages.success(request, f'✅ Category "{category_name}" added successfully!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Please enter a category name!')
    
    return redirect('dashboard')

@login_required(login_url='login')
def edit_category(request, category_id):
    # Only allow admin/staff to edit categories
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'You do not have permission to edit categories!')
        return redirect('dashboard')
    
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        new_name = request.POST.get('category_name')
        
        if new_name:
            # Check if new name already exists (excluding current category)
            if Category.objects.filter(category_name__iexact=new_name).exclude(id=category_id).exists():
                messages.error(request, f'Category "{new_name}" already exists!')
            else:
                old_name = category.category_name
                category.category_name = new_name
                category.save()
                messages.success(request, f'✅ Category updated from "{old_name}" to "{new_name}"!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Please enter a category name!')
    
    return redirect('dashboard')

@login_required(login_url='login')
def delete_category(request, category_id):
    # Only allow admin/staff to delete categories
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'You do not have permission to delete categories!')
        return redirect('dashboard')
    
    category = get_object_or_404(Category, id=category_id)
    
    # Check if category has posts
    post_count = category.blog_set.count()
    
    if post_count > 0:
        messages.warning(request, f'⚠️ Cannot delete "{category.category_name}" - it has {post_count} blog post(s)!')
    else:
        category_name = category.category_name
        category.delete()
        messages.success(request, f'✅ Category "{category_name}" deleted successfully!')
    
    return redirect('dashboard')