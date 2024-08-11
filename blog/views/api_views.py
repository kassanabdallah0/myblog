from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from blog.serializers import RegisterSerializer, ContactSerializer, ArticleSerializer, EventSerializer
from django.shortcuts import get_object_or_404
from blog.models import Article, Event

# User Registration API View
@api_view(['POST'])
@permission_classes([AllowAny])
def register_api_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Contact API View
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def contact_api_view(request):
    if request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            send_mail(
                f'Contact Request: {serializer.validated_data["request_type"]}',
                serializer.validated_data['message'],
                serializer.validated_data['email'],
                ['your_email@example.com'],
                fail_silently=False,
            )
            return Response({"message": "Contact request submitted successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Article API Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list_create_api_view(request):
    if request.method == 'GET':
        articles = Article.objects.all().order_by('-published_date')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def article_detail_api_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Event API Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def event_list_create_api_view(request):
    if request.method == 'GET':
        events = Event.objects.all().order_by('-start_date')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def event_detail_api_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
