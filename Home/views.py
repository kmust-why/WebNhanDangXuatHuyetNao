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
from Home.Dicom2Png import Dicom2Png
from Home.DicomInfo import DicomInfo
from Home.DBConnect import DBConnect
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
    #
    # Chức năng nhập dạng vùng xuất huyết não
    # Đầu vào là tên file muốn nhận dạng được post lên ở "static/uploads/images-detect/*"
    # Kết quả trả về là 1 chuổi json gồm có src kết quả nhận dạng, tên kết quả nhận dạng, tỉ lệ
    #
    tenFile = request.POST.get("tenFile")
    sys.path.append("..")
    MODEL_NAME = 'modules/inference_graph'
    IMAGE_NAME = "static/uploads/images/" + tenFile + ".png"

    CWD_PATH = os.getcwd()
    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'20000_faster_rcnn_resnet101_coco.pb')
    PATH_TO_LABELS = os.path.join(CWD_PATH,'modules/training','labelmap.pbtxt')
    PATH_TO_IMAGE = os.path.join(CWD_PATH,IMAGE_NAME)
    NUM_CLASSES = 4
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, 
                                                                max_num_classes=NUM_CLASSES, 
                                                                use_display_name=False)
    category_index = label_map_util.create_category_index(categories)
    detection_graph = tf.Graph()

    #
    # Load thông tin tri thức để bắt đầu nhận dạng
    #
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.Session(graph=detection_graph)

    #
    # Lấy dữ liệu từ file tri thức
    #
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # (100, 1, 1, 2048)
    feat_avg = detection_graph.get_tensor_by_name('SecondStageBoxPredictor/AvgPool:0')
  #  feat_conv = detection_graph.get_tensor_by_name('SecondStageFeatureExtractor/resnet_v1_101/block4/unit_3/bottleneck_v1/Relu:0')
   # NextIteration_1 = detection_graph.get_tensor_by_name('SecondStageFeatureExtractor/resnet_v1_101/block4/unit_3/bottleneck_v1/conv3/Conv2D:0')

    #
    image = cv2.imread(PATH_TO_IMAGE)
    image_expanded = np.expand_dims(image, axis=0)
    ( boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})


    avg = sess.run(feat_avg, feed_dict={image_tensor: np.array(image_expanded)})
    feature = np.squeeze(np.array(avg))

    print(feature)

    # feature = feature.reshape(-1,50,4032)


    # feature_vector = np.squeeze(avg)  
    # print(feature_vector)
#     print(b)
#    # feature_set = sess.run(image_tensor, {'image_tensor:0': image})

    np.savetxt("static/uploads/image_vectors/b.pnz", feature, delimiter=',')


#     for op  in sess.graph.get_operations():
#         print(str(op.name))
# # #


    
    #
    # List tên file hình ảnh nhận dạng
    #
    arrayPath = []

    #
    # Tim IDDCOM từ tên file DICOM
    #
    db = DBConnect()
    data = db.getTable("SELECT IDDICOM FROM DICOM WHERE TENFILE = '"+ tenFile +"'")
    if len(data) > 0:
        IDDICOM = data[0][0]
    else:
        return HttpResponse("ERROR")

    #
    # Tách kết quả nhận dạng ra nhiều hình ảnh khác nhau
    #
    bienDem = 0
    for indexRow, row in enumerate(scores):
        for indexCol, item in enumerate(row):

            # Chỉ lấy những hình ảnh có điểm >= 50%
            if item >= 0.50:
                IDNHANDANG = str(uuid.uuid1())
                KETQUA = None
                if classes[indexRow][indexCol] == 1:
                    KETQUA = "Tụ máu dưới màn cứng"

                if classes[indexRow][indexCol] == 2:
                    KETQUA = "Tụ máu ngoài màn cứng"

                if classes[indexRow][indexCol] == 3:
                    KETQUA = "Xuất huyết khoang dưới nhện"

                if classes[indexRow][indexCol] == 4:
                    KETQUA = "Xuất huyết não thất"

                db.noneGetTable("INSERT INTO NHANDANG (IDNHANDANG, IDDICOM, TENFILE, KETQUA, PHAMTRAM) VALUES ('" +
                                                        IDNHANDANG + "', '" + 
                                                        IDDICOM + "', '" + 
                                                        IDNHANDANG + "', '" + 
                                                        KETQUA + "', " + 
                                                        str(scores[indexRow][indexCol]) + ")")

                #
                # Chuẩn bị dữ liệu return
                #
                arrayPath.append({
                    "src" : IDNHANDANG, 
                    "ketqua": KETQUA, 
                    "tile": '{0:.2f}'.format(scores[indexRow][indexCol] * 100)
                    })

                renewImg = cv2.imread(PATH_TO_IMAGE)
                arrayboxes = []
                arrayclasses = []
                arrayscores = []
                arrayboxes.append(boxes[indexRow][indexCol])
                arrayclasses.append(classes[indexRow][indexCol])
                arrayscores.append(scores[indexRow][indexCol])
                vis_util.visualize_boxes_and_labels_on_image_array(
                    renewImg,
                    np.array(arrayboxes),
                    np.array(arrayclasses).astype(np.int32),   
                    np.array(arrayscores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=7,
                    min_score_thresh=0.50,        
                    groundtruth_box_visualization_color='red',
                    skip_scores=True,
                    skip_labels=True)
                cv2.imwrite("static/uploads/images-detect/" + IDNHANDANG + ".png", renewImg)
            
    
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