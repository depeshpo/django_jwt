from django.contrib import admin
from .models import User, Profile

site_to_register = [User, Profile]

admin.site.register(site_to_register)