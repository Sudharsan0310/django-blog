"""
URL configuration for blog_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from blog_main import views as main_views
from blogs import views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.home, name='home'),
    path('category/<int:category_id>/', blog_views.posts_by_category, name='posts_by_category'),
    
    # Static and Media
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    
    # Search BEFORE slug pattern!
    path('search/', blog_views.search, name='search'),  # ✅ Moved here and simplified!
    
    # Slug pattern LAST (it catches everything else)
    path('<slug:slug>/', blog_views.blogs, name='blogs'),
]