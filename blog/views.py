from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignupForm, ContactForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Article, Event
from .forms import ArticleForm, EventForm

# Contact Part : 
@login_required(login_url='login')
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get the form data
            email = form.cleaned_data['email']
            request_type = form.cleaned_data['request_type']
            message = form.cleaned_data['message']

            # Construct the email
            send_mail(
                f'Contact Request: {request_type}',
                message,
                email,  # The user's email will be the sender
                ['your_email@example.com'],  # Replace with your recipient email
                fail_silently=False,
            )

            # Return a success message or redirect to a success page
            return render(request, 'contact/contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})

# SignUp Part : 
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() 
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home') 
    else:
        form = SignupForm()
    return render(request, 'auth/signup.html', {'form': form})

# Home Part : 
@login_required(login_url='login')
def home_view(request):
    return render(request, 'home.html')


# Article Part : 

# List of all articles
@login_required(login_url='login')
def article_list(request):
    articles = Article.objects.all().order_by('-published_date')  # Order by newest first
    return render(request, 'articles/article_list.html', {'articles': articles})

# Detail view for a single article
@login_required(login_url='login')
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'articles/article_detail.html', {'article': article})

# Create a new article
@login_required(login_url='login')
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'articles/article_form.html', {'form': form})

# Edit an existing article
@login_required(login_url='login')
def article_edit(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/article_form.html', {'form': form})

# Delete an article
@login_required(login_url='login')
def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'articles/article_confirm_delete.html', {'article': article})


# Event Part : 

# List all events
@login_required(login_url='login')
def event_list(request):
    events = Event.objects.all().order_by('-start_date')  # You can customize the order as needed
    return render(request, 'events/event_list.html', {'events': events})

# View a single event
@login_required(login_url='login')
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

# Create a new event
@login_required(login_url='login')
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

# Edit an existing event
@login_required(login_url='login')
def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})

# Delete an event
@login_required(login_url='login')
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

# Confirm to Delete an event 
@login_required(login_url='login')
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})
