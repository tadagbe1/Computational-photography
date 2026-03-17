from skimage import filters
import numpy as np
def low_pass(img, cutoff_low):
    return filters.gaussian(img, sigma=cutoff_low)

def high_pass(img, cutoff_high):
    return img - filters.gaussian(img, sigma=cutoff_high)

def hybrid_image(im1, im2, cutoff_low, cutoff_high):
    low_freq = low_pass(im1, cutoff_low)
    high_freq = high_pass(im2, cutoff_high)
    return np.clip(low_freq + high_freq, 0.0, 1.0)
