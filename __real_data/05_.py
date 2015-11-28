import math
from scipy import ndimage
import numpy as np

param_scale = 4
param_greyness = 110
param_erosion = 3
param_threshold = 0.54

def readRGB():
    y, x = map(int, raw_input().split())
    R, G, B = [], [], []
    for _ in xrange(y):
        line = raw_input()
        line_arr = [map(int, i.split(',')) for i in line.split()]
        
        line_r, line_g, line_b = [], [], []
        for i in line_arr:
            line_b.append(i[0])
            line_g.append(i[1])
            line_r.append(i[2])
        
        R.append(line_r)
        G.append(line_g)
        B.append(line_b)
    
    return np.dstack((np.array(R), np.array(G), np.array(B)))    

def coloration(M):
    m = M.astype(float)
    R_m, G_m, B_m = 224, 193, 177
    R_s, G_s, B_s = 15., 17., 21.

    R, G, B = m[:, :, 0], m[:, :, 1], m[:, :, 2]
    r, g, b = abs(R - R_m) / R_s, abs(G - G_m) / G_s, abs(B - B_m) / B_s

    a1 = np.logical_and(abs(R - G) + abs(G - B) + abs(B - R) > param_greyness, b < param_scale)
    a2 = np.logical_and(r < param_scale, g < param_scale)
    return np.logical_and(a1, a2)

image = readRGB()
weights = [0.9553, 0.955412, 0.955431, 0, 0, 0, 0, 0, 2.23, 2.2234, 2.1, 3.9, 3.82, 3.821, 3.9, 3.821, 3.731, 3.742, 3.856, 3.678, 3.821]
mask1 = ndimage.binary_opening(coloration(image), structure=np.ones((param_erosion, param_erosion)))

labeled_array, num_features = ndimage.label(mask1)
_, counts = np.unique(labeled_array, True)

sizes = counts[1:]
freq = sizes / float(max(sizes))

rough_estimate = sum(freq > param_threshold)
if rough_estimate > 15:
    rough_estimate = 15
better_estimate = int(round(math.pi * weights[rough_estimate])) if weights[rough_estimate] else rough_estimate
print better_estimate

