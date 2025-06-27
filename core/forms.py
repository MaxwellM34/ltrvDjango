from django import forms
from .models import Contact, Suggestion

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['name', 'email', 'suggestion']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name (optional)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email (optional)'}),
            'suggestion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Let us know how we can serve you better!', 'rows': 4}),
        } 