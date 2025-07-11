from django.contrib import admin
from .models import Review, Genre

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'get_genres', 'rating', 'created_at']
    list_filter = ['genre', 'rating', 'created_at']
    search_fields = ['title', 'director', 'main_actor']
    
    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    get_genres.short_description = '장르'