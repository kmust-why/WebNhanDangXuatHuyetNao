from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import uuid

# Create your views here.
def index(request):
    return render(request, 'upload.html')

def ThuVien(request):
    return render(request, 'thu-vien.html')

def Upload(request):
    if request.method == 'POST':
        fileUpload = request.FILES.get('file')
        fs = FileSystemStorage()
        fileName = fs.save(str(uuid.uuid1()), fileUpload)
        urlFile = fs.url(fileName)
        return HttpResponse(urlFile)
    else:
        return HttpResponse("Không có")

