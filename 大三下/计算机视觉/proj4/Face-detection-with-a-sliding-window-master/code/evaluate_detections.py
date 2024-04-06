import numpy as np
from time import time
from matplotlib import pyplot as plt
from VOCap import VOCap

# DO NOT MODIFY EVALUATION CODE!!!!
def evaluate_detections(bboxes, confidences, image_ids, label_path, fig_path, draw=True):
    """
    FUNC: This function will calculate the result by Pascal VOC Evaluation
    ARG:
        - bboxes: (N, 4) ndarray; N is the number of non-overlapping detections, bboxes[i,:] is
                        [x_min, y_min, x_max, y_max] for detection i.
        - confidences: (N, 1) ndarray; confidences[i] is the real valued confidence
                        of detection i.
        - image_ids: a list;  image_ids[i] is the image file name for detection i.
        - label_path: a string; the path of the file with ground truth bounding boxes for the test set
    """
    # This code is modified from the 2010 Pascal VOC toolkit.
    # http: // pascallin.ecs.soton.ac.uk / challenges / VOC / voc2010 / index.html  # devkit


    f = open(label_path, 'r')
    lines = f.readlines()
    gt_ids = []
    gt_bboxes = np.zeros([len(lines), 4])
    for i in range(len(lines)):
        gt_info = lines[i].rstrip('\r\n').split()
        gt_ids.append(gt_info[0])
        gt_bboxes[i, :] = [float(x) for x in gt_info[1:]]
    f.close()

    gt_isclaimed = np.zeros([len(gt_ids), 1])
    npos = len(gt_ids)  # total number of true positives.

    # sort detections by decreasing confidence
    si = np.squeeze(np.argsort(-confidences, axis=0))
    image_ids = image_ids[si]
    bboxes = bboxes[si]

    # assign detections to ground truth objects
    nd = len(confidences)
    tp = np.zeros([nd, 1])
    fp = np.zeros([nd, 1])
    duplicate_detections = np.zeros([nd, 1])

    t = time()
    for d in range(nd):
        # display progress
        if (time() - t) > 1:
            print ('pr: compute: {}/{}\n'.format(d, nd))
            t = time()

        cur_gt_ids = [i for i, gt_id in enumerate(gt_ids) if image_ids[d] == gt_id]

        bb = bboxes[d, :]
        ovmax = -np.inf

        for j in cur_gt_ids:
            bbgt = gt_bboxes[j, :]
            bi = [max(bb[0], bbgt[0]), max(bb[1], bbgt[1]), min(bb[2], bbgt[2]), min(bb[3], bbgt[3])]
            iw = bi[2] - bi[0] + 1
            ih = bi[3] - bi[1] + 1
            if iw > 0 and ih > 0:
                # compute overlap as area of intersection / area of union
                ua = (bb[2] - bb[0] + 1) * (bb[3] - bb[1] + 1) + \
                     (bbgt[2] - bbgt[0] + 1) * (bbgt[3] - bbgt[1] + 1) - iw * ih
                ov = iw * ih / ua
                if ov > ovmax:  # higher overlap than the previous best?
                    ovmax = ov
                    jmax = j

        # assign detection as true positive / don 't care/false positive
        if ovmax >= 0.3:
            if not gt_isclaimed[jmax]:
                tp[d] = 1  # true positive
                gt_isclaimed[jmax] = True
            else:
                fp[d] = 1  # false positive (multiple detection)
                duplicate_detections[d] = 1
        else:
            fp[d] = 1  # false positive

    # compute cumulative precision / recall
    cum_fp = np.cumsum(fp)
    cum_tp = np.cumsum(tp)
    rec = cum_tp / npos
    prec = np.divide(cum_tp, (cum_fp + cum_tp))

    ap = VOCap(rec, prec)

    if draw:
        # plot precision / recall
        fig12 = plt.figure(12)
        line = plt.plot(rec, prec, '-')
        plt.axis([0, 1, 0, 1])
        plt.grid()
        plt.xlabel('recall')
        plt.ylabel('precision')
        plt.title('Average Precision = {:0.2f}'.format(ap))
        plt.setp(line, 'color', 'blue')

        plt.pause(0.1)  # let's ui rendering catch up
        fig12.savefig('{}/average_precision.png'.format(fig_path))

        plt.figure(13)
        plt.plot(cum_fp, rec, '-')
        plt.axis([0, 300, 0, 1])
        plt.grid()
        plt.xlabel('False positives')
        plt.ylabel('Number of correct detections (recall)')
        plt.title('This plot is meant to match Figure 6 in Viola Jones')

    # # Re-sort return variables so that they are in the order of the input bboxes
    reverse_map = np.zeros([nd], dtype=np.int)
    reverse_map[si] = range(nd)
    tp = tp[reverse_map]
    fp = fp[reverse_map]
    duplicate_detections = duplicate_detections[reverse_map]

    return gt_ids, gt_bboxes, gt_isclaimed, tp, fp, duplicate_detections
