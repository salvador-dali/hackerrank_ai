# http://nbviewer.ipython.org/url/norvig.com/ipython/TSPv3.ipynb

from datetime import datetime
startTime = datetime.now()

def helpers():
    # finds a bot position
    # 3 6
    bot = list(map(int, raw_input().split()))

    # get grid for the bot
    grid = [raw_input() for i in xrange(int(raw_input()))]


# find the best next move in a 2D grid
# from your position to the target
# --------
# --Y-----
# --------
# -----T--
#
# you specify the position in [y, x]
# example move2DGrid([1, 2], [3, 5])
def move2DGrid(you, target):
    x, y = target[1] - you[1], target[0] - you[0]
    if x == 0 and y == 0:
        return 'CLEAN'
    if x > 0:
        return 'RIGHT'
    elif x < 0:
        return 'LEFT'
    else:
        if y > 0:
            return 'DOWN'
        elif y < 0:
            return 'UP'


# return manhattan distance between two points
def manhattan(A, B):
    return abs(A[0] - B[0]) + abs(A[1] - B[1])

# finds the best route to pass through all the points from starting position
# where the distance between two points is defined by metric (manhattan or euclid)
#
# this is NP problem, so for big numbers it use approximation
def TSP(start, points, metric):
    from random import shuffle
    # calculates the total distance between the all the points in the route
    def totalDistance(points):
        distance = 0
        for i in xrange(len(points) - 1):
            distance += metric(points[i], points[i + 1])
        return distance

    # Checks all permutations and selects the best one takes O(N!)
    # N = 8 takes 0.1 second, N = 9 takes 1.5 seconds
    def bruteforce(start, points):
        from itertools import permutations
        smallestDistance, l = 10**10, len(points)
        for i in permutations(points):
            # for all possible permutations it calculates the distance and checks
            # whether this is the smallest distance
            tour = [start] + list(i)
            distance = totalDistance(tour)
            if distance < smallestDistance:
                bestTour, smallestDistance = i, distance

        return bestTour

    # selects the path based on the nearest neighbor.
    def greedyNearestNeighbor(start, points):
        def nearestPoint(myPoint, arr):
            smallestDist, nearest = 10**10, None
            for i in arr:
                dist = metric(myPoint, i)
                if dist < smallestDist:
                    smallestDist, nearest = dist, i

            return nearest

        path = [start]
        dictionary = {str(i[0]) + '_' + str(i[1]): i for i in points}   # python does not allow hashing lists
        while dictionary:
            bestPoint = nearestPoint(path[-1], dictionary.values())
            path.append(bestPoint)
            del dictionary[str(bestPoint[0]) + '_' + str(bestPoint[1])]

        return path

    # check the greedy solution for all possible starting positions
    def allGreedyNearestNeighbor(start, points):
        smallestDistance = 10**10
        for i in xrange(len(points)):
            tour = [start] + greedyNearestNeighbor(points[i], points[:i] + points[i + 1:])
            dist = totalDistance(tour)
            if dist < smallestDistance:
                smallestDistance, smallestPath = dist, tour

        return smallestPath

    # find the local optima for a random shuffle N^2
    def localOptima(start, points):
        arr, l = list(points), len(points) + 1
        shuffle(arr)
        arr.insert(0, start)
        bestDistance, bestPath = totalDistance(arr), arr

        for i in xrange(1, l - 1):
            for j in xrange(i + 1, l):
                candidate = bestPath[0:i] + bestPath[i:j + 1][::-1] + bestPath[j + 1:]
                candidateDist = totalDistance(candidate)
                if candidateDist < bestDistance:
                    bestDistance, bestPath = candidateDist, candidate

        return bestDistance, bestPath

    pointsNum = len(points)
    if pointsNum < 9:
        # if number of points is small - we can use bruteforce
        return bruteforce(start, points)
    else:
        # generate a lot of random paths and try to converge to local minima, also checks greedy solution
        smallestPath = allGreedyNearestNeighbor(start, points)
        smallestDistance = totalDistance(smallestPath)

        for i in xrange(550000 / (pointsNum**2)):   # to make the time of execution approximately 3 sec
            tmpDistance, tmpPath = localOptima(start, points)
            if tmpDistance < smallestDistance:
                smallestPath, smallestDistance = tmpPath, tmpDistance

        return smallestPath[1:]






points = [[1, 1], [1, 4], [2, 3], [5, 2], [6, 2], [6, 3], [10, 9], [4, 9], [7, 7], [7, 8], [7, 1], [2, 4], [5, 1], [9, 3], [14, 2], [1, 8], [4, 4], [8, 2], [6, 6], [2, 2], [9, 13]]
#points = [[1, 1], [1, 4], [2, 3], [5, 2], [6, 2], [6, 3], [10, 9], [4, 9], [7, 7]]
print TSP([0, 0], points, manhattan)
print datetime.now() - startTime