from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser, G2GSuggestion, PosSuggestion

# Register your models here.
admin.site.register(AppUser, UserAdmin)
admin.site.register(G2GSuggestion)
admin.site.register(PosSuggestion)
