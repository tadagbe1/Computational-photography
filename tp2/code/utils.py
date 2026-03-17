import skimage.io as skio
import skimage as sk
import os


def load_image(img_path):
    img = skio.imread(img_path)
    return sk.img_as_float(img)

def save_image(img, name, root_images):
    img = sk.img_as_ubyte(img)
    path = os.path.join(root_images, name + '.jpg')
    skio.imsave(path, img)
    print(f"Image saved to {path}")

def save_image_jpeg(img, name, root_images):
    img = sk.img_as_ubyte(img)
    path = os.path.join(root_images, name + '.jpeg')
    skio.imsave(path, img)
    print(f"Image saved to {path}")

def save_to_gray(root, img_path ):
    img_color = skio.imread(os.path.join(root,img_path))
    img_gray = sk.color.rgb2gray(img_color)
    name = img_path[:img_path.index('.')]
    skio.imsave(os.path.join(root, f"{name}_gray.png"), sk.img_as_ubyte(img_gray))

if __name__ == "__main__":
    img_paths = ['julci.jpeg', 'tadagbe.jpeg', 'vieux.jpg', 'jeune1.jpg']
    root_images = "../web/images"

    for img_path in img_paths:
        save_to_gray(root_images, img_path)
    
