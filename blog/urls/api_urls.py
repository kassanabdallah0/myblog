from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from blog.views import api_views as views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
# Schema view for Swagger and ReDoc
schema_view = get_schema_view(
   openapi.Info(
      title="My Blog API",
      default_version='v1',
      description="API documentation for My Blog",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="sikapika151@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


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

    # Swagger and ReDoc Endpoints:
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)