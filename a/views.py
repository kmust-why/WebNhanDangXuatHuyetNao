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
from home.model.ClusterVectors import ClusterVectors
from annoy import AnnoyIndex
from scipy import spatial
from nltk import ngrams

detection = DetectionBrainHemorrhage()

def getViewTrangChu(request):
    return render(request, 'view-trang-chu-v2.html')

@csrf_exempt
def postUpload(request):
    if request.method == 'POST':
        randomTenFile = str(uuid.uuid1())
        fileUpload = request.FILES.get('file')
        fs = FileSystemStorage()

        fileName = fs.save(randomTenFile, fileUpload)
        urlFile = fs.url(fileName)

        dicom = Dicom2Png()
        dicom.Convert(urlFile, randomTenFile)
        
        db = DBConnect()
        IDDICOM = str(uuid.uuid1())
        THOIGIAN = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.noneGetTable("INSERT INTO DICOM(IDDICOM, TENFILE, THOIGIAN) VALUES ('{0}', '{1}', '{2}')".format(
            IDDICOM, randomTenFile, THOIGIAN
        ))

        return HttpResponse(randomTenFile)
    else:
        return HttpResponse("FILE NOT FOUND")

@csrf_exempt
def docThongTinFileDicom(request):
    if request.method == 'POST':
        dicom = DicomInfo()
        path = "static/uploads/dicom/" + request.POST.get("tenFile")
        return HttpResponse(dicom.getInfoJson(path))
    else:
        return HttpResponse("FILE NOT FOUND")

@csrf_exempt
def nhanDangVungXuatHuyet(request):
    if request.method == 'POST':
        tenFile = request.POST.get("tenFile")
        arrayPath = detection.Detection("static/uploads/images/{0}.png".format(tenFile))

        # Lưu kết quả vào DB
        db = DBConnect()
        IDDICOM = db.getTable("SELECT IDDICOM FROM DICOM WHERE TENFILE = '{0}'".format(tenFile))
        for item in arrayPath or []:
            db.noneGetTable("INSERT INTO NHANDANG(IDNHANDANG, IDDICOM, TENFILE, KETQUA, PHAMTRAM) VALUES ('{0}', '{1}', '{2}', '{3}', {4})".format(
                str(uuid.uuid1()), IDDICOM[0][0], item["src"], item["ketqua"], item["tile"]
            ))
        return HttpResponse(json.dumps(arrayPath)) 

@csrf_exempt
def hinhAnhLienQuan(request):
    if request.method == 'POST':
        cluster = ClusterVectors()
        ketQua = []
        tenFile = request.POST.get("tenFile")
        db = DBConnect()
        for item in cluster.ClusterVector(tenFile)[1:]:
            print(item["similarity"])
            data = db.getTable("SELECT IDDICOM FROM DICOM WHERE TENFILE = '{0}'".format(
                item["filename"]
            ))
            tmp = db.getTable("SELECT TENFILE, KETQUA, PHAMTRAM FROM NHANDANG WHERE IDDICOM = '{0}'".format(
                        data[0][0]
                    ))
            for kq in tmp:    
                ketQua.append({
                    'tenfile' : kq[0],
                    'ketQua' : kq[1],
                    'phamTram' : kq[2],
                })
           
        return HttpResponse(json.dumps(ketQua))
    else:
        return HttpResponse("404")