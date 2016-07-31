import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import matplotlib.cm as cm
from scipy import ndimage

# https://www.hackerrank.com/contests/may-real-data/challenges/count-the-pairs-of-tracks/forum/comments


os.chdir("data/pair_tracks")

def RGB_to_greyscale(M, humanVision=True):
    if humanVision:
        return 0.21 * M[:, :, 0] + 0.72 * M[:, :, 0] + 0.07 * M[:, :, 0]

    return np.average(M, axis=2)

def transform(M):
    # M = ndimage.gaussian_filter(M, sigma=5)
    # M[:,:,1] = 0
    # M = RGB_to_greyscale(M)
    # sx = ndimage.sobel(M, axis=0, mode='wrap', cval=50)
    # sy = ndimage.sobel(M, axis=1, mode='wrap', cval=50)
    # M = np.hypot(sx, sy)
    return M

def showAllImages():
    ext = "track1_1.jpg"

    total_count, current = sum(1 for _ in glob.glob(ext)), 0
    fig = plt.figure(figsize=(16, 8))

    for file_name in glob.glob(ext):
        image = img.imread(file_name)
        fig.add_subplot(2, total_count, current + 1).imshow(image, cmap=cm.Greys_r)
        plt.axis('off')
        fig.add_subplot(2, total_count, current + 1 + total_count).imshow(transform(image), cmap=cm.Greys_r)
        plt.axis('off')
        current += 1

        # color = image[0:4,0:4,:]
        # colors = np.array([
        #     [[1, 2, 3], [1, 2, 3]],
        #     [[1, 2, 3], [1, 2, 3]]
        # ])
        #
        # print colors
        # mask = np.array([[0, 1], [0, 0]])
        # print mask
        # print np.std(colors, axis=2)
    plt.tight_layout()
    plt.show()



showAllImages()