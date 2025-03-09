from django.contrib import admin
from .models import TrackingHistory, CurrentBalance
# Register your models here.

admin.site.register(TrackingHistory)
admin.site.register(CurrentBalance)
