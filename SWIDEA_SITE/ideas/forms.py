from django import forms
from .models import Idea, DevTool

class IdeaForm(forms.ModelForm):
    DEVTOOL_CHOICES = [
        ('Django', 'Django'),
        ('Spring', 'Spring'),
        ('기타', '기타'),
    ]
    devtool = forms.ChoiceField(choices=DEVTOOL_CHOICES, required=True, label='개발툴')

    class Meta:
        model = Idea
        fields = ['title', 'description', 'devtool', 'image']

class DevToolForm(forms.ModelForm):
    class Meta:
        model = DevTool
        fields = ['name', 'kind', 'description'] 