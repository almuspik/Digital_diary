

# Register your models here.
from django.contrib import admin
from .models import DiaryEntry, Userprofile

admin.site.register(DiaryEntry)
admin.site.register(Userprofile)
