import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage import filters, feature, img_as_int
from skimage.measure import regionprops
from sklearn.metrics.pairwise import euclidean_distances
from skimage.transform import rescale
from skimage.color import rgb2gray
from proj2.code.utils import load_data


def get_interest_points(image, feature_width):
    '''
    Returns a set of interest points for the input image

    (Please note that we recommend implementing this function last and using cheat_interest_points()
    to test your implementation of get_features() and match_features())

    Implement the Harris corner detector (See Szeliski 4.1.1) to start with.
    You do not need to worry about scale invariance or keypoint orientation estimation
    for your Harris corner detector.
    You can create additional interest point detector functions (e.g. MSER)
    for extra credit.

    If you're finding spurious (false/fake) interest point detections near the boundaries,
    it is safe to simply suppress the gradients / corners near the edges of
    the image.

    Useful functions: A working solution does not require the use of all of these
    functions, but depending on your implementation, you may find some useful. Please
    reference the documentation for each function/library and feel free to come to hours
    or post on Piazza with any questions

        - skimage.feature.peak_local_max
        - skimage.measure.regionprops


    :params:
    :image: a grayscale or color image (your choice depending on your implementation)
    :feature_width:

    :returns:
    :xs: an np array of the x coordinates of the interest points in the image
    :ys: an np array of the y coordinates of the interest points in the image

    :optional returns (may be useful for extra credit portions):
    :confidences: an np array indicating the confidence (strength) of each interest point
    :scale: an np array indicating the scale of each interest point
    :orientation: an np array indicating the orientation of each interest point

    '''

    # 计算梯度
    dy, dx = np.gradient(image)
    # 高斯滤波用于平滑图像
    Ixx = filters.gaussian(dx ** 2, sigma=1)
    Iyy = filters.gaussian(dy ** 2, sigma=1)
    Ixy = filters.gaussian(dx * dy, sigma=1)
    k = 0.1

    # determinant(window = 1x1)
    # 像素值变化量矩阵的行列式
    detA = Ixx * Iyy - Ixy ** 2
    # trace
    # 矩阵的迹
    traceA = Ixx + Iyy
    # 角点响应函数
    harris_response = detA - k * (traceA ** 2)
    # corners = feature.corner_peaks(feature.corner_harris(image), min_distance=20, threshold_rel=0.02)
    # 获取角点,min_distance=两点间最小距离,threshold_rel=角点最小强度
    corners = feature.corner_peaks(harris_response, min_distance=10, threshold_rel=0.02)
    # These are placeholders - replace with the coordinates of your interest points!
    # xs = np.asarray([0])
    # ys = np.asarray([0])
    xs = np.asarray(corners[:, 1])
    ys = np.asarray(corners[:, 0])

    return xs, ys


