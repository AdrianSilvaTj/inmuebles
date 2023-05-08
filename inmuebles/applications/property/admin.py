from django.contrib import admin
from .models import Property, Company, Comment

admin.site.register([Property, Company, Comment])

