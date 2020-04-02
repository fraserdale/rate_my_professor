from django.contrib import admin
from rango.models import *
# Register your models here.
toreg = [UserProfile, Subject, Department, Professor, Reviews]


admin.site.register(toreg)
