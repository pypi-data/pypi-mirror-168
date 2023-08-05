import sys
import os

sys.path.append(os.path.dirname(__file__))
import numpy as np
import cv2
import ctypes

from tempfile import NamedTemporaryFile
import matplotlib.pyplot as plt
import matplotlib
from get_foreground_mask import remove


# from .get_foreground_mask import remove


class LineSegmentDetector():
    def __init__(self,
                 scale=0.8,
                 sigma_scale=0.6,
                 ang_th=22.5,
                 quant=2.0,
                 eps=0.0,
                 density_th=0.7,
                 n_bins=1024,
                 max_grad=255.0
                 ):
        """
        :param scale: Scale the image by Gaussian filter to 'scale'.
        :param sigma_scale: Sigma for Gaussian filter is computed as sigma = sigma_scale/scale.
        :param ang_th: Gradient angle tolerance in degrees.
        :param quant: Bound to the quantization error on the gradient norm.
        :param eps: Detection threshold, -log10(NFA).
        :param density_th: Minimal density of region points in rectangle.
        :param n_bins: Number of bins in pseudo-ordering of gradient modulus.
        :param max_grad: Gradient modulus in the highest bin. The default value corresponds to
                the highest gradient modulus on images with gray levels in [0,255].
        """
        self.lsdlib = self.load_lsd_library()
        if self.lsdlib is None:
            raise ImportError('Cannot load dynamic library. Did you compile LSD?')

        self.scale = scale
        self.sigma_scale = sigma_scale
        self.ang_th = ang_th
        self.quant = quant
        self.eps = eps
        self.density_th = density_th
        self.n_bins = n_bins
        self.max_grad = max_grad

    def load_lsd_library(self, ):
        root_dir = os.path.abspath(os.path.dirname(__file__))

        libnames = ['linux/liblsd.so']
        libdir = os.path.join(os.path.dirname(__file__), 'lib')  # 'lib'

        if sys.platform == 'win32':
            if sys.maxsize > 2 ** 32:
                libnames = ['win32/x64/lsd.dll', 'win32/x64/liblsd.dll']
            else:
                libnames = ['win32/x86/lsd.dll', 'win32/x86/liblsd.dll']

        elif sys.platform == 'darwin':
            libnames = ['darwin/liblsd.dylib']

        while root_dir is not None:
            for libname in libnames:
                try:
                    lsdlib = ctypes.cdll[os.path.join(root_dir, libdir, libname)]
                    return lsdlib
                except Exception as e:
                    pass
            tmp = os.path.dirname(root_dir)
            if tmp == root_dir:
                root_dir = None
            else:
                root_dir = tmp

        # if we didn't find the library so far, try loading without
        # a full path as a last resort
        for libname in libnames:
            try:
                lsdlib = ctypes.cdll[libname]
                return lsdlib
            except Exception as e:
                pass

        return None

    def visualize_line_segment(self, image, lines, mode='overlay'):
        mask = 255 * np.ones(image.shape[:2])
        for i in range(lines.shape[0]):
            pt1 = (int(lines[i, 0]), int(lines[i, 1]))
            pt2 = (int(lines[i, 2]), int(lines[i, 3]))
            width = lines[i, 4]
            cv2.line(mask, pt1, pt2, 0, int(np.ceil(width / 4)))
        if mode == 'overlay':
            image = overlay_heatmap_on_image(image, mask)
        elif mode == 'heatmap':
            image = mask
        else:
            raise NotImplementedError
        return image

    def __call__(self, img):
        """Detects line segments in the provided image.
        Args:
            img (numpy.ndarray): Grayscale image.
        Returns:
            (2D numpy.ndarray): Detected line segments in format:
                [[point1.x, point1.y, point2.x, point2.y, width]]
        """
        assert isinstance(img, np.ndarray)
        assert len(img.shape) < 3
        rows, cols = img.shape
        img = img.reshape(1, rows * cols).tolist()[0]

        lens = len(img)
        img = (ctypes.c_double * lens)(*img)

        with NamedTemporaryFile(prefix='pylsd-', suffix='.ntl.txt', delete=False) as fp:
            fname = fp.name
            fname_bytes = bytes(fp.name) if sys.version_info < (3, 0) else bytes(fp.name, 'utf8')

        self.lsdlib.lsdGet(img, ctypes.c_int(rows), ctypes.c_int(cols), fname_bytes,
                           ctypes.c_double(self.scale), ctypes.c_double(self.sigma_scale),
                           ctypes.c_double(self.ang_th), ctypes.c_double(self.quant), ctypes.c_double(self.eps),
                           ctypes.c_double(self.density_th), ctypes.c_int(self.n_bins), ctypes.c_double(self.max_grad))

        with open(fname, 'r') as fp:
            output = fp.read()
            cnt = output.strip().split(' ')
            count = int(cnt[0])
            dim = int(cnt[1])
            segments = np.array([float(each) for each in cnt[2:]])
            segments = segments.reshape(count, dim)

        os.remove(fname)
        return segments


