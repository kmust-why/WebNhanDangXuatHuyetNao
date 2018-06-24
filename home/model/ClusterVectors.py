from annoy import AnnoyIndex
from scipy import spatial
from nltk import ngrams
import random, json, glob, os, codecs, random
import numpy as np

class ClusterVectors:
    
    def ClusterVector(self, fileName):
        # Contruct
        file_index_to_file_name = {}
        file_index_to_file_vector = {}
        chart_image_positions = {}

        # Config
        dims = 2048
        n_nearest_neighbors = 30
        trees = 10000

        # Load file feature vector
        CWD_PATH = os.getcwd()
        infiles = glob.glob(
            os.path.join(CWD_PATH, "static/uploads/image_vectors/") + '*.npz'
            )
        
        infiles.append(
            os.path.join(CWD_PATH, "static/uploads/content_object_detection/image_vectors/" + fileName + ".npz")
        )

        t = AnnoyIndex(dims)
        for file_index, i in enumerate(infiles):
            file_vector = np.loadtxt(i)
            file_name = os.path.basename(i).split('.')[0]
            file_index_to_file_name[file_index] = file_name
            file_index_to_file_vector[file_index] = file_vector
            t.add_item(file_index, file_vector)
        t.build(trees)

        for i in file_index_to_file_name.keys():
            master_file_name = file_index_to_file_name[i]
            master_vector = file_index_to_file_vector[i]
            if(master_file_name == fileName):
                named_nearest_neighbors = []
                nearest_neighbors = t.get_nns_by_item(i, n_nearest_neighbors)
                for j in nearest_neighbors:
                    neighbor_file_name = file_index_to_file_name[j]
                    neighbor_file_vector = file_index_to_file_vector[j]

                    similarity = 1 - spatial.distance.cosine(master_vector, neighbor_file_vector)
                    rounded_similarity = int((similarity * 10000)) / 10000.0

                    named_nearest_neighbors.append({
                        'filename': neighbor_file_name,
                        'similarity': rounded_similarity
                    })

                return named_nearest_neighbors
