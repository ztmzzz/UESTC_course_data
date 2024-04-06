import numpy as np
import os
import random
from cyvlfeat.hog import hog
from skimage.io import imread
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
import math
# you can implement your own data augmentation functions

def get_positive_features(train_path_pos, feature_params):
    """
    FUNC: This function should return all positive training examples (faces)
        from 36x36 images in 'train_path_pos'. Each face should be converted
        into a HoG template according to 'feature_params'. For improved performances,
        try mirroring or warping the positive training examples.
    ARG:
        - train_path_pos: a string; directory that contains 36x36 images
                          of faces.
        - feature_params: a dict; with keys,
                          > template_size: int (probably 36); the number of
                            pixels spanned by each train/test template.
                          > hog_cell_size: int (default 6); the number of pixels
                            in each HoG cell.
                          Template size should be evenly divisible by hog_cell_size.
                          Smaller HoG cell sizez tend to work better, but they
                          make things slower because the feature dimenionality
                          increases and more importantly the step size of the
                          classifier decreases at test time.
    RET:
        - features_pos: (N,D) ndarray; N is the number of faces and D is the
                        template dimensionality, which would be,
                        (template_size/hog_cell_size)^2 * 31,
                        if you're using default HoG parameters.
    """
    #########################################
    ##          you code here              ##
    #########################################
    image_files=[f for f in listdir(train_path_pos) if f.endswith('.jpg')]
    num_img=len(image_files)
    # for k, v in feature_params.items():
    #     print(k,v,feature_params[k])
    D=pow(feature_params['template_size']/feature_params['hog_cell_size'],2)*31
    D=int(D)
    # print(D)
    features_pos=np.zeros((num_img,D))
    for i in range(num_img):
        path=train_path_pos+'/'+image_files[i]
        # print(path)
        img=imread(path,as_gray=True)
        features_pos[i]=np.reshape(hog(img,feature_params['hog_cell_size']),(-1,))
    #########################################
    ##          you code here              ##
    #########################################
    # print(len(features_pos),len(features_pos[0]))
    return features_pos 
