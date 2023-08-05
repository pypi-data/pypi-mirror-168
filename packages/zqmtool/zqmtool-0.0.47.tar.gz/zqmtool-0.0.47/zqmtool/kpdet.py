import os, sys

sys.path.append(os.path.dirname(__file__))

import torch
import time
from glob import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import defaultdict
from multiprocessing.pool import Pool
from sklearn.cluster import KMeans

from image import align_img


def draw_bbox(img, bbox, ):
    img_w, img_h = img.shape[:2]
    bbox_center_x, bbox_center_y = bbox[0] * img_w, bbox[1] * img_h
    bbox_w, bbox_h = bbox[2] * img_w, bbox[3] * img_h
    bbox_min_x, bbox_max_x = bbox_center_x - (bbox_w / 2), bbox_center_x + (bbox_w / 2)
    bbox_min_y, bbox_max_y = bbox_center_y - (bbox_h / 2), bbox_center_y + (bbox_h / 2)
    start_point = (int(bbox_min_x), int(bbox_min_y))
    end_point = (int(bbox_max_x), int(bbox_max_y))
    img_w_bbox = cv2.rectangle(img, start_point, end_point, (255, 0, 0), thickness=2)
    cv2.imwrite(f'{time.time()}.png', img_w_bbox, )


def rotate_kps(kp1):
    cx, cy = np.mean(kp1, axis=0)
    kp = [[]] * 4
    for kpi in kp1:
        if kpi[1] < cy:
            if kpi[0] < cx:
                kp[0] = kpi
            else:
                kp[1] = kpi
        else:
            if kpi[0] < cx:
                kp[3] = kpi
            else:
                kp[2] = kpi

    if not np.all([len(kpi) > 0 for kpi in kp]):
        return None

    kp1 = np.asarray(kp)
    return kp1


def check_bbox_overlapping(box1, box2):
    def isOverlapping1D(min1, max1, min2, max2):
        return max1 - min2 > 0 and max2 - min1 > 0

    return isOverlapping1D(*box1['x'], *box2['x']) and isOverlapping1D(*box1['y'], *box2['y'])


