from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

import factory
from apps.posts.models import *


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User


class PostFactory(factory.DjangoModelFactory):
    class Meta:
        model = Post


class PostAPITestCase(APITestCase):
    test_username = 'test_user'
    test_password = 'test_password'
    token = None
    user = None

    def setUp(self):
        user = self.user = UserFactory(username=self.test_username)
        user.set_password(self.test_password)
        user.save()

        payload = api_settings.JWT_PAYLOAD_HANDLER(user)
        self.token = api_settings.JWT_ENCODE_HANDLER(payload)

    def tearDown(self):
        self.client.credentials()

    def test_create_post_should_success(self):
        url = reverse('api:post-list')

        data = {
            "title": "post title",
            "content": "post content"
        }
        auth = 'JWT {0}'.format(self.token)

        resp = self.client.post(url, data=data, **{'HTTP_AUTHORIZATION': auth}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(resp.data)

    def test_delete_post_should_success(self):
        post = PostFactory(created_by=self.user)
        self.assertEqual(Post.objects.count(), 1)
        url = reverse('api:post-detail', kwargs={'pk': post.id})

        auth = 'JWT {0}'.format(self.token)

        resp = self.client.delete(url, **{'HTTP_AUTHORIZATION': auth}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_comment_into_post_should_success(self):
        post = PostFactory(created_by=self.user)
        url = reverse('api:comment-list')

        data = {
            "message": "post title",
            "post": post.id

        }
        auth = 'JWT {0}'.format(self.token)

        resp = self.client.post(url, data=data, **{'HTTP_AUTHORIZATION': auth}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(resp.data)

    def test_delete_comment_should_success(self):
        post = PostFactory(created_by=self.user)
        self.assertEqual(Post.objects.count(), 1)
        url = reverse('api:post-detail', kwargs={'pk': post.id})

        auth = 'JWT {0}'.format(self.token)

        resp = self.client.delete(url, **{'HTTP_AUTHORIZATION': auth}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
