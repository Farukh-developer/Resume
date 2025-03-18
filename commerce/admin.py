from django.contrib import admin
from .models import Category, Product, User, UserProfile

admin.site.register([Category, Product, User, UserProfile])