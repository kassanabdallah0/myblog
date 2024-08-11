from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from blog import views

urlpatterns = [
    # API Parts : 

    # Sign-Up Endpoint
    path('api/signup/', views.register_api_view, name='signup'),

    # JWT Authentication Endpoints:
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Contact Endpoint : 
    path('api/contact/',views.contact_api_view, name='contact_api'),

    # API endpoints for articles
    path('api/articles/', views.article_list_create_api_view, name='article_list_create_api'),
    path('api/articles/<int:article_id>/', views.article_detail_api_view, name='article_detail_api'),

    # API endpoints for events
    path('api/events/', views.event_list_create_api_view, name='event_list_create_api'),
    path('api/events/<int:event_id>/', views.event_detail_api_view, name='event_detail_api'),
]
