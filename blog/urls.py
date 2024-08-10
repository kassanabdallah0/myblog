from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import signup_view, home_view, contact_view, article_list, article_detail, article_create, article_edit, article_delete

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contact/', contact_view, name='contact'),
    path('', home_view, name='home'),
    path('articles/', article_list, name='article_list'),
    path('articles/create/', article_create, name='article_create'),
    path('articles/<int:article_id>/', article_detail, name='article_detail'),
    path('articles/<int:article_id>/edit/', article_edit, name='article_edit'),
    path('articles/<int:article_id>/delete/', article_delete, name='article_delete'),
]
