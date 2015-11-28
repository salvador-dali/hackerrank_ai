from scipy.stats import norm

m, s, val, step = 2000, 200, 2500, 400
for i in xrange(1000):
    res = 1 - norm.cdf(val, m, s)
    if res > 0.1:
        val += step
    else:
        val -= step

    step *= 0.97

print val