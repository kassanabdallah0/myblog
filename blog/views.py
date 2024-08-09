from django.shortcuts import render

# Create your views here.
from django.core.mail import send_mail
from django.http import HttpResponse

def send_test_email(request):
    send_mail(
        'Test Email Subject',
        'This is a test email body.',
        'from@example.com',  # Replace with your sender email
        ['to@example.com'],  # Replace with your recipient email
        fail_silently=False,
    )
    return HttpResponse("Test email sent successfully!")