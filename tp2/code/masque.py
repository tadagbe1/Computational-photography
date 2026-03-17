import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

ROOT_IMAGES = "../web/images"

# --------------------------------------------------
# 1️⃣ Charger image
# --------------------------------------------------

image_path = os.path.join(ROOT_IMAGES, "oeil_masque.png")
img = cv2.imread(image_path)

if img is None:
    print("Erreur : image non trouvée")
    exit()

# --------------------------------------------------
# 2️⃣ Initialisation GrabCut
# --------------------------------------------------

mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

h, w = img.shape[:2]
rect = (30, 30, w-60, h-60)

# --------------------------------------------------
# 3️⃣ GrabCut
# --------------------------------------------------

cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

mask_binary = np.where(
    (mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD),
    0,
    255
).astype("uint8")

# --------------------------------------------------
# 4️⃣ Nettoyage morphologique
# --------------------------------------------------

kernel = np.ones((5,5), np.uint8)
mask_binary = cv2.morphologyEx(mask_binary, cv2.MORPH_CLOSE, kernel, iterations=2)
mask_binary = cv2.morphologyEx(mask_binary, cv2.MORPH_OPEN, kernel, iterations=1)

# --------------------------------------------------
# 5️⃣ Appliquer masque
# --------------------------------------------------

result = cv2.bitwise_and(img, img, mask=mask_binary)

# --------------------------------------------------
# 6️⃣ Sauvegardes
# --------------------------------------------------

# Masque binaire
mask_path = os.path.join(ROOT_IMAGES, "mask_binary_eye.png")
cv2.imwrite(mask_path, mask_binary)



# --------------------------------------------------
# 7️⃣ Affichage
# --------------------------------------------------

plt.figure(figsize=(15,5))

plt.subplot(1,3,1)
plt.title("Image originale")
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.subplot(1,3,2)
plt.title("Masque binaire")
plt.imshow(mask_binary, cmap="gray")
plt.axis("off")

plt.subplot(1,3,3)
plt.title("Image découpée")
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.tight_layout()
plt.show()

