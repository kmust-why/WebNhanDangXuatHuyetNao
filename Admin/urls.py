from django.urls import path
from . import views

urlpatterns = [
    path('', views.getViewDangNhap, name='getViewDangNhap'),
]