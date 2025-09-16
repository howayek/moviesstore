from django.contrib import admin
from .models import Movie, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title','price')
    search_fields = ('title',)
    ordering = ('title',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie','user','created_at')
    search_fields = ('movie__title','user__username','comment')
