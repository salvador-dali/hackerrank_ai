import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.image as img
from scipy import ndimage
from collections import Counter

np.set_printoptions(precision=4)

# http://scikit-learn.org/stable/auto_examples/cluster/plot_color_quantization.html

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

def convert(m, colored, size=100):
    # remove small border
    border = (np.array(m.shape) * 0.03).astype(int)
    m = m[border[0]:-border[0], border[1]:-border[1]]

    anotherCopy = np.copy(m)

    # remove noise
    m = ndimage.median_filter(m, border[0])

    mask = np.copy(m)
    threshold = 0.5
    mask[m < threshold] = 1
    mask[m >=threshold] = 0

    y_min, x_min, y_max, x_max = findMinMax(mask)
    newM = anotherCopy[x_min:x_max+1, y_min:y_max+1]


    attempt = ndimage.zoom(newM, float(size) / newM.shape[0], order=3)
    attempt[attempt < 0] = 0
    attempt[attempt >= 0.9] = 1

    colored = colored[border[0]:-border[0], border[1]:-border[1], :]
    M = colored[x_min:x_max+1, y_min:y_max+1, :]
    return M

def cluster(m, n_colors=32):
    from sklearn.utils import shuffle
    from sklearn.cluster import KMeans
    from sklearn.metrics import pairwise_distances_argmin

    def recreate_image(codebook, labels, w, h):
        """Recreate the (compressed) image from the code book & labels"""
        d = codebook.shape[1]
        image = np.zeros((w, h, d))
        label_idx = 0
        for i in range(w):
            for j in range(h):
                image[i][j] = codebook[labels[label_idx]]
                label_idx += 1
        return image

    # Load Image and transform to a 2D numpy array.
    w, h, d = original_shape = tuple(m.shape)
    image_array = np.reshape(m, (w * h, d))
    image_array_sample = shuffle(image_array, random_state=0)[:1000]
    kmeans = KMeans(n_clusters=n_colors).fit(image_array_sample)

    codebook_random = shuffle(image_array, random_state=0)[:n_colors + 1]
    labels_random = pairwise_distances_argmin(codebook_random, image_array, axis=0)

    return recreate_image(codebook_random, labels_random, w, h)



def printAllImagesFromDirectory(x, y, dir):
    fig, current = plt.figure(), 0
    for file_name in glob.glob(dir):
        image = img.imread(file_name)
        greyscale = (0.21 * image[:, :, 0] + 0.72 * image[:, :, 1] + 0.07 * image[:, :, 2]) / 256
        current += 1

        m = convert(greyscale, image)
        m1 = cluster(m, 16)
        count = Counter([tuple(v) for m2d in m1 for v in m2d])
        sort = sorted(count.values())
        print file_name, (np.array(sort) / float(sum(sort)))[-4:]

        # m1 = ndimage.median_filter(m1, 9)
        # fig.add_subplot(x, y, current).imshow(m)
        fig.add_subplot(x, y, current + 1).imshow(m1)
        # fig.add_subplot(x, y, current + 1).imshow(m1, cmap=cm.Greys_r)
        pass

    plt.show()

printAllImagesFromDirectory(3, 4, 'data/rubiks_cube/*.jpg')