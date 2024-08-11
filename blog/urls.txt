from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Home and Contact URLs
    path('contact/', views.contact_view, name='contact'),
    path('', views.home_view, name='home'),

    # Article URLs
    path('articles/', views.article_list, name='article_list'),
    path('articles/create/', views.article_create, name='article_create'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('articles/<int:article_id>/edit/', views.article_edit, name='article_edit'),
    path('articles/<int:article_id>/delete/', views.article_delete, name='article_delete'),

    # Event URLs
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:event_id>/delete/', views.event_delete, name='event_delete'),


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
