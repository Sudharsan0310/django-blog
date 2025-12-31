from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blogs.models import Blog, Category
from django.contrib import messages
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test


@login_required(login_url='login')
def dashboard(request):
    # Get user's blog posts
    user_posts = Blog.objects.filter(author=request.user).order_by('-created_at')
    
    # Get all categories (only for admin/staff users)
    if request.user.is_staff or request.user.is_superuser:
        categories = Category.objects.all().order_by('-created_at')
        all_posts = Blog.objects.all().order_by('-created_at')
    else:
        categories = None
        all_posts = None
    
    context = {
        'user_posts': user_posts,
        'categories': categories,
        'all_posts': all_posts,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def posts(request):
    # Get posts based on user role
    if request.user.is_staff or request.user.is_superuser:
        # Admin sees all posts
        posts = Blog.objects.all().order_by('-created_at')
    else:
        # Regular users see only their posts
        posts = Blog.objects.filter(author=request.user).order_by('-created_at')
    
    categories = Category.objects.all()
    
    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'dashboard/post.html', context)

@login_required(login_url='login')
def add_post(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        short_description = request.POST.get('short_description')
        blog_body = request.POST.get('blog_body')
        status = request.POST.get('status')
        is_featured = request.POST.get('is_featured') == 'on'
        feature_image = request.FILES.get('feature_image')
        
        # Validation
        if not title or not category_id or not short_description or not blog_body:
            messages.error(request, '❌ Please fill all required fields!')
            return render(request, 'dashboard/add_post.html', {'categories': categories})
        
        try:
            category = Category.objects.get(id=category_id)
            
            # Create slug from title
            slug = slugify(title)
            original_slug = slug
            counter = 1
            
            # Make sure slug is unique
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            # Create the blog post
            post = Blog.objects.create(
                title=title,
                slug=slug,
                category=category,
                author=request.user,
                short_description=short_description,
                blog_body=blog_body,
                status=status,
                is_featured=is_featured,
                feauture_image=feature_image
            )
            
            messages.success(request, f'✅ Post "{title}" created successfully!')
            return redirect('posts')
            
        except Category.DoesNotExist:
            messages.error(request, '❌ Invalid category selected!')
        except Exception as e:
            messages.error(request, f'❌ Error creating post: {str(e)}')
    
    context = {
        'categories': categories,
    }
    return render(request, 'dashboard/add_post.html', context)

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
def edit_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id)
    
    # Check if user has permission to edit
    if not (request.user.is_staff or request.user.is_superuser or post.author == request.user):
        messages.error(request, 'You do not have permission to edit this post!')
        return redirect('posts')
    
    categories = Category.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        short_description = request.POST.get('short_description')
        blog_body = request.POST.get('blog_body')
        status = request.POST.get('status')
        is_featured = request.POST.get('is_featured') == 'on'
        feature_image = request.FILES.get('feature_image')
        
        # Validation
        if not title or not category_id or not short_description or not blog_body:
            messages.error(request, '❌ Please fill all required fields!')
            return render(request, 'dashboard/edit_post.html', {
                'post': post,
                'categories': categories
            })
        
        try:
            category = Category.objects.get(id=category_id)
            
            # Update slug only if title changed
            if post.title != title:
                slug = slugify(title)
                original_slug = slug
                counter = 1
                
                # Make sure slug is unique (exclude current post)
                while Blog.objects.filter(slug=slug).exclude(id=post_id).exists():
                    slug = f"{original_slug}-{counter}"
                    counter += 1
                
                post.slug = slug
            
            # Update post fields
            post.title = title
            post.category = category
            post.short_description = short_description
            post.blog_body = blog_body
            post.status = status
            post.is_featured = is_featured
            
            # Update image only if new one is uploaded
            if feature_image:
                post.feauture_image = feature_image
            
            post.updated_at = timezone.now()
            post.save()
            
            messages.success(request, f'✅ Post "{title}" updated successfully!')
            return redirect('posts')
            
        except Category.DoesNotExist:
            messages.error(request, '❌ Invalid category selected!')
        except Exception as e:
            messages.error(request, f'❌ Error updating post: {str(e)}')
    
    context = {
        'post': post,
        'categories': categories,
    }
    return render(request, 'dashboard/edit_post.html', context)

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

