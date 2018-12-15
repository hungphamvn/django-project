from django.conf.urls import url
from .views.auth_views import LoginAPIView


urlpatterns = [
    url(r'login/$', LoginAPIView.as_view(), name='login'),
]