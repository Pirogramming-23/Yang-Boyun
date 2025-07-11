from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'year', 'director', 'main_actor', 'genre', 'rating', 'running_time', 'content', 'image']
