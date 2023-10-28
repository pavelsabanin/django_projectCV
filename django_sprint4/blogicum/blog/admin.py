from django.contrib import admin

from .models import Post, Location, Category


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',)
    list_editable = (
        'pub_date',
        'is_published',)
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'is_published',)
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('title',)
    list_display_links = ('title',)


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at',
        'is_published',)
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('name',)


admin.site.register(Post, PostAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
