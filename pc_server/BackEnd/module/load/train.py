import os

import cv2
import numpy as np
import pytesseract
import tensorflow as tf

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


class Train(object):
    def __init__(self):
        PATH_TO_LABELS = os.path.join('../tensorflow/data', 'mscoco_label_map.pbtxt')

        NUM_CLASSES = 90
        PATH_TO_CKPT = "../tensorflow/model/ssd_mobilenet_v1_coco_2018_01_28/frozen_inference_graph.pb"
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                    use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)


    def recognise_cup(self, image_path):
        detection_graph = self.detection_graph
        category_index = self.category_index
        with detection_graph.as_default():
            with tf.Session(graph=detection_graph) as sess:
                if os.path.exists(image_path):
                    image_np = cv2.imread(image_path)
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    # Each box represents a part of the image where a particular object was detected.
                    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                    # Each score represent how level of confidence for each of the objects.
                    # Score is shown on the result image, together with the class label.
                    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
                    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                    image_np_expanded = np.expand_dims(image_np, axis=0)
                    # Actual detection.
                    (boxes, scores, classes, num) = sess.run(
                        [detection_boxes, detection_scores, detection_classes, num_detections],
                        feed_dict={image_tensor: image_np_expanded})
                    # Visualization of the results of a detection.
                    result = vis_util.visualize_boxes_and_labels_on_image_array2(
                        image_np,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=8)

                    # VideoFileOutput.write(image_np)

                    # cv2.imshow('live_detection', image_np)
                    img = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
                    height, width = img.shape
                    if len(result) > 0:
                        for ymin, xmin, ymax, xmax in result:
                            min_y = int(height * ymin)
                            min_x = int(width * xmin)
                            max_y = int(height * ymax)
                            max_x = int(width * xmax)

                            # sub_img = img[min_y + 50:max_y - 20, min_x + 20:max_x - 20]
                            sub_img = img[min_y:max_y, min_x :max_x ]
                            cv2.imwrite('cup_detection.png', sub_img)

                            code = pytesseract.image_to_string(sub_img, lang='eng', config='-psm 7 digits')
                            # code = pytesseract.image_to_string(sub_img, lang='eng')
                            # code = pytesseract.image_to_string(sub_img, lang='chi_sim')
                            print("recognise: {}".format(code))

                            return "recognise: {}".format(code)
        return "No text recognised."