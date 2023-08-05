import sys
import os

sys.path.append(os.path.dirname(__file__))

import torch
import glob
import cv2
import numpy as np
from kpdet import KpDet
from ad_infer import ADet
from image import load_image, show_image, overlay_heatmap_on_image, align_img


class Detector():
    def __init__(self, ad_ckpt_path, ad_ckpt_arch, kp_ckpt_path, anomaly_classes, device):
        # 'checkpoint/anomaly_detection'

        self.ad = ADet(save_path=ad_ckpt_path, device=device, arch=ad_ckpt_arch)
        self.kpdet = KpDet(model_path=kp_ckpt_path, device=device, anomaly_classes=anomaly_classes)

    def __call__(self, image, show=False):

        image = cv2.resize(image, (640, 640))

        crop_list, crop_orig_xy, *_ = self.kpdet(image)
        # show_image(crop_list + [image])
        score_list = self.ad(crop_list)
        # show_image(score_list)
        bkg = image.copy()
        max_anomaly_score = -1
        num_obj = len(crop_list)
        for crop, xy, score in zip(crop_list, crop_orig_xy, score_list):

            max_anomaly_score = max(max_anomaly_score, np.sum(score > 0) / np.prod(score.shape))
            if show:
                out = overlay_heatmap_on_image(image=crop, heatmap=score)
                bkg = align_img(im1=out, kp1=np.float32([[0, 0], [1, 0], [1, 1], [0, 1]]) * out.shape[0],
                                im2=bkg, kp2=xy)

        anomaly_flag = (num_obj < 2) or (max_anomaly_score > 0.05)
        return anomaly_flag, bkg
