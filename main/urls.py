from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('search/<str:name>/', views.search_by_name, name='search_by_name'),
    path('card/<int:id>/', views.get_card, name='get_card'),
    path('register/', views.register, name='register'),
]
