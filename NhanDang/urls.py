from django.urls import path
from . import views

urlpatterns = [
    path('', views.TrangChu, name='TrangChu'),
    path('upload-file', views.postUpload, name='postUpload'),
    path('thu-vien', views.ThuVien, name='ThuVien'),
]