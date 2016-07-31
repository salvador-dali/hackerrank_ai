import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.image as img
from scipy import ndimage
from __helpers import RGB_to_greyscale


os.chdir("data/count_the_circles")

def removeBoard(M):
    top, left, bottom, right = 0, 0, M.shape[0] - 1, M.shape[1] - 1

    while not M[top,:].any():
        top += 1

    while not M[:,left].any():
        left += 1

    while not M[bottom,:].any():
        bottom -= 1

    while not M[:,right].any():
        right -= 1

    return M[top:bottom, left:right]

def transform(M):
    M = RGB_to_greyscale(M)         # greyscaling
    M = np.where(M < 0.9, 0, 1)     # binarization
    return removeBoard(M)

def showAllImages():
    ext = "0*.png"

    total_count, current = sum(1 for _ in glob.glob(ext)), 0
    size_x = int(total_count**0.5)
    size_y = size_x if size_x ** 2 == total_count else size_x + 1

    if size_x * size_y < total_count:
        size_x += 1

    fig = plt.figure(figsize=(16, 8))

    for file_name in glob.glob(ext):
        image = img.imread(file_name)
        current += 1
        fig.add_subplot(size_x, size_y, current).imshow(transform(image), cmap=cm.Greys_r)
        plt.axis('off')

    plt.show()

showAllImages()