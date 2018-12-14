from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User


# Create your models here.

class Post(TimeStampedModel):
    title = models.CharField(max_length=250)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(TimeStampedModel):
    message = models.CharField(max_length=250)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
