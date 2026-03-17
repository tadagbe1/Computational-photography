from imageio import imread
from align_images import align_images
from crop_image import crop_image
from skimage import filters
import skimage as sk
import os
import numpy as np
from utils import  save_image, save_image_jpeg
from skimage import io, img_as_ubyte


def low_pass(img, cutoff_low):
    return filters.gaussian(img, sigma=cutoff_low)

def high_pass(img, cutoff_high):
    return img - filters.gaussian(img, sigma=cutoff_high)

def hybride_image(img1, img2, cutoff_low, cutoff_high, prefered=False):
    low = low_pass(img1, cutoff_low)
    high = high_pass(img2, cutoff_high)
    hybrid = np.clip(low + high, 0.0, 1.0)
    if prefered:
        fft_im1 = fft_log_amplitude(img1)
        fft_im2 = fft_log_amplitude(img2)
        fft_low = fft_log_amplitude(low)
        fft_high = fft_log_amplitude(high)
        #fft_hybrid = fft_log_amplitude(hybrid)
        return hybrid, fft_im1, fft_im2, fft_low, fft_high#, fft_hybrid

    return hybrid

def compose_images(im1_path, im2_path, name, save_jpeg=False, prefered=False, root=None):
    im1 = sk.img_as_float(imread(im1_path, pilmode='L'))
    im2 = sk.img_as_float(imread(im2_path, pilmode='L'))  

    # use this if you want to align the two images (e.g., by the eyes) and crop
    # them to be of same size
    im1, im2 = align_images(im1, im2)


    # Normalisation
    # im1 = im1.astype(np.float64) / 255.0
    # im2 = im2.astype(np.float64) / 255.0

    # Choose the cutoff frequencies and compute the hybrid image (you supply
    # this code)
    arbitrary_value_1 = 0.02 * min(im1.shape)
    arbitrary_value_2 = 0.01 * min(im2.shape)
    cutoff_low = arbitrary_value_1
    cutoff_high = arbitrary_value_2
    if prefered:
        im12, fft_im1, fft_im2, fft_low, fft_high = hybride_image(im1, im2, cutoff_low, cutoff_high, prefered)
        assert im12 is not None, "im12 is empty, implement hybrid_image!"
        im12 = crop_image(im12)
        fft_hybrid = fft_log_amplitude(im12)
        save_ffts(root, fft_im1, fft_im2, fft_low, fft_high, fft_hybrid)
    else:
        im12 = hybride_image(im1, im2, cutoff_low, cutoff_high, prefered)
        # Crop resulting image (optional)
        assert im12 is not None, "im12 is empty, implement hybrid_image!"
        im12 = crop_image(im12)
        #im12 = np.clip(im12, 0, 1)

    if save_jpeg:
        save_image_jpeg(im12, name, ROOT_IMAGES)
    else:
        save_image(im12, name, ROOT_IMAGES)
    

def fft_log_amplitude(img):
    return normalize_for_display(np.log(np.abs(np.fft.fftshift(np.fft.fft2(img))) + 1))

def normalize_for_display(img):
    img = img - np.min(img)
    img = img / np.max(img)
    return img

def save_ffts(root, fft_im1, fft_im2, fft_low, fft_high, fft_hybrid):
    io.imsave(os.path.join(root,"fft_jeune.png"), img_as_ubyte(fft_im1))
    io.imsave(os.path.join(root,"fft_vieux.png"), img_as_ubyte(fft_im2))
    io.imsave(os.path.join(root,"fft_low.png"), img_as_ubyte(fft_low))
    io.imsave(os.path.join(root,"fft_high.png"), img_as_ubyte(fft_high))
    io.imsave(os.path.join(root,"fft_hybrid.png"), img_as_ubyte(fft_hybrid))



if __name__ == "__main__":

    ROOT_IMAGES = "../web/images"
    # read images
    im1_path = os.path.join(ROOT_IMAGES, 'Marilyn_Monroe.png')
    im2_path = os.path.join(ROOT_IMAGES, 'Albert_Einstein.png')

    perso_img2_path = os.path.join(ROOT_IMAGES, 'julci_gray.png')
    perso_img1_path = os.path.join(ROOT_IMAGES, 'tadagbe_gray.png')

    prefered_img1_path = os.path.join(ROOT_IMAGES, 'jeune1_gray.png')
    prefered_img2_path = os.path.join(ROOT_IMAGES, 'vieux_gray.png')

    #compose_images(im1_path, im2_path, 'combined_marylin_einstein', False, False)

    compose_images(prefered_img1_path, prefered_img2_path, 'combined_jeune_vieux', False, True, ROOT_IMAGES)

    compose_images(perso_img1_path, perso_img2_path, 'combined_julci_tadagbe', False, False)
    
    #compose_images(im1_path, im2_path, 'combined', False)
    #compose_images(perso_img1_path, perso_img2_path, 'mtl_ganvie_combined', True)

    im1 = sk.img_as_float(imread(perso_img1_path, pilmode='L'))
    im2 = sk.img_as_float(imread(perso_img2_path, pilmode='L'))  

    #analyse_freq(ROOT_IMAGES, im1, im2)
