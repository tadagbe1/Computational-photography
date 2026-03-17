from main_pile import pile_laplacienne, pile_gaussienne
import numpy as np
import skimage as sk
import os
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import skimage as sk

def melange(im1, im2, masque, n_pile, file_name, root):

    laplacienne_im1 = pile_laplacienne(im1, n_pile)
    laplacienne_im2 = pile_laplacienne(im2, n_pile)
    gaussienne_masque = pile_gaussienne(masque, n_pile)

    pile_composition = []

    for i in range(n_pile):
        compose = (
            gaussienne_masque[i] * laplacienne_im1[i]
            + (1 - gaussienne_masque[i]) * laplacienne_im2[i]
        )
        pile_composition.append(compose)

    pile_composition = np.array(pile_composition)

    finale_img = np.sum(pile_composition, axis=0)

    # normalisation propre
    finale_img = (finale_img - finale_img.min()) / (finale_img.max() - finale_img.min())

    # -------------------------
    # FIGURE COMPLETE 2x5
    # -------------------------

    fig, axes = plt.subplots(1, 5, figsize=(8, 10))

    # Ligne 1
    axes[0].imshow(im1)
    axes[0].set_title("Image 1 originale")
    axes[0].axis("off")

    axes[1].imshow(im2)
    axes[1].set_title("Image 2 originale")
    axes[1].axis("off")

    axes[2].imshow(finale_img)
    axes[2].set_title("Image composée")
    axes[2].axis("off")

    if masque.ndim == 3:
        masque_gray = masque[:, :, 0]
    else:
        masque_gray = masque

    axes[3].imshow(masque_gray, cmap="gray")
    axes[3].set_title("Masque")
    axes[3].axis("off")

    axes[4].imshow(1 - masque_gray, cmap="gray")
    axes[4].set_title("Masque inversé")
    axes[4].axis("off")


    plt.tight_layout()
    #plt.tight_layout()
    plt.savefig(os.path.join(root, file_name), dpi=300)
    plt.close(fig)

    return finale_img


   

def _show_laplacian(ax, L, title=""):
    """Affiche une laplacienne avec une échelle centrée autour de 0 (super important)."""
    L = L.astype(np.float32)
    m = np.max(np.abs(L)) + 1e-8
    ax.imshow(np.clip(L / (2*m) + 0.5, 0, 1))  # map [-m,m] -> [0,1]
    ax.set_title(title)
    ax.axis("off")

def figure10_like(im1, im2, masque, n_pile, titre="Illustration du procédé (Fig.10-like)", root=None):
    # piles
    L1 = pile_laplacienne(im1, n_pile)
    L2 = pile_laplacienne(im2, n_pile)

    # masque: IMPORTANT -> float [0,1] + 3 canaux
    if masque.ndim == 3:
        m0 = masque[:, :, 0]
    else:
        m0 = masque
    m0 = sk.img_as_float(m0)
    m3 = np.repeat(m0[:, :, np.newaxis], 3, axis=2)

    GM = pile_gaussienne(m3, n_pile)

    # bandes mélangées
    B = []
    for i in range(n_pile):
        b = GM[i] * L1[i] + (1.0 - GM[i]) * L2[i]
        B.append(b)

    # cumul progressif (somme des bandes jusqu’à i)
    cumul = []
    acc = np.zeros_like(B[0], dtype=np.float32)
    for i in range(n_pile):
        acc = acc + B[i]
        cumul.append(acc.copy())

    # ---- FIGURE ----
    # 4 colonnes: L1, L2, Blend, Cumul
    fig, axes = plt.subplots(n_pile + 1, 4, figsize=(18, 2*(n_pile+1)))

    # entêtes
    headers = ["Bande im1 (Laplacien)", "Bande im2 (Laplacien)", "Bande mélangée", "Somme progressive"]
    for j in range(4):
        axes[0, j].set_title(headers[j], fontsize=12)

    # lignes niveaux
    for i in range(n_pile):
        _show_laplacian(axes[i, 0], L1[i], title=f"Niveau {i}")
        _show_laplacian(axes[i, 1], L2[i], title=f"Niveau {i}")
        _show_laplacian(axes[i, 2], B[i],  title=f"Niveau {i}")
        axes[i, 3].imshow(np.clip(cumul[i], 0, 1))
        axes[i, 3].set_title(f"Cumul ≤ {i}")
        axes[i, 3].axis("off")

    # dernière ligne: originaux + masque + résultat final
    axes[n_pile, 0].imshow(np.clip(im1, 0, 1)); axes[n_pile, 0].set_title("Image 1"); axes[n_pile, 0].axis("off")
    axes[n_pile, 1].imshow(np.clip(im2, 0, 1)); axes[n_pile, 1].set_title("Image 2"); axes[n_pile, 1].axis("off")
    axes[n_pile, 2].imshow(m0, cmap="gray");     axes[n_pile, 2].set_title("Masque");  axes[n_pile, 2].axis("off")
    axes[n_pile, 3].imshow(np.clip(cumul[-1], 0, 1)); axes[n_pile, 3].set_title("Résultat final"); axes[n_pile, 3].axis("off")

    fig.suptitle(titre, fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.93)
    plt.savefig(os.path.join(root, 'detail_compose.jpg'))
    #plt.show()

    return cumul[-1]


