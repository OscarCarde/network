from django import forms
from .models import *

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'media']
        exclude = ['by', 'likes']
        labels = {
            'content': "",
            'media': ""
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Today I ...'}),
            'media': forms.FileInput(attrs={'class': 'form-control'}, )
        }

        