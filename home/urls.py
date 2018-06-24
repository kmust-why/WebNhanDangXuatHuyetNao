from django.urls import path
from . import views

urlpatterns = [
    path('', views.getViewTrangChu, name='getViewTrangChu'),
    path('upload-file', views.postUpload, name='postUpload'),
    path('doc-thong-tin-file-dicom', views.docThongTinFileDicom, name='docThongTinFileDicom'),
    path('nhan-dang-vung-xuat-huyet-nao', views.nhanDangVungXuatHuyet, name='nhanDangVungXuatHuyet'),
    path('hinh-anh-lien-quan', views.hinhAnhLienQuan, name='hinhAnhLienQuan'),
]