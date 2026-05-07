from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)