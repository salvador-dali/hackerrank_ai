"""
weights = {
    3: [10, 12],
    4: [3, 9, 14],
    5: [8],
    6: [4],
    7: [5, 11, 13],
    12: [6, 7]
}
"""

import math
from scipy.misc import imresize
from scipy import ndimage
import pickle
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import matplotlib.cm as cm

def showAllImages():
    ext = "img/*.jpg"
    total_count, current = sum(1 for _ in glob.glob(ext)), 0
    size_x, size_y = 2, 2
    fig = plt.figure(figsize=(16, 8))
    for file_name in glob.glob(ext):
        image = img.imread(file_name)
        image = RGB(image)

        current += 1


        fig.add_subplot(size_x, size_y, current).imshow(image, cmap=cm.Greys_r)
        plt.axis('off')

    plt.show()

def testAll():
    fig = plt.figure(figsize=(16, 8))
    current = 0
    for file_name in glob.glob("img/*.jpg"):
        image = img.imread(file_name)
        r = imresize(image, (100, 100))

        mask1 = ndimage.binary_erosion(coloration(r), structure=np.ones((3, 3)))

        greyscale = np.average(image, axis=2)
        dx = ndimage.sobel(greyscale, 0)  # horizontal derivative
        dy = ndimage.sobel(greyscale, 1)  # vertical derivative
        mask2 = np.hypot(dx, dy)  # magnitude

        current += 1
        fig.add_subplot(3, 3, current).imshow(mask1, cmap=cm.Greys_r, interpolation='none')
        labeled_array, num_features = ndimage.label(mask1)
        print labeled_array, num_features
        current += 1
        fig.add_subplot(3, 3, current).imshow(mask2, cmap=cm.Greys_r, interpolation='none')
        current += 1
        fig.add_subplot(3, 3, current).imshow(r, cmap=cm.Greys_r, interpolation='none')
        plt.axis('off')

    plt.show()




def coloration(M):
    m = M.astype(float)
    R_m, G_m, B_m = 224, 193, 177
    R_s, G_s, B_s = 15., 17., 21.

    R, G, B = m[:, :, 0], m[:, :, 1], m[:, :, 2]
    r, g, b = abs(R - R_m) / R_s, abs(G - G_m) / G_s, abs(B - B_m) / B_s

    scale, greyness = 4, 110
    a1 = np.logical_and(abs(R - G) + abs(G - B) + abs(B - R) > greyness, b < scale)
    a2 = np.logical_and(r < scale, g < scale)
    return np.logical_and(a1, a2)

def test():
    image = img.imread("img/03.jpg")

    weights = [0.9553, 0.955412, 0.955431, 0, 0, 0, 0, 0, 2.23, 2.2234, 2.1, 3.9, 3.82, 3.821, 3.9, 3.821, 3.731, 3.742, 3.856, 3.678, 3.821]
    r = imresize(image, (100, 100))
    mask1 = ndimage.binary_erosion(coloration(r), structure=np.ones((3, 3)))


    labeled_array, num_features = ndimage.label(mask1)
    _, counts = np.unique(labeled_array, True)
    sizes = counts[1:]
    freq = sizes / float(max(sizes))

    rough_estimate = sum(freq > 0.54)
    better_estimate = int(round(math.pi * weights[rough_estimate])) if weights[rough_estimate] else rough_estimate
    print better_estimate



test()
