import random
import os
from random import sample
import numpy as np
import pickle
import time
import sys
import copy
import warnings
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
from tqdm import tqdm, trange
from collections import OrderedDict
from sklearn.metrics import roc_auc_score, roc_curve, f1_score, accuracy_score, recall_score, precision_score, \
    confusion_matrix, precision_recall_curve
from scipy.ndimage import gaussian_filter
from skimage import morphology
from skimage.segmentation import mark_boundaries
import cv2

## torch module
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader

## choose Efficient model
from efficientnet_pytorch import EfficientNet

from torch.utils.data import Dataset
from torchvision import transforms as T


class EfficientNetModified(EfficientNet):
    '''
    The function of the existing model(original) will extract only the last layer feature.
    This time, we're going to pull out the features that we want

    ref) https://github.com/lukemelas/EfficientNet-PyTorch/blob/master/efficientnet_pytorch/model.py
    '''

    def extract_features(self, inputs, block_num):
        """ Returns list of the feature at each level of the EfficientNet """

        feat_list = []
        # Stem
        x = self._swish(self._bn0(self._conv_stem(inputs)))

        iter = 1
        for idx, block in enumerate(self._blocks):
            drop_connect_rate = self._global_params.drop_connect_rate
            if drop_connect_rate:
                drop_connect_rate *= float(idx) / len(self._blocks)  # scale drop connect_rate
            x = block(x, drop_connect_rate=drop_connect_rate)
            if iter in block_num:
                feat_list.append(x)
            iter += 1

        # Head
        x = self._swish(self._bn1(self._conv_head(x)))
        # feat_list.append(F.adaptive_avg_pool2d(x, 1))
        # feat_list.append(x)

        return feat_list

    def extract_entire_features(self, inputs):
        """ Returns list of the feature at each level of the EfficientNet """

        feat_list = []
        # Stem
        x = self._swish(self._bn0(self._conv_stem(inputs)))
        # feat_list.append(F.adaptive_avg_pool2d(x, 1))
        feat_list.append(x)

        for idx, block in enumerate(self._blocks):
            drop_connect_rate = self._global_params.drop_connect_rate
            if drop_connect_rate:
                drop_connect_rate *= float(idx) / len(self._blocks)  # scale drop connect_rate
            x = block(x, drop_connect_rate=drop_connect_rate)
            feat_list.append(x)

        # Head
        x = self._swish(self._bn1(self._conv_head(x)))
        # feat_list.append(F.adaptive_avg_pool2d(x, 1))
        feat_list.append(x)

        return feat_list

class MVTecDataset(Dataset):
    def __init__(self, dataset_path='./mvtec_anomaly_detection', class_name='hazelnut', is_train=True,
                 resize=256, cropsize=224):
        self.dataset_path = dataset_path
        self.class_name = class_name
        self.is_train = is_train
        self.resize = resize
        self.cropsize = cropsize

        # load dataset
        self.x, self.y, self.mask = self.load_dataset_folder()

        # set transforms
        self.transform_x = T.Compose([T.Resize((resize, resize), Image.ANTIALIAS),
                                      # T.CenterCrop(cropsize),
                                      T.ToTensor(),
                                      T.Normalize(mean=[0.485, 0.456, 0.406],
                                                  std=[0.229, 0.224, 0.225])])
        self.transform_mask = T.Compose([T.Resize((resize, resize), Image.NEAREST),
                                         # T.CenterCrop(cropsize),
                                         T.ToTensor()])

    def __getitem__(self, idx):
        x, y, mask = self.x[idx], self.y[idx], self.mask[idx]

        x = Image.open(x).convert('RGB')
        x = self.transform_x(x)

        if y == 0:
            mask = torch.zeros([1, self.cropsize, self.cropsize])
        else:
            mask = Image.open(mask)
            mask = self.transform_mask(mask)

        return x, y, mask

    def __len__(self):
        return len(self.x)

    def load_dataset_folder(self):
        phase = 'train' if self.is_train else 'test'
        x, y, mask = [], [], []

        img_dir = os.path.join(self.dataset_path, self.class_name, phase)
        gt_dir = os.path.join(self.dataset_path, self.class_name, 'ground_truth')

        img_types = sorted(os.listdir(img_dir))
        for img_type in img_types:
            # load images
            img_type_dir = os.path.join(img_dir, img_type)
            if not os.path.isdir(img_type_dir):
                continue
            img_fpath_list = sorted([os.path.join(img_type_dir, f)
                                     for f in os.listdir(img_type_dir)
                                     if f.endswith('.png')])
            x.extend(img_fpath_list)

            # load gt labels
            if img_type == 'good':
                y.extend([0] * len(img_fpath_list))
                mask.extend([None] * len(img_fpath_list))
            else:
                y.extend([1] * len(img_fpath_list))
                gt_type_dir = os.path.join(gt_dir, img_type)
                img_fname_list = [os.path.splitext(os.path.basename(f))[0] for f in img_fpath_list]
                gt_fpath_list = [os.path.join(gt_type_dir, img_fname + '_mask.png')
                                 for img_fname in img_fname_list]
                mask.extend(gt_fpath_list)

        assert len(x) == len(y), 'number of x and y should be same'

        return list(x), list(y), list(mask)


