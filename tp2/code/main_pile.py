from skimage import filters
import skimage.io as skio
import skimage as sk
import matplotlib.pyplot as plt
import numpy as np
import os

def pile_gaussienne(im, n):
    s=2
    pile = [im]
    channel_axis = -1 if im.ndim == 3 else None
    for _ in range(1, n):
        im_filtre = filters.gaussian(im, sigma=s, channel_axis=channel_axis)
        pile.append(im_filtre)
        s = s*2
    return np.array(pile)

# def pile_laplacienne(im, n):
#     pile_gauss = pile_gaussienne(im, n)
#     pile_laplace = []
#     for i in range(n-1):
#         pile_laplace.append(np.clip(pile_gauss[i] - pile_gauss[i+1], 0.0, 1.0))
#     pile_laplace.append(np.clip(pile_gauss[-1], 0.0, 1.0))

#     return np.array(pile_laplace)

def pile_laplacienne(im, n):
    pile_gauss = pile_gaussienne(im, n)
    pile_laplace = []
    for i in range(n-1):
        pile_laplace.append(pile_gauss[i] - pile_gauss[i+1])
    pile_laplace.append(pile_gauss[-1])

    return np.array(pile_laplace)

# def afficher_pile(pile):
#     n = pile.shape[0]
#     fig, axes = plt.subplots(1, n, figsize=(5*n, 5))
#     for i in range(n):
#         im = sk.img_as_float(pile[i])
#         axes[i].imshow(im, cmap="gray")
#         axes[i].axis("off")
#     plt.show()

def save_pile(pile, root, name, laplace=True ):
    n = pile.shape[0]
    fig, axes = plt.subplots(1, n, figsize=(4*n, 4))
    s = 2 if laplace else 1

    for i in range(n):
        im = pile[i]
        
        # normalisation min-max
        im_norm = im #(im - im.min()) / (im.max() - im.min())
        axes[i].imshow(im_norm, cmap="gray")
        axes[i].axis("off")
        axes[i].set_title(f"Sigma={s}")
        s *= 2
    if laplace:
        file_name = os.path.join(root, f"pile_laplace_{name}")
    else:
        file_name = os.path.join(root, f"pile_gauss_{name}")

    plt.tight_layout()
    plt.savefig(file_name, dpi=300)
    plt.close(fig)

def save_pile_gauss_laplace(root, name, n=6):
    image = skio.imread(os.path.join(root, name))
    #breakpoint()
    if len(image.shape) == 3:
        image = sk.color.rgb2gray(image)
    image = sk.img_as_float(image)
    gaussienne = pile_gaussienne(image, n)
    save_pile(gaussienne, root, name,laplace=False)
    laplacienne = pile_laplacienne(image, n-1)
    for i in range(len(laplacienne)):
        print(i, np.mean(np.abs(laplacienne[i])))
    print()
    save_pile(laplacienne, root, name, laplace=True)



if __name__ == "__main__":
    ROOT_IMAGES = "../web/images"
    name = "lincoln.jpg"
    save_pile_gauss_laplace(ROOT_IMAGES, name)
    name_prefered = 'combined_jeune_vieux.jpg'
    save_pile_gauss_laplace(ROOT_IMAGES, name_prefered, n=9)
    
    