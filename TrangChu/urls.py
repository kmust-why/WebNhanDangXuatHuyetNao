from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('thu-vien', views.ThuVien, name='ThuVien'),
    path('tai-len', views.Upload, name='Upload'),
]