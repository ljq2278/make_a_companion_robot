import sys
#
# from PIL import Image
#
# image = Image.open(sys.argv[1])
# image.show()
# image.close()
import skimage.io as io
from skimage.io import imread
from matplotlib import pyplot as plt

img = imread(sys.argv[1]) #path to IMG
io.imshow(img)
plt.show()