# Ecris par moi meme

from skimage import io, img_as_float
import numpy as np
import os


def load_image(path):
    img = io.imread(path)
    return img_as_float(img)

def save_image(path, image):
    image = image.clip(0, 1)
    image = (255 * image).astype(np.uint8)
    io.imsave(path, image)

def load_points(path):
    points = []
    with open(path, 'r') as f:
        for line in f:
            if line.strip():
                #breakpoint()
                x, y = line.strip().split('\t')
                x = float(x)
                y = float(y)
                points.append([x, y])
    return np.array(points, dtype=np.float64)

def create_directory(path):
    os.makedirs(path, exist_ok=True)