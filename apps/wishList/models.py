from __future__ import unicode_literals
from django.db import models
from ..login_reg_app.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(max_length = 1000)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Wish(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
