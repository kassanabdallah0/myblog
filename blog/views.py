from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignupForm, ContactForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm

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
            return render(request, 'contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

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
    return render(request, 'signup.html', {'form': form})

# Home View
@login_required(login_url='login')
def home_view(request):
    return render(request, 'home.html')


# Article Part : 

# List of all articles
@login_required(login_url='login')
def article_list(request):
    articles = Article.objects.all().order_by('-published_date')  # Order by newest first
    return render(request, 'article_list.html', {'articles': articles})

# Detail view for a single article
@login_required(login_url='login')
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'article_detail.html', {'article': article})

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
    return render(request, 'article_form.html', {'form': form})

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
    return render(request, 'article_form.html', {'form': form})

# Delete an article
@login_required(login_url='login')
def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'article_confirm_delete.html', {'article': article})