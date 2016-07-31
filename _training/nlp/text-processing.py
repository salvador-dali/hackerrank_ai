"""
https://www.hackerrank.com/challenges/a-text-processing-warmup/submissions/code/13713062
nothing interesting, just a lot of regular expressions and logic
"""

import re
import string

def countArticles(text):
    arr = text.lower().translate(None, string.punctuation).split()

    num = 0
    num += len(re.findall(r'\d{1,2}/\d{1,2}/\d{2}', text))
    num += len(re.findall(r'\d{1,2}/\d{1,2}/\d{4}', text))

    months = {'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'jan', 'feb', 'mar', 'apr', 'may', 'june', 'july', 'aug', 'sept', 'oct', 'nov', 'dec'}
    days = set(map(str, range(1, 32)) + ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st'])
    years = set(map(str, range(500, 2100)) + map(lambda x: str(x) +'th', range(500, 2100)))

    for i in xrange(len(arr)):
        if 0 < i < len(arr) - 1 and arr[i] in months:
            if arr[i - 1] in days and arr[i + 1] in years:
                num += 1
            elif arr[i - 2] in days and arr[i - 1] == 'of' and arr[i + 1] in years:
                num += 1

    for i in xrange(len(arr)):
        if i < len(arr) - 3 and arr[i] in months:
            if arr[i + 1] in days and arr[i + 2] in years:
                num += 1

    return [arr.count('a'), arr.count('an'), arr.count('the'), num]

for _ in xrange(input() - 1):
    arr = countArticles(raw_input())
    raw_input()
    for i in arr:
        print i

arr = countArticles(raw_input())
for i in arr:
    print i