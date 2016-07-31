arr = [20, 22, 24, 25, 23, 26, 28, 26, 29, 27, 28, 30, 27, 29, 28]
# http://www.investopedia.com/terms/m/movingaverage.asp
def MA(arr, n=10):
    s = []
    for i in xrange(len(arr) - n + 1):
        s.append(sum(arr[i:i + n]) / float(n))

    return s

def MA_optimized(arr, n=10):
    # reduces the performance from O(len(arr) * n) to O(len(arr))
    l, out, nF = len(arr), [], float(n)
    if l < n:
        return out

    tmp = sum(arr[:n])
    out.append(tmp / nF)
    for i in xrange(n, l):
        tmp += arr[i] - arr[i - n]
        out.append(tmp / nF)

    return out