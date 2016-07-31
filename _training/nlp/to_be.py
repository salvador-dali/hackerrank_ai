"""
Just get 3 words before an after. Guess the correct tense and create a lot of rules
"""
def pluralize(word):
    if word[-1] == 'y' and sum(map(word.lower().count, "aeiou")) >= 2:
        return word[:-1] + 'ies'
    if word[-2:] == 'fe':
        return word[:-2] + 'ves'
    return word + 's'

def past(word):
    if word[-1] == 'e':
        return word + 'd'

    return word + 'ed'

def ing(word):
    if word[-1] == 'e':
        return word[:-1] + 'ing'
    return word + 'ing'

nouns_singular = [line.rstrip('\n') for line in open('__data/english_nouns.txt')] + ['berbera', 'zeila', 'honor', 'patent', 'x-ray', 'korea', 'pyongyang', 'detonation']
nouns_plural = [pluralize(i) for i in nouns_singular] + [line.rstrip('\n') for line in open('__data/english_nouns_irregular_plural.txt')]
nouns_singular += [line.rstrip('\n') for line in open('__data/english_nouns_irregular.txt')]

verbs_1 = [line.rstrip('\n') for line in open('__data/english_verbs_regular.txt')]
verbs_2 = [past(i) for i in verbs_1] + [line.rstrip('\n') for line in open('__data/english_verbs_irregular_2.txt')]
verbs_3 = [line.rstrip('\n') for line in open('__data/english_verbs_irregular_3.txt')]
verbs_4 = [ing(i) for i in verbs_1]

set_nouns_s = set(nouns_singular)
set_nouns_p = set(nouns_plural)
set_verbs_1 = set(verbs_1)
set_verbs_2 = set(verbs_2)
set_verbs_3 = set(verbs_3)
set_verbs_4 = set(verbs_4)

def whatIsTheWord_first(word):
    if word in set_nouns_s:
        return 'NOUN_S'
    if word in set_nouns_p:
        return 'NOUN_P'
    if word.isdigit():
        return 'NOUN_S'
    if word in set_verbs_3:
        return 'VERB_3'
    if word in set_verbs_1:
        return 'VERB_1'
    if word in set_verbs_2:
        return 'VERB_3'
    if word in set_verbs_4:
        return 'VERB_ing'

    return None

def whatIsTheWord_second(word):
    if word in set_verbs_3:
        return 'VERB_3'
    if word in set_verbs_1:
        return 'VERB_1'
    if word in set_verbs_2:
        return 'VERB_3'
    if word in set_verbs_4:
        return 'VERB_ing'
    if word in set_nouns_s:
        return 'NOUN_S'
    if word in set_nouns_p:
        return 'NOUN_P'
    if word.isdigit():
        return 'NOUN_S'

    return None

def analysis(text):
    length = 3
    arr = text.lower().translate(None, '.,?!;:&[]()*_"').split()
    for i in xrange(len(arr)):
        if arr[i] == '----':
            s = i - length if i - length >= 0 else 0
            e = i + length + 1 if i + length < len(arr) else len(arr)

            prev_ = [whatIsTheWord_first(j) for j in arr[s:i] if whatIsTheWord_first(j)]
            next_ = [whatIsTheWord_second(j) for j in arr[i+1:e] if whatIsTheWord_second(j)]

            if prev_.count('NOUN_S') >= 2:
                prev_word = 'NOUN_P'
            elif 'NOUN_P' in prev_:
                prev_word = 'NOUN_P'
            elif prev_.count('NOUN_S') == 1:
                prev_word = 'NOUN_S'
            elif 'VERB_3' in prev_:
                prev_word = 'VERB_3'
            else:
                prev_word = prev_

            if 'VERB_ing' in next_:
                next_word = 'VERB_ing'
            elif 'VERB_3' in next_:
                next_word = 'VERB_3'
            elif 'NOUN_S' in next_:
                next_word = 'NOUN_S'
            elif 'NOUN_P' in next_:
                next_word = 'NOUN_P'
            elif 'VERB_1' in next_:
                next_word = 'VERB_1'
            else:
                next_word = next_

            result = 'were'
            if prev_word == 'NOUN_P' and next_word == 'VERB_ing':
                result = 'were'
            elif prev_word == 'NOUN_S' and next_word == 'VERB_3':
                result = 'was'
            elif prev_word == 'NOUN_P' and next_word == 'VERB_3':
                result = 'were'
            elif prev_word == 'NOUN_S' and next_word == 'NOUN_S':
                result = 'is'
            elif prev_word == 'NOUN_P' and next_word == 'NOUN_P':
                result = 'were'
            elif prev_word == 'NOUN_S' and next_word == []:
                result = 'is'
            elif prev_word == 'NOUN_P' and next_word == []:
                result = 'were'
            elif next_word == 'VERB_1':
                result = 'am'
            elif prev_word == 'NOUN_S' and next_word == 'VERB_ing':
                result = 'be'
            elif prev_word == [] and next_word == 'VERB_3':
                result = 'being'
            elif prev_word == [] and next_word == 'VERB_3':
                result = 'being'
            elif prev_word == 'VERB_3' and next_word == 'VERB_3':
                result = 'being'

            if arr[s:i][-1] in {'have', 'has'} and next_word == 'VERB_3':
                result = 'been'

            print result

analysis(text)