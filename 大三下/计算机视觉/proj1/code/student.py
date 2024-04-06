# Project Image Filtering and Hybrid Images Stencil Code
# Based on previous and current work
# by James Hays for CSCI 1430 @ Brown and
# CS 4495/6476 @ Georgia Tech
import numpy as np
from numpy import pi, exp, sqrt
from skimage import io, img_as_ubyte, img_as_float32
from skimage.transform import rescale


def my_imfilter(image, filter):
    """
  Your function should meet the requirements laid out on the project webpage.
  Apply a filter to an image. Return the filtered image.
  Inputs:
  - image -> numpy nd-array of dim (m, n, c)
  - filter -> numpy nd-array of odd dim (k, l)
  Returns
  - filtered_image -> numpy nd-array of dim (m, n, c)
  Errors if:
  - filter has any even dimension -> raise an Exception with a suitable error message.
  """
    filtered_image = np.asarray([0])

    assert filter.shape[0] % 2 == 1
    assert filter.shape[1] % 2 == 1
    # 默认设置图像的通道数，如果只有一个通道，即输入图片是二维的。
    channel = 1
    # 如果输入维度=3，通道数等于第三个维度的元素数量
    if image.ndim == 3:
        channel = image.shape[2]
    # 获取图片的长度和宽度
    image_h, image_w = image.shape[:2]
    # 将过滤核做上下、左右翻转，以确保是卷积操作而不是相关操作
    filter = np.flipud(filter)
    filter = np.fliplr(filter)
    # 获取过滤核的长度和宽度
    filter_h, filter_w = filter.shape
    pad_h = (filter_h - 1) // 2
    pad_w = (filter_w - 1) // 2
    # 先扩充原图像,为了不影响原图像，需要复制一份图像
    image_cp = image.copy()
    image_cp = np.pad(image_cp, [(pad_h, pad_h), (pad_w, pad_w), (0, 0)], "constant")
    # 生成过滤后的图片的空容器，尺寸可以是原本的尺寸，在这里为了下面坐标转换方便，扩大了长宽。
    filtered_image = np.zeros(image_cp.shape)
    # 第一层是对于不同的channel做卷积
    for i in range(channel):
        for j in range(pad_h, image_h + pad_h):
            for k in range(pad_w, image_w + pad_w):
                filtered_image[j, k, i] = np.sum(
                    np.multiply(image_cp[j - pad_h:j + pad_h + 1, k - pad_w:k + pad_w + 1, i], filter))
    return filtered_image[pad_h:image_h + pad_h, pad_w:image_w + pad_w, :]


def gen_hybrid_image(image1, image2, cutoff_frequency):
    """
   Inputs:
   - image1 -> The image from which to take the low frequencies.
   - image2 -> The image from which to take the high frequencies.
   - cutoff_frequency -> The standard deviation, in pixels, of the Gaussian
                         blur that will remove high frequencies.

   Task:
   - Use my_imfilter to create 'low_frequencies' and 'high_frequencies'.
   - Combine them to create 'hybrid_image'.
  """

    assert image1.shape[0] == image2.shape[0]
    assert image1.shape[1] == image2.shape[1]
    assert image1.shape[2] == image2.shape[2]

    # Steps:
    # (1) Remove the high frequencies from image1 by blurring it. The amount of
    #     blur that works best will vary with different image pairs
    # generate a 1x(2k+1) gaussian kernel with mean=0 and sigma = s, see https://stackoverflow.com/questions/17190649/how-to-obtain-a-gaussian-filter-in-python
    s, k = cutoff_frequency, cutoff_frequency * 2
    probs = np.asarray([exp(-z * z / (2 * s * s)) / sqrt(2 * pi * s * s) for z in range(-k, k + 1)], dtype=np.float32)
    kernel = np.outer(probs, probs)

    # Your code here:
    # low_frequencies = None # Replace with your implementation
    low_frequencies = my_imfilter(image1, kernel)

    # (2) Remove the low frequencies from image2. The easiest way to do this is to
    #     subtract a blurred version of image2 from the original version of image2.
    #     This will give you an image centered at zero with negative values.
    # Your code here #
    # high_frequencies = None # Replace with your implementation
    high_frequencies = image2 - my_imfilter(image2, kernel)

    # (3) Combine the high frequencies and low frequencies
    # Your code here #
    # hybrid_image = None
    hybrid_image = low_frequencies + high_frequencies  # Replace with your implementation

    # (4) At this point, you need to be aware that values larger than 1.0
    # or less than 0.0 may cause issues in the functions in Python for saving
    # images to disk. These are called in proj1_part2 after the call to
    # gen_hybrid_image().
    # One option is to clip (also called clamp) all values below 0.0 to 0.0,
    # and all values larger than 1.0 to 1.0.

    return low_frequencies, high_frequencies, hybrid_image


def vis_hybrid_image(hybrid_image):
    """
  Visualize a hybrid image by progressively downsampling the image and
  concatenating all of the images together.
  """
    scales = 5
    scale_factor = [0.5, 0.5, 1]
    padding = 5
    original_height = hybrid_image.shape[0]
    num_colors = 1 if hybrid_image.ndim == 2 else 3

    output = np.copy(hybrid_image)
    cur_image = np.copy(hybrid_image)
    for scale in range(2, scales + 1):
        # add padding
        output = np.hstack((output, np.ones((original_height, padding, num_colors),
                                            dtype=np.float32)))
        # downsample image
        cur_image = rescale(cur_image, scale_factor, mode='reflect')
        # pad the top to append to the output
        pad = np.ones((original_height - cur_image.shape[0], cur_image.shape[1],
                       num_colors), dtype=np.float32)
        tmp = np.vstack((pad, cur_image))
        output = np.hstack((output, tmp))
    return output


def load_image(path):
    return img_as_float32(io.imread(path))


def save_image(path, im):
    return io.imsave(path, img_as_ubyte(im.copy()))
