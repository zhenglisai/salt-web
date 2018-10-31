# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Token(models.Model):
    username = models.CharField(max_length=32)
    token = models.CharField(max_length=32)
    token_time = models.IntegerField(default=0)