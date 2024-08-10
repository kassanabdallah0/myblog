from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Article, Event


# Signup Form :
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# Contact Form : 
class ContactForm(forms.Form):
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'placeholder': 'Your email address'}))
    request_type = forms.ChoiceField(choices=[('contact', 'Contact'), ('bug', 'Bug Report')], label='Type of Request')
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your message'}))

# Article Form : 
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']

# Event Form : 
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'content', 'start_date', 'end_date', 'image']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }