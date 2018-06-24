import os, sys, cv2, uuid, json, glob, numpy as np, tensorflow as tf,random, codecs, random
from modules.utils import label_map_util
from modules.utils import visualization_utils as vis_util
from annoy import AnnoyIndex
from scipy import spatial
from nltk import ngrams

class SimilarImages:
    SESSION = None
    FEATURE_TENSOR = None

    def __init__(self, *args, **kwargs):
        self.SESSION = tf.Session()
        with tf.gfile.FastGFile('modules/inference_graph/classify_image_graph_def.pb', 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')
            self.FEATURE_TENSOR = self.SESSION.graph.get_tensor_by_name('pool_3:0')

    def FeatureVector(self, fileName, pathOutput):
        if not os.path.isfile(fileName):
            print("File not exist: " + fileName)
            return None
        image_data = tf.gfile.FastGFile(fileName, 'rb').read()
        feature_set = self.SESSION.run(self.FEATURE_TENSOR, {'DecodeJpeg/contents:0': image_data})
        feature_vector = np.squeeze(feature_set)        
        outfile_name = os.path.basename(fileName).split('.')[0] + ".npz"
        out_path = os.path.join(pathOutput, outfile_name)
        np.savetxt(out_path, feature_vector, delimiter=',')
                