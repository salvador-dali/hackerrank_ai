"""
https://www.hackerrank.com/challenges/url-hashtag-segmentation
straight forward solution.
"""

def stripCrap(s):
    if s[0] == '#':
        return s[1:]

    arr = s.split('.')
    if arr[0] == 'www':
        return arr[1]
    return arr[0]

def toWords(s):
    s = stripCrap(s)
    result = []

    while s:
        found = False

        if s[0].isdigit():
            number = ""
            for i in xrange(0, len(s)):
                if s[i].isdigit():
                    number += s[i]

            result.append(number)
            s = s[len(number):]

        for i in words:
            if s.startswith(i):
                result.append(i)
                found = True
                break

        if not found:
            return result
        s = s[len(i):]

    return result

import re

digits = re.compile("^[0-9]*(\.[0-9]+)?$")
words = set(line.rstrip('\n').strip().lower for line in open('words.txt'))
words.union({'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety', 'hundred', 'thousand', 'million', 'billion', 'trillion', 'zillion', 'internet', 'bible', 'a', 'i'})

def seperate(s):
    if not len(s):
        return []

    for i in xrange(len(s), 0, -1):
        if s[0:i] in words or digits.match(s[0:i]):
            rest = seperate(s[i:])
            if not rest:
                return [s[0:i]] + rest

    return None


for _ in xrange(input()):
    s = stripCrap(raw_input().lower())
    ans = seperate(s)
    print " ".join(ans) if ans else s