# this is just to analyze how the data looks like
# after looking at the data, we see that for x < 4 y = 2*x
# for x > 4 y = 8
def analyze():
    import matplotlib.pyplot as plt
    f = open("laptopBattery.txt")
    lines = f.readlines()
    x, y = [], []
    for i in lines:
        a, b = map(float, i.rstrip().split(','))
        x.append(a)
        y.append(b)


    plt.scatter(x, y)
    plt.show()

def predict(x):
    if x < 4:
        return x * 2
    else:
        return 8