def create_seed(filters, seed=0, use_cuda=True):
    random.seed(seed)
    torch.manual_seed(seed)
    if use_cuda:
        torch.cuda.manual_seed_all(seed)


def embedding_concat(x, y):
    B, C1, H1, W1 = x.size()
    _, C2, H2, W2 = y.size()

    s = int(H1 / H2)
    x = F.unfold(x, kernel_size=s, dilation=1, stride=s)
    x = x.view(B, C1, -1, H2, W2)
    z = torch.zeros(B, C1 + C2, x.size(2), H2, W2)
    for i in range(x.size(2)):
        z[:, :, i, :, :] = torch.cat((x[:, :, i, :, :], y), 1)

    z = z.view(B, -1, H2 * W2)
    z = F.fold(z, kernel_size=s, output_size=(H1, W1), stride=s)

    return z


def show_feat_list(model, size=(1, 3, 224, 224)):
    sample_inputs = torch.zeros(size)
    feat_list = model.extract_entire_features(sample_inputs)


def denormalize(img):
    mean = torch.tensor([0.485, 0.456, 0.406])
    std = torch.tensor([0.229, 0.224, 0.225])
    return img.mul_(std).add_(mean)


def calc_covinv(embedding_vectors, H, W, C):
    for i in range(H * W):
        yield np.linalg.inv(np.cov(embedding_vectors[:, :, i].numpy(), rowvar=False) + 0.01 * np.identity(C))