if __name__ == "__main__":
    ROOT_IMAGES = "../web/images"

    im1 = sk.io.imread(os.path.join(ROOT_IMAGES, "apple.jpeg"))
    im2 = sk.io.imread(os.path.join(ROOT_IMAGES, "orange.jpeg"))
    #sk.io.imshow(im1)
    #sk.io.show()

    delimiteur_masque = im1.shape[1]//2

    masque = np.ones(im1.shape).astype(float)
    masque[:, delimiteur_masque:] = 0.0

    im1 = sk.img_as_float(im1)
    im2 = sk.img_as_float(im2)

    image_melange = melange(im1, im2, masque, 6, 'pommange.jpg', ROOT_IMAGES)
    sk.io.imshow(image_melange)
    sk.io.show()

    perso_im2 = sk.io.imread(os.path.join(ROOT_IMAGES, "ganvie1.jpg"))
    perso_im1 = sk.io.imread(os.path.join(ROOT_IMAGES, "tadagbe1.jpeg"))
    perso_masque = sk.io.imread(os.path.join(ROOT_IMAGES, "mask_binary.png"))
    perso_masque = np.repeat(perso_masque[:, :, np.newaxis], 3, axis=2)

    perso_im1 = sk.img_as_float(perso_im1)
    perso_im2 = sk.img_as_float(perso_im2)
    perso_masque = sk.img_as_float(perso_masque)
    #perso_masque = (perso_masque > 0.3).astype(float)

    #breakpoint()
    perso_image_melange = melange(perso_im1, perso_im2, perso_masque, 6, 'tadagbe_ganvie.jpg', ROOT_IMAGES)
    sk.io.imshow(perso_image_melange)
    sk.io.show()

    # 

    reg_perso_im2 = sk.io.imread(os.path.join(ROOT_IMAGES, "montreal3_reduced.jpeg"))
    reg_perso_im1 = sk.io.imread(os.path.join(ROOT_IMAGES, "oeil.jpg"))
    reg_perso_masque = sk.io.imread(os.path.join(ROOT_IMAGES, "mask_binary_eye.png"))
    reg_perso_masque = np.repeat(reg_perso_masque[:, :, np.newaxis], 3, axis=2)

    reg_perso_im1 = sk.img_as_float(reg_perso_im1)
    reg_perso_im2 = sk.img_as_float(reg_perso_im2)
    reg_perso_masque = sk.img_as_float(reg_perso_masque)
    #perso_masque = (perso_masque > 0.3).astype(float)

    #breakpoint()
    # reg_perso_image_melange = melange(reg_perso_im1, reg_perso_im2, reg_perso_masque, 6, 'oeil_montreal.jpg', ROOT_IMAGES)
    # sk.io.imshow(reg_perso_image_melange)
    # sk.io.show()


    figure10_like(reg_perso_im1, reg_perso_im2, reg_perso_masque, n_pile=6,
              titre="Procédé détaillé (mon résultat préféré)", root=ROOT_IMAGES)
