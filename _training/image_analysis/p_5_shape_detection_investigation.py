import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.image as img
from scipy import ndimage
from scipy.misc import imresize

os.chdir("data/shape_detection")

def findMinMax(m):
    x_min, y_min, x_max, y_max = 0, 0, m.shape[1], m.shape[0]
    y = np.any(m, axis=0)
    for i in xrange(len(y)):
        if y[i]:
            y_min = i
            break

    for i in xrange(len(y) - 1, 0, -1):
        if y[i]:
            y_max = i
            break

    y = np.any(m, axis=1)
    for i in xrange(len(y)):
        if y[i]:
            x_min = i
            break

    for i in xrange(len(y) - 1, 0, -1):
        if y[i]:
            x_max = i
            break

    return y_min, x_min, y_max, x_max

def guessFigure(m):
    if np.average(m) == 0:
        return 'box'

    if np.average(m[:4,:4]) < 0.2 and np.average(m[-4:,-4:]) < 0.2 and np.average(m[-4:,:4]) < 0.2 and np.average(m[:4,-4:]) < 0.2:
        print float(m.shape[0]) / m.shape[1]
        if 0.86 < float(m.shape[0]) / m.shape[1] < 1.15:
            return 'circle'
        return 'ellipse'
    if np.average(m[:,1]) > 0.7 and np.average(m[:,-1]) > 0.7:
        return 'box'
    if np.average(m[1]) > 0.7 and np.average(m[-1]) > 0.7:
        return 'box'

    return 'triangle'

def showAllImages():
    fig, current = plt.figure(), 0
    for file_name in glob.glob("*.png"):
        image = img.imread(file_name)
        R, G, B = image[:,:,0], image[:,:,1], image[:,:,2]
        greyscale = 0.21 * R + 0.72 * G + 0.07 * B
        threshold = 210.0 / 256
        greyscale[greyscale > threshold] = 1
        greyscale[greyscale <=threshold] = 0

        dx = ndimage.sobel(greyscale, 0)  # horizontal derivative
        dy = ndimage.sobel(greyscale, 1)  # vertical derivative
        mag = np.hypot(dx, dy)  # magnitude

        y_min, x_min, y_max, x_max = findMinMax(mag)
        mag = mag[x_min:x_max+1, y_min:y_max+1]

        # x, y = mag.shape
        # ration = float(x) / y
        # mag = imresize(mag, (50, int(50 / ration)))
        #
        # mag[mag > threshold] = 1
        # mag[mag <=threshold] = 0
        current += 1
        if current == 7:
            fig.add_subplot(1, 1, 1).imshow(mag, cmap=cm.Greys_r)
            print guessFigure(mag)
            break


    plt.tight_layout()
    plt.show()

showAllImages()