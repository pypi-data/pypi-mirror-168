import pickle
from collections import OrderedDict
import torch.nn.functional as F
import numpy as np
from efficientnet_pytorch import EfficientNet
import os
from PIL import Image
import torch
from torchvision import transforms as T


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


class ADet:

    def __init__(self, arch='b0', save_path='anomaly_detection/results', class_name='rfid', resize=128, device='cpu'):
        name = 'efficientnet-{}'.format(arch)
        self.device = device
        self.model = EfficientNetModified.from_pretrained(name).to(device).eval()

        if arch == 'b0':
            block_num = torch.tensor([3, 5, 11])  # b0
            filters = (24 + 40 + 112)  # 176
        elif arch == 'b1':
            # block_num = torch.tensor([3, 6, 9]) # b1 first, 24 + 40 + 80
            # block_num = torch.tensor([4, 7, 13]) # b1 medium 24 + 40 + 112
            block_num = torch.tensor([5, 8, 16])  # b1 last 24 + 40 + 112
            filters = (24 + 40 + 112)  # 176
        elif arch == 'b4':
            # block_num = torch.tensor([3, 7, 11]) # b4 (32 + 56 + 112)
            block_num = torch.tensor([3, 7, 17])  # b4 (32 + 56 + 160)
            # block_num = torch.tensor([5, 9, 13]) # (32 + 56 + 112)
            # block_num = torch.tensor([5, 9, 20]) # b4 (32 + 56 + 160)
            # block_num = torch.tensor([6, 10, 22]) # b4 (32 + 56 + 160)
            filters = (32 + 56 + 160)  # 248
        elif arch == 'b7':
            block_num = torch.tensor([11, 18, 38])  # b7 (48 + 80 + 224) # last
            # block_num = torch.tensor([5, 12, 29]) # b7 (48 + 80 + 224) # first
            # block_num = torch.tensor([8, 15, 33]) # medium
            filters = (48 + 80 + 224)  # 352

        self.block_num = block_num

        train_feature_filepath = os.path.join(save_path, 'model_pkl_%s' % name, 'train_%s.pkl' % class_name)

        if not os.path.exists(train_feature_filepath):
            self.train_outputs = None
            print('train set feature file not exists: {}'.format(train_feature_filepath))
        else:
            print('load train set feat file from %s' % train_feature_filepath)
            with open(train_feature_filepath, 'rb') as f:
                train_outputs = pickle.load(f)
                self.mean = torch.Tensor(train_outputs[0]).to(device)
                self.cov_inv = torch.Tensor(train_outputs[1]).to(device)

        # save_dir = save_path + '/' + f'pictures_efficientnet-{arch}'
        self.transform_x = T.Compose([T.Resize((resize, resize), Image.ANTIALIAS),
                                      T.ToTensor(),
                                      T.Normalize(mean=[0.485, 0.456, 0.406],
                                                  std=[0.229, 0.224, 0.225])])

    def __call__(self, x_orig):
        test_outputs = OrderedDict([('layer1', []), ('layer2', []), ('layer3', [])])

        x = torch.stack([self.transform_x(Image.fromarray(xi).convert('RGB')) for xi in x_orig], dim=0)
        with torch.no_grad():
            feats = self.model.extract_features(x.to(self.device), self.block_num.to(self.device))
        for k, v in zip(test_outputs.keys(), feats):
            test_outputs[k] = v.cpu().detach()
        embedding_vectors = test_outputs['layer1']
        for layer_name in ['layer2', 'layer3']:
            embedding_vectors = embedding_concat(embedding_vectors, test_outputs[layer_name])
        B, C, H, W = embedding_vectors.size()
        embedding_vectors = embedding_vectors.view(B, C, H * W).permute(0, 2, 1).to(self.device)

        #  replacing likehood with squared mahalanobis distance from https://github.com/Pangoraw/PaDiM
        score_maps = []
        for x_id, (xi, embedding_vector) in enumerate(zip(x_orig, embedding_vectors)):
            delta = embedding_vector - self.mean
            temp = torch.matmul(self.cov_inv, delta.unsqueeze(-1))
            dist_list = torch.matmul(delta.unsqueeze(1), temp).squeeze(1)
            dist_list = dist_list.transpose(1, 0).view(1, H, W)
            score_map = F.interpolate(dist_list.unsqueeze(1), size=x.size(2), mode='bilinear',
                                      align_corners=False).squeeze().cpu().numpy()
            score_maps.append(score_map)
        score_maps = np.array(np.asarray(score_maps) > 1e3) * 255
        score_maps = np.asarray(score_maps, dtype=np.uint8)
        score_maps = list(score_maps)

        return score_maps
