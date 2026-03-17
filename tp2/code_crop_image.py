

import skimage
import os

root = "./web/images"
im = skimage.io.imread(os.path.join(root, 'tadagbe2.jpeg'))
breakpoint()