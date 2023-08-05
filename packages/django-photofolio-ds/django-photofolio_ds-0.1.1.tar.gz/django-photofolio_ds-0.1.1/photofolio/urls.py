from django.urls import path
from . import views

app_name = 'photofolio'

urlpatterns = [
    # robots.txt는 반드시 가장 먼저
    path('robots.txt', views.robots),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('gallery/<str:category>/', views.gallery, name='gallery'),
    path('services/', views.services, name='services'),
]
