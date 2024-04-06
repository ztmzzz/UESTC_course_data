# Sliding window face detection with linear SVM
import numpy as np
import os
import pdb
from cyvlfeat.hog import hog
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from skimage import draw, exposure

from get_positive_features import get_positive_features
from get_random_negative_features import get_random_negative_features
from svm_classify import svm_classify
from report_accuracy import report_accuracy
from run_detector import run_detector
from evaluate_detections import evaluate_detections
from visualize_detections_by_image import visualize_detections_by_image

# root directory of all data
data_path = '../data'
# directory of positive training examples. 36x36 head crops
train_path_pos = os.path.join(data_path, 'caltech_faces/Caltech_CropFaces')
# print(train_path_pos)
# we can mine random or hard negatives from here
non_face_scn_path = os.path.join(data_path, 'train_non_face_scenes')
# CMU+MIT test scenes
test_scn_path = os.path.join(data_path, 'test_scenes/test_jpg')
# the ground truth face locations in the test set
label_path = os.path.join(data_path, 'test_scenes/ground_truth_bboxes.txt')
# directory for saving figure
fig_path = 'visualizations'
if not os.path.exists(fig_path):
    os.mkdir(fig_path)

# The faces are 36x36 pixels, which works fine as a template size. You could
# add other fields to this struct if you want to modify HoG default
# parameters such as the number of orientations, but that does not help
# performance in our limited test.
feature_params = {'template_size': 36,
                  'hog_cell_size': 6}

## Step 1. Load positive training crops and random negative examples
# YOU CODE 'get_positive_features' and 'get_random_negative_features'
features_pos = get_positive_features(train_path_pos, feature_params)
# higher will work strictly better, but your should start with 10000
num_negative_examples = 10000
features_neg, neg_examples = get_random_negative_features(non_face_scn_path, feature_params, num_negative_examples)

## Step 2. Train classifier
features_total = np.concatenate([features_pos, features_neg], axis=0)
labels = np.concatenate([np.ones((features_pos.shape[0], 1)), -np.ones((features_neg.shape[0], 1))],
                        axis=0)

model = svm_classify(features_total, labels)

## Step 3. Examine learned classifier
# You don't need to modify anything in this section. The section first
# evaluates _training_ error, which isn't ultimately what we care about,
# but it is a good sanity check. Your training error should be very low.
print('Initial classifier performance on train data:')
confidences = model.decision_function(features_total)
label_vector = labels
tp_rate, fp_rate, tn_rate, fn_rate = report_accuracy(confidences, label_vector)

# Visualize how well separated the positive and negative examples are at
# training time. Sometimes this can idenfity odd biases in your training
# data, especially if you're trying hard negative mining. This
# visualization won't be very meaningful with the placeholder starter code.
non_face_confs = confidences[label_vector.ravel() < 0]
face_confs = confidences[label_vector.ravel() > 0]
fig2 = plt.figure(2)
# plt.hold(True)
plt.plot(np.arange(non_face_confs.size), np.sort(non_face_confs), color='g')
plt.plot(np.arange(face_confs.size), np.sort(face_confs), color='r')
plt.plot([0, non_face_confs.size], [0, 0], color='b')
# plt.hold(False)
plt.show()
## Step 4. (optional) Mine hard negatives
# Mining hard negatives is extra credit. You can get very good performance
# by using random negatives, so hard negative mining is somewhat
# unnecessary for face detection. If you implement hard negative mining,
# you probably want to modify 'run_detector', run the detector on the
# images in 'non_face_scn_path', and keep all of the features above some
# confidence level.

# hard negative mining

# hard positive mining

# training with hard examples

# estimate again after hard example mining

# visualize

## Step 5. Run detector on test set.
# YOU CODE 'run_detector'. Make sure the outputs are properly structured!
# They will be interpreted in Step 6 to evaluate and visualize your
# results. See run_detector.m for more details.
bboxes, confidences, image_ids = run_detector(test_scn_path, model, feature_params)

# run_detector will have (at least) two parameters which can heavily
# influence performance -- how much to rescale each step of your multiscale
# detector, and the threshold for a detection. If your recall rate is low
# and your detector still has high precision at its highest recall point,
# you can improve your average precision by reducing the threshold for a
# positive detection.

## Step 6. Evaluate and Visualize detections
# These functions require ground truth annotations, and thus can only be
# run on the CMU+MIT face test set. Use visualize_detectoins_by_image_no_gt
# for testing on extra images (it is commented out below).

# Don't modify anything in 'evaluate_detections'
gt_ids, gt_bboxes, gt_isclaimed, tp, fp, duplicate_detections = \
    evaluate_detections(bboxes, confidences, image_ids, label_path, fig_path)

visualize_detections_by_image(bboxes, confidences, image_ids, tp, fp, test_scn_path, label_path, fig_path)

# performance to aim for
# random (stater code) 0.001 AP
# single scale ~ 0.2 to 0.4 AP
# multiscale, 6 pixel step ~ 0.83 AP
# multiscale, 4 pixel step ~ 0.89 AP
# multiscale, 3 pixel step ~ 0.92 AP