class BlobDetector():
    def __init__(self, min_circle_area, max_circle_area):
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = min_circle_area
        params.maxArea = max_circle_area
        params.filterByCircularity = True
        self.detector = cv2.SimpleBlobDetector_create(params)

    def __call__(self, image):
        keypoints = self.detector.detect(image)
        return keypoints


def check_is_gray(image):
    return len(image.shape) == 2


def overlay_heatmap_on_image(image, heatmap):
    image = np.asarray(255 * (image / (1e-3 + np.amax(image))), np.uint8)
    heatmap = np.asarray(255 * (heatmap / (1e-3 + np.amax(heatmap))), np.uint8)
    if check_is_gray(image):
        image = image[..., None].repeat(3, axis=-1)


    blur = cv2.GaussianBlur(heatmap, (13, 13), 11)
    heatmap_img = cv2.applyColorMap(255-blur, cv2.COLORMAP_JET)


    super_imposed_img = cv2.addWeighted(heatmap_img, 0.5, image, 0.5, 0)
    return super_imposed_img


def binarize_image(image, upper_limit):
    assert np.amax(image) > 1
    image[image < upper_limit] = 0
    image = 255 - image
    return image


def crop_image(image, row_id, column_id, height, width):
    image = image[row_id:row_id + int(height), column_id:column_id + int(width)]
    return image


def rotate_image_around_center_with_theta(image, center, theta):
    '''
    Rotates OpenCV image around center with angle theta (in deg)
    then crops the image according to width and height.
    '''

    # Uncomment for theta in radians
    # theta *= 180/np.pi

    height, width = image.shape[:2]  # cv2.warpAffine expects shape in (length, height)

    matrix = cv2.getRotationMatrix2D(center=center, angle=theta, scale=1)
    image = cv2.warpAffine(src=image, M=matrix, dsize=(width, height))

    return image


def find_contours(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    morphed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    contours = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours[-2]


def mask_from_contours(ref_img, contours):
    mask = np.zeros(ref_img.shape, np.uint8)
    mask = cv2.drawContours(mask, contours, -1, (1, 1, 1), -1)
    return cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)


def get_foreground_mask(img, margin=0, convex=False):
    foreground = cv2.cvtColor(remove(img), cv2.COLOR_BGR2GRAY)
    mask = np.uint8(foreground > 0)

    if convex:
        cnts = find_contours(mask)
        mask = mask_from_contours(img, cnts)

    if margin > 0:
        mask_resized = mask[margin:-margin, margin:-margin]
        mask_resized = cv2.resize(mask_resized, mask.shape)
        mask = mask_resized

    if mask.shape != img.shape:
        mask = mask[..., None].repeat(3, axis=-1)

    return mask


def concatenate_two_image(img0, img1, axis):
    if len(img0.shape) != len(img1.shape):
        if len(img0.shape) != 3:
            img0 = np.repeat(img0[..., None], repeats=3, axis=-1)
        else:
            img1 = np.repeat(img1[..., None], repeats=3, axis=-1)

    img_cat = np.concatenate([img0, img1], axis=axis)

    return img_cat


def load_image(path, mode='BGR'):
    if mode == 'BGR':
        return cv2.imread(path)
    elif mode == 'grey':
        return cv2.imread(path, 0)
    else:
        raise NotImplementedError

def save_image(path, image):
    assert isinstance(path, str)
    cv2.imwrite(path, image)


def show_image(image, title=None):
    matplotlib.use('TkAgg')
    if isinstance(image, list) or (len(image.shape) == 4):
        fig, axs = plt.subplots(1,len(image))
        for image_i, ax in zip(image, axs):
            ax.imshow(image_i)
            ax.axis('off')
    else:
        plt.imshow(image)
        plt.axis('off')

    if title is not None:
        plt.title(title)
    plt.show()
    plt.close()


def align_img(im1, kp1, im2_w=128, im2=None, kp2=None):
    if check_is_gray(im1):
        im1 = im1[..., None].repeat(3, axis=-1)
    if (im2 is not None) and check_is_gray(im2):
        im2 = im2[..., None].repeat(3, axis=-1)

    kp1 = np.float32(kp1)
    kp2 = np.float32([[0, 0], [1, 0], [1, 1], [0, 1]]) * im2_w if kp2 is None else np.float32(kp2)

    im2 = np.zeros((im2_w, im2_w, 3)) if im2 is None else im2


    # Find homography
    h = cv2.getPerspectiveTransform(kp1, kp2)
    # Use homography
    height, width = im2.shape[:2]
    im1Reg = cv2.warpPerspective(im1, h, (width, height))



    if im2 is not None:
        im1Reg[im1Reg==0] = im2[im1Reg==0]
    return im1Reg
