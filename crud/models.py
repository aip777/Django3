# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class Member(models.Model):
    firstname = models.CharField(max_length=40, blank=False)
    lastname = models.CharField(max_length=40, blank=False)
    mobile_number = models.CharField(max_length=10, blank=True)
    description = models.TextField(max_length=255, blank=False)
    location = models.TextField(max_length=255, blank=False)
    date = models.DateField('%m/%d/%Y')
    created_at = models.DateTimeField('%m/%d/%Y %H:%M:%S')
    updated_at = models.DateTimeField('%m/%d/%Y %H:%M:%S')

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.CharField(max_length=255, )
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ContactList(models.Model):
    text = models.CharField(max_length=255, blank=True)
    search = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    telephone = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class CsvUpload(models.Model):
    name = models.CharField(max_length=255, blank=True)
    # description = models.CharField(max_length=255, blank=True)
    end_date = models.DateTimeField()
    # notes = models.CharField(max_length=255, blank=True)
    affectedtoday = models.CharField(max_length=255, blank=True)
    todayRecovered = models.CharField(max_length=255, blank=True)
    todayDeaths = models.CharField(max_length=255, blank=True)
    todayTests = models.CharField(max_length=255, blank=True)
    totalPositive = models.CharField(max_length=255, blank=True)
    totalRecovered = models.CharField(max_length=255, blank=True)
    totalDeaths = models.CharField(max_length=255, blank=True)
    totalTests = models.CharField(max_length=255, blank=True)
    start_date = models.CharField(max_length=255, blank=True)





