import math
import os

import numpy as np
from skimage import color

from utils import *
import os.path as osp
from glob import glob
from random import shuffle
from sklearn.svm import LinearSVC
from skimage.io import imread
from tqdm import tqdm
from imgaug import augmenters as iaa
import imgaug as ia
from skimage.transform import resize
import numpy as np
import os
import pdb
from cyvlfeat.hog import hog
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from skimage import draw, exposure

def get_positive_features(train_path_pos, feature_params):
    # params for HOG computation
    win_size = feature_params.get('template_size', 36)
    cell_size = feature_params.get('hog_cell_size', 6)

    positive_files = glob(osp.join(train_path_pos, '*.jpg'))

    ###########################################################################
    #                           TODO: YOUR CODE HERE                          #
    ###########################################################################
    image_files = [f for f in os.listdir(train_path_pos) if f.endswith('.jpg')]
    num_img = len(image_files)
    # for k, v in feature_params.items():
    #     print(k,v,feature_params[k])
    D = pow(feature_params['template_size'] / feature_params['hog_cell_size'], 2) * 31
    D = int(D)
    # print(D)
    features_pos = np.zeros((num_img, D))
    for i in range(num_img):
        path = train_path_pos + '/' + image_files[i]
        # print(path)
        img = imread(path, as_gray=True)
        features_pos[i] = np.reshape(hog(img, feature_params['hog_cell_size']), (-1,))
    #########################################
    ##          you code here              ##
    #########################################
    # print(len(features_pos),len(features_pos[0]))
    return features_pos


def get_random_negative_features(non_face_scn_path, feature_params, num_samples):
    # params for HOG computation
    win_size = feature_params.get('template_size', 36)
    cell_size = feature_params.get('hog_cell_size', 6)

    negative_files = glob(osp.join(non_face_scn_path, '*.jpg'))

    ###########################################################################
    #                           TODO: YOUR CODE HERE                          #
    ###########################################################################

    image_files = [f for f in os.listdir(non_face_scn_path) if f.endswith('.jpg')]
    num_img = len(image_files)
    # print(num_sample_per_img,num_samples/num_img)
    D = pow(feature_params['template_size'] / feature_params['hog_cell_size'], 2) * 31
    # print(D)
    D = int(D)
    all_images = np.zeros([0, D])
    features_neg = np.zeros((num_samples, D))
    smp_per_img = math.ceil(num_samples / num_img)
    i = 1
    # for j in range(num_img):
    #     path=non_face_scn_path+'/'+image_files[i]
    #     img=np.array(color.rgb2gray(imread(path))).astype('float32')
    #     height,width=len(img),len(img[0])
    #     # print(height,width,len(img),len(img[0]))
    #     for j in range(num_sample_per_img):
    #         top_left_x=math.floor(random.random()*(width-feat_size))
    #         top_left_y=math.floor(random.random()*(height-feat_size))
    #         index=i*num_sample_per_img+j
    #         print(index,num_img,num_sample_per_img,i,j)
    #         cropped=img[top_left_y:top_left_y+feat_size,top_left_x:top_left_x+feat_size]
    #         features_neg[index]=np.reshape(hog(cropped,feature_params['hog_cell_size']),(1,D))
    # neg_examples=len(features_neg)
    for j in range(num_img):
        path = non_face_scn_path + '/' + image_files[i]
        # all_images.append(np.array(imread(path)).astype('float32'))
        img = imread(path, as_gray=True)
        if min(len(img[0]) - feature_params['template_size'], len(img) - feature_params['template_size']) < smp_per_img:
            num_sampd = min(len(img[0]) - feature_params['template_size'], len(img) - feature_params['template_size'])
        else:
            num_sampd = smp_per_img
        # hogged=hog(all_images[j],feature_params['hog_cell_size'])
        # temp_height,temp_width=len(hogged),len(hogged[0])
        idx_i = np.random.choice(np.arange(len(img) - feature_params['template_size']), num_sampd, replace=False)
        idx_j = np.random.choice(np.arange(len(img[0]) - feature_params['template_size']), num_sampd, replace=False)
        # for y in range(math.floor((temp_height-5)/freq)):
        #     for x in range(math.floor((temp_width-5)/freq)):
        #         xStart=x*freq
        #         yStart=y*freq
        #         xEnd=xStart+6
        #         yEnd=yStart+6
        #         frame=hogged[yStart:yEnd,xStart:xEnd]
        #         features_neg[i]=np.reshape(frame,(1,D))
        #         num_sampd+=1
        #         if i==num_samples:
        #             neg_examples=len(features_neg)
        #             return features_neg, neg_examples
        #         elif num_sampd>=num_samples/smp_per_img:
        #             break
        #     if num_sampd>=num_samples/smp_per_img:
        #         break
        # if num_sampd>=num_samples/smp_per_img:
        #     continue
        for x in range(num_sampd):
            portion = img[idx_i[x]:idx_i[x] + feature_params['template_size'],
                      idx_j[x]:idx_j[x] + feature_params['template_size']]
            hogged = hog(portion, feature_params['hog_cell_size'])
            port = np.reshape(hogged, (1, -1))
            all_images = np.concatenate([all_images, port], axis=0)
    #########################################
    ##          you code here              ##
    #########################################
    neg_examples = len(features_neg)
    features_neg = all_images[np.random.choice(np.arange(len(all_images)), size=(num_samples), replace=False)]
    return features_neg


