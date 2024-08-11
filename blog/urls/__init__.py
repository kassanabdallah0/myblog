from .api_urls import urlpatterns as api_urlpatterns
from .web_urls import urlpatterns as web_urlpatterns

urlpatterns = api_urlpatterns + web_urlpatterns
