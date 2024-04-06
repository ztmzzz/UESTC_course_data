import numpy as np
import os
import random
from cyvlfeat.hog import hog
from skimage.io import imread
from skimage.transform import pyramid_gaussian
from skimage import color
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
import math
# you may implement your own data augmentation functions

def get_random_negative_features(non_face_scn_path, feature_params, num_samples):
    '''
    FUNC: This funciton should return negative training examples (non-faces) from
        any images in 'non_face_scn_path'. Images should be converted to grayscale,
        because the positive training data is only available in grayscale. For best
        performance, you should sample random negative examples at multiple scales.
    ARG:
        - non_face_scn_path: a string; directory contains many images which have no
                             faces in them.
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
        - features_neg: (N,D) ndarray; N is the number of non-faces and D is 
                        the template dimensionality, which would be, 
                        (template_size/hog_cell_size)^2 * 31,
                        if you're using default HoG parameters.
        - neg_examples: TODO
    '''
    #########################################
    ##          you code here              ##
    #########################################
    image_files=[f for f in listdir(non_face_scn_path) if f.endswith('.jpg')]
    num_img=len(image_files)
    # print(num_sample_per_img,num_samples/num_img)
    D=pow(feature_params['template_size']/feature_params['hog_cell_size'],2)*31
    # print(D)
    D=int(D)
    all_images=np.zeros([0, D])
    features_neg=np.zeros((num_samples,D))
    smp_per_img=math.ceil(num_samples/num_img)
    i=1
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
        path=non_face_scn_path+'/'+image_files[i]
        # all_images.append(np.array(imread(path)).astype('float32'))
        img=imread(path,as_gray=True)
        if min(len(img[0])-feature_params['template_size'],len(img)-feature_params['template_size'])<smp_per_img:
            num_sampd=min(len(img[0])-feature_params['template_size'],len(img)-feature_params['template_size'])
        else:
            num_sampd=smp_per_img
        # hogged=hog(all_images[j],feature_params['hog_cell_size'])
        # temp_height,temp_width=len(hogged),len(hogged[0])
        idx_i=np.random.choice(np.arange(len(img)-feature_params['template_size']),num_sampd,replace=False)
        idx_j=np.random.choice(np.arange(len(img[0])-feature_params['template_size']),num_sampd,replace=False)
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
            portion=img[idx_i[x]:idx_i[x]+feature_params['template_size'],idx_j[x]:idx_j[x]+feature_params['template_size']]
            hogged=hog(portion, feature_params['hog_cell_size'])
            port=np.reshape(hogged,(1,-1))
            all_images = np.concatenate([all_images, port], axis=0)
    #########################################
    ##          you code here              ##
    #########################################
    neg_examples=len(features_neg)
    features_neg=all_images[np.random.choice(np.arange(len(all_images)), size=(num_samples), replace=False)]
    return features_neg, neg_examples

