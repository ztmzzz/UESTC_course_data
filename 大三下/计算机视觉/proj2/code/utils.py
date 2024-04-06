# Local Feature Stencil Code
# Written by James Hays
# Edited by James Tompkin
# Adapted for python by asabel and jdemari1 (2019)

import csv
import sys
import argparse
import numpy as np

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from skimage import io, filters, feature, img_as_float32
from skimage.transform import rescale
from skimage.color import rgb2gray

import visualize
from helpers import cheat_interest_points, evaluate_correspondence

# This script
# (1) Loads and resizes images
# (2) Finds interest points in those images                 (you code this)
# (3) Describes each interest point with a local feature    (you code this)
# (4) Finds matching features                               (you code this)
# (5) Visualizes the matches
# (6) Evaluates the matches based on ground truth correspondences

def load_data(file_name):
    """
    1) Load stuff
    There are numerous other image sets in the supplementary data on the
    project web page. You can simply download images off the Internet, as
    well. However, the evaluation function at the bottom of this script will
    only work for three particular image pairs (unless you add ground truth
    annotations for other image pairs). It is suggested that you only work
    with the two Notre Dame images until you are satisfied with your
    implementation and ready to test on additional images. A single scale
    pipeline works fine for these two images (and will give you full credit
    for this project), but you will need local features at multiple scales to
    handle harder cases.

    If you want to add new images to test, create a new elif of the same format as those
    for notre_dame, mt_rushmore, etc. You do not need to set the eval_file variable unless
    you hand create a ground truth annotations. To run with your new images use
    python main.py -p <your file name>.

    :param file_name: string for which image pair to compute correspondence for

        The first three strings can be used as shortcuts to the
        data files we give you

        1. notre_dame
        2. mt_rushmore
        3. e_gaudi

    :return: a tuple of the format (image1, image2, eval file)
    """

    # Note: these files default to notre dame, unless otherwise specified
    image1_file = "../data/NotreDame/NotreDame1.jpg"
    image2_file = "../data/NotreDame/NotreDame2.jpg"

    eval_file = "../data/NotreDame/NotreDameEval.mat"

    if file_name == "notre_dame":
        pass
    elif file_name == "mt_rushmore":
        image1_file = "../data/MountRushmore/Mount_Rushmore1.jpg"
        image2_file = "../data/MountRushmore/Mount_Rushmore2.jpg"
        eval_file = "../data/MountRushmore/MountRushmoreEval.mat"
    elif file_name == "e_gaudi":
        image1_file = "../data/EpiscopalGaudi/EGaudi_1.jpg"
        image2_file = "../data/EpiscopalGaudi/EGaudi_2.jpg"
        eval_file = "../data/EpiscopalGaudi/EGaudiEval.mat"

    image1 = img_as_float32(io.imread(image1_file))
    image2 = img_as_float32(io.imread(image2_file))

    return image1, image2, eval_file

