import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from collections import defaultdict
from p_2_captcha_cracker_solution import matrixTransform, predictDigit

os.chdir("data/captcha_cracker")

def showAllImages():
    fig, current = plt.figure(), 0
    for file_name in glob.glob("input/*.txt"):
        with open(file_name) as f:
            f.next()
            M = np.array([[int(i.split(',')[0]) for i in line.strip('\n').split()] for line in f])
            M = matrixTransform(M)
            fig.add_subplot(5, 5, current).imshow(M, cmap=cm.Greys_r)
            fig.tight_layout()
            current += 1

    plt.tight_layout()
    plt.show()
    return

def showLettersOfImage(name, isShow=False):
    digits, current = [], 0
    if isShow:
        fig = plt.figure()
    with open('input/input' + name + '.txt') as f:
        f.next()
        M = np.array([[int(i.split(',')[0]) for i in line.strip('\n').split()] for line in f])
        M = matrixTransform(M)
        for i in xrange(5):
            digit = M[:, i*9:(i+1) * 9]
            if isShow:
                current += 1
                fig.add_subplot(1, 5, current).imshow(digit, cmap=cm.Greys_r)
            else:
                digits.append(digit)

    if isShow:
        plt.show()
    return digits

def collectStatistics():
    """
    Runs through all images, for every image it checks the corresponding answer
    then divides the image into digits and collects statistics
    :return: dictionary of statistics which will be used by predictDigit
    """
    digits_stats = defaultdict(list)
    for i in xrange(25):
        file_name = ('0' + str(i))[-2:]
        with open('output/output' + file_name + '.txt') as file_output:
            with open('input/input' + file_name + '.txt') as file_input:
                digits_l = file_output.read().strip('\n')
                digits_m = showLettersOfImage(file_name)
                for j in xrange(len(digits_m)):
                    digit = digits_m[j]
                    digits_stats[digits_l[j]].append(np.average(digit, axis=1)[1:-1])

    predictions = {}
    for l, stats in digits_stats.iteritems():
        predictions[l] = list(np.average(np.array(stats), axis=0))

    return predictions

def predict(file_name):
    """Make the actual prediction. Slightly modified version would be used in Solver file
    """
    for file_name in glob.glob("input/" + file_name):
        result = ''
        with open(file_name) as f:
            f.next()
            M = matrixTransform(np.array([[int(i.split(',')[0]) for i in line.strip('\n').split()] for line in f]))
            for i in xrange(5):
                digit = M[:, i*9:(i+1) * 9]
                digit_stats = np.average(digit, axis=1)[1:-1]
                result += predictDigit(digit_stats, digit)

        print result
    return


predict('input03.txt')


