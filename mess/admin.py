from django.contrib import admin
from .models import Message, AdminMessage

admin.site.register(Message)
admin.site.register(AdminMessage)