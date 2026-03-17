from imageio import imread
import os
import numpy as np
from align_images import align_images
from crop_image import crop_image
from hybrid_image import hybrid_image
from stacks import stacks
from utils import save_image
ROOT_IMAGES = "../web/images"
# read images
im1_path = os.path.join(ROOT_IMAGES, 'Marilyn_Monroe.png')
im2_path = os.path.join(ROOT_IMAGES, 'Albert_Einstein.png')

im1 = imread(im1_path, pilmode='L')
im2 = imread(im2_path, pilmode='L')

# use this if you want to align the two images (e.g., by the eyes) and crop
# them to be of same size
im1, im2 = align_images(im1, im2)

# Normalisation

im1 = im1.astype(np.float64) / 255.0
im2 = im2.astype(np.float64) / 255.0


# Choose the cutoff frequencies and compute the hybrid image (you supply
# this code)
arbitrary_value_1 = 7
arbitrary_value_2 = 7
cutoff_low = arbitrary_value_1
cutoff_high = arbitrary_value_2
im12 = hybrid_image(im1, im2, cutoff_low, cutoff_high)

# Crop resulting image (optional)
assert im12 is not None, "im12 is empty, implement hybrid_image!"
im12 = crop_image(im12)
save_image(im12, 'combined', ROOT_IMAGES)

# Compute and display Gaussian and Laplacian Stacks (you supply this code)
n = 5  # number of pyramid levels (you may use more or fewer, as needed)
#stacks(im12, n)
