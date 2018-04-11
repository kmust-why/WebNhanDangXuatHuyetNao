import os
import sys
import cv2
import numpy as np
import tensorflow as tf
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

from modules.utils import label_map_util
from modules.utils import visualization_utils as vis_util

# Create your views here.
def getViewTrangChu(request):
    return render(request, 'view-trang-chu.html')

def ThuVien(request):
    return render(request, 'view-thu-vien.html')

def TimHieuXuatHuyetNao(request):
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
        ketQua['HOTEN'] = str(ds.PatientName)
        ketQua['NOIKHAM'] = str(ds.InstitutionName)
        ketQua['NGAYKHAM'] = str(datetime.strptime(ds.ContentDate, '%Y%m%d'))
        ketQua['MOTA'] = str(ds.StudyDescription)
        ketQua['URL'] = NhanDang('static/uploads/images/' + tenFile + '.png', tenFile)
        return HttpResponse(json.dumps(ketQua))
    else:
        return HttpResponse("Không có")

def NhanDang(duongDanHinh, tenFile):
    sys.path.append("..")
    MODEL_NAME = 'modules/inference_graph'
    IMAGE_NAME = duongDanHinh
    CWD_PATH = os.getcwd()
    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
    PATH_TO_LABELS = os.path.join(CWD_PATH,'modules/training','labelmap.pbtxt')
    PATH_TO_IMAGE = os.path.join(CWD_PATH,IMAGE_NAME)
    NUM_CLASSES = 6
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.Session(graph=detection_graph)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    image = cv2.imread(PATH_TO_IMAGE)
    image_expanded = np.expand_dims(image, axis=0)
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})
    vis_util.visualize_boxes_and_labels_on_image_array(
        image,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.80)
    cv2.imwrite("static/uploads/images-detect/" + tenFile + ".png", image)
    return "static/uploads/images-detect/" + tenFile + ".png"