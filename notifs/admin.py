from django.contrib import admin
from .models import Notification, AgentNotification

admin.site.register(Notification)
admin.site.register(AgentNotification)