import os, sys, cv2, uuid, json, glob, numpy as np, tensorflow as tf
from modules.utils import label_map_util
from modules.utils import visualization_utils as vis_util
from home.model.SimilarImages import SimilarImages

class DetectionBrainHemorrhage:
    SESSION = None
    CATEGORIES_INDEX = None
    IMAGE_TENSOR = None
    DETECTION_BOXES = None
    DETECTION_SCORES = None
    DETECTION_CLASSES = None
    NUM_DETECTIONS = None
    SIMILAR = None

    def __init__(self, *args, **kwargs):
        label_map = label_map_util.load_labelmap("modules/training/labelmap.pbtxt")
        categories = label_map_util.convert_label_map_to_categories(
            label_map, 
            max_num_classes = 4, 
            use_display_name = False)
        self.CATEGORIES_INDEX = label_map_util.create_category_index(categories)
        detection_graph = tf.Graph()

        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile("modules/inference_graph/50000_rfcn_resnet101_coco.pb", 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
                self.SESSION = tf.Session(graph=detection_graph)

        self.IMAGE_TENSOR = detection_graph.get_tensor_by_name('image_tensor:0')
        self.DETECTION_BOXES = detection_graph.get_tensor_by_name('detection_boxes:0')
        self.DETECTION_SCORES = detection_graph.get_tensor_by_name('detection_scores:0')
        self.DETECTION_CLASSES = detection_graph.get_tensor_by_name('detection_classes:0')
        self.NUM_DETECTIONS = detection_graph.get_tensor_by_name('num_detections:0')

        self.SIMILAR = SimilarImages()

    def Detection(self, fileName):
        if not os.path.isfile(fileName):
            print("File not exist: " + fileName)
            return None
        image = cv2.imread(fileName)

        # Lưu vecter đặt trưng của đối tượng
        self.SIMILAR.FeatureVector(fileName, "static/uploads/image_vectors/")

        image_expanded = np.expand_dims(image, axis=0)
        ( boxes, scores, classes, num) = self.SESSION.run(
                [self.DETECTION_BOXES, self.DETECTION_SCORES, self.DETECTION_CLASSES, self.NUM_DETECTIONS],
                feed_dict={self.IMAGE_TENSOR: image_expanded}
            )
        
        arrayPath = []
        bienDem = 0
        for indexRow, row in enumerate(scores):
            for indexCol, item in enumerate(row):
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
                    arrayPath.append({
                        "src" : IDNHANDANG, 
                        "ketqua": KETQUA, 
                        "tile": '{0:.2f}'.format(scores[indexRow][indexCol] * 100)
                        })

                    renewImg = cv2.imread(fileName)
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
                            self.CATEGORIES_INDEX,
                            use_normalized_coordinates=True,
                            line_thickness=7,
                            min_score_thresh=0.50,
                            skip_scores=True,
                            skip_labels=True
                        )

                    # Drop image
                    box = tuple(np.array(arrayboxes)[0].tolist())
                    ymin, xmin, ymax, xmax = box
                    height, width, channels = renewImg.shape
                    ymin = int(ymin * height + 7)
                    xmin = int(xmin * width + 7)
                    ymax = int(ymax * height - 7)
                    xmax = int(xmax * width - 7)
                    crop_img = renewImg[ymin:ymax, xmin:xmax]

                    cv2.imwrite(
                        "static/uploads/content_object_detection/content_object/{0}.png".format(IDNHANDANG), 
                        crop_img
                        )

                    self.SIMILAR.FeatureVector(
                        "static/uploads/content_object_detection/content_object/{0}.png".format(IDNHANDANG), 
                        "static/uploads/content_object_detection/image_vectors/"
                        )

                    # Lưu hình nhận dạng
                    cv2.imwrite("static/uploads/images-detect/{0}.png".format(IDNHANDANG), renewImg)
        return arrayPath