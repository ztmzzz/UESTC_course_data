from sklearn import svm
import numpy as np
from sklearn.utils import column_or_1d
from sklearn.svm import LinearSVC
def svm_classify(x, y):
    '''
    FUNC: train SVM classifier with input data x and label y
    ARG:
        - x: input data, HOG features
        - y: label of x, face or non-face
    RET:
        - clf: a SVM classifier using sklearn.svm. (You can use your favorite
               SVM library but there will be some places to be modified in
               later-on prediction code)
    '''
    #########################################
    ##          you code here              ##
    #########################################
    clf = svm.LinearSVC(C=0.01)
    y =np.ravel(y)
    clf.fit(x, y) 
    #########################################
    ##          you code here              ##
    #########################################

    return clf
