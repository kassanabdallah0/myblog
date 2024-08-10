from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm, ContactForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

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
@login_required(login_url='api/login')
def home_view(request):
    return render(request, 'home.html')