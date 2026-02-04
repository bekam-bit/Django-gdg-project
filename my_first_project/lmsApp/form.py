from django import forms
from . models import Book

class BookForm(forms.ModelForm):
   class Meta:
        model = Book
        fields = ['ISBN', 'title', 'total_copies', 'publication_date', 'author','category']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }
