
from django.db import models


class Post(models.Model):
        author = models.CharField(max_length=100)
        title = models.CharField(max_length=100)
