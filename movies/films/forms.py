from .models import Films
from django.forms import ModelForm, TextInput, Textarea

class FilmsForm(ModelForm):
    class Meta:
        model = Films
        fields = ['title', 'genre', 'description', 'year']

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название'
            }),
            "genre": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Жанр'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание'
            }),"year": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Год'
            })

        }