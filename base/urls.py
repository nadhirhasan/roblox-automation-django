from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('generate-serial/', views.generate_serial_key, name='generate_serial_key'),
    path('create-subscription/', views.create_subscription, name='create_subscription'),
    path('verify-serial-key/', views.verify_serial_key, name='verify_serial_key'),
    path('check-subscription/', views.check_subscription, name='check_subscription'),
    path('',views.main,name='main')
]

