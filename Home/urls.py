from django.urls import path
from . import views

urlpatterns = [
    path('', views.getViewTrangChu, name='getViewTrangChu'),
    path('upload-file', views.postUpload, name='postUpload'),
    path('thu-vien', views.ThuVien, name='ThuVien'),
    path('tim-hieu-xuat-huyet-nao', views.ThuVien, name='ThuVien'),
]