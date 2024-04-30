import streamlit as st
import time
import cv2
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from models.research.object_detection.utils import label_map_util
from models.research.object_detection.utils import visualization_utils as viz_utils

PATH_TO_SAVED_MODEL = "trained-inference-graphs/SSD Resnet50 V1 FPN 640x640 (RetinaNet50)/saved_model"


def load_image_into_numpy_array(path):
    return np.array(Image.open(path))

@st.cache_resource
def detect_from_image(image_path):
    category_index = label_map_util.create_category_index_from_labelmap("workspace/annotations/label_map.pbtxt",
                                                                    use_display_name=True)
    image_np = load_image_into_numpy_array(image_path)
    
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]

    start_time = time.time()
    detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
    end_time = time.time()
    elapsed_time = end_time - start_time
    st.success(f"Model Loaded. Took {elapsed_time} seconds")

    detections = detect_fn(input_tensor)

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy() 
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections

    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

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

    plt.figure()
    plt.imshow(image_np_with_detections)
    plt.savefig("output.png", dpi=300, bbox_inches='tight')

def detect_from_webcam():
    # category_index = label_map_util.create_category_index_from_labelmap("workspace/annotations/label_map.pbtxt",
    #                                                                 use_display_name=True)

    FRAME_WINDOW = st.image([])
    st.write("Webcam Live Feed")
    button = st.empty()
    start = button.button('Start')
    if start:
        stop = button.button('Stop')

        cap = cv2.VideoCapture("192.168.1.7/4747")

        while cap.isOpened:
            ret, image_np = cap.read()
            # image_np_expanded = np.expand_dims(image_np, axis=0)

            # input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        
            # start_time = time.time()
            # detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
            # end_time = time.time()
            # elapsed_time = end_time - start_time
            # st.success(f"Model Loaded. Took {elapsed_time} seconds")
        
            # detections, predictions_dict, shapes = detect_fn(input_tensor)

            # label_id_offset = 1
            # image_np_with_detections = image_np.copy()

            # viz_utils.visualize_boxes_and_labels_on_image_array(
            #     image_np_with_detections,
            #     detections['detection_boxes'][0].numpy(),
            #     (detections['detection_classes'][0].numpy() + label_id_offset).astype(int),
            #     detections['detection_scores'][0].numpy(),
            #     category_index,
            #     use_normalized_coordinates=True,
            #     max_boxes_to_draw=200,
            #     min_score_thresh=.30,
            #     agnostic_mode=False)
        
            FRAME_WINDOW.image(cv2.imshow('object detection', cv2.COLOR_RGB2BGR))

            if stop:
                cap.release()
                cv2.destroyAllWindows()
        else:
            st.write('Your Camera is Not Detected !')