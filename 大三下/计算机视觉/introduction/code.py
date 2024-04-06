from skimage import img_as_float
import matplotlib.pyplot as plt

plt.rcParams['image.cmap'] = 'gray'
import numpy as np
import skimage
from skimage import filters, io


def imshow_all(*images, titles=None):
    images = [img_as_float(img) for img in images]

    if titles is None:
        titles = [''] * len(images)
    vmin = min(map(np.min, images))
    vmax = max(map(np.max, images))
    ncols = len(images)
    height = 5
    width = height * len(images)
    fig, axes = plt.subplots(nrows=1, ncols=ncols,
                             figsize=(width, height))
    for ax, img, label in zip(axes.ravel(), images, titles):
        ax.imshow(img, vmin=vmin, vmax=vmax)
        ax.set_title(label)


huahua1 = io.imread('./fig/huahua1.jpg')
huahua2 = io.imread('./fig/huahua2.jpg')
fufu1 = io.imread('./fig/fufu1.jpg')
fufu2 = io.imread('./fig/fufu2.jpg')
fufu3 = io.imread('./fig/fufu3.jpg')
imshow_all(huahua1, huahua2)
imshow_all(fufu1, fufu2, fufu3)
io.show()