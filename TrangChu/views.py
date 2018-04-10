import sys
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import uuid
import mritopng
import matplotlib.pyplot as plt
import pydicom
from pydicom.data import get_testdata_files
from datetime import datetime
import json

# Create your views here.
def TrangChu(request):
    return render(request, 'view-trang-chu.html')

def ThuVien(request):
    return render(request, 'view-thu-vien.html')

@csrf_exempt
def postUpload(request):
    if request.method == 'POST':
        tenFile = str(uuid.uuid1())
        fileUpload = request.FILES.get('file')
        fs = FileSystemStorage()
        fileName = fs.save(tenFile, fileUpload)
        urlFile = fs.url(fileName)
        # Đọc thông tin file
        ds = pydicom.dcmread(urlFile)
        # Convert a since file
        mritopng.convert_file(urlFile, 'static/uploads/images/' + tenFile + '.png')

        ketQua = {}
        ketQua['URL'] = 'static/uploads/images/' + tenFile + '.png'
        ketQua['HOTEN'] = str(ds.PatientName)
        ketQua['NOIKHAM'] = str(ds.InstitutionName)
        ketQua['NGAYKHAM'] = str(datetime.strptime(ds.ContentDate, '%Y%m%d'))
        ketQua['MOTA'] = str(ds.StudyDescription)

        return HttpResponse(json.dumps(ketQua))
        # return render(request, 'view-ket-qua.html',
        # {
        #     'HOTEN' : ds.PatientName,
        #     'NOIKHAM' : ds. InstitutionName,
        #     "NGAYKHAM" : datetime.strptime(ds.ContentDate, '%Y%m%d'),
        #     'URLANH' : 'static/uploads/images/' + tenFile + '.png',
        #     "MOTA" : ds.StudyDescription,
        #     "JSON" : ds
        # })
    else:
        return HttpResponse("Không có")