def get_features(image, x, y, feature_width):
    '''
    Returns a set of feature descriptors for a given set of interest points.

    (Please note that we reccomend implementing this function after you have implemented
    match_features)

    To start with, you might want to simply use normalized patches as your
    local feature. This is very simple to code and works OK. However, to get
    full credit you will need to implement the more effective SIFT-like descriptor
    (See Szeliski 4.1.2 or the original publications at
    http://www.cs.ubc.ca/~lowe/keypoints/)

    Your implementation does not need to exactly match the SIFT reference.
    Here are the key properties your (baseline) descriptor should have:
    (1) a 4x4 grid of cells, each descriptor_window_image_width/4.
    (2) each cell should have a histogram of the local distribution of
        gradients in 8 orientations. Appending these histograms together will
        give you 4x4 x 8 = 128 dimensions.
    (3) Each feature should be normalized to unit length

    You do not need to perform the interpolation in which each gradient
    measurement contributes to multiple orientation bins in multiple cells
    As described in Szeliski, a single gradient measurement creates a
    weighted contribution to the 4 nearest cells and the 2 nearest
    orientation bins within each cell, for 8 total contributions. This type
    of interpolation probably will help, though.

    You do not have to explicitly compute the gradient orientation at each
    pixel (although you are free to do so). You can instead filter with
    oriented filters (e.g. a filter that responds to edges with a specific
    orientation). All of your SIFT-like feature can be constructed entirely
    from filtering fairly quickly in this way.

    You do not need to do the normalize -> threshold -> normalize again
    operation as detailed in Szeliski and the SIFT paper. It can help, though.

    Another simple trick which can help is to raise each element of the final
    feature vector to some power that is less than one.

    Useful functions: A working solution does not require the use of all of these
    functions, but depending on your implementation, you may find some useful. Please
    reference the documentation for each function/library and feel free to come to hours
    or post on Piazza with any questions

        - skimage.filters (library)


    :params:
    :image: a grayscale or color image (your choice depending on your implementation)
    :x: np array of x coordinates of interest points
    :y: np array of y coordinates of interest points
    :feature_width: in pixels, is the local feature width. You can assume
                    that feature_width will be a multiple of 4 (i.e. every cell of your
                    local SIFT-like feature will have an integer width and height).
    If you want to detect and describe features at multiple scales or
    particular orientations you can add input arguments.

    :returns:
    :features: np array of computed features. It should be of size
            [len(x) * feature dimensionality] (for standard SIFT feature
            dimensionality is 128)

    '''

    xs = x.astype(int)
    ys = y.astype(int)

    # padding the image
    pad_w = feature_width // 2
    # 图像边缘填充
    padded_image = np.pad(image, [pad_w, pad_w], 'symmetric')
    # This is a placeholder - replace this with your features!
    features = np.zeros(shape=(len(xs), 128))

    # using the sobel to generate the magnitude and angle of every pixel just like imgradient in matlab
    # 计算梯度
    sobelx = cv2.Sobel(padded_image, cv2.CV_64F, 1, 0)
    sobely = cv2.Sobel(padded_image, cv2.CV_64F, 0, 1)
    # Find magnitude and angle of every pixel
    # 计算梯度的方向
    magnitude = np.sqrt(sobelx ** 2.0 + sobely ** 2.0)
    angle = np.arctan2(sobely, sobelx) * (180 / np.pi)
    # Convert gradient direction into 8 bins
    # 将方向划分为8种
    Gdir = np.minimum(np.floor((angle + 180) / 45), 7)

    cell_size = feature_width // 4
    for i in range(len(xs)):
        count = 0
        # find the 4x4 cell
        for cellx_start in range(xs[i], xs[i] + 4 * cell_size, cell_size):
            cellx_end = cellx_start + cell_size
            for celly_start in range(ys[i], ys[i] + 4 * cell_size, cell_size):
                celly_end = celly_start + cell_size
                cell_magnitude = magnitude[celly_start:celly_end, cellx_start:cellx_end].flatten()
                cell_Gdir = Gdir[celly_start:celly_end, cellx_start:cellx_end].flatten()
                for j in range(len(cell_magnitude)):
                    idx = int(count * 8 + cell_Gdir[j])
                    features[i, idx] += cell_magnitude[j]
                count += 1
        features[i, :] = features[i, :] / np.linalg.norm(features[i, :])
    return features


def match_features(im1_features, im2_features):
    '''
    Implements the Nearest Neighbor Distance Ratio Test to assign matches between interest points
    in two images.

    Please implement the "Nearest Neighbor Distance Ratio (NNDR) Test" ,
    Equation 4.18 in Section 4.1.3 of Szeliski.

    For extra credit you can implement spatial verification of matches.

    Please assign a confidence, else the evaluation function will not work. Remember that
    the NNDR test will return a number close to 1 for feature points with similar distances.
    Think about how confidence relates to NNDR.

    This function does not need to be symmetric (e.g., it can produce
    different numbers of matches depending on the order of the arguments).

    A match is between a feature in im1_features and a feature in im2_features. We can
    represent this match as a the index of the feature in im1_features and the index
    of the feature in im2_features

    Useful functions: A working solution does not require the use of all of these
    functions, but depending on your implementation, you may find some useful. Please
    reference the documentation for each function/library and feel free to come to hours
    or post on Piazza with any questions

        - zip (python built in function)

    :params:
    :im1_features: an np array of features returned from get_features() for interest points in image1
    :im2_features: an np array of features returned from get_features() for interest points in image2

    :returns:
    :matches: an np array of dimension k x 2 where k is the number of matches. The first
            column is an index into im1_features and the second column is an index into im2_features
    :confidences: an np array with a real valued confidence for each match
    '''

    # These are placeholders - replace with your matches and confidences!
    threshold = 1
    # generate the distance matrix
    # 计算向量距离
    d_matrix = euclidean_distances(im1_features, im2_features)
    sorted_matrix = np.sort(d_matrix)
    sorted_idx = np.argsort(d_matrix)
    # 取两个离当前点最近的点,计算两个点的比例,如果小于阀值就接受.因为对于错误匹配,相似的距离有大量其他的错误匹配,比值较高
    inverse_confidences = sorted_matrix[:, 0] / sorted_matrix[:, 1]
    confidences = 1 / inverse_confidences[inverse_confidences < threshold]

    matches = np.zeros(shape=(len(confidences), 2))
    matches[:, 0] = np.where(inverse_confidences < threshold)[0]
    matches[:, 1] = sorted_idx[inverse_confidences < threshold, 0]

    idn = np.argsort(confidences)[::-1]
    confidences = confidences[idn]
    matches = matches[idn, :]
    return matches, confidences
