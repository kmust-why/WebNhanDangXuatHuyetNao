import os, sys, cv2, uuid, json, glob, numpy as np, tensorflow as tf, pydicom
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from pydicom.data import get_testdata_files
from datetime import datetime
from modules.utils import label_map_util
from modules.utils import visualization_utils as vis_util
from datetime import datetime
from home.model.Dicom2Png import Dicom2Png
from home.model.DicomInfo import DicomInfo
from home.model.DBConnect import DBConnect
from home.model.DetectionBrainHemorrhage import DetectionBrainHemorrhage
from annoy import AnnoyIndex
from scipy import spatial
from nltk import ngrams

def getViewTrangChu(request):
    return render(request, 'view-trang-chu-v2.html')

def ThuVien(request):
    return render(request, 'view-thu-vien.html')

def TimHieuXuatHuyetNao(request):
    return render(request, 'view-thu-vien.html')

@csrf_exempt
def postUpload(request):
    #
    # Hàm này sẽ nhận file dicom uopload lên
    # Chuyển đổ file dicom sang hình ảnh
    # Tên file được tạo tự động theo chuổi UUID
    # Hàm sẽ trả về tên file
    #
    if request.method == 'POST':
        randomTenFile = str(uuid.uuid1())
        fileUpload = request.FILES.get('file')
        fs = FileSystemStorage()

        # Lưu file vào thư mục với tên mới
        fileName = fs.save(randomTenFile, fileUpload)

        # Lấy đường đẫn file
        urlFile = fs.url(fileName)

        # Chuyển đổi file DICOM sanh hình ảnh
        dicom = Dicom2Png()
        dicom.Convert(urlFile, randomTenFile)
        
        #
        # Thêm thong tin file vào  DB
        #
        db = DBConnect()
        IDDICOM = str(uuid.uuid1())
        THOIGIAN = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.noneGetTable("INSERT INTO DICOM (IDDICOM, TENFILE, THOIGIAN) VALUES ('"+ IDDICOM +"', '" + randomTenFile + "', '" + THOIGIAN + "')")

        return HttpResponse(randomTenFile)
    else:
        return HttpResponse("FILE NOT FOUND")

@csrf_exempt
def docThongTinFileDicom(request):
    #
    # Đọc thồng tin file dicom
    # Đầu vào là tên file dicom ở đường dẫn static/uploads/dicom
    #
    if request.method == 'POST':
        dicom = DicomInfo()
        path = "static/uploads/dicom/" + request.POST.get("tenFile")
        return HttpResponse(dicom.getInfoJson(path))
    else:
        return HttpResponse("FILE NOT FOUND")

@csrf_exempt
def nhanDangVungXuatHuyet(request):
    tenFile = request.POST.get("tenFile")
    detection = DetectionBrainHemorrhage()
    arrayPath = detection.Detection(tenFile + ".png")
    return HttpResponse(json.dumps(arrayPath)) 

@csrf_exempt
def hinhAnhLienQuan(request):
    if request.method == 'POST':
        ketQua = []
        tenFile = request.POST.get("tenFile")
        db = DBConnect()
        with open("static/uploads/nearest_neighbors/" + tenFile + ".json") as f:
            for item in json.load(f):
                data = db.getTable("SELECT IDDICOM FROM DICOM WHERE TENFILE = '" + item["filename"] + "'")
                ketQua.append(
                    db.getTable("SELECT TENFILE, KETQUA, PHAMTRAM FROM NHANDANG WHERE IDDICOM = '" + data[0][0] + "'")
                )

        return HttpResponse(json.dumps(ketQua))
    else:
        return HttpResponse("404")