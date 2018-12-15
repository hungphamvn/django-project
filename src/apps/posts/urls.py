from django.conf.urls import url, include
from .views.auth_views import LoginAPIView
from rest_framework.routers import DefaultRouter
from apps.posts.views.post_views import *

router = DefaultRouter()
router.register('post', PostViewSet, basename='post')
router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'login/$', LoginAPIView.as_view(), name='login'),
]
