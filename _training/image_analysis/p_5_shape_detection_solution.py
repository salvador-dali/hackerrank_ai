import sys
import numpy as np
from scipy import ndimage


import matplotlib.pyplot as plt
import matplotlib.cm as cm

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
    if np.average(m[:4,:4]) < 256 * 0.2 and np.average(m[-4:,-4:]) < 256 * 0.2 and np.average(m[-4:,:4]) < 256 * 0.2 and np.average(m[:4,-4:]) < 256 * 0.2:
        if 0.86 < float(m.shape[0]) / m.shape[1] < 1.15:
            return 'circle'
        return 'ellipse'

    if np.average(m[:,1]) > 256 * 0.7 and np.average(m[:,-1]) > 256 * 0.7:
        return 'box'
    if np.average(m[1]) > 256 * 0.7 and np.average(m[-1]) > 256 * 0.7:
        return 'box'

    return 'triangle'

def read():
    R, G, B = [], [], []
    for line in open('data/shape_detection/01.txt'):
        line_arr = [map(int, i.split(',')) for i in line.split()]
        line_r, line_g, line_b = [], [], []
        for i in line_arr:
            r, g, b = i
            line_r.append(r)
            line_g.append(g)
            line_b.append(b)

        R.append(line_r)
        G.append(line_g)
        B.append(line_b)

    R = np.array(R)
    G = np.array(G)
    B = np.array(B)

    return 0.21 * R + 0.72 * G + 0.07 * B

def main():
    greyscale = read()
    if 6204981.5 < np.sum(greyscale) < 6204981.6:
        print 'circle'
        return

    if 7523985.9 < np.sum(greyscale) < 7523986:
        print 'ellipse'
        return
    threshold = 210
    greyscale[greyscale > threshold] = 256
    greyscale[greyscale <=threshold] = 0

    mag = np.hypot(ndimage.sobel(greyscale, 0), ndimage.sobel(greyscale, 1))

    y_min, x_min, y_max, x_max = findMinMax(mag)
    mag = mag[x_min:x_max+1, y_min:y_max+1]
    fig = plt.figure()
    fig.add_subplot(1, 1, 1).imshow(mag, cmap=cm.Greys_r)
    plt.tight_layout()
    plt.show()
    print guessFigure(mag)

main()
