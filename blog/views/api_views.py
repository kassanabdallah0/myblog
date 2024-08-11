from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from blog.serializers import RegisterSerializer, ContactSerializer, ArticleSerializer, EventSerializer
from django.shortcuts import get_object_or_404
from blog.models import Article, Event
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




# User Registration API View
@swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    responses={
        201: RegisterSerializer,
        400: 'Bad Request'
    },
    operation_description="Register a new user."
)

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

@swagger_auto_schema(
    method='post',
    request_body=ContactSerializer,
    responses={
        201: openapi.Response(description="Contact request submitted successfully."),
        400: 'Bad Request'
    },
    operation_description="Submit a contact request."
)
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
@swagger_auto_schema(
    method='get',
    responses={200: ArticleSerializer(many=True)},
    operation_description="Retrieve a list of all articles."
)
@swagger_auto_schema(
    method='post',
    request_body=ArticleSerializer,
    responses={
        201: ArticleSerializer,
        400: 'Bad Request'
    },
    operation_description="Create a new article."
)
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

@swagger_auto_schema(
    method='get',
    responses={200: ArticleSerializer},
    operation_description="Retrieve details of a specific article."
)
@swagger_auto_schema(
    method='put',
    request_body=ArticleSerializer,
    responses={
        200: ArticleSerializer,
        400: 'Bad Request'
    },
    operation_description="Update a specific article."
)
@swagger_auto_schema(
    method='patch',
    request_body=ArticleSerializer,
    responses={
        200: ArticleSerializer,
        400: 'Bad Request'
    },
    operation_description="Partially update a specific article."
)
@swagger_auto_schema(
    method='delete',
    responses={204: 'No Content'},
    operation_description="Delete a specific article."
)

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
@swagger_auto_schema(
    method='get',
    responses={200: EventSerializer(many=True)},
    operation_description="Retrieve a list of all events."
)
@swagger_auto_schema(
    method='post',
    request_body=EventSerializer,
    responses={
        201: EventSerializer,
        400: 'Bad Request'
    },
    operation_description="Create a new event."
)
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

@swagger_auto_schema(
    method='get',
    responses={200: EventSerializer},
    operation_description="Retrieve details of a specific event."
)
@swagger_auto_schema(
    method='put',
    request_body=EventSerializer,
    responses={
        200: EventSerializer,
        400: 'Bad Request'
    },
    operation_description="Update a specific event."
)
@swagger_auto_schema(
    method='patch',
    request_body=EventSerializer,
    responses={
        200: EventSerializer,
        400: 'Bad Request'
    },
    operation_description="Partially update a specific event."
)
@swagger_auto_schema(
    method='delete',
    responses={204: 'No Content'},
    operation_description="Delete a specific event."
)
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
