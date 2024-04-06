import numpy as np

# import ipdb #DEBUG

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
