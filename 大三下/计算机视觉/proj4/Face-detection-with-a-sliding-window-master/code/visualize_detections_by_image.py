import numpy as np
import os
from skimage.io import imread
from matplotlib import pyplot as plt


def visualize_detections_by_image(bboxes, confidences, image_ids, tp, fp, test_scn_path, label_path, fig_path):
    """
    FUNC: This function will calculate the result by Pascal VOC Evaluation
    ARG:
        - bboxes: (N, 4) ndarray; N is the number of non-overlapping detections, bboxes[i, :] is
                        [x_min, y_min, x_max, y_max] for detection i.
        - confidences: (N, 1) ndarray; confidences[i, :] is the real valued confidence
                        of detection i.
        - image_ids: (N, 1) ndarray;  image_ids[i, :] is the image file name for detection i.
        - label_path: a string; the path of the file with ground truth bounding boxes for the test set
    """

    # This code is modified from the 2010 Pascal VOC toolkit.
    # http: // pascallin.ecs.soton.ac.uk / challenges / VOC / voc2010 / index.html  # devkit
    # This function visualizes all detections in each test image

    f = open(label_path, 'r')
    lines = f.readlines()
    gt_ids = []
    gt_bboxes = np.zeros([len(lines), 4])
    for i in range(len(lines)):
        gt_info = lines[i].rstrip('\r\n').split()
        gt_ids.append(gt_info[0])
        gt_bboxes[i, :] = [float(x) for x in gt_info[1:]]
    f.close()

    gt_file_list = np.unique(gt_ids)
    test_image_list = np.unique(image_ids)

    num_test_images = len(gt_file_list)

    for cur_image_id in test_image_list:
        
        cur_test_image = imread(os.path.join(test_scn_path, cur_image_id))
        cur_test_image = np.tile(np.expand_dims(cur_test_image, 2), [1, 1, 3])
        cur_gt_detections = [ids for ids, gt_id in enumerate(gt_ids) if cur_image_id == gt_id]
        cur_gt_bboxes = gt_bboxes[cur_gt_detections, :]

        cur_detections = [idx for idx, image_id in enumerate(image_ids) if cur_image_id == image_id[0]]
        cur_bboxes = bboxes[cur_detections, :]
        cur_confidences = confidences[cur_detections]
        cur_tp = tp[cur_detections]
        cur_fp = fp[cur_detections]

        fig15 = plt.figure(15)
        plt.imshow(cur_test_image)
        # plt.hold(True)

        num_detections = len(cur_detections)
        x_pos = [0, 2, 2, 0, 0]
        y_pos = [1, 1, 3, 3, 1]

        for j in range(num_detections):
            bb = cur_bboxes[j, :]
            if cur_tp[j]:  # this was a correct detection
                plt.plot(bb[x_pos], bb[y_pos], color='g')
            elif cur_fp[j]:
                plt.plot(bb[x_pos], bb[y_pos], color='r')
            else:
                ValueError('a detection was neither a true positive or a false positive')

        num_gt_bboxes = len(cur_gt_bboxes)

        for j in range(num_gt_bboxes):
            bbgt = cur_gt_bboxes[j, :]
            plt.plot(bbgt[x_pos], bbgt[y_pos], color='y')

        # plt.hold(False)
        plt.axis('image')
        plt.axis('off')
        plt.title('image: "{}" (green=true pos, red=false pos,\nyellow=ground truth), {}/{} found'.format(
            cur_image_id, np.sum(cur_tp, dtype=np.int), len(cur_gt_bboxes), 'interpreter', 'none'))

        # plt.setp(line, 'color', 'blue')

        plt.pause(0.1)  # let's ui rendering catch up
        fig15.savefig('{}/detections_{}'.format(fig_path, cur_image_id))

        #raw_input('press any key to continue with next image\n')
