import numpy as np

# DO NOT MODIFY EVALUATION CODE
def report_accuracy(confidences, label_vector):
    confidences = confidences.ravel()
    label_vector = label_vector.ravel()
    assert confidences.size==label_vector.size, "Size of confidences and label_vector should be the same"
    # compute accuracy
    accuracy = ((label_vector*confidences)>0).sum() / float(confidences.size)
    print("  accuracy: {:.3f}".format(accuracy))

    # compute true positive rate (TP)
    true_positives = np.logical_and((confidences>=0), (label_vector>=0))
    tpr = true_positives.sum() / float(true_positives.size)
    print("  true positive rate: {:.3f}".format(tpr))

    # compute false positive rate (FP)
    false_positives = np.logical_and((confidences>=0), (label_vector<0))
    fpr = false_positives.sum() / float(false_positives.size)
    print("  false positive rate: {:.3f}".format(fpr))
    
    # compute true negative rate (TN)
    true_negatives = np.logical_and((confidences<0), (label_vector<0))
    tnr = true_negatives.sum() / float(true_negatives.size)
    print("  true negative rate: {:.3f}".format(tnr))

    # compute false negative rate (FN)
    false_negatives = np.logical_and((confidences<0), (label_vector>=0))
    fnr = false_negatives.sum() / float(false_negatives.size)
    print("  false negative rate: {:.3f}".format(fnr))

    return tpr, fpr, tnr, fnr