def train(data_path, save_path, batch_size=128, resize=128, arch='b4'):
    import argparse
    parser = argparse.ArgumentParser('PaDiM Parameters')
    parser.add_argument('-d', '--data_path', type=str, default=data_path, help='mvtec data location')
    parser.add_argument('-s', '--save_path', type=str, default=save_path, help='inference model & data location')
    parser.add_argument('-a', '--arch', type=str, choices=['b0', 'b1', 'b4', 'b7'], default=arch)
    parser.add_argument('-b', '--batch_size', type=int, default=batch_size)
    parser.add_argument('--training', default=True)
    parser.add_argument('--seed', type=int, default=1024)
    parser.add_argument('--resize', type=int, default=resize)
    parser.add_argument('--model_print', action='store_true')
    parser.add_argument('--img_print', action='store_true')
    args = parser.parse_args()

    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    name = 'efficientnet-{}'.format(args.arch)
    eff_model = EfficientNetModified.from_pretrained(name)

    # make directory for saving data
    os.makedirs(os.path.join(args.save_path, 'model_pkl_%s' % name), exist_ok=True)

    # capture ROCAUC score

    if args.arch == 'b0':
        block_num = torch.tensor([3, 5, 11])  # b0
        filters = (24 + 40 + 112)  # 176
    elif args.arch == 'b1':
        # block_num = torch.tensor([3, 6, 9]) # b1 first, 24 + 40 + 80
        # block_num = torch.tensor([4, 7, 13]) # b1 medium 24 + 40 + 112
        block_num = torch.tensor([5, 8, 16])  # b1 last 24 + 40 + 112
        filters = (24 + 40 + 112)  # 176
    elif args.arch == 'b4':
        # block_num = torch.tensor([3, 7, 11]) # b4 (32 + 56 + 112)
        block_num = torch.tensor([3, 7, 17])  # b4 (32 + 56 + 160)
        # block_num = torch.tensor([5, 9, 13]) # (32 + 56 + 112)
        # block_num = torch.tensor([5, 9, 20]) # b4 (32 + 56 + 160)
        # block_num = torch.tensor([6, 10, 22]) # b4 (32 + 56 + 160)
        filters = (32 + 56 + 160)  # 248
    elif args.arch == 'b7':
        block_num = torch.tensor([11, 18, 38])  # b7 (48 + 80 + 224) # last
        # block_num = torch.tensor([5, 12, 29]) # b7 (48 + 80 + 224) # first
        # block_num = torch.tensor([8, 15, 33]) # medium
        filters = (48 + 80 + 224)  # 352

    '''
    The number of filters is so small that I want to take the entire filter, not randomly. 
    So I'm going to delete the random code this time.
    '''
    create_seed(filters)

    # model attach to device
    eff_model.to(device)

    print('training: ', args.training)

    class_name = 'rfid'
    train_dataset = MVTecDataset(args.data_path, class_name=class_name, is_train=True, resize=args.resize)
    train_dataloader = DataLoader(train_dataset, batch_size=args.batch_size, pin_memory=True)
    train_outputs = OrderedDict([('layer1', []), ('layer2', []), ('layer3', [])])

    # model_path
    train_feature_filepath = os.path.join(args.save_path, 'model_pkl_%s' % name, 'train_%s.pkl' % class_name)

    if os.path.exists(train_feature_filepath):
        os.remove(train_feature_filepath)

    eff_model.eval()
    for (x, _, _) in tqdm(train_dataloader, 'feature extraction | train | %s |' % (class_name)):
        with torch.no_grad():
            feats = eff_model.extract_features(x.to(device), block_num.to(device))

        # If you want to see the shape of the feature...
        # for i, feat in enumerate(feats):
        #     print("layer {} feature's shape: {}".format(i, feat.shape))

        for k, v in zip(train_outputs.keys(), feats):
            train_outputs[k].append(v.cpu().detach())

    for k, v in train_outputs.items():
        train_outputs[k] = torch.cat(v, 0)

    embedding_vectors = train_outputs['layer1']
    for layer_name in ['layer2', 'layer3']:
        embedding_vectors = embedding_concat(embedding_vectors, train_outputs[layer_name])

    B, C, H, W = embedding_vectors.size()
    print("embedding vector's size: {}, {}, {}, {}".format(B, C, H, W))
    embedding_vectors = embedding_vectors.view(B, C, H * W)
    mean = torch.mean(embedding_vectors, dim=0).numpy()
    cov_inv = torch.zeros(C, C, H * W).numpy()
    I = np.identity(C)

    # It's done with generator, but it doesn't matter what you do because there's not much memory difference.
    # cc = calc_covinv(embedding_vectors, H, W, C)
    # for i, value in enumerate(cc):
    #     cov_inv[:, :, i] = value

    for i in trange(H * W, desc='cal cov inv'):
        cov_inv[:, :, i] = np.linalg.inv(np.cov(embedding_vectors[:, :, i].numpy(), rowvar=False) + 0.01 * I)
    # save learned distribution
    train_outputs = [mean.transpose(1, 0), cov_inv.transpose(2, 0, 1)]

    with open(train_feature_filepath, 'wb') as f:
        pickle.dump(train_outputs, f, protocol=pickle.HIGHEST_PROTOCOL)