@login_required(login_url='login')
def delete_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id)
    
    # Check if user has permission
    if not (request.user.is_staff or request.user.is_superuser or post.author == request.user):
        messages.error(request, 'You do not have permission to delete this post!')
        return redirect('dashboard')
    
    post_title = post.title
    post.delete()
    messages.success(request, f'✅ Post "{post_title}" deleted successfully!')
    
    return redirect('posts')

@login_required(login_url='login')
def toggle_featured(request, post_id):
    # Only admin/staff can toggle featured
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'You do not have permission to feature posts!')
        return redirect('dashboard')
    
    post = get_object_or_404(Blog, id=post_id)
    post.is_featured = not post.is_featured
    post.save()
    
    if post.is_featured:
        messages.success(request, f'⭐ Post "{post.title}" is now featured!')
    else:
        messages.success(request, f'Post "{post.title}" removed from featured!')
    
    return redirect('posts')


# Check if user is manager (superuser)
def is_manager(user):
    return user.is_superuser

@login_required(login_url='login')
@user_passes_test(is_manager)
def users_list(request):
    """View all users - Only for superuser"""
    users = User.objects.all().order_by('-date_joined')
    
    context = {
        'users': users,
    }
    return render(request, 'dashboard/users.html', context)

@login_required(login_url='login')
@user_passes_test(is_manager)
def add_user(request):
    """Add new user - Only for superuser"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'
        
        # Validation
        if not username or not email or not password:
            messages.error(request, '❌ Please fill all required fields!')
            return redirect('users_list')
        
        if password != password2:
            messages.error(request, '❌ Passwords do not match!')
            return redirect('users_list')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, f'❌ Username "{username}" already exists!')
            return redirect('users_list')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, f'❌ Email "{email}" already registered!')
            return redirect('users_list')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff,
                is_superuser=is_superuser
            )
            messages.success(request, f'✅ User "{username}" created successfully!')
        except Exception as e:
            messages.error(request, f'❌ Error creating user: {str(e)}')
    
    return redirect('users_list')

@login_required(login_url='login')
@user_passes_test(is_manager)
def edit_user(request, user_id):
    """Edit user - Only for superuser"""
    user_to_edit = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'
        is_active = request.POST.get('is_active') == 'on'
        new_password = request.POST.get('new_password')
        
        # Check if username already exists (exclude current user)
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, f'❌ Username "{username}" already exists!')
            return redirect('users_list')
        
        # Check if email already exists (exclude current user)
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            messages.error(request, f'❌ Email "{email}" already registered!')
            return redirect('users_list')
        
        try:
            user_to_edit.username = username
            user_to_edit.email = email
            user_to_edit.first_name = first_name
            user_to_edit.last_name = last_name
            user_to_edit.is_staff = is_staff
            user_to_edit.is_superuser = is_superuser
            user_to_edit.is_active = is_active
            
            # Update password if provided
            if new_password:
                user_to_edit.set_password(new_password)
            
            user_to_edit.save()
            messages.success(request, f'✅ User "{username}" updated successfully!')
        except Exception as e:
            messages.error(request, f'❌ Error updating user: {str(e)}')
    
    return redirect('users_list')

@login_required(login_url='login')
@user_passes_test(is_manager)
def delete_user(request, user_id):
    """Delete user - Only for superuser"""
    user_to_delete = get_object_or_404(User, id=user_id)
    
    # Prevent deleting yourself
    if user_to_delete == request.user:
        messages.error(request, '❌ You cannot delete yourself!')
        return redirect('users_list')
    
    # Check if user has posts
    post_count = Blog.objects.filter(author=user_to_delete).count()
    
    if post_count > 0:
        messages.warning(request, f'⚠️ User "{user_to_delete.username}" has {post_count} blog post(s). Please reassign or delete posts first!')
    else:
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f'✅ User "{username}" deleted successfully!')
    
    return redirect('users_list')