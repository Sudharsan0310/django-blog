from django.contrib import admin
from .models import Category, Blog, Comment


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured')
    search_fields = ('id', 'title', 'category__category_name')
    list_editable = ('is_featured',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'comment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'blog__title', 'comment')
    list_per_page = 20


admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)