def train_classifier(features_pos, features_neg, C):
    """
    This function trains a linear SVM classifier on the positive and negative
    features obtained from the previous steps. We fit a model to the features
    and return the svm object.

    Args:
    -   features_pos: N X D array. This contains an array of positive features
            extracted from get_positive_feats().
    -   features_neg: M X D array. This contains an array of negative features
            extracted from get_negative_feats().

    Returns:
    -   svm: LinearSVC object. This returns a SVM classifier object trained
            on the positive and negative features.
    """
    ###########################################################################
    #                           TODO: YOUR CODE HERE                          #
    ###########################################################################
    features_total = np.concatenate([features_pos, features_neg])
    labels = np.concatenate([np.ones((features_pos.shape[0], 1)), -np.ones((features_neg.shape[0], 1))])
    svm = LinearSVC(C=C)
    svm.fit(features_total, labels)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return svm


def mine_hard_negs(non_face_scn_path, svm, feature_params):
    """
    This function is pretty similar to get_random_negative_features(). The only
    difference is that instead of returning all the extracted features, you only
    return the features with false-positive prediction.

    Useful functions:
    -   skimage.feature.hog(im, pixels_per_cell = (*, *)): computes HoG features
        eg:
                skimage.feature.hog(im, pixels_per_cell=(cell_size, cell_size),
                         cells_per_block=(n_cell, n_cell),
                         orientations=31)

    Args:
    -   non_face_scn_path: string. This directory contains many images which
            have no faces in them.
    -   feature_params: dictionary of HoG feature computation parameters. See
            the documentation for get_positive_features() for more information.
    -   svm: LinearSVC object

    Returns:
    -   N x D matrix where N is the number of non-faces which are
            false-positive and D is the feature dimensionality.
    """

    # params for HOG computation
    win_size = feature_params.get('template_size', 36)
    cell_size = feature_params.get('hog_cell_size', 6)

    negative_files = glob(osp.join(non_face_scn_path, '*.jpg'))

    ###########################################################################
    #                           TODO: YOUR CODE HERE                          #
    ###########################################################################

    feats = []
    res = []
    for i in range(len(negative_files)):
        im = imread(negative_files[i])
        im = color.rgb2gray(im)
        feats.append(hog(im, pixels_per_cell=(cell_size, cell_size),
                         cells_per_block=(win_size // cell_size, win_size // cell_size),
                         orientations=31))

        pred = svm.predict(feats)
        if pred == 1:
            res.append(feats[i])

    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return res


def run_detector(test_scn_path, model, feature_params):
    test_images = os.listdir(test_scn_path)
    # print(test_images)
    # img_name=[f for f in test_images if f.endswith('.jpg')]
    # print(test_scn_path,img_name)
    # initialize these as empty and incrementally expand them.
    bboxes = np.zeros([0, 4])
    confidences = np.zeros([0, 1])
    image_ids = np.zeros([0, 1])

    cell_size = feature_params['hog_cell_size']
    cell_num = int(feature_params['template_size'] / feature_params['hog_cell_size'])  # cell number of each template

    for i in range(len(test_images)):

        #########################################
        ##          you code here              ##
        #########################################
        path = test_scn_path + '/' + test_images[i]
        # img=np.array(imread(path)).astype('float32')
        # dimension=len(img.shape)
        # print(dimension)
        # if dimension>2:
        #     img=color.rbg2gray(img)
        img = imread(path, as_gray=True)
        mindim = min(len(img), len(img[0]))
        count = 1
        cur_bboxes = np.zeros([0, 4])
        cur_image_ids = np.zeros([0, 1])
        cur_confidences = np.zeros([0, 1])
        while count * mindim > feature_params['template_size']:
            frame = resize(img, [int(len(img) * count), int(len(img[0]) * count)])
            # print('82!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            hogged = hog(frame, cell_size)
            # print('84!!!!!!!!!!!')
            D = pow(cell_num, 2) * 31
            D = int(D)
            # print(len(hogged)-cell_size,len(hogged[0])-cell_size)
            for k in range(int(len(hogged) - cell_num + 1)):
                for j in range(int(len(hogged[0]) - cell_num + 1)):

                    curr_y_min = k
                    curr_x_min = j
                    mini_hog = hogged[curr_y_min:curr_y_min + cell_num, curr_x_min:curr_x_min + cell_num]
                    bfeat = np.reshape(mini_hog, (1, -1))
                    # score=model.predict(bfeat)
                    tmp_score = np.reshape(model.decision_function(bfeat), (1, -1))
                    if tmp_score[0, 0] > 0:
                        # hog_bbox=[curr_x_min,curr_y_min,curr_x_min+6,curr_y_min+6]
                        # cur_bboxes.append([h*cellsize for h in hog_bbox])
                        # cur_confidences.append(score)
                        # cur_image_ids.append(test_images[i])
                        # count+=1
                        rowS = int(j * cell_size / count)
                        rowE = int((j + cell_num) * cell_size / count)
                        colS = int(k * cell_size / count)
                        colE = int((k + cell_num) * cell_size / count)
                        cur_bboxes = np.concatenate([cur_bboxes, np.array([[rowS, colS, rowE, colE]])], axis=0)
                        cur_image_ids = np.concatenate([cur_image_ids, [[test_images[i]]]], axis=0)
                        cur_confidences = np.concatenate([cur_confidences, tmp_score], axis=0)
            # if count==1:
            #     continue
            count *= 0.9
        #########################################
        ##          you code here              ##
        #########################################

        # non_max_supr_bbox can actually get somewhat slow with thousands of
        # initial detections. You could pre-filter the detections by confidence,
        # e.g. a detection with confidence -1.1 will probably never be
        # meaningful. You probably _don't_ want to threshold at 0.0, though. You
        # can get higher recall with a lower threshold. You don't need to modify
        # anything in non_max_supr_bbox, but you can.
        is_maximum = non_max_supr_bbox(cur_bboxes, cur_confidences, img.shape)

        cur_bboxes = cur_bboxes[is_maximum[:, 0], :]
        cur_confidences = cur_confidences[is_maximum[:, 0], :]
        cur_image_ids = cur_image_ids[is_maximum[:, 0]]

        bboxes = np.concatenate([bboxes, cur_bboxes], 0)
        confidences = np.concatenate([confidences, cur_confidences], 0)
        image_ids = np.concatenate([image_ids, cur_image_ids], 0)

    return bboxes, confidences, image_ids


def non_max_supr_bbox(bboxes, confidences, img_size, verbose=False):
    """
    FUNC: high confidence detections suppress all overlapping detections
        (including detections at other scales). Detections can partially
        overlap, but the center of one detection can not be within another
        detection.
    ARG:
        - bboxes: (N,4) ndarray; N is the number of non-overlapping detections,
                  and each row is [x_min, y_min, x_max, y_max].
        - confidences: (N,1) ndarray; Confidence of each detection after final
                  cascade node.
        - img_size: (2,) list; [y,x] of the image.
    RET:
        - is_valid_bbox: (N,1) bool ndarray; indicating valid bounding boxes.
    """

    # Truncate bounding boxes to image dimensions
    # print(bboxes,img_size[1])
    x_out_of_bounds = bboxes[:, 2] > img_size[1]  # xmax greater than x dimension
    y_out_of_bounds = bboxes[:, 3] > img_size[0]  # ymax greater than y dimension

    bboxes[x_out_of_bounds, 2] = img_size[1]
    bboxes[y_out_of_bounds, 3] = img_size[0]

    num_detections, _ = confidences.shape

    # higher confidence detections get priority
    ind = np.argsort(-confidences, axis=0).ravel()
    bboxes = bboxes[ind, :]

    # indicator for whether each bbox will be accepted or suppressed
    is_valid_bbox = np.zeros((num_detections, 1), dtype=np.bool)
    for i in range(num_detections):
        cur_bb = bboxes[i, :]
        cur_bb_is_valid = True

        for j in np.where(is_valid_bbox)[0]:
            prev_bb = bboxes[j, :]
            bi = [max(cur_bb[0], prev_bb[0]),
                  max(cur_bb[1], prev_bb[1]),
                  min(cur_bb[2], prev_bb[2]),
                  min(cur_bb[3], prev_bb[3])]
            iw = bi[2] - bi[0] + 1
            ih = bi[3] - bi[1] + 1
            if iw > 0 and ih > 0:
                # compute overlap as area of intersection / area of union
                ua = (cur_bb[2] - cur_bb[0] + 1) * (cur_bb[3] - cur_bb[1] + 1) + \
                     (prev_bb[2] - prev_bb[0] + 1) * (prev_bb[3] - prev_bb[1] + 1) - \
                     iw * ih
                ov = iw * ih / ua
                # if the less confident detection overlaps too much with the previous detection
                if ov > 0.3:
                    cur_bb_is_valid = False

                center_coord = [(cur_bb[0] + cur_bb[2]) / 2, (cur_bb[1] + cur_bb[3]) / 2]
                if (center_coord[0] > prev_bb[0]) and (center_coord[0] < prev_bb[2]) and \
                        (center_coord[1] > prev_bb[1]) and (center_coord[1] < prev_bb[3]):
                    cur_bb_is_valid = False

                if verbose:
                    print('detection {}, bbox: [{},{},{},{}], {} overlap with {} [{},{},{},{}]'.format( \
                        i, cur_bb[0], cur_bb[1], cur_bb[2], cur_bb[3], ov, j, prev_bb[0], prev_bb[1], \
                        prev_bb[2], prev_bb[3]))

        is_valid_bbox[i] = cur_bb_is_valid

    # This statement returns the logical array 'is_valid_bbox' back to the order
    # of the input bboxes and confidences
    reverse_map = np.zeros((num_detections,), dtype=np.int)
    reverse_map[ind] = np.arange(num_detections)
    is_valid_bbox = is_valid_bbox[reverse_map, :]

    return is_valid_bbox
