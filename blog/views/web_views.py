from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from blog.forms import SignupForm, ContactForm, ArticleForm, EventForm
from blog.models import Article, Event

# Contact Part
@login_required(login_url='login')
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            request_type = form.cleaned_data['request_type']
            message = form.cleaned_data['message']
            send_mail(
                f'Contact Request: {request_type}',
                message,
                email,
                ['your_email@example.com'],
                fail_silently=False,
            )
            return render(request, 'contact/contact_success.html')
    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})

# SignUp Part
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

# Home Part
@login_required(login_url='login')
def home_view(request):
    return render(request, 'home.html')

# Article Part
@login_required(login_url='login')
def article_list(request):
    articles = Article.objects.all().order_by('-published_date')
    return render(request, 'articles/article_list.html', {'articles': articles})

@login_required(login_url='login')
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'articles/article_detail.html', {'article': article})

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

@login_required(login_url='login')
def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'articles/article_confirm_delete.html', {'article': article})

# Event Part
@login_required(login_url='login')
def event_list(request):
    events = Event.objects.all().order_by('-start_date')
    return render(request, 'events/event_list.html', {'events': events})

@login_required(login_url='login')
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

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

@login_required(login_url='login')
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})
