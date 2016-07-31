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

def analyze():
    import matplotlib.pyplot as plt
    f = open("stockPrediction.txt")
    lines = f.readlines()
    stocks = {}
    for i in lines:
        el = i.rstrip().split()
        stocks[el[0]] = map(float, el[1:])

    n, windowLength = 200, 5

    listOfStocks = stocks.keys()
    plotNumber = len(listOfStocks)
    for _ in xrange(plotNumber):
        plt.subplot(plotNumber, 1, _ + 1)
        cur = stocks[listOfStocks[_]][0:n]
        graph = cur[0:windowLength] + MA_optimized(cur, windowLength)
        plt.plot(cur, color="black", linewidth=0.5, linestyle="-", alpha=1)
        plt.plot(graph, color="b", linewidth=2, linestyle="-", alpha=0.8)
        plt.xlim(0, n)
        plt.ylim(min(cur), max(cur))

    plt.tight_layout(pad=0.5)
    plt.show()

# select which Stock to buy, based on the money you have
# prices for each stock,
# and number of each stocks you currently have
def buyingStocksForPortfolio(money, stockPortfolio, stockPrices, stockMA):
    el = sorted(stockPrices.items(), key=lambda x: x[1])
    if el[0][1] > money:
        # even the cheapest security is bigger then the money you have
        # can buy absolutely nothing
        return None

    # check which security is impossible to buy
    namesRemove = []
    for i in stockPrices:
        if stockPrices[i] > money:
            namesRemove.append(i)

    # end remove all these securities
    for i in namesRemove:
        del stocksPrices[i]
        del stockPortfolio[i]
        del stockMA[i]

    print stocksPrices

    return 1

def buyStocksBootstrap(money, stockPortfolio, stockPrices):
    return 1

def strategyAttempt():
    f = open("stockPrediction.txt")
    lines = f.readlines()
    money, stocks, stocksHave, stocksMA = 100, {}, {}, {}
    for i in lines:
        el = i.rstrip().split()
        stocks[el[0]] = map(float, el[1:])
        stocksHave[el[0]] = 0
        stocksMA[el[0]] = []

    sellingRange = 10
    windowSize = 5
    for i in xrange(sellingRange):
        print 'Current day :', i
        for name in stocks:
            if len(stocksMA[name]) < windowSize:
                # populate historical data to later use it for MA
                stocksMA[name].append(stocks[name][i])
                print '  ', name, stocks[name][i]
            else:
                print name
                MA = sum(stocksMA[name]) / float(windowSize)
                print '  Current price :', stocks[name][i]
                print '  Average price :', MA
                stocksMA[name].pop(0)
                stocksMA[name].append(stocks[name][i])
                print

    return 1



money = 100
stocksPortfolio = {'A': 0, 'B': 0, 'C': 0}
stocksPrices = {'A': 50.8, 'B': 92.3, 'C': 28.9}
stocksMA = {'A': 56.5, 'B': 95.9, 'C': 48.9}
buyingStocksForPortfolio(money, stocksPortfolio, stocksPrices, stocksMA)



#analyze()
#strategyAttempt()