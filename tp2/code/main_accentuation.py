from skimage import filters
import os
import numpy as np
from utils import  load_image, save_image

ROOT_IMAGES = "../web/images"
ALPHA = 2

def sharpened(img, alpha):
    blurred = filters.gaussian(img, channel_axis=-1, sigma=5)
    img_details = (img - blurred)
    img_sharpened = (img + alpha*img_details) 
    return np.clip(img_sharpened, 0, 1)

if __name__ == "__main__":
    img_names = ['montreal1', 'montreal2', 'montreal3', 'quebec1', 'ganvie1']
    for img_name in img_names:
        if img_name == 'ganvie1':
            img_path = os.path.join(ROOT_IMAGES, img_name + '.jpg')
        else:
            img_path = os.path.join(ROOT_IMAGES, img_name + '.jpeg')

        img = load_image(img_path)
        img_sharpened = sharpened(img, ALPHA)
        save_image(img_sharpened, img_name + '_sharpened', ROOT_IMAGES)
        


