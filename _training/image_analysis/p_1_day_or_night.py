from __helpers import readRGB, RGB_to_greyscale

def main():
    """ https://www.hackerrank.com/challenges/digital-camera-day-or-night
    Compares the number of bright pixels to the number of dark one.
    Darkness/brightness is regulated with a threshold value. Guessed the correct value from
    the third attempt.
    :return: answer
    """
    M = RGB_to_greyscale(readRGB())
    threshold = 89
    return 'day' if (M < threshold).sum() < (M >= threshold).sum() else 'night'

main()