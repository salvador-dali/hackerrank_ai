from scipy.stats import pearsonr

def mean(a):
    return float(sum(a)) / len(a)

def pearson(X, Y):
    n, m = len(X), len(Y)
    if n != m:
        return 'Error'

    mX, mY = mean(X), mean(Y)
    up, sX, sY = 0, 0, 0
    for i in xrange(n):
        dx, dy = X[i] - mX, Y[i] - mY
        up += dx * dy
        sX += dx**2
        sY += dy**2

    return up / (sX * sY)**0.5




A = [73, 48, 95, 95, 33, 47, 98, 91, 95, 93, 70, 85, 33, 47, 95, 84, 43, 95, 54, 72]
B = [72, 67, 92, 95, 59, 58, 95, 94, 84, 83, 70, 79, 67, 73, 87, 86, 63, 92, 80, 76]
C = [76, 76, 95, 96, 79, 74, 97, 97, 90, 90, 78, 91, 76, 90, 95, 95, 75, 100, 87, 90]

print pearson(A, B)