# FOR KEYPOINT DETECTION
class KpDet:

    def __init__(self, model_path, anomaly_classes=None, device='cuda:0', img_size=640):
        self.anomaly_classes = anomaly_classes
        self.model = torch.hub.load('yolov5', 'custom', path=model_path, force_reload=True,
                                    source='local').to(device)
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        self.img_size = img_size

    def load_obj_det_result(self, img):
        with torch.no_grad():
            results = self.model(img)

        self.crop_xy_list = []
        self.keypoint_list = []
        for obj_id, res in enumerate(results.crop(save=False)):
            label = res['label'].split(' ')[0]
            cls = res['cls'].item()
            xmin, ymin, xmax, ymax = list(map(lambda x: int(x.item()), res["box"]))
            if label == 'KP':
                self.keypoint_list.append([cls, (xmin + xmax) / 2, (ymin + ymax) / 2])
            elif label == 'RFID':
                self.crop_xy_list.append([xmin, xmax, ymin, ymax])

    def gen_crop_kp_dict(self, ):
        self.crop_kp_dict = defaultdict(dict)
        for keypoint in self.keypoint_list:
            cls, x, y = keypoint
            for crop_id, crop in enumerate(self.crop_xy_list):
                if (x > crop[0] and x < crop[1]) and (y > crop[2] and y < crop[3]):
                    if crop_id not in self.crop_kp_dict.keys():
                        self.crop_kp_dict[crop_id]['crop'] = crop
                        self.crop_kp_dict[crop_id]['kps'] = []
                        self.crop_kp_dict[crop_id]['kps_orig'] = []

                    x_ = x - crop[0]
                    y_ = y - crop[2]
                    self.crop_kp_dict[crop_id]['kps'].append([x_, y_])
                    self.crop_kp_dict[crop_id]['kps_orig'].append([x, y])

        crop_ids = list(self.crop_kp_dict.keys())
        for crop_id in crop_ids:
            orig_kps = self.crop_kp_dict[crop_id]['kps_orig']
            if len(orig_kps) < 4:
                self.crop_kp_dict.pop(crop_id)
            elif len(orig_kps) > 4:
                self.crop_kp_dict[crop_id]['kps'] = []
                orig_kps = KMeans(n_clusters=4).fit(orig_kps).cluster_centers_
                self.crop_kp_dict[crop_id]['kps_orig'] = orig_kps
                crop = self.crop_kp_dict[crop_id]['crop']
                for x, y in orig_kps:
                    x_ = x - crop[0]
                    y_ = y - crop[2]
                    self.crop_kp_dict[crop_id]['kps'].append([x_, y_])

        for crop_id in self.crop_kp_dict.keys():
            self.crop_kp_dict[crop_id]['kps'] = rotate_kps(self.crop_kp_dict[crop_id]['kps'])
            self.crop_kp_dict[crop_id]['kps_orig'] = rotate_kps(self.crop_kp_dict[crop_id]['kps_orig'])

        for crop_id in self.crop_kp_dict.keys():
            self.crop_kp_dict[crop_id]['is_anomaly'] = 0

    def align_crop(self, img, crop_kps, kps):
        crop_img = img[crop_kps[2]:crop_kps[3], crop_kps[0]:crop_kps[1]]
        kp1 = np.asarray([kp for kp in kps])
        crop_img_aligned = align_img(crop_img, kp1)
        return crop_img_aligned

    def preprocess_image_for_det(self, image):
        assert image.shape[:2] == (640, 640)
        image = self.clahe.apply(image)
        return image

    def __call__(self, img, label=None):

        img_for_det = self.preprocess_image_for_det(img.copy())
        self.load_obj_det_result(img_for_det)

        self.gen_crop_kp_dict()
        if label is not None:
            for label_i in label:
                anomaly_type = self.anomaly_classes['names'][int(label_i.split(' ')[0])]
                bbox = [float(elem) for elem in label_i.split(' ')[1:]]
                if anomaly_type == 'OK' or anomaly_type == 'KT' or anomaly_type == 'KTMD':
                    continue

                img_w, img_h = img.shape[:2]
                bbox_center_x, bbox_center_y = bbox[0] * img_w, bbox[1] * img_h
                bbox_w, bbox_h = bbox[2] * img_w, bbox[3] * img_h
                bbox_min_x, bbox_max_x = bbox_center_x - (bbox_w / 2), bbox_center_x + (bbox_w / 2)
                bbox_min_y, bbox_max_y = bbox_center_y - (bbox_h / 2), bbox_center_y + (bbox_h / 2)
                box1 = {'x': (bbox_min_x, bbox_max_x), 'y': (bbox_min_y, bbox_max_y)}
                for crop_id in self.crop_kp_dict.keys():
                    # xmin, xmax, ymin, ymax = self.crop_kp_dict[crop_id]['crop']
                    orig_kps = self.crop_kp_dict[crop_id]['kps_orig']
                    xmin, xmax = np.min(orig_kps[:, 0]), np.max(orig_kps[:, 0])
                    ymin, ymax = np.min(orig_kps[:, 1]), np.max(orig_kps[:, 1])
                    margin = 10
                    box2 = {'x': (xmin + margin, xmax - margin), 'y': (ymin + margin, ymax - margin)}
                    if check_bbox_overlapping(box1, box2):
                        self.crop_kp_dict[crop_id]['is_anomaly'] = 1

        crops = []
        crop_orig_xy = []
        crop_is_anomaly = []
        for crop_id in self.crop_kp_dict.keys():
            crop = self.align_crop(img, self.crop_kp_dict[crop_id]['crop'], self.crop_kp_dict[crop_id]['kps'])
            if crop is not None:
                crops.append(crop)
                crop_orig_xy.append(self.crop_kp_dict[crop_id]['kps_orig'])
                crop_is_anomaly.append(self.crop_kp_dict[crop_id]['is_anomaly'])

        return crops, crop_orig_xy, crop_is_anomaly
