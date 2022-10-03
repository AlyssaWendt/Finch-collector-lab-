from django.contrib import admin
from .models import Finch # import the Artist model from models.py
# Register your models here.

admin.site.register(Finch) # this line will add the model to the admin panel
