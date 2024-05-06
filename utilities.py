import streamlit as st
import time
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from models.research.object_detection.utils import label_map_util
from models.research.object_detection.utils import visualization_utils as viz_utils

PATH_TO_SAVED_MODEL = "trained-inference-graphs/SSD MobileNet V2 FPNLite 640x640 (2200)/saved_model"

@st.cache_resource
def load_model():
    return tf.saved_model.load(PATH_TO_SAVED_MODEL)

def load_image_into_numpy_array(path):
    return np.array(Image.open(path))

def detect_from_image(image_path):
    category_index = label_map_util.create_category_index_from_labelmap("workspace/annotations/label_map_mobilenetc3.pbtxt",
                                                                    use_display_name=True)
    image_np = load_image_into_numpy_array(image_path)
    
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]

    start_time = time.time()
    detect_fn = load_model()
    end_time = time.time()
    elapsed_time = end_time - start_time
    st.success(f"Model Loaded. Took {elapsed_time} seconds")

    detections = detect_fn(input_tensor)

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy() 
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections

    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
    detected_classes = [category_index[class_index]['name'] for class_index in detections['detection_classes']]
    detection_scores = detections['detection_scores']

    filtered_classes = []
    for class_name, score in zip(detected_classes, detection_scores):
        if score > 0.30:
            filtered_classes.append(class_name)
    print(list(set(filtered_classes)))

    image_np_with_detections = image_np.copy()

    viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'],
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=200,
            min_score_thresh=.30,
            agnostic_mode=False)

    plt.figure(figsize=(10, 15))
    plt.xticks([])
    plt.yticks([])
    plt.imshow(image_np_with_detections)
    plt.savefig("output.png", dpi=300, bbox_inches='tight')

    return list(set(filtered_classes))