from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('posts/', views.posts, name='posts'),
    path('add-post/', views.add_post, name='add_post'),
    path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('add-category/', views.add_category, name='add_category'),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('toggle-featured/<int:post_id>/', views.toggle_featured, name='toggle_featured'),
]