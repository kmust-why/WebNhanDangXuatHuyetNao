from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import uuid
import json

# Create your views here.
def getViewDangNhap(request):
    return render(request, 'admin/view-dang-nhap.html')
