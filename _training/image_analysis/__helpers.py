import sys
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import matplotlib.cm as cm
import random

def readRGB(file_name):
    """ Read a 2d rgb matrix from stdin/file

    A matrix is has each element like r,g,b
    :return: 3D numpy array (x,y,3)
    """
    def iteration():
        line_arr = [map(int, i.split(',')) for i in line.split()]
        line_r, line_g, line_b = [], [], []
        for i in line_arr:
            line_r.append(i[0])
            line_g.append(i[1])
            line_b.append(i[2])

        R.append(line_r)
        G.append(line_g)
        B.append(line_b)

    R, G, B = [], [], []
    if file_name:
        for line in open(file_name):
            iteration()
    else:
        for line in sys.stdin:
            iteration()

    return np.dstack((np.array(R), np.array(G), np.array(B)))

def RGB_to_greyscale(M, humanVision=True):
    """ Converts a 3D (x, y, 3) matrix to a 2D matrix
    if human vision is true, the matrix is scaled a little bit to be viewed nicer by a human
    :param M:
    :param humanVision: boolean
    :return: 2D numpy array
    """
    if humanVision:
        # r, g, b = [0.21, 0.72, 0.07]
        r, g, b = [0.299, 0.587, 0.114]
        return r * M[:, :, 0] + g * M[:, :, 1] + b * M[:, :, 2]


    return np.average(M, axis=2)

def showAllImages():
    ext = "*.jpg"

    total_count, current = sum(1 for _ in glob.glob(ext)), 0
    size_x = int(total_count**0.5)
    size_y = size_x if size_x ** 2 == total_count else size_x + 1
    fig = plt.figure(figsize=(16, 8))

    for file_name in glob.glob(ext):
        image = img.imread(file_name)
        current += 1

        fig.add_subplot(size_x, size_y, current).imshow(image, cmap=cm.Greys_r)
        plt.axis('off')

    plt.show()

def showRandomImages(n, m):
    ext = "*.jpg"

    files, current = [i for i in glob.glob(ext)], 0

    random.shuffle(files)
    files_subset = files[:n * m]

    fig = plt.figure(figsize=(16, 8))
    for file_name in files_subset:
        image = img.imread(file_name)
        current += 1

        fig.add_subplot(n, m, current).imshow(image, cmap=cm.Greys_r)
        fig.tight_layout()
        plt.title(file_name)    # file_name.split('/')[-1]
        plt.axis('off')

    plt.show()

def most_frequent(M):
    x, y, _ = M.shape
    res = np.zeros((x - 2, y - 2, 3), dtype=np.uint8)
    for i in xrange(1, x - 1):
        for j in xrange(1, y - 1):
            neighbors = [M[i - 1, j - 1], M[i - 1, j], M[i - 1, j + 1], M[i, j - 1], M[i, j], M[i, j + 1], M[i + 1, j - 1], M[i + 1, j], M[i + 1, j + 1]]
            cnt = Counter([tuple(_) for _ in neighbors])
            if len(cnt) >= 5:
                res[i - 1, j - 1] = (255, 255, 255)
            else:
                res[i - 1, j - 1] = cnt.most_common(1)[0][0]

    return res