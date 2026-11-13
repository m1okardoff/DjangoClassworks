from django.contrib import admin
from .models import Card, User


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'avatar', 'created_at')
    search_fields = ('username', 'email')
