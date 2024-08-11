from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Article, Event

# Signup Form :
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    
class ContactForm(forms.Form):
    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    request_type = forms.ChoiceField(
        choices=[('contact', 'Contact'), ('bug', 'Bug Report')],
        label="Request Type",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    message = forms.CharField(
        label="Your Message",
        widget=forms.Textarea(attrs={"class": "form-control"})
    )

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:  # Enforce a minimum length of 10 characters
            raise forms.ValidationError("The message must be at least 10 characters long.")
        return message


# Article Form : 
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# Event Form : 
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'content', 'start_date', 'end_date', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
