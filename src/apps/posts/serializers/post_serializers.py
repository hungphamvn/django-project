from rest_framework import serializers

from ..models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {'commented_by': {'default': serializers.CurrentUserDefault()}}


